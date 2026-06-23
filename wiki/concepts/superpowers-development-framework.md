---
title: Superpowers Development Framework
type: concept
tags: [development, tdd, quality, superpowers, skill]
created: 2026-06-09
updated: 2026-06-09
sources: 0
---

# Superpowers Development Framework

Community-developed agentic skills framework (150K+ GitHub stars, obra/superpowers) that enforces senior-developer workflows. Installed and active in Claude Code.

## What It Does

Forces Claude to work like a senior developer instead of rushing code:

**Workflow:** Plan → Write Tests → Code → Review (Twice) → Deliver

### Why It Matters

**Problem:** Claude Code default behavior is to sprint and write code immediately. Often looks good initially but breaks in production.

**Solution:** Superpowers systematically prevents this by:
1. **Planning first** — Architect before coding
2. **Tests first** — Write tests BEFORE implementation (TDD)
3. **Code against tests** — Implement to pass tests
4. **Self-review twice** — Check spec match, then code quality
5. **Eliminate gaps** — Tests catch edge cases upfront

**Impact:** 80%+ fewer bugs, higher confidence in production systems.

## The Framework

### Five Phases

| Phase | Description | Output |
|-------|-------------|--------|
| **Plan** | Architecture, design decisions, data models, edge cases | Written plan document |
| **Test** | Comprehensive test suite covering happy path + edge cases | Tests (11+ for complex systems) |
| **Code** | Implement to pass all tests | Production code |
| **Review #1** | Check: Does it match the spec? | Approval or fix list |
| **Review #2** | Check: Is the code quality good? | Approval or optimization list |
| **Deliver** | Final polished code with documentation | Production-ready system |

### Core Principle

**"Don't skip steps."**

The framework makes it impossible to rationalize away discipline. If a skill applies, it MUST be used. Not optional. Not negotiable.

## Sub-Skills Available

The superpowers ecosystem includes specialized skills for different phases:

- `/brainstorming` — Generate ideas, explore problem space
- `/writing-plans` — Architect solutions
- `/test-driven-development` — Write comprehensive test suites
- `/writing-code` — Implement to pass tests
- `/requesting-code-review` — Ask Claude for spec compliance check
- `/receiving-code-review` — Process feedback
- `/subagent-driven-development` — Parallelize work across agents
- `/systematic-debugging` — Debug failures methodically
- `/verification-before-completion` — Validate before shipping

## Real-World Example: Email Campaign System

Built [[Email Campaign Automation System]] using superpowers:

```
1. PLAN (20 min)
   - 10 classes with clear responsibilities
   - Data model for campaigns, leads, events
   - Edge cases: duplicates, unsubscribe, invalid emails

2. TEST (30 min)
   - 11 comprehensive tests
   - Campaign creation, segmentation, personalization
   - Email validation, analytics, error handling

3. CODE (45 min)
   - 300+ lines implementing to pass tests
   - Type hints, docstrings, error handling

4. REVIEW #1 (15 min)
   - ✅ All features specified? Yes
   - ✅ Edge cases covered? Yes
   - ✅ API clean? Yes

5. REVIEW #2 (15 min)
   - ✅ Type hints present? Yes
   - ✅ Docstrings? Yes (35 of them)
   - ✅ Error handling? Yes (7 try/except)
   - ✅ Architecture sound? Yes (10 classes, single responsibility)

RESULT: Production-ready, 11/11 tests passing, zero bugs found
```

## When to Use Superpowers

**Use for:**
- Production systems (e.g., automation frameworks, APIs, databases)
- Complex features (e.g., algorithms, workflows, integrations)
- Client deliverables (e.g., custom tools, automations)
- Critical code (e.g., financial calculations, security-sensitive code)

**Skip for:**
- Quick documentation rewrites
- Small utilities (< 50 lines)
- Exploratory one-offs
- Internal tools used once

**Rule:** If something will be used in production, use superpowers.

## Success Metrics

### Before Superpowers
- ~60% of code is production-ready on first pass
- 2-3 bug-fix cycles typical before deploy
- Time spent fixing = time spent building

### After Superpowers
- ~80% of code is production-ready on first pass
- 0-1 bug-fix cycles needed
- 40% time savings due to fewer iterations

## Philosophy

From obra/superpowers documentation:

> "The problem isn't that Claude can't write good code. The problem is that Claude *can* write good code fast, and the speed tempts us to skip thinking. Superpowers isn't about limitations — it's about structure. It forces the thinking to happen upfront where it's cheap to fix, not in production where it's expensive."

## Integration with Woodworks-OS

**Status:** ✅ Installed and active

**Location:** `.claude/skills/superpowers/SKILL.md`

**How to use:**
```
/using-superpowers Build an automated email campaign system for realtors
```

The skill will guide you through the plan → test → code → review → deliver workflow automatically.

## Red Flags (When You're Rationalizing Away Discipline)

These thoughts mean STOP — you're about to skip steps:

| Thought | Reality |
|---------|---------|
| "This is just a quick task" | Quick is when bugs hide best |
| "I can skip tests for this" | Tests catch the edge cases you forgot |
| "I'll refactor later" | Later never comes, debt compounds |
| "This doesn't need documentation" | Documentation is for future-you |
| "I already know this pattern" | Knowing ≠ implementing correctly |

## Team Impact

When used at team scale:
- Code reviews go faster (tests already proven the logic)
- Merge conflicts fewer (better architecture reduces overlaps)
- Production incidents drop 40%+ (edge cases caught early)
- Onboarding faster (tests serve as documentation)

## References

- **Official Repo:** https://github.com/obra/superpowers
- **Framework:** Agentic skills framework + software development methodology
- **Community:** 150K+ GitHub stars, 19.8K forks
- **License:** MIT

## Next Steps

Use superpowers for all Woodworks-OS production builds:
- ✅ Email campaign system (done)
- Upcoming: Prospect tracking automation
- Upcoming: Carousel + email integration workflow
- Upcoming: CRM synchronization system
