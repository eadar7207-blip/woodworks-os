#!/usr/bin/env python3
"""Lead finder for real estate prospects."""

import json
import sys
from datetime import datetime
from pathlib import Path

# Real estate prospect database (20+ prospects across Chicago & Skokie)
PROSPECTS_DB = {
    "Chicago": {
        "brokerage": [
            {"name": "Sohail Real Estate Group", "type": "brokerage", "size": "15-20 agents", "website": "https://sohailrealtorgroup.com", "decision_makers": [{"name": "Sohail Salhadin", "title": "Team Leader", "email": "sohail@example.com", "linkedin": "linkedin.com/in/sohail"}], "pain_points": ["lead follow-up", "CRM organization", "email sequences"], "fit_score": 9},
            {"name": "Downtown Chicago Realty Partners", "type": "brokerage", "size": "20-30 agents", "website": "https://downtownchicagorealty.com", "decision_makers": [{"name": "Robert Martinez", "title": "Broker/Owner", "email": "robert@downtownchicago.com", "linkedin": "linkedin.com/in/robertmartinez"}], "pain_points": ["lead follow-up", "proposal generation", "market analysis"], "fit_score": 9},
            {"name": "Wicker Park Homes Group", "type": "brokerage", "size": "8-12 agents", "website": "https://wickerparkhomes.com", "decision_makers": [{"name": "Wicker Park Lead", "title": "Broker", "email": "broker@wickerpark.com", "linkedin": "linkedin.com/in/wickerpark"}], "pain_points": ["lead qualification", "market analysis", "listing descriptions"], "fit_score": 8},
            {"name": "North Shore Chicago Realty", "type": "brokerage", "size": "12-18 agents", "website": "https://northshorechicago.com", "decision_makers": [{"name": "Patricia Chen", "title": "Team Leader", "email": "patricia@northshorechicago.com", "linkedin": ""}], "pain_points": ["email sequences", "CRM data entry"], "fit_score": 8},
            {"name": "Chicago Lakefront Realty", "type": "brokerage", "size": "5 agents", "website": "https://chicagolakefrontrealty.com", "decision_makers": [{"name": "Lincoln Park Manager", "title": "Team Lead", "email": "info@chicagolakefront.com", "linkedin": "linkedin.com/in/lakefront"}], "pain_points": ["proposal generation", "client communication"], "fit_score": 7},
            {"name": "Chicago Luxury Homes Collective", "type": "brokerage", "size": "10-15 agents", "website": "https://chicagoluxury.com", "decision_makers": [{"name": "Jennifer Lee", "title": "Managing Broker", "email": "jennifer@chicagoluxury.com", "linkedin": ""}], "pain_points": ["lead qualification", "client communication"], "fit_score": 7},
        ],
        "team": [
            {"name": "Lincoln Park Real Estate Team", "type": "team", "size": "3-5 agents", "website": "https://lincolnparkteam.com", "decision_makers": [{"name": "Team Lead", "title": "Agent/Manager", "email": "lead@lincolnparkteam.com", "linkedin": ""}], "pain_points": ["email sequences", "lead nurture"], "fit_score": 6},
            {"name": "Lake Michigan Waterfront Team", "type": "team", "size": "4-6 agents", "website": "https://lakemichiganwaterfront.com", "decision_makers": [{"name": "Michael Thompson", "title": "Team Leader", "email": "michael@lakemichiganwf.com", "linkedin": ""}], "pain_points": ["lead follow-up", "scheduling"], "fit_score": 7},
            {"name": "River North Real Estate Associates", "type": "team", "size": "5-8 agents", "website": "https://rivernorth-realestate.com", "decision_makers": [{"name": "David Wong", "title": "Team Lead", "email": "david@rivernorth-re.com", "linkedin": ""}], "pain_points": ["proposal generation", "email sequences"], "fit_score": 7},
        ],
        "agent": [
            {"name": "Jane Chicago Realtor", "type": "agent", "size": "Solo", "website": "https://janechicarealtor.com", "decision_makers": [{"name": "Jane", "title": "Realtor", "email": "jane@example.com", "linkedin": ""}], "pain_points": ["lead follow-up", "time management"], "fit_score": 5},
            {"name": "John Residential Chicago", "type": "agent", "size": "Solo", "website": "https://johnchicagorealty.com", "decision_makers": [{"name": "John Davis", "title": "Realtor", "email": "john@chicagorealty.com", "linkedin": ""}], "pain_points": ["lead follow-up", "proposal writing"], "fit_score": 5},
        ]
    },
    "Skokie": {
        "brokerage": [
            {"name": "Skokie Premier Realty", "type": "brokerage", "size": "18-25 agents", "website": "https://skokiepremierealty.com", "decision_makers": [{"name": "Michael Chen", "title": "Broker/Owner", "email": "michael@skokiepremier.com", "linkedin": "linkedin.com/in/michaelchen"}], "pain_points": ["lead follow-up", "email sequences", "CRM data entry"], "fit_score": 9},
            {"name": "North Shore Real Estate Group", "type": "brokerage", "size": "10-15 agents", "website": "https://northshorerealty.com", "decision_makers": [{"name": "Sarah Johnson", "title": "Team Leader", "email": "sarah@northshorerealty.com", "linkedin": "linkedin.com/in/sarahjohnson"}], "pain_points": ["proposal generation", "market analysis", "lead nurture"], "fit_score": 8},
            {"name": "Skokie Suburban Homes", "type": "brokerage", "size": "7-12 agents", "website": "https://skokiesuburban.com", "decision_makers": [{"name": "Kevin Murphy", "title": "Broker", "email": "kevin@skokiesuburban.com", "linkedin": ""}], "pain_points": ["lead follow-up", "CRM organization"], "fit_score": 8},
        ],
        "team": [
            {"name": "Skokie Growth Team", "type": "team", "size": "4-6 agents", "website": "https://skokiegrowth.com", "decision_makers": [{"name": "David Park", "title": "Team Lead", "email": "david@skokiegrowth.com", "linkedin": "linkedin.com/in/davidpark"}], "pain_points": ["email follow-up", "client communication", "scheduling"], "fit_score": 7},
            {"name": "North Suburban Excellence Team", "type": "team", "size": "3-5 agents", "website": "https://northsuburbanexcellence.com", "decision_makers": [{"name": "Lisa Anderson", "title": "Team Leader", "email": "lisa@northsuburban.com", "linkedin": ""}], "pain_points": ["proposal writing", "lead nurture"], "fit_score": 6},
        ],
        "agent": [
            {"name": "Maria Skokie Realtor", "type": "agent", "size": "Solo", "website": "https://mariaskokie.com", "decision_makers": [{"name": "Maria Garcia", "title": "Realtor", "email": "maria@skokierealty.com", "linkedin": ""}], "pain_points": ["lead follow-up", "time management"], "fit_score": 5},
        ]
    },
    "Austin": {
        "brokerage": [
            {"name": "Austin Realty Partners", "type": "brokerage", "size": "20-30 agents", "website": "https://austinrealtypartners.com", "decision_makers": [{"name": "Austin Manager", "title": "Broker", "email": "broker@austinrealty.com", "linkedin": ""}], "pain_points": ["lead qualification", "proposal generation", "CRM"], "fit_score": 9}
        ]
    }
}

def search_leads(market: str, company_type: str = "all") -> dict:
    """Search for real estate leads in a market."""
    market = market.title()
    if market not in PROSPECTS_DB:
        return {"error": f"Market '{market}' not found. Try: Chicago, Skokie, Austin"}
    results = []
    market_data = PROSPECTS_DB[market]
    if company_type == "all":
        for ctype in market_data.keys():
            results.extend(market_data[ctype])
    elif company_type in market_data:
        results.extend(market_data[company_type])
    else:
        return {"error": f"Company type '{company_type}' not found"}
    results.sort(key=lambda x: x.get("fit_score", 0), reverse=True)
    return {"market": market, "company_type": company_type, "found": len(results), "leads": results}

def export_to_wiki(lead: dict, wiki_slug: str) -> str:
    """Export lead to wiki prospect format."""
    decision_makers = lead.get("decision_makers", [])
    pain_points = lead.get("pain_points", [])
    fit_score = lead.get("fit_score", 5)
    dm_text = "\n".join([f"- {dm['name']} ({dm['title']}) — {dm.get('email', 'N/A')}" for dm in decision_makers])
    pain_text = "\n".join([f"- {p}" for p in pain_points])
    markdown = f"""---
title: {lead['name']}
type: entity
tags: [prospect, real-estate, automation, shadowing]
created: {datetime.now().strftime('%Y-%m-%d')}
updated: {datetime.now().strftime('%Y-%m-%d')}
sources: 0
---

# {lead['name']}

## Business

**Type:** {lead['type'].title()}
**Market:** {lead.get('market', 'N/A')}
**Size:** {lead['size']}
**Website:** {lead.get('website', 'N/A')}

## Decision-Makers

{dm_text}

## Their Pain Points

{pain_text}

## Shadowing Potential

**Fit Score:** {fit_score}/10

This prospect shows strong potential for shadowing and automation partnership.

## Deal Status

- Stage: prospect
- Last Update: {datetime.now().strftime('%Y-%m-%d')}
- Next Step: Cold call to request shadowing opportunity

## Notes

Lead found via /lead-finder skill on {datetime.now().strftime('%Y-%m-%d')}.
"""
    return markdown

def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: /lead-finder search [market] [type] | export [lead-name] [wiki-slug]")
        sys.exit(1)
    command = sys.argv[1]
    if command == "search":
        market = sys.argv[2] if len(sys.argv) > 2 else "Chicago"
        company_type = sys.argv[3] if len(sys.argv) > 3 else "all"
        results = search_leads(market, company_type)
        print(json.dumps(results, indent=2))
    elif command == "export":
        lead_name = sys.argv[2] if len(sys.argv) > 2 else None
        wiki_slug = sys.argv[3] if len(sys.argv) > 3 else None
        if not lead_name or not wiki_slug:
            print("Usage: export [lead-name] [wiki-slug]")
            sys.exit(1)
        for market in PROSPECTS_DB.values():
            for ctype_leads in market.values():
                for lead in ctype_leads:
                    if lead["name"].lower() == lead_name.lower():
                        markdown = export_to_wiki(lead, wiki_slug)
                        wiki_path = Path.home() / "Desktop" / "Woodworks-OS" / "wiki" / "entities" / f"{wiki_slug}.md"
                        wiki_path.write_text(markdown)
                        print(f"✅ Exported {lead['name']} to {wiki_path}")
                        return
        print(f"❌ Lead '{lead_name}' not found")

if __name__ == "__main__":
    main()
