# Lead Finder

Research real estate prospects by market. Find contact info, decision-makers, and assess fit for AI automation services.

## Operations

### `/lead-finder search [market] [company-type]`
Search for real estate prospects in a location.

**Parameters:**
- `market`: City/region (e.g., "Chicago", "Austin", "San Francisco")
- `company-type`: "agent" | "brokerage" | "team" | "all"

**Returns:** Structured lead data with name, size, decision-makers, contact, fit score

Example: `/lead-finder search Chicago brokerage`

### `/lead-finder export [lead-name] [wiki-page]`
Export a lead to prospect wiki format for tracking.

Example: `/lead-finder export "Sohail Real Estate Group" sohail-real-estate-group`

## What It Does

1. **Search**: Finds real estate companies by market + type
2. **Gather**: Collects contact info, decision-maker names/titles
3. **Assess**: Scores fit for AI automation (1-10)
4. **Export**: Formats for wiki/prospect tracking

## Scoring

Fit Score (1-10):
- 9-10: Team/brokerage with visible lead follow-up pain, 10+ agents
- 7-8: Smaller teams, adoption potential
- 5-6: Solo agents, niche brokerages
- <5: Not a fit for agency services

## Output Format

```json
{
  "name": "Company Name",
  "type": "brokerage",
  "market": "Chicago",
  "size": "25 agents",
  "website": "https://example.com",
  "decision_makers": [
    {
      "name": "Jane Doe",
      "title": "Broker",
      "email": "jane@example.com",
      "linkedin": "linkedin.com/in/janedoe"
    }
  ],
  "fit_score": 8,
  "pain_points": ["lead follow-up", "proposal generation", "email sequences"],
  "notes": "Growing team, visible tech investment"
}
```
