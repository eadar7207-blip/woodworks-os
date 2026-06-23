---
name: voice-receptionist
description: AI receptionist for real estate - schedule appointments, qualify leads, take messages. No phone/Twilio needed.
usage: /voice-receptionist "{caller_message}"
examples:
  - /voice-receptionist "I want to schedule a showing for Friday afternoon"
  - /voice-receptionist "I'm selling my condo in 3 months, interested in listing"
  - /voice-receptionist "Can you leave a message for Sohail about the Oak Street property?"
---

# Voice Receptionist Skill

An AI receptionist that handles real estate calls. Built with Claude + automation framework integration.

**What it does:**
- 📅 **Schedule appointments** — Caller says when they want to see a property
- 🎯 **Qualify leads** — Ask questions, score as hot/warm/cold
- 💬 **Take messages** — Capture caller info and message for agent

**No phone needed.** Simulates a complete call in text.

---

## How to Use

### Basic Usage
```
/voice-receptionist "{what the caller says}"
```

### Examples

**Schedule an appointment:**
```
/voice-receptionist "Hi, I'd like to see the property on Oak Street. I'm free Friday afternoon."
```

**Qualify a lead:**
```
/voice-receptionist "I'm thinking about selling my condo in Lincoln Park. It's a 2-bed, 2-bath. I'd like to sell within 3 months for around $600K."
```

**Take a message:**
```
/voice-receptionist "Hi, I'd like to leave a message for Sohail about the property at 123 Oak Street."
```

---

## What You Get Back

```json
{
  "intent": "schedule_appointment|qualify_lead|take_message",
  "receptionist_response": "Perfect! I can help you...",
  "entities": {
    "property_address": "123 Oak St",
    "preferred_time": "Friday 2 PM",
    "lead_score": "warm",
    "caller_name": "John Smith"
  },
  "action": {
    "type": "schedule_appointment|create_lead|log_activity",
    "details": {...}
  },
  "call_data": {
    "call_id": "...",
    "transcript": "[full conversation]",
    "duration": "2:45"
  }
}
```

---

## Real Examples

### Example 1: Appointment
```
Input: "Hi, I'd like to see the 3-bedroom on Oak Street. Friday afternoon works for me."

Output:
Intent: schedule_appointment
Response: "Great! I have 2 PM or 4 PM available on Friday. Which works better?"
Entities: {property: "123 Oak St", preferred_time: "Friday afternoon"}
```

### Example 2: Lead Qualification
```
Input: "I'm selling my condo. It's 2 bed, 2 bath in Lincoln Park. I want to sell in 3 months for $600K."

Output:
Intent: qualify_lead
Response: "Perfect! That's a great timeline. I'm logging your information..."
Entities: {
  property: "2BR/2BA condo, Lincoln Park",
  timeline: "3 months",
  budget: "$600K",
  lead_score: "hot"
}
```

### Example 3: Message Taking
```
Input: "Can you leave a message for Sohail? I'm interested in the property at 123 Oak Street."

Output:
Intent: take_message
Response: "Of course! I've logged your message. Sohail will get back to you soon."
Entities: {message: "Interested in 123 Oak Street", caller_info: "captured"}
```

---

## Features

✅ **Real conversations** — Sounds like a real receptionist  
✅ **Intent detection** — Automatically understands what caller wants  
✅ **Entity extraction** — Pulls out names, times, addresses, budgets  
✅ **Lead scoring** — Qualifies leads as hot/warm/cold  
✅ **Database logging** — Everything saved for follow-up  
✅ **Integration ready** — Calls your automation framework (Calendar, CRM, Send skills)  
✅ **No phone needed** — Pure text-based, works in Claude Code  

---

## Use Cases

- **Test the receptionist** — See it in action
- **Train agents** — Show what automation can do
- **Lead qualification** — Quick scoring before agent follow-up
- **Message capturing** — Take notes when agents busy
- **Workflow automation** — Chain with other skills

---

## Integration with Workflows

Use in automation workflows:

```yaml
# .claude/automations/real-estate-intake.yml
steps:
  - skill: voice-receptionist
    input: "I'm interested in selling my property"
    capture: [intent, entities, lead_score]
  
  - skill: crm
    action: create_lead
    data: "{{ captured.entities }}"
  
  - skill: send
    action: email
    to: "{{ agent_email }}"
    subject: "New {{ captured.lead_score }} lead"
```

---

## Tips

- **Be specific** — Give details (location, timeline, budget, etc.)
- **Ask questions** — If receptionist asks, answer to qualify better
- **Check entities** — See what got extracted
- **Use lead_score** — Hot leads get priority follow-up

---

## How It Works

1. **You input** — What the caller would say
2. **Receptionist processes** — Claude analyzes intent, entities, best response
3. **Actions execute** — Books appointments, creates leads, logs messages
4. **Data returned** — Structured data for next steps
5. **Database saves** — Everything logged for history

---

## Next Steps

- Want to see a live demo? Run `python3 demo.py` in the project
- Want to integrate with phone? See `/projects/voice-receptionist/DEPLOYMENT.md`
- Want to customize responses? Edit the Claude system prompt in `claude_engine.py`

---

Built for Eitan Adar's automation agency.  
Based on `/projects/voice-receptionist/` — fully tested, production-ready.
