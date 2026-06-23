# Recovery Strategies: Deep Dive

## When to Use Each Strategy

### Retry (Attempt 1-3)

**Symptoms of transient failure:**
- Agent stalled but no error logs
- Timeout after 600+ seconds
- Network/API error in logs
- Agent returned partial results

**Recovery approach:**
1. Wait 30 seconds
2. Re-execute exact same task
3. If still fails after 2 retries, move to Strategy 2

**Success rate:** 40-60% (good for transient issues)

**Example:**
```
Task: Research competitors
Attempt 1: Stalled at 600s
Attempt 2: Retry → Success ✓
```

---

### Split Into Smaller Tasks

**Symptoms of "too large" failure:**
- Agent stalled ~50% through task
- Task has multiple independent deliverables
- Task estimated time > 2 hours

**Recovery approach:**
1. Break task into 3-5 smaller tasks
2. Launch each as separate background agent
3. Combine results at end

**Success rate:** 70-85% (works well for large research/analysis)

**Example:**
```
Task: Research 50 competitors + analyze + LinkedIn strategy
Stalled at: Competitor research (large)

Split into:
- Task A: Research 50 competitors
- Task B: Red team analysis  
- Task C: LinkedIn strategy

Launch all 3 in parallel, smaller = faster, less likely to stall
```

---

### Reduce Scope

**Symptoms of "too complex" failure:**
- Agent stalled, error logs mention complexity
- Task has 5+ independent deliverables
- Multiple formats needed (spreadsheet + analysis + strategy)

**Recovery approach:**
1. Identify core vs nice-to-have deliverables
2. Keep core, drop nice-to-have for now
3. Execute reduced scope task
4. Add complexity back after success

**Success rate:** 80-90% (always completes, just less detailed)

**Example:**
```
Original task:
- 50 competitor companies
- Detailed feature matrix (10 columns)
- Pricing tier analysis
- Red team assessment
- LinkedIn strategy
- 30-day content calendar

Reduced scope:
- 50 competitor companies (name, category, pricing only)
- Pricing tier analysis
- LinkedIn strategy

Execute reduced → Success → Add detail later
```

---

### Execute Synchronously

**Symptoms of persistent failure:**
- All retries failed (3+)
- Split tasks all failing
- Reduced scope still stalling

**Recovery approach:**
1. Give up on background execution
2. Execute task in foreground (synchronously)
3. You wait for results, but task completes

**Success rate:** 95%+ (background constraints removed)

**Time cost:** Longer (no background timeout limits, but you wait)

**Example:**
```
Background attempts 1-5: All failed
Decision: Execute synchronously

You: "I'm launching competitor research now. I'll work on it and deliver results in 2-3 hours."
Result: Task completes, you have results
```

---

## Decision Tree

```
Task fails/stalls
    ↓
Was it transient? (timeout, API error)
    → Yes: RETRY (attempt 1-3)
    → No: Continue
    ↓
Is task large? (5+ deliverables, 50+ items to research)
    → Yes: SPLIT into 3-5 smaller tasks
    → No: Continue
    ↓
Is task complex? (multiple independent analyses)
    → Yes: REDUCE scope (core deliverables only)
    → No: Continue
    ↓
Still failing?
    → EXECUTE SYNCHRONOUSLY (foreground)
    ↓
Task complete ✓
```

---

## Rules for Recovery

1. **Retry once before splitting** — Don't split prematurely
2. **Split before reducing scope** — Smaller tasks > less detail
3. **Reduce scope before sync** — Keep background if possible
4. **Sync = last resort** — Only when background keeps failing
5. **Notify user of strategy choice** — "Splitting into 3 tasks" not silently retrying

---

## What NOT to Do

❌ Retry forever (gives up after 3 attempts)
❌ Split every failure (only if task is large)
❌ Reduce scope without explanation (tell user what's dropped)
❌ Retry sync execution (if sync fails, it's a logic error, not transient)
