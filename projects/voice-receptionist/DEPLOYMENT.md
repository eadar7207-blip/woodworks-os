# Deployment Guide

Production deployment checklist and setup instructions.

---

## Pre-Deployment Checklist

- [ ] All environment variables set (see `.env.example`)
- [ ] Database migrations run (`python3 init_db.py`)
- [ ] Tests passing (`pytest tests/`)
- [ ] Skill Bridge API is healthy (`curl http://localhost:9000/health`)
- [ ] API keys obtained and verified
- [ ] HTTPS certificate obtained (Twilio requires HTTPS webhooks)
- [ ] Logging configured (CloudWatch or ELK)
- [ ] Monitoring/alerting set up

---

## Environment Setup

### Production Environment Variables

Create `/etc/voice-receptionist/.env.prod`:

```bash
# LLM APIs
ANTHROPIC_API_KEY=sk-ant-xxxx
OPENAI_API_KEY=sk-xxxx
ELEVENLABS_API_KEY=xxxx

# Twilio
TWILIO_ACCOUNT_SID=ACxxxx
TWILIO_AUTH_TOKEN=xxxx
TWILIO_PHONE_NUMBER=+1xxxxxxxxxx

# Automation Framework
SKILL_BRIDGE_URL=http://localhost:9000
EXECUTOR_URL=http://localhost:5000
AUTOMATION_API_KEY=xxxx

# Database
DATABASE_URL=postgresql://user:pass@db-server:5432/voice_receptionist

# Server
PORT=5001
DEBUG=False
LOG_LEVEL=INFO
ENVIRONMENT=production
```

---

## Database Migration (SQLite → PostgreSQL)

For production, migrate from SQLite to PostgreSQL:

```bash
# 1. Export SQLite data
sqlite3 voice_receptionist.db .dump > export.sql

# 2. Create PostgreSQL database
createdb voice_receptionist
psql voice_receptionist < schema.sql

# 3. Update DATABASE_URL in .env.prod
DATABASE_URL=postgresql://user:pass@host:5432/voice_receptionist

# 4. Modify voice_receptionist/database.py to use PostgreSQL
# (see TODO comment in code)
```

---

## Systemd Service Setup

Create `/etc/systemd/system/voice-receptionist.service`:

```ini
[Unit]
Description=AI Voice Receptionist
After=network.target

[Service]
Type=simple
User=voice-receptionist
WorkingDirectory=/opt/voice-receptionist
EnvironmentFile=/etc/voice-receptionist/.env.prod
ExecStart=/usr/bin/python3 /opt/voice-receptionist/app.py
Restart=on-failure
RestartSec=5
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl enable voice-receptionist
sudo systemctl start voice-receptionist
sudo systemctl status voice-receptionist
```

Monitor logs:

```bash
sudo journalctl -u voice-receptionist -f
```

---

## Twilio Configuration

### 1. Get Twilio Phone Number

```bash
# Log in to Twilio Console
# https://console.twilio.com/
# Phone Numbers → Buy a Number
# Choose country, area code, search for available numbers
```

### 2. Configure Webhook

Point Twilio to your Flask app:

```
Phone Number Settings → Voice & Fax
Webhook URL: https://your-domain.com/call/start
```

### 3. Test Incoming Call

```bash
# From Twilio Console
# Phone Numbers → [Your Number]
# Make a test call to verify webhook is reached
```

---

## HTTPS Configuration

### Option 1: Self-signed Certificate (Dev)

```bash
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
# Update app.py to use SSL:
# app.run(host='0.0.0.0', port=5001, ssl_context=('cert.pem', 'key.pem'))
```

### Option 2: Let's Encrypt (Production)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot certonly --standalone -d your-domain.com
# Place in: /etc/letsencrypt/live/your-domain.com/
```

### Option 3: CloudFlare Proxy (Recommended)

1. Point DNS to CloudFlare
2. Enable SSL/TLS in CloudFlare dashboard
3. No certificate needed on your server (CloudFlare handles it)

---

## Monitoring & Alerting

### Prometheus Metrics

Add to `app.py`:

```python
from prometheus_client import Counter, Histogram, generate_latest
import time

call_counter = Counter('voice_calls_total', 'Total calls', ['intent'])
call_duration = Histogram('voice_call_duration_seconds', 'Call duration')
skill_errors = Counter('skill_call_errors_total', 'Skill API errors', ['skill'])

@app.route('/metrics')
def metrics():
    return generate_latest()
```

Scrape in Prometheus:

```yaml
scrape_configs:
  - job_name: 'voice-receptionist'
    static_configs:
      - targets: ['localhost:5001']
    metrics_path: '/metrics'
```

### Alerting Rules

```yaml
# prometheus-alerts.yml
groups:
  - name: voice-receptionist
    rules:
      - alert: HighErrorRate
        expr: rate(skill_call_errors_total[5m]) > 0.05
        for: 5m
        annotations:
          summary: "High error rate in voice receptionist"

      - alert: CallProcessingLatency
        expr: histogram_quantile(0.95, call_duration) > 300
        for: 10m
        annotations:
          summary: "Calls taking longer than 5 min"

      - alert: ServiceDown
        expr: up{job="voice-receptionist"} == 0
        for: 1m
        annotations:
          summary: "Voice receptionist service is down"
```

### CloudWatch (AWS)

```python
import watchtower
import logging

# Add CloudWatch handler
cloudwatch_handler = watchtower.CloudWatchLogHandler()
logger.addHandler(cloudwatch_handler)
```

---

## Scaling

### Horizontal Scaling (Multiple Servers)

1. Run multiple Flask instances behind a load balancer (nginx, HAProxy)
2. Use shared PostgreSQL database (not SQLite)
3. Use Redis for session state (optional)

```bash
# Load balancer config (nginx)
upstream voice_receptionist {
    server localhost:5001;
    server localhost:5002;
    server localhost:5003;
}

server {
    listen 80;
    location / {
        proxy_pass http://voice_receptionist;
    }
}
```

### Rate Limiting

Add rate limiter to Flask:

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/call/<call_id>/message')
@limiter.limit("10 per minute")
def process_message(call_id):
    # ...
```

---

## Health Checks

### Application Health Check

```bash
curl http://localhost:5001/health
# {"status": "healthy", "timestamp": "..."}
```

### Skill Bridge Health Check

```bash
curl http://localhost:9000/health
# Should return 200 OK
```

Add healthcheck to systemd:

```ini
[Service]
ExecHealthCheck=/usr/bin/curl -f http://localhost:5001/health
```

---

## Backup & Recovery

### Database Backup

```bash
# PostgreSQL
pg_dump voice_receptionist > backup_$(date +%Y%m%d).sql

# Restore
psql voice_receptionist < backup_20260610.sql
```

### Call Recording Backup

```bash
# If storing recordings, back up S3 or external storage
aws s3 sync s3://voice-recordings /local/backup/
```

---

## Performance Tuning

### Database Indexing

```sql
-- Add indexes for common queries
CREATE INDEX idx_calls_agent_id ON calls(agent_id);
CREATE INDEX idx_calls_created_at ON calls(created_at);
CREATE INDEX idx_leads_agent_id ON leads_captured(lead_score);
CREATE INDEX idx_appointments_scheduled_time ON appointments_scheduled(scheduled_time);
```

### Connection Pooling

```python
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=40
)
```

### Caching

Cache property listings and agent availability:

```python
from functools import lru_cache
import time

@lru_cache(maxsize=128)
def get_property_info(address):
    # Cache property lookups for 1 hour
    return lookup_mls(address)
```

---

## Security

### API Key Rotation

1. Generate new API key in .env.prod
2. Test with new key
3. Update all Twilio configurations
4. Restart service
5. Remove old key

### CORS Configuration

```python
from flask_cors import CORS

CORS(app, origins=['https://your-domain.com'])
```

### Input Validation

```python
@app.before_request
def validate_request():
    if request.method == 'POST':
        # Validate JSON schema
        schema = {
            "type": "object",
            "properties": {
                "transcript": {"type": "string", "maxLength": 5000}
            }
        }
        jsonschema.validate(request.json, schema)
```

---

## Rollback Procedure

If deployment fails:

1. Check service status: `systemctl status voice-receptionist`
2. View logs: `journalctl -u voice-receptionist -n 100`
3. Rollback to previous version:
   ```bash
   git checkout main
   pip3 install -r requirements.txt
   systemctl restart voice-receptionist
   ```
4. Verify: `curl http://localhost:5001/health`

---

## Production Checklist

- [ ] Environment variables set correctly
- [ ] Database backed up
- [ ] HTTPS certificate installed
- [ ] Twilio webhooks configured
- [ ] Logging to CloudWatch/ELK
- [ ] Monitoring/alerting active
- [ ] Load balancer configured (if scaling)
- [ ] Health checks passing
- [ ] Rate limiting enabled
- [ ] Error handling tested
- [ ] Skill Bridge API responding
- [ ] Call tests successful
- [ ] Documentation updated
- [ ] Team trained on monitoring dashboard
