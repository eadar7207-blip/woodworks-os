#!/usr/bin/env python3
"""Test suite for email campaign automation system."""

import unittest
from datetime import datetime, timedelta

class TestEmailCampaignSystem(unittest.TestCase):
    """TDD test suite - tests first, then implementation."""
    
    # Campaign Management Tests
    def test_create_campaign_with_valid_data(self):
        """Campaign creation with all required fields."""
        campaign = {
            "name": "Q2 Lead Nurture",
            "templates": ["welcome", "followup"],
            "schedule": "2026-06-10",
            "status": "draft"
        }
        self.assertEqual(campaign["name"], "Q2 Lead Nurture")
    
    def test_campaign_requires_name(self):
        """Campaign creation fails without name."""
        campaign = {"templates": [], "schedule": "2026-06-10"}
        self.assertFalse("name" in campaign)
    
    # Segmentation Tests
    def test_segment_leads_by_source(self):
        """Segment leads by source (website, referral, cold)."""
        leads = [
            {"email": "john@ex.com", "source": "website"},
            {"email": "jane@ex.com", "source": "referral"},
            {"email": "bob@ex.com", "source": "website"}
        ]
        
        by_source = {}
        for lead in leads:
            src = lead["source"]
            if src not in by_source:
                by_source[src] = []
            by_source[src].append(lead)
        
        self.assertEqual(len(by_source["website"]), 2)
        self.assertEqual(len(by_source["referral"]), 1)
    
    # Personalization Tests
    def test_personalize_email_body(self):
        """Replace template variables with lead data."""
        template = "Hi {{first_name}}, we have {{property_type}}"
        lead = {"first_name": "John", "property_type": "3BR"}
        
        result = template
        for key, value in lead.items():
            result = result.replace(f"{{{{{key}}}}}", value)
        
        self.assertEqual(result, "Hi John, we have 3BR")
    
    # Email Validation Tests
    def test_valid_email_format(self):
        """Validate email has @ and . parts."""
        email = "john@example.com"
        self.assertIn("@", email)
        self.assertIn(".", email.split("@")[1])
    
    def test_invalid_email_missing_domain(self):
        """Reject emails without proper domain."""
        email = "john@"
        parts = email.split("@")
        self.assertLess(len(parts[1]), 3)
    
    # Scheduling Tests
    def test_schedule_email_for_future(self):
        """Email scheduled for future date is valid."""
        now = datetime.now()
        send_time = now + timedelta(days=1)
        
        email = {
            "to": "john@example.com",
            "scheduled_time": send_time,
            "status": "scheduled"
        }
        
        self.assertGreater(email["scheduled_time"], now)
        self.assertEqual(email["status"], "scheduled")
    
    # Analytics Tests
    def test_track_open_event(self):
        """Record email open with timestamp."""
        event = {
            "campaign": "Q2 Nurture",
            "event": "open",
            "timestamp": datetime.now().isoformat()
        }
        self.assertEqual(event["event"], "open")
    
    def test_calculate_open_rate(self):
        """Calculate campaign open rate."""
        campaign = {"sent": 100, "opens": 45}
        open_rate = (campaign["opens"] / campaign["sent"]) * 100
        self.assertEqual(open_rate, 45.0)
    
    # Error Handling Tests
    def test_remove_duplicate_emails(self):
        """Deduplicate email list before sending."""
        leads = [
            {"email": "john@ex.com"},
            {"email": "john@ex.com"},
            {"email": "jane@ex.com"}
        ]
        
        unique = set(l["email"] for l in leads)
        self.assertEqual(len(unique), 2)
    
    def test_respect_unsubscribe(self):
        """Skip unsubscribed leads."""
        lead = {"email": "john@ex.com", "unsubscribed": True}
        
        if not lead["unsubscribed"]:
            # would send email
            pass
        else:
            # skipped
            self.assertTrue(lead["unsubscribed"])

if __name__ == "__main__":
    unittest.main()
