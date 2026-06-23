# Chunking Strategy Guide

## How to Break a Task into Chunks

### Step 1: Identify the goal
- What's the final deliverable?
- How many independent parts are there?

### Step 2: Find natural breakpoints
- By volume (research 1-20, 21-40, 41-60)
- By analysis type (data gathering, synthesis, strategy)
- By deliverable (report 1, report 2, report 3)

### Step 3: Estimate time per chunk
- Aim for 30-60 min per chunk
- If estimate > 60 min, split further
- If estimate < 15 min, combine with another chunk

### Step 4: Check independence
- Can chunk 2 run without chunk 1?
- Can chunk 3 be retried independently?
- If not, recombine chunks

---

## Example Breakdowns

### Research Task (50 items)

**Bad chunking:**
```
Chunk 1: Research items 1-50 and analyze
❌ Too large, will timeout
```

**Good chunking:**
```
Chunk 1: Research items 1-15 (20 min)
Chunk 2: Research items 16-30 (20 min)
Chunk 3: Research items 31-45 (20 min)
Chunk 4: Research items 46-50 + landscape analysis (30 min)
Chunk 5: Red team assessment (40 min)
✓ Each chunk 20-40 min, independent, deliverable-focused
```

---

### Analysis Task (Report + Strategy + Content)

**Bad chunking:**
```
Chunk 1: Everything (analysis + strategy + content)
❌ Too large, dependencies unclear
```

**Good chunking:**
```
Chunk 1: Market analysis (40 min) → analysis.md
Chunk 2: Red team assessment (35 min) → red-team.md
Chunk 3: Strategy document (45 min) → strategy.md
Chunk 4: LinkedIn content plan (30 min) → linkedin.md
✓ Each chunk is independent, clear output, 30-45 min
```

---

## Time Estimation Rules

- **Research:** ~2-3 min per item × quantity = chunk time
- **Analysis:** ~30 min per major analysis type
- **Writing:** ~10-15 min per 500 words
- **Synthesis:** ~30-40 min per major insight/framework

**Always pad by 20-30%** for unknowns.

---

## Retry Logic

If chunk fails:
1. Identify which chunk failed
2. Retry that chunk only
3. Don't restart earlier chunks
4. Don't start later chunks until this one succeeds

**Example:**
```
✓ Chunk 1 done
✓ Chunk 2 done
✗ Chunk 3 fails → Retry chunk 3 (don't redo 1-2)
✓ Chunk 3 done (retry)
→ Continue with chunk 4
```

---

## When Chunks Are Too Small/Large

**Too small (< 15 min):**
- Combine with next chunk
- Less overhead from progress updates

**Too large (> 90 min):**
- Split into 2-3 smaller chunks
- Reduces timeout risk

**Goldilocks (30-60 min):**
- Fast enough to avoid timeout
- Slow enough to minimize overhead
- Best reliability
