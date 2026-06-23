---
description: Create invoices, track payments, and manage billing for projects
---

# /invoicing

Create invoices, track payments, and manage your revenue. All invoices live in the wiki.

Read `.claude/skills/invoicing/SKILL.md` for full operations and guidelines, then follow the instructions there based on what the user asks for.

Supported operations:
- `/invoicing create [prospect] [amount] [description]` — Create an invoice
- `/invoicing send [invoice number]` — Mark invoice as sent
- `/invoicing paid [invoice number]` — Record payment received
- `/invoicing follow-up [days]` — Show overdue invoices
- `/invoicing dashboard` — Financial snapshot (revenue, outstanding, overdue)
