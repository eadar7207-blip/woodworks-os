# Twilio Quick Start (5 minutes)

Get your voice receptionist answering real phone calls.

---

## 1. Sign Up for Twilio

https://www.twilio.com/console

You get **$15 free credits** to test.

---

## 2. Get Your Credentials

In Twilio Console:
```
Account Info (top right)
- Account SID: ACxxxxxxxxxxxx
- Auth Token: your-token-here
```

Save these.

---

## 3. Buy a Phone Number

In Twilio Console:
```
Phone Numbers → Buy a Number
- Country: United States
- Area Code: 312 (Chicago) or your area
- Buy (costs ~$1-2/month)

Your number: +1-312-555-1234
```

Save this.

---

## 4. Update .env

Create `.env.local`:

```bash
# Twilio
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your-token-here
TWILIO_PHONE_NUMBER=+1-312-555-1234

# Claude & APIs
ANTHROPIC_API_KEY=sk-ant-xxxx
OPENAI_API_KEY=sk-xxxx
ELEVENLABS_API_KEY=xxxx

# Server
PORT=5001
DEBUG=False
```

---

## 5. Deploy Server

You need a public URL. Choose one:

### Option A: Heroku (Easiest)

```bash
# Install Heroku
brew install heroku

# Deploy
heroku create your-unique-name
git push heroku main

# Get your URL
heroku apps:info
# Dyno name: https://your-unique-name.herokuapp.com

# Set env vars
heroku config:set TWILIO_ACCOUNT_SID=ACxxxx
heroku config:set TWILIO_AUTH_TOKEN=xxxx
heroku config:set ANTHROPIC_API_KEY=sk-ant-xxxx
# ... set others
```

### Option B: Your Own Server

```bash
# On your server:
python3 app.py

# Get public URL (use ngrok for testing)
ngrok http 5001
# Gives you: https://abc123.ngrok.io
```

---

## 6. Configure Twilio Webhook

In Twilio Console:
```
Phone Numbers → Manage Numbers → Your Number

Under Voice section:
"A Call Comes In" 
→ Set to: https://your-url.com/call/incoming
→ Method: POST

Save
```

---

## 7. Test

Call your Twilio number from any phone:

```
+1-312-555-1234 (your number)
```

You should hear: "Hi! Thanks for calling. How can I help you today?"

Speak naturally. Receptionist responds.

---

## Done ✅

Your voice receptionist is live.

See **TWILIO_SETUP.md** for detailed docs.
