# Skill Bridge API

A REST API server that makes Claude Code skills programmatically callable from the automation executor.

## Overview

Skill Bridge acts as a middleware between your automation executor and Claude Code skills. Instead of executing skills via subprocess calls, the executor sends HTTP requests to Skill Bridge, which handles skill invocation, response parsing, and result standardization.

### Architecture

```
Automation Executor
    ↓ (HTTP POST /invoke/prospect)
Skill Bridge API (Flask)
    ↓ (builds command, executes via subprocess)
Claude Code CLI
    ↓ (skill execution)
Skill Bridge (parses response)
    ↓ (extracts structured data)
Executor (receives JSON)
```

## Features

- **REST API** for invoking Claude Code skills
- **Skill metadata** with parameter validation
- **Response parsing** that extracts structured data from text-based skill outputs
- **Async invocation** for long-running skills with polling support
- **SQLite database** for tracking all invocations
- **Comprehensive logging** for debugging and monitoring
- **API key authentication** (optional)
- **Error handling** with detailed error messages

## Supported Skills

1. **prospect** - Research and manage sales prospects
2. **proposal** - Generate and manage business proposals
3. **crm** - Manage customer relationship management data
4. **send** - Send emails and messages
5. **tasks** - Create and manage tasks
6. **content** - Generate and manage content
7. **calendar** - Manage calendar events
8. **invoicing** - Create and manage invoices
9. **automate** - Create and manage automation workflows
10. **wiki** - Read and manage wiki knowledge base

## Installation

### Prerequisites

- Python 3.8+
- Flask 2.3+
- Claude Code CLI installed and accessible

### Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create environment configuration (optional):
```bash
cat > .env.local << EOF
SKILL_BRIDGE_HOST=0.0.0.0
SKILL_BRIDGE_PORT=9000
SKILL_BRIDGE_DEBUG=false
SKILL_BRIDGE_API_KEY=your_api_key_here
SKILL_TIMEOUT=120
CLAUDE_CODE_WORKSPACE=/path/to/workspace
EOF
```

3. Run the server:
```bash
python skill_bridge.py
```

The API will be available at `http://localhost:9000`

## API Endpoints

### Health Check

```
GET /health

Response:
{
    "status": "healthy",
    "timestamp": "2024-01-15T10:30:00.000000",
    "version": "1.0.0"
}
```

### List Available Skills

```
GET /available-skills

Response:
{
    "total": 10,
    "skills": [
        {
            "name": "prospect",
            "description": "Research and manage sales prospects",
            "actions": ["research", "outreach", "update", "pipeline"],
            "parameters": {
                "research": {
                    "required": ["name", "company"],
                    "optional": ["industry", "location"],
                    "description": "Research a prospect..."
                },
                ...
            }
        },
        ...
    ]
}
```

### Get Skill Details

```
GET /skills/<skill_name>

Example: GET /skills/prospect

Response:
{
    "name": "prospect",
    "description": "Research and manage sales prospects",
    "actions": ["research", "outreach", "update", "pipeline"],
    "parameters": { ... }
}
```

### Invoke Skill Synchronously

```
POST /invoke/<skill_name>

Request Body:
{
    "action": "action_name",
    "params": {
        "param1": "value1",
        "param2": "value2"
    }
}

Example:
POST /invoke/prospect
{
    "action": "research",
    "params": {
        "name": "John Smith",
        "company": "ABC Real Estate"
    }
}

Response:
{
    "status": "completed|failed|error",
    "output": {
        "company_info": { ... },
        "contacts": [ ... ],
        "social_links": { ... }
    },
    "raw_output": "...",
    "confidence": 0.85,
    "invocation_id": "uuid",
    "duration_ms": 2500,
    "error": "..." (if status is error/failed)
}
```

### Invoke Skill Asynchronously

```
POST /invoke/<skill_name>/async

Request Body:
{
    "action": "action_name",
    "params": { ... }
}

Response (202 Accepted):
{
    "status": "queued",
    "invocation_id": "uuid",
    "message": "Skill invocation ... queued for execution"
}
```

### Get Async Invocation Status

```
GET /status/<invocation_id>

Response:
{
    "invocation_id": "uuid",
    "status": "queued|running|completed|failed",
    "skill_name": "prospect",
    "action": "research",
    "created_at": "2024-01-15T10:30:00",
    "started_at": "2024-01-15T10:30:01",
    "completed_at": "2024-01-15T10:30:05",
    "output": { ... },
    "error": "..." (if failed)
}
```

### Get Invocation History

```
GET /history?skill=prospect&status=completed&limit=50

Query Parameters:
- skill: filter by skill name (optional)
- status: filter by status (optional)
- limit: number of records (default: 100)

Response:
{
    "total": 3,
    "invocations": [
        {
            "id": "uuid",
            "skill_name": "prospect",
            "action": "research",
            "params": { ... },
            "status": "completed",
            "result": { ... },
            "created_at": "...",
            "completed_at": "...",
            "duration_ms": 2500
        },
        ...
    ]
}
```

## Integration with Automation Executor

To integrate Skill Bridge with your automation executor, modify the `SkillAction` class in your executor:

```python
import requests

class SkillAction:
    def __init__(self, skill_bridge_url="http://localhost:9000", api_key=None):
        self.base_url = skill_bridge_url
        self.headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}

    def execute(self, action_config, variables=None):
        """Execute skill via Skill Bridge API."""
        variables = variables or {}
        
        skill_name = action_config.get("skill")
        action = action_config.get("action", "default")
        params = action_config.get("params", {})
        
        # Interpolate variables
        params = self._interpolate(params, variables)
        
        # Invoke skill via API
        url = f"{self.base_url}/invoke/{skill_name}"
        response = requests.post(
            url,
            json={"action": action, "params": params},
            headers=self.headers,
            timeout=30
        )
        
        response.raise_for_status()
        return response.json()
    
    def _interpolate(self, value, variables):
        # Interpolate variables in parameters
        if isinstance(value, str):
            for key, val in variables.items():
                value = value.replace(f"{{{{{key}}}}}", str(val))
        elif isinstance(value, dict):
            return {k: self._interpolate(v, variables) for k, v in value.items()}
        elif isinstance(value, list):
            return [self._interpolate(item, variables) for item in value]
        return value
```

## Usage Examples

### Example 1: Research a Prospect

```bash
curl -X POST http://localhost:9000/invoke/prospect \
  -H "Content-Type: application/json" \
  -d '{
    "action": "research",
    "params": {
      "name": "John Smith",
      "company": "ABC Real Estate"
    }
  }'
```

### Example 2: Generate a Proposal

```bash
curl -X POST http://localhost:9000/invoke/proposal \
  -H "Content-Type: application/json" \
  -d '{
    "action": "generate",
    "params": {
      "prospect_name": "John Smith",
      "company": "ABC Real Estate",
      "scope": "Lead automation system",
      "budget": "10000"
    }
  }'
```

### Example 3: Send Email

```bash
curl -X POST http://localhost:9000/invoke/send \
  -H "Content-Type: application/json" \
  -d '{
    "action": "email",
    "params": {
      "to": "john@abc.com",
      "subject": "Your Proposal",
      "body": "Here is your proposal..."
    }
  }'
```

### Example 4: Async Invocation with Polling

```bash
# Start async invocation
RESPONSE=$(curl -X POST http://localhost:9000/invoke/proposal/async \
  -H "Content-Type: application/json" \
  -d '{
    "action": "generate",
    "params": { ... }
  }')

INVOCATION_ID=$(echo $RESPONSE | jq -r .invocation_id)

# Poll for status
curl http://localhost:9000/status/$INVOCATION_ID
```

## Response Parsing

Skill Bridge includes intelligent response parsers that extract structured data from skill outputs.

### Supported Response Formats

1. **JSON** - Returned as-is with confidence 1.0
2. **Text with key-value pairs** - Extracted into a dict
3. **Skill-specific formats** - Special parsers for each skill

### Confidence Scores

Responses include a `confidence` score (0-1) indicating confidence in the parsed output:

- **1.0** - Valid JSON response
- **0.8-0.9** - High-confidence text parsing
- **0.5-0.7** - Partial/moderate confidence
- **0.3-0.4** - Low confidence (raw output returned)
- **0.0-0.2** - Very low confidence (parsing failed)

## Database

Skill Bridge uses SQLite for persistent storage:

- **skill_invocations** - All skill invocations (sync and completed async)
- **skill_cache** - Cached skill metadata
- **async_invocations** - Pending and running async invocations

Database is located at: `.claude/skills/skill-bridge/bridge.db`

## Logging

All requests and invocations are logged to:

`.claude/skills/skill-bridge/skill_bridge.log`

## Testing

Run the test suite:

```bash
python -m pytest test_skill_bridge.py -v
```

Test coverage includes:

- Skill definitions validation
- Response parsing for all skills
- Database operations
- REST API endpoints
- End-to-end workflows

## Error Handling

Skill Bridge provides detailed error messages for common failure scenarios:

```json
{
    "status": "error",
    "error": "Parameter validation failed: Missing required parameter: company",
    "invocation_id": "uuid"
}
```

Common errors:

- **Parameter validation failed** - Missing or invalid parameters
- **Skill not found** - Requested skill doesn't exist
- **Execution failed** - Skill execution returned non-zero exit code
- **Timeout** - Skill took longer than configured timeout
- **Parse error** - Failed to parse skill response

## Configuration

### Environment Variables

- `SKILL_BRIDGE_HOST` - Listen address (default: 0.0.0.0)
- `SKILL_BRIDGE_PORT` - Listen port (default: 9000)
- `SKILL_BRIDGE_DEBUG` - Debug mode (default: false)
- `SKILL_BRIDGE_API_KEY` - Optional API key for authentication
- `SKILL_TIMEOUT` - Skill execution timeout in seconds (default: 120)
- `CLAUDE_CODE_WORKSPACE` - Path to Claude Code workspace

### Security

To enable API key authentication, set `SKILL_BRIDGE_API_KEY` environment variable:

```bash
export SKILL_BRIDGE_API_KEY="your-secret-key"
```

Then include the API key in requests:

```bash
curl -H "Authorization: Bearer your-secret-key" http://localhost:9000/health
```

## Deployment

### Systemd Service

Create `/etc/systemd/system/skill-bridge.service`:

```ini
[Unit]
Description=Skill Bridge API
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/workspace
ExecStart=/usr/bin/python3 /path/to/skill_bridge.py
Restart=on-failure
RestartSec=10

Environment="SKILL_BRIDGE_HOST=127.0.0.1"
Environment="SKILL_BRIDGE_PORT=9000"

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl enable skill-bridge
sudo systemctl start skill-bridge
sudo systemctl status skill-bridge
```

### Docker (Optional)

Dockerfile example:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV SKILL_BRIDGE_HOST=0.0.0.0
ENV SKILL_BRIDGE_PORT=9000

EXPOSE 9000

CMD ["python", "skill_bridge.py"]
```

Build and run:

```bash
docker build -t skill-bridge .
docker run -p 9000:9000 skill-bridge
```

## Troubleshooting

### Claude CLI not found

Ensure Claude Code is installed and `~/.local/bin/claude` is accessible:

```bash
which claude
# or
ls ~/.local/bin/claude
```

### Skill timeout

Increase `SKILL_TIMEOUT` if skills need more time:

```bash
export SKILL_TIMEOUT=300
python skill_bridge.py
```

### Database locked

If you see "database is locked" errors, ensure only one Skill Bridge instance is running:

```bash
lsof -p :9000  # Check what's using port 9000
```

### Response parsing issues

Check the `raw_output` field in responses to see the actual skill output. You may need to add a custom parser in `response_parser.py`.

## Production Readiness Checklist

- [x] Parameter validation
- [x] Error handling and logging
- [x] Database persistence
- [x] Async invocation support
- [x] API key authentication
- [x] Health check endpoint
- [x] Comprehensive testing
- [x] Response parsing for all skills
- [x] Timeout handling
- [x] Graceful error messages

## Contributing

To add support for a new skill:

1. Add skill definition to `skill_definitions.py`
2. Implement response parser in `response_parser.py` (optional)
3. Add tests in `test_skill_bridge.py`
4. Document in this README

## License

Part of Adar Realty Studio automation framework.
