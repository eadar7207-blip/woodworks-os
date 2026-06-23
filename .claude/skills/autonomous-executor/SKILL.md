# Autonomous Executor

Accepts complex tasks and executes them autonomously with periodic status updates and final reporting. Use when you have research, analysis, content creation, or multi-step projects that don't require real-time interaction.

---

## How It Works

User assigns task → Claude breaks into subtasks → Executes autonomously → **If fails, auto-recovers** → Provides final result

**You don't babysit.** Task runs to completion. If it fails, recovery is automatic (retry, split, reduce scope, or sync execute). You only see success.

---

## Built-In Failure Recovery

Autonomous-executor now includes task-resilience logic:
- **Detects failures/stalls** automatically
- **Picks best recovery strategy** (retry, split, reduce scope, sync)
- **Re-executes transparently** (you don't have to do anything)
- **Notifies you of success** (not failure)

---

## Operations

### `/autonomous [project name] [task description]` - Assign an autonomous task

User provides:
- Project name (for tracking)
- Task description (what needs to be done)
- Optional: deadline, constraints, output format

Claude executes:
1. Breaks task into subtasks
2. Completes each subtask
3. Provides status checkpoint every 30-60 min
4. Delivers final result with summary

**Example:** `/autonomous competitor-analysis Research 50 real estate automation competitors. Map pricing, features, target market. Deliverable: spreadsheet + competitive gaps analysis.`

**Output:**
```
✓ Task accepted: competitor-analysis
Subtasks identified:
  1. Find 50 RE automation companies
  2. Research pricing for each
  3. Map features + target market
  4. Analyze gaps + threats
  5. Create summary spreadsheet

Status: Starting research (estimated 1-2 hours)
I'll checkpoint every 30 min with progress.
```

---

## Status Checkpoints

Every 30-60 minutes, you get:

```
⏱️ Checkpoint: competitor-analysis [2/4 complete]
- Completed: Found 30 companies, researched 20
- In progress: Mapping features for remaining 30
- Next: Create spreadsheet + gap analysis
- ETA: 45 minutes
```

---

## Final Delivery

When complete:

```
✅ Task complete: competitor-analysis
Deliverables:
- 50-company competitive spreadsheet
- Gap analysis + market positioning
- Red team assessment (threats + opportunities)
- Recommendations for differentiation

Files saved to: /wiki/synthesis/
Time invested: 2.5 hours
Quality: High-effort synthesis (not rushed)
```

---

## Task Types (Works Great For)

- **Research:** Market analysis, competitor mapping, trend research
- **Analysis:** Red team assessment, SWOT analysis, strategic planning
- **Content:** Business plans, proposals, pitch decks, case studies
- **Writing:** Long-form content, documentation, marketing copy
- **Strategy:** Competitive positioning, GTM planning, roadmaps

---

## Task Types (Doesn't Work For)

- Real-time interaction needed (coding with user input)
- Approval gates every step (get feedback first, then continue)
- External API/tool calls (requires your approval)

---

## Constraints

- Task must be breakable into independent subtasks
- No real-time decisions (if task needs you, I ask async)
- Output must be self-contained (no "then you do X")
- Deadline: Tell me if urgent (affects priority)

---

## Example Workflow (Success Path)

**You (2pm):**
```
/autonomous linkedin-strategy Create a LinkedIn profile strategy for Eitan Adar selling RE automation. Include: positioning statement, target audience, content pillars, posting schedule, engagement tactics. Deliverable: markdown document + action checklist.
```

**Claude (immediately):**
```
✓ Task accepted: linkedin-strategy
Subtasks: [5 steps identified]
Status: Starting
```

**You (go do other stuff)**

**Claude (3:00pm):**
```
✅ Complete: linkedin-strategy
Deliverable: /wiki/synthesis/linkedin-strategy.md
- Positioning statement (3 variants)
- Content pillars (5 core topics)
- Posting schedule (daily/3x week options)
- 30-day engagement plan

Ready to execute when you are.
```

---

## Example Workflow (With Auto-Recovery)

**You (2pm):**
```
/autonomous competitor-research Research 50 RE automation competitors + red team + LinkedIn strategy.
```

**Claude (immediately):**
```
✓ Task accepted: competitor-research
Status: Starting
```

**You (go do other stuff)**

**Claude (fails internally, auto-recovers):**
```
[Internal: Task stalled at 50% → Too large → Split into 3 smaller tasks]
[Internal: Launching: Competitor research, Red team, LinkedIn strategy]
[Internal: All 3 succeed]
```

**Claude (3:00pm):**
```
✅ Complete: competitor-research
Deliverables:
- /wiki/synthesis/competitor-landscape.md
- /wiki/synthesis/red-team-assessment.md
- /wiki/synthesis/linkedin-strategy.md

(Auto-recovered from failure by splitting into 3 smaller tasks)
```

---

## What You Never See

- ❌ "Task failed" notifications
- ❌ Stalled task discoveries
- ❌ Recovery decisions to make
- ❌ Manual retry/split/retry loops

**What you see:**
- ✅ Task started
- ✅ Task completed (with deliverables)

**Recovery happens automatically in the background.**
