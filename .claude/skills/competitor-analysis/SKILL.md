# Competitor Analysis Skill

This skill generates a monthly competitor analysis report for a business.

## Steps

1. Research 6-8 competitors via web search
2. Profile each competitor: description, pricing, target market, strengths, weaknesses
3. Synthesize a gap analysis and recommended actions
4. Write data as JSON to /tmp/competitor_data.json
5. Generate PDF report
6. Commit report to reports/ folder
7. Write wiki synthesis page

## JSON Schema

```json
{
  "business_name": "string",
  "industry": "string",
  "generated_date": "YYYY-MM-DD",
  "report_period": "string",
  "executive_summary": "string",
  "competitors": [
    {
      "name": "string",
      "website": "string",
      "description": "string",
      "pricing": "string",
      "target_market": "string",
      "strengths": ["string"],
      "weaknesses": ["string"],
      "notable_features": ["string"]
    }
  ],
  "gap_analysis": {
    "market_gaps": ["string"],
    "opportunities": ["string"],
    "threats": ["string"]
  },
  "recommended_actions": [
    {
      "priority": "high|medium|low",
      "action": "string",
      "rationale": "string"
    }
  ],
  "market_overview": "string"
}
```

## Usage

```bash
python3 .claude/skills/competitor-analysis/scripts/generate_logo.py --output /tmp/adar_logo.png
python3 .claude/skills/competitor-analysis/scripts/generate_pdf.py \
  --data /tmp/competitor_data.json \
  --logo /tmp/adar_logo.png \
  --primary-color '#1B3A6B' \
  --accent-color '#4A9EDB' \
  --output /tmp/adar-report.pdf
```
