---
name: gsd
description: Use when you need GSD workflows, templates, or references. Load workflows for specs, testing, and validation. Copy templates for structured artifacts. Check references for patterns and guidance.
argument-hint: [workflow|template|reference] [name or keyword]
---

## Get Shit Done (GSD) Command

Access 91 workflows, 36 templates, and 62 references from the GSD framework.

## Usage

### List available resources
```
/gsd list workflows
/gsd list templates
/gsd list references
```

### Load a workflow
```
/gsd workflow add-phase
/gsd workflow code-review
/gsd workflow autonomous
/gsd workflow ship
```

### Copy a template
```
/gsd template ai-spec
/gsd template validation
/gsd template debug
/gsd template uat
```

### Check a reference
```
/gsd reference common-bug-patterns
/gsd reference ai-frameworks
/gsd reference context-budget
```

### Search by keyword
```
/gsd search "email"
/gsd search "test"
/gsd search "autonomous"
```

## What's Available

### Workflows (91 total)
**Phases:** `add-phase`, `ai-integration-phase`, `research-phase`, `discovery`, `kickoff`
**Development:** `add-feature`, `code-review`, `code-review-fix`, `refactor`, `add-backlog`
**Testing:** `add-tests`, `audit-uat`, `ai-evals`, `test-integration`
**Delivery:** `ship`, `complete-milestone`, `deprecation`, `incident-response`
**Maintenance:** `cleanup`, `upgrade`, `migrate`, `monitor-setup`
**Autonomous:** `autonomous` (no babysitting execution)

**Most useful:**
- `add-phase.md` — Start new feature with acceptance criteria
- `code-review.md` — Systematic code review
- `ai-integration-phase.md` — Add AI/agent components
- `audit-uat.md` — User acceptance testing
- `autonomous.md` — Execute tasks independently
- `ship.md` — Production delivery checklist

### Templates (36 total)
- `AI-SPEC.md` — AI/agent feature specification
- `UI-SPEC.md` — User interface specification
- `VALIDATION.md` — Testing and validation framework
- `DEBUG.md` — Systematic debugging process
- `UAT.md` — User acceptance testing checklist
- `SECURITY.md` — Security review checklist
- `README.md` — Project documentation

### References (62 total)
- `common-bug-patterns.md` — 30+ recurring bugs to watch
- `ai-frameworks.md` — How LLMs work, prompting techniques
- `agent-contracts.md` — Defining agent responsibilities
- `context-budget.md` — Token limits and optimization
- `artifact-types.md` — What to generate and when
- `checkpoints.md` — Validation points in workflows
- `debugger-philosophy.md` — Systematic debugging

## Real Estate Automation Examples

**Building email campaign feature:**
```
1. /gsd workflow add-phase
   → Define what we're building
2. /gsd template ai-spec
   → Spec the email engine
3. Use superpowers for implementation
4. /gsd workflow code-review
   → Systematic review
5. /gsd workflow audit-uat
   → Validate before shipping
```

**Autonomous prospect research:**
```
1. /gsd workflow autonomous
   → Set up independent execution
2. /gsd reference ai-frameworks
   → Load reasoning patterns
3. Claude executes with checkpoints
4. /gsd template validation
   → Verify results
```

**Code review workflow:**
```
1. /gsd workflow code-review
   → Follow review process
2. /gsd reference common-bug-patterns
   → Check for 30+ patterns
3. /gsd template validation
   → Verify against spec
```

## How It Works

When you run `/gsd workflow [name]`, I:
1. Load the workflow from `.claude/gsd/workflows/[name].md`
2. Display it in a readable format
3. You follow the steps in order
4. Each step tells you exactly what to do

When you run `/gsd template [name]`, I:
1. Copy the template from `.claude/gsd/templates/[name].md`
2. Show you the structure
3. You customize it for your project

When you run `/gsd reference [name]`, I:
1. Load the reference from `.claude/gsd/references/[name].md`
2. Display it with key sections highlighted
3. You use it during your work

## Workflow Philosophy

From GSD:

> 1. Write the spec first (what are we building?)
> 2. Test the spec (does it make sense?)
> 3. Implement to spec (how do we build it?)
> 4. Validate against spec (did we build it right?)
> 5. Ship with confidence (it's ready)

Use workflows to enforce this discipline systematically.

## Integration with Superpowers

**Superpowers** (code quality):
- Plan → Test → Code → Review → Deliver

**GSD** (spec-driven):
- Spec → Validate Spec → Code → Validate Code → Ship

Use them together:
1. GSD workflow → create detailed spec
2. Superpowers planning → architecture design
3. Superpowers testing → TDD implementation
4. GSD validation → UAT and shipping checklist

## Notes

- All workflows are in `.claude/gsd/workflows/`
- All templates are in `.claude/gsd/templates/`
- All references are in `.claude/gsd/references/`
- You can read any file directly if you prefer
- Copy templates into your project and customize them
- Load references anytime for guidance
