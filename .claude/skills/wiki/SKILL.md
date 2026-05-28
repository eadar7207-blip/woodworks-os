---
name: wiki
description: Use when the user says /wiki, wants to update the wiki, log a new insight, ingest a source, or sync the wiki after a working session
---

# Wiki

## Wiki Location

`wiki/` relative to the repo root.

Always read `wiki/index.md` and `wiki/log.md` (last 5 entries) before doing anything.

---

## Operations

### `/wiki` with no arguments - ask what to do

"What would you like to do with the wiki? Options: ingest a source, update from this session, ask a question, or lint."

### `/wiki update` - sync wiki from current session

After any working session where something meaningful happened, run this to push updates in.

1. Identify what changed: new decisions, new contact info, new product direction, project status changes
2. Update relevant entity / concept / synthesis pages
3. Update `wiki/overview.md` if priorities or key questions changed
4. Update `wiki/index.md` if new pages were created
5. Append to `wiki/log.md`

### `/wiki ingest [source]` - process a new source

When the user drops a file, pastes content, or points to a URL:

1. Read the source fully
2. Summarize key takeaways (2-5 bullets) - confirm with the user before filing
3. Create a source summary page in `wiki/sources/` with frontmatter
4. Update or create entity pages for people / companies / products mentioned
5. Update or create concept pages for ideas / frameworks worth preserving
6. Update `wiki/index.md` and append to `wiki/log.md`

### `/wiki [question]` - query the wiki

When the user asks a question:

1. Read `wiki/index.md` to find relevant pages
2. Read relevant pages
3. Synthesize the answer with citations to specific pages
4. If the answer is non-trivial analysis, file it as a synthesis page in `wiki/synthesis/`
5. Append to `wiki/log.md`

### `/wiki lint` - health check

1. Scan all pages for contradictions, stale claims, orphan pages, missing cross-references
2. Flag each issue with a suggested fix
3. Suggest new sources or questions to investigate
4. Append a lint entry to `wiki/log.md`

---

## Page Frontmatter (required on all wiki pages)

```yaml
---
title: Page Title
type: entity | concept | source | synthesis | overview
tags: [tag1, tag2]
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: 0
---
```

## Log Entry Format (append-only)

```
## [YYYY-MM-DD] operation | Title or Description
- What was done
- Pages created or updated
```

## Cross-Reference Style

Use Obsidian wiki links: `[[Page Title]]`

---

## What Goes Where

- `wiki/entities/` - people, companies, products
- `wiki/concepts/` - ideas, frameworks, strategies, product concepts
- `wiki/sources/` - one page per ingested source
- `wiki/synthesis/` - answered questions, analyses, strategic summaries
- `wiki/overview.md` - big picture, updated periodically
- `wiki/index.md` - catalog, updated on every change
- `wiki/log.md` - append-only operation log
