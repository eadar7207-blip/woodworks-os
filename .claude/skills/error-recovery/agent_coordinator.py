"""Agent team coordinator for autonomous error recovery."""
import json
import time
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from database import RecoveryDatabase
from recovery_strategies import ErrorAnalyzer, FailureClassifier


class ErrorAnalyzerAgent:
    """Analyzes errors and recommends recovery strategies."""

    def __init__(self, db: RecoveryDatabase):
        self.db = db
        self.analyzer = ErrorAnalyzer()
        self.classifier = FailureClassifier()

    def diagnose(self, execution_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Diagnose failure and return recovery recommendation.

        Returns:
        {
            "execution_id": str,
            "error_type": str,
            "error_message": str,
            "failed_step": dict,
            "recommended_strategy": str,
            "confidence": float,
            "is_recoverable": bool,
            "max_attempts": int,
        }
        """
        error_message = execution_data.get("error_message", "Unknown error")
        steps = execution_data.get("steps", [])

        # Find failed step
        failed_step = None
        for step in steps:
            if step.get("status") == "failed":
                failed_step = step
                break

        if failed_step and failed_step.get("error_message"):
            error_message = failed_step.get("error_message")

        # Classify error
        error_type = self.classifier.classify(error_message)

        # Recommend strategy
        strategy_name, confidence = self.analyzer.analyze(error_message)

        # Determine if recoverable
        is_recoverable = self.classifier.should_retry(error_type) and confidence > 0.3

        return {
            "execution_id": execution_data.get("execution_id"),
            "error_type": error_type,
            "error_message": error_message,
            "failed_step": failed_step,
            "recommended_strategy": strategy_name,
            "confidence": confidence,
            "is_recoverable": is_recoverable,
            "max_attempts": 5,
        }


class RecoveryExecutorAgent:
    """Executes recovery strategies and re-runs failed steps."""

    def __init__(self, db: RecoveryDatabase):
        self.db = db
        self.analyzer = ErrorAnalyzer()

    def execute_recovery(
        self,
        execution_id: str,
        step_data: Dict[str, Any],
        diagnosis: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Execute recovery strategy and track attempt.

        Returns:
        {
            "attempt_id": str,
            "execution_id": str,
            "strategy_used": str,
            "status": "success" | "failed",
            "result_message": str,
            "modified_params": dict,
            "duration_ms": int,
        }
        """
        strategy_name = diagnosis["recommended_strategy"]
        original_params = step_data.get("input_data", {})

        # Get strategy instance
        strategy = self.analyzer.get_strategy(strategy_name)
        if not strategy:
            return {
                "status": "failed",
                "result_message": f"Strategy {strategy_name} not found",
            }

        start_time = time.time()

        # Execute recovery
        try:
            success, modified_params, result_message = strategy.recover(
                execution_id,
                step_data,
                original_params,
            )
        except Exception as e:
            success = False
            modified_params = {}
            result_message = f"Recovery execution failed: {str(e)}"

        duration_ms = int((time.time() - start_time) * 1000)

        # Create recovery attempt record
        attempt_number = len(
            self.db.get_recovery_attempts_for_execution(execution_id)
        ) + 1

        attempt_id = self.db.create_recovery_attempt(
            execution_id=execution_id,
            step_id=step_data.get("id"),
            attempt_number=attempt_number,
            strategy_used=strategy_name,
            error_type=diagnosis["error_type"],
            error_message=diagnosis["error_message"],
            original_params=original_params,
            modified_params=modified_params,
        )

        # Update attempt record with result
        status = "success" if success else "failed"
        self.db.update_recovery_attempt(
            attempt_id=attempt_id,
            status=status,
            result_message=result_message,
            duration_ms=duration_ms,
        )

        return {
            "attempt_id": attempt_id,
            "execution_id": execution_id,
            "strategy_used": strategy_name,
            "status": status,
            "result_message": result_message,
            "modified_params": modified_params,
            "duration_ms": duration_ms,
        }


class ValidationAgent:
    """Validates recovery success and determines next steps."""

    def __init__(self, db: RecoveryDatabase):
        self.db = db

    def validate(
        self,
        execution_id: str,
        recovery_result: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Validate recovery and determine if we should retry with different strategy.

        Returns:
        {
            "is_resolved": bool,
            "confidence": float,
            "next_action": "success" | "retry_different_strategy" | "escalate",
            "message": str,
        }
        """
        attempts = self.db.get_recovery_attempts_for_execution(execution_id)

        if recovery_result["status"] == "success":
            return {
                "is_resolved": True,
                "confidence": 0.95,
                "next_action": "success",
                "message": recovery_result["result_message"],
            }

        # Check if we've exhausted attempts
        if len(attempts) >= 5:
            return {
                "is_resolved": False,
                "confidence": 0.0,
                "next_action": "escalate",
                "message": "Max recovery attempts (5) exhausted. Manual intervention required.",
            }

        # Otherwise, suggest trying different strategy
        return {
            "is_resolved": False,
            "confidence": 0.5,
            "next_action": "retry_different_strategy",
            "message": f"Recovery attempt {len(attempts)} failed. Will try different strategy.",
        }


class ErrorRecoveryCoordinator:
    """Coordinates error recovery agent team."""

    def __init__(self, db_path: str = "executor.db"):
        self.db = RecoveryDatabase(db_path)
        self.error_analyzer = ErrorAnalyzerAgent(self.db)
        self.recovery_executor = RecoveryExecutorAgent(self.db)
        self.validator = ValidationAgent(self.db)

    def recover_failure(self, execution_id: str) -> Dict[str, Any]:
        """
        Main entry point: detect, diagnose, and recover from failure.

        Workflow:
        1. Load execution data
        2. ErrorAnalyzer diagnoses the failure
        3. RecoveryExecutor attempts recovery
        4. Validator checks if recovery succeeded
        5. Return summary

        Returns:
        {
            "execution_id": str,
            "diagnosis": dict,
            "recovery_result": dict,
            "validation": dict,
            "success": bool,
        }
        """
        # Load execution data
        execution_data = self.db.get_execution_with_steps(execution_id)
        if not execution_data:
            return {
                "success": False,
                "error": f"Execution {execution_id} not found",
            }

        # Step 1: Diagnose
        diagnosis = self.error_analyzer.diagnose(execution_data)

        if not diagnosis["is_recoverable"]:
            return {
                "execution_id": execution_id,
                "diagnosis": diagnosis,
                "success": False,
                "message": "Error is not recoverable with available strategies",
            }

        # Step 2: Execute recovery
        failed_step = diagnosis["failed_step"]
        recovery_result = self.recovery_executor.execute_recovery(
            execution_id,
            failed_step,
            diagnosis,
        )

        # Step 3: Validate
        validation = self.validator.validate(execution_id, recovery_result)

        # Determine success
        success = validation["is_resolved"]

        # Update failure pattern for learning
        error_pattern = self._extract_pattern(diagnosis["error_message"])
        self.db.update_failure_pattern(
            error_pattern=error_pattern,
            error_type=diagnosis["error_type"],
            recovery_status=recovery_result["status"],
            recommended_strategy=diagnosis["recommended_strategy"],
        )

        return {
            "execution_id": execution_id,
            "diagnosis": diagnosis,
            "recovery_result": recovery_result,
            "validation": validation,
            "success": success,
            "message": validation["message"],
        }

    def monitor_for_failures(self, max_age_hours: int = 1) -> Dict[str, Any]:
        """
        Monitor for new failures and attempt recovery.

        Returns statistics on failures found and recovery attempts.
        """
        # Get recent failed executions
        failed_executions = self.db.get_failed_executions(limit=20)

        results = {
            "timestamp": datetime.utcnow().isoformat(),
            "failures_checked": len(failed_executions),
            "recovery_attempts": [],
            "summary": {
                "total_checked": 0,
                "recovered": 0,
                "unrecoverable": 0,
                "escalated": 0,
            },
        }

        for failed_exec in failed_executions:
            execution_id = failed_exec["execution_id"]

            # Check if already has recovery attempts
            attempts = self.db.get_recovery_attempts_for_execution(execution_id)
            if attempts:
                continue  # Already being recovered

            # Try recovery
            recovery_summary = self.recover_failure(execution_id)

            results["recovery_attempts"].append({
                "execution_id": execution_id,
                "success": recovery_summary.get("success", False),
                "message": recovery_summary.get("message"),
            })

            if recovery_summary.get("success"):
                results["summary"]["recovered"] += 1
            elif "escalate" in recovery_summary.get("validation", {}).get("next_action", ""):
                results["summary"]["escalated"] += 1
            else:
                results["summary"]["unrecoverable"] += 1

            results["summary"]["total_checked"] += 1

        return results

    def get_status(self) -> Dict[str, Any]:
        """Get current recovery status and statistics."""
        failed_executions = self.db.get_failed_executions(limit=100)
        all_attempts = []

        for failed_exec in failed_executions:
            attempts = self.db.get_recovery_attempts_for_execution(
                failed_exec["execution_id"]
            )
            all_attempts.extend(attempts)

        successful_attempts = sum(1 for a in all_attempts if a["status"] == "success")
        total_attempts = len(all_attempts)
        success_rate = (
            successful_attempts / total_attempts if total_attempts > 0 else 0
        )

        return {
            "timestamp": datetime.utcnow().isoformat(),
            "failed_executions": len(failed_executions),
            "total_recovery_attempts": total_attempts,
            "successful_recoveries": successful_attempts,
            "success_rate": success_rate,
            "recent_failures": [
                {
                    "execution_id": e["execution_id"],
                    "workflow_id": e["workflow_id"],
                    "error": e["error_message"],
                    "created_at": e["created_at"],
                }
                for e in failed_executions[:10]
            ],
        }

    def get_config(self) -> Dict[str, Any]:
        """Get recovery configuration."""
        default_config = {
            "max_retry_attempts": 5,
            "backoff_strategy": "exponential",
            "backoff_times": [2, 4, 8],
            "monitor_interval_seconds": 120,
            "failure_age_threshold_hours": 24,
            "auto_recovery_enabled": True,
            "notification_on_success": True,
            "notification_on_exhausted": True,
        }

        stored_config = self.db.get_all_config()
        return {**default_config, **stored_config}

    def set_config(self, config: Dict[str, Any]):
        """Update recovery configuration."""
        for key, value in config.items():
            self.db.set_config(key, value)

    @staticmethod
    def _extract_pattern(error_message: str) -> str:
        """Extract a pattern from error message for aggregation."""
        # Remove specific values, keep patterns
        import re
        pattern = re.sub(r'"[^"]*"', '"{value}"', error_message)
        pattern = re.sub(r"'[^']*'", "'{value}'", pattern)
        pattern = re.sub(r"\d+", "{number}", pattern)
        return pattern[:100]  # Limit length for storage
