---
name: calendar
description: View availability, schedule calls, block focus time, and manage your calendar
---

# Calendar

Manage your time and schedule. View what's coming up, schedule calls with prospects, and block focus time for deep work.

---

## Operations

### `/calendar view [timeframe]` - See your upcoming schedule

Timeframes:
- `today` — what's on your calendar today
- `week` — this week's schedule
- `next 7` — next 7 days
- `next 30` — next 30 days

Shows:
- Time blocks (calls, meetings, focus time)
- Free slots for new calls
- Busiest days
- Notes on each event

Example: `/calendar view week`

### `/calendar schedule [prospect] [topic] [duration]` - Book a call

When scheduling a prospect call:

1. Check your availability (pull free slots from calendar)
2. Suggest 2-3 times that work
3. User picks one
4. Create calendar event:
   - Title: `Call: [Prospect Name] - [Topic]`
   - Duration: [user specified, default 30 min]
   - Add to your calendar (and prospect if possible)
5. Update prospect status to `demo-scheduled` or `contact-made` depending on stage
6. Log in `/crm log [prospect name]`

Example: `/calendar schedule ABC Real Estate Group lead follow-up automation 30 min`

Then you provide: preferred date/time

### `/calendar block [hours] [type] [date]` - Block focus time

Lock time for deep work:

- `/calendar block 2 focus-work today` — 2 hours of uninterrupted work today
- `/calendar block 4 automation-build 2026-06-03` — full day of build work
- `/calendar block 1 proposal-writing tomorrow` — proposal writing time

Shows what time blocks are available for deep work vs. calls.

Example: `/calendar block 3 client-calls thursday`

### `/calendar conflicts` - Check for scheduling issues

Shows:
- Double-booked times (if any)
- Back-to-back meetings with no buffer
- Days where you have no focus time
- Suggested optimization

Helps prevent burnout and keep some time for admin work.

### `/calendar capacity` - See your availability at a glance

Shows:
- Hours scheduled this week (calls, meetings)
- Hours available for focus work
- Recommended hours: 60% meetings/client time, 40% deep work
- If you're overbooked, suggests what to move or decline

Example output:
```
This Week:
- Scheduled: 8 hours (calls, meetings)
- Focus time available: 12 hours
- Recommended balance: 10 hours calls / 10 hours focus
Status: Good balance ✓
```

---

## Calendar Integration

This skill works best when connected to your actual calendar (Google Calendar or Outlook):

**Setup (one-time):**
- Link your Google Calendar or Outlook to Claude Code
- Give Claude access to read your calendar
- It will see your real availability and avoid double-booking

**Without integration:**
- Tell Claude when you're free (e.g., "I'm available Tue-Thu 2-4pm")
- Log calls manually after they happen

---

## Meeting Best Practices

**Call scheduling:**
- Default 30 min for initial calls or demos
- 60 min for detailed discovery or complex scopes
- Build in 15-min buffer between back-to-back calls

**Focus time:**
- Block 2-4 hours minimum for deep work (automation builds, proposal writing)
- No meetings during focus blocks
- Best times: early morning or late afternoon

**Capacity limits:**
- Aim for no more than 10 hours of meetings/calls per week
- Keep 20 hours minimum for delivery and admin work
- If you're at 15+ hours of meetings, you can't deliver quality work

---

## Linking to Your Workflow

When you schedule a call, it automatically:
1. Creates calendar event with prospect name and topic
2. Updates prospect status (e.g., `contact-made` → `demo-scheduled`)
3. Logs in `wiki/log.md` that demo was scheduled
4. Sets reminder 1 hour before call

When call ends:
- `/crm log [prospect name]` to capture outcome
- Calendar event auto-notes with result (interested, objections, next steps)

---

## Time Blocking Strategy

Suggested weekly structure:

| Time | Monday | Tuesday | Wednesday | Thursday | Friday |
|------|--------|---------|-----------|----------|--------|
| 9-11am | Focus | Demo | Demo | Focus | Focus |
| 11-12 | Calls | Calls | Calls | Calls | Admin |
| 1-3pm | Focus | Focus | Demo | Focus | Planning |
| 3-5pm | Calls | Calls | Calls | Calls | Calls |

Adjust based on your rhythm, but pattern: cluster calls, protect focus time.

---

## Overbooked? What to Do

If your calendar is slammed:
1. Move lower-priority calls to next week
2. Batch calls on 2-3 days (e.g., all calls on Tue/Thu)
3. Use group calls for multiple prospects with similar needs
4. Block focus time non-negotiably

If you can't do all three (sell, deliver, manage), you need to hire or automate something. Log this as a priority in `wiki/overview.md`.
