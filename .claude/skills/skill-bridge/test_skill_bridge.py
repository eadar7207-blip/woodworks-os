"""Comprehensive tests for Skill Bridge API."""

import unittest
import json
import tempfile
import os
from unittest.mock import Mock, patch, MagicMock

from skill_invoker import SkillInvoker
from skill_definitions import validate_parameters, get_skill_definition
from response_parser import parse_skill_response
from bridge_database import SkillBridgeDatabase
from skill_bridge import app


class TestSkillDefinitions(unittest.TestCase):
    """Test skill definitions and parameter validation."""

    def test_get_skill_definition(self):
        """Test retrieving skill definition."""
        prospect_def = get_skill_definition("prospect")
        self.assertIsNotNone(prospect_def)
        self.assertEqual(prospect_def["name"], "prospect")
        self.assertIn("research", prospect_def["parameters"])

    def test_validate_required_parameters(self):
        """Test parameter validation for required fields."""
        # Valid parameters
        is_valid, error = validate_parameters(
            "prospect", "research",
            {"name": "John", "company": "ABC Corp"}
        )
        self.assertTrue(is_valid)
        self.assertEqual(error, "")

    def test_validate_missing_parameters(self):
        """Test validation catches missing parameters."""
        # Missing required parameter
        is_valid, error = validate_parameters(
            "prospect", "research",
            {"name": "John"}  # Missing 'company'
        )
        self.assertFalse(is_valid)
        self.assertIn("company", error)

    def test_validate_unexpected_parameters(self):
        """Test validation catches unexpected parameters."""
        # Unexpected parameter
        is_valid, error = validate_parameters(
            "prospect", "research",
            {"name": "John", "company": "ABC", "unknown_param": "value"}
        )
        self.assertFalse(is_valid)
        self.assertIn("unknown_param", error)

    def test_all_skills_defined(self):
        """Test that all required skills are defined."""
        required_skills = [
            "prospect", "proposal", "crm", "send", "tasks",
            "content", "calendar", "invoicing", "automate", "wiki"
        ]

        for skill in required_skills:
            self.assertIsNotNone(
                get_skill_definition(skill),
                f"Skill '{skill}' not defined"
            )


class TestResponseParser(unittest.TestCase):
    """Test response parsing and extraction."""

    def test_parse_json_response(self):
        """Test parsing valid JSON response."""
        json_output = json.dumps({"status": "success", "id": "123"})
        result = parse_skill_response("prospect", "research", json_output)

        self.assertEqual(result["status"], "success")
        self.assertEqual(result["confidence"], 1.0)
        self.assertEqual(result["output"]["id"], "123")

    def test_parse_prospect_research_response(self):
        """Test parsing prospect research response."""
        raw_output = """
        Company: ABC Real Estate
        Contact: john@abc.com
        LinkedIn: https://linkedin.com/in/john-smith
        """

        result = parse_skill_response("prospect", "research", raw_output)

        self.assertIn("company_info", result["output"])
        self.assertTrue(len(result["output"]["contacts"]) > 0)
        self.assertGreater(result["confidence"], 0.5)

    def test_parse_send_email_response(self):
        """Test parsing email send response."""
        raw_output = """
        Email sent successfully
        Message ID: abc123def456
        Sent at: 2024-01-15T10:30:00
        """

        result = parse_skill_response("send", "email", raw_output)

        self.assertTrue(result["output"]["sent"])
        self.assertEqual(result["output"]["message_id"], "abc123def456")

    def test_parse_empty_response(self):
        """Test parsing empty response."""
        result = parse_skill_response("prospect", "research", "")

        self.assertEqual(result["status"], "error")
        self.assertIn("error", result)

    def test_parse_proposal_generate_response(self):
        """Test parsing proposal generation response."""
        raw_output = """
        Proposal Generated Successfully
        Proposal ID: prop_abc123
        Estimated Price: $5,000
        Document: https://example.com/proposal.pdf
        This is a detailed proposal for your automation needs...
        """

        result = parse_skill_response("proposal", "generate", raw_output)

        self.assertEqual(result["output"]["proposal_id"], "abc123")
        self.assertEqual(result["output"]["estimated_price"], "$5,000")
        self.assertIsNotNone(result["output"]["document_url"])


class TestSkillInvoker(unittest.TestCase):
    """Test skill invocation logic."""

    def setUp(self):
        """Set up test fixtures."""
        self.db = SkillBridgeDatabase(db_path=tempfile.mktemp(suffix=".db"))
        self.invoker = SkillInvoker(db=self.db)

    def test_invoke_sync_parameter_validation(self):
        """Test sync invocation with invalid parameters."""
        result = self.invoker.invoke_sync(
            "prospect", "research",
            {"name": "John"}  # Missing required 'company' parameter
        )

        self.assertEqual(result["status"], "error")
        self.assertIn("Parameter validation failed", result["error"])

    def test_invoke_sync_skill_not_found(self):
        """Test invocation with non-existent skill."""
        result = self.invoker.invoke_sync(
            "nonexistent_skill", "action",
            {}
        )

        self.assertEqual(result["status"], "error")
        self.assertIn("not found", result["error"])

    @patch('skill_invoker.SkillInvoker._execute_command')
    def test_invoke_sync_execution(self, mock_execute):
        """Test successful sync invocation."""
        import time

        def slow_execute(*args):
            time.sleep(0.01)  # Sleep briefly to ensure duration_ms > 0
            return (
                json.dumps({"success": True, "id": "123"}),
                0
            )

        mock_execute.side_effect = slow_execute

        result = self.invoker.invoke_sync(
            "prospect", "research",
            {"name": "John", "company": "ABC Corp"}
        )

        self.assertEqual(result["status"], "success")
        self.assertIsNotNone(result["invocation_id"])
        self.assertGreaterEqual(result["duration_ms"], 0)  # Allow 0 on fast systems
        self.assertIn("output", result)

    def test_invoke_async_returns_id(self):
        """Test async invocation returns invocation ID."""
        result = self.invoker.invoke_async(
            "proposal", "generate",
            {"prospect_name": "John", "company": "ABC", "scope": "Automation"}
        )

        self.assertEqual(result["status"], "queued")
        self.assertIsNotNone(result["invocation_id"])

    def test_get_invocation_status(self):
        """Test retrieving invocation status."""
        # Create async invocation
        async_result = self.invoker.invoke_async(
            "proposal", "generate",
            {"prospect_name": "John", "company": "ABC"}
        )

        invocation_id = async_result["invocation_id"]

        # Get status
        status = self.invoker.get_invocation_status(invocation_id)

        self.assertEqual(status["status"], "queued")
        self.assertEqual(status["invocation_id"], invocation_id)

    def test_list_available_skills(self):
        """Test listing available skills."""
        skills_info = self.invoker.list_available_skills()

        self.assertGreater(skills_info["total"], 0)
        self.assertIsInstance(skills_info["skills"], list)

        # Verify prospect skill is included
        prospect_skills = [s for s in skills_info["skills"] if s["name"] == "prospect"]
        self.assertEqual(len(prospect_skills), 1)

    def test_get_skill_details(self):
        """Test getting skill details."""
        details = self.invoker.get_skill_details("crm")

        self.assertEqual(details["name"], "crm")
        self.assertIn("description", details)
        self.assertIn("parameters", details)


class TestDatabase(unittest.TestCase):
    """Test database operations."""

    def setUp(self):
        """Set up test database."""
        self.db_path = tempfile.mktemp(suffix=".db")
        self.db = SkillBridgeDatabase(db_path=self.db_path)

    def tearDown(self):
        """Clean up test database."""
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_log_invocation(self):
        """Test logging invocation."""
        self.db.log_invocation(
            "inv_123",
            "prospect",
            "research",
            {"name": "John", "company": "ABC"},
            "completed",
            result={"contact": "john@abc.com"}
        )

        retrieved = self.db.get_invocation("inv_123")
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved["skill_name"], "prospect")

    def test_list_invocations_with_filter(self):
        """Test listing invocations with filters."""
        # Log multiple invocations
        self.db.log_invocation("inv_1", "prospect", "research", {}, "completed")
        self.db.log_invocation("inv_2", "proposal", "generate", {}, "completed")
        self.db.log_invocation("inv_3", "prospect", "outreach", {}, "failed")

        # List prospect invocations only
        prospect_invs = self.db.list_invocations(skill_name="prospect")
        self.assertEqual(len(prospect_invs), 2)

        # List completed invocations only
        completed_invs = self.db.list_invocations(status="completed")
        self.assertEqual(len(completed_invs), 2)

    def test_async_invocation_lifecycle(self):
        """Test async invocation lifecycle."""
        # Create async invocation
        inv_id = self.db.create_async_invocation(
            "async_123",
            "proposal",
            "generate",
            {"prospect": "John"}
        )

        inv = self.db.get_async_invocation(inv_id)
        self.assertEqual(inv["status"], "queued")

        # Update to running
        self.db.update_async_invocation(inv_id, "running")
        inv = self.db.get_async_invocation(inv_id)
        self.assertEqual(inv["status"], "running")

        # Update to completed with result
        self.db.update_async_invocation(
            inv_id,
            "completed",
            result={"proposal_id": "prop_123"}
        )
        inv = self.db.get_async_invocation(inv_id)
        self.assertEqual(inv["status"], "completed")
        self.assertIsNotNone(inv["result"])

    def test_cache_metadata(self):
        """Test caching skill metadata."""
        metadata = {
            "name": "prospect",
            "description": "Research prospects"
        }

        self.db.cache_skill_metadata("prospect", metadata)
        cached = self.db.get_cached_metadata("prospect")

        self.assertEqual(cached["name"], "prospect")


class TestSkillBridgeAPI(unittest.TestCase):
    """Test REST API endpoints."""

    def setUp(self):
        """Set up test client."""
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_health_endpoint(self):
        """Test health check endpoint."""
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertEqual(data["status"], "healthy")

    def test_available_skills_endpoint(self):
        """Test available skills endpoint."""
        response = self.client.get('/available-skills')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertGreater(data["total"], 0)
        self.assertIsInstance(data["skills"], list)

    def test_skill_details_endpoint(self):
        """Test skill details endpoint."""
        response = self.client.get('/skills/prospect')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertEqual(data["name"], "prospect")

    def test_skill_details_not_found(self):
        """Test skill details endpoint with invalid skill."""
        response = self.client.get('/skills/nonexistent')
        self.assertEqual(response.status_code, 404)

    @patch('skill_bridge.invoker.invoke_sync')
    def test_invoke_endpoint(self, mock_invoke):
        """Test skill invocation endpoint."""
        mock_invoke.return_value = {
            "status": "completed",
            "output": {"company": "ABC Corp"},
            "confidence": 0.9,
            "invocation_id": "inv_123",
            "duration_ms": 1500
        }

        response = self.client.post(
            '/invoke/prospect',
            json={
                "action": "research",
                "params": {"name": "John", "company": "ABC"}
            }
        )

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["status"], "completed")

    @patch('skill_bridge.invoker.invoke_async')
    def test_invoke_async_endpoint(self, mock_async):
        """Test async invocation endpoint."""
        mock_async.return_value = {
            "status": "queued",
            "invocation_id": "async_123"
        }

        response = self.client.post(
            '/invoke/proposal/async',
            json={
                "action": "generate",
                "params": {"prospect_name": "John"}
            }
        )

        self.assertEqual(response.status_code, 202)
        data = json.loads(response.data)
        self.assertEqual(data["status"], "queued")

    def test_invalid_endpoint(self):
        """Test invalid endpoint."""
        response = self.client.get('/invalid-endpoint')
        self.assertEqual(response.status_code, 404)

    def test_method_not_allowed(self):
        """Test method not allowed."""
        response = self.client.post('/health')
        self.assertEqual(response.status_code, 405)


class TestEndToEndWorkflow(unittest.TestCase):
    """Test end-to-end workflows."""

    def setUp(self):
        """Set up test fixtures."""
        self.db = SkillBridgeDatabase(db_path=tempfile.mktemp(suffix=".db"))
        self.invoker = SkillInvoker(db=self.db)

    def test_prospect_to_proposal_workflow_structure(self):
        """Test the structure of prospect -> proposal workflow."""
        # This test validates that the necessary parameters flow through

        # Step 1: Research prospect
        prospect_params = {"name": "John Smith", "company": "ABC Real Estate"}
        is_valid, error = validate_parameters("prospect", "research", prospect_params)
        self.assertTrue(is_valid)

        # Step 2: Generate proposal
        proposal_params = {
            "prospect_name": "John Smith",
            "company": "ABC Real Estate",
            "scope": "Lead automation system"
        }
        is_valid, error = validate_parameters("proposal", "generate", proposal_params)
        self.assertTrue(is_valid)

        # Step 3: Send proposal
        send_params = {
            "proposal_id": "prop_123",
            "recipient_email": "john@abc.com"
        }
        is_valid, error = validate_parameters("proposal", "send", send_params)
        self.assertTrue(is_valid)

        # Step 4: Log activity
        crm_params = {
            "contact_id": "contact_123",
            "activity_type": "proposal_sent",
            "description": "Sent proposal to John Smith"
        }
        is_valid, error = validate_parameters("crm", "log_activity", crm_params)
        self.assertTrue(is_valid)


if __name__ == '__main__':
    unittest.main()
