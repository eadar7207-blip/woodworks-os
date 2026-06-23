"""Main error recovery skill module."""
import os
import sys
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
from agent_coordinator import ErrorRecoveryCoordinator


class ErrorRecoverySkill:
    """Main skill interface for error recovery."""

    def __init__(self, db_path: str = "executor.db"):
        self.coordinator = ErrorRecoveryCoordinator(db_path)
        self.db_path = db_path
        self.log_dir = Path(".claude/automations/.logs/recovery")
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def start_monitoring(self, interval_seconds: int = 120) -> Dict[str, Any]:
        """
        Start background monitoring for failures.

        In production, this would run as a systemd service or cron job.
        For now, runs once and returns.
        """
        config = self.coordinator.get_config()
        interval = config.get("monitor_interval_seconds", 120)

        self._log("INFO", f"Starting error recovery monitor (interval: {interval}s)")

        # Perform one monitoring cycle
        results = self.coordinator.monitor_for_failures()

        summary = {
            "status": "monitoring_started",
            "interval_seconds": interval,
            "check_results": results,
            "log_file": str(self.log_dir / "recovery.log"),
        }

        self._log("INFO", json.dumps(summary))
        return summary

    def recover(self, execution_id: str) -> Dict[str, Any]:
        """
        Manually trigger recovery for a specific failed execution.

        Args:
            execution_id: UUID of failed execution

        Returns:
            Recovery result with diagnosis, attempt, and validation
        """
        self._log("INFO", f"Triggering manual recovery for execution {execution_id}")

        result = self.coordinator.recover_failure(execution_id)

        self._log("INFO", json.dumps({
            "execution_id": execution_id,
            "success": result.get("success"),
            "message": result.get("message"),
        }))

        return result

    def get_status(self) -> Dict[str, Any]:
        """Get current recovery status and statistics."""
        status = self.coordinator.get_status()
        self._log("INFO", f"Status check: {status['total_recovery_attempts']} attempts, "
                          f"{status['success_rate']:.1%} success rate")
        return status

    def get_config(self) -> Dict[str, Any]:
        """Get recovery configuration."""
        return self.coordinator.get_config()

    def set_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Update recovery configuration."""
        self.coordinator.set_config(config)
        return self.coordinator.get_config()

    def get_logs(self, hours: int = 1) -> str:
        """Get recovery logs from last N hours."""
        log_file = self.log_dir / "recovery.log"
        if not log_file.exists():
            return "No logs found"

        # Read recent lines
        with open(log_file, 'r') as f:
            lines = f.readlines()

        # Filter by time if specified
        cutoff_time = datetime.utcnow().timestamp() - (hours * 3600)
        recent_lines = []

        for line in lines[-1000:]:  # Last 1000 lines
            try:
                log_entry = json.loads(line)
                if log_entry.get("timestamp") and \
                   datetime.fromisoformat(log_entry["timestamp"]).timestamp() > cutoff_time:
                    recent_lines.append(line)
            except:
                recent_lines.append(line)

        return "\n".join(recent_lines)

    def _log(self, level: str, message: str):
        """Log to recovery log file."""
        log_file = self.log_dir / "recovery.log"

        timestamp = datetime.utcnow().isoformat()

        # Try to parse as JSON, if not just wrap it
        try:
            if message.startswith("{"):
                log_entry = json.loads(message)
                log_entry["timestamp"] = timestamp
                log_entry["level"] = level
            else:
                log_entry = {
                    "timestamp": timestamp,
                    "level": level,
                    "message": message,
                }
        except:
            log_entry = {
                "timestamp": timestamp,
                "level": level,
                "message": message,
            }

        with open(log_file, 'a') as f:
            f.write(json.dumps(log_entry) + "\n")


def main():
    """CLI entry point."""
    # Find executor database
    db_path = find_executor_db()

    skill = ErrorRecoverySkill(db_path)

    if len(sys.argv) < 2:
        print(json.dumps({"error": "Missing command"}))
        sys.exit(1)

    command = sys.argv[1]

    try:
        if command == "start":
            interval = int(sys.argv[2]) if len(sys.argv) > 2 else 120
            result = skill.start_monitoring(interval)
            print(json.dumps(result))

        elif command == "recover":
            if len(sys.argv) < 3:
                print(json.dumps({"error": "Missing execution_id"}))
                sys.exit(1)
            execution_id = sys.argv[2]
            result = skill.recover(execution_id)
            print(json.dumps(result, default=str))

        elif command == "status":
            result = skill.get_status()
            print(json.dumps(result, default=str))

        elif command == "config":
            if len(sys.argv) > 2 and sys.argv[2] == "set":
                config = json.loads(sys.argv[3])
                result = skill.set_config(config)
            else:
                result = skill.get_config()
            print(json.dumps(result))

        elif command == "logs":
            hours = int(sys.argv[2]) if len(sys.argv) > 2 else 1
            result = skill.get_logs(hours)
            print(result)

        else:
            print(json.dumps({"error": f"Unknown command: {command}"}))
            sys.exit(1)

    except Exception as e:
        print(json.dumps({
            "error": str(e),
            "type": type(e).__name__,
        }))
        sys.exit(1)


def find_executor_db() -> str:
    """Find executor.db in known locations."""
    search_paths = [
        "executor.db",
        ".claude/automations/executor.db",
        "./.claude/automations/executor.db",
        os.path.expanduser("~/.claude/automations/executor.db"),
    ]

    for path in search_paths:
        if os.path.exists(path):
            return path

    # Default
    return "executor.db"


if __name__ == "__main__":
    main()
