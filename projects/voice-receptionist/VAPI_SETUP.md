# Vapi Integration Setup

Use Vapi for voice instead of Twilio. Simpler, faster, better.

---

## What is Vapi?

Vapi handles:
- ✅ Phone calls (inbound + outbound)
- ✅ Voice transcription (automatic)
- ✅ Voice synthesis (automatic)
- ✅ Call routing and IVR
- ✅ Recording + storage

You provide:
- ✅ Claude API (your LLM)
- ✅ Business logic (our receptionist)

---

## Step 1: Create Vapi Account

1. Go to https://vapi.ai
2. Sign up (free tier available)
3. Get your API key from dashboard
4. Save it

---

## Step 2: Buy a Phone Number (Optional)

Vapi can:
- **Buy a number** — $1-2/month through Vapi (~$0.015/min calls)
- **Use your number** — Port existing number
- **Use web widget** — No phone number needed (test mode)

For testing, use **web widget** (free, no phone number needed).

---

## Step 3: Create an Assistant

In Vapi dashboard → **Assistants** → **Create New**

Configuration:
```
Name: Real Estate Receptionist
Model: Claude 3.5 Sonnet
Provider: Anthropic
API Key: sk-ant-xxxx

System Prompt:
"You are an AI receptionist for a real estate agency.
- Schedule property showings
- Qualify leads (budget, timeline, location)
- Take messages for agents
- Answer property questions

Be professional, friendly, and helpful."

Voice: (choose one)
- Accent: American
- Speed: 1.0x
- Warmth: 8/10
```

Click **Save**.

---

## Step 4: Generate Phone Number

In Vapi dashboard → **Assistants** → Your Assistant → **Phone Numbers**

Option A: **Buy a new number**
- Cost: $1-2/month
- Setup: 1 minute
- You get: +1-XXX-XXX-XXXX

Option B: **Web widget** (free, for testing)
- Cost: $0
- Setup: 1 minute
- You get: embeddable chat + voice widget

Choose **Web Widget** for testing, **Buy Number** for production.

---

## Step 5: Configure Claude Backend

In your Vapi assistant settings:

```
LLM Provider: Anthropic
Model: claude-3-5-sonnet-20241022
API Key: sk-ant-xxxxxxxxxxxx

System Prompt:
You are a real estate receptionist. Handle three types of calls:

1. SCHEDULE APPOINTMENT
   - Listen for property address and preferred time
   - Confirm availability
   - Say "I've scheduled your showing for [time]"

2. QUALIFY LEAD
   - Ask: "Are you buying or selling?"
   - If selling: "How many beds/baths? Timeline? Budget?"
   - Score as HOT/WARM/COLD based on timeline
   - Say "An agent will contact you within 24 hours"

3. TAKE MESSAGE
   - Get caller's name and number
   - Get message for agent
   - Say "I've passed your message to [agent]"

Be conversational. Sound like a real receptionist.
```

Click **Save**.

---

## Step 6: Test with Web Widget

In Vapi dashboard → Your Assistant → **Embed**

Copy the embed code:
```html
<script src="https://cdn.vapi.ai/web.js"></script>
<script>
  Vapi.setWebCallButton({
    assistantId: "your-assistant-id-here",
    buttonPosition: "bottom-right",
    buttonColor: "#00d4aa"
  });
</script>
```

Or just click **Test** in the dashboard to chat/call right now.

---

## Step 7: Connect to Your Database (Optional)

Vapi → Webhooks → Add webhook URL

On call end, Vapi sends:
```json
{
  "call_id": "...",
  "transcript": "...",
  "duration": 120,
  "assistant_id": "...",
  "status": "completed"
}
```

Your Flask server can receive this at `/webhook/vapi`:
```python
@app.route('/webhook/vapi', methods=['POST'])
def vapi_webhook():
    data = request.get_json()
    call_id = data['call_id']
    transcript = data['transcript']
    
    # Save to database
    db.create_call({
        'call_id': call_id,
        'transcript': transcript,
        'duration': data['duration']
    })
    
    return {'success': True}
```

---

## Step 8: Go Live

Option A: **Web Widget** (instant)
```
Embed code on website
- Customers click button
- Voice call starts
- No phone number needed
```

Option B: **Phone Number** ($1-2/month)
```
Buy number in Vapi
- Share +1-312-555-1234 with agents
- People call
- Receptionist answers
```

---

## Pricing

**Vapi:**
- Free tier: unlimited usage, limited calls
- Paid tier: $0.05-0.15/min (varies by number type)
- Phone number: $1-2/month

**Claude API:**
- Sonnet: ~$3 per 1M input tokens
- Per call cost: ~$0.03-0.10

**Total per call:**
- ~5 min call = $0.25-0.75 (Vapi) + $0.05 (Claude) = **~$0.30-0.80/call**

---

## Benefits Over Twilio

| Feature | Vapi | Twilio |
|---------|------|--------|
| Setup time | 5 min | 30 min |
| Voice handling | Built-in | Manual |
| Transcription | Auto | Manual |
| TTS | Auto | Manual |
| Cost | Lower | Higher |
| Ease | Easy | Complex |

Vapi = Twilio + Whisper + ElevenLabs all in one.

---

## Next Steps

1. ✅ Create Vapi account
2. ✅ Create assistant with Claude
3. ✅ Test with web widget
4. ✅ (Optional) Buy phone number
5. ✅ Deploy

See dashboard for monitoring, call logs, metrics.

---

## Support

Vapi docs: https://docs.vapi.ai
Discord: https://discord.gg/vapi

Questions? Check their guides or ask in community.
