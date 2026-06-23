# Tech Stack & Platform Selection

## Voice/Phone Platform

### Decision: Twilio (with ElevenLabs for TTS)

**Why Twilio:**
- Industry standard for voice automation
- Excellent real estate integrations (many CRM plugins)
- Programmable voice, messaging, video all in one
- Good documentation and SDKs
- Mature error handling and reliability

**Why NOT:**
- Vonage: Less flexible, higher complexity
- Bandwidth: Smaller ecosystem
- Custom SIP: Too much infrastructure overhead

**Twilio Pricing:**
- Inbound call: $0.015/minute
- Typical 3-5 min call: $0.045-$0.075
- 100 calls/month: ~$5-7
- 1000 calls/month: ~$50-75
- Monthly rental (local number): $1

**Setup:**
```bash
pip install twilio
# Set env vars:
# TWILIO_ACCOUNT_SID
# TWILIO_AUTH_TOKEN
# TWILIO_PHONE_NUMBER
```

## Transcription

### Decision: OpenAI Whisper API (with fallback to local Whisper)

**Why Whisper API:**
- Best accuracy for real estate jargon (addresses, agent names, property terms)
- Fast (1-2 seconds for 30-second audio)
- Cost-effective ($0.02 per 15 minutes of audio)
- Same provider as Claude, easier integration

**API Pricing:**
- $0.02 per 15 minutes of audio
- 100 calls × 4 min avg = 400 min = ~$0.53
- 1000 calls × 4 min = 4000 min = ~$5.30

**Setup:**
```bash
pip install openai
from openai import OpenAI
client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
```

## Language Model

### Decision: Claude 3.5 Sonnet (via Anthropic API)

**Why Claude:**
- Specifically trained to understand real estate context
- Better at instruction-following (important for complex multi-turn flows)
- Cost-effective ($3/MTok input, $15/MTok output)
- Already integrated with Eitan's framework
- Better at zero-shot reasoning than GPT-4 for business logic

**Pricing:**
- Input tokens: ~$0.003 per 1K tokens
- Output tokens: ~$0.015 per 1K tokens
- Per call estimate: ~500 input tokens + 200 output = $0.002 per call
- 1000 calls/month: ~$2

**Setup:**
```bash
pip install anthropic
from anthropic import Anthropic
client = Anthropic(api_key=os.environ['ANTHROPIC_API_KEY'])
```

## Text-to-Speech

### Decision: ElevenLabs (best voice quality for customer-facing)

**Why ElevenLabs:**
- Natural-sounding voices (essential for receptionist experience)
- Fast synthesis (2-3 seconds for 50 words)
- Multi-language support
- Has real estate agent voices available

**Alternatives Considered:**
- Google Cloud TTS: Good but slower, more expensive ($4/1M chars)
- AWS Polly: Cheaper but lower quality
- Local TTS (Piper): Free but lower quality, more latency
- Deepgram: Good but newer, less stable

**ElevenLabs Pricing:**
- Free tier: 10k characters/month (good for MVP)
- Paid: $5/month = 50k chars/month
- Production: $99/month = 1M chars/month
- Cost per call (1 minute response): ~0.3 cents

**Setup:**
```bash
pip install elevenlabs
from elevenlabs.client import ElevenLabs
client = ElevenLabs(api_key=os.environ['ELEVENLABS_API_KEY'])
```

## Backend Framework

### Decision: Flask (keep it simple, match existing setup)

**Why Flask:**
- Matches Eitan's existing automation executor (already using Flask at localhost:5000)
- Lightweight, easy to extend
- Good async support with Celery if needed
- Integrates well with Twilio webhooks

**Setup:**
```bash
pip install flask flask-cors python-dotenv
```

## Database

### Decision: SQLite (with migration to PostgreSQL for production)

**Why SQLite:**
- Zero infrastructure
- Perfect for MVP/demo
- Can migrate to PostgreSQL with one migration file

**Schema:** See ARCHITECTURE.md for full schema

## Real Estate Data

### Decision: Embedded JSON + API integration

For MVP:
- Hardcoded property listings (10-20 sample properties)
- Stored as JSON in `data/properties.json`

For production:
- Integration with MLS API (RETS protocol)
- Zillow API (property details)
- Agent's existing CRM (property inventory)

## API Integration Layer

Calls to existing Eitan framework:
- **Skill Bridge:** http://localhost:9000 (for skill invocation)
- **Automation Executor:** http://localhost:5000 (for workflow triggers)

Authentication:
```python
SKILL_BRIDGE_URL = "http://localhost:9000"
EXECUTOR_URL = "http://localhost:5000"
API_KEY = os.environ['AUTOMATION_API_KEY']  # shared key
```

## Development Stack

- **Language:** Python 3.9+
- **Package Manager:** pip + requirements.txt
- **Testing:** pytest + pytest-asyncio
- **Linting:** black, flake8
- **Logging:** Python logging + ELK for production
- **IDE:** VS Code (Flask extension)

## Full Requirements

```
twilio==9.0.0
openai==1.3.0
anthropic==0.7.0
elevenlabs==0.2.0
flask==3.0.0
flask-cors==4.0.0
python-dotenv==1.0.0
pytest==7.4.0
pytest-asyncio==0.21.0
black==23.9.0
flake8==6.1.0
```

## Cost Breakdown (Monthly, 1000 calls)

| Service | Calls | Rate | Cost |
|---------|-------|------|------|
| Twilio | 1000 | $0.015/min (4min avg) | $60 |
| Whisper | 1000 | $0.02/15min | $5 |
| Claude 3.5 | 1000 | $0.002/call avg | $2 |
| ElevenLabs | 1000 | $0.003/call avg | $3 |
| Server | 1 | flat | $50 (if cloud) |
| **Total** | | | **~$120** |

**Per-Agent Pricing Model:**
- Fixed: $50/month (base automation + hosting)
- Variable: $0.120 per call (all services)
- Break-even: ~420 calls/month
- Recommended margin: 3-5x cost = $0.36-$0.60/call → $3-5/month per agent

## Deployment Options

### MVP (Dev/Demo)
- Local Flask server
- Twilio free trial (10 minutes of calls)
- Simulated voice input (text)
- Localhost databases

### Production (Lite)
- VPS (DigitalOcean $5-10/month)
- Twilio production account
- CloudFlare for HTTPS
- PostgreSQL on same VPS

### Production (Scale)
- AWS EC2 + RDS
- Twilio webhooks
- S3 for call recordings
- CloudWatch for monitoring
- Auto-scaling based on call volume

## Environment Variables

```bash
# Twilio
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
TWILIO_PHONE_NUMBER=+1234567890

# LLM
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# TTS
ELEVENLABS_API_KEY=your_key

# Framework Integration
AUTOMATION_API_KEY=your_key
SKILL_BRIDGE_URL=http://localhost:9000
EXECUTOR_URL=http://localhost:5000

# Database
DATABASE_URL=sqlite:///receptionist.db

# Logging
LOG_LEVEL=INFO
```

## Deployment Checklist

- [ ] All API keys set in environment
- [ ] Database migrations run
- [ ] Twilio number configured with webhook URL
- [ ] TLS certificate for HTTPS (Twilio requires it)
- [ ] Test call from real phone
- [ ] Verify skill calls to localhost:9000 work
- [ ] Monitor logs for errors
- [ ] Set up alerting (failed calls, API errors)
