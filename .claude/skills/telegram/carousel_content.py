"""Carousel content library - real prompts for each topic."""

CAROUSEL_CONTENT = {
    "lead-qualification": {
        "title": "Lead Qualification",
        "emoji": "🎯",
        "prompts": [
            "Analyze this lead's profile and tell me: (1) Are they serious or just browsing? (2) What's their likely budget? (3) Best next step?",
            "I got 50 new leads. Rank the top 10 by likelihood to close. Here's the data: [paste]",
            "Write a personalized follow-up for this lead who visited 5 properties but ignored my calls. Lead: [details]",
            "Create a qualification scoring system for my leads. Here's my data: [paste]",
            "Help me identify which leads are ready to buy vs. which need more nurturing."
        ],
        "cta": "Use this prompt to instantly qualify your leads and focus on the hot prospects."
    },
    "proposal-generation": {
        "title": "Proposal Generation",
        "emoji": "📄",
        "prompts": [
            "Create a professional proposal for a [property type] in [area]. Client: [name]. Price: [price]. Selling points: [list].",
            "Write an executive summary for this listing that emphasizes ROI for investors. Property: [details].",
            "Generate 3 proposal angles for the same property targeting: investor, family homebuyer, first-time buyer.",
            "Create a proposal template I can use for all my listings that looks premium but saves me time.",
            "Write a compelling cover letter for this offer to make my buyer stand out."
        ],
        "cta": "Generate professional proposals in 2 minutes instead of 2 hours."
    },
    "email-sequences": {
        "title": "Email Sequences",
        "emoji": "📧",
        "prompts": [
            "Write a follow-up sequence for prospects who viewed properties but didn't make offers. Context: [details]. Make it personal, not salesy.",
            "Create an educational email that positions me as a market expert. Topic: [market]. Include stats and insights.",
            "Write a win-back email for clients who went cold 6 months ago. Make them feel valued, not pressured.",
            "Design a 5-email nurture sequence for leads who aren't ready to buy yet. Include: education, lifestyle, testimonials.",
            "Help me write a post-showing follow-up that addresses buyer hesitations and moves them toward an offer."
        ],
        "cta": "Email sequences that actually get responses and move prospects forward."
    },
    "crm-organization": {
        "title": "CRM Organization",
        "emoji": "📊",
        "prompts": [
            "Analyze my CRM: How many leads are stale? Which need follow-up today? What deals are closing soon? Data: [paste]",
            "Create a follow-up schedule for my 30 active prospects. Categorize by urgency and suggest contact frequency.",
            "Write CRM note templates so I don't forget critical details: initial contact, property interest, objections, next steps.",
            "Help me clean up my CRM database. I have duplicates and old data. Strategy: [paste current state]",
            "Design a CRM workflow that ensures no lead falls through the cracks."
        ],
        "cta": "Keep your CRM clean and never miss a follow-up again."
    },
    "market-analysis": {
        "title": "Market Analysis",
        "emoji": "📈",
        "prompts": [
            "Analyze the [neighborhood] market: price trends (12mo), days on market, buyer profiles, emerging trends. Be realistic.",
            "Compare 3 neighborhoods for my clients. They want [property type]. Analyze: price/sqft, appreciation, schools, commute.",
            "Create a weekly market update I can send to my sphere. Focus: what's happening, what it means, action items.",
            "Help me understand the [market type] opportunity. I'm seeing [trend]. Is this real or just noise?",
            "Write a market report for this neighborhood that positions it as an investment opportunity."
        ],
        "cta": "Instant market insights without the 2-hour research session."
    },
    "client-communication": {
        "title": "Client Communication",
        "emoji": "💬",
        "prompts": [
            "Write an email to a buyer getting cold feet about [concern]. Reassure without being pushy.",
            "Help me communicate bad news professionally. [Situation: offer fell through / inspection found issues / appraisal came in low].",
            "Create a celebration message for a client after closing. Warm and genuine, not generic.",
            "Write a response to a seller who wants to renegotiate after inspection. Professional but firm.",
            "Help me handle this objection: '[objection]'. What's the consultative response?"
        ],
        "cta": "Say the right thing at the right time to keep deals alive."
    },
    "negotiation-scripts": {
        "title": "Negotiation Scripts",
        "emoji": "💰",
        "prompts": [
            "Help me craft a response to this lowball offer. Property value: [price]. Offer: [price]. Market: [context]. Counter strategy?",
            "Write a script for handling a seller emotional about their home. I need to be empathetic but professional.",
            "Create talking points: convince a seller to reduce price and close faster vs. holding out for higher price.",
            "Write a script for negotiating repair credits after inspection without losing the deal.",
            "Help me handle a multiple offer situation. I need to make my buyer's offer stand out."
        ],
        "cta": "Negotiate with confidence and close more deals."
    },
    "listing-descriptions": {
        "title": "Listing Descriptions",
        "emoji": "🏠",
        "prompts": [
            "Write a compelling listing description for a [property type] in [neighborhood]. Key features: [list]. Make buyers excited.",
            "Create 3 different listing titles for the same property targeting: luxury buyers, investors, families.",
            "Write a detailed walkthrough description that sells the lifestyle, not just the features. Property: [details]",
            "Create an agent's notes section that highlights what the listing photos don't show. Property: [details]",
            "Write a property description that emphasizes ROI potential for an investment property. Property: [details]"
        ],
        "cta": "Write listing descriptions that sell homes faster."
    },
    "open-house-scripts": {
        "title": "Open House Scripts",
        "emoji": "🚪",
        "prompts": [
            "Write a script for greeting buyers at an open house and qualifying them quickly. Property: [type]",
            "Create talking points for the top 3 features of this property. Property: [details]",
            "Write a follow-up email template for open house visitors. Property: [address]",
            "Help me answer these common open house questions: [list questions]. Property: [details]",
            "Create a sign-in sheet prompt that gets buyers to volunteer contact info. Property: [address]"
        ],
        "cta": "Turn open house visitors into qualified leads."
    },
    "objection-handling": {
        "title": "Objection Handling",
        "emoji": "🚫",
        "prompts": [
            "Help me respond to this buyer objection: '[objection]'. Market context: [context]. What's the best response?",
            "Create a script for handling price objections. Market data: [data]. How do I justify the price?",
            "Write responses to these seller concerns: '[concern 1]', '[concern 2]'. What do I say?",
            "Help me handle 'I want to think about it' without losing the lead. What's the right follow-up?",
            "Create a response to 'I'm working with another agent.' How do I stay competitive?"
        ],
        "cta": "Handle objections like a pro and move deals forward."
    },
    "buyer-personas": {
        "title": "Buyer Personas",
        "emoji": "👥",
        "prompts": [
            "Create a detailed buyer persona for this market. Demographics: [data]. What do they want?",
            "Analyze these buyer profiles and tell me the 3 most valuable segments. Buyer data: [paste]",
            "Write targeted messaging for first-time buyers vs. move-up buyers in my market.",
            "Create an investor buyer persona for [market type]. What properties interest them most?",
            "Design messaging that appeals to [buyer type] based on market research. Market: [details]"
        ],
        "cta": "Target the right buyers with the right message."
    },
    "social-media-content": {
        "title": "Social Media Content",
        "emoji": "📱",
        "prompts": [
            "Create 5 Instagram caption ideas for listing photos that get engagement. Property: [details]",
            "Write LinkedIn posts about real estate market trends. Topic: [trend]. Make it insightful.",
            "Generate 10 TikTok video concepts for real estate agents. Focus: [education/entertainment/trends]",
            "Create Facebook post templates for listing launches, open houses, client testimonials.",
            "Write captions for before/after home renovation photos. Property: [details]"
        ],
        "cta": "Create social content that builds your authority."
    },
    "video-scripts": {
        "title": "Video Scripts",
        "emoji": "🎬",
        "prompts": [
            "Write a 60-second property walkthrough script for this listing. Property: [details]",
            "Create a market update video script for [neighborhood]. Include: trends, opportunities, data.",
            "Write an agent introduction video script (30 seconds). Include: background, specialty, personality.",
            "Create a 'home buying tips' video script for first-time buyers. Topic: [specific tip]",
            "Write a testimonial prompt script for asking clients to record video reviews. Focus: [what to mention]"
        ],
        "cta": "Script videos that convert viewers to leads."
    },
    "team-training": {
        "title": "Team Training",
        "emoji": "👨‍🏫",
        "prompts": [
            "Create a training guide for new agents on [process]. Topic: [lead follow-up/showings/negotiations]",
            "Write a 1-page cheat sheet on the most important real estate terms. Target: [new agents/VAs]",
            "Design a role-play scenario for practicing client conversations. Situation: [objection/negotiation/bad news]",
            "Create a daily huddle agenda that takes 15 minutes and covers: [priorities/wins/blockers]",
            "Write a peer coaching script for experienced agents to teach newer team members a skill."
        ],
        "cta": "Build a high-performing team through smart training."
    },
    "lead-nurture": {
        "title": "Lead Nurture Campaigns",
        "emoji": "🌱",
        "prompts": [
            "Design a 12-week nurture email campaign for cold leads. Focus: [education/market updates/value]",
            "Create touchpoint plan for leads not ready to buy. Frequency: [weekly/biweekly]. Topics: [what to send]",
            "Write a retargeting email for leads who abandoned your lead magnet. Offer: [incentive]",
            "Design a seasonal campaign (holidays, spring market, tax season). Season: [which one]",
            "Create a 'stay in touch' email template that doesn't feel salesy. Focus: providing value."
        ],
        "cta": "Nurture leads into buyers with strategic campaigns."
    },
    "pricing-strategy": {
        "title": "Pricing Strategy",
        "emoji": "💵",
        "prompts": [
            "Analyze comparable sales for this property and recommend a listing price. Property: [details]",
            "Help a seller decide between pricing high with a longer sale vs. lower for quick close. Context: [details]",
            "Create a pricing presentation for a seller who thinks their home is worth more. Market data: [paste]",
            "Write talking points for explaining why a property is priced below/at/above market. Context: [property details]",
            "Design a pricing strategy for a [market condition] market (buyer's/seller's/balanced)."
        ],
        "cta": "Price right and close faster."
    },
    "inspection-handling": {
        "title": "Inspection Handling",
        "emoji": "🔍",
        "prompts": [
            "Help me respond to a major inspection finding. Issue: [details]. How do I handle seller/buyer concerns?",
            "Write a script for negotiating repair credits vs. credits at closing. Issue: [what needs repair]",
            "Create a buyer education email explaining inspection results. Issue: [what was found]. Severity: [minor/major]",
            "Help me advise a buyer on whether [issue] is a deal-breaker. Issue: [details]. Market: [context]",
            "Write a seller response to repair requests after inspection. Requests: [details]. Budget: [amount]"
        ],
        "cta": "Navigate inspections without losing deals."
    },
    "closing-checklist": {
        "title": "Closing Checklist",
        "emoji": "✅",
        "prompts": [
            "Create a closing checklist for a [transaction type] deal. Include: documents, deadlines, responsibilities.",
            "Write instructions for buyers on what to expect at closing. Include: documents, costs, timeline.",
            "Design a 'final walkthrough' checklist for buyers before closing. Include: what to verify, what to check.",
            "Create a closing day communication plan. Include: when to contact buyer, lender, title company.",
            "Write a post-closing follow-up email template. Include: thank you, next steps, referral ask."
        ],
        "cta": "Close deals smoothly with a solid checklist."
    },
    "referral-generation": {
        "title": "Referral Generation",
        "emoji": "🤝",
        "prompts": [
            "Write a referral request email to send 30 days after closing. Property: [address]. Make it specific.",
            "Create a referral incentive program outline. Offer: [discount/gift/commission]. How do I promote it?",
            "Design a client appreciation event invitation email. Event: [type]. Goal: generate referrals.",
            "Write a script for asking past clients for referrals during a phone call. Context: [how long ago sold]",
            "Create a referral thank-you email template. Include: appreciation, reward details, next steps."
        ],
        "cta": "Turn happy clients into your best source of leads."
    },
    "investor-outreach": {
        "title": "Investor Outreach",
        "emoji": "💼",
        "prompts": [
            "Write a property analysis pitch for an investor. Property: [details]. ROI: [estimated returns]",
            "Create a market opportunity email for investors interested in [market type]. Market: [details]",
            "Design an investor buyer profile and targeting strategy. Goal: [number of deals]. Market: [location]",
            "Write a cold outreach email to a potential investor in [market]. Opportunity: [property type/location]",
            "Create an 'off-market deal' pitch email for investors. Deal: [property details]. Opportunity: [why it's good]"
        ],
        "cta": "Build an investor network and close big deals."
    },
    "home-staging": {
        "title": "Home Staging Advice",
        "emoji": "🎨",
        "prompts": [
            "Give staging advice for a [property type] to maximize curb appeal. Property: [condition/style]",
            "Create a 10-item staging checklist for sellers who don't want to spend much. Budget: [low/medium]",
            "Write staging recommendations for a home that's not selling. Issues: [current problems/style]",
            "Design a virtual staging suggestion email for a seller hesitant about spending on staging. Property: [type]",
            "Create before/after staging talking points for listing photos. Property: [type/condition]"
        ],
        "cta": "Stage to sell with smart, budget-friendly advice."
    },
    "first-time-buyer": {
        "title": "First-Time Buyer Guide",
        "emoji": "🏡",
        "prompts": [
            "Write a 'first-time buyer' guide covering: financing, offers, inspection, closing. Format: step-by-step.",
            "Create a down payment options guide for first-time buyers. Include: conventional, FHA, VA loans.",
            "Write a buying timeline guide showing: pre-approval → offer → closing. Include: what happens when.",
            "Design a 'getting pre-approved' email series for first-time buyers. Topics: [credit, docs, process]",
            "Create a 'common first-time buyer mistakes' guide. Include: 5 things NOT to do when buying."
        ],
        "cta": "Build trust with first-time buyers through education."
    },
    "luxury-homes": {
        "title": "Luxury Home Marketing",
        "emoji": "💎",
        "prompts": [
            "Write a luxury property description that appeals to high-net-worth buyers. Property: [details]",
            "Create marketing talking points for a luxury property. Focus: [lifestyle/location/exclusivity/amenities]",
            "Design a VIP showing package for a luxury property. Include: private showing, catering, concierge.",
            "Write a 'investment opportunity' pitch for a luxury property to investors. Property: [location/details]",
            "Create luxury buyer personas and messaging that resonates with them. Market: [location]"
        ],
        "cta": "Market luxury homes to the right high-value buyers."
    },
    "relocation-services": {
        "title": "Relocation Services",
        "emoji": "✈️",
        "prompts": [
            "Create a relocation package offer for corporate clients moving to [city]. Services: [list what you offer]",
            "Write a 'welcome to [city]' guide for relocating families. Include: neighborhoods, schools, amenities.",
            "Design an employer partnership pitch for relocation services. Company: [type]. Opportunity: [benefit]",
            "Create a relocation client onboarding sequence. Topics: [market overview, neighborhood tours, timing]",
            "Write a 'area guide' email series for relocating clients. Topics: [neighborhoods/schools/lifestyle]"
        ],
        "cta": "Build a relocation business and dominate market arrivals."
    }
}
