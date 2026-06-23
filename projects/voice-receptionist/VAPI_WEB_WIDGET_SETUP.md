# Vapi Web Widget Setup

Live in 3 steps.

---

## Step 1: Get Your Assistant ID

1. Go to https://vapi.ai (sign in if needed)
2. Click your assistant
3. Click **Settings**
4. Copy the **Assistant ID** (looks like: `asst_abc123xyz`)

---

## Step 2: Update index.html

Open `index.html` in this folder.

Find this line:
```javascript
const ASSISTANT_ID = "YOUR_ASSISTANT_ID_HERE";
```

Replace `YOUR_ASSISTANT_ID_HERE` with your actual ID from Step 1.

Example:
```javascript
const ASSISTANT_ID = "asst_a1b2c3d4e5f6g7h8";
```

Save the file.

---

## Step 3: Open in Browser

Double-click `index.html` or:

```bash
open index.html
```

A page opens with a purple button in the bottom right.

Click it. Say something:

```
"I want to see the 3-bedroom on Oak Street Friday afternoon"
```

Receptionist responds with voice. ✅

---

## Done

Your AI receptionist is live.

**No server. No deployment. Just works.**

---

## To Share

Host this file anywhere:
- GitHub Pages (free)
- Vercel (free)
- Netlify (free)
- Your website

Share the link. People click and call.

---

## Test Scenarios

Try these:

1. **Schedule:** "I'd like to see a 3-bedroom"
2. **Qualify:** "I'm selling my condo in 3 months"
3. **Message:** "Leave a message for the agent"

Receptionist should respond appropriately.

---

## Next Steps

- ✅ Web widget working
- ⏳ (Optional) Buy phone number for $1-2/month
- ⏳ (Optional) Integrate with your CRM (webhook)
- ⏳ (Optional) Customize voice, personality, system prompt

See VAPI_SETUP.md for advanced options.
