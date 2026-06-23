#!/usr/bin/env python3
"""
Demo script showing error recovery in action.
Simulates failures and recovery process.
"""

import json
from recovery_strategies import ErrorAnalyzer, FailureClassifier
from agent_coordinator import ErrorAnalyzerAgent, RecoveryExecutorAgent
import tempfile
import os
from database import RecoveryDatabase


def demo_error_classification():
    """Demo 1: Error classification"""
    print("\n" + "="*60)
    print("DEMO 1: Error Classification")
    print("="*60)

    errors = [
        "Connection timeout while fetching data",
        "Invalid email address format: test@",
        "Skill 'email' not found in registry",
        "Payload exceeds maximum size of 10MB",
        "Permission denied: access to CRM database",
        "Service temporarily unavailable, please retry",
    ]

    classifier = FailureClassifier()

    for error in errors:
        error_type = classifier.classify(error)
        retriable = classifier.should_retry(error_type)
        print(f"\nError: {error}")
        print(f"  Type: {error_type}")
        print(f"  Retriable: {retriable}")


def demo_strategy_selection():
    """Demo 2: Automatic strategy selection"""
    print("\n" + "="*60)
    print("DEMO 2: Strategy Selection")
    print("="*60)

    analyzer = ErrorAnalyzer()

    errors_and_strategies = [
        ("Connection timeout", "RETRY"),
        ("Invalid email address", "RETRY_WITH_MODIFIED_PARAMS"),
        ("Rate limit exceeded", "REDUCE_SCOPE"),
        ("Skill 'email' not found", "FALLBACK_ACTION"),
        ("Failed to log activity to CRM", "SKIP_STEP"),
    ]

    for error, expected_strategy in errors_and_strategies:
        strategy, confidence = analyzer.analyze(error)
        match = "✓" if strategy == expected_strategy else "✗"
        print(f"\n{match} Error: {error}")
        print(f"  Expected: {expected_strategy}")
        print(f"  Selected: {strategy}")
        print(f"  Confidence: {confidence:.1%}")


def demo_recovery_attempt():
    """Demo 3: Recovery attempt tracking"""
    print("\n" + "="*60)
    print("DEMO 3: Recovery Attempt Tracking")
    print("="*60)

    # Create temp database
    temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
    temp_db.close()
    db = RecoveryDatabase(temp_db.name)

    execution_id = "demo-exec-123"
    step_id = "demo-step-1"

    # Simulate 3 recovery attempts
    attempts_data = [
        {
            "attempt": 1,
            "strategy": "RETRY",
            "status": "failed",
            "message": "Still timeout after wait 2s",
            "duration": 2050,
        },
        {
            "attempt": 2,
            "strategy": "RETRY",
            "status": "failed",
            "message": "Still timeout after wait 4s",
            "duration": 4200,
        },
        {
            "attempt": 3,
            "strategy": "RETRY",
            "status": "success",
            "message": "Retry succeeded after wait 8s",
            "duration": 8350,
        },
    ]

    for attempt_data in attempts_data:
        attempt_id = db.create_recovery_attempt(
            execution_id=execution_id,
            step_id=step_id,
            attempt_number=attempt_data["attempt"],
            strategy_used=attempt_data["strategy"],
            error_type="TRANSIENT",
            error_message="Connection timeout",
        )

        db.update_recovery_attempt(
            attempt_id=attempt_id,
            status=attempt_data["status"],
            result_message=attempt_data["message"],
            duration_ms=attempt_data["duration"],
        )

    # Show results
    attempts = db.get_recovery_attempts_for_execution(execution_id)
    print(f"\nExecution: {execution_id}")
    print(f"Total recovery attempts: {len(attempts)}\n")

    for attempt in attempts:
        status_icon = "✓" if attempt["status"] == "success" else "✗"
        print(f"{status_icon} Attempt {attempt['attempt_number']}: {attempt['strategy_used']}")
        print(f"  Status: {attempt['status']}")
        print(f"  Message: {attempt['result_message']}")
        print(f"  Duration: {attempt['duration_ms']}ms")

    # Show pattern learning
    pattern = db.get_failure_pattern("Connection timeout")
    if pattern:
        print(f"\nPattern Learning:")
        print(f"  Error pattern: {pattern['error_pattern']}")
        print(f"  Total occurrences: {pattern['total_occurrences']}")
        print(f"  Success rate: {pattern['success_rate']:.1%}")
        print(f"  Recommended: {pattern['recommended_strategy']}")

    os.unlink(temp_db.name)


def demo_error_analyzer_agent():
    """Demo 4: Error analyzer agent diagnosis"""
    print("\n" + "="*60)
    print("DEMO 4: Error Analyzer Agent")
    print("="*60)

    temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
    temp_db.close()
    db = RecoveryDatabase(temp_db.name)
    agent = ErrorAnalyzerAgent(db)

    execution_data = {
        "execution_id": "demo-exec-456",
        "error_message": "Initial error (overridden by step)",
        "steps": [
            {
                "id": "demo-step-1",
                "step_index": 0,
                "step_name": "research_prospect",
                "status": "completed",
            },
            {
                "id": "demo-step-2",
                "step_index": 1,
                "step_name": "send_email",
                "status": "failed",
                "error_message": "Invalid email address format provided",
            },
        ],
    }

    diagnosis = agent.diagnose(execution_data)

    print(f"\nExecution ID: {diagnosis['execution_id']}")
    print(f"Failed Step: {diagnosis['failed_step']['step_name']}")
    print(f"Error: {diagnosis['error_message']}")
    print(f"\nDiagnosis:")
    print(f"  Error Type: {diagnosis['error_type']}")
    print(f"  Recommended Strategy: {diagnosis['recommended_strategy']}")
    print(f"  Confidence: {diagnosis['confidence']:.1%}")
    print(f"  Recoverable: {diagnosis['is_recoverable']}")
    print(f"  Max Attempts: {diagnosis['max_attempts']}")

    os.unlink(temp_db.name)


def demo_all_strategies():
    """Demo 5: All recovery strategies"""
    print("\n" + "="*60)
    print("DEMO 5: All Recovery Strategies")
    print("="*60)

    analyzer = ErrorAnalyzer()
    strategies = analyzer.get_all_strategies()

    print(f"\nTotal strategies: {len(strategies)}\n")

    for name, strategy in strategies.items():
        print(f"{name}")
        print(f"  Description: {strategy.description}")

        # Test each strategy with a relevant error
        test_errors = {
            "RETRY": "Connection timeout",
            "RETRY_WITH_MODIFIED_PARAMS": "Invalid parameter format",
            "SKIP_STEP": "CRM logging failed",
            "REDUCE_SCOPE": "Payload too large",
            "FALLBACK_ACTION": "Skill 'email' not found",
        }

        if name in test_errors:
            score = strategy.analyze_error(test_errors[name])
            print(f"  Example error: {test_errors[name]}")
            print(f"  Detection score: {score:.1%}")
        print()


def main():
    """Run all demos"""
    print("\n" + "█"*60)
    print("ERROR RECOVERY SKILL - INTERACTIVE DEMO")
    print("█"*60)

    demo_error_classification()
    demo_strategy_selection()
    demo_recovery_attempt()
    demo_error_analyzer_agent()
    demo_all_strategies()

    print("\n" + "="*60)
    print("Demo Complete!")
    print("="*60)
    print("\nTo run in production:")
    print("  python3 error_recovery.py start")
    print("\nTo recover a specific failure:")
    print("  python3 error_recovery.py recover {execution_id}")
    print("\nTo check status:")
    print("  python3 error_recovery.py status")
    print()


if __name__ == "__main__":
    main()
