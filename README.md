# Adar Realty Studio

A Claude Code starter for builders. Clone, open in VS Code, run `/onboard`, and you have a personalized executive assistant with a persistent second brain.

Built by [Woodworks Realty Studio](https://woodworksrealtystudio.com).

---

## Install

1. Install Claude Code: https://claude.ai/code
2. Install VS Code and the Claude Code extension
3. Clone this repo:
   ```bash
   git clone git@github.com:woodworksrealtystudio-stack/woodworks-os.git
   cd woodworks-os
   ```
4. Open the folder in VS Code
5. Open the Claude Code panel: `Cmd+Shift+P` → "Claude Code: Open"
6. In Claude, run:
   ```
   /onboard
   ```

That's it. Claude will ask you three questions and personalize the repo.

---

## What's inside

```
woodworks-os/
├── CLAUDE.md                    # router: identity, rules, links to the wiki
├── .claude/
│   ├── rules/communication-style.md
│   ├── skills/wiki/SKILL.md     # bundled wiki skill
│   └── commands/onboard.md      # the /onboard slash command
├── wiki/
│   ├── CLAUDE.md                # wiki schema
│   ├── overview.md              # current picture, one page
│   ├── index.md                 # catalog of all pages
│   ├── log.md                   # append-only operation log
│   ├── entities/                # people, companies, products
│   ├── concepts/                # ideas, frameworks, strategies
│   ├── sources/                 # ingested videos, podcasts, files
│   └── synthesis/               # analyses, decisions
└── projects/                    # your work, one folder per project
```

---

## Daily use

After any working session where something meaningful happened, run:

```
/wiki update
```

This pulls what you and Claude just discussed into the wiki so future sessions remember it.

When you drop a file, paste a transcript, or point to a URL:

```
/wiki ingest [source]
```

When you have a question:

```
/wiki [your question]
```

---

## Make it your own

This repo is the shared starter. To run it as your own private repo with its own history:

```bash
rm -rf .git
git init
git add .
git commit -m "initial commit"
# create a new private repo on your own GitHub, then:
git remote add origin git@github.com:yourname/your-os.git
git push -u origin main
```

---

## License

MIT. See [LICENSE](./LICENSE).
