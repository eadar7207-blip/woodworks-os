#!/usr/bin/env python3
"""
Sohail Real Estate Group - AI Lead Follow-Up System
Run: python3 server.py
Open: http://localhost:5050
"""
import json
import os
import smtplib
import ssl
import threading
from datetime import datetime
from email.mime.text import MIMEText
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

import anthropic

# Load .env
_env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
if os.path.exists(_env_path):
    with open(_env_path) as _f:
        for _line in _f:
            _line = _line.strip()
            if _line and not _line.startswith("#") and "=" in _line:
                _k, _, _v = _line.partition("=")
                if _v:
                    os.environ.setdefault(_k.strip(), _v.strip())

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
GMAIL_USER        = os.getenv("GMAIL_USER", "")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD", "").replace(" ", "")
AGENT_EMAIL       = os.getenv("AGENT_EMAIL", GMAIL_USER)
ADMIN_PASSWORD    = os.getenv("ADMIN_PASSWORD", "sohail2024")

leads_log = []


# ── AI ──────────────────────────────────────────────────────────────────────

def ai_follow_up_email(name, interest, timeline, budget, phone=""):
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    phone_line = f"- Phone: {phone}" if phone else ""
    msg = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=300,
        messages=[{"role": "user", "content": f"""You are an AI assistant for Sohail Real Estate Group in Chicago.
A new lead just came in. Write a short, warm, personalized follow-up email to send to them.

Lead details:
- Name: {name}
- Looking to: {interest}
- Timeline: {timeline}
- Budget: {budget}
{phone_line}

Rules:
- 3-4 sentences max
- Sound like a real person, not a robot
- Mention their specific interest and timeline
- End with a clear next step (schedule a quick call)
- Sign off as "Sohail Real Estate Group"
- No subject line, just the body
"""}]
    )
    return msg.content[0].text


# ── EMAIL ────────────────────────────────────────────────────────────────────

def send_gmail(to: str, subject: str, body: str):
    if not GMAIL_USER or not GMAIL_APP_PASSWORD:
        print(f"[EMAIL NOT CONFIGURED] Would send to {to}:\n{body}")
        return
    try:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = GMAIL_USER
        msg["To"] = to
        ctx = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ctx) as s:
            s.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            s.sendmail(GMAIL_USER, to, msg.as_string())
        print(f"[EMAIL] Sent to {to}: {subject}")
    except Exception as e:
        print(f"[EMAIL ERROR] {e}")


def notify_agent(lead: dict):
    subject = f"New Lead: {lead['name']} - {lead['interest']}"
    body = f"""New lead came in at {lead['submitted_at']}

Name:     {lead['name']}
Email:    {lead['email']}
Phone:    {lead.get('phone', 'not provided')}
Interest: {lead['interest']}
Timeline: {lead['timeline']}
Budget:   {lead['budget']}

AI already sent this follow-up to the lead:
---
{lead.get('ai_response', '')}
---

Call them now while they're hot.
"""
    send_gmail(AGENT_EMAIL, subject, body)


def send_lead_confirmation(lead: dict):
    """Send the AI-written email to the lead themselves."""
    if not lead.get("email") or not lead.get("ai_response"):
        return
    send_gmail(
        lead["email"],
        "Thanks for reaching out - Sohail Real Estate Group",
        lead["ai_response"]
    )


# ── HTML ─────────────────────────────────────────────────────────────────────

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Sohail Real Estate Group - AI Demo</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #0f0f13; color: #f0f0f0; min-height: 100vh; }

  .header { background: #0f0f13; border-bottom: 1px solid #1e1e2e; padding: 20px 32px; display: flex; align-items: center; gap: 12px; }
  .logo { width: 36px; height: 36px; background: #7c5cff; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 16px; }
  .header h1 { font-size: 17px; font-weight: 600; }
  .header .badge { font-size: 12px; color: #6b7280; margin-left: 8px; background: #1e1e2e; padding: 2px 8px; border-radius: 20px; }

  .hero { text-align: center; padding: 64px 24px 48px; }
  .hero h2 { font-size: 42px; font-weight: 700; line-height: 1.15; max-width: 640px; margin: 0 auto 16px; }
  .hero h2 span { color: #7c5cff; }
  .hero p { color: #9ca3af; font-size: 18px; max-width: 500px; margin: 0 auto; }

  .stats { display: flex; justify-content: center; gap: 48px; padding: 32px 24px; border-top: 1px solid #1e1e2e; border-bottom: 1px solid #1e1e2e; margin: 0 0 48px; }
  .stat .number { font-size: 32px; font-weight: 700; color: #7c5cff; text-align: center; }
  .stat .label { font-size: 13px; color: #6b7280; margin-top: 4px; text-align: center; }

  .demo-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; max-width: 1000px; margin: 0 auto 64px; padding: 0 24px; }

  .card { background: #16161f; border: 1px solid #1e1e2e; border-radius: 16px; padding: 32px; }
  .card h3 { font-size: 18px; font-weight: 600; margin-bottom: 6px; }
  .card .subtitle { font-size: 13px; color: #6b7280; margin-bottom: 24px; }

  .form-group { margin-bottom: 16px; }
  .form-group label { display: block; font-size: 13px; color: #9ca3af; margin-bottom: 6px; font-weight: 500; }
  .form-group input, .form-group select { width: 100%; background: #0f0f13; border: 1px solid #2a2a3e; border-radius: 8px; padding: 10px 14px; color: #f0f0f0; font-size: 14px; outline: none; }
  .form-group input:focus, .form-group select:focus { border-color: #7c5cff; }
  .form-group select option { background: #16161f; }

  .btn { width: 100%; padding: 12px; background: #7c5cff; color: white; border: none; border-radius: 8px; font-size: 15px; font-weight: 600; cursor: pointer; transition: background 0.2s; }
  .btn:hover { background: #6a4de8; }
  .btn:disabled { background: #3a3a5c; cursor: not-allowed; }

  .response-area { margin-top: 20px; display: none; }
  .response-area.visible { display: block; }
  .response-box { background: #0f0f13; border: 1px solid #2a2a3e; border-radius: 8px; padding: 16px; font-size: 14px; color: #d1d5db; line-height: 1.6; white-space: pre-wrap; }
  .response-tag { display: inline-block; font-size: 11px; font-weight: 600; padding: 3px 8px; border-radius: 20px; margin-bottom: 10px; }
  .tag-pending { background: #2a2a1e; color: #facc15; }
  .tag-done { background: #1e2a1e; color: #4ade80; }
  .timer { font-size: 12px; color: #6b7280; margin-top: 8px; }

  .email-note { font-size: 12px; color: #4ade80; margin-top: 8px; }

  .leads-list { min-height: 200px; }
  .lead-item { border-bottom: 1px solid #1e1e2e; padding: 14px 0; }
  .lead-item:last-child { border-bottom: none; }
  .lead-name { font-weight: 600; font-size: 14px; }
  .lead-meta { font-size: 12px; color: #6b7280; margin-top: 4px; }
  .lead-status { display: inline-block; font-size: 11px; padding: 2px 8px; border-radius: 20px; margin-top: 6px; }
  .status-new { background: #1e2040; color: #818cf8; }
  .status-responded { background: #1e2a1e; color: #4ade80; }
  .empty-state { color: #4b5563; font-size: 14px; padding: 32px 0; text-align: center; }

  @media (max-width: 700px) { .demo-grid { grid-template-columns: 1fr; } .stats { gap: 24px; } .hero h2 { font-size: 28px; } }
</style>
</head>
<body>

<div class="header">
  <div class="logo">S</div>
  <h1>Sohail Real Estate Group</h1>
  <span class="badge">AI Demo</span>
</div>

<div class="hero">
  <h2>Every lead gets a reply in <span>under 60 seconds</span>. Automatically.</h2>
  <p>Submit a test lead below and watch the AI respond in real time.</p>
</div>

<div class="stats">
  <div class="stat"><div class="number">&lt;60s</div><div class="label">Average response time</div></div>
  <div class="stat"><div class="number">24/7</div><div class="label">Always on, no days off</div></div>
  <div class="stat"><div class="number">100%</div><div class="label">Leads contacted</div></div>
</div>

<div class="demo-grid">
  <div class="card">
    <h3>Submit a Test Lead</h3>
    <div class="subtitle">Fill this out as if you're a new buyer or seller.</div>
    <form id="leadForm">
      <div class="form-group">
        <label>Full Name</label>
        <input type="text" id="name" placeholder="e.g. John Smith" required>
      </div>
      <div class="form-group">
        <label>Email</label>
        <input type="email" id="email" placeholder="your@email.com" required>
      </div>
      <div class="form-group">
        <label>Phone (optional)</label>
        <input type="tel" id="phone" placeholder="(312) 555-0100">
      </div>
      <div class="form-group">
        <label>I'm looking to...</label>
        <select id="interest">
          <option value="buy a home in Chicago">Buy a home in Chicago</option>
          <option value="sell my property">Sell my property</option>
          <option value="invest in Chicago real estate">Invest in Chicago real estate</option>
        </select>
      </div>
      <div class="form-group">
        <label>Timeline</label>
        <select id="timeline">
          <option value="ASAP - within 30 days">ASAP - within 30 days</option>
          <option value="1-3 months">1-3 months</option>
          <option value="3-6 months">3-6 months</option>
          <option value="just exploring">Just exploring</option>
        </select>
      </div>
      <div class="form-group">
        <label>Budget</label>
        <select id="budget">
          <option value="$300K-$500K">$300K - $500K</option>
          <option value="$500K-$800K">$500K - $800K</option>
          <option value="$800K+">$800K+</option>
        </select>
      </div>
      <button type="submit" class="btn" id="submitBtn">Submit Lead</button>
    </form>
    <div class="response-area" id="responseArea">
      <div class="response-tag tag-pending" id="responseTag">Generating AI response...</div>
      <div class="response-box" id="responseBox"></div>
      <div class="timer" id="timerLabel"></div>
      <div class="email-note" id="emailNote"></div>
    </div>
  </div>

  <div class="card">
    <h3>Live Lead Feed</h3>
    <div class="subtitle">Every submitted lead, updated in real time.</div>
    <div class="leads-list" id="leadsList">
      <div class="empty-state">No leads yet. Submit one on the left.</div>
    </div>
  </div>
</div>

<script>
let startTime;

document.getElementById('leadForm').addEventListener('submit', async function(e) {
  e.preventDefault();
  const btn = document.getElementById('submitBtn');
  btn.disabled = true;
  btn.textContent = 'Processing...';
  startTime = Date.now();

  const data = {
    name: document.getElementById('name').value,
    email: document.getElementById('email').value,
    phone: document.getElementById('phone').value,
    interest: document.getElementById('interest').value,
    timeline: document.getElementById('timeline').value,
    budget: document.getElementById('budget').value,
  };

  const responseArea = document.getElementById('responseArea');
  const responseBox  = document.getElementById('responseBox');
  const responseTag  = document.getElementById('responseTag');
  const timerLabel   = document.getElementById('timerLabel');
  const emailNote    = document.getElementById('emailNote');

  responseArea.classList.add('visible');
  responseTag.className = 'response-tag tag-pending';
  responseTag.textContent = 'AI generating response...';
  responseBox.textContent = '';
  timerLabel.textContent = '';
  emailNote.textContent = '';

  try {
    const res  = await fetch('/submit-lead', { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify(data) });
    const json = await res.json();
    const elapsed = ((Date.now() - startTime) / 1000).toFixed(1);

    responseTag.className = 'response-tag tag-done';
    responseTag.textContent = 'AI responded';
    responseBox.textContent = json.ai_response;
    timerLabel.textContent = `Response generated in ${elapsed}s`;
    emailNote.textContent = 'Email sent to lead + agent notified';

    refreshLeads();
  } catch (err) {
    responseTag.textContent = 'Error';
    responseBox.textContent = err.message;
  }

  btn.disabled = false;
  btn.textContent = 'Submit Another Lead';
});

async function refreshLeads() {
  const res   = await fetch('/leads');
  const leads = await res.json();
  const list  = document.getElementById('leadsList');
  if (!leads.length) { list.innerHTML = '<div class="empty-state">No leads yet.</div>'; return; }
  list.innerHTML = leads.slice().reverse().map(l => `
    <div class="lead-item">
      <div class="lead-name">${l.name}</div>
      <div class="lead-meta">${l.interest} &middot; ${l.timeline} &middot; ${l.budget}</div>
      <div class="lead-meta">${l.email}${l.phone ? ' &middot; ' + l.phone : ''}</div>
      <div class="lead-meta">Submitted ${l.submitted_at}</div>
      ${l.status === 'responded'
        ? `<span class="lead-status status-responded">AI responded at ${l.responded_at}</span>`
        : '<span class="lead-status status-new">Processing...</span>'}
    </div>
  `).join('');
}

setInterval(refreshLeads, 3000);
</script>
</body>
</html>
"""


# ── HTTP SERVER ───────────────────────────────────────────────────────────────

class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def send_json(self, data, status=200):
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, X-Admin-Password")
        self.end_headers()

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/leads":
            # Require admin password header or query param
            pw = self.headers.get("X-Admin-Password") or ""
            if pw != ADMIN_PASSWORD:
                self.send_json({"error": "unauthorized"}, 401)
                return
            self.send_json(leads_log)
        elif path == "/health":
            self.send_json({"status": "ok"})
        else:
            body = HTML.encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    def _process_lead(self, data: dict):
        lead = {
            "id": len(leads_log) + 1,
            "name":      data.get("name", ""),
            "email":     data.get("email", ""),
            "phone":     data.get("phone", ""),
            "interest":  data.get("interest", ""),
            "timeline":  data.get("timeline", ""),
            "budget":    data.get("budget", ""),
            "source":    data.get("source", "form"),
            "submitted_at": datetime.now().strftime("%I:%M:%S %p"),
            "status":    "processing",
            "ai_response": "",
            "responded_at": "",
        }
        leads_log.append(lead)

        try:
            lead["ai_response"] = ai_follow_up_email(
                lead["name"], lead["interest"], lead["timeline"], lead["budget"], lead["phone"]
            )
            lead["responded_at"] = datetime.now().strftime("%I:%M:%S %p")
            lead["status"] = "responded"
        except Exception as e:
            lead["ai_response"] = f"(AI error: {e})"
            lead["status"] = "error"

        # Fire emails in background - don't block the response
        threading.Thread(target=notify_agent, args=(lead,), daemon=True).start()
        threading.Thread(target=send_lead_confirmation, args=(lead,), daemon=True).start()

        return lead

    def do_POST(self):
        path = urlparse(self.path).path
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length)

        try:
            data = json.loads(raw) if raw else {}
        except Exception:
            self.send_json({"error": "invalid json"}, 400)
            return

        if path in ("/submit-lead", "/webhook/lead"):
            lead = self._process_lead(data)
            self.send_json(lead)
        else:
            self.send_json({"error": "not found"}, 404)


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5050))
    server = HTTPServer(("0.0.0.0", port), Handler)
    print(f"Running at http://localhost:{port}")
    print(f"Webhook: POST http://localhost:{port}/webhook/lead")
    print(f"Agent notifications -> {AGENT_EMAIL}")
    server.serve_forever()
