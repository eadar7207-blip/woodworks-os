# Twilio Integration Setup

Get real phone calls working with your voice receptionist in 15 minutes.

---

## Step 1: Create Twilio Account

1. Go to https://www.twilio.com/console
2. Sign up (free account)
3. Get your credentials:
   - **Account SID** (starts with `AC`)
   - **Auth Token** (long string)
4. Save these for later

---

## Step 2: Buy a Phone Number

1. In Twilio Console → **Phone Numbers** → **Buy a Number**
2. Choose country (US)
3. Search for area code (e.g., 312 for Chicago)
4. Buy a number (~$1-2/month)
5. Save your number (e.g., `+1-312-555-1234`)

---

## Step 3: Deploy Your Server

You need a publicly accessible server (not localhost).

### Option A: Heroku (Free, Easiest)

```bash
# Install Heroku CLI
brew install heroku

# Login
heroku login

# Create app
heroku create your-app-name

# Set environment variables
heroku config:set TWILIO_ACCOUNT_SID=ACxxxx
heroku config:set TWILIO_AUTH_TOKEN=xxxx
heroku config:set TWILIO_PHONE_NUMBER=+1-312-555-1234
heroku config:set ANTHROPIC_API_KEY=sk-ant-xxxx
heroku config:set OPENAI_API_KEY=sk-xxxx
heroku config:set ELEVENLABS_API_KEY=xxxx

# Deploy
git push heroku main
```

Your app runs at: `https://your-app-name.herokuapp.com`

### Option B: DigitalOcean ($5/month)

```bash
# Create droplet, SSH in, then:
git clone your-repo
cd voice-receptionist
python3 app.py
```

Access at: `https://your-server-ip:5001`

### Option C: AWS/Google Cloud

Follow their deployment docs, set environment variables, deploy.

---

## Step 4: Configure Twilio Webhook

1. In Twilio Console → **Phone Numbers** → **Manage Numbers** → Your Number
2. Scroll to **Voice**
3. Set **"A Call Comes In"** webhook to:
   ```
   https://your-app-name.herokuapp.com/call/incoming
   ```
4. Method: **POST**
5. Save

---

## Step 5: Update Environment Variables

Create `.env.prod` on your server:

```bash
# Twilio
TWILIO_ACCOUNT_SID=ACxxxx
TWILIO_AUTH_TOKEN=xxxx
TWILIO_PHONE_NUMBER=+1-312-555-1234

# LLM & APIs
ANTHROPIC_API_KEY=sk-ant-xxxx
OPENAI_API_KEY=sk-xxxx
ELEVENLABS_API_KEY=xxxx

# Server
PORT=5001
ENVIRONMENT=production
```

Then load it:
```bash
source .env.prod
python3 app.py
```

---

## Step 6: Test

1. Call your Twilio phone number from any phone
2. Wait for it to ring (5-10 seconds)
3. Receptionist answers: "Hi! Thanks for calling. How can I help you today?"
4. Speak naturally
5. Receptionist responds with voice

---

## How It Works

```
Person calls → Twilio receives → sends webhook to your server
                                      ↓
                            Flask receives call
                                      ↓
                            Transcribe audio (Whisper)
                                      ↓
                            Claude analyzes (intent, response)
                                      ↓
                            Synthesize voice (ElevenLabs)
                                      ↓
                            Play response to caller
                                      ↓
                            Save to database
```

---

## Pricing

**Twilio:**
- Incoming calls: $0.0075/min (~$0.45/hour)
- Outgoing calls: $0.013/min (~$0.78/hour)
- SMS: $0.0075 per message
- Free tier: $15 in credits (test only)

**OpenAI Whisper:**
- $0.02 per audio minute

**ElevenLabs TTS:**
- $0.30 per 1M characters (~$0.003 per 100-word response)

**Total per call:**
- ~5 min call = $0.05 (Twilio) + $0.10 (Whisper) + $0.015 (TTS) = **~$0.17/call**
- Suggest charging: $0.50-1.00/call (3-6x margin)

---

## Troubleshooting

**Problem: Webhook not working**
- Check Twilio logs: Console → Monitor → Logs
- Verify URL is accessible: `curl https://your-domain/call/incoming`
- Check firewall/port forwarding

**Problem: Audio not transcribing**
- Verify `OPENAI_API_KEY` is set
- Check Whisper API is responsive
- Look at app logs for errors

**Problem: Voice response not playing**
- Verify `ELEVENLABS_API_KEY` is set
- Check ElevenLabs account has credits
- Test TTS in isolation

**Problem: Slow responses**
- Claude API calls take 2-3 seconds
- Whisper transcription: 1-2 seconds
- TTS synthesis: 1-3 seconds
- Total: 4-8 seconds per exchange (normal)

---

## Next Steps

1. ✅ Set up Twilio account
2. ✅ Buy phone number
3. ✅ Deploy server
4. ✅ Configure webhook
5. ✅ Test with a real call
6. ⏳ Monitor metrics (call volume, lead quality, costs)
7. ⏳ Tune Claude prompts for your agents
8. ⏳ Set up call recordings (optional)

---

## Support

See `README.md` for API docs, `DEPLOYMENT.md` for production checklist.

Questions? Check Twilio docs: https://www.twilio.com/docs/voice
