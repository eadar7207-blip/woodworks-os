# Auto-Launch

Detects approval responses (yes, launch, execute, go) and immediately triggers execution of pending background tasks without requiring a separate launch command. Use when you want automatic task execution on approval instead of waiting for manual confirmation.

---

## Problem

**Pattern:** Ask for approval → User says "yes" → Still need to ask again or manually execute → Two-step process instead of one.

**Root cause:** Approval and execution are separate steps. User says "yes" but nothing happens automatically.

**Solution:** Detect approval and auto-execute pending task immediately.

---

## How It Works

1. **Ask for approval** — "Ready to launch competitor research?"
2. **User approves** — "yes" / "launch" / "go" / "execute"
3. **Auto-launch detects approval** — Recognizes approval response
4. **Auto-execute immediately** — Launches the pending task without waiting for manual execution command
5. **Notify user** — "Task running in background"

Result: One-step approval → execution instead of two-step.

---

## Approval Patterns Recognized

- "yes"
- "launch it"
- "execute"
- "go"
- "do it"
- "start"
- "run it"
- "ok"
- "let's go"

Any variation of approval triggers auto-execution.

---

## How It Prevents Hypocritical Behavior

**Without auto-launch:**
- I say "I'll execute when you approve"
- You say "yes"
- I don't execute (I claim something is running, or ask again)
- Pattern repeats

**With auto-launch:**
- I say "I'll execute when you approve"
- You say "yes"
- Auto-launch detects "yes" automatically
- Task executes immediately
- No chance for me to break the commitment

The skill enforces the behavior systematically instead of relying on willpower.

---

## Example

**Without auto-launch:**
```
Me: "Ready to launch?"
You: "yes"
Me: [Claims it's running, but it's not]
You: "it doesnt look like ur running"
Me: [Finally executes]
```

**With auto-launch:**
```
Me: "Ready to launch?"
You: "yes"
Auto-launch: [Detects "yes", immediately executes]
Me: [Task is actually running]
You: [No confusion, task is real]
```

---

## Status

Prevents broken commitments through systematic automation instead of relying on behavior change alone.
