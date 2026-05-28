---
description: First-time setup. Asks three questions and personalizes this repo.
---

# /onboard

Welcome the user and walk them through three-question first-time setup.

## Idempotency check

First, read `CLAUDE.md` and look for the substring `{{USER_NAME}}`.

- **If `{{USER_NAME}}` is NOT present:** the repo is already onboarded. Reply with exactly: "This repo is already onboarded. To re-onboard, manually reset the `{{PLACEHOLDERS}}` in `CLAUDE.md` and run `/onboard` again." Then stop.
- **If `{{USER_NAME}}` IS present:** continue to the interview.

## Interview

Ask these three questions, one at a time, waiting for the user's reply before asking the next. Be brief - no preamble between questions.

1. "What's your full name?"
2. "What are you building? Give me one sentence."
3. "What's your single top priority right now?"

Store the answers as `userName`, `userBusiness`, `userTopPriority`.

## Write the answers

Compute `userSlug` = the user's full name lowercased, with spaces replaced by `-`, and any non-alphanumeric/non-hyphen characters removed. Example: "Jane Smith Jr." -> "jane-smith-jr".

Compute `today` = the current date in `YYYY-MM-DD` format.

Perform these edits in order:

1. **Edit `CLAUDE.md`:** use `Edit` with `replace_all: true` for each of these three substitutions:
   - `{{USER_NAME}}` → `userName`
   - `{{USER_BUSINESS}}` → `userBusiness`
   - `{{USER_TOP_PRIORITY}}` → `userTopPriority`

2. **Edit `wiki/overview.md`:** same three substitutions with `replace_all: true`. Also update the frontmatter `updated:` field to `today`.

3. **Create `wiki/entities/{userSlug}.md`** with this exact content (substituting values):

   ```markdown
   ---
   title: {{userName}}
   type: entity
   tags: [person, owner]
   created: {{today}}
   updated: {{today}}
   sources: 0
   ---

   # {{userName}}

   ## Who

   {{userBusiness}}

   ## Top Priority

   {{userTopPriority}}

   ## Open Questions

   _To be filled in as questions accumulate._
   ```

4. **Edit `wiki/index.md`:** replace the `_None yet. Run `/onboard` to create your first entity page._` line under "Entities - People" with:

   ```
   - [[{{userName}}]](entities/{{userSlug}}.md) - owner (updated: {{today}})
   ```

5. **Append to `wiki/log.md`:** add this block to the end of the file:

   ```
   ## [{{today}}] onboard | First-time setup
   - User identified as {{userName}}
   - Created wiki/entities/{{userSlug}}.md
   - Seeded wiki/overview.md and wiki/index.md
   ```

## Confirm

Reply with exactly:

"You're set up. Try `/wiki update` after your next working session to start building out the brain."

Then stop.
