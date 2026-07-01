# Deployment Security

Before deploying any automation to a scheduled trigger, webhook, cloud cron, or any target that will run unattended: ask for an explicit security review first — check for exposed API keys/secrets, unprotected webhook endpoints, missing signature verification, and anything that would be a problem if the code or its config were made public.

## Do Not
- Commit secrets to a repo, chat, or a workflow markdown file — secrets live in `.env` only, per the WAT framework in the root CLAUDE.md
- Deploy something with a public webhook and no auth/signature check without flagging it first
