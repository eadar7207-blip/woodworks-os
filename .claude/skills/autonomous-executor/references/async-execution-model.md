# Async Execution Model

## How Autonomous Tasks Work

### The Contract

**You provide:** Task description + constraints
**Claude provides:** Breakdown + execution + checkpoints + final result

**You don't provide:** Real-time feedback at each step

---

## Execution Phases

### Phase 1: Task Acceptance
- Parse task description
- Identify subtasks
- Estimate timeline
- Check feasibility
- Return plan + checkpoint schedule

### Phase 2: Autonomous Execution
- Complete subtask 1
- Complete subtask 2
- (Continue autonomously)
- Provide checkpoint every 30-60 min

### Phase 3: Synthesis & Delivery
- Compile results
- Write summary
- Deliver final output
- File in wiki/synthesis/

---

## Checkpoint Strategy

**Frequency:** Every 30-60 minutes (varies by task size)

**Content:**
- What's done
- What's in progress
- What's remaining
- ETA to completion

**Purpose:** Keep you informed, not interrupt work

---

## Quality Over Speed

Autonomous execution prioritizes:
1. Thoughtful analysis (not rushed)
2. Comprehensive research (not surface-level)
3. Synthesis that makes sense (not forced)
4. Documentation that's usable (not raw output)

Time = Quality

---

## When to Use Async

Good use cases:
- Research (find + analyze + summarize)
- Planning (business plans, strategies, roadmaps)
- Analysis (red teams, competitive assessment, SWOT)
- Content (long-form, structured, high-effort)
- Synthesis (pulling together complex information)

Bad use cases:
- Coding (needs your input/approval at steps)
- Decisions (needs your judgment)
- External actions (needs your approval)
- Real-time needs (can't wait 2 hours)

---

## What "Autonomous" Means

✓ Complete task to completion without asking
✓ Make reasonable judgment calls
✓ Deliver high-effort, thoughtful work
✓ Checkpoint async (inform, don't interrupt)

✗ Don't ask for approval on every step
✗ Don't oversimplify to finish faster
✗ Don't interrupt you in real-time
✗ Don't require your constant feedback

---

## Example: Competitor Research

**Task:** Research 50 RE automation competitors

**Autonomously:**
1. Identify 50 companies (search, compilation)
2. Research each (pricing, features, positioning)
3. Map competitive landscape (gaps, threats, opportunities)
4. Synthesize findings (patterns, whitespace, recommendations)
5. Create deliverable (spreadsheet + analysis)

**Checkpoint every 30-45 min:** Progress + ETA

**Deliver:** Complete competitive analysis (no babysitting needed)
