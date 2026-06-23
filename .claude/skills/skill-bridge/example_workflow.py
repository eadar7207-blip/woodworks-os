#!/usr/bin/env python3
"""
Example: Complete End-to-End Workflow
Demonstrates: Research → Proposal → Send → Log

This example shows how to use Skill Bridge to execute a complete
prospect workflow without subprocess calls.
"""

import requests
import json
import time
from typing import Dict, Any


class SkillBridgeClient:
    """Simple client for Skill Bridge API."""

    def __init__(self, base_url: str = "http://localhost:9000", api_key: str = None):
        self.base_url = base_url
        self.headers = {"Content-Type": "application/json"}
        if api_key:
            self.headers["Authorization"] = f"Bearer {api_key}"

    def health_check(self) -> bool:
        """Check if Skill Bridge is running."""
        try:
            response = requests.get(f"{self.base_url}/health", headers=self.headers)
            return response.status_code == 200
        except requests.exceptions.ConnectionError:
            return False

    def invoke_skill(self, skill_name: str, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Invoke a skill synchronously."""
        url = f"{self.base_url}/invoke/{skill_name}"
        response = requests.post(
            url,
            json={"action": action, "params": params},
            headers=self.headers,
            timeout=60
        )
        response.raise_for_status()
        return response.json()

    def invoke_skill_async(self, skill_name: str, action: str, params: Dict[str, Any]) -> str:
        """Queue a skill for async execution and return invocation ID."""
        url = f"{self.base_url}/invoke/{skill_name}/async"
        response = requests.post(
            url,
            json={"action": action, "params": params},
            headers=self.headers
        )
        response.raise_for_status()
        result = response.json()
        return result["invocation_id"]

    def get_status(self, invocation_id: str) -> Dict[str, Any]:
        """Get the status of an async invocation."""
        url = f"{self.base_url}/status/{invocation_id}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def wait_for_completion(self, invocation_id: str, timeout: int = 300) -> Dict[str, Any]:
        """Wait for async invocation to complete."""
        start_time = time.time()

        while time.time() - start_time < timeout:
            status = self.get_status(invocation_id)

            if status["status"] in ["completed", "failed"]:
                return status

            print(f"  Status: {status['status']}... waiting")
            time.sleep(2)

        raise TimeoutError(f"Invocation {invocation_id} timed out after {timeout} seconds")


class ProspectWorkflow:
    """Complete prospect workflow using Skill Bridge."""

    def __init__(self, client: SkillBridgeClient):
        self.client = client

    def execute(self, prospect_name: str, company: str, email: str = None) -> Dict[str, Any]:
        """Execute complete prospect workflow.

        Steps:
        1. Research prospect
        2. Generate proposal
        3. Send proposal (if email provided)
        4. Log activity in CRM

        Args:
            prospect_name: Name of prospect
            company: Company name
            email: Prospect email (optional)

        Returns:
            Dict with results from all steps
        """

        print(f"\n{'='*60}")
        print(f"PROSPECT WORKFLOW: {prospect_name} @ {company}")
        print(f"{'='*60}\n")

        results = {
            "prospect_name": prospect_name,
            "company": company,
            "steps": {}
        }

        # Step 1: Research Prospect
        print("Step 1: Researching prospect...")
        try:
            research_result = self.client.invoke_skill(
                "prospect",
                "research",
                {"name": prospect_name, "company": company}
            )

            results["steps"]["research"] = research_result
            print(f"  Status: {research_result['status']}")
            print(f"  Confidence: {research_result.get('confidence', 'N/A')}")
            print(f"  Duration: {research_result.get('duration_ms', 'N/A')}ms")

            if research_result["status"] not in ["completed", "success"]:
                print(f"  Error: {research_result.get('error', 'Unknown error')}")
                return results

            prospect_info = research_result.get("output", {})
            print(f"  Company info: {prospect_info.get('company_info', {})}")

            # Extract email if not provided
            if not email and prospect_info.get("contacts"):
                email = prospect_info["contacts"][0].get("email")
                print(f"  Extracted email: {email}")

        except Exception as e:
            print(f"  ERROR: {e}")
            results["steps"]["research"] = {"status": "error", "error": str(e)}
            return results

        # Step 2: Generate Proposal
        print("\nStep 2: Generating proposal...")
        try:
            proposal_result = self.client.invoke_skill(
                "proposal",
                "generate",
                {
                    "prospect_name": prospect_name,
                    "company": company,
                    "scope": "Lead automation system"
                }
            )

            results["steps"]["proposal"] = proposal_result
            print(f"  Status: {proposal_result['status']}")
            print(f"  Confidence: {proposal_result.get('confidence', 'N/A')}")
            print(f"  Duration: {proposal_result.get('duration_ms', 'N/A')}ms")

            if proposal_result["status"] not in ["completed", "success"]:
                print(f"  Error: {proposal_result.get('error', 'Unknown error')}")
                return results

            proposal_output = proposal_result.get("output", {})
            proposal_id = proposal_output.get("proposal_id")
            estimated_price = proposal_output.get("estimated_price")

            print(f"  Proposal ID: {proposal_id}")
            print(f"  Estimated Price: {estimated_price}")

        except Exception as e:
            print(f"  ERROR: {e}")
            results["steps"]["proposal"] = {"status": "error", "error": str(e)}
            return results

        # Step 3: Send Proposal
        if email:
            print(f"\nStep 3: Sending proposal to {email}...")
            try:
                send_result = self.client.invoke_skill(
                    "proposal",
                    "send",
                    {
                        "proposal_id": proposal_id,
                        "recipient_email": email
                    }
                )

                results["steps"]["send"] = send_result
                print(f"  Status: {send_result['status']}")
                print(f"  Sent at: {send_result.get('output', {}).get('sent_at', 'N/A')}")

            except Exception as e:
                print(f"  ERROR: {e}")
                results["steps"]["send"] = {"status": "error", "error": str(e)}
        else:
            print("\nStep 3: Skipped (no email provided)")

        # Step 4: Log CRM Activity
        print("\nStep 4: Logging CRM activity...")
        try:
            crm_result = self.client.invoke_skill(
                "crm",
                "log_activity",
                {
                    "contact_id": f"contact_{prospect_name.replace(' ', '_').lower()}",
                    "activity_type": "proposal_generated",
                    "description": f"Generated and sent proposal to {prospect_name} at {company}"
                }
            )

            results["steps"]["crm_log"] = crm_result
            print(f"  Status: {crm_result['status']}")
            print(f"  Activity ID: {crm_result.get('output', {}).get('activity_id', 'N/A')}")

        except Exception as e:
            print(f"  ERROR: {e}")
            results["steps"]["crm_log"] = {"status": "error", "error": str(e)}

        # Summary
        print(f"\n{'='*60}")
        print("WORKFLOW SUMMARY")
        print(f"{'='*60}")
        completed = sum(1 for s in results["steps"].values() if s.get("status") in ["completed", "success"])
        total = len(results["steps"])
        print(f"Steps completed: {completed}/{total}")

        for step_name, step_result in results["steps"].items():
            status_symbol = "✓" if step_result.get("status") in ["completed", "success"] else "✗"
            print(f"  {status_symbol} {step_name}: {step_result.get('status', 'unknown')}")

        results["summary"] = {
            "completed_steps": completed,
            "total_steps": total,
            "success": completed == total
        }

        return results


class AsyncWorkflowExample:
    """Example of using async invocation for long-running skills."""

    def __init__(self, client: SkillBridgeClient):
        self.client = client

    def execute_long_running_proposal(self, prospect_name: str, company: str):
        """Queue a long-running proposal generation and wait for completion."""

        print(f"\n{'='*60}")
        print("ASYNC WORKFLOW: Long-Running Proposal Generation")
        print(f"{'='*60}\n")

        # Queue async invocation
        print("Queuing async proposal generation...")
        invocation_id = self.client.invoke_skill_async(
            "proposal",
            "generate",
            {
                "prospect_name": prospect_name,
                "company": company,
                "scope": "Advanced lead automation with AI"
            }
        )

        print(f"Invocation ID: {invocation_id}\n")
        print("Waiting for completion (polling)...")

        # Wait for completion
        final_status = self.client.wait_for_completion(invocation_id, timeout=300)

        print(f"\nFinal Status: {final_status['status']}")

        if final_status["status"] == "completed":
            output = final_status.get("output", {})
            print(f"Proposal ID: {output.get('proposal_id')}")
            print(f"Estimated Price: {output.get('estimated_price')}")
        else:
            print(f"Error: {final_status.get('error')}")

        return final_status


def main():
    """Run complete workflow examples."""

    # Initialize client
    print("Initializing Skill Bridge client...")
    client = SkillBridgeClient()

    # Check health
    if not client.health_check():
        print("ERROR: Cannot connect to Skill Bridge")
        print("Make sure Skill Bridge is running: python3 skill_bridge.py")
        return

    print("✓ Skill Bridge is running\n")

    # Example 1: Complete synchronous workflow
    print("\n" + "="*60)
    print("EXAMPLE 1: Complete Synchronous Workflow")
    print("="*60)

    workflow = ProspectWorkflow(client)
    result1 = workflow.execute(
        prospect_name="John Smith",
        company="ABC Real Estate",
        email="john@abc.com"
    )

    # Example 2: Another prospect
    print("\n\n" + "="*60)
    print("EXAMPLE 2: Another Prospect")
    print("="*60)

    result2 = workflow.execute(
        prospect_name="Jane Doe",
        company="XYZ Properties"
    )

    # Example 3: Async workflow
    print("\n\n" + "="*60)
    print("EXAMPLE 3: Async Workflow (Long-Running)")
    print("="*60)

    async_workflow = AsyncWorkflowExample(client)
    result3 = async_workflow.execute_long_running_proposal(
        prospect_name="Bob Wilson",
        company="123 Realty Group"
    )

    # Final summary
    print("\n\n" + "="*60)
    print("FINAL SUMMARY")
    print("="*60)
    print(f"Example 1: {'PASSED' if result1['summary']['success'] else 'FAILED'}")
    print(f"Example 2: {'PASSED' if result2['summary']['success'] else 'FAILED'}")
    print(f"Example 3: {'PASSED' if result3['status'] == 'completed' else 'FAILED'}")


if __name__ == "__main__":
    main()
