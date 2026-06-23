#!/usr/bin/env python3
"""
Integration tests demonstrating skill executor with real-world workflows.
These tests verify that the skill executor can handle complete end-to-end workflows.
"""

import unittest
import json
from skill_executor import SkillExecutor
from skill_invoker import SkillInvoker
from bridge_database import SkillBridgeDatabase
import tempfile
import os


class TestSkillIntegration(unittest.TestCase):
    """Test skill executor in realistic scenarios."""

    def setUp(self):
        """Set up test fixtures with temporary database."""
        # Create temporary database
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.db_path = self.temp_db.name

        # Initialize components
        self.executor = SkillExecutor(timeout=30)
        self.db = SkillBridgeDatabase(db_path=self.db_path)
        self.invoker = SkillInvoker(db=self.db, executor=self.executor)

    def tearDown(self):
        """Clean up temporary database."""
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_prospect_research_workflow(self):
        """Test a complete prospect research workflow."""
        # Simulate prospect research output
        research_output = """
        Company: TechCorp Inc
        Industry: Software Development
        Founded: 2015
        Employees: 150+

        Key Contacts:
        John Smith - john.smith@techcorp.com
        Jane Doe - jane.doe@techcorp.com

        Social Links:
        LinkedIn: https://linkedin.com/in/john-smith-12345
        Website: https://techcorp.com
        """

        # Parse the output
        result = self.executor._parse_prospect_research(research_output)

        # Verify structure
        self.assertEqual(result["status"], "success")
        self.assertGreater(result["confidence"], 0.7)
        self.assertIn("company_info", result["output"])
        self.assertIn("contacts", result["output"])
        self.assertIn("social_links", result["output"])

        # Verify extracted data
        self.assertGreater(len(result["output"]["contacts"]), 0)
        emails = [c.get("email") for c in result["output"]["contacts"]]
        self.assertIn("john.smith@techcorp.com", emails)
        self.assertIn("jane.doe@techcorp.com", emails)

    def test_proposal_generation_workflow(self):
        """Test proposal generation and tracking."""
        # Simulate proposal generation
        proposal_output = """
        Proposal Generation Complete
        Proposal ID: PROP_2024_001
        Estimated Price: $15,000
        Document URL: https://docs.example.com/proposals/PROP_2024_001.pdf

        Scope:
        - Lead automation system
        - CRM integration
        - Email automation

        Timeline: 8 weeks
        """

        result = self.executor._parse_proposal_generate(proposal_output)

        self.assertEqual(result["status"], "success")
        self.assertGreater(result["confidence"], 0.7)
        self.assertEqual(result["output"]["proposal_id"], "PROP_2024_001")
        self.assertEqual(result["output"]["estimated_price"], "$15,000")
        self.assertIsNotNone(result["output"]["document_url"])

    def test_proposal_send_workflow(self):
        """Test sending a proposal."""
        send_output = """
        Email sent successfully
        Sent at: 2024-01-15T10:30:00
        Recipient: john@example.com
        Tracking ID: track_abc123xyz
        Subject: Your Custom Proposal - TechCorp Inc
        """

        result = self.executor._parse_proposal_send(send_output)

        self.assertEqual(result["status"], "success")
        self.assertTrue(result["output"]["sent"])
        self.assertIsNotNone(result["output"]["sent_at"])
        self.assertEqual(result["output"]["tracking_id"], "track_abc123xyz")

    def test_crm_activity_logging_workflow(self):
        """Test logging activity in CRM."""
        log_output = """
        Activity logged successfully
        Activity ID: ACT_2024_001
        Logged at: 2024-01-15T14:30:00
        Contact: John Smith
        Type: Proposal Sent
        Duration: N/A
        Notes: Sent initial proposal for lead automation
        Status: Completed
        """

        result = self.executor._parse_crm_log_activity(log_output)

        self.assertEqual(result["status"], "success")
        self.assertGreater(result["confidence"], 0.7)
        self.assertEqual(result["output"]["activity_id"], "ACT_2024_001")
        self.assertIsNotNone(result["output"]["logged_at"])

    def test_contact_update_workflow(self):
        """Test updating contact information."""
        update_output = """
        Contact updated successfully
        Contact ID: CONT_123
        Updated fields:
        - name: John Smith (updated)
        - email: john.smith@newcorp.com
        - phone: +1-555-1234
        - company: NewCorp Inc
        """

        result = self.executor._parse_crm_update_contact(update_output)

        self.assertTrue(result["output"]["updated"])
        self.assertEqual(result["output"]["contact_id"], "CONT_123")
        self.assertIn("email", result["output"]["updated_fields"])

    def test_email_send_workflow(self):
        """Test sending an email."""
        email_output = """
        Email sent successfully
        Message ID: msg_xyz789
        Sent at: 2024-01-15T15:45:00
        To: john@example.com
        Subject: Follow-up: Your Proposal Review
        Status: Delivered
        """

        result = self.executor._parse_send_email(email_output)

        self.assertEqual(result["status"], "success")
        self.assertTrue(result["output"]["sent"])
        self.assertIsNotNone(result["output"]["message_id"])

    def test_task_creation_workflow(self):
        """Test creating a task."""
        task_output = """
        Task created successfully
        Task ID: TASK_2024_001
        Created at: 2024-01-15T16:00:00
        Title: Follow up with John Smith
        Priority: High
        Due date: 2024-01-22
        Assignee: Sarah Johnson
        """

        result = self.executor._parse_tasks_create(task_output)

        self.assertEqual(result["status"], "success")
        self.assertGreater(result["confidence"], 0.7)
        self.assertEqual(result["output"]["task_id"], "TASK_2024_001")
        self.assertIsNotNone(result["output"]["created_at"])

    def test_complete_workflow_pipeline(self):
        """Test a complete pipeline: research -> proposal -> send -> log."""
        # Step 1: Research
        research_output = """
        Company: ABC Real Estate
        Founded: 2010
        Contacts: john@abc.com, jane@abc.com
        LinkedIn: https://linkedin.com/in/john-doe
        """

        research_result = self.executor._parse_prospect_research(research_output)
        self.assertEqual(research_result["status"], "success")

        # Step 2: Generate Proposal
        proposal_output = """
        Proposal ID: PROP_2024_ABC
        Estimated Price: $10,000
        URL: https://docs.example.com/PROP_2024_ABC.pdf
        """

        proposal_result = self.executor._parse_proposal_generate(proposal_output)
        self.assertEqual(proposal_result["status"], "success")
        proposal_id = proposal_result["output"]["proposal_id"]

        # Step 3: Send Proposal
        send_output = """
        Email sent successfully
        Sent to: john@abc.com
        Tracking ID: track_123456
        Sent at: 2024-01-15T10:00:00
        """

        send_result = self.executor._parse_proposal_send(send_output)
        self.assertEqual(send_result["status"], "success")

        # Step 4: Log Activity
        log_output = """
        Activity logged
        Activity ID: ACT_2024_ABC
        Type: Proposal Sent
        Logged at: 2024-01-15T10:05:00
        """

        log_result = self.executor._parse_crm_log_activity(log_output)
        self.assertEqual(log_result["status"], "success")

        # Verify workflow completion
        pipeline_results = {
            "research": research_result,
            "proposal": proposal_result,
            "send": send_result,
            "log": log_result
        }

        completed = sum(1 for r in pipeline_results.values() if r["status"] == "success")
        self.assertEqual(completed, 4)

    def test_error_recovery_workflow(self):
        """Test error handling and recovery."""
        # Simulate a missing email error
        error_output = """
        Error: Invalid email address
        Field: recipient_email
        Value: invalid-email
        Please provide a valid email address.
        """

        result = self.executor._parse_generic(error_output, "proposal", "send")

        self.assertEqual(result["status"], "error")
        self.assertLess(result["confidence"], 0.8)

    def test_partial_success_workflow(self):
        """Test handling of partial successes."""
        partial_output = """
        Partially completed
        Contacts found: 2
        Company info: Retrieved
        Social links: Not found
        """

        result = self.executor._parse_prospect_research(partial_output)

        # Should still be successful if we got contacts and company info
        self.assertIn(result["status"], ["success", "partial"])
        self.assertGreater(result["confidence"], 0.4)

    def test_json_response_handling(self):
        """Test handling of JSON responses from skills."""
        json_output = """
        Here's the structured result:

        ```json
        {
            "status": "success",
            "prospect_id": "PROSP_123",
            "company": "TechCorp",
            "contacts": [
                {"name": "John", "email": "john@techcorp.com"},
                {"name": "Jane", "email": "jane@techcorp.com"}
            ],
            "confidence": 0.95
        }
        ```
        """

        result = self.executor._parse_skill_output("prospect", "research", json_output)

        self.assertEqual(result["status"], "success")
        self.assertEqual(result["confidence"], 0.95)
        output = result["output"]
        self.assertEqual(output["prospect_id"], "PROSP_123")
        self.assertEqual(len(output["contacts"]), 2)

    def test_database_invocation_tracking(self):
        """Test that skill invocations are properly tracked in database."""
        # Log an invocation
        self.db.log_invocation(
            invocation_id="test_123",
            skill_name="prospect",
            action="research",
            params={"name": "John", "company": "ABC"},
            status="completed",
            result={"company_info": {"name": "ABC Corp"}},
            duration_ms=1500
        )

        # Retrieve the invocation
        invocation = self.db.get_invocation("test_123")

        self.assertIsNotNone(invocation)
        self.assertEqual(invocation["skill_name"], "prospect")
        self.assertEqual(invocation["action"], "research")
        self.assertEqual(invocation["status"], "completed")
        self.assertEqual(invocation["duration_ms"], 1500)

    def test_database_filtering_by_skill(self):
        """Test filtering invocations by skill name."""
        # Log multiple invocations
        self.db.log_invocation(
            invocation_id="inv_001",
            skill_name="prospect",
            action="research",
            params={},
            status="completed"
        )

        self.db.log_invocation(
            invocation_id="inv_002",
            skill_name="proposal",
            action="generate",
            params={},
            status="completed"
        )

        # Filter by skill
        prospect_invocations = self.db.list_invocations(skill_name="prospect")

        self.assertEqual(len(prospect_invocations), 1)
        self.assertEqual(prospect_invocations[0]["skill_name"], "prospect")

    def test_skill_invoker_integration(self):
        """Test the SkillInvoker integration with executor and database."""
        # Verify invoker is properly configured
        self.assertIsNotNone(self.invoker.executor)
        self.assertIsNotNone(self.invoker.db)
        self.assertIsInstance(self.invoker.executor, SkillExecutor)

    def test_response_confidence_scoring(self):
        """Test confidence scoring across different parsers."""
        # High confidence - JSON response
        json_result = self.executor._parse_skill_output(
            "proposal",
            "generate",
            '{"proposal_id": "P123", "price": "$5000"}'
        )
        self.assertEqual(json_result["confidence"], 0.95)

        # Good confidence - well-formed text
        text_result = self.executor._parse_proposal_generate(
            "Proposal ID: PROP_001\nPrice: $5000"
        )
        self.assertGreater(text_result["confidence"], 0.7)

        # Lower confidence - minimal info
        minimal_result = self.executor._parse_generic(
            "Something happened", "unknown", "action"
        )
        self.assertLess(minimal_result["confidence"], 0.7)


class TestExecutorPromptBuilding(unittest.TestCase):
    """Test skill prompt building."""

    def setUp(self):
        """Set up test fixtures."""
        self.executor = SkillExecutor()

    def test_simple_parameters(self):
        """Test building prompt with simple parameters."""
        prompt = self.executor._build_skill_prompt(
            "send",
            "email",
            {
                "to": "john@example.com",
                "subject": "Test",
                "body": "Test email"
            }
        )

        self.assertIn("send", prompt)
        self.assertIn("email", prompt)
        self.assertIn("john@example.com", prompt)
        self.assertIn("Test", prompt)

    def test_complex_parameters(self):
        """Test building prompt with complex parameters."""
        prompt = self.executor._build_skill_prompt(
            "proposal",
            "generate",
            {
                "prospect_name": "John Smith",
                "company": "Acme Corp",
                "scope": "Lead automation",
                "budget": 10000,
                "timeline": "4 weeks",
                "features": ["Email automation", "Lead tracking"]
            }
        )

        self.assertIn("prospect_name", prompt)
        self.assertIn("Lead automation", prompt)
        self.assertIn("features", prompt)


if __name__ == "__main__":
    unittest.main()
