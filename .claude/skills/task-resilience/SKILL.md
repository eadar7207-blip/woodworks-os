# Task Resilience

Detects failed or stalled background tasks and automatically recovers by selecting the optimal retry strategy. Ensures user is notified of success, not failure. Use when background agents fail so you never see a stalled/failed task — only the successful result.

---

## How It Works

**Problem:** User launches background task → Task fails/stalls → User discovers failure later (disappointing)

**Solution:** Task fails → System auto-detects → Picks best recovery strategy → Re-executes → Notifies success

**Result:** User comes back to working task, not broken one.

---

## Recovery Strategies

### Strategy 1: Retry (Same Task, Same Approach)
- **When:** Task failed due to transient error (timeout, API hiccup)
- **Action:** Re-execute exact same task
- **Success rate:** High for transient failures
- **Example:** Agent stalled due to timeout → retry

### Strategy 2: Split Into Smaller Tasks
- **When:** Large task stalled (too much in one go)
- **Action:** Break task into 3-5 smaller background agents
- **Success rate:** High (smaller = faster = less likely to stall)
- **Example:** "Research 50 competitors" stalls → Split into: "Research 1-20", "Research 21-35", "Research 36-50"

### Strategy 3: Reduce Scope
- **When:** Task is complex, too many deliverables
- **Action:** Drop nice-to-haves, focus on core deliverables
- **Success rate:** Medium (delivers 80% instead of 100%, faster)
- **Example:** "Competitor research + red team + LinkedIn strategy" stalls → Focus on competitor research only, add others after

### Strategy 4: Execute Synchronously
- **When:** Background approach keeps failing
- **Action:** Execute task in foreground (takes longer, but completes)
- **Success rate:** Very high (no background timeout constraints)
- **Example:** All retries fail → Execute now, you wait for results

---

## How Recovery Triggers

**Automatic Detection:**
- Background agent stalls for 600+ seconds
- Background agent returns error/failure status
- Task notification arrives with `status: failed`

**Recovery Decision:**
1. Analyze task type + failure reason
2. Pick strategy most likely to succeed:
   - Transient error → Retry
   - Too large → Split
   - Too complex → Reduce scope
   - Still failing → Sync execute
3. Execute recovery
4. Notify user of result (success)

---

## Example: Competitor Research Recovery

**Initial attempt (fails):**
```
/autonomous competitive-analysis Research 50 RE automation competitors + red team + LinkedIn strategy

❌ Failed: Agent stalled (no progress for 600s)
```

**Auto-recovery (Strategy 2: Split):**
```
Task resilience detected failure. Splitting into 3 smaller tasks:

✓ Task 1: Research 50 competitors + map landscape
✓ Task 2: Red team assessment (threats + vulnerabilities)
✓ Task 3: LinkedIn strategy (positioning + content)

Launching 3 background agents (smaller = faster)...
```

**Outcome:**
```
✅ All 3 tasks complete
Deliverables:
- competitor-landscape.md
- red-team-assessment.md
- linkedin-strategy.md

Recovered automatically. No user intervention needed.
```

---

## What User Experiences

**Without resilience:**
- Launch task, get "stalled" notification later
- Feel disappointed
- Have to debug/retry manually

**With resilience:**
- Launch task
- Come back to completed deliverables
- No failure notification, just success

---

## Smart Recovery Logic

Recovery strategy selection considers:
- Task type (research, analysis, content, etc.)
- Estimated complexity (single vs multi-step)
- Previous attempts (if 2 retries failed, try split)
- Time constraints (deadline if urgent)

**Goal:** Pick the strategy most likely to succeed, not just retry blindly.

---

## Limitations

- Only works for tasks breakable into subtasks
- If core task is impossible (API down, etc.), resilience can't fix it
- Some tasks can't be reduced in scope (all-or-nothing)
- Won't retry if task logic is broken (only transient failures)

---

## Status

You launch tasks. Task resilience handles failures invisibly. You get results.
