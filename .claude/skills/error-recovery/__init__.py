"""Error Recovery Skill - Autonomous failure detection and recovery."""

from error_recovery import ErrorRecoverySkill
from agent_coordinator import ErrorRecoveryCoordinator
from database import RecoveryDatabase
from recovery_strategies import ErrorAnalyzer, FailureClassifier

__version__ = "1.0.0"
__all__ = [
    "ErrorRecoverySkill",
    "ErrorRecoveryCoordinator",
    "RecoveryDatabase",
    "ErrorAnalyzer",
    "FailureClassifier",
]
