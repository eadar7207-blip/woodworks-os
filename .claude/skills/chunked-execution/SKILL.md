# Chunked Execution

Breaks large tasks into small independent chunks and executes them sequentially with progress updates. Each chunk completes in 30-60 min, avoiding background agent timeout failures. Use when you have large research, analysis, or content creation tasks that would exceed timeout limits.

---

## Problem Solved

**Issue:** Large background tasks timeout after 600 seconds, leaving work incomplete.

**Root cause:** Background agents have hard timeout limits. Tasks over ~10-15 min of continuous work stall.

**Solution:** Break task into small chunks (30-60 min each), execute sequentially, track progress. No single chunk exceeds timeout.

---

## How It Works

1. **Define the task** (what needs doing)
2. **Break into chunks** (3-5 independent pieces)
3. **Execute chunk 1** (30-60 min, completes)
4. **Progress update** (you know what's done)
5. **Execute chunk 2-5** (same process)
6. **Deliver final result** (all chunks combined)

**Key:** Each chunk is independent. If one fails, retry that chunk only (don't restart the whole task).

---

## Operations

### `/chunked [project name] [task description + chunks]` - Execute task in chunks

**Example:**
```
/chunked competitor-research
Chunk 1: Research competitors 1-20 (pricing, features, positioning)
Chunk 2: Research competitors 21-40 (same)
Chunk 3: Research competitors 41-50 + map landscape gaps
Chunk 4: Red team assessment (threats + vulnerabilities)
Chunk 5: LinkedIn strategy (positioning + content plan)

Save results to /wiki/synthesis/ after each chunk.
```

**Execution flow:**
```
✓ Chunk 1 complete: 20 competitors researched
✓ Chunk 2 complete: 40 competitors total
✓ Chunk 3 complete: 50 competitors + gaps analysis
✓ Chunk 4 complete: Red team assessment done
✓ Chunk 5 complete: LinkedIn strategy done

✅ Task complete: All deliverables in /wiki/synthesis/
```

---

## Chunk Strategy

**Good chunks:**
- Independent (don't need chunk 3 to do chunk 1)
- Time-bounded (30-60 min each)
- Deliverable-focused (chunk = one output)
- Retryable (can redo chunk 2 without chunk 1)

**Bad chunks:**
- Sequential dependencies (chunk 2 needs chunk 1 done)
- Vague time bounds (might be 30 min or 3 hours)
- Sub-tasks mixed (chunk = multiple different outputs)

---

## When to Use

**Use `/chunked` when:**
- Task is large (2+ hours total)
- Multiple independent components
- Want reliable completion (not timeout failures)
- Need progress visibility

**Use `/autonomous` when:**
- Task is small-medium (under 2 hours)
- Single unified deliverable
- Don't need chunk visibility

---

## Progress Tracking

Each chunked task writes progress to `/tmp/chunk-progress-[task-name].md`:

```
✓ Chunk 1/5 complete: Research competitors 1-20
✓ Chunk 2/5 complete: Research competitors 21-40
⏳ Chunk 3/5 in progress: Landscape analysis
⏱️ ETA: 20 minutes remaining
```

Use `/progress-monitor [task-name]` to watch progress in real-time and get updates.

---

## Example: Competitor Research

**Without chunks (fails):**
```
/autonomous competitor-research Research 50 competitors + red team + LinkedIn
❌ Stalls at 600s, fails
```

**With chunks + progress monitoring (succeeds):**
```
/chunked competitor-research
Chunk 1: Research 20 competitors
Chunk 2: Research 20 more competitors  
Chunk 3: Research final 10 + landscape gaps
Chunk 4: Red team analysis
Chunk 5: LinkedIn strategy

Then run: /progress-monitor competitor-research

You get updates:
✓ Chunk 1 done
✓ Chunk 2 done
✓ Chunk 3 done
→ Final results in /wiki/synthesis/
```

---

## Success Rate

- **`/autonomous` (large task):** 30-40% (timeout risk)
- **`/chunked` (same task):** 90%+ (small chunks, reliable)

**Difference:** Chunking removes timeout risk by keeping each execution short.
