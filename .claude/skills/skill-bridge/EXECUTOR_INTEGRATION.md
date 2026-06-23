# Automation Executor Integration

This guide shows how to integrate Skill Bridge with your automation executor.

## Overview

Instead of invoking skills via subprocess, the executor sends HTTP requests to Skill Bridge, which manages skill invocation, response parsing, and result standardization.

## Changes to Executor

### 1. Update SkillAction Class

Modify `.claude/worktrees/agent-a30d54a8a75ba81d8/executor/actions.py`:

Replace the current `SkillAction` class with this bridge-aware version:

```python
import requests
import json
import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv(".env.local")


class SkillAction:
    """Invoke Claude Code skills via Skill Bridge API.
    
    Supports both direct invocation (fallback) and bridge-based invocation.
    """

    def __init__(self, 
                 retry_config: RetryConfig = None, 
                 workspace_path: str = None,
                 skill_bridge_url: Optional[str] = None,
                 use_bridge: bool = True):
        """Initialize skill action handler.
        
        Args:
            retry_config: Retry configuration
            workspace_path: Path to workspace
            skill_bridge_url: URL of Skill Bridge API (e.g., http://localhost:9000)
            use_bridge: Whether to use Skill Bridge (True) or fallback to subprocess (False)
        """
        self.retry_config = retry_config or RetryConfig()
        self.workspace_path = workspace_path or os.getenv("CLAUDE_CODE_WORKSPACE", ".")
        self.skill_bridge_url = skill_bridge_url or os.getenv(
            "SKILL_BRIDGE_URL", 
            "http://localhost:9000"
        )
        self.use_bridge = use_bridge
        self.api_key = os.getenv("SKILL_BRIDGE_API_KEY")
        self.timeout = int(os.getenv("SKILL_TIMEOUT", 30))

    def execute(self, action_config: Dict[str, Any], variables: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute a skill using Skill Bridge or direct invocation.
        
        Action config format:
        {
            "skill": "prospect",
            "action": "research",  # Optional, defaults to "default"
            "params": {
                "name": "John Smith",
                "company": "ABC Corp"
            }
        }
        """
        variables = variables or {}

        skill_name = action_config.get("skill")
        action = action_config.get("action", "default")
        params = action_config.get("params", {})

        # Interpolate parameters
        params = {k: self._interpolate(v, variables) for k, v in params.items()}

        if self.use_bridge:
            return self._invoke_via_bridge(skill_name, action, params)
        else:
            return self._invoke_direct(skill_name, action, params)

    def _invoke_via_bridge(self, skill_name: str, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Invoke skill via Skill Bridge API."""
        def invoke():
            headers = {"Content-Type": "application/json"}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"

            url = f"{self.skill_bridge_url}/invoke/{skill_name}"
            
            response = requests.post(
                url,
                json={"action": action, "params": params},
                headers=headers,
                timeout=self.timeout
            )
            
            response.raise_for_status()
            return response.json()

        result, success = retry_with_backoff(invoke, self.retry_config)

        if not success:
            raise Exception(
                f"Skill {skill_name}/{action} failed after {self.retry_config.max_retries} retries"
            )

        return result

    def _invoke_direct(self, skill_name: str, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback: invoke skill directly via subprocess."""
        # This is the existing implementation
        # ... [keep the old subprocess-based implementation here]
        pass

    @staticmethod
    def _interpolate(value: Any, variables: Dict[str, Any]) -> Any:
        """Interpolate variables in strings."""
        if isinstance(value, str):
            for key, val in variables.items():
                value = value.replace(f"{{{{{key}}}}}", str(val))
        elif isinstance(value, dict):
            return {k: SkillAction._interpolate(v, variables) for k, v in value.items()}
        elif isinstance(value, list):
            return [SkillAction._interpolate(item, variables) for item in value]
        return value
```

### 2. Update ActionFactory

Modify the `ActionFactory` class to pass Skill Bridge URL:

```python
class ActionFactory:
    """Factory for creating action handlers."""

    def __init__(self, retry_config: RetryConfig = None):
        self.retry_config = retry_config or RetryConfig(
            max_retries=int(os.getenv("MAX_RETRIES", 3)),
            backoff_factor=float(os.getenv("RETRY_BACKOFF_FACTOR", 2.0)),
        )

    def create_handler(self, action_type: str):
        """Create an action handler for a given type."""
        if action_type == "http":
            return HTTPAction(self.retry_config)
        elif action_type == "email":
            return MailgunAction(self.retry_config)
        elif action_type == "skill":
            # Create SkillAction with Skill Bridge support
            skill_bridge_url = os.getenv("SKILL_BRIDGE_URL", "http://localhost:9000")
            use_bridge = os.getenv("USE_SKILL_BRIDGE", "true").lower() == "true"
            return SkillAction(
                retry_config=self.retry_config,
                skill_bridge_url=skill_bridge_url,
                use_bridge=use_bridge
            )
        else:
            raise ValueError(f"Unknown action type: {action_type}")
```

### 3. Update Environment Configuration

Add to `.env.local`:

```bash
# Skill Bridge Configuration
SKILL_BRIDGE_URL=http://localhost:9000
USE_SKILL_BRIDGE=true
SKILL_BRIDGE_API_KEY=your-optional-api-key
SKILL_TIMEOUT=120
```

## Executor Workflow with Skill Bridge

### 1. Direct Invocation

```python
from executor.actions import ActionFactory

factory = ActionFactory()
skill_action = factory.create_handler("skill")

result = skill_action.execute(
    {
        "skill": "prospect",
        "action": "research",
        "params": {
            "name": "John Smith",
            "company": "ABC Real Estate"
        }
    },
    variables={}
)

# Result:
# {
#     "status": "completed",
#     "output": {
#         "company_info": {...},
#         "contacts": [...]
#     },
#     "confidence": 0.85,
#     "invocation_id": "uuid",
#     "duration_ms": 2500
# }
```

### 2. Error Handling

```python
try:
    result = skill_action.execute(action_config, variables)
    
    if result["status"] == "error":
        print(f"Skill error: {result['error']}")
    elif result["status"] == "completed":
        output = result["output"]
        confidence = result["confidence"]
        
        if confidence < 0.5:
            print(f"Low confidence ({confidence}), verify output manually")
        
        # Process output
        print(output)
        
except Exception as e:
    print(f"Failed to execute skill: {e}")
```

## Workflow Example: Prospect → Proposal → Send → Log

```python
class ProspectWorkflow:
    """End-to-end prospect workflow using Skill Bridge."""
    
    def __init__(self, executor_url="http://localhost:8000"):
        self.executor_url = executor_url
        self.action_factory = ActionFactory()
    
    def execute(self, prospect_name: str, company: str):
        """Execute full prospect workflow."""
        
        skill_action = self.action_factory.create_handler("skill")
        
        # Step 1: Research prospect
        print(f"Step 1: Researching {prospect_name}...")
        research_result = skill_action.execute({
            "skill": "prospect",
            "action": "research",
            "params": {
                "name": prospect_name,
                "company": company
            }
        })
        
        if research_result["status"] != "completed":
            raise Exception(f"Research failed: {research_result.get('error')}")
        
        prospect_info = research_result["output"]
        prospect_email = prospect_info["contacts"][0]["email"] if prospect_info["contacts"] else None
        
        # Step 2: Generate proposal
        print("Step 2: Generating proposal...")
        proposal_result = skill_action.execute({
            "skill": "proposal",
            "action": "generate",
            "params": {
                "prospect_name": prospect_name,
                "company": company,
                "scope": "Lead automation system"
            }
        })
        
        if proposal_result["status"] != "completed":
            raise Exception(f"Proposal generation failed: {proposal_result.get('error')}")
        
        proposal_id = proposal_result["output"]["proposal_id"]
        
        # Step 3: Send proposal
        if prospect_email:
            print("Step 3: Sending proposal...")
            send_result = skill_action.execute({
                "skill": "proposal",
                "action": "send",
                "params": {
                    "proposal_id": proposal_id,
                    "recipient_email": prospect_email
                }
            })
            
            if send_result["status"] == "completed":
                print(f"Proposal sent to {prospect_email}")
        
        # Step 4: Log activity in CRM
        print("Step 4: Logging activity...")
        crm_result = skill_action.execute({
            "skill": "crm",
            "action": "log_activity",
            "params": {
                "contact_id": "contact_123",  # Would come from research
                "activity_type": "proposal_sent",
                "description": f"Sent proposal to {prospect_name} at {company}"
            }
        })
        
        print("Workflow completed!")
        return {
            "prospect_info": prospect_info,
            "proposal_id": proposal_id,
            "success": True
        }


# Usage:
workflow = ProspectWorkflow()
result = workflow.execute("John Smith", "ABC Real Estate")
```

## Async Invocation Example

For long-running skills, use async invocation:

```python
class AsyncSkillInvoker:
    """Handle async skill invocations."""
    
    def __init__(self, skill_bridge_url="http://localhost:9000"):
        self.skill_bridge_url = skill_bridge_url
        self.api_key = os.getenv("SKILL_BRIDGE_API_KEY")
    
    def invoke_async(self, skill_name: str, action: str, params: Dict[str, Any]) -> str:
        """Queue skill invocation and return invocation ID."""
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        
        url = f"{self.skill_bridge_url}/invoke/{skill_name}/async"
        
        response = requests.post(
            url,
            json={"action": action, "params": params},
            headers=headers
        )
        
        response.raise_for_status()
        result = response.json()
        
        return result["invocation_id"]
    
    def get_status(self, invocation_id: str) -> Dict[str, Any]:
        """Get async invocation status."""
        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        
        url = f"{self.skill_bridge_url}/status/{invocation_id}"
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        return response.json()
    
    def wait_for_completion(self, invocation_id: str, timeout: int = 300) -> Dict[str, Any]:
        """Wait for async invocation to complete."""
        import time
        
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            status = self.get_status(invocation_id)
            
            if status["status"] in ["completed", "failed"]:
                return status
            
            time.sleep(5)  # Poll every 5 seconds
        
        raise TimeoutError(f"Invocation {invocation_id} timed out")


# Usage:
invoker = AsyncSkillInvoker()

# Queue proposal generation (might take time)
invocation_id = invoker.invoke_async(
    "proposal",
    "generate",
    {"prospect_name": "John", "company": "ABC", "scope": "Automation"}
)

print(f"Proposal generation queued: {invocation_id}")

# Wait for completion
result = invoker.wait_for_completion(invocation_id)

if result["status"] == "completed":
    print(f"Proposal generated: {result['output']}")
else:
    print(f"Failed: {result.get('error')}")
```

## Fallback Behavior

If Skill Bridge is unavailable, the executor can fallback to direct subprocess invocation:

```python
# In .env.local:
USE_SKILL_BRIDGE=false

# This uses the old subprocess-based approach
```

## Monitoring Integration

Track invocation history:

```python
def get_invocation_history(skill_name: str = None, status: str = None):
    """Get history of all skill invocations."""
    params = {}
    if skill_name:
        params["skill"] = skill_name
    if status:
        params["status"] = status
    
    response = requests.get(
        "http://localhost:9000/history",
        params=params
    )
    
    return response.json()


# Usage:
history = get_invocation_history(skill_name="prospect", status="completed")
print(f"Total prospect research invocations: {history['total']}")

for inv in history["invocations"]:
    print(f"  - {inv['id']}: {inv['status']} ({inv['duration_ms']}ms)")
```

## Security Considerations

1. **API Key**: Set `SKILL_BRIDGE_API_KEY` in environment for authentication
2. **Network**: Run Skill Bridge on localhost by default (requires local network access)
3. **Logging**: Skill Bridge logs all invocations - monitor `.claude/skills/skill-bridge/skill_bridge.log`
4. **Rate Limiting**: Implement at reverse proxy level if needed

## Performance Tuning

### Skill Timeout

Increase for long-running skills:

```bash
export SKILL_TIMEOUT=300  # 5 minutes
```

### Parallel Invocations

Multiple executor instances can call the same Skill Bridge (uses SQLite with proper locking).

### Response Caching

For frequently researched prospects, add caching:

```python
import hashlib
import json

class CachedSkillAction:
    def __init__(self, skill_action, ttl_seconds=3600):
        self.skill_action = skill_action
        self.ttl_seconds = ttl_seconds
        self.cache = {}
    
    def execute(self, action_config, variables=None):
        # Create cache key
        key = hashlib.md5(
            json.dumps(action_config, sort_keys=True).encode()
        ).hexdigest()
        
        if key in self.cache:
            cached_time, cached_result = self.cache[key]
            if time.time() - cached_time < self.ttl_seconds:
                return cached_result
        
        # Execute and cache
        result = self.skill_action.execute(action_config, variables)
        self.cache[key] = (time.time(), result)
        
        return result
```

## Troubleshooting

### "Failed to connect to Skill Bridge"

Ensure Skill Bridge is running:

```bash
ps aux | grep skill_bridge
curl http://localhost:9000/health
```

### "Invocation timeout"

Increase `SKILL_TIMEOUT` or use async invocation for long-running skills.

### "Parameter validation failed"

Check skill parameters in `/available-skills` endpoint or `SKILLS.md`.

### "Low confidence in response"

Check `raw_output` field to see actual skill output. May need custom response parser.
