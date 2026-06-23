"""Simple skill executor - mocks real skill behavior for testing."""

import json
from datetime import datetime

class SimpleSkillExecutor:
    """Mock skill executor that returns realistic data without needing CLI."""

    @staticmethod
    def execute_prospect_research(name: str, company: str, **kwargs) -> dict:
        """Mock prospect research - returns realistic contact data."""
        return {
            "name": name,
            "company": company,
            "status": "prospect",
            "company_info": {
                "name": company,
                "industry": "Real Estate",
                "size": "5-10 employees",
                "location": "Chicago, IL"
            },
            "contacts": [
                {"name": name, "title": "Owner", "email": f"{name.lower().replace(' ', '.')}@{company.lower().replace(' ', '')}.com"}
            ],
            "social_links": {
                "linkedin": f"https://linkedin.com/company/{company.lower()}",
                "website": f"https://{company.lower().replace(' ', '')}.com"
            },
            "recent_activity": [
                {"date": datetime.now().isoformat(), "activity": "research_initiated"}
            ],
            "research_date": datetime.now().isoformat()
        }

    @staticmethod
    def execute_proposal_generate(prospect_name: str, company: str, scope: str = "", **kwargs) -> dict:
        """Mock proposal generation - returns proposal content."""
        return {
            "proposal_id": f"PROP-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "prospect_name": prospect_name,
            "company": company,
            "scope": scope,
            "proposal_content": f"""
# Proposal: Real Estate Lead Automation

**For:** {prospect_name} at {company}
**Scope:** {scope}

## Executive Summary
We propose implementing an automated lead management system tailored to {company}'s specific workflow.

## Services Included
- Lead research and qualification automation
- CRM integration and activity logging
- Email follow-up automation
- Pipeline management and reporting

## Investment
- Setup: $2,500
- Monthly: $500
- Expected ROI: 40% within 90 days

## Timeline
- Week 1: System setup and configuration
- Week 2: Integration and testing
- Week 3: Training and go-live

## Next Steps
We're ready to discuss your specific needs and timeline.
            """.strip(),
            "estimated_price": "$2,500 setup + $500/month",
            "document_url": "#",
            "created_date": datetime.now().isoformat()
        }

    @staticmethod
    def execute_crm_log_activity(activity_type: str, contact_name: str = "", email: str = "",
                                 company: str = "", activity_description: str = "", **kwargs) -> dict:
        """Mock CRM activity logging - returns confirmation."""
        return {
            "activity_id": f"ACT-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "contact_name": contact_name,
            "email": email,
            "company": company,
            "activity_type": activity_type,
            "activity_description": activity_description,
            "logged_at": datetime.now().isoformat(),
            "confirmation": f"Activity '{activity_type}' logged successfully for {contact_name}",
            "status": "logged"
        }

    @staticmethod
    def execute_send_email(to: str, subject: str, body: str, **kwargs) -> dict:
        """Mock email sending - returns confirmation."""
        return {
            "sent": True,
            "to": to,
            "subject": subject,
            "sent_at": datetime.now().isoformat(),
            "confirmation": f"Email sent to {to}",
            "status": "sent"
        }

    @staticmethod
    def execute_skill(skill_name: str, action: str, params: dict) -> dict:
        """Execute mock skill based on skill name and action."""

        if skill_name == "prospect" and action == "research":
            return SimpleSkillExecutor.execute_prospect_research(**params)

        elif skill_name == "proposal" and action == "generate":
            return SimpleSkillExecutor.execute_proposal_generate(**params)

        elif skill_name == "crm" and action == "log_activity":
            return SimpleSkillExecutor.execute_crm_log_activity(**params)

        elif skill_name == "send" and action == "email":
            return SimpleSkillExecutor.execute_send_email(**params)

        else:
            return {
                "error": f"Skill {skill_name}/{action} not implemented",
                "status": "error"
            }
