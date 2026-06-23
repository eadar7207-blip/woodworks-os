# Progress File Format

## Standard Format

Progress files are written to `/tmp/chunk-progress-[task-name].md` during execution.

## Schema

```
✓ Chunk [N]/[TOTAL] complete: [chunk description] ([elapsed time])
⏳ Chunk [N]/[TOTAL] in progress: [chunk description]
⏱️ Started: [YYYY-MM-DD HH:MM]
⏱️ ETA: [X minutes remaining]
```

## Examples

### Running task (3 chunks done, 1 in progress, 1 remaining)

```
✓ Chunk 1/5 complete: Research competitors 1-20 (25 min)
✓ Chunk 2/5 complete: Research competitors 21-40 (25 min)
✓ Chunk 3/5 complete: Landscape analysis (30 min)
⏳ Chunk 4/5 in progress: Red team assessment
⏱️ Started: 2026-06-05 14:30
⏱️ ETA: 40 minutes remaining
```

### Completed task

```
✓ Chunk 1/5 complete: Research competitors 1-20 (25 min)
✓ Chunk 2/5 complete: Research competitors 21-40 (25 min)
✓ Chunk 3/5 complete: Landscape analysis (30 min)
✓ Chunk 4/5 complete: Red team assessment (40 min)
✓ Chunk 5/5 complete: LinkedIn strategy (45 min)
✅ Task complete
🎯 Deliverables: /wiki/synthesis/competitor-landscape.md, /wiki/synthesis/red-team-assessment.md, /wiki/synthesis/linkedin-strategy.md
```

## Monitoring Logic

Progress Monitor:
1. Reads progress file every 30 seconds
2. Compares to last known state
3. Reports new completions
4. Reports every 10 minutes even if no change (to show it's still working)
5. Reports final completion + deliverable location

## Error Handling

If progress file doesn't exist after 5 minutes:
- Task may not have started
- May be queued
- May have failed to initialize

If progress stops updating:
- May be stalled
- May be processing a long chunk
- Manual check recommended after 30 min no update
