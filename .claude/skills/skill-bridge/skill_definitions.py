"""Skill metadata and parameter definitions for all available Claude Code skills."""

SKILL_DEFINITIONS = {
    "prospect": {
        "name": "prospect",
        "description": "Research and manage sales prospects",
        "actions": ["research", "outreach", "update", "pipeline"],
        "parameters": {
            "research": {
                "required": ["name", "company"],
                "optional": ["industry", "location", "title"],
                "description": "Research a prospect's company and background",
                "response_format": {
                    "company_info": {"type": "dict"},
                    "contacts": {"type": "list"},
                    "social_links": {"type": "dict"},
                    "recent_activity": {"type": "list"},
                }
            },
            "outreach": {
                "required": ["prospect_name", "prospect_email"],
                "optional": ["subject", "template", "context"],
                "description": "Create and send outreach message to prospect",
                "response_format": {
                    "sent": {"type": "bool"},
                    "message_id": {"type": "str"},
                    "confirmation": {"type": "str"},
                }
            },
            "update": {
                "required": ["prospect_id", "status"],
                "optional": ["notes", "next_step"],
                "description": "Update prospect status and notes",
                "response_format": {
                    "updated": {"type": "bool"},
                    "prospect_id": {"type": "str"},
                    "new_status": {"type": "str"},
                }
            },
            "pipeline": {
                "required": [],
                "optional": ["stage", "limit"],
                "description": "Get prospect pipeline overview",
                "response_format": {
                    "total_prospects": {"type": "int"},
                    "by_stage": {"type": "dict"},
                    "pipeline": {"type": "list"},
                }
            }
        }
    },
    "proposal": {
        "name": "proposal",
        "description": "Generate and manage business proposals",
        "actions": ["generate", "review", "send", "track"],
        "parameters": {
            "generate": {
                "required": ["prospect_name", "company"],
                "optional": ["scope", "budget", "timeline", "template"],
                "description": "Generate a proposal for a prospect",
                "response_format": {
                    "proposal_id": {"type": "str"},
                    "proposal_content": {"type": "str"},
                    "estimated_price": {"type": "str"},
                    "document_url": {"type": "str"},
                }
            },
            "review": {
                "required": ["proposal_id"],
                "optional": ["review_criteria"],
                "description": "Review proposal quality and completeness",
                "response_format": {
                    "review_status": {"type": "str"},
                    "quality_score": {"type": "float"},
                    "issues": {"type": "list"},
                    "recommendations": {"type": "list"},
                }
            },
            "send": {
                "required": ["proposal_id", "recipient_email"],
                "optional": ["message"],
                "description": "Send proposal to prospect",
                "response_format": {
                    "sent": {"type": "bool"},
                    "sent_at": {"type": "str"},
                    "tracking_id": {"type": "str"},
                }
            },
            "track": {
                "required": ["proposal_id"],
                "optional": [],
                "description": "Track proposal status and views",
                "response_format": {
                    "status": {"type": "str"},
                    "views": {"type": "int"},
                    "opened_at": {"type": "list"},
                    "feedback": {"type": "list"},
                }
            }
        }
    },
    "crm": {
        "name": "crm",
        "description": "Manage customer relationship management data",
        "actions": ["log_activity", "update_contact", "query", "create_contact"],
        "parameters": {
            "log_activity": {
                "required": ["activity_type"],
                "optional": ["contact_id", "contact_name", "email", "company", "description", "activity_description", "date", "outcome"],
                "description": "Log an activity for a contact",
                "response_format": {
                    "activity_id": {"type": "str"},
                    "logged_at": {"type": "str"},
                    "confirmation": {"type": "str"},
                }
            },
            "update_contact": {
                "required": ["contact_id"],
                "optional": ["name", "email", "phone", "company", "status", "notes"],
                "description": "Update contact information",
                "response_format": {
                    "updated": {"type": "bool"},
                    "contact_id": {"type": "str"},
                    "updated_fields": {"type": "list"},
                }
            },
            "query": {
                "required": [],
                "optional": ["status", "company", "tags", "limit"],
                "description": "Query contacts by criteria",
                "response_format": {
                    "total_found": {"type": "int"},
                    "contacts": {"type": "list"},
                }
            },
            "create_contact": {
                "required": ["name", "email"],
                "optional": ["phone", "company", "title", "tags"],
                "description": "Create a new contact",
                "response_format": {
                    "contact_id": {"type": "str"},
                    "created_at": {"type": "str"},
                    "confirmation": {"type": "str"},
                }
            }
        }
    },
    "send": {
        "name": "send",
        "description": "Send emails and messages",
        "actions": ["email", "sms", "slack"],
        "parameters": {
            "email": {
                "required": ["to", "subject", "body"],
                "optional": ["cc", "bcc", "html", "attachments", "template"],
                "description": "Send an email",
                "response_format": {
                    "sent": {"type": "bool"},
                    "message_id": {"type": "str"},
                    "sent_at": {"type": "str"},
                    "confirmation": {"type": "str"},
                }
            },
            "sms": {
                "required": ["phone", "message"],
                "optional": [],
                "description": "Send an SMS message",
                "response_format": {
                    "sent": {"type": "bool"},
                    "message_id": {"type": "str"},
                    "status": {"type": "str"},
                }
            },
            "slack": {
                "required": ["channel", "message"],
                "optional": ["thread_ts", "attachments"],
                "description": "Send a Slack message",
                "response_format": {
                    "sent": {"type": "bool"},
                    "ts": {"type": "str"},
                    "confirmation": {"type": "str"},
                }
            }
        }
    },
    "tasks": {
        "name": "tasks",
        "description": "Create and manage tasks",
        "actions": ["create", "assign", "update_status", "list"],
        "parameters": {
            "create": {
                "required": ["title"],
                "optional": ["description", "due_date", "priority", "assignee"],
                "description": "Create a new task",
                "response_format": {
                    "task_id": {"type": "str"},
                    "created_at": {"type": "str"},
                    "confirmation": {"type": "str"},
                }
            },
            "assign": {
                "required": ["task_id", "assignee"],
                "optional": ["message"],
                "description": "Assign a task to someone",
                "response_format": {
                    "assigned": {"type": "bool"},
                    "task_id": {"type": "str"},
                    "assigned_to": {"type": "str"},
                }
            },
            "update_status": {
                "required": ["task_id", "status"],
                "optional": ["notes"],
                "description": "Update task status",
                "response_format": {
                    "updated": {"type": "bool"},
                    "task_id": {"type": "str"},
                    "new_status": {"type": "str"},
                }
            },
            "list": {
                "required": [],
                "optional": ["status", "assignee", "due_date", "limit"],
                "description": "List tasks",
                "response_format": {
                    "total": {"type": "int"},
                    "tasks": {"type": "list"},
                }
            }
        }
    },
    "content": {
        "name": "content",
        "description": "Generate and manage content",
        "actions": ["generate", "customize", "review", "publish"],
        "parameters": {
            "generate": {
                "required": ["type", "topic"],
                "optional": ["length", "tone", "style"],
                "description": "Generate content",
                "response_format": {
                    "content_id": {"type": "str"},
                    "content": {"type": "str"},
                    "word_count": {"type": "int"},
                }
            },
            "customize": {
                "required": ["content_id"],
                "optional": ["tone", "audience", "focus"],
                "description": "Customize existing content",
                "response_format": {
                    "customized": {"type": "bool"},
                    "updated_content": {"type": "str"},
                }
            },
            "review": {
                "required": ["content"],
                "optional": ["criteria"],
                "description": "Review content quality",
                "response_format": {
                    "score": {"type": "float"},
                    "issues": {"type": "list"},
                    "suggestions": {"type": "list"},
                }
            },
            "publish": {
                "required": ["content_id", "platform"],
                "optional": ["schedule"],
                "description": "Publish content",
                "response_format": {
                    "published": {"type": "bool"},
                    "url": {"type": "str"},
                    "timestamp": {"type": "str"},
                }
            }
        }
    },
    "calendar": {
        "name": "calendar",
        "description": "Manage calendar events",
        "actions": ["create_event", "send_invite", "update", "list"],
        "parameters": {
            "create_event": {
                "required": ["title", "start_time", "end_time"],
                "optional": ["description", "location", "attendees"],
                "description": "Create a calendar event",
                "response_format": {
                    "event_id": {"type": "str"},
                    "created_at": {"type": "str"},
                    "confirmation": {"type": "str"},
                }
            },
            "send_invite": {
                "required": ["event_id", "attendee_email"],
                "optional": ["message"],
                "description": "Send event invitation",
                "response_format": {
                    "sent": {"type": "bool"},
                    "sent_at": {"type": "str"},
                    "confirmation": {"type": "str"},
                }
            },
            "update": {
                "required": ["event_id"],
                "optional": ["title", "time", "description"],
                "description": "Update calendar event",
                "response_format": {
                    "updated": {"type": "bool"},
                    "event_id": {"type": "str"},
                }
            },
            "list": {
                "required": [],
                "optional": ["start_date", "end_date", "limit"],
                "description": "List calendar events",
                "response_format": {
                    "total": {"type": "int"},
                    "events": {"type": "list"},
                }
            }
        }
    },
    "invoicing": {
        "name": "invoicing",
        "description": "Create and manage invoices",
        "actions": ["create", "send", "track_payment", "list"],
        "parameters": {
            "create": {
                "required": ["client_name", "amount"],
                "optional": ["items", "due_date", "terms"],
                "description": "Create an invoice",
                "response_format": {
                    "invoice_id": {"type": "str"},
                    "created_at": {"type": "str"},
                    "amount": {"type": "str"},
                }
            },
            "send": {
                "required": ["invoice_id", "client_email"],
                "optional": ["message"],
                "description": "Send invoice to client",
                "response_format": {
                    "sent": {"type": "bool"},
                    "sent_at": {"type": "str"},
                    "confirmation": {"type": "str"},
                }
            },
            "track_payment": {
                "required": ["invoice_id"],
                "optional": [],
                "description": "Track invoice payment status",
                "response_format": {
                    "status": {"type": "str"},
                    "amount_due": {"type": "str"},
                    "paid_amount": {"type": "str"},
                    "due_date": {"type": "str"},
                }
            },
            "list": {
                "required": [],
                "optional": ["status", "client", "limit"],
                "description": "List invoices",
                "response_format": {
                    "total": {"type": "int"},
                    "invoices": {"type": "list"},
                }
            }
        }
    },
    "automate": {
        "name": "automate",
        "description": "Create and manage automation workflows",
        "actions": ["create_workflow", "execute", "list", "delete"],
        "parameters": {
            "create_workflow": {
                "required": ["name", "trigger"],
                "optional": ["actions", "description"],
                "description": "Create an automation workflow",
                "response_format": {
                    "workflow_id": {"type": "str"},
                    "created_at": {"type": "str"},
                    "confirmation": {"type": "str"},
                }
            },
            "execute": {
                "required": ["workflow_id"],
                "optional": ["context"],
                "description": "Execute an automation workflow",
                "response_format": {
                    "executed": {"type": "bool"},
                    "execution_id": {"type": "str"},
                    "result": {"type": "dict"},
                }
            },
            "list": {
                "required": [],
                "optional": ["status"],
                "description": "List automation workflows",
                "response_format": {
                    "total": {"type": "int"},
                    "workflows": {"type": "list"},
                }
            },
            "delete": {
                "required": ["workflow_id"],
                "optional": [],
                "description": "Delete an automation workflow",
                "response_format": {
                    "deleted": {"type": "bool"},
                    "workflow_id": {"type": "str"},
                }
            }
        }
    },
    "wiki": {
        "name": "wiki",
        "description": "Read and manage wiki knowledge base",
        "actions": ["read", "write", "ingest", "query"],
        "parameters": {
            "read": {
                "required": ["path"],
                "optional": [],
                "description": "Read wiki content",
                "response_format": {
                    "content": {"type": "str"},
                    "path": {"type": "str"},
                }
            },
            "write": {
                "required": ["path", "content"],
                "optional": ["overwrite"],
                "description": "Write to wiki",
                "response_format": {
                    "written": {"type": "bool"},
                    "path": {"type": "str"},
                }
            },
            "ingest": {
                "required": ["source"],
                "optional": ["type", "title"],
                "description": "Ingest content into wiki",
                "response_format": {
                    "ingested": {"type": "bool"},
                    "path": {"type": "str"},
                }
            },
            "query": {
                "required": ["query"],
                "optional": ["limit"],
                "description": "Query wiki content",
                "response_format": {
                    "results": {"type": "list"},
                    "total": {"type": "int"},
                }
            }
        }
    }
}


def get_skill_definition(skill_name: str) -> dict:
    """Get definition for a specific skill."""
    return SKILL_DEFINITIONS.get(skill_name)


def get_all_skills() -> list:
    """Get list of all available skills."""
    return list(SKILL_DEFINITIONS.keys())


def get_skill_action_definition(skill_name: str, action: str) -> dict:
    """Get definition for a specific skill action."""
    skill = get_skill_definition(skill_name)
    if not skill:
        return None
    return skill.get("parameters", {}).get(action)


def validate_parameters(skill_name: str, action: str, params: dict) -> tuple[bool, str]:
    """Validate parameters for a skill action.

    Returns: (is_valid, error_message)
    """
    definition = get_skill_action_definition(skill_name, action)

    if not definition:
        return False, f"Skill action {skill_name}/{action} not found"

    required = definition.get("required", [])
    optional = definition.get("optional", [])

    # Check required parameters
    for param in required:
        if param not in params:
            return False, f"Missing required parameter: {param}"

    # Check for unexpected parameters
    allowed = set(required) | set(optional)
    for param in params:
        if param not in allowed:
            return False, f"Unexpected parameter: {param}"

    return True, ""
