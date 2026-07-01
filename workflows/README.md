# Workflows

Markdown SOPs for recurring tasks. These are living documents -- update them when you learn something new.

## Conventions
- One file per workflow (e.g. `scrape_website.md`, `qualify_lead.md`)
- Each file should include: objective, required inputs, tools to call, expected output, edge cases
- Don't delete or overwrite without being asked -- these are instructions, not throwaway notes

## Adding a new workflow
Copy this structure:

```
# Workflow Name

## Objective
What this workflow accomplishes.

## Inputs
- input_1: description
- input_2: description

## Steps
1. Step one -- call `tools/script.py` with X
2. Step two -- ...

## Output
What the final result looks like and where it goes.

## Edge Cases
- Known failure modes and how to handle them
```
