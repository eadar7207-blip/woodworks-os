# Skill Bridge - Quick Start Guide

Get Skill Bridge up and running in 5 minutes.

## What is Skill Bridge?

Skill Bridge is a REST API that makes Claude Code skills callable via HTTP requests. Instead of your automation executor invoking skills via subprocess, it sends HTTP requests to Skill Bridge, which handles everything and returns structured JSON.

## Installation

### Step 1: Install Dependencies

```bash
cd .claude/skills/skill-bridge
pip install -r requirements.txt
```

### Step 2: Start the Server

```bash
python3 skill_bridge.py
```

Output:
```
INFO:skill_bridge:Starting Skill Bridge API on 0.0.0.0:9000
 * Running on http://0.0.0.0:9000
```

### Step 3: Verify It's Running

```bash
curl http://localhost:9000/health
```

Response:
```json
{
    "status": "healthy",
    "timestamp": "2024-01-15T10:30:00.000000",
    "version": "1.0.0"
}
```

## Basic Usage

### List Available Skills

```bash
curl http://localhost:9000/available-skills | jq .
```

### Research a Prospect

```bash
curl -X POST http://localhost:9000/invoke/prospect \
  -H "Content-Type: application/json" \
  -d '{
    "action": "research",
    "params": {
      "name": "John Smith",
      "company": "ABC Real Estate"
    }
  }' | jq .
```

Response:
```json
{
    "status": "completed",
    "output": {
        "company_info": {
            "name": "ABC Real Estate",
            "industry": "Real Estate",
            ...
        },
        "contacts": [...],
        "social_links": {...}
    },
    "confidence": 0.85,
    "invocation_id": "550e8400-e29b-41d4...",
    "duration_ms": 2500
}
```

### Generate a Proposal

```bash
curl -X POST http://localhost:9000/invoke/proposal \
  -H "Content-Type: application/json" \
  -d '{
    "action": "generate",
    "params": {
      "prospect_name": "John Smith",
      "company": "ABC Real Estate",
      "scope": "Lead automation system"
    }
  }' | jq .
```

### Send an Email

```bash
curl -X POST http://localhost:9000/invoke/send \
  -H "Content-Type: application/json" \
  -d '{
    "action": "email",
    "params": {
      "to": "john@abc.com",
      "subject": "Your Proposal",
      "body": "Here is your proposal for the lead automation system..."
    }
  }' | jq .
```

### Log CRM Activity

```bash
curl -X POST http://localhost:9000/invoke/crm \
  -H "Content-Type: application/json" \
  -d '{
    "action": "log_activity",
    "params": {
      "contact_id": "contact_123",
      "activity_type": "proposal_sent",
      "description": "Sent proposal to John Smith"
    }
  }' | jq .
```

## Integration with Executor

### Step 1: Update Executor Configuration

Add to `.env.local`:

```bash
SKILL_BRIDGE_URL=http://localhost:9000
USE_SKILL_BRIDGE=true
```

### Step 2: Modify SkillAction

In your executor's `actions.py`, update the `SkillAction` class to use the bridge (see EXECUTOR_INTEGRATION.md).

### Step 3: Use in Workflows

```python
from executor.actions import ActionFactory

factory = ActionFactory()
skill_action = factory.create_handler("skill")

# Execute any skill
result = skill_action.execute({
    "skill": "prospect",
    "action": "research",
    "params": {
        "name": "John Smith",
        "company": "ABC Real Estate"
    }
})

print(result["output"])
```

## Response Format

All responses include:

- **status** - "completed", "partial", "error", "failed"
- **output** - Structured extracted data
- **raw_output** - Original skill output (if text-based)
- **confidence** - 0-1 score (higher = more confident in parsing)
- **invocation_id** - UUID for tracking
- **duration_ms** - Execution time in milliseconds
- **error** - Error message (if status is error/failed)

## Async Invocation (for Long-Running Skills)

### Queue Invocation

```bash
RESPONSE=$(curl -s -X POST http://localhost:9000/invoke/proposal/async \
  -H "Content-Type: application/json" \
  -d '{
    "action": "generate",
    "params": {
      "prospect_name": "John Smith",
      "company": "ABC Real Estate"
    }
  }')

INVOCATION_ID=$(echo $RESPONSE | jq -r '.invocation_id')
echo "Invocation ID: $INVOCATION_ID"
```

### Poll for Status

```bash
curl http://localhost:9000/status/$INVOCATION_ID | jq .
```

Response while running:
```json
{
    "invocation_id": "550e8400-e29b-41d4-a716-446655440000",
    "status": "running",
    "skill_name": "proposal",
    "action": "generate",
    "created_at": "2024-01-15T10:30:00.000000"
}
```

Response when complete:
```json
{
    "invocation_id": "550e8400-e29b-41d4-a716-446655440000",
    "status": "completed",
    "output": {
        "proposal_id": "prop_123",
        "estimated_price": "$5,000"
    }
}
```

## Production Deployment

### Using Systemd

```bash
# Copy service file
sudo cp systemd-skill-bridge.service /etc/systemd/system/

# Edit to set correct paths
sudo nano /etc/systemd/system/systemd-skill-bridge.service

# Enable and start
sudo systemctl daemon-reload
sudo systemctl enable skill-bridge
sudo systemctl start skill-bridge

# Check status
sudo systemctl status skill-bridge
```

### Docker

```bash
docker build -t skill-bridge .
docker run -p 9000:9000 skill-bridge
```

## Configuration

### Environment Variables

```bash
# Network
SKILL_BRIDGE_HOST=0.0.0.0        # Listen address
SKILL_BRIDGE_PORT=9000           # Listen port
SKILL_BRIDGE_DEBUG=false         # Debug mode

# Timeouts
SKILL_TIMEOUT=120                # Skill execution timeout (seconds)

# Security
SKILL_BRIDGE_API_KEY=your-key    # Optional API key

# Workspace
CLAUDE_CODE_WORKSPACE=/path/to/workspace
```

### Requiring API Key

```bash
# Set in environment
export SKILL_BRIDGE_API_KEY="your-secret-key"

# Include in requests
curl -H "Authorization: Bearer your-secret-key" http://localhost:9000/health
```

## Monitoring

### Check Health

```bash
curl http://localhost:9000/health
```

### View Logs

```bash
tail -f .claude/skills/skill-bridge/skill_bridge.log
```

### Get Invocation History

```bash
# All invocations
curl http://localhost:9000/history | jq .

# Prospect invocations only
curl http://localhost:9000/history?skill=prospect | jq .

# Failed invocations
curl http://localhost:9000/history?status=failed | jq .

# Last 10
curl http://localhost:9000/history?limit=10 | jq .
```

## Common Tasks

### Research Multiple Prospects

```python
prospects = [
    ("John Smith", "ABC Real Estate"),
    ("Jane Doe", "XYZ Properties"),
    ("Bob Wilson", "123 Realty")
]

import requests

for name, company in prospects:
    response = requests.post(
        "http://localhost:9000/invoke/prospect",
        json={
            "action": "research",
            "params": {"name": name, "company": company}
        }
    )
    result = response.json()
    print(f"{name}: {result['status']}")
```

### Full Workflow (Research → Proposal → Send)

```python
import requests

def prospect_workflow(name, company, email):
    base_url = "http://localhost:9000"
    
    # Step 1: Research
    research = requests.post(
        f"{base_url}/invoke/prospect",
        json={"action": "research", "params": {"name": name, "company": company}}
    ).json()
    print(f"Research: {research['status']}")
    
    # Step 2: Generate Proposal
    proposal = requests.post(
        f"{base_url}/invoke/proposal",
        json={"action": "generate", "params": {"prospect_name": name, "company": company}}
    ).json()
    print(f"Proposal: {proposal['status']}")
    proposal_id = proposal["output"]["proposal_id"]
    
    # Step 3: Send
    send = requests.post(
        f"{base_url}/invoke/proposal",
        json={"action": "send", "params": {"proposal_id": proposal_id, "recipient_email": email}}
    ).json()
    print(f"Send: {send['status']}")
    
    return {"research": research, "proposal": proposal, "send": send}

# Run workflow
result = prospect_workflow("John Smith", "ABC Real Estate", "john@abc.com")
```

### Error Handling

```python
import requests

def safe_invoke(skill, action, params):
    try:
        response = requests.post(
            f"http://localhost:9000/invoke/{skill}",
            json={"action": action, "params": params},
            timeout=30
        )
        response.raise_for_status()
        result = response.json()
        
        if result["status"] == "error":
            print(f"Error: {result['error']}")
            return None
        
        if result.get("confidence", 1.0) < 0.5:
            print(f"Warning: Low confidence ({result['confidence']})")
            print(f"Raw output: {result.get('raw_output')}")
        
        return result["output"]
    
    except requests.exceptions.ConnectionError:
        print("Error: Cannot connect to Skill Bridge")
        return None
    except requests.exceptions.Timeout:
        print("Error: Skill Bridge request timed out")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

# Safe invocation
output = safe_invoke("prospect", "research", {"name": "John", "company": "ABC"})
if output:
    print(output)
```

## Troubleshooting

### Cannot Connect to Server

```bash
# Check if running
ps aux | grep skill_bridge

# Check port
lsof -i :9000

# Check logs
tail .claude/skills/skill-bridge/skill_bridge.log
```

### Skills Timing Out

Increase `SKILL_TIMEOUT`:

```bash
export SKILL_TIMEOUT=300
python3 skill_bridge.py
```

### Parameter Validation Error

Check available parameters:

```bash
curl http://localhost:9000/available-skills | jq '.skills[] | select(.name=="prospect")'
```

Or see SKILLS.md in this directory.

### Low Confidence Parsing

Check `raw_output` in response to see actual skill output:

```bash
curl -s http://localhost:9000/invoke/prospect \
  -H "Content-Type: application/json" \
  -d '{...}' | jq '.raw_output'
```

## Next Steps

- Read **API.md** for complete endpoint documentation
- Read **SKILLS.md** for all skill parameters
- Read **EXECUTOR_INTEGRATION.md** for executor integration
- Read **README.md** for architecture and advanced features

## Support

For issues, check the logs:

```bash
tail -50 .claude/skills/skill-bridge/skill_bridge.log
```

Database queries:

```bash
sqlite3 .claude/skills/skill-bridge/bridge.db
# Then: SELECT * FROM skill_invocations LIMIT 10;
```

## Architecture

```
Your Code
    ↓
HTTP Request (curl, requests, fetch)
    ↓
Skill Bridge API (Flask)
    ↓
Skill Invoker
    ↓
Claude Code CLI (subprocess)
    ↓
Claude Code Skill
    ↓
Response Parser
    ↓
JSON Response
    ↓
Your Code
```

Done! You now have a working Skill Bridge API.
