# Quick Start Guide

Get voice receptionist running in 5 minutes.

---

## 1. Clone & Setup (1 min)

```bash
cd projects/voice-receptionist
cp .env.example .env.local
# Edit .env.local with your API keys
```

**Minimal keys needed:**
- `ANTHROPIC_API_KEY` — Get from https://console.anthropic.com
- `OPENAI_API_KEY` — Get from https://platform.openai.com
- `ELEVENLABS_API_KEY` — Get from https://elevenlabs.io

---

## 2. Install Dependencies (1 min)

```bash
pip3 install -r requirements.txt
```

---

## 3. Initialize Database (30 seconds)

```bash
python3 -c "from voice_receptionist.database import Database; Database()"
echo "✅ Database ready"
```

---

## 4. Run Demo (2 min)

See the receptionist in action with 3 scenarios:

```bash
python3 demo.py
```

Output shows:
- ✅ Appointment scheduling
- ✅ Lead qualification  
- ✅ Message taking

---

## 5. Start Server (1 min)

```bash
python3 app.py
```

Server running at: `http://localhost:5001`

**Health check:**
```bash
curl http://localhost:5001/health
```

---

## Next: Skill Bridge Integration

Make sure Eitan's automation framework is running:

```bash
# Check Skill Bridge
curl http://localhost:9000/health
```

If OK, receptionist will:
- ✅ Book appointments via Calendar skill
- ✅ Create leads in CRM skill
- ✅ Send confirmations via Send skill

---

## Troubleshooting

**"ModuleNotFoundError: No module named 'anthropic'"**
```bash
pip3 install -r requirements.txt
```

**"Skill Bridge connection refused"**
- Make sure automation executor running at localhost:9000
- Check: `curl http://localhost:9000/health`

**"Database locked"**
```bash
rm voice_receptionist.db
python3 -c "from voice_receptionist.database import Database; Database()"
```

---

## What Next?

1. **Test with real API keys** — Replace placeholders in `.env.local`
2. **Integrate with Skill Bridge** — See `INTEGRATION.md`
3. **Deploy to production** — See `DEPLOYMENT.md`
4. **Connect Twilio** — See `README.md` for phone setup

---

## File Overview

```
voice-receptionist/
├── app.py                      # Flask server
├── demo.py                     # 3-scenario demo
├── requirements.txt            # Dependencies
├── README.md                   # Full documentation
├── ARCHITECTURE.md             # System design
├── INTEGRATION.md              # Skill Bridge API
├── DEPLOYMENT.md               # Production setup
├── INTEGRATION_CHECKLIST.md    # Pre-launch checklist
└── voice_receptionist/
    ├── claude_engine.py        # Claude decision logic
    ├── conversation.py         # Call state management
    ├── skill_client.py         # Skill Bridge HTTP client
    ├── database.py             # SQLite persistence
    └── tts.py                  # Text-to-speech
```

---

## Questions?

- Architecture: see `ARCHITECTURE.md`
- Integration: see `INTEGRATION.md`
- Deployment: see `DEPLOYMENT.md`
- Examples: see `tests/` folder
