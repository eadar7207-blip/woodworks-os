# Approval Detection Logic

## Recognized Approval Patterns

Single-word approvals:
- "yes"
- "go"
- "launch"
- "execute"
- "do it"
- "start"
- "run"
- "ok"

Multi-word approvals:
- "launch it"
- "execute it"
- "do it"
- "let's go"
- "start it"
- "run it"
- "yes go"

## How Detection Works

1. Listen for user response to "Ready to launch?" or similar approval questions
2. Parse user's response
3. Match against approval patterns (case-insensitive)
4. If match found: trigger auto-execution
5. If no match: wait for clarification

## Pending Task State

When I ask "Ready to launch?", the pending task is held in state:
- Task type (autonomous, chunked, etc.)
- Task description
- Parameters
- Execution method (Agent tool, background)

When approval is detected, auto-launch immediately executes using this stored state.

## Edge Cases

- Typos ("yse", "laucnh") — require exact match to prevent false positives
- Contextual approvals ("sounds good", "let's do it") — keep pattern list focused on explicit approvals
- No false positives — better to ask again than execute the wrong thing

## Integration with Other Skills

Auto-launch works with:
- `/autonomous` — execute small tasks
- `/chunked` — execute large tasks (broken into chunks)
- Any background task requiring approval

Auto-launch is invisible to these skills — they just work normally, auto-launch handles the approval→execution bridge.
