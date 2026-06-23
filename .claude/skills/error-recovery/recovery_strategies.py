"""Recovery strategy implementations for error recovery."""
import time
import json
import re
from typing import Dict, Any, Optional, Tuple
from datetime import datetime


class RecoveryStrategy:
    """Base class for recovery strategies."""

    name: str
    description: str

    def analyze_error(self, error_message: str) -> float:
        """
        Analyze error and return confidence score (0.0-1.0) that this
        strategy will work for this error.
        """
        raise NotImplementedError

    def recover(
        self,
        execution_id: str,
        step_data: Dict[str, Any],
        original_params: Dict[str, Any],
    ) -> Tuple[bool, Dict[str, Any], Optional[str]]:
        """
        Attempt recovery. Returns:
        - success (bool): whether recovery succeeded
        - modified_params (dict): parameters used for retry
        - result_message (str): summary of recovery attempt
        """
        raise NotImplementedError


class RetryStrategy(RecoveryStrategy):
    """Retry with exponential backoff for transient errors."""

    name = "RETRY"
    description = "Retry with exponential backoff (2s, 4s, 8s)"

    TRANSIENT_PATTERNS = [
        r"timeout",
        r"timed out",
        r"connection refused",
        r"connection reset",
        r"connection timeout",
        r"temporary failure",
        r"service unavailable",
        r"temporarily unavailable",
        r"try again",
        r"api unavailable",
    ]

    def analyze_error(self, error_message: str) -> float:
        """Check if error looks transient."""
        error_lower = error_message.lower()

        for pattern in self.TRANSIENT_PATTERNS:
            if re.search(pattern, error_lower):
                return 0.9  # High confidence for transient errors

        # Medium confidence for generic errors (might be transient)
        if len(error_message) < 100:
            return 0.4

        return 0.0

    def recover(
        self,
        execution_id: str,
        step_data: Dict[str, Any],
        original_params: Dict[str, Any],
    ) -> Tuple[bool, Dict[str, Any], Optional[str]]:
        """Retry with exponential backoff."""
        max_attempts = 3
        backoff_times = [2, 4, 8]  # seconds

        for attempt in range(max_attempts):
            if attempt > 0:
                wait_time = backoff_times[min(attempt - 1, len(backoff_times) - 1)]
                time.sleep(wait_time)

            # In real implementation, would re-execute the step here
            # For now, just return that we attempted
            attempt_num = attempt + 1
            result = f"Retry attempt {attempt_num}/{max_attempts}"

            if attempt_num < max_attempts:
                return False, original_params, result
            else:
                return True, original_params, f"Retry succeeded after {max_attempts} attempts"

        return False, original_params, "Retry exhausted"


class RetryWithModifiedParamsStrategy(RecoveryStrategy):
    """Retry with modified parameters for configuration errors."""

    name = "RETRY_WITH_MODIFIED_PARAMS"
    description = "Modify parameters and retry (sanitize, simplify, reformat)"

    CONFIG_ERROR_PATTERNS = [
        r"invalid.*format",
        r"bad.*parameter",
        r"required.*missing",
        r"invalid.*value",
        r"malformed",
        r"syntax error",
        r"invalid.*address",
        r"invalid.*email",
        r"invalid.*json",
        r"type error",
    ]

    def analyze_error(self, error_message: str) -> float:
        """Check if error is configuration-related."""
        error_lower = error_message.lower()

        for pattern in self.CONFIG_ERROR_PATTERNS:
            if re.search(pattern, error_lower):
                return 0.85  # High confidence for config errors

        return 0.0

    def recover(
        self,
        execution_id: str,
        step_data: Dict[str, Any],
        original_params: Dict[str, Any],
    ) -> Tuple[bool, Dict[str, Any], Optional[str]]:
        """Modify parameters and retry."""
        modified_params = self._modify_params(original_params)

        modifications = []

        # Sanitize string parameters
        for key, value in modified_params.items():
            if isinstance(value, str):
                original_len = len(value)
                # Trim whitespace
                value = value.strip()
                # Lowercase
                value = value.lower()

                if key.endswith("email") or "email" in key:
                    # Additional email-specific sanitization
                    value = value.lower()
                    value = re.sub(r"\s+", "", value)

                if len(value) < original_len:
                    modifications.append(f"Sanitized {key}")

                modified_params[key] = value

        result = f"Modified params: {'; '.join(modifications) if modifications else 'No changes needed'}"
        return True, modified_params, result

    def _modify_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Create modified copy of parameters."""
        return json.loads(json.dumps(params))  # Deep copy


class SkipStepStrategy(RecoveryStrategy):
    """Skip non-critical step and continue workflow."""

    name = "SKIP_STEP"
    description = "Skip failed step and continue to next step"

    NON_CRITICAL_PATTERNS = [
        r"optional",
        r"logging",
        r"log activity",
        r"crm",
        r"notification",
        r"email",
        r"slack",
        r"webhook",
    ]

    def analyze_error(self, error_message: str) -> float:
        """Check if step can be safely skipped."""
        error_lower = error_message.lower()

        # Check step name and error message for non-critical indicators
        for pattern in self.NON_CRITICAL_PATTERNS:
            if re.search(pattern, error_lower):
                return 0.7  # Medium-high confidence for non-critical

        return 0.0

    def recover(
        self,
        execution_id: str,
        step_data: Dict[str, Any],
        original_params: Dict[str, Any],
    ) -> Tuple[bool, Dict[str, Any], Optional[str]]:
        """Skip step and continue."""
        step_name = step_data.get("step_name", "unknown")
        result = f"Skipped step '{step_name}'. Workflow will continue with next step."
        return True, original_params, result


class ReduceScopeStrategy(RecoveryStrategy):
    """Reduce task scope for size-related errors."""

    name = "REDUCE_SCOPE"
    description = "Reduce input size/complexity"

    SCOPE_ERROR_PATTERNS = [
        r"too large",
        r"too many",
        r"exceeds",
        r"limit",
        r"maximum",
        r"payload too large",
        r"request too large",
        r"input too large",
        r"out of memory",
        r"rate limit",
    ]

    def analyze_error(self, error_message: str) -> float:
        """Check if error is scope-related."""
        error_lower = error_message.lower()

        for pattern in self.SCOPE_ERROR_PATTERNS:
            if re.search(pattern, error_lower):
                return 0.8  # High confidence for scope errors

        return 0.0

    def recover(
        self,
        execution_id: str,
        step_data: Dict[str, Any],
        original_params: Dict[str, Any],
    ) -> Tuple[bool, Dict[str, Any], Optional[str]]:
        """Reduce scope of operation."""
        modified_params = self._reduce_scope(original_params)

        modifications = []
        for key in ["limit", "count", "batch_size", "max_items", "max_results"]:
            if key in modified_params:
                original = original_params.get(key)
                modified = modified_params.get(key)
                if original and modified and modified < original:
                    modifications.append(f"{key}: {original} → {modified}")

        result = f"Reduced scope. {'; '.join(modifications)}" if modifications else "Scope reduction applied"
        return True, modified_params, result

    def _reduce_scope(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Create reduced-scope copy of parameters."""
        modified = json.loads(json.dumps(params))

        # Reduce common limit parameters by 50%
        for key in ["limit", "count", "batch_size", "max_items", "max_results"]:
            if key in modified and isinstance(modified[key], int):
                original = modified[key]
                modified[key] = max(1, int(original / 2))  # At least 1

        return modified


class FallbackActionStrategy(RecoveryStrategy):
    """Use alternative action/skill if primary fails."""

    name = "FALLBACK_ACTION"
    description = "Use alternative skill/action"

    SKILL_FALLBACKS = {
        "email": ["send", "crm"],
        "slack": ["email", "send"],
        "webhook": ["crm", "email"],
        "send": ["email", "crm"],
    }

    def analyze_error(self, error_message: str) -> float:
        """Check if skill/action not found."""
        error_lower = error_message.lower()

        not_found_patterns = [
            r"skill.+not found",
            r"action.+not found",
            r"unknown skill",
            r"unknown action",
            r"no such",
        ]

        for pattern in not_found_patterns:
            if re.search(pattern, error_lower):
                return 0.85  # High confidence for skill not found

        return 0.0

    def recover(
        self,
        execution_id: str,
        step_data: Dict[str, Any],
        original_params: Dict[str, Any],
    ) -> Tuple[bool, Dict[str, Any], Optional[str]]:
        """Use fallback skill/action."""
        action_type = step_data.get("action_type", "unknown")
        fallback = self._find_fallback(action_type)

        if fallback:
            result = f"Falling back from {action_type} to {fallback}"
            return True, original_params, result
        else:
            result = f"No fallback available for {action_type}"
            return False, original_params, result

    def _find_fallback(self, action: str) -> Optional[str]:
        """Find suitable fallback for action."""
        action_lower = action.lower()

        for primary, fallbacks in self.SKILL_FALLBACKS.items():
            if primary in action_lower:
                return fallbacks[0] if fallbacks else None

        return None


class ErrorAnalyzer:
    """Analyzes errors and selects best recovery strategy."""

    def __init__(self):
        self.strategies = [
            RetryStrategy(),
            RetryWithModifiedParamsStrategy(),
            SkipStepStrategy(),
            ReduceScopeStrategy(),
            FallbackActionStrategy(),
        ]

    def analyze(self, error_message: str) -> Tuple[str, float]:
        """
        Analyze error and return best strategy name and confidence score.

        Returns: (strategy_name, confidence_score)
        """
        best_strategy = None
        best_score = 0.0

        for strategy in self.strategies:
            score = strategy.analyze_error(error_message)
            if score > best_score:
                best_score = score
                best_strategy = strategy

        # Default to retry if no clear winner
        if best_strategy is None:
            best_strategy = self.strategies[0]  # RetryStrategy
            best_score = 0.3

        return best_strategy.name, best_score

    def get_strategy(self, strategy_name: str) -> Optional[RecoveryStrategy]:
        """Get strategy instance by name."""
        for strategy in self.strategies:
            if strategy.name == strategy_name:
                return strategy
        return None

    def get_all_strategies(self) -> Dict[str, RecoveryStrategy]:
        """Get all strategies as dict."""
        return {strategy.name: strategy for strategy in self.strategies}


class FailureClassifier:
    """Classifies failure types based on error messages."""

    ERROR_TYPES = {
        "TRANSIENT": [
            r"timeout",
            r"connection",
            r"temporary",
            r"try again",
            r"unavailable",
        ],
        "CONFIGURATION": [
            r"invalid",
            r"bad.*parameter",
            r"required.*missing",
            r"malformed",
            r"syntax error",
        ],
        "SKILL_ERROR": [
            r"skill.+not found",
            r"action.+not found",
            r"unknown skill",
            r"no such",
        ],
        "SCOPE_ERROR": [
            r"too large",
            r"too many",
            r"exceeds",
            r"limit",
            r"rate limit",
        ],
        "PERMISSION_ERROR": [
            r"permission denied",
            r"access denied",
            r"unauthorized",
            r"forbidden",
        ],
    }

    @classmethod
    def classify(cls, error_message: str) -> str:
        """Classify error into a type."""
        error_lower = error_message.lower()

        for error_type, patterns in cls.ERROR_TYPES.items():
            for pattern in patterns:
                if re.search(pattern, error_lower):
                    return error_type

        return "UNKNOWN"

    @classmethod
    def should_retry(cls, error_type: str) -> bool:
        """Determine if error type should be retried."""
        retriable = ["TRANSIENT", "CONFIGURATION", "SKILL_ERROR"]
        return error_type in retriable
