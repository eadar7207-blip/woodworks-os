#!/usr/bin/env python3
"""
Persistent Problem Solver
Tries different approaches until a task succeeds. Never gives up.
"""

import sys
import json
import time
import subprocess
from enum import Enum
from datetime import datetime


class Strategy(Enum):
    """Recovery strategies in order of attempt"""
    RETRY = "retry"
    SPLIT = "split"
    SIMPLIFY = "simplify"
    CHANGE_TOOL = "change_tool"
    HUMAN_INPUT = "human_input"


class PersistentProblemSolver:
    """Tries different approaches until task succeeds"""

    def __init__(self, task, failure_reason, max_attempts=5):
        self.task = task
        self.failure_reason = failure_reason
        self.max_attempts = max_attempts
        self.attempts = []
        self.strategies = [
            Strategy.RETRY,
            Strategy.SPLIT,
            Strategy.SIMPLIFY,
            Strategy.CHANGE_TOOL,
            Strategy.HUMAN_INPUT,
        ]

    def log_attempt(self, strategy, result, details=""):
        """Log an attempt"""
        self.attempts.append({
            'strategy': strategy.value,
            'result': 'success' if result else 'failed',
            'details': details,
            'timestamp': datetime.utcnow().isoformat()
        })

    def attempt_retry(self):
        """Strategy 1: Retry with backoff"""
        print(f"🔄 Attempt 1: Retry with backoff")

        # Simulate retry with exponential backoff
        for i in range(3):
            wait_time = (2 ** i) * 5  # 5s, 10s, 20s
            print(f"   Waiting {wait_time}s before retry {i+1}...")
            time.sleep(wait_time)

            # Simulate task execution
            success = self._simulate_task_execution("retry", i+1)
            if success:
                self.log_attempt(Strategy.RETRY, True, f"Succeeded on retry {i+1}")
                return True

        self.log_attempt(Strategy.RETRY, False, "Failed after 3 retries")
        return False

    def attempt_split(self):
        """Strategy 2: Split into subtasks"""
        print(f"🔀 Attempt 2: Split into subtasks")

        # Analyze task complexity
        subtask_count = self._estimate_subtask_count()
        print(f"   Breaking into {subtask_count} subtasks...")

        subtasks = self._generate_subtasks(subtask_count)
        successful = 0

        for i, subtask in enumerate(subtasks, 1):
            print(f"   Subtask {i}/{subtask_count}: {subtask[:50]}...")
            success = self._simulate_task_execution("subtask", i)
            if success:
                successful += 1

        all_success = successful == len(subtasks)
        self.log_attempt(
            Strategy.SPLIT,
            all_success,
            f"Completed {successful}/{len(subtasks)} subtasks"
        )
        return all_success

    def attempt_simplify(self):
        """Strategy 3: Simplify approach"""
        print(f"📉 Attempt 3: Simplify approach")

        # Remove complexity
        simplifications = [
            "Remove optional features",
            "Focus on core deliverable",
            "Skip extra validation",
            "Use faster but less comprehensive method"
        ]

        for simp in simplifications:
            print(f"   Trying: {simp}...")
            success = self._simulate_task_execution("simplified", simplifications.index(simp)+1)
            if success:
                self.log_attempt(
                    Strategy.SIMPLIFY,
                    True,
                    f"Succeeded with simplification: {simp}"
                )
                return True

        self.log_attempt(Strategy.SIMPLIFY, False, "All simplifications failed")
        return False

    def attempt_change_tool(self):
        """Strategy 4: Change tool/method"""
        print(f"🔧 Attempt 4: Change tool/method")

        alternative_tools = [
            "Switch to alternative API",
            "Use local processing instead of cloud",
            "Run in parallel instead of sequential",
            "Change processing order/priority"
        ]

        for tool in alternative_tools:
            print(f"   Trying: {tool}...")
            success = self._simulate_task_execution("alt_tool", alternative_tools.index(tool)+1)
            if success:
                self.log_attempt(
                    Strategy.CHANGE_TOOL,
                    True,
                    f"Succeeded with: {tool}"
                )
                return True

        self.log_attempt(Strategy.CHANGE_TOOL, False, "All alternative tools failed")
        return False

    def attempt_human_input(self):
        """Strategy 5: Escalate to human"""
        print(f"🆘 Attempt 5: Escalate to human")

        escalation_msg = {
            'status': 'needs_input',
            'task': self.task,
            'tried_approaches': [a['strategy'] for a in self.attempts],
            'question': 'All automated approaches failed. How should we approach this differently?',
            'suggestions': [
                'Clarify task requirements',
                'Provide domain expertise',
                'Adjust constraints/expectations',
                'Suggest alternative method'
            ]
        }

        self.log_attempt(
            Strategy.HUMAN_INPUT,
            False,
            "Escalated to human for guidance"
        )

        return escalation_msg

    def _estimate_subtask_count(self):
        """Estimate how many subtasks needed"""
        # Simple heuristic: longer task = more subtasks
        task_length = len(self.task)
        if task_length > 200:
            return 5
        elif task_length > 100:
            return 3
        else:
            return 2

    def _generate_subtasks(self, count):
        """Generate subtasks from main task"""
        # Simple generation: break by keywords
        keywords = ['and', ',', 'also', 'plus']
        parts = self.task
        for kw in keywords:
            if kw in parts:
                parts = parts.split(kw)
                break

        # If we didn't split, just divide the task
        if isinstance(parts, str):
            words = parts.split()
            chunk_size = len(words) // count
            parts = [' '.join(words[i*chunk_size:(i+1)*chunk_size]) for i in range(count)]

        return parts[:count]

    def _simulate_task_execution(self, method, attempt):
        """Simulate task execution (in real version, would execute actual task)"""
        # In real implementation, would:
        # 1. Generate actual task code based on method
        # 2. Execute it
        # 3. Check for success

        # For demo, use simple probability: earlier attempts more likely to fail
        import random
        base_success_rate = 0.3 + (attempt * 0.15)  # 45%, 60%, 75%...
        success = random.random() < base_success_rate
        return success

    def solve(self):
        """Try strategies until one succeeds"""
        print(f"🎯 Persistent Problem Solver starting")
        print(f"   Task: {self.task[:60]}...")
        print(f"   Failure: {self.failure_reason}\n")

        attempt_num = 1

        while attempt_num <= self.max_attempts:
            if attempt_num == 1:
                result = self.attempt_retry()
            elif attempt_num == 2:
                result = self.attempt_split()
            elif attempt_num == 3:
                result = self.attempt_simplify()
            elif attempt_num == 4:
                result = self.attempt_change_tool()
            else:
                result = self.attempt_human_input()

            print()

            # Check for success
            if result is True:
                return self._success_result()
            elif isinstance(result, dict) and result.get('status') == 'needs_input':
                return result

            attempt_num += 1

        # All attempts failed
        return self._failure_result()

    def _success_result(self):
        """Format success result"""
        successful_strategy = self.attempts[-1]['strategy']
        return {
            'status': 'success',
            'task': self.task,
            'original_failure': self.failure_reason,
            'recovery_strategy': successful_strategy,
            'attempts': len(self.attempts),
            'all_attempts': self.attempts,
            'message': f'✅ Task recovered using {successful_strategy} strategy',
            'timestamp': datetime.utcnow().isoformat()
        }

    def _failure_result(self):
        """Format failure result"""
        return {
            'status': 'escalated',
            'task': self.task,
            'original_failure': self.failure_reason,
            'attempts_made': len(self.attempts),
            'all_attempts': self.attempts,
            'message': '⚠️  All automated strategies failed. Needs human intervention.',
            'need_help': True,
            'timestamp': datetime.utcnow().isoformat()
        }


def main():
    """CLI interface"""
    if len(sys.argv) < 3:
        print('Usage: python solver.py "<task>" "<failure_reason>"')
        print('Example: python solver.py "Research 50 competitors" "Agent stalled (600s)"')
        sys.exit(1)

    task = sys.argv[1]
    failure_reason = sys.argv[2]

    solver = PersistentProblemSolver(task, failure_reason)
    result = solver.solve()

    print(f"\n{'='*60}")
    print(json.dumps(result, indent=2))
    print(f"{'='*60}")


if __name__ == '__main__':
    main()
