# Progress Monitor

Reads progress files from running chunked tasks and reports real-time updates to you. Shows what's complete, what's in progress, and estimated time remaining. Use when you need visibility into background chunked-execution tasks without waiting until completion.

---

## How It Works

1. **Chunked task runs** — writes progress to `/tmp/chunk-progress-[task-name].md`
2. **You start monitoring** — `/progress-monitor [task-name]`
3. **Progress Monitor reads file** — every 30 seconds
4. **Reports updates** — when chunks complete or status changes
5. **You see real-time progress** — no radio silence

---

## Progress File Format

Chunked tasks write progress like this:

```
✓ Chunk 1/5 complete: Research competitors 1-20 (25 min)
✓ Chunk 2/5 complete: Research competitors 21-40 (25 min)
⏳ Chunk 3/5 in progress: Landscape analysis
⏱️ Started: 2026-06-05 14:30
⏱️ ETA: 20 minutes remaining
```

Progress Monitor parses this and reports back.

---

## Operations

### `/progress-monitor [task-name]` - Watch a running task

**Example:** `/progress-monitor competitor-research`

Monitors `/tmp/chunk-progress-competitor-research.md` and reports:
- When chunks complete
- Current chunk progress
- ETA updates
- Final completion

**Updates reported:**
- New chunk completion
- Every 10 minutes even if no change
- Final completion + deliverable location

---

## Example Workflow

**You launch task:**
```
/chunked competitor-research
[5 chunks identified]
```

**You start monitoring:**
```
/progress-monitor competitor-research
```

**You see updates:**
```
✓ Chunk 1/5 complete: Research 1-20 (25 min elapsed)
✓ Chunk 2/5 complete: Research 21-40 (25 min elapsed)
⏳ Chunk 3/5 in progress: Landscape analysis
ETA: 30 minutes

[10 min later]
✓ Chunk 3/5 complete: Landscape analysis (30 min elapsed)
⏳ Chunk 4/5 in progress: Red team assessment
ETA: 40 minutes

[40 min later]
✓ Chunk 4/5 complete: Red team assessment
✓ Chunk 5/5 complete: LinkedIn strategy
✅ Task complete
Deliverables: /wiki/synthesis/
```

---

## Why This Matters

Without progress monitoring:
- Task runs "in the background"
- You have no visibility
- You don't know if it's working or stuck
- You can't see progress

With progress monitoring:
- Real-time updates every chunk
- Know exactly what's done and what's remaining
- See ETAs
- Know immediately if something goes wrong

---

## Status

Production-ready. Use with `/chunked` for full visibility into large task execution.
