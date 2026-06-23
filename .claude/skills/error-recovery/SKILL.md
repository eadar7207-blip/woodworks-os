# Error Recovery

Autonomously detects, diagnoses, and recovers from automation failures. Acts as an agent team coordinator that spawns specialized sub-agents for error analysis, recovery execution, and validation — without requiring user intervention.

---

## How It Works

**Problem:** Automation fails → User discovers failure later → Manual debugging needed

**Solution:** Failure occurs → Error analyzer diagnoses → Recovery executor implements strategy → Validator confirms success

**Result:** User comes back to recovered workflow, not broken one.

---

## Recovery Strategies

### Strategy 1: RETRY (Transient Errors)
- **When:** Timeout, temporary API failure, network hiccup
- **Action:** Re-execute with exponential backoff (2s, 4s, 8s)
- **Max attempts:** 3 per error
- **Success rate:** High for true transient failures
- **Example:** Skill timeout → retry with 2x backoff

### Strategy 2: RETRY_WITH_MODIFIED_PARAMS (Skill/Configuration Errors)
- **When:** Skill not found, bad parameters, invalid input format
- **Action:** Modify parameters (simplify input, adjust format, reduce scope)
- **Success rate:** Medium (depends on whether modification fixes root cause)
- **Example:** Email skill fails (invalid address) → retry with sanitized input

### Strategy 3: SKIP_STEP (Non-Critical Step Failures)
- **When:** Step consistently fails but workflow can proceed without it
- **Action:** Skip failed step, continue to next step in sequence
- **Success rate:** High (depends on step criticality)
- **Example:** Optional CRM logging fails → skip it, complete other steps

### Strategy 4: REDUCE_SCOPE (Scope Too Large)
- **When:** Task too large, too many parameters, too much data
- **Action:** Reduce input size, limit data set, simplify scope
- **Success rate:** Medium-high (may deliver 80% instead of 100%)
- **Example:** Analyze 1000 leads → reduce to 100, retry

### Strategy 5: FALLBACK_ACTION (Primary Action Unavailable)
- **When:** Primary skill unavailable, primary action not found
- **Action:** Use alternative skill/action to achieve same outcome
- **Success rate:** Depends on availability of suitable fallback
- **Example:** Primary email skill fails → fallback to `/send` skill

---

## Agent Team Approach

When failure detected:

1. **Error Analyzer Agent** — Reads execution data, parses error message, determines error type + suggests recovery strategy
2. **Recovery Executor Agent** — Implements recovery strategy, re-executes workflow step, tracks attempt
3. **Validation Agent** — Confirms recovery succeeded or determines next recovery attempt

All agents run autonomously without user prompting.

---

## CLI Commands

```bash
/error-recovery start
  Start monitoring (runs in background every 2 minutes)

/error-recovery status
  Show: current failed executions, recovery attempts, success rate

/error-recovery recover {execution_id}
  Manually trigger recovery for specific failed execution

/error-recovery config
  Show: retry limits, backoff strategy, recovery thresholds

/error-recovery logs
  Show recovery logs from last N hours
```

---

## Database Tracking

All recovery attempts tracked in SQLite:
- **recovery_attempts** — Each attempt with strategy, status, error
- **failure_patterns** — Aggregated error patterns and success rates

Enables learning: system gets smarter over time about which strategies work.

---

## Example: Email Skill Failure Recovery

**Execution fails:**
```
workflow: test-follow-up-sequence
step: send_email
error: "Invalid email address format"
```

**Error Analyzer diagnoses:**
```
Error type: CONFIGURATION_ERROR (bad params)
Root cause: Email address invalid/malformed
Suggested strategy: RETRY_WITH_MODIFIED_PARAMS (sanitize email)
Criticality: Medium (non-optional step, high impact)
```

**Recovery Executor implements:**
```
Attempting: RETRY_WITH_MODIFIED_PARAMS
Modifying: trim whitespace, lowercase, validate format
Re-executing: send_email with cleaned params
```

**Validation confirms:**
```
✓ Recovery successful
Execution status: completed
Output: Email sent to cleaned address
```

---

## Monitoring & Notifications

- Checks for new failures every 2 minutes
- Spawns agents only when fixable failure detected
- Sends summary notification when:
  - Recovery succeeds (via `/send` skill)
  - Max retry attempts exhausted (requires user intervention)

---

## Limitations

- Requires SQLite database with execution history
- Can't fix impossible errors (API permanently down, invalid logic)
- Some steps can't be skipped (all-or-nothing workflow dependencies)
- Fallback actions only work if suitable alternative exists

---

## Status

Runs invisibly. Detects failures, spawns agents, recovers automatically. You see success.
