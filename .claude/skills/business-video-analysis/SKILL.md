---
name: business-video-analysis
description: Use when you share a YouTube video link to analyze how it's relevant to Adar Realty Studio. Extracts key insights, identifies business applications, and connects to your automation agency goals.
argument-hint: [youtube-url or "analyze [url]"]
---

## Business Video Analysis

Post a YouTube video link and get business-relevant analysis tailored to your AI automation agency (Adar Realty Studio).

## Usage

Simply post a YouTube link:
```
/business-video-analysis https://youtube.com/watch?v=...
```

Or explicit format:
```
/business-video-analysis analyze https://youtube.com/watch?v=...
```

## What It Does

1. **Extracts content** — Gets video transcript or speech-to-text
2. **Identifies insights** — Pulls key takeaways and frameworks
3. **Maps to your business** — Connects to real estate automation + agency building
4. **Generates report** — Shows relevance, applications, and action items

## Output

You get a structured analysis:

```
## Video: [Title]
**Duration:** [length]
**Channel:** [creator]

## Key Insights
- [insight 1]
- [insight 2]
- [insight 3]

## Relevance to Adar Realty Studio
- Real estate angle: [how this applies to RE]
- Automation angle: [how this applies to AI/automation]
- Agency building: [how this supports your business model]

## Applicable Frameworks
- [Relevant framework from your wiki]
- [Relevant concept]

## Immediate Applications
1. [Action item 1]
2. [Action item 2]
3. [Action item 3]

## Who to Share This With
- Prospects: [Why this matters to prospects]
- Team: [Why this matters to team]
- Research: [What to investigate further]
```

## Examples

**Real estate specific video:**
```
/business-video-analysis https://youtube.com/watch?v=REalestate
↓
Video: "5 Ways to Automate Lead Follow-Up"
Relevance: 80% (direct to your pain points)
Applications: Email campaign system, CRM sync, lead nurture automation
```

**Agency building video:**
```
/business-video-analysis https://youtube.com/watch?v=agencybuilding
↓
Video: "Scaling Your Service Business"
Relevance: 70% (applicable to your growth phase)
Applications: Pricing model, client delivery, operations
```

**AI/automation video:**
```
/business-video-analysis https://youtube.com/watch?v=AItrends
↓
Video: "Latest AI Trends 2026"
Relevance: 65% (general knowledge + specific applications)
Applications: Agent frameworks, prompt engineering, system design
```

## Context Used

The analysis draws from your wiki:
- **Business model:** AI automation agency (real estate niche)
- **Current systems:** Email campaigns, carousel automation, lead finder, prospect tracking
- **Target pain points:** Lead follow-up, proposals, CRM, email sequences
- **Strategic goals:** Build automation + become real estate agent + $11-18K/month revenue

## When to Use

- **Learning:** "How does this relate to what we're building?"
- **Research:** "Is this worth deeper investigation?"
- **Inspiration:** "Can we apply this pattern to our work?"
- **Validation:** "Does this confirm our approach?"
- **Competitive intel:** "What are competitors doing?"

## Output Destinations

Results are:
- **Shown immediately** in the chat
- **Optionally saved** to `wiki/sources/video-analysis-[date].md` if you want to keep it
- **Cross-referenced** to relevant wiki concepts

## Notes

- Works with any YouTube video (long-form content)
- Transcript-based when available, Whisper-based otherwise
- Analysis is filtered for YOUR business context (not generic)
- Identifies both direct applications and inspiration sources
- Flags red flags or things to watch out for

## Real Examples from Your Work

**If you analyzed Bryan Casella carousel video:**
→ "Design patterns: 60/40 whitespace rule, typography hierarchy, neon colors"
→ "Application: Applied to carousel system"

**If you analyzed competitor automation tool demo:**
→ "Positioning gap: They focus on enterprise, you focus on solo/team agents"
→ "Application: Underserved market = competitive advantage"

**If you analyzed AI reasoning frameworks:**
→ "Agent contract patterns: responsibility definitions, error handling"
→ "Application: Could improve lead-finder and prospect research agents"
