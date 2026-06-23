"""Invoke Claude Code skills and manage execution."""

import subprocess
import json
import os
import time
import uuid
from typing import Dict, Any, Tuple
from datetime import datetime

from skill_definitions import validate_parameters, get_skill_definition
from response_parser import parse_skill_response
from bridge_database import SkillBridgeDatabase
from skill_executor import SkillExecutor


class SkillInvoker:
    """Invoke Claude Code skills and manage their execution."""

    def __init__(self, workspace_path: str = None, db: SkillBridgeDatabase = None, executor: SkillExecutor = None):
        self.workspace_path = workspace_path or os.getenv("CLAUDE_CODE_WORKSPACE", ".")
        self.claude_path = os.path.expanduser("~/.local/bin/claude")
        self.db = db or SkillBridgeDatabase()
        self.timeout = int(os.getenv("SKILL_TIMEOUT", 120))
        self.executor = executor or SkillExecutor(
            claude_path=self.claude_path,
            timeout=self.timeout,
            workspace_path=self.workspace_path
        )

    def invoke_sync(
        self,
        skill_name: str,
        action: str,
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Invoke a skill synchronously and return result.

        Returns:
        {
            "status": "completed" | "failed" | "error",
            "output": <extracted_data>,
            "raw_output": <original_output>,
            "confidence": <float>,
            "duration_ms": <int>,
            "error": <error_message>,
            "invocation_id": <id>
        }
        """
        invocation_id = str(uuid.uuid4())
        start_time = time.time()

        try:
            # Validate parameters
            is_valid, error_msg = validate_parameters(skill_name, action, params)
            if not is_valid:
                result = {
                    "status": "error",
                    "error": f"Parameter validation failed: {error_msg}",
                    "invocation_id": invocation_id,
                    "duration_ms": int((time.time() - start_time) * 1000)
                }
                self.db.log_invocation(
                    invocation_id, skill_name, action, params,
                    "failed", error=error_msg
                )
                return result

            # Check if skill exists
            skill_def = get_skill_definition(skill_name)
            if not skill_def:
                error = f"Skill '{skill_name}' not found"
                result = {
                    "status": "error",
                    "error": error,
                    "invocation_id": invocation_id,
                    "duration_ms": int((time.time() - start_time) * 1000)
                }
                self.db.log_invocation(
                    invocation_id, skill_name, action, params,
                    "failed", error=error
                )
                return result

            # Execute skill using the enhanced executor
            executor_result = self.executor.execute_skill_command(skill_name, action, params)

            # Handle executor errors
            if executor_result["status"] == "error":
                result = {
                    "status": "failed",
                    "error": executor_result["error"],
                    "raw_output": executor_result["raw_output"],
                    "invocation_id": invocation_id,
                    "duration_ms": int((time.time() - start_time) * 1000)
                }
                self.db.log_invocation(
                    invocation_id, skill_name, action, params,
                    "failed", error=executor_result["error"],
                    duration_ms=result["duration_ms"]
                )
                return result

            # Build parsed response
            parsed = {
                "status": executor_result["status"],
                "output": executor_result.get("output", {}),
                "raw_output": executor_result.get("raw_output", ""),
                "confidence": executor_result.get("confidence", 0.7)
            }

            result = {
                "status": parsed["status"],
                "output": parsed["output"],
                "raw_output": parsed["raw_output"],
                "confidence": parsed["confidence"],
                "invocation_id": invocation_id,
                "duration_ms": int((time.time() - start_time) * 1000),
            }

            if "error" in parsed:
                result["error"] = parsed["error"]

            self.db.log_invocation(
                invocation_id, skill_name, action, params,
                parsed["status"], result=parsed["output"],
                duration_ms=result["duration_ms"]
            )

            return result

        except Exception as e:
            error = str(e)
            result = {
                "status": "error",
                "error": error,
                "invocation_id": invocation_id,
                "duration_ms": int((time.time() - start_time) * 1000)
            }
            self.db.log_invocation(
                invocation_id, skill_name, action, params,
                "error", error=error,
                duration_ms=result["duration_ms"]
            )
            return result

    def invoke_async(
        self,
        skill_name: str,
        action: str,
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Queue a skill invocation for async execution.

        Returns invocation ID for polling status.
        """
        invocation_id = str(uuid.uuid4())

        try:
            # Validate parameters
            is_valid, error_msg = validate_parameters(skill_name, action, params)
            if not is_valid:
                return {
                    "status": "error",
                    "error": f"Parameter validation failed: {error_msg}",
                    "invocation_id": invocation_id
                }

            # Create async invocation record
            try:
                self.db.create_async_invocation(invocation_id, skill_name, action, params)
            except Exception as db_error:
                return {
                    "status": "error",
                    "error": f"Database error: {str(db_error)}",
                    "invocation_id": invocation_id
                }

            return {
                "status": "queued",
                "invocation_id": invocation_id,
                "message": f"Skill invocation {invocation_id} queued for execution"
            }

        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "invocation_id": invocation_id
            }

    def get_invocation_status(self, invocation_id: str) -> Dict[str, Any]:
        """Get status of an async invocation."""
        try:
            invocation = self.db.get_async_invocation(invocation_id)

            if not invocation:
                return {
                    "status": "not_found",
                    "error": f"Invocation {invocation_id} not found"
                }

            result = {
                "invocation_id": invocation_id,
                "status": invocation["status"],
                "skill_name": invocation["skill_name"],
                "action": invocation["action"],
                "created_at": invocation["created_at"],
            }

            if invocation["started_at"]:
                result["started_at"] = invocation["started_at"]

            if invocation["completed_at"]:
                result["completed_at"] = invocation["completed_at"]

            if invocation["result"]:
                result["output"] = json.loads(invocation["result"])

            if invocation["error"]:
                result["error"] = invocation["error"]

            return result

        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }


    def list_available_skills(self) -> Dict[str, Any]:
        """Get list of available skills and their metadata."""
        from skill_definitions import SKILL_DEFINITIONS

        skills = []
        for skill_name, definition in SKILL_DEFINITIONS.items():
            skill_info = {
                "name": definition["name"],
                "description": definition["description"],
                "actions": definition.get("actions", []),
                "parameters": {}
            }

            for action, param_def in definition.get("parameters", {}).items():
                skill_info["parameters"][action] = {
                    "required": param_def.get("required", []),
                    "optional": param_def.get("optional", []),
                    "description": param_def.get("description", "")
                }

            skills.append(skill_info)

        return {
            "total": len(skills),
            "skills": skills
        }

    def get_skill_details(self, skill_name: str) -> Dict[str, Any]:
        """Get detailed information about a specific skill."""
        skill_def = get_skill_definition(skill_name)

        if not skill_def:
            return {"error": f"Skill '{skill_name}' not found"}

        return skill_def
