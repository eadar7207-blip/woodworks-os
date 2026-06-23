# Vapi Quick Start (5 minutes)

Live voice receptionist in 5 minutes. No phone number needed for testing.

---

## 1. Sign Up

https://vapi.ai

Free tier. No credit card needed.

---

## 2. Create Assistant

**Dashboard → Assistants → Create New**

```
Name: Real Estate Receptionist
Description: AI receptionist for scheduling, lead qualification, messages

Model: Claude 3.5 Sonnet
API Key: sk-ant-xxxxxxxxxxxx

System Prompt:
You are a friendly AI receptionist for a real estate agency.
- Schedule property showings (confirm address, time, name)
- Qualify leads (ask beds, timeline, budget, score as HOT/WARM/COLD)
- Take messages (get name, number, message)
- Answer property questions
Keep responses brief and conversational.
```

Click **Create**.

---

## 3. Test with Web Widget

In your new assistant, click **Test**.

A chat window opens. Type or click the mic icon to speak.

Test scenarios:
```
"I'd like to see the 3-bedroom on Oak Street Friday afternoon"
→ Should ask to confirm time

"I'm selling my condo in 3 months for $600K"
→ Should score as HOT and ask for contact info

"Leave a message for Sohail"
→ Should take message
```

---

## 4. Get Your Phone Number (Optional)

Click **Phone Numbers → Buy New Number**

- Cost: $1-2/month
- Area code: Choose yours (312 for Chicago)
- Instant activation

You get: **+1-312-555-1234** (example)

People can now call this number.

---

## 5. Done ✅

That's it. Your receptionist is live.

**For testing:** Use web widget (free, no phone number)
**For production:** Buy phone number ($1-2/month)

---

## Next

See **VAPI_SETUP.md** for:
- Webhook integration (log calls to database)
- Advanced configuration
- Monitoring + metrics
- Scaling

---

## Cost

- Vapi: Free tier (limited) or $0.05-0.15/min
- Claude API: ~$0.03 per call
- Phone: $1-2/month

**Total: ~$0.30-0.80 per 5-min call**

Charge agents $1-3/call → 3-10x margin.
