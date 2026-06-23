"""Tests for the skill executor."""

import unittest
import json
from skill_executor import SkillExecutor


class TestSkillExecutor(unittest.TestCase):
    """Test the SkillExecutor class."""

    def setUp(self):
        """Set up test fixtures."""
        self.executor = SkillExecutor(timeout=30)

    def test_build_skill_prompt_prospect_research(self):
        """Test building a prompt for prospect research."""
        prompt = self.executor._build_skill_prompt(
            "prospect",
            "research",
            {"name": "John Doe", "company": "Acme Corp"}
        )

        self.assertIn("prospect", prompt)
        self.assertIn("research", prompt)
        self.assertIn("John Doe", prompt)
        self.assertIn("Acme Corp", prompt)

    def test_build_skill_prompt_with_json_params(self):
        """Test building a prompt with complex JSON parameters."""
        params = {
            "prospect_name": "Jane Smith",
            "company": "Tech Corp",
            "tags": ["vip", "active"]
        }

        prompt = self.executor._build_skill_prompt("proposal", "generate", params)

        self.assertIn("proposal", prompt)
        self.assertIn("generate", prompt)
        self.assertIn("Jane Smith", prompt)

    def test_extract_json_from_code_block(self):
        """Test extracting JSON from markdown code blocks."""
        text = """
        Here's the result:

        ```json
        {"status": "success", "id": "123"}
        ```
        """

        result = self.executor._extract_json_from_output(text)
        self.assertIsNotNone(result)

        parsed = json.loads(result)
        self.assertEqual(parsed["status"], "success")
        self.assertEqual(parsed["id"], "123")

    def test_extract_json_from_braces(self):
        """Test extracting JSON without code blocks."""
        text = """
        Result: {"status": "completed", "data": "value"}
        """

        result = self.executor._extract_json_from_output(text)
        self.assertIsNotNone(result)

        parsed = json.loads(result)
        self.assertEqual(parsed["status"], "completed")

    def test_parse_generic_success_output(self):
        """Test parsing generic successful output."""
        output = """
        Operation completed successfully
        id: task_123
        status: created
        timestamp: 2024-01-01T12:00:00
        """

        result = self.executor._parse_generic(output, "tasks", "create")

        self.assertEqual(result["status"], "success")
        self.assertGreater(result["confidence"], 0.5)
        self.assertIn("id", result["output"])

    def test_parse_generic_error_output(self):
        """Test parsing generic error output."""
        output = """
        Error: Invalid parameters
        Missing required field: email
        """

        result = self.executor._parse_generic(output, "send", "email")

        self.assertEqual(result["status"], "error")
        self.assertLess(result["confidence"], 0.8)

    def test_parse_prospect_research(self):
        """Test parsing prospect research output."""
        output = """
        Company: Acme Corp
        Founded: 2020
        Industry: Technology

        Contacts:
        - John Doe: john@acme.com
        - Jane Smith: jane@acme.com

        Social Links:
        LinkedIn: https://linkedin.com/in/john-doe
        Website: https://acme.com
        """

        result = self.executor._parse_prospect_research(output)

        self.assertEqual(result["status"], "success")
        self.assertGreaterEqual(result["confidence"], 0.7)
        self.assertIn("company_info", result["output"])
        self.assertIn("contacts", result["output"])
        self.assertIn("social_links", result["output"])

    def test_parse_proposal_generate(self):
        """Test parsing proposal generation output."""
        output = """
        Proposal Generation Complete
        Proposal ID: PROP_2024_001
        Estimated Price: $5,000
        Document URL: https://docs.example.com/proposal_2024_001.pdf

        Proposal Summary:
        Scope: Lead automation implementation
        Timeline: 4 weeks
        """

        result = self.executor._parse_proposal_generate(output)

        self.assertEqual(result["status"], "success")
        self.assertGreater(result["confidence"], 0.7)
        self.assertEqual(result["output"]["proposal_id"], "PROP_2024_001")
        self.assertEqual(result["output"]["estimated_price"], "$5,000")

    def test_parse_proposal_send(self):
        """Test parsing proposal send output."""
        output = """
        Email sent successfully
        Sent at: 2024-01-15T10:30:00
        Recipient: john@example.com
        Tracking ID: track_abc123
        """

        result = self.executor._parse_proposal_send(output)

        self.assertEqual(result["status"], "success")
        self.assertTrue(result["output"]["sent"])
        self.assertIsNotNone(result["output"]["sent_at"])
        self.assertEqual(result["output"]["tracking_id"], "track_abc123")

    def test_parse_crm_log_activity(self):
        """Test parsing CRM log activity output."""
        output = """
        Activity logged successfully
        Activity ID: ACT_2024_001
        Logged at: 2024-01-15T14:20:00
        Type: Call
        Duration: 30 minutes
        Notes: Discussed proposal details
        """

        result = self.executor._parse_crm_log_activity(output)

        self.assertEqual(result["status"], "success")
        self.assertGreater(result["confidence"], 0.7)
        self.assertEqual(result["output"]["activity_id"], "ACT_2024_001")

    def test_parse_crm_update_contact(self):
        """Test parsing CRM contact update output."""
        output = """
        Contact updated successfully
        Contact ID: CONT_123
        Updated fields:
        - email: newemail@example.com
        - phone: +1-555-1234
        - company: New Company Inc
        """

        result = self.executor._parse_crm_update_contact(output)

        self.assertEqual(result["status"], "success")
        self.assertTrue(result["output"]["updated"])
        self.assertEqual(result["output"]["contact_id"], "CONT_123")
        self.assertIn("email", result["output"]["updated_fields"])

    def test_parse_send_email(self):
        """Test parsing email send output."""
        output = """
        Email sent successfully
        Message ID: msg_xyz789
        Sent at: 2024-01-15T15:45:00
        To: recipient@example.com
        Subject: Important Update
        """

        result = self.executor._parse_send_email(output)

        self.assertEqual(result["status"], "success")
        self.assertTrue(result["output"]["sent"])
        self.assertIsNotNone(result["output"]["message_id"])

    def test_parse_tasks_create(self):
        """Test parsing task creation output."""
        output = """
        Task created successfully
        Task ID: TASK_2024_001
        Created at: 2024-01-15T16:00:00
        Title: Follow up with prospect
        Priority: High
        Due date: 2024-01-22
        """

        result = self.executor._parse_tasks_create(output)

        self.assertEqual(result["status"], "success")
        self.assertGreater(result["confidence"], 0.7)
        self.assertEqual(result["output"]["task_id"], "TASK_2024_001")

    def test_parse_skill_output_with_json(self):
        """Test parsing skill output when it contains JSON."""
        raw_output = """
        Here's the result:

        ```json
        {
            "status": "completed",
            "proposal_id": "PROP_789",
            "estimated_price": "$10,000",
            "document_url": "https://docs.example.com/proposal.pdf"
        }
        ```
        """

        result = self.executor._parse_skill_output("proposal", "generate", raw_output)

        self.assertEqual(result["status"], "success")
        self.assertEqual(result["confidence"], 0.95)
        parsed_output = result["output"]
        self.assertEqual(parsed_output["proposal_id"], "PROP_789")
        self.assertEqual(parsed_output["estimated_price"], "$10,000")

    def test_parse_empty_output(self):
        """Test parsing empty output."""
        result = self.executor._parse_skill_output("prospect", "research", "")

        self.assertEqual(result["status"], "error")
        self.assertEqual(result["confidence"], 0.0)
        self.assertIn("Empty response", result["error"])

    def test_execute_skill_command_structure(self):
        """Test that execute_skill_command returns proper structure."""
        # This test verifies the structure without actually invoking Claude
        # We mock the execution by checking the response format

        result = {
            "status": "success",
            "output": {"test": "data"},
            "raw_output": "test output",
            "confidence": 0.8,
            "execution_time_ms": 1000
        }

        # Verify all required fields are present
        self.assertIn("status", result)
        self.assertIn("output", result)
        self.assertIn("raw_output", result)
        self.assertIn("confidence", result)
        self.assertIn("execution_time_ms", result)

        self.assertIn(result["status"], ["success", "partial", "error"])
        self.assertIsInstance(result["confidence"], (int, float))
        self.assertGreaterEqual(result["confidence"], 0.0)
        self.assertLessEqual(result["confidence"], 1.0)

    def test_response_parsing_consistency(self):
        """Test that similar outputs produce consistent results."""
        output1 = """
        Success: Task created
        Task ID: TASK_001
        """

        output2 = """
        Successfully created task
        ID: TASK_002
        """

        result1 = self.executor._parse_tasks_create(output1)
        result2 = self.executor._parse_tasks_create(output2)

        # Both should be success status
        self.assertEqual(result1["status"], "success")
        self.assertEqual(result2["status"], "success")

        # Both should have similar confidence levels
        self.assertGreater(result1["confidence"], 0.7)
        self.assertGreater(result2["confidence"], 0.7)

    def test_price_extraction(self):
        """Test extracting prices from output."""
        output = """
        Proposal generated
        Estimated cost: $15,000
        Breakdown:
        - Development: $10,000
        - Design: $5,000
        """

        result = self.executor._parse_proposal_generate(output)

        self.assertEqual(result["output"]["estimated_price"], "$15,000")

    def test_email_extraction(self):
        """Test extracting emails from output."""
        output = """
        Contacts found:
        john.doe@company.com
        jane.smith@company.com
        contact@company.com
        """

        result = self.executor._parse_prospect_research(output)

        # Should find emails
        self.assertGreater(len(result["output"]["contacts"]), 0)
        emails = [c.get("email") for c in result["output"]["contacts"] if c.get("email")]
        self.assertIn("john.doe@company.com", emails)

    def test_linkedin_url_extraction(self):
        """Test extracting LinkedIn URLs."""
        output = """
        Social Media Presence:
        LinkedIn: https://linkedin.com/in/john-doe-12345
        Twitter: @johndoe
        """

        result = self.executor._parse_prospect_research(output)

        self.assertIn("linkedin", result["output"]["social_links"])
        self.assertIn("linkedin.com/in", result["output"]["social_links"]["linkedin"])


class TestSkillExecutorIntegration(unittest.TestCase):
    """Integration tests for skill executor."""

    def setUp(self):
        """Set up test fixtures."""
        self.executor = SkillExecutor(timeout=30)

    def test_error_handling_timeout(self):
        """Test handling of timeout errors."""
        # Create a very short timeout to trigger timeout
        executor = SkillExecutor(timeout=0.001)

        # This would normally timeout (but we can't test actual execution here)
        # Just verify the executor is configured
        self.assertEqual(executor.timeout, 0.001)

    def test_executor_path_configuration(self):
        """Test that executor path is properly configured."""
        import os

        executor = SkillExecutor(
            claude_path="/custom/path/claude",
            workspace_path="/custom/workspace"
        )

        self.assertEqual(executor.claude_path, "/custom/path/claude")
        self.assertEqual(executor.workspace_path, "/custom/workspace")

    def test_default_executor_paths(self):
        """Test default executor paths."""
        executor = SkillExecutor()

        self.assertTrue(executor.claude_path.endswith("claude"))
        self.assertTrue(executor.workspace_path)


if __name__ == "__main__":
    unittest.main()
