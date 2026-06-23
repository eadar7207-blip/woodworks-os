---
name: invoicing
description: Create invoices, track payments, and manage billing for projects
---

# Invoicing

Generate invoices from proposals, track payment status, and manage your revenue. Invoices stay in the wiki for easy reference.

---

## Operations

### `/invoicing create [prospect name] [amount] [description]` - Create an invoice

When creating an invoice:

1. Pull prospect and proposal context from wiki
2. Ask: payment terms (50/50 split, net 30, upfront, etc.), due date
3. Generate invoice with:
   - Invoice number (auto-incrementing)
   - Client name and info
   - Description of work (automation build, retainer, consulting, etc.)
   - Amount due
   - Due date
   - Payment terms and instructions
   - Your business info

4. Save to `wiki/invoices.md`
5. Update prospect record with invoice info

Example: `/invoicing create ABC Real Estate Group 3500 "Lead Follow-Up Automation - Build Phase"`

Then you provide: payment terms, due date

### `/invoicing send [invoice number]` - Mark invoice as sent

When you send an invoice:

1. Update status to `sent`
2. Record send date
3. Calculate expected payment date based on terms
4. Set reminder for follow-up if not paid by due date

Example: `/invoicing send INV-001`

### `/invoicing paid [invoice number]` - Record payment

When payment arrives:

1. Update status to `paid`
2. Record payment date and amount
3. Update prospect to `closed-won` (if it was the final payment)
4. Log the revenue in `wiki/log.md`

Example: `/invoicing paid INV-001`

### `/invoicing follow-up [days]` - Show overdue invoices

List invoices past due date:

- `/invoicing follow-up 3` — invoices overdue by 3+ days
- `/invoicing follow-up 7` — invoices more than a week past due
- `/invoicing follow-up all` — all outstanding invoices

Shows:
- Invoice number and amount
- Client name
- Days overdue
- Suggested action (email reminder, call, stop work until paid)

### `/invoicing dashboard` - Financial snapshot

Shows:
- Total revenue this month
- Outstanding invoices (unpaid amount and count)
- Expected revenue (invoices sent, pending payment)
- Overdue invoices (alert!)
- Average payment time
- Monthly revenue trend

---

## Invoice Structure

Invoices live in `wiki/invoices.md`:

```markdown
---
title: Invoices
type: invoicing
updated: YYYY-MM-DD
---

# Invoices

## [YYYY-MM] (organized by month)

| Invoice # | Client | Amount | Date Sent | Due Date | Status | Days Outstanding |
|-----------|--------|--------|-----------|----------|--------|-------------------|
| INV-001 | ABC Real Estate | $3,500 | 2026-05-29 | 2026-06-12 | sent | 0 |
| INV-002 | XYZ Realty | $5,000 | 2026-05-28 | 2026-06-11 | paid | - |

### INV-001 - ABC Real Estate Group
- **Amount:** $3,500
- **Description:** Lead Follow-Up Automation - Build Phase
- **Sent:** 2026-05-29
- **Due:** 2026-06-12 (Net 30)
- **Status:** sent
- **Terms:** 50% on start, 50% on completion
- **Notes:** First payment received 2026-05-15

### INV-002 - XYZ Realty
- **Amount:** $5,000
- **Description:** Multi-Step Lead Scoring Automation
- **Sent:** 2026-05-28
- **Due:** 2026-06-11 (Net 14)
- **Status:** paid (2026-06-09)
- **Terms:** Net 14
- **Notes:** Paid on time, quick turnaround

## Retainers

| Client | Monthly | Status | Last Paid | Next Due |
|--------|---------|--------|-----------|----------|
| ABC Real Estate | $1,500 | active | 2026-05-01 | 2026-06-01 |
```

---

## Payment Terms & Strategy

**Common options for automation projects:**

- **50/50 split** — Half upfront to start, half on completion (best for you, lower risk)
- **Net 30** — Full invoice due 30 days after send (standard for larger projects)
- **Upfront** — Full payment before you start (great for small projects or new clients)
- **Monthly retainer** — $X per month for ongoing optimization and support (recurring revenue)

**Recommendation for your business:**
- Projects < $2,500: Upfront or 50/50
- Projects $2,500-$10,000: 50/50 split
- Projects > $10,000: 50% deposit, 25% mid-build, 25% completion
- Retainers: Monthly invoice, due first of month

---

## Retainer Invoicing

After a project closes, offer ongoing support:

- **Optimization Retainer:** $500-$2,000/month
  - Monitor automations
  - Fix issues
  - Quarterly optimization
  - Ad-hoc consulting

Create recurring invoice:
- Template: `[Client] - Monthly Retainer - [Month]`
- Amount: agreed monthly rate
- Due: 1st of each month
- Auto-generate on the 1st

---

## Payment Collection Best Practices

**Invoice timing:**
- Send within 24 hours of proposal acceptance
- For upfront payment, send immediately
- For splits, send first payment invoice before starting work

**Follow-up:**
- Overdue by 3 days: Friendly reminder email
- Overdue by 7 days: Call or direct message
- Overdue by 14 days: Stop work until payment received (with notice)

**Incentives:**
- 2% discount for payment within 7 days (builds goodwill)
- Late fee after 30 days (protects your cash flow)

---

## Linking to Your Workflow

When you create an invoice:
1. It references the proposal and prospect from the wiki
2. `/proposal [prospect] [brief]` creates the proposal
3. `/invoicing create [prospect] [amount]` turns it into an invoice
4. Once paid, update prospect status to `closed-won`

Revenue flows: prospect → proposal → invoice → payment → logged in wiki/log.md

---

## Financial Health Checks

Review monthly in `wiki/overview.md`:

- Total revenue this month (invoiced)
- Total collected (actually paid)
- Outstanding (not yet paid)
- Collection rate (% of invoices paid on time)
- Average client value

Goal: 90%+ of invoices collected within 30 days. If worse, tighten payment terms.
