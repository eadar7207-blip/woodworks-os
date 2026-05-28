# Wiki Schema

This is the schema for the wiki under this folder. It governs how I (the LLM) read, write, and maintain the wiki. Follow these rules in every session.

---

## What This Wiki Is

A persistent, compounding second brain. It covers:
- The domain the user is working in
- Business development and strategy
- Key people, contacts, and relationships
- Products, tools, and frameworks the user is building or evaluating
- Personal knowledge, learnings, and self-improvement

Everything ingested should be filtered for relevance to the user's work and goals.

---

## Folder Structure

```
wiki/
├── CLAUDE.md           # This file - the schema
├── overview.md         # High-level synthesis of what the wiki knows
├── index.md            # Content catalog - updated on every ingest
├── log.md              # Append-only operation log
├── entities/           # People, companies, products
├── concepts/           # Ideas, frameworks, strategies
├── sources/            # One summary page per raw source
└── synthesis/          # Analyses, comparisons, answered questions
```

All pages are markdown. Use `[[wiki links]]` style cross-references between pages (Obsidian-compatible).

---

## Page Frontmatter

Every wiki page gets this header:

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

---

## Page Types

### Entity pages (`wiki/entities/`)
One page per person, company, or product.
- People: name, role, relationship to the user, key facts, open questions
- Companies: what they do, relevance, key facts
- Products: what it is, how it works, the user's take on it

### Concept pages (`wiki/concepts/`)
One page per idea, framework, or strategy.
- What it is (plain language)
- Why it matters to the user specifically
- Related entities and concepts (cross-links)
- Key sources (cross-links)

### Source pages (`wiki/sources/`)
One page per raw source ingested (a meeting, a podcast episode, a file).
- Original title and author/host
- Key takeaways (bullet list)
- What wiki pages this updated
- Notable quotes or data points

### Synthesis pages (`wiki/synthesis/`)
Outputs from queries and analysis sessions.
- The question or prompt that generated it
- The answer or analysis
- Sources cited
- Date generated

### Overview (`wiki/overview.md`)
High-level synthesis of what the wiki knows. Updated periodically (not on every ingest). Covers: current picture, key open questions, what to investigate next.

---

## Operations

### Ingest a new source

When the user says "ingest [source]" or drops a file:

1. Read the source fully
2. Briefly discuss key takeaways with the user (2-5 bullets)
3. Create a source summary page in `wiki/sources/`
4. Update or create entity pages for any people, companies, or products mentioned
5. Update or create concept pages for any frameworks or ideas worth preserving
6. Update `wiki/index.md`
7. Append an entry to `wiki/log.md`

### Answer a query

When the user asks a question:

1. Read `wiki/index.md` to find relevant pages
2. Read the relevant pages
3. Synthesize an answer, cite specific pages
4. If the answer is valuable (non-trivial analysis), file it as a synthesis page
5. Append an entry to `wiki/log.md`

### Lint the wiki

When the user says "lint the wiki":

1. Scan all pages for contradictions, stale claims, orphan pages, missing cross-references
2. Flag each issue and suggest a fix
3. Suggest new questions or sources to investigate
4. Append a lint entry to `wiki/log.md`

---

## Index Format

`wiki/index.md` is organized by category. Each entry:

```
- [[Page Title]](path/to/page.md) - one-line description (updated: YYYY-MM-DD)
```

Categories: Sources | Entities - People | Entities - Companies & Products | Concepts | Synthesis

---

## Log Format

`wiki/log.md` is append-only. Each entry:

```
## [YYYY-MM-DD] operation | Title or Description
- What was done
- Pages created or updated
```

Operations: `ingest` | `query` | `lint` | `update` | `onboard`

---

## Tone and Writing Style

- Write for the user, not for a general audience
- Be direct and concrete - no corporate speak
- Bullet points over paragraphs in most cases
- Opinions and assessments are welcome, label them clearly (`Assessment:`)
- Flag contradictions explicitly: `Note: this contradicts [[Other Page]]`

---

## What I Don't Do

- I don't delete wiki pages - I update or deprecate them
- I don't write wiki content into `CLAUDE.md`
- I don't wait to be asked to update cross-references - I do it proactively
