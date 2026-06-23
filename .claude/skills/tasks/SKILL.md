---
name: tasks
description: Manage to-dos, priorities, and project tracking — create, update, and track task progress
---

# Tasks

Manage your to-do list, priorities, and project work. All tasks live in the wiki so they persist across sessions.

---

## Operations

### `/tasks add [title]` - Create a new task

When adding a task:

1. Ask: priority (high/medium/low), due date (optional), project (optional), who's doing it
2. Create a task entry in `wiki/tasks.md` with:
   - Task name
   - Status: pending | in-progress | done
   - Priority: high | medium | low
   - Due date (if set)
   - Project (if applicable)
   - Notes or context

3. Update `wiki/overview.md` if this is a high-priority blocking item

Example: `/tasks add Draft proposal for ABC Real Estate`

Then you provide: due date, priority, project name

### `/tasks update [task name] [status]` - Move task status

Statuses: `pending | in-progress | done`

- `/tasks update Draft proposal in-progress` — you're working on it now
- `/tasks update Draft proposal done` — mark it complete

When you mark something done, log it in `wiki/log.md` with the outcome.

### `/tasks view [filter]` - Show your tasks

Filters:
- `today` — tasks due today or overdue
- `week` — tasks due this week
- `high` — high-priority tasks only
- `in-progress` — what you're currently working on
- `[project-name]` — all tasks for a specific project
- `all` — everything

Example: `/tasks view high` shows all high-priority tasks

### `/tasks dashboard` - Task summary

Show:
- High-priority tasks due soon
- Tasks in progress (what you're working on now)
- Overdue tasks
- This week's workload
- Next 3 critical items

One-screen view of what matters.

---

## Task Structure in Wiki

Tasks live in `wiki/tasks.md` in this format:

```markdown
---
title: Tasks
type: tasks
updated: YYYY-MM-DD
---

# Tasks

## [Project Name] (if organizing by project)

- [ ] [Task Name] | Priority: high | Due: YYYY-MM-DD | Status: pending
- [x] [Task Name] | Priority: medium | Due: YYYY-MM-DD | Status: done
- [ ] [Task Name] | Priority: low | Due: YYYY-MM-DD | Status: in-progress

## Inbox (unsorted or quick tasks)

- [ ] [Task Name] | Priority: medium | Status: pending
```

Use checkboxes: `[ ]` for pending/in-progress, `[x]` for done.

---

## Linking Tasks to Your Work

Tasks can reference:
- Prospects: `[[ABC Real Estate]]` (links to prospect page)
- Projects: `projects/[project-name]`
- Automations: reference `/automate` outputs
- Proposals: note which proposal this supports

Example task:
```
- [ ] Draft proposal for [[ABC Real Estate]] | Priority: high | Due: 2026-06-05
```

---

## Priority Rules

- **High** — Blocks other work or revenue-critical (proposal due, lead follow-up, client issue)
- **Medium** — Important but not blocking (skill refinement, wiki update, content creation)
- **Low** — Nice-to-have or can wait (cleanup, documentation, learning)

---

## Weekly Review

Every Monday, run `/tasks dashboard` to see:
- What didn't get done last week (why?)
- What's critical this week
- What can move to next week

Update `wiki/overview.md` if workload is heavy or capacity is constrained.

---

## Task Lifecycle

1. **Create** — `/tasks add [name]` with priority and due date
2. **Work** — `/tasks update [name] in-progress` when you start
3. **Complete** — `/tasks update [name] done` when finished
4. **Log** — Major task completions get a line in `wiki/log.md`

Keep the list lean — if you have 20+ pending tasks, re-prioritize. Focus beats volume.
