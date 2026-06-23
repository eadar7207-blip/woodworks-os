"""Comprehensive tests for error recovery skill."""
import unittest
import sqlite3
import json
import tempfile
import os
from pathlib import Path
from datetime import datetime

from database import RecoveryDatabase
from recovery_strategies import (
    ErrorAnalyzer,
    FailureClassifier,
    RetryStrategy,
    RetryWithModifiedParamsStrategy,
    SkipStepStrategy,
    ReduceScopeStrategy,
    FallbackActionStrategy,
)
from agent_coordinator import (
    ErrorAnalyzerAgent,
    RecoveryExecutorAgent,
    ValidationAgent,
    ErrorRecoveryCoordinator,
)


class TestRecoveryDatabase(unittest.TestCase):
    """Test database layer."""

    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.temp_db.close()
        self.db = RecoveryDatabase(self.temp_db.name)

    def tearDown(self):
        os.unlink(self.temp_db.name)

    def test_create_recovery_attempt(self):
        """Test creating recovery attempt record."""
        attempt_id = self.db.create_recovery_attempt(
            execution_id="exec-123",
            step_id="step-1",
            attempt_number=1,
            strategy_used="RETRY",
            error_type="TRANSIENT",
            error_message="Timeout occurred",
        )

        self.assertIsNotNone(attempt_id)

        attempts = self.db.get_recovery_attempts_for_execution("exec-123")
        self.assertEqual(len(attempts), 1)
        self.assertEqual(attempts[0]["strategy_used"], "RETRY")

    def test_update_recovery_attempt(self):
        """Test updating recovery attempt."""
        attempt_id = self.db.create_recovery_attempt(
            execution_id="exec-124",
            step_id="step-1",
            attempt_number=1,
            strategy_used="RETRY",
            error_type="TRANSIENT",
            error_message="Timeout",
        )

        self.db.update_recovery_attempt(
            attempt_id=attempt_id,
            status="success",
            result_message="Retry succeeded",
            duration_ms=500,
        )

        attempts = self.db.get_recovery_attempts_for_execution("exec-124")
        self.assertEqual(attempts[0]["status"], "success")
        self.assertEqual(attempts[0]["result_message"], "Retry succeeded")

    def test_failure_pattern_tracking(self):
        """Test failure pattern aggregation."""
        self.db.update_failure_pattern(
            error_pattern="timeout error",
            error_type="TRANSIENT",
            recovery_status="success",
            recommended_strategy="RETRY",
        )

        pattern = self.db.get_failure_pattern("timeout error")
        self.assertIsNotNone(pattern)
        self.assertEqual(pattern["successful_recoveries"], 1)

        # Update again
        self.db.update_failure_pattern(
            error_pattern="timeout error",
            error_type="TRANSIENT",
            recovery_status="failed",
            recommended_strategy="RETRY",
        )

        pattern = self.db.get_failure_pattern("timeout error")
        self.assertEqual(pattern["total_occurrences"], 2)
        self.assertEqual(pattern["failed_recoveries"], 1)


class TestRecoveryStrategies(unittest.TestCase):
    """Test recovery strategy implementations."""

    def test_retry_strategy_transient_detection(self):
        """Test RETRY strategy detects transient errors."""
        strategy = RetryStrategy()

        # Should match transient errors
        score = strategy.analyze_error("Connection timeout occurred")
        self.assertGreater(score, 0.5)

        score = strategy.analyze_error("Service temporarily unavailable")
        self.assertGreater(score, 0.5)

    def test_retry_modified_params_detection(self):
        """Test RETRY_WITH_MODIFIED_PARAMS detects config errors."""
        strategy = RetryWithModifiedParamsStrategy()

        score = strategy.analyze_error("Invalid email address format")
        self.assertGreater(score, 0.5)

        score = strategy.analyze_error("Bad parameter value")
        self.assertGreater(score, 0.5)

    def test_skip_step_strategy(self):
        """Test SKIP_STEP strategy identifies non-critical steps."""
        strategy = SkipStepStrategy()

        score = strategy.analyze_error("Failed to log activity to CRM")
        self.assertGreater(score, 0.3)

    def test_reduce_scope_strategy_detection(self):
        """Test REDUCE_SCOPE detects size-related errors."""
        strategy = ReduceScopeStrategy()

        score = strategy.analyze_error("Payload too large")
        self.assertGreater(score, 0.5)

        score = strategy.analyze_error("Request exceeds maximum size")
        self.assertGreater(score, 0.5)

    def test_fallback_action_detection(self):
        """Test FALLBACK_ACTION detects skill not found."""
        strategy = FallbackActionStrategy()

        score = strategy.analyze_error("Skill 'email' not found")
        self.assertGreater(score, 0.5)

    def test_strategy_recovery(self):
        """Test strategy recovery execution."""
        strategy = RetryWithModifiedParamsStrategy()

        success, params, message = strategy.recover(
            execution_id="exec-1",
            step_data={"step_name": "send_email"},
            original_params={"email": "  TEST@EXAMPLE.COM  "},
        )

        self.assertTrue(success)
        self.assertIn("test@example.com", params.get("email", "").lower())


class TestErrorAnalyzer(unittest.TestCase):
    """Test error analysis."""

    def setUp(self):
        self.analyzer = ErrorAnalyzer()

    def test_analyze_transient_error(self):
        """Test analyzer selects RETRY for transient errors."""
        strategy, score = self.analyzer.analyze("Connection timeout")
        self.assertEqual(strategy, "RETRY")
        self.assertGreater(score, 0.5)

    def test_analyze_config_error(self):
        """Test analyzer selects RETRY_WITH_MODIFIED_PARAMS for config errors."""
        strategy, score = self.analyzer.analyze("Invalid email address")
        self.assertEqual(strategy, "RETRY_WITH_MODIFIED_PARAMS")
        self.assertGreater(score, 0.5)

    def test_analyze_scope_error(self):
        """Test analyzer selects REDUCE_SCOPE for size errors."""
        strategy, score = self.analyzer.analyze("Payload exceeds maximum size")
        self.assertEqual(strategy, "REDUCE_SCOPE")
        self.assertGreater(score, 0.5)

    def test_get_strategy(self):
        """Test retrieving strategy instances."""
        strategy = self.analyzer.get_strategy("RETRY")
        self.assertIsNotNone(strategy)
        self.assertEqual(strategy.name, "RETRY")


class TestFailureClassifier(unittest.TestCase):
    """Test error classification."""

    def test_classify_transient(self):
        """Test classifying transient errors."""
        error_type = FailureClassifier.classify("Connection timeout")
        self.assertEqual(error_type, "TRANSIENT")

    def test_classify_configuration(self):
        """Test classifying configuration errors."""
        error_type = FailureClassifier.classify("Invalid parameter format")
        self.assertEqual(error_type, "CONFIGURATION")

    def test_classify_skill_error(self):
        """Test classifying skill errors."""
        error_type = FailureClassifier.classify("Skill 'email' not found")
        self.assertEqual(error_type, "SKILL_ERROR")

    def test_classify_scope_error(self):
        """Test classifying scope errors."""
        error_type = FailureClassifier.classify("Input too large for processing")
        self.assertEqual(error_type, "SCOPE_ERROR")

    def test_should_retry(self):
        """Test retriability determination."""
        self.assertTrue(FailureClassifier.should_retry("TRANSIENT"))
        self.assertTrue(FailureClassifier.should_retry("CONFIGURATION"))
        self.assertTrue(FailureClassifier.should_retry("SKILL_ERROR"))
        self.assertFalse(FailureClassifier.should_retry("PERMISSION_ERROR"))


class TestErrorAnalyzerAgent(unittest.TestCase):
    """Test error analyzer agent."""

    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.temp_db.close()
        self.db = RecoveryDatabase(self.temp_db.name)
        self.agent = ErrorAnalyzerAgent(self.db)

    def tearDown(self):
        os.unlink(self.temp_db.name)

    def test_diagnose_transient_error(self):
        """Test diagnosing transient error."""
        execution_data = {
            "execution_id": "exec-1",
            "error_message": "Connection timeout",
            "steps": [
                {
                    "id": "step-1",
                    "status": "failed",
                    "error_message": "Connection timeout",
                }
            ],
        }

        diagnosis = self.agent.diagnose(execution_data)

        self.assertEqual(diagnosis["error_type"], "TRANSIENT")
        self.assertEqual(diagnosis["recommended_strategy"], "RETRY")
        self.assertTrue(diagnosis["is_recoverable"])

    def test_diagnose_config_error(self):
        """Test diagnosing configuration error."""
        execution_data = {
            "execution_id": "exec-2",
            "error_message": "Invalid email format",
            "steps": [
                {
                    "id": "step-1",
                    "status": "failed",
                    "error_message": "Invalid email format",
                }
            ],
        }

        diagnosis = self.agent.diagnose(execution_data)

        self.assertEqual(diagnosis["error_type"], "CONFIGURATION")
        self.assertTrue(diagnosis["is_recoverable"])


class TestRecoveryExecutorAgent(unittest.TestCase):
    """Test recovery executor agent."""

    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.temp_db.close()
        self.db = RecoveryDatabase(self.temp_db.name)
        self.agent = RecoveryExecutorAgent(self.db)

    def tearDown(self):
        os.unlink(self.temp_db.name)

    def test_execute_retry_recovery(self):
        """Test executing RETRY strategy."""
        diagnosis = {
            "recommended_strategy": "RETRY",
            "error_type": "TRANSIENT",
            "error_message": "Connection timeout",
        }

        step_data = {
            "id": "step-1",
            "step_name": "fetch_data",
            "input_data": {"url": "https://api.example.com/data"},
        }

        result = self.agent.execute_recovery("exec-1", step_data, diagnosis)

        self.assertEqual(result["strategy_used"], "RETRY")
        self.assertIn("attempt", result["result_message"].lower())


class TestValidationAgent(unittest.TestCase):
    """Test validation agent."""

    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.temp_db.close()
        self.db = RecoveryDatabase(self.temp_db.name)
        self.agent = ValidationAgent(self.db)

    def tearDown(self):
        os.unlink(self.temp_db.name)

    def test_validate_success(self):
        """Test validation of successful recovery."""
        recovery_result = {
            "status": "success",
            "result_message": "Recovery succeeded",
        }

        validation = self.agent.validate("exec-1", recovery_result)

        self.assertTrue(validation["is_resolved"])
        self.assertEqual(validation["next_action"], "success")

    def test_validate_exhausted_attempts(self):
        """Test validation when max attempts reached."""
        # Create 5 failed attempts
        for i in range(5):
            self.db.create_recovery_attempt(
                execution_id="exec-2",
                step_id="step-1",
                attempt_number=i + 1,
                strategy_used="RETRY",
                error_type="TRANSIENT",
                error_message="Timeout",
            )

        recovery_result = {
            "status": "failed",
            "result_message": "Recovery failed",
        }

        validation = self.agent.validate("exec-2", recovery_result)

        self.assertFalse(validation["is_resolved"])
        self.assertEqual(validation["next_action"], "escalate")


class TestErrorRecoveryCoordinator(unittest.TestCase):
    """Test main coordinator."""

    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.temp_db.close()
        self.coordinator = ErrorRecoveryCoordinator(self.temp_db.name)

    def tearDown(self):
        os.unlink(self.temp_db.name)

    def test_get_status(self):
        """Test getting recovery status."""
        status = self.coordinator.get_status()

        self.assertIn("total_recovery_attempts", status)
        self.assertIn("success_rate", status)
        self.assertIn("recent_failures", status)

    def test_get_config(self):
        """Test getting configuration."""
        config = self.coordinator.get_config()

        self.assertIn("max_retry_attempts", config)
        self.assertIn("backoff_strategy", config)
        self.assertEqual(config["max_retry_attempts"], 5)

    def test_set_config(self):
        """Test updating configuration."""
        new_config = {"max_retry_attempts": 3}
        self.coordinator.set_config(new_config)

        config = self.coordinator.get_config()
        self.assertEqual(config["max_retry_attempts"], 3)

    def test_extract_pattern(self):
        """Test error pattern extraction."""
        pattern = ErrorRecoveryCoordinator._extract_pattern(
            'Invalid email "test@example.com" provided'
        )

        self.assertNotIn("test@example.com", pattern)
        self.assertIn("{value}", pattern)


class TestIntegration(unittest.TestCase):
    """Integration tests."""

    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.temp_db.close()
        self.coordinator = ErrorRecoveryCoordinator(self.temp_db.name)

    def tearDown(self):
        os.unlink(self.temp_db.name)

    def test_full_recovery_workflow(self):
        """Test complete recovery workflow."""
        # Simulate execution with failure
        execution_data = {
            "execution_id": "exec-integration-1",
            "error_message": "Connection timeout",
            "steps": [
                {
                    "id": "step-1",
                    "status": "failed",
                    "error_message": "Connection timeout",
                    "input_data": {"url": "https://api.example.com"},
                }
            ],
        }

        # Insert execution for coordinator to find
        db = self.coordinator.db
        db.get_execution_with_steps = lambda exec_id: (
            execution_data if exec_id == "exec-integration-1" else None
        )

        # Run recovery
        result = self.coordinator.recover_failure("exec-integration-1")

        # Verify recovery was attempted
        self.assertIn("diagnosis", result)
        self.assertIn("recovery_result", result)
        self.assertIn("validation", result)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling."""

    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.temp_db.close()
        self.coordinator = ErrorRecoveryCoordinator(self.temp_db.name)

    def tearDown(self):
        os.unlink(self.temp_db.name)

    def test_nonexistent_execution(self):
        """Test handling nonexistent execution."""
        result = self.coordinator.recover_failure("nonexistent-exec-id")
        self.assertFalse(result.get("success", True))

    def test_unknown_error_type(self):
        """Test handling unknown error types."""
        classifier = FailureClassifier()
        error_type = classifier.classify("Some completely unknown error XYZ123")
        self.assertEqual(error_type, "UNKNOWN")

    def test_empty_error_message(self):
        """Test handling empty error message."""
        analyzer = ErrorAnalyzer()
        strategy, score = analyzer.analyze("")
        # Should still return a strategy
        self.assertIsNotNone(strategy)


if __name__ == "__main__":
    unittest.main()
