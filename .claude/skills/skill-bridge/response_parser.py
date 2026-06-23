"""Parse and extract structured data from skill responses."""

import json
import re
from typing import Dict, Any, List, Tuple
from datetime import datetime


class ResponseParser:
    """Parse skill responses and extract structured data."""

    @staticmethod
    def parse_response(skill_name: str, action: str, raw_output: str) -> Dict[str, Any]:
        """Parse raw skill output into structured JSON.

        Returns a dict with:
        - status: "success" or "partial" or "error"
        - output: extracted structured data
        - confidence: float 0-1 indicating confidence in extraction
        - raw_output: original output
        """
        if not raw_output:
            return {
                "status": "error",
                "output": None,
                "confidence": 0.0,
                "raw_output": raw_output,
                "error": "Empty response from skill"
            }

        # Try to parse as JSON first
        try:
            parsed = json.loads(raw_output)
            return {
                "status": "success",
                "output": parsed,
                "confidence": 1.0,
                "raw_output": raw_output,
            }
        except json.JSONDecodeError:
            pass

        # Use skill-specific parsers
        parser_method = getattr(ResponseParser, f"_parse_{skill_name}_{action}", None)
        if parser_method:
            return parser_method(raw_output)

        # Fall back to generic parsing
        return ResponseParser._parse_generic(raw_output, skill_name, action)

    @staticmethod
    def _parse_generic(raw_output: str, skill_name: str, action: str) -> Dict[str, Any]:
        """Generic parser for skill responses."""
        # Extract key-value pairs
        extracted = {}
        lines = raw_output.split('\n')

        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip().lower().replace(' ', '_')
                value = value.strip()
                extracted[key] = value

        if extracted:
            return {
                "status": "partial",
                "output": extracted,
                "confidence": 0.5,
                "raw_output": raw_output,
            }

        # Return raw output as fallback
        return {
            "status": "success",
            "output": {"content": raw_output},
            "confidence": 0.3,
            "raw_output": raw_output,
        }

    # Prospect parsers
    @staticmethod
    def _parse_prospect_research(raw_output: str) -> Dict[str, Any]:
        """Parse prospect research response."""
        extracted = {
            "company_info": {},
            "contacts": [],
            "social_links": {},
            "recent_activity": []
        }

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
                # Try to extract email
                emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', line)
                if emails:
                    extracted["contacts"].append({"email": emails[0]})
            elif "social" in line.lower() or "linkedin" in line.lower():
                current_section = "social_links"
                if "linkedin" in line.lower():
                    linkedin_urls = re.findall(r'https://linkedin\.com/in/[\w-]+', line)
                    if linkedin_urls:
                        extracted["social_links"]["linkedin"] = linkedin_urls[0]

            if current_section and ":" in line:
                key, value = line.split(':', 1)
                key = key.strip().lower()
                value = value.strip()
                if isinstance(extracted.get(current_section), dict):
                    extracted[current_section][key] = value

        if extracted["contacts"] or extracted["company_info"]:
            confidence = 0.7

        return {
            "status": "success" if confidence > 0.6 else "partial",
            "output": extracted,
            "confidence": confidence,
            "raw_output": raw_output,
        }

    @staticmethod
    def _parse_prospect_outreach(raw_output: str) -> Dict[str, Any]:
        """Parse prospect outreach response."""
        extracted = {
            "sent": False,
            "message_id": None,
            "confirmation": None
        }

        if any(word in raw_output.lower() for word in ["sent", "success", "completed"]):
            extracted["sent"] = True
            confidence = 0.9
        else:
            confidence = 0.3

        # Extract message ID if present
        msg_ids = re.findall(r'[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}', raw_output)
        if msg_ids:
            extracted["message_id"] = msg_ids[0]
            confidence = min(1.0, confidence + 0.1)

        extracted["confirmation"] = raw_output.split('\n')[0][:100]

        return {
            "status": "success" if extracted["sent"] else "partial",
            "output": extracted,
            "confidence": confidence,
            "raw_output": raw_output,
        }

    # Proposal parsers
    @staticmethod
    def _parse_proposal_generate(raw_output: str) -> Dict[str, Any]:
        """Parse proposal generation response."""
        extracted = {
            "proposal_id": None,
            "proposal_content": None,
            "estimated_price": None,
            "document_url": None
        }

        # Extract proposal ID - handle formats like "prop_abc123" or "proposal_id: abc123"
        proposal_ids = re.findall(r'(?:proposal[_-]?id[:\s]*)?([a-zA-Z0-9]+\d{2,})', raw_output, re.IGNORECASE)
        if not proposal_ids:
            proposal_ids = re.findall(r'prop[_-]?([a-zA-Z0-9]+)', raw_output, re.IGNORECASE)
        if proposal_ids:
            extracted["proposal_id"] = proposal_ids[0]

        # Extract estimated price
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
            "confidence": confidence,
            "raw_output": raw_output,
        }

    @staticmethod
    def _parse_proposal_send(raw_output: str) -> Dict[str, Any]:
        """Parse proposal send response."""
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

        # Extract tracking ID
        tracking_ids = re.findall(r'[a-f0-9]{8}[a-f0-9]{4}', raw_output)
        if tracking_ids:
            extracted["tracking_id"] = tracking_ids[0]

        return {
            "status": "success" if extracted["sent"] else "partial",
            "output": extracted,
            "confidence": confidence,
            "raw_output": raw_output,
        }

    # CRM parsers
    @staticmethod
    def _parse_crm_log_activity(raw_output: str) -> Dict[str, Any]:
        """Parse CRM log activity response."""
        extracted = {
            "activity_id": None,
            "logged_at": None,
            "confirmation": raw_output.split('\n')[0][:100] if raw_output else None
        }

        # Extract activity ID
        activity_ids = re.findall(r'activity[_-]?id[:\s]+(\w+)', raw_output, re.IGNORECASE)
        if activity_ids:
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
            "confidence": confidence,
            "raw_output": raw_output,
        }

    @staticmethod
    def _parse_crm_update_contact(raw_output: str) -> Dict[str, Any]:
        """Parse CRM update contact response."""
        extracted = {
            "updated": False,
            "contact_id": None,
            "updated_fields": []
        }

        if any(word in raw_output.lower() for word in ["updated", "saved", "success"]):
            extracted["updated"] = True

        # Extract contact ID
        contact_ids = re.findall(r'contact[_-]?id[:\s]+(\w+)', raw_output, re.IGNORECASE)
        if contact_ids:
            extracted["contact_id"] = contact_ids[0]

        # Try to extract field updates
        field_pattern = r'(name|email|phone|company|status)[\s:]*(.+?)(?=\n|$)'
        fields = re.findall(field_pattern, raw_output, re.IGNORECASE)
        if fields:
            extracted["updated_fields"] = [f[0] for f in fields]

        confidence = 0.7 if extracted["updated"] else 0.4

        return {
            "status": "success" if extracted["updated"] else "partial",
            "output": extracted,
            "confidence": confidence,
            "raw_output": raw_output,
        }

    # Send parsers
    @staticmethod
    def _parse_send_email(raw_output: str) -> Dict[str, Any]:
        """Parse email send response."""
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

        # Extract message ID - try multiple patterns
        msg_ids = re.findall(r'(?:message[_\s]?id[:\s]+)([a-zA-Z0-9]+)', raw_output, re.IGNORECASE)
        if not msg_ids:
            msg_ids = re.findall(r'[a-f0-9]{8}[a-f0-9]{4}[a-f0-9]{4}', raw_output)
        if not msg_ids:
            # Try just alphanumeric sequence (but not single words)
            msg_ids = re.findall(r'[a-zA-Z0-9]{8,20}(?:[a-zA-Z0-9]*\d+)', raw_output)
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
            "confidence": confidence,
            "raw_output": raw_output,
        }

    # Tasks parsers
    @staticmethod
    def _parse_tasks_create(raw_output: str) -> Dict[str, Any]:
        """Parse task creation response."""
        extracted = {
            "task_id": None,
            "created_at": None,
            "confirmation": raw_output.split('\n')[0][:100] if raw_output else None
        }

        # Extract task ID
        task_ids = re.findall(r'task[_-]?id[:\s]+(\w+)', raw_output, re.IGNORECASE)
        if task_ids:
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
            "confidence": confidence,
            "raw_output": raw_output,
        }

    # Default fallback for unimplemented parsers
    def __getattr__(self, name):
        if name.startswith('_parse_'):
            return self._parse_generic
        raise AttributeError(f"'{self.__class__.__name__}' has no attribute '{name}'")


def parse_skill_response(skill_name: str, action: str, raw_output: str) -> Dict[str, Any]:
    """Parse a skill response into structured data."""
    parser = ResponseParser()
    return parser.parse_response(skill_name, action, raw_output)
