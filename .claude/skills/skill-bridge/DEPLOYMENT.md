# Skill Bridge - Deployment Guide

Complete instructions for deploying Skill Bridge in development, staging, and production environments.

---

## Development Deployment

### Quick Start (Manual)

```bash
# Navigate to skill bridge directory
cd .claude/skills/skill-bridge

# Install dependencies (one-time)
pip install -r requirements.txt

# Run the server
python3 skill_bridge.py
```

Access at: `http://localhost:9000`

### Verify Installation

```bash
# In another terminal
curl http://localhost:9000/health

# Or test with a skill
curl -X POST http://localhost:9000/invoke/prospect \
  -H "Content-Type: application/json" \
  -d '{
    "action": "research",
    "params": {"name": "Test", "company": "Test Corp"}
  }'
```

### Development Configuration

Create `.env.local`:

```bash
SKILL_BRIDGE_HOST=127.0.0.1
SKILL_BRIDGE_PORT=9000
SKILL_BRIDGE_DEBUG=true
SKILL_TIMEOUT=120
CLAUDE_CODE_WORKSPACE=/path/to/woodworks-os
```

---

## Staging Deployment

### Using Systemd (Recommended for Linux)

#### 1. Create Service File

```bash
# Copy the provided service file
sudo cp systemd-skill-bridge.service /etc/systemd/system/

# Edit to set your paths and user
sudo nano /etc/systemd/system/systemd-skill-bridge.service
```

Update these lines:
```ini
User=your-username
Group=your-group
WorkingDirectory=/home/your-user/woodworks-os
ExecStart=/usr/bin/python3 /home/your-user/woodworks-os/.claude/skills/skill-bridge/skill_bridge.py
```

#### 2. Enable and Start Service

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable auto-start on boot
sudo systemctl enable skill-bridge

# Start the service
sudo systemctl start skill-bridge

# Check status
sudo systemctl status skill-bridge

# View logs
sudo journalctl -u skill-bridge -f
```

#### 3. Configure Environment

Add to `/etc/systemd/system/systemd-skill-bridge.service`:

```ini
[Service]
Environment="SKILL_BRIDGE_HOST=127.0.0.1"
Environment="SKILL_BRIDGE_PORT=9000"
Environment="SKILL_BRIDGE_API_KEY=your-secret-key"
Environment="SKILL_TIMEOUT=120"
```

Then reload:
```bash
sudo systemctl daemon-reload
sudo systemctl restart skill-bridge
```

### Using Docker (Alternative)

#### 1. Build Image

```bash
cd .claude/skills/skill-bridge

# Build Docker image
docker build -t skill-bridge:latest .

# Verify build
docker images | grep skill-bridge
```

#### 2. Create Docker Container

```bash
# Run container
docker run -d \
  --name skill-bridge \
  -p 9000:9000 \
  -e SKILL_BRIDGE_HOST=0.0.0.0 \
  -e SKILL_BRIDGE_PORT=9000 \
  -v /path/to/woodworks-os:/app/workspace \
  skill-bridge:latest

# Check logs
docker logs -f skill-bridge

# Stop container
docker stop skill-bridge

# Remove container
docker rm skill-bridge
```

#### 3. Docker Compose (Optional)

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  skill-bridge:
    build: .
    container_name: skill-bridge
    ports:
      - "9000:9000"
    environment:
      SKILL_BRIDGE_HOST: 0.0.0.0
      SKILL_BRIDGE_PORT: 9000
      SKILL_BRIDGE_DEBUG: "false"
      SKILL_TIMEOUT: 120
    volumes:
      - /path/to/woodworks-os:/app/workspace
    restart: unless-stopped
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

Run with:
```bash
docker-compose up -d
docker-compose logs -f
docker-compose down
```

---

## Production Deployment

### Architecture

```
Client
  ↓
Load Balancer (nginx/HAProxy)
  ↓
Skill Bridge API (multiple instances)
  ↓
PostgreSQL Database (shared)
  ↓
Claude Code Workspace (shared NFS/mount)
```

### Prerequisites

- Linux (Ubuntu 20.04+ recommended)
- Python 3.8+
- systemd or Docker
- PostgreSQL 12+ (for multi-server setup)
- nginx (for reverse proxy)

### Step 1: Database Setup (PostgreSQL)

For multi-server deployments, migrate from SQLite to PostgreSQL:

```bash
# Install PostgreSQL
sudo apt install postgresql postgresql-contrib

# Create database and user
sudo -u postgres psql

# In psql shell:
CREATE DATABASE skill_bridge;
CREATE USER skill_bridge_user WITH PASSWORD 'your-secure-password';
ALTER ROLE skill_bridge_user SET client_encoding TO 'utf8';
ALTER ROLE skill_bridge_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE skill_bridge_user SET default_transaction_deferrable TO on;
ALTER ROLE skill_bridge_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE skill_bridge TO skill_bridge_user;
\q
```

Update `bridge_database.py` to use PostgreSQL (or add environment variable for DB connection).

### Step 2: Install Skill Bridge

```bash
# Create application user
sudo useradd -m -s /bin/bash skill-bridge

# Create directory
sudo mkdir -p /opt/skill-bridge
cd /opt/skill-bridge

# Clone/copy files
sudo git clone <repo> . # or copy files
sudo chown -R skill-bridge:skill-bridge /opt/skill-bridge

# Install dependencies
cd /opt/skill-bridge
pip3 install -r requirements.txt
```

### Step 3: Configure Environment

Create `/opt/skill-bridge/.env.production`:

```bash
# Network
SKILL_BRIDGE_HOST=127.0.0.1
SKILL_BRIDGE_PORT=9000
SKILL_BRIDGE_DEBUG=false

# Security
SKILL_BRIDGE_API_KEY=your-very-secure-random-key

# Timeouts
SKILL_TIMEOUT=120

# Database (PostgreSQL)
DATABASE_URL=postgresql://skill_bridge_user:password@localhost:5432/skill_bridge

# Workspace
CLAUDE_CODE_WORKSPACE=/path/to/woodworks-os

# Logging
LOG_LEVEL=INFO
```

Secure the file:
```bash
sudo chmod 600 /opt/skill-bridge/.env.production
```

### Step 4: Systemd Service (Multi-Instance)

For high availability, run multiple instances:

Create `/etc/systemd/system/skill-bridge@.service`:

```ini
[Unit]
Description=Skill Bridge API Instance %i
Documentation=https://github.com/your-org/woodworks-os
After=network.target postgresql.service

[Service]
Type=simple
User=skill-bridge
Group=skill-bridge

WorkingDirectory=/opt/skill-bridge

Environment="PATH=/usr/local/bin:/usr/bin:/bin"
Environment="PYTHONUNBUFFERED=1"

# Load environment from file
EnvironmentFile=/opt/skill-bridge/.env.production

# Port assignment (9000 + instance number)
Environment="SKILL_BRIDGE_PORT=900%i"

ExecStart=/usr/bin/python3 /opt/skill-bridge/skill_bridge.py

Restart=on-failure
RestartSec=10
StartLimitInterval=600
StartLimitBurst=3

StandardOutput=journal
StandardError=journal
SyslogIdentifier=skill-bridge-%i

KillMode=mixed
KillSignal=SIGTERM
TimeoutStopSec=30

[Install]
WantedBy=multi-user.target
```

Start multiple instances:
```bash
sudo systemctl enable skill-bridge@{0,1,2}
sudo systemctl start skill-bridge@{0,1,2}
sudo systemctl status skill-bridge@{0,1,2}
```

### Step 5: Nginx Reverse Proxy

Create `/etc/nginx/sites-available/skill-bridge`:

```nginx
upstream skill_bridge_backend {
    least_conn;
    server 127.0.0.1:9000;
    server 127.0.0.1:9001;
    server 127.0.0.1:9002;
}

server {
    listen 80;
    server_name skill-bridge.example.com;

    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name skill-bridge.example.com;

    # SSL Configuration
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # Logging
    access_log /var/log/nginx/skill-bridge-access.log;
    error_log /var/log/nginx/skill-bridge-error.log;

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=skill_bridge_limit:10m rate=10r/s;
    limit_req zone=skill_bridge_limit burst=20 nodelay;

    # Proxy settings
    proxy_connect_timeout 60s;
    proxy_send_timeout 60s;
    proxy_read_timeout 60s;

    location / {
        proxy_pass http://skill_bridge_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /health {
        access_log off;
        proxy_pass http://skill_bridge_backend;
    }
}
```

Enable:
```bash
sudo ln -s /etc/nginx/sites-available/skill-bridge /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Step 6: Monitoring & Logging

#### Systemd Logging

```bash
# View all logs
sudo journalctl -u "skill-bridge@*" -f

# View specific instance
sudo journalctl -u skill-bridge@0 -f

# Persistent journald
sudo mkdir -p /var/log/journal
sudo systemctl restart systemd-journald
```

#### Log Rotation

Create `/etc/logrotate.d/skill-bridge`:

```
/var/log/skill-bridge/*.log {
    daily
    rotate 7
    compress
    delaycompress
    notifempty
    create 0640 skill-bridge skill-bridge
    sharedscripts
    postrotate
        /bin/systemctl reload-or-restart skill-bridge@*.service > /dev/null 2>&1 || true
    endscript
}
```

#### Prometheus Metrics (Optional)

Add to `skill_bridge.py`:

```python
from prometheus_client import Counter, Histogram, generate_latest
import time

# Metrics
skill_invocations_total = Counter(
    'skill_invocations_total',
    'Total skill invocations',
    ['skill_name', 'status']
)
skill_invocation_duration = Histogram(
    'skill_invocation_duration_ms',
    'Skill invocation duration',
    ['skill_name']
)

# Add metrics collection to invoke_skill()
# Then expose at /metrics endpoint
```

### Step 7: Health Checks & Monitoring

#### Systemd Health Check

The service will auto-restart on failure. Monitor status:

```bash
systemctl status skill-bridge@0
```

#### Prometheus Scrape Config

Add to `prometheus.yml`:

```yaml
scrape_configs:
  - job_name: 'skill-bridge'
    static_configs:
      - targets: ['skill-bridge.example.com:443']
    scheme: https
    metrics_path: '/metrics'
```

#### Custom Health Monitoring

```bash
#!/bin/bash
# Check all instances

for i in {0,1,2}; do
    response=$(curl -s http://127.0.0.1:$((9000+$i))/health)
    status=$(echo $response | jq -r '.status')
    
    if [ "$status" = "healthy" ]; then
        echo "✓ Instance $i: healthy"
    else
        echo "✗ Instance $i: unhealthy"
        systemctl restart skill-bridge@$i
    fi
done
```

### Step 8: Backup & Recovery

#### Database Backup

```bash
# PostgreSQL backup
pg_dump -U skill_bridge_user skill_bridge > /backups/skill_bridge_$(date +%Y%m%d).sql

# Restore
psql -U skill_bridge_user skill_bridge < /backups/skill_bridge_20240115.sql
```

#### Application Backup

```bash
# Daily backup
tar czf /backups/skill-bridge_$(date +%Y%m%d).tar.gz /opt/skill-bridge
```

#### Backup Script

Create `/usr/local/bin/backup-skill-bridge`:

```bash
#!/bin/bash

BACKUP_DIR="/backups/skill-bridge"
RETENTION_DAYS=30

mkdir -p $BACKUP_DIR

# Database backup
pg_dump -U skill_bridge_user skill_bridge | \
    gzip > $BACKUP_DIR/database_$(date +%Y%m%d-%H%M%S).sql.gz

# Application backup
tar czf $BACKUP_DIR/application_$(date +%Y%m%d-%H%M%S).tar.gz /opt/skill-bridge

# Cleanup old backups
find $BACKUP_DIR -name "*.gz" -mtime +$RETENTION_DAYS -delete

echo "Backup completed at $(date)"
```

Add to crontab:
```bash
0 2 * * * /usr/local/bin/backup-skill-bridge
```

### Step 9: Security Hardening

#### Firewall Rules

```bash
# Allow traffic to nginx only (not direct to skill-bridge)
sudo ufw default deny incoming
sudo ufw allow 22/tcp      # SSH
sudo ufw allow 80/tcp      # HTTP
sudo ufw allow 443/tcp     # HTTPS
sudo ufw enable
```

#### API Key Rotation

```bash
# Generate new key
NEW_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")

# Update environment
sudo nano /opt/skill-bridge/.env.production
# Change SKILL_BRIDGE_API_KEY=$NEW_KEY

# Restart services
sudo systemctl restart skill-bridge@{0,1,2}
```

#### SELinux (CentOS/RHEL)

```bash
# Create policy for skill-bridge
sudo semanage fcontext -a -t httpd_sys_rw_content_t "/opt/skill-bridge(/.*)?"
sudo semanage port -a -t http_port_t -p tcp 9000-9002
sudo restorecon -Rv /opt/skill-bridge
```

---

## Monitoring Checklist

- [ ] Health checks passing (curl /health)
- [ ] API responding to requests
- [ ] Database connections stable
- [ ] Error rate < 1%
- [ ] Response time < 10s (p99)
- [ ] Disk space > 20% free
- [ ] CPU usage < 80%
- [ ] Memory usage < 80%
- [ ] Logs rotating correctly
- [ ] Backups running daily

---

## Troubleshooting

### Service won't start

```bash
# Check logs
sudo journalctl -u skill-bridge@0 -n 50

# Check Python syntax
python3 -m py_compile skill_bridge.py

# Check dependencies
pip3 list | grep -i flask
```

### High memory usage

```bash
# Monitor process
top -p $(pgrep -f skill_bridge)

# Restart service
sudo systemctl restart skill-bridge@0

# Check for memory leaks in logs
```

### Database locked

```bash
# Check active connections
psql -c "SELECT * FROM pg_stat_activity;"

# Kill idle connections
SELECT pg_terminate_backend(pg_stat_activity.pid)
  FROM pg_stat_activity
  WHERE state = 'idle' AND query_start < now() - interval '1 hour';
```

### Port already in use

```bash
# Find process using port
sudo lsof -i :9000

# Kill process
sudo kill -9 <PID>
```

---

## Performance Tuning

### Python WSGI Server (Production)

Replace Flask's built-in server with Gunicorn:

```bash
pip3 install gunicorn

# Run with Gunicorn
gunicorn --workers 4 --threads 2 --worker-class gthread \
  --bind 127.0.0.1:9000 \
  --access-logfile /var/log/skill-bridge/access.log \
  --error-logfile /var/log/skill-bridge/error.log \
  skill_bridge:app
```

### Database Connection Pooling

Add to `bridge_database.py`:

```python
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20
)
```

---

## Rollback Procedure

If deployment fails:

```bash
# Stop services
sudo systemctl stop skill-bridge@{0,1,2}

# Restore from backup
cd /opt/skill-bridge
git revert <commit-hash>
# or
tar xzf /backups/skill-bridge_backup.tar.gz

# Restore database
psql -U skill_bridge_user skill_bridge < /backups/database_backup.sql

# Restart
sudo systemctl start skill-bridge@{0,1,2}

# Verify
curl https://skill-bridge.example.com/health
```

---

## Summary

**Development:** Run locally with `python3 skill_bridge.py`
**Staging:** Use systemd service on single server
**Production:** Multi-instance with nginx load balancer and PostgreSQL

See QUICK_START.md for testing and README.md for full documentation.
