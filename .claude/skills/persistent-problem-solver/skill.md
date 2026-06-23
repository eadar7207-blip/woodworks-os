---
name: persistent-problem-solver
description: Never gives up. When a task fails, automatically tries different approaches until one works. Pivots strategy, breaks problems differently, finds alternative paths.
usage: /persistent-problem-solver "{failed_task}" "{failure_reason}"
examples:
  - /persistent-problem-solver "Research 50 real estate competitors" "Agent stalled after 600s"
  - /persistent-problem-solver "Generate marketing content" "Claude API timeout"
  - /persistent-problem-solver "Analyze sales data" "Database connection failed"
---

# Persistent Problem Solver

A skill that never gives up. When tasks fail, it automatically tries different approaches until one works. Not just retry — actually pivot strategy.

**What it does:**
- 🔄 **Detects failures** — Task failed? Captures the reason
- 🧠 **Analyzes root cause** — Why did it fail? Transient error? Too big? Wrong approach?
- 🔀 **Pivots strategy** — Tries completely different method
- 🔁 **Keeps trying** — If approach B fails, try approach C, D, E...
- ✅ **Succeeds or escalates** — Either delivers result or asks for help

---

## How It Works

### Failed Task Lifecycle

```
Task: "Research 50 RE automation competitors"
Status: FAILED (agent stalled after 600s)
         ↓
Persistent Problem Solver detects
         ↓
Analysis: "Task too big, needs breaking down"
         ↓
Try Approach A: Split into 3 smaller research tasks
         ├─ Task A1: Competitors 1-20 ✅ Success
         ├─ Task A2: Competitors 21-35 ✅ Success
         ├─ Task A3: Competitors 36-50 ✅ Success
         ↓
Result: All 50 competitors researched
Delivered: competitor-analysis.md
Status: ✅ RECOVERED
```

---

## Approach Selection

When a task fails, Persistent Problem Solver tries approaches in order:

### Attempt 1: **Retry with backoff**
- Same approach, wait & retry with exponential backoff
- Best for: Transient errors (timeout, API hiccup, temporary block)
- Success rate: 40-50%

### Attempt 2: **Split into subtasks**
- Break large task into 3-5 smaller independent pieces
- Run in parallel or sequence
- Best for: Tasks that stall due to size/complexity
- Success rate: 70-80%

### Attempt 3: **Simplify the approach**
- Remove dependencies, constraints, nice-to-haves
- Focus on core deliverable only
- Add extras later after success
- Best for: Over-engineered solutions
- Success rate: 60-70%

### Attempt 4: **Change the tool/method**
- If using Claude API → try local processing
- If using one tool → try alternative tool
- If sequential → try parallel
- Best for: Tool/resource issues
- Success rate: 50-60%

### Attempt 5: **Get human input**
- Escalate to you with: "Here's what I tried. How should I approach this differently?"
- Best for: Truly stuck (approach A-D all failed)
- Success rate: High (human insight)

---

## Real Examples

### Example 1: API Timeout
```
Task: "Generate 100 property descriptions"
Error: "Claude API timeout on request 47"

Attempt 1: Retry with backoff ✅ SUCCESS
→ Same task, wait 10s, retry
→ Succeeds on second try

Result: All 100 descriptions generated
```

### Example 2: Task Too Large
```
Task: "Analyze 1000 competitor websites + red team + pricing strategy"
Error: "Agent stalled, no progress for 600s"

Attempt 1: Retry with backoff ❌ Failed again
Attempt 2: Split into subtasks ✅ SUCCESS
→ Split into:
  - Analyze 1000 websites (chunked into 5 tasks)
  - Red team assessment
  - Pricing strategy
→ All 3 complete

Result: Full analysis delivered
```

### Example 3: Tool Limitation
```
Task: "Process 10GB video file"
Error: "GPU memory exceeded"

Attempt 1: Retry ❌ Same error
Attempt 2: Split into smaller files ✅ SUCCESS
→ Break into 5 × 2GB chunks
→ Process each chunk
→ Merge results

Result: Full video processed
```

### Example 4: Needs Human Help
```
Task: "Design marketing campaign for luxury real estate"
Error: "Too vague, doesn't know target audience"

Attempt 1: Simplify ❌ Still too vague
Attempt 2: Change approach ❌ Doesn't improve
Attempt 3: Split ❌ Can't without more info
Attempt 4: Get human input ✅ YOU DECIDE
→ "I've tried 3 approaches. Tell me: Target audience? Budget? Timeline?"
→ You provide info
→ Restarts with clear context

Result: Campaign designed correctly
```

---

## Configuration

In `.claude/settings.json`:

```json
{
  "persistent_problem_solver": {
    "max_attempts": 5,
    "timeout_per_attempt": 600,
    "escalate_after_attempts": 4,
    "strategies": ["retry", "split", "simplify", "change_tool", "human_input"],
    "parallelization": true,
    "notification_level": "success_only"
  }
}
```

**Key settings:**
- `max_attempts` — How many different approaches to try (default: 5)
- `escalate_after_attempts` — After how many failures, ask for human help
- `parallelization` — Can subtasks run in parallel? (faster)
- `notification_level` — When to notify you (only on success, or on each attempt)

---

## Automatic Triggering

Add this hook to `.claude/settings.json`:

```json
{
  "hooks": {
    "on_task_failure": {
      "trigger": "task_failed",
      "action": "invoke_skill",
      "skill": "persistent-problem-solver",
      "auto_run": true,
      "background": true,
      "notify_on": "success"
    }
  }
}
```

**What this does:**
- When ANY task fails → Persistent Problem Solver launches automatically
- Runs in background (you don't wait)
- Tries approaches A, B, C, D until one works
- Notifies you only on success (or when it needs your input)

---

## Output

When task recovers:

```json
{
  "original_task": "Research 50 competitors",
  "original_failure": "Agent stalled (600s timeout)",
  "recovery_approach": "Split into 3 subtasks",
  "attempts_made": 2,
  "final_status": "SUCCESS",
  "result_file": "competitor-analysis.md",
  "time_taken": "15 minutes",
  "message": "Task completed via subtask approach. Delivered: competitor-analysis.md"
}
```

---

## When It Works Best

✅ **Good use cases:**
- Large research/analysis tasks (too big, stalls)
- API-dependent tasks (transient failures)
- Complex multi-step workflows (needs breaking down)
- Resource-intensive operations (GPU memory, timeouts)

❌ **Won't help with:**
- Broken logic (wrong approach entirely)
- Impossible requests (API down permanently, impossible constraint)
- Requires domain expertise you don't have

For impossible cases → Escalates to you with context.

---

## Integration Examples

### With Auto-Launch
```
You: "Research 50 competitors"
Fails after 600s
Auto-launch triggers → Persistent Problem Solver
Tries split approach → SUCCESS
You get notified: "Research complete: competitor-analysis.md"
```

### With Chunked Execution
```
You: /chunked big-research
Chunk 1: Part A ✅
Chunk 2: Part B ❌ FAILS
Persistent Problem Solver detects
Tries different approach → ✅
Chunk 2 completes
Result: All chunks delivered
```

---

Built for Eitan Adar's automation agency.
Never give up. Always find a way.
