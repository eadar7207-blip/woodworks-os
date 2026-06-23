"""SQLite database for skill bridge invocations and caching."""

import sqlite3
import json
import os
from datetime import datetime
from typing import Dict, Any, List, Optional
from contextlib import contextmanager


class SkillBridgeDatabase:
    """Database for tracking skill invocations and caching metadata."""

    def __init__(self, db_path: str = ".claude/skills/skill-bridge/bridge.db"):
        self.db_path = db_path
        self._ensure_directory()
        self._init_db()

    def _ensure_directory(self):
        """Ensure database directory exists."""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

    @contextmanager
    def _get_connection(self):
        """Get database connection context manager."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def _init_db(self):
        """Initialize database tables."""
        with self._get_connection() as conn:
            cursor = conn.cursor()

            # Skill invocations table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS skill_invocations (
                    id TEXT PRIMARY KEY,
                    skill_name TEXT NOT NULL,
                    action TEXT,
                    params TEXT NOT NULL,
                    status TEXT NOT NULL,
                    result TEXT,
                    error TEXT,
                    created_at TEXT NOT NULL,
                    completed_at TEXT,
                    duration_ms INTEGER
                )
            """)

            # Skill metadata cache table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS skill_cache (
                    skill_name TEXT PRIMARY KEY,
                    metadata TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            """)

            # Async invocations table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS async_invocations (
                    id TEXT PRIMARY KEY,
                    skill_name TEXT NOT NULL,
                    action TEXT,
                    params TEXT NOT NULL,
                    status TEXT NOT NULL,
                    result TEXT,
                    error TEXT,
                    created_at TEXT NOT NULL,
                    started_at TEXT,
                    completed_at TEXT,
                    worker_id TEXT
                )
            """)

            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_skill_invocations_skill
                ON skill_invocations(skill_name)
            """)

            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_skill_invocations_status
                ON skill_invocations(status)
            """)

            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_async_invocations_status
                ON async_invocations(status)
            """)

    def log_invocation(
        self,
        invocation_id: str,
        skill_name: str,
        action: str,
        params: Dict[str, Any],
        status: str,
        result: Optional[Dict[str, Any]] = None,
        error: Optional[str] = None,
        duration_ms: Optional[int] = None
    ):
        """Log a skill invocation."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO skill_invocations
                (id, skill_name, action, params, status, result, error, created_at, completed_at, duration_ms)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                invocation_id,
                skill_name,
                action,
                json.dumps(params),
                status,
                json.dumps(result) if result else None,
                error,
                datetime.now().isoformat(),
                datetime.now().isoformat() if status in ["completed", "failed"] else None,
                duration_ms
            ))

    def get_invocation(self, invocation_id: str) -> Optional[Dict[str, Any]]:
        """Get an invocation by ID."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM skill_invocations WHERE id = ?", (invocation_id,))
            row = cursor.fetchone()

            if not row:
                return None

            return dict(row)

    def list_invocations(
        self,
        skill_name: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """List invocations with optional filtering."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            query = "SELECT * FROM skill_invocations WHERE 1=1"
            params = []

            if skill_name:
                query += " AND skill_name = ?"
                params.append(skill_name)

            if status:
                query += " AND status = ?"
                params.append(status)

            query += " ORDER BY created_at DESC LIMIT ?"
            params.append(limit)

            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    def cache_skill_metadata(self, skill_name: str, metadata: Dict[str, Any]):
        """Cache skill metadata."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO skill_cache
                (skill_name, metadata, updated_at)
                VALUES (?, ?, ?)
            """, (
                skill_name,
                json.dumps(metadata),
                datetime.now().isoformat()
            ))

    def get_cached_metadata(self, skill_name: str) -> Optional[Dict[str, Any]]:
        """Get cached skill metadata."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT metadata FROM skill_cache WHERE skill_name = ?", (skill_name,))
            row = cursor.fetchone()

            if not row:
                return None

            return json.loads(row[0])

    def create_async_invocation(
        self,
        invocation_id: str,
        skill_name: str,
        action: str,
        params: Dict[str, Any]
    ) -> str:
        """Create an async invocation record."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO async_invocations
                (id, skill_name, action, params, status, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                invocation_id,
                skill_name,
                action,
                json.dumps(params),
                "queued",
                datetime.now().isoformat()
            ))

        return invocation_id

    def update_async_invocation(
        self,
        invocation_id: str,
        status: str,
        result: Optional[Dict[str, Any]] = None,
        error: Optional[str] = None,
        worker_id: Optional[str] = None
    ):
        """Update an async invocation."""
        update_dict = {"status": status}

        if result:
            update_dict["result"] = json.dumps(result)

        if error:
            update_dict["error"] = error

        if worker_id:
            update_dict["worker_id"] = worker_id

        if status == "running":
            update_dict["started_at"] = datetime.now().isoformat()
        elif status in ["completed", "failed"]:
            update_dict["completed_at"] = datetime.now().isoformat()

        with self._get_connection() as conn:
            cursor = conn.cursor()

            set_clause = ", ".join([f"{k} = ?" for k in update_dict.keys()])
            values = list(update_dict.values()) + [invocation_id]

            cursor.execute(f"""
                UPDATE async_invocations
                SET {set_clause}
                WHERE id = ?
            """, values)

    def get_async_invocation(self, invocation_id: str) -> Optional[Dict[str, Any]]:
        """Get an async invocation by ID."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM async_invocations WHERE id = ?", (invocation_id,))
            row = cursor.fetchone()

            if not row:
                return None

            return dict(row)

    def list_async_invocations(
        self,
        status: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """List async invocations with optional filtering."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            query = "SELECT * FROM async_invocations WHERE 1=1"
            params = []

            if status:
                query += " AND status = ?"
                params.append(status)

            query += " ORDER BY created_at DESC LIMIT ?"
            params.append(limit)

            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    def cleanup_old_invocations(self, days: int = 30):
        """Clean up old invocation records."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM skill_invocations
                WHERE datetime(created_at) < datetime('now', '-' || ? || ' days')
            """, (days,))

            cursor.execute("""
                DELETE FROM async_invocations
                WHERE datetime(created_at) < datetime('now', '-' || ? || ' days')
                AND status IN ('completed', 'failed')
            """, (days,))
