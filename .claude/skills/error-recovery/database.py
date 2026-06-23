"""SQLite database layer for error recovery tracking."""
import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
import os


class RecoveryDatabase:
    """SQLite wrapper for error recovery state persistence."""

    def __init__(self, db_path: str = "executor.db"):
        self.db_path = db_path
        self.init_schema()

    def get_connection(self):
        """Get a database connection."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_schema(self):
        """Initialize recovery tracking tables."""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Recovery attempts table - tracks each recovery action
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS recovery_attempts (
                id TEXT PRIMARY KEY,
                execution_id TEXT NOT NULL,
                step_id TEXT,
                attempt_number INTEGER,
                strategy_used TEXT,
                error_type TEXT,
                error_message TEXT,
                original_params TEXT,
                modified_params TEXT,
                status TEXT DEFAULT 'pending',
                result_message TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP,
                duration_ms INTEGER,
                FOREIGN KEY (execution_id) REFERENCES executions(id)
            )
        """)

        # Failure patterns table - aggregated learning data
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS failure_patterns (
                id TEXT PRIMARY KEY,
                error_pattern TEXT UNIQUE,
                error_type TEXT,
                total_occurrences INTEGER DEFAULT 1,
                successful_recoveries INTEGER DEFAULT 0,
                failed_recoveries INTEGER DEFAULT 0,
                recommended_strategy TEXT,
                last_seen TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(error_pattern)
            )
        """)

        # Recovery config table - settings and thresholds
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS recovery_config (
                key TEXT PRIMARY KEY,
                value TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()
        conn.close()

    def create_recovery_attempt(
        self,
        execution_id: str,
        step_id: str,
        attempt_number: int,
        strategy_used: str,
        error_type: str,
        error_message: str,
        original_params: Dict = None,
        modified_params: Dict = None,
    ) -> str:
        """Create a new recovery attempt record."""
        import uuid
        attempt_id = str(uuid.uuid4())

        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO recovery_attempts
            (id, execution_id, step_id, attempt_number, strategy_used, error_type,
             error_message, original_params, modified_params, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'pending')
        """, (
            attempt_id,
            execution_id,
            step_id,
            attempt_number,
            strategy_used,
            error_type,
            error_message,
            json.dumps(original_params or {}),
            json.dumps(modified_params or {}),
        ))

        conn.commit()
        conn.close()
        return attempt_id

    def update_recovery_attempt(
        self,
        attempt_id: str,
        status: str,
        result_message: str = None,
        duration_ms: int = None,
    ):
        """Update recovery attempt result."""
        conn = self.get_connection()
        cursor = conn.cursor()

        completed_at = datetime.utcnow() if status in ["success", "failed"] else None

        cursor.execute("""
            UPDATE recovery_attempts
            SET status = ?, result_message = ?, completed_at = ?, duration_ms = ?
            WHERE id = ?
        """, (status, result_message, completed_at, duration_ms, attempt_id))

        conn.commit()
        conn.close()

    def get_recovery_attempts_for_execution(self, execution_id: str) -> List[Dict]:
        """Get all recovery attempts for an execution."""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM recovery_attempts
            WHERE execution_id = ?
            ORDER BY attempt_number ASC
        """, (execution_id,))

        rows = cursor.fetchall()
        conn.close()

        return [
            {
                "id": row["id"],
                "execution_id": row["execution_id"],
                "step_id": row["step_id"],
                "attempt_number": row["attempt_number"],
                "strategy_used": row["strategy_used"],
                "error_type": row["error_type"],
                "error_message": row["error_message"],
                "status": row["status"],
                "result_message": row["result_message"],
                "created_at": row["created_at"],
                "completed_at": row["completed_at"],
                "duration_ms": row["duration_ms"],
            }
            for row in rows
        ]

    def update_failure_pattern(
        self,
        error_pattern: str,
        error_type: str,
        recovery_status: str,
        recommended_strategy: str,
    ):
        """Update or create failure pattern record."""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Check if pattern exists
        cursor.execute(
            "SELECT id FROM failure_patterns WHERE error_pattern = ?",
            (error_pattern,)
        )

        if cursor.fetchone():
            # Update existing pattern
            if recovery_status == "success":
                cursor.execute("""
                    UPDATE failure_patterns
                    SET total_occurrences = total_occurrences + 1,
                        successful_recoveries = successful_recoveries + 1,
                        last_seen = ?,
                        updated_at = ?
                    WHERE error_pattern = ?
                """, (datetime.utcnow(), datetime.utcnow(), error_pattern))
            else:
                cursor.execute("""
                    UPDATE failure_patterns
                    SET total_occurrences = total_occurrences + 1,
                        failed_recoveries = failed_recoveries + 1,
                        last_seen = ?,
                        updated_at = ?
                    WHERE error_pattern = ?
                """, (datetime.utcnow(), datetime.utcnow(), error_pattern))
        else:
            # Create new pattern
            import uuid
            pattern_id = str(uuid.uuid4())

            successful = 1 if recovery_status == "success" else 0
            failed = 0 if recovery_status == "success" else 1

            cursor.execute("""
                INSERT INTO failure_patterns
                (id, error_pattern, error_type, total_occurrences,
                 successful_recoveries, failed_recoveries, recommended_strategy, last_seen)
                VALUES (?, ?, ?, 1, ?, ?, ?, ?)
            """, (
                pattern_id,
                error_pattern,
                error_type,
                successful,
                failed,
                recommended_strategy,
                datetime.utcnow(),
            ))

        conn.commit()
        conn.close()

    def get_failure_pattern(self, error_pattern: str) -> Optional[Dict]:
        """Get failure pattern data."""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM failure_patterns WHERE error_pattern = ?",
            (error_pattern,)
        )

        row = cursor.fetchone()
        conn.close()

        if not row:
            return None

        return {
            "error_pattern": row["error_pattern"],
            "error_type": row["error_type"],
            "total_occurrences": row["total_occurrences"],
            "successful_recoveries": row["successful_recoveries"],
            "failed_recoveries": row["failed_recoveries"],
            "success_rate": row["successful_recoveries"] / row["total_occurrences"] if row["total_occurrences"] > 0 else 0,
            "recommended_strategy": row["recommended_strategy"],
            "last_seen": row["last_seen"],
        }

    def get_failed_executions(self, limit: int = 10) -> List[Dict]:
        """Get recent failed executions from executor database."""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                SELECT id, workflow_id, status, error_message, created_at
                FROM executions
                WHERE status = 'failed'
                ORDER BY created_at DESC
                LIMIT ?
            """, (limit,))

            rows = cursor.fetchall()
            conn.close()

            return [
                {
                    "execution_id": row["id"],
                    "workflow_id": row["workflow_id"],
                    "status": row["status"],
                    "error_message": row["error_message"],
                    "created_at": row["created_at"],
                }
                for row in rows
            ]
        except Exception:
            # Executions table may not exist yet
            conn.close()
            return []

    def get_execution_with_steps(self, execution_id: str) -> Optional[Dict]:
        """Get execution and all its steps."""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            # Get execution
            cursor.execute(
                "SELECT * FROM executions WHERE id = ?",
                (execution_id,)
            )
            exec_row = cursor.fetchone()

            if not exec_row:
                conn.close()
                return None

            # Get steps
            cursor.execute(
                """SELECT id, step_index, step_name, action_type, status,
                          input_data, output_data, error_message
                   FROM execution_steps
                   WHERE execution_id = ?
                   ORDER BY step_index""",
                (execution_id,)
            )
            step_rows = cursor.fetchall()
            conn.close()

            return {
                "execution_id": exec_row["id"],
                "workflow_id": exec_row["workflow_id"],
                "status": exec_row["status"],
                "error_message": exec_row["error_message"],
                "created_at": exec_row["created_at"],
                "steps": [
                    {
                        "id": step["id"],
                        "step_index": step["step_index"],
                        "step_name": step["step_name"],
                        "action_type": step["action_type"],
                        "status": step["status"],
                        "input_data": json.loads(step["input_data"] or "{}"),
                        "output_data": json.loads(step["output_data"] or "{}"),
                        "error_message": step["error_message"],
                    }
                    for step in step_rows
                ]
            }
        except Exception:
            # Tables may not exist yet
            conn.close()
            return None

    def set_config(self, key: str, value: Any):
        """Set a configuration value."""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT OR REPLACE INTO recovery_config (key, value, updated_at)
            VALUES (?, ?, ?)
        """, (key, json.dumps(value), datetime.utcnow()))

        conn.commit()
        conn.close()

    def get_config(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT value FROM recovery_config WHERE key = ?",
            (key,)
        )

        row = cursor.fetchone()
        conn.close()

        if not row:
            return default

        return json.loads(row["value"])

    def get_all_config(self) -> Dict[str, Any]:
        """Get all configuration."""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT key, value FROM recovery_config")
        rows = cursor.fetchall()
        conn.close()

        return {
            row["key"]: json.loads(row["value"])
            for row in rows
        }
