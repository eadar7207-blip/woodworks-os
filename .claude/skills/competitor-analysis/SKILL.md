---
name: competitor-analysis
description: Run a full competitor research workflow for any business and output a branded PDF report. Use when the user wants to analyze their competitive landscape, track what competitors are doing, find market gaps, or get a strategic overview of their industry. Accepts brand inputs (logo, colors) each run so it works for any client.
---

# Competitor Analysis Skill

## What This Does

Researches competitors for a given business using web search, synthesizes findings, and generates a branded PDF report with:
- Cover page (logo + brand colors)
- Executive summary
- Competitor profiles (what they do, pricing, strengths, weaknesses)
- Competitive gap analysis
- Recommended actions
- Sources

## How to Run

The user will either invoke `/competitor-analysis` directly or ask you to run a competitor analysis. Collect these inputs:

**Required:**
- `business_name` — name of the business
- `description` — what the business does and who it serves
- `industry` — the market space (e.g. "AI automation agency for real estate")

**Branding (required for PDF):**
- `logo` — file path to a PNG logo (ask the user if not provided)
- `primary_color` — hex code (e.g. `#1A2B3C`)
- `accent_color` — optional second hex (defaults to a lighter shade if omitted)

**Optional:**
- `output` — where to save the PDF (default: `~/Desktop/[business-name]-competitor-report-[YYYY-MM-DD].pdf`)
- `num_competitors` — how many to profile (default: 6-8)

If inputs are missing, ask the user before proceeding.

---

## Execution Steps

### Step 1: Research — Find Competitors

Run 3-4 web searches to discover the competitive landscape. Tailor queries to the industry:

```
"[industry] companies 2026"
"best [service type] tools alternatives"
"[industry] market leaders"
"[business description] competitors"
```

From results, identify 6-8 concrete competitors with websites. Prioritize:
- Direct competitors (same service, same audience)
- Well-funded or growing players
- Companies with visible pricing or positioning

### Step 2: Profile Each Competitor

For each competitor, fetch their website and extract:
- What they offer (1-2 sentences)
- Pricing (if public — note "undisclosed" if not)
- Target market / customer type
- 2-3 clear strengths
- 2-3 weaknesses or gaps

Use `WebFetch` on their homepage + pricing page. If a site blocks fetching, note it and move on.

### Step 3: Synthesize

After profiling all competitors, produce the analysis sections:

**Executive Summary** (3-5 bullets):
- Biggest competitive threat
- Biggest opportunity
- Key market trend
- Where the business currently stands

**Gap Analysis:**
- Where your business wins vs. competitors
- Underserved needs in the market
- Emerging trends competitors aren't addressing

**Recommended Actions** (3-5 concrete steps):
- Specific, actionable — not generic advice
- Tied directly to the gap analysis findings

### Step 4: Build the JSON Data File

Assemble all research into this JSON structure and write it to a temp file (e.g. `/tmp/competitor_data.json`):

```json
{
  "business_name": "...",
  "industry": "...",
  "description": "...",
  "generated_date": "YYYY-MM-DD",
  "executive_summary": [
    "Bullet 1",
    "Bullet 2",
    "Bullet 3"
  ],
  "competitors": [
    {
      "name": "Competitor Name",
      "website": "https://...",
      "what_they_do": "One or two sentence description.",
      "pricing": "e.g. $99/mo starter, $499/mo pro — or 'Undisclosed'",
      "target_market": "Who they sell to",
      "strengths": ["Strength 1", "Strength 2", "Strength 3"],
      "weaknesses": ["Weakness 1", "Weakness 2"]
    }
  ],
  "gap_analysis": {
    "where_you_win": ["Point 1", "Point 2", "Point 3"],
    "underserved_needs": ["Need 1", "Need 2"],
    "market_trends": ["Trend 1", "Trend 2"]
  },
  "recommended_actions": [
    "Action 1",
    "Action 2",
    "Action 3",
    "Action 4"
  ],
  "sources": [
    "https://competitor1.com",
    "https://competitor2.com"
  ]
}
```

### Step 5: Generate the PDF

Call the generator script:

```bash
python3 /Users/main10servicesgmail.com/Desktop/Woodworks-OS/.claude/skills/competitor-analysis/scripts/generate_pdf.py \
  --data /tmp/competitor_data.json \
  --logo "/path/to/logo.png" \
  --primary-color "#1A2B3C" \
  --accent-color "#4A8FC4" \
  --output "/path/to/output.pdf"
```

If no logo is provided, omit `--logo` (the script handles it gracefully).
If no accent color, omit it (the script auto-derives one).

### Step 6: Save to Wiki

Write a synthesis page at `wiki/synthesis/competitor-analysis-[YYYY-MM-DD].md`:

```markdown
---
title: Competitor Analysis — [Business Name] — [Date]
type: synthesis
tags: [competitor-analysis, [industry]]
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: [number of competitors researched]
---

# Competitor Analysis: [Business Name]

## Question
What does the competitive landscape look like for [Business Name] in [industry]?

## Key Findings
- [Executive summary bullets]

## Competitors Analyzed
- [List of competitor names with one-line summary each]

## Top Opportunities
- [Gap analysis highlights]

## Recommended Actions
- [Action items]

## Output
PDF saved to: [output path]
```

Then append to `wiki/log.md`:
```
## [YYYY-MM-DD] query | Competitor Analysis — [Business Name]
- Researched [N] competitors in [industry]
- Generated branded PDF report
- PDF: [output path]
- Wiki: wiki/synthesis/competitor-analysis-[date].md
```

---

## Scheduling

To run this on a recurring schedule, use `/schedule` after the first successful run. Suggest monthly for most businesses, weekly for fast-moving markets.

---

## Notes

- If a competitor's site blocks web fetching, gather what you can from search result snippets
- Keep competitor profiles factual — flag speculation clearly
- PDF generation requires: `pip install reportlab pillow`
- The script uses Helvetica (built-in) so no font installation needed
