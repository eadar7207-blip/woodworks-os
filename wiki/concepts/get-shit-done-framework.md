---
title: Get Shit Done (GSD) Framework
type: concept
tags: [development, workflows, templates, methodology, gsd]
created: 2026-06-09
updated: 2026-06-09
sources: 0
---

# Get Shit Done (GSD) Framework

Comprehensive meta-prompting and spec-driven development system (64K GitHub stars). Provides workflows, templates, and references for spec-driven development, testing, auditing, and autonomous execution.

## What It Does

GSD provides three complementary systems:

### 1. Workflows (91 templates)
Step-by-step processes for common development tasks:
- **Setup:** `project-init.md`, `setup-dev.md`
- **Development:** `add-phase.md`, `ai-integration-phase.md`, `code-review.md`
- **Testing:** `add-tests.md`, `audit-uat.md`, `ai-evals.md`
- **Delivery:** `complete-milestone.md`, `ship.md`
- **Maintenance:** `cleanup.md`, `audit-fix.md`, `deprecation.md`
- **Research:** `research-phase.md`, `discovery.md`
- **Autonomous:** `autonomous.md` (no babysitting)

### 2. Templates (36 documents)
Structured templates for different artifact types:
- **AI-SPEC.md** — AI/agent feature specifications
- **UI-SPEC.md** — User interface specifications
- **DEBUG.md** — Systematic debugging process
- **VALIDATION.md** — Testing and validation framework
- **UAT.md** — User acceptance testing
- **SECURITY.md** — Security review checklist
- **README.md** — Project documentation template

### 3. References (62 guides)
Deep reference material covering:
- **AI Frameworks** — How LLMs work, prompting patterns, reasoning
- **Agent Contracts** — Defining agent responsibilities, interfaces
- **Context Budget** — Managing token limits, context windows
- **Common Bug Patterns** — 30+ recurring bugs to watch for
- **Artifact Types** — What outputs to generate and when
- **Checkpoints** — When/how to validate work
- **Debugger Philosophy** — How to think about debugging

## Comparison: GSD vs Superpowers

| Aspect | Superpowers | GSD |
|--------|------------|-----|
| **Focus** | Senior-dev workflow (plan→test→code→review) | Spec-driven development + templates + references |
| **Approach** | Forces discipline through framework | Provides templates + playbooks + guidance |
| **Use Case** | Production-ready code (bugs ↓40%) | Structured specs + testing + autonomous work |
| **Output** | Clean code with 100% test coverage | Validated specs → code → tests → delivery |
| **Team Scale** | Individual dev → small team | Full project lifecycle, large teams |

**Best**: Use **both together**
- GSD for specs, workflows, and templates
- Superpowers for code quality and testing discipline

## How to Use GSD

### Workflow Examples

**Starting a new feature:**
```
1. Run `/gsd/workflows/add-phase.md` → creates spec + acceptance criteria
2. Run `/gsd/workflows/ai-integration-phase.md` → adds AI components
3. Run `/gsd/templates/AI-SPEC.md` → structured specification
4. Use superpowers for implementation (plan → test → code → review)
5. Run `/gsd/workflows/audit-uat.md` → validate before shipping
```

**Autonomous task (no babysitting):**
```
1. Load `/gsd/workflows/autonomous.md`
2. Specify task scope, checkpoints, deliverables
3. Claude executes independently
4. Checkpoints every 30-60 min
5. Final delivery with validation
```

**Code review:**
```
1. Run `/gsd/workflows/code-review.md`
2. Use `/gsd/templates/VALIDATION.md` checklist
3. Load `/gsd/references/common-bug-patterns.md`
4. Systematic review catching 80%+ of bugs
```

### Available Workflows

Core workflows in `.claude/gsd/workflows/`:

| Category | Files |
|----------|-------|
| Phases | add-phase, ai-integration-phase, research-phase, discovery, kickoff |
| Development | add-backlog, add-feature, code-review, code-review-fix, refactor |
| Testing | add-tests, audit-uat, ai-evals, test-integration, load-test |
| Quality | audit-fix, audit-milestone, lint, security-audit, perf-audit |
| Delivery | ship, complete-milestone, deprecation, incident-response |
| Maintenance | cleanup, upgrade, migrate, monitor-setup |

## Installation

**Location:** `.claude/gsd/` (installed 2026-06-09)

**Components:**
- 91 workflow templates
- 36 reference templates
- 62 deep reference guides
- 5 context templates (dev, research, review, qa, ops)

## Real Estate Automation Use Cases

**Build an email campaign:**
```
1. Spec phase: `/gsd/workflows/add-phase.md`
   → Define features, acceptance criteria
   
2. AI spec: `/gsd/templates/AI-SPEC.md`
   → Campaign engine, personalization, analytics
   
3. Development: Use superpowers
   → Plan → test → code → review
   
4. Testing: `/gsd/workflows/audit-uat.md`
   → Validate email sending, open tracking, metrics
   
5. Deliver: `/gsd/workflows/ship.md`
   → Production checklist, monitoring setup
```

**Agent prospecting research:**
```
1. Run `/gsd/workflows/research-phase.md`
2. Use `/gsd/templates/RESEARCH.md` (if exists) or create notes
3. Load `/gsd/references/ai-frameworks.md` for reasoning
4. Autonomous execution with checkpoints
5. Synthesize findings into wiki
```

## Integration with Woodworks-OS

**Complements existing systems:**
- **Superpowers** — Code quality + TDD discipline
- **Lead Finder** — Find prospects at scale
- **Email Campaign System** — Nurture automation
- **Wiki** — Persistent memory

**Workflow for new projects:**
1. GSD specs (what are we building?)
2. Superpowers planning (how do we build it well?)
3. Code implementation (with TDD)
4. GSD validation (did we build it right?)
5. Wiki documentation (what did we learn?)

## Key Features by Domain

### For Code
- AI-SPEC.md for agent features
- VALIDATION.md for testing strategies
- common-bug-patterns.md (30+ patterns)
- code-review.md workflow

### For Specs
- 7 different spec templates (UI, API, AI, Security, etc.)
- Checkpoint recommendations
- Acceptance criteria framework

### For Testing
- audit-uat.md (user acceptance testing)
- ai-evals.md (AI system evaluation)
- VALIDATION.md template
- test-integration.md workflow

### For Teams
- Agent contract definitions
- Context templates for different roles
- Large-scale workflow orchestration
- Incident response procedures

## References Available

Load any reference from `.claude/gsd/references/`:

- `ai-frameworks.md` — How LLMs think, prompting techniques
- `agent-contracts.md` — Defining agent responsibilities
- `common-bug-patterns.md` — 30+ recurring bugs
- `context-budget.md` — Token limits and optimization
- `artifact-types.md` — What to generate and when
- `checkpoints.md` — Validation points in workflows
- `debugger-philosophy.md` — Systematic debugging

## Philosophy

From GSD documentation:

> "Get Shit Done means:
> 1. Write the spec first (what are we building?)
> 2. Test the spec (does it make sense?)
> 3. Implement to spec (how do we build it?)
> 4. Validate against spec (did we build it right?)
> 5. Ship with confidence (it's ready)
>
> No half-finished implementations. No guessing. No surprises in production."

## Next Steps

Use GSD for all major Woodworks-OS projects:
- ✅ Email Campaign (already used superpowers, could add GSD specs)
- Prospect outreach automation
- Carousel + email integration
- Real estate CRM sync system

Load workflow templates as needed. Reference guides are always available for deep dives.

## References

- **Repo:** https://github.com/gsd-build/get-shit-done (archived, redirects to open-gsd)
- **Active repo:** https://github.com/open-gsd/gsd-core
- **Framework:** Spec-driven development + autonomous execution
- **Community:** 64K stars, active development
- **License:** MIT
