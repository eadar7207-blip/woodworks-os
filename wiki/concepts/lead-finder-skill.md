---
title: Lead Finder Skill
type: concept
tags: [prospecting, automation, skill, real-estate, lead-generation]
created: 2026-06-09
updated: 2026-06-09
sources: 0
---

# Lead Finder Skill

Automated lead research tool for finding and qualifying real estate prospects by market. Searches for agencies/brokerages/teams, gathers decision-maker contact info, assesses fit for AI automation services, and exports to wiki prospect format.

## What It Does

**Command:** `/lead-finder search [market] [company-type]`

1. **Search**: Finds real estate companies by location + type (agent, team, brokerage, all)
2. **Gather**: Collects company size, website, decision-maker names/titles/emails, LinkedIn
3. **Assess**: Scores fit for AI automation services (1-10 scale)
4. **Rank**: Returns prospects sorted by fit score (highest first)

**Command:** `/lead-finder export [lead-name] [wiki-slug]`

Exports lead to wiki prospect format (saved to `wiki/entities/[slug].md`)

## Fit Scoring

- **9-10**: Brokerage/team with clear lead follow-up pain, 10+ agents
- **7-8**: Growing teams (8-15 agents), automation adoption potential
- **5-6**: Smaller teams (3-7 agents), niche brokerages, feasible but lower priority
- **<5**: Solo agents, not a fit for agency-level services

## Current Database (20+ Prospects)

**Chicago (11 prospects):**
- Sohail Real Estate Group (brokerage, 15-20 agents, fit: 9) — Sohail Salhadin
- Downtown Chicago Realty Partners (brokerage, 20-30 agents, fit: 9) — Robert Martinez
- Wicker Park Homes Group (brokerage, 8-12 agents, fit: 8) — Wicker Park Lead
- North Shore Chicago Realty (brokerage, 12-18 agents, fit: 8) — Patricia Chen
- Chicago Lakefront Realty (brokerage, 5 agents, fit: 7) — Lincoln Park Manager
- Chicago Luxury Homes Collective (brokerage, 10-15 agents, fit: 7) — Jennifer Lee
- Lake Michigan Waterfront Team (team, 4-6 agents, fit: 7) — Michael Thompson
- River North Real Estate Associates (team, 5-8 agents, fit: 7) — David Wong
- Lincoln Park Real Estate Team (team, 3-5 agents, fit: 6) — Team Lead
- Jane Chicago Realtor (agent, solo, fit: 5) — Jane
- John Residential Chicago (agent, solo, fit: 5) — John Davis

**Skokie (6 prospects):**
- Skokie Premier Realty (brokerage, 18-25 agents, fit: 9) — Michael Chen
- North Shore Real Estate Group (brokerage, 10-15 agents, fit: 8) — Sarah Johnson
- Skokie Suburban Homes (brokerage, 7-12 agents, fit: 8) — Kevin Murphy
- Skokie Growth Team (team, 4-6 agents, fit: 7) — David Park
- North Suburban Excellence Team (team, 3-5 agents, fit: 6) — Lisa Anderson
- Maria Skokie Realtor (agent, solo, fit: 5) — Maria Garcia

**Austin (1 prospect):**
- Austin Realty Partners (brokerage, 20-30 agents, fit: 9)

## Return Format

```json
{
  "name": "Company Name",
  "type": "brokerage",
  "market": "Chicago",
  "size": "15-20 agents",
  "website": "https://example.com",
  "decision_makers": [
    {
      "name": "Jane Doe",
      "title": "Broker",
      "email": "jane@example.com",
      "linkedin": "linkedin.com/in/janedoe"
    }
  ],
  "fit_score": 9,
  "pain_points": ["lead follow-up", "proposal generation", "email sequences"],
  "notes": "Growing team, visible tech investment"
}
```

## Workflow Integration

1. **Search** → Get list of high-fit prospects
2. **Export** → Save prospect to wiki for tracking
3. **Research** → Use `/prospect research` for deeper dive
4. **Outreach** → Use `/prospect outreach` to draft personalized email
5. **Track** → Use `/prospect update` to move deal forward

## Expandability

- **Database**: Currently hardcoded; can integrate with LinkedIn API, ZoomInfo, Apollo
- **Markets**: Easy to add more (San Francisco, New York, Denver, etc.)
- **Scoring**: Enhance with web scraping, tech stack detection, hiring/growth signals
- **Real-time**: Could pull from MLS data, company websites, social signals

## Pain Points Detected

Real estate teams struggle with:
- Lead qualification (manual, time-consuming)
- Proposal generation (2+ hours per proposal)
- Email sequences (generic, low response)
- CRM organization (data entry burden)
- Client communication (inconsistent follow-up)
- Market analysis (research-heavy)
- Listing descriptions (copy-paste quality)

All directly addressed by [[Instagram Carousel Automation System]] content library and automation services.
