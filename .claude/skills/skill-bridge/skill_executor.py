"""Enhanced skill executor that properly invokes Claude Code skills."""

import subprocess
import json
import os
import re
import time
from typing import Dict, Any, Tuple, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class SkillExecutor:
    """Execute Claude Code skills using the --print and --json modes."""

    def __init__(self, claude_path: str = None, timeout: int = 120, workspace_path: str = None):
        """Initialize the skill executor.

        Args:
            claude_path: Path to claude CLI (defaults to ~/.local/bin/claude)
            timeout: Timeout in seconds for skill execution
            workspace_path: Working directory for skill execution
        """
        self.claude_path = claude_path or os.path.expanduser("~/.local/bin/claude")
        self.timeout = timeout
        self.workspace_path = workspace_path or os.getcwd()

    def execute_skill_command(
        self,
        skill_name: str,
        action: str,
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute a skill by calling it with the /skill-name syntax.

        Args:
            skill_name: Name of the skill (prospect, proposal, crm, etc.)
            action: Action to perform (research, generate, log_activity, etc.)
            params: Parameters for the action

        Returns:
            {
                "status": "success" | "partial" | "error",
                "output": <extracted_data>,
                "raw_output": <original_output>,
                "confidence": <float>,
                "execution_time_ms": <int>,
                "error": <error_message>
            }
        """
        start_time = time.time()

        try:
            # Build the prompt to invoke the skill
            prompt = self._build_skill_prompt(skill_name, action, params)

            # Execute Claude Code with the skill invocation
            raw_output = self._execute_claude_command(prompt)

            execution_time = int((time.time() - start_time) * 1000)

            # Parse the response
            parsed = self._parse_skill_output(skill_name, action, raw_output)

            return {
                "status": parsed.get("status", "success"),
                "output": parsed.get("output", {}),
                "raw_output": raw_output,
                "confidence": parsed.get("confidence", 0.7),
                "execution_time_ms": execution_time,
                "error": parsed.get("error")
            }

        except subprocess.TimeoutExpired:
            return {
                "status": "error",
                "output": None,
                "raw_output": "",
                "confidence": 0.0,
                "execution_time_ms": int((time.time() - start_time) * 1000),
                "error": f"Skill execution timed out after {self.timeout} seconds"
            }

        except FileNotFoundError:
            return {
                "status": "error",
                "output": None,
                "raw_output": "",
                "confidence": 0.0,
                "execution_time_ms": int((time.time() - start_time) * 1000),
                "error": f"Claude CLI not found at {self.claude_path}"
            }

        except Exception as e:
            return {
                "status": "error",
                "output": None,
                "raw_output": str(e),
                "confidence": 0.0,
                "execution_time_ms": int((time.time() - start_time) * 1000),
                "error": str(e)
            }

    def _build_skill_prompt(self, skill_name: str, action: str, params: Dict[str, Any]) -> str:
        """Build a prompt to invoke a skill via Claude Code.

        Args:
            skill_name: Name of the skill
            action: Action to perform
            params: Parameters for the action

        Returns:
            A prompt string that invokes the skill
        """
        # Format parameters as a readable list
        param_str = ""
        for key, value in params.items():
            if isinstance(value, str):
                param_str += f"  - {key}: {value}\n"
            else:
                param_str += f"  - {key}: {json.dumps(value)}\n"

        # Create a prompt that invokes the skill
        prompt = f"""Use the /{skill_name} skill to perform the following action:

Action: {action}
Parameters:
{param_str}

Return the result in a structured format with:
- success or failure status
- any relevant IDs or identifiers
- any extracted data
- a confirmation message

IMPORTANT: Return your response as valid JSON with fields like status, output, confirmation, etc."""

        return prompt

    def _execute_claude_command(self, prompt: str) -> str:
        """Execute Claude Code with a prompt and return the output.

        Args:
            prompt: The prompt to send to Claude Code

        Returns:
            The raw text output from Claude Code
        """
        # Use --print mode for non-interactive output
        # Use --output-format json for structured output
        cmd = [
            self.claude_path,
            "--print",
            "--bare",  # Minimal mode to avoid hooks and complex setup
            prompt
        ]

        logger.debug(f"Executing: {' '.join(cmd[:3])} [prompt]")

        result = subprocess.run(
            cmd,
            cwd=self.workspace_path,
            capture_output=True,
            text=True,
            timeout=self.timeout
        )

        # Return stdout, or stderr if stdout is empty
        output = result.stdout or result.stderr
        logger.debug(f"Claude command exit code: {result.returncode}")

        return output

    def _parse_skill_output(
        self,
        skill_name: str,
        action: str,
        raw_output: str
    ) -> Dict[str, Any]:
        """Parse the raw output from Claude Code.

        Args:
            skill_name: Name of the skill
            action: Action performed
            raw_output: Raw output from Claude Code

        Returns:
            Parsed result with status, output, and confidence
        """
        if not raw_output:
            return {
                "status": "error",
                "output": None,
                "confidence": 0.0,
                "error": "Empty response from Claude Code"
            }

        # Try to extract JSON from the output
        json_match = self._extract_json_from_output(raw_output)

        if json_match:
            try:
                parsed = json.loads(json_match)
                return {
                    "status": "success",
                    "output": parsed,
                    "confidence": 0.95
                }
            except json.JSONDecodeError:
                pass

        # Fall back to skill-specific parsing
        return self._parse_skill_specific(skill_name, action, raw_output)

    def _extract_json_from_output(self, text: str) -> Optional[str]:
        """Extract JSON from text output.

        Args:
            text: Text that may contain JSON

        Returns:
            Extracted JSON string or None
        """
        # Try to find JSON in code blocks
        json_block_match = re.search(r'```(?:json)?\s*({.*?})\s*```', text, re.DOTALL)
        if json_block_match:
            return json_block_match.group(1)

        # Try to find JSON starting with { and ending with }
        brace_match = re.search(r'{.*}', text, re.DOTALL)
        if brace_match:
            return brace_match.group(0)

        return None

    def _parse_skill_specific(
        self,
        skill_name: str,
        action: str,
        raw_output: str
    ) -> Dict[str, Any]:
        """Parse skill-specific output.

        Args:
            skill_name: Name of the skill
            action: Action performed
            raw_output: Raw output text

        Returns:
            Parsed result
        """
        # Delegate to skill-specific parser
        method_name = f"_parse_{skill_name}_{action}"
        parser_method = getattr(self, method_name, None)

        if parser_method:
            return parser_method(raw_output)

        # Generic fallback parser
        return self._parse_generic(raw_output, skill_name, action)

    def _parse_generic(self, raw_output: str, skill_name: str, action: str) -> Dict[str, Any]:
        """Generic parser for skill outputs.

        Args:
            raw_output: Raw output text
            skill_name: Name of the skill
            action: Action performed

        Returns:
            Parsed result
        """
        # Check for success indicators
        success_indicators = ["success", "completed", "done", "created", "generated", "sent", "logged"]
        error_indicators = ["error", "failed", "not found", "invalid", "missing"]

        output_lower = raw_output.lower()

        # Determine status
        has_success = any(ind in output_lower for ind in success_indicators)
        has_error = any(ind in output_lower for ind in error_indicators)

        if has_error:
            status = "error"
            confidence = 0.7
        elif has_success:
            status = "success"
            confidence = 0.8
        else:
            status = "partial"
            confidence = 0.5

        # Extract key-value pairs
        extracted = {}
        lines = raw_output.split('\n')

        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip().lower().replace(' ', '_')
                value = value.strip()
                if key and value:
                    extracted[key] = value

        # If no key-value pairs found, return raw output
        if not extracted:
            extracted = {"content": raw_output}

        return {
            "status": status,
            "output": extracted,
            "confidence": confidence
        }

    # Skill-specific parsers

    def _parse_prospect_research(self, raw_output: str) -> Dict[str, Any]:
        """Parse prospect research output."""
        extracted = {
            "company_info": {},
            "contacts": [],
            "social_links": {},
            "recent_activity": []
        }

        # First, extract all emails from the entire output
        all_emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', raw_output)
        for email in all_emails:
            # Check if we already have this email
            if not any(c.get("email") == email for c in extracted["contacts"]):
                extracted["contacts"].append({"email": email})

        lines = raw_output.split('\n')
        current_section = None
        confidence = 0.5

        for line in lines:
            line = line.strip()
            if not line:
                continue

            if "company" in line.lower():
                current_section = "company_info"
            elif "contact" in line.lower() or "email" in line.lower():
                current_section = "contacts"
            elif "social" in line.lower() or "linkedin" in line.lower():
                current_section = "social_links"
                # Extract LinkedIn URLs
                linkedin_urls = re.findall(r'https://linkedin\.com/in/[\w-]+', line)
                for url in linkedin_urls:
                    extracted["social_links"]["linkedin"] = url

            if current_section and ":" in line:
                key, value = line.split(':', 1)
                key = key.strip().lower()
                value = value.strip()
                if isinstance(extracted.get(current_section), dict):
                    extracted[current_section][key] = value

        if extracted["contacts"] or extracted["company_info"]:
            confidence = 0.8

        return {
            "status": "success" if confidence > 0.7 else "partial",
            "output": extracted,
            "confidence": confidence
        }

    def _parse_prospect_outreach(self, raw_output: str) -> Dict[str, Any]:
        """Parse prospect outreach output."""
        extracted = {
            "sent": False,
            "message_id": None,
            "confirmation": raw_output.split('\n')[0][:200] if raw_output else None
        }

        # Check if sent successfully
        if any(word in raw_output.lower() for word in ["sent", "success", "completed"]):
            extracted["sent"] = True
            confidence = 0.9
        else:
            confidence = 0.3

        # Extract message ID
        msg_ids = re.findall(r'[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}', raw_output)
        if msg_ids:
            extracted["message_id"] = msg_ids[0]
            confidence = min(1.0, confidence + 0.1)

        return {
            "status": "success" if extracted["sent"] else "partial",
            "output": extracted,
            "confidence": confidence
        }

    def _parse_proposal_generate(self, raw_output: str) -> Dict[str, Any]:
        """Parse proposal generation output."""
        extracted = {
            "proposal_id": None,
            "proposal_content": None,
            "estimated_price": None,
            "document_url": None
        }

        # Extract proposal ID - look for PROP_XXXX pattern first
        proposal_ids = re.findall(r'PROP[_-]([A-Z0-9_]+)', raw_output, re.IGNORECASE)
        if not proposal_ids:
            # Then try generic ID pattern
            proposal_ids = re.findall(r'(?:proposal[_-]?id[:\s]*)?([a-zA-Z0-9]+\d{2,})', raw_output, re.IGNORECASE)
        if not proposal_ids:
            proposal_ids = re.findall(r'prop[_-]?([a-zA-Z0-9]+)', raw_output, re.IGNORECASE)

        if proposal_ids:
            # Keep the full ID including PROP_ if it was part of the match
            match = re.search(r'(PROP[_-][A-Z0-9_]+)', raw_output, re.IGNORECASE)
            if match:
                extracted["proposal_id"] = match.group(1)
            else:
                extracted["proposal_id"] = proposal_ids[0]

        # Extract price
        prices = re.findall(r'\$\d+(?:,\d{3})*(?:\.\d{2})?', raw_output)
        if prices:
            extracted["estimated_price"] = prices[0]

        # Extract URLs
        urls = re.findall(r'https?://[^\s]+', raw_output)
        if urls:
            extracted["document_url"] = urls[0]

        # Use first 500 chars as proposal content
        extracted["proposal_content"] = raw_output[:500] if raw_output else None

        confidence = 0.6
        if extracted["proposal_id"] and extracted["estimated_price"]:
            confidence = 0.85

        return {
            "status": "success" if confidence > 0.7 else "partial",
            "output": extracted,
            "confidence": confidence
        }

    def _parse_proposal_send(self, raw_output: str) -> Dict[str, Any]:
        """Parse proposal send output."""
        extracted = {
            "sent": False,
            "sent_at": None,
            "tracking_id": None
        }

        if any(word in raw_output.lower() for word in ["sent", "success", "completed"]):
            extracted["sent"] = True
            confidence = 0.9
        else:
            confidence = 0.3

        # Extract timestamp
        timestamps = re.findall(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}', raw_output)
        if timestamps:
            extracted["sent_at"] = timestamps[0]
            confidence = min(1.0, confidence + 0.1)
        else:
            extracted["sent_at"] = datetime.now().isoformat()

        # Extract tracking ID - look for track_XXXX pattern or hex
        tracking_ids = re.findall(r'track[_-]([a-z0-9]+)', raw_output, re.IGNORECASE)
        if not tracking_ids:
            tracking_ids = re.findall(r'[a-f0-9]{8}[a-f0-9]{4}', raw_output)

        if tracking_ids:
            # Keep full ID if it has prefix
            match = re.search(r'(track[_-][a-z0-9]+)', raw_output, re.IGNORECASE)
            if match:
                extracted["tracking_id"] = match.group(1)
            else:
                extracted["tracking_id"] = tracking_ids[0]

        return {
            "status": "success" if extracted["sent"] else "partial",
            "output": extracted,
            "confidence": confidence
        }

    def _parse_crm_log_activity(self, raw_output: str) -> Dict[str, Any]:
        """Parse CRM log activity output."""
        extracted = {
            "activity_id": None,
            "logged_at": None,
            "confirmation": raw_output.split('\n')[0][:100] if raw_output else None
        }

        # Extract activity ID - look for ACT_XXXX pattern or generic ID
        activity_ids = re.findall(r'ACT[_-]([A-Z0-9_]+)', raw_output, re.IGNORECASE)
        if not activity_ids:
            activity_ids = re.findall(r'activity[_-]?id[:\s]+(\w+)', raw_output, re.IGNORECASE)

        if activity_ids:
            # Keep full ID if it has prefix
            match = re.search(r'(ACT[_-][A-Z0-9_]+)', raw_output, re.IGNORECASE)
            if match:
                extracted["activity_id"] = match.group(1)
            else:
                extracted["activity_id"] = activity_ids[0]

        # Extract timestamp
        timestamps = re.findall(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}', raw_output)
        if timestamps:
            extracted["logged_at"] = timestamps[0]
        else:
            extracted["logged_at"] = datetime.now().isoformat()

        success = any(word in raw_output.lower() for word in ["logged", "recorded", "success"])
        confidence = 0.8 if success else 0.5

        return {
            "status": "success" if success else "partial",
            "output": extracted,
            "confidence": confidence
        }

    def _parse_crm_update_contact(self, raw_output: str) -> Dict[str, Any]:
        """Parse CRM update contact output."""
        extracted = {
            "updated": False,
            "contact_id": None,
            "updated_fields": []
        }

        if any(word in raw_output.lower() for word in ["updated", "saved", "success"]):
            extracted["updated"] = True

        # Extract contact ID - look for CONT_XXXX pattern or generic ID
        contact_ids = re.findall(r'CONT[_-]([A-Z0-9_]+)', raw_output, re.IGNORECASE)
        if not contact_ids:
            contact_ids = re.findall(r'contact[_-]?id[:\s]+(\w+)', raw_output, re.IGNORECASE)

        if contact_ids:
            # Keep full ID if it has prefix
            match = re.search(r'(CONT[_-][A-Z0-9_]+)', raw_output, re.IGNORECASE)
            if match:
                extracted["contact_id"] = match.group(1)
            else:
                extracted["contact_id"] = contact_ids[0]

        # Extract field updates
        field_pattern = r'(name|email|phone|company|status)[\s:]*(.+?)(?=\n|$)'
        fields = re.findall(field_pattern, raw_output, re.IGNORECASE)
        if fields:
            extracted["updated_fields"] = [f[0] for f in fields]

        confidence = 0.7 if extracted["updated"] else 0.4

        return {
            "status": "success" if extracted["updated"] else "partial",
            "output": extracted,
            "confidence": confidence
        }

    def _parse_send_email(self, raw_output: str) -> Dict[str, Any]:
        """Parse email send output."""
        extracted = {
            "sent": False,
            "message_id": None,
            "sent_at": None,
            "confirmation": None
        }

        if any(word in raw_output.lower() for word in ["sent", "success", "completed", "queued"]):
            extracted["sent"] = True
            confidence = 0.9
        else:
            confidence = 0.3

        # Extract message ID
        msg_ids = re.findall(r'(?:message[_\s]?id[:\s]+)([a-zA-Z0-9]+)', raw_output, re.IGNORECASE)
        if not msg_ids:
            msg_ids = re.findall(r'[a-f0-9]{8}[a-f0-9]{4}[a-f0-9]{4}', raw_output)
        if msg_ids:
            extracted["message_id"] = msg_ids[0]
            confidence = min(1.0, confidence + 0.1)

        # Extract timestamp
        timestamps = re.findall(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}', raw_output)
        if timestamps:
            extracted["sent_at"] = timestamps[0]
        else:
            extracted["sent_at"] = datetime.now().isoformat()

        extracted["confirmation"] = raw_output.split('\n')[0][:200] if raw_output else "Email sent"

        return {
            "status": "success" if extracted["sent"] else "partial",
            "output": extracted,
            "confidence": confidence
        }

    def _parse_tasks_create(self, raw_output: str) -> Dict[str, Any]:
        """Parse task creation output."""
        extracted = {
            "task_id": None,
            "created_at": None,
            "confirmation": raw_output.split('\n')[0][:100] if raw_output else None
        }

        # Extract task ID - look for TASK_XXXX pattern or generic ID
        task_ids = re.findall(r'TASK[_-]([A-Z0-9_]+)', raw_output, re.IGNORECASE)
        if not task_ids:
            task_ids = re.findall(r'task[_-]?id[:\s]+(\w+)', raw_output, re.IGNORECASE)

        if task_ids:
            # Keep full ID if it has prefix
            match = re.search(r'(TASK[_-][A-Z0-9_]+)', raw_output, re.IGNORECASE)
            if match:
                extracted["task_id"] = match.group(1)
            else:
                extracted["task_id"] = task_ids[0]

        # Extract timestamp
        timestamps = re.findall(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}', raw_output)
        if timestamps:
            extracted["created_at"] = timestamps[0]
        else:
            extracted["created_at"] = datetime.now().isoformat()

        success = any(word in raw_output.lower() for word in ["created", "success"])
        confidence = 0.8 if success else 0.5

        return {
            "status": "success" if success else "partial",
            "output": extracted,
            "confidence": confidence
        }


if __name__ == "__main__":
    # Test the executor
    import logging

    logging.basicConfig(level=logging.DEBUG)

    executor = SkillExecutor()

    print("Testing Skill Executor")
    print("=" * 60)

    # Test prospect research
    print("\n1. Testing prospect research...")
    result = executor.execute_skill_command(
        "prospect",
        "research",
        {
            "name": "John Doe",
            "company": "Acme Corp"
        }
    )
    print(f"Status: {result['status']}")
    print(f"Confidence: {result['confidence']}")
    print(f"Execution time: {result['execution_time_ms']}ms")

    # Test sending email
    print("\n2. Testing send email...")
    result = executor.execute_skill_command(
        "send",
        "email",
        {
            "to": "john@example.com",
            "subject": "Test Email",
            "body": "This is a test email"
        }
    )
    print(f"Status: {result['status']}")
    print(f"Confidence: {result['confidence']}")
    print(f"Output: {json.dumps(result['output'], indent=2)}")
