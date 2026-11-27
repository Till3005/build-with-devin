# Guide 16 — Skills & plugins: the post-playbook packaging layer

**Goal:** encode your org's repeatable procedures as `SKILL.md` files so every session and Bot follows them — and package/share them across repos with plugins.
**Level:** intermediate · the layer that replaced playbooks
**Sources:** [docs.devin.ai/product-guides/skills](https://docs.devin.ai/product-guides/skills) · [release notes](https://docs.devin.ai/release-notes/overview) · complements [Guide 9](playbooks-and-knowledge.md)

## Why skills are the layer that matters now

Playbooks are moving to Skills: accounts migrate one at a time, and new accounts (from Oct 24, 2026) get Skills only — each playbook becomes a skill with the same org/enterprise scope. Skills also follow the open **Agent Skills** standard, so the same files work across other coding agents. Everything you knew about writing playbooks transfers; the file format and discovery model are what changed.

| Artifact | Lives in | Best for |
| --- | --- | --- |
| Knowledge | Customize page / repo notes | Standing context — facts Devin can't know |
| Bot instructions | The Bot | Job law for one employee |
| Skill | `SKILL.md` in repo, or a plugin | A named, invocable procedure |
| Rule | Plugin | Always-on constraint ("never force-push") |
| Hook | Plugin | Deterministic enforcement around tool calls |

## Step 1 — Where skills live

Two discovery sources, both automatic:

1. **Repositories** — commit `SKILL.md` files; Devin scans all ten vendor paths in every connected repo: `.agents/skills/` (recommended), `.devin/skills/`, `.github/skills/`, `.claude/skills/`, `.cognition/skills/`, `.windsurf/skills/`, `.cursor/skills/`, `.codex/skills/`, `.codeium/skills/`, `.kiro/skills/`. Repo skills are branch-versioned — a mid-session clone is scanned when it finishes.
2. **Plugins** — a plugin bundles skills + rules + MCP servers + hooks, installed at personal, organization, or enterprise scope; its skills are in context before any repo clones.

## Step 2 — The SKILL.md contract

```markdown
---
name: test-before-pr
description: Run the dev server and verify pages before any frontend PR.
argument-hint: <environment>
triggers: ["user"]
allowed-tools: read, grep, glob
permissions:
  allow: ["Exec(npm run *)"]
---

## Setup
1. `docker-compose up -d postgres` && `npm run dev`
## Verify
1. Open each page touched by the diff
2. Screenshot at 1280px and 375px
```

Frontmatter that changes behavior:

- **`description`** — the only thing Devin sees at session start; it decides auto-invocation. Write it as a trigger ("verify pages before any frontend PR"), not a summary.
- **`triggers: ["user"]`** — disables auto-invocation; use it for anything destructive (deploys, migrations).
- **`argument-hint`** + `$ARGUMENTS`/`$1` — parameterize: `@skills:deploy staging`.
- **`allowed-tools` / `permissions`** — pre-approve or gate tools while the skill runs.

## Step 3 — Invocation paths

- **Automatic:** Devin matches the task against `description` and loads the body into context for the rest of the session.
- **Explicit:** `@skills:<name> [args]` in a session or Bot message — the reliable way to share a procedure across a team.
- **Suggested:** after Devin learns something (how to boot your stack), it proposes a `SKILL.md` in the session timeline with a **Create PR** button — accept it; this is how skill libraries grow without writing sessions.

## Step 4 — Growing the library

- Run two sessions in parallel against a new skill; gaps surface in minutes.
- When you correct Devin mid-session, add the correction to the skill so the next session starts smarter.
- Promote repo-proven skills into an org plugin so every repo gets them without copying.

## Walkthrough — a repo skill invoked for real, on Devin CLI v3000.14 (swe-2-flash-medium)

Step 3's *explicit* path, end-to-end: a `coverage-check` skill committed at `.devin/skills/coverage-check/SKILL.md` in a demo repo, then invoked in a fresh session. Discovery works exactly as documented — typing `/` surfaced the skill by name, with its `description` as the autocomplete blurb.

**Video (60 s, silent):** SKILL.md → slash autocomplete → `Invoked skill coverage-check` → approval → report.

[![The skill's report — per-function coverage tables for app.py and orders.py](https://till3005.github.io/built-with-devin/assets/guides/skills-and-plugins/walkthrough-poster.webp)](https://till3005.github.io/built-with-devin/assets/guides/skills-and-plugins/walkthrough.mp4)

![1. The skill on disk — frontmatter name/description, then a numbered procedure](https://till3005.github.io/built-with-devin/assets/guides/skills-and-plugins/step1-skill-file.webp)
*1. The skill on disk — `.devin/skills/coverage-check/SKILL.md`: frontmatter `name`/`description`, then a numbered procedure*

![2. Typing `/` lists the skill — name + description are the autocomplete entry](https://till3005.github.io/built-with-devin/assets/guides/skills-and-plugins/step2-slash-autocomplete.webp)
*2. Typing `/` lists the skill — name + `description` are exactly what discovery loads*

![3. `Invoked skill coverage-check` — the first command already waits on an Allow](https://till3005.github.io/built-with-devin/assets/guides/skills-and-plugins/step3-invoked.webp)
*3. `Invoked skill coverage-check` — its first command still needs an Allow*

![4. The procedure runs verbatim — unittest, then read every source and test file](https://till3005.github.io/built-with-devin/assets/guides/skills-and-plugins/step4-coverage-report.webp)
*4. The procedure runs verbatim — `python3 -m unittest -v`, then reads app.py, orders.py, both test files*

![5. Result: full coverage — per-function tables naming every branch; no files modified, no commits](https://till3005.github.io/built-with-devin/assets/guides/skills-and-plugins/step5-full-coverage.webp)
*5. Result: full coverage — every branch accounted for, exactly the report the SKILL.md asked for*

## Govern plugins and MCP access

- **Offered vs. Required is an admin choice.** Org and enterprise admins can mark a marketplace plugin as **Offered** instead of **Required**. Required plugins are part of the managed baseline; Offered plugins are optional for members. Do not use Required for a convenience bundle — it expands the managed baseline for every member.
- **Use the narrowest MCP approval.** MCP tool approval cards now include **Allow for this session**. Prefer it when the task needs a tool repeatedly but the permission should die with the session; reserve broader approval for tools you have already audited.
- **API keys belong in secrets.** Blank headers on API-key marketplace MCP servers are bound to secrets, and unused secrets are flagged. Keep raw keys out of plugin config, prompts, and chat.
- **Automatic does not mean unauthenticated.** New custom MCP servers start with **Automatic** authentication selected. Verify what the server actually negotiates before connecting it to production scopes.

## Verify it

- [ ] A fresh session lists your skill by name (name + description load at start)
- [ ] `@skills:<name>` runs the procedure verbatim, with arguments substituting
- [ ] A `triggers:["user"]` skill never fires on its own
- [ ] A plugin-installed skill is available before the repo finishes cloning

## Pitfalls

- **Over-specifying.** Specific commands/flags/strings are the point; rigid prose isn't. Skills that narrate every decision remove Devin's ability to adapt mid-run.
- **Writing the body but not the description.** Auto-invocation keys on the description; a great body with a vague description never fires.
- **Letting destructive skills auto-invoke.** Deploys and migrations belong behind `triggers:["user"]` or an explicit `permissions.ask` gate.
- **Keeping secrets in skills.** A skill is read by every session in scope — credentials go in the secrets store, referenced as `$VAR`.

## Knowledge check

1. Why does `description` matter more than the skill body? *(It's the only text loaded at session start — it drives auto-invocation; the body loads only after the skill is chosen.)*
2. When should a procedure be a plugin skill rather than a repo skill? *(When every repo/session in a scope needs it — plugins load before cloning and can't drift per-branch.)*
3. How do you make a skill safe for destructive steps? *(`triggers:["user"]` for explicit-only invocation, plus `permissions.ask` on the dangerous tool matchers.)*

## Sources

- [Devin Skills docs](https://docs.devin.ai/product-guides/skills) — file format, discovery paths, frontmatter
- [Release notes](https://docs.devin.ai/release-notes/overview) — playbooks→Skills migration, Customize page
- Related: [Guide 9 — Playbooks & knowledge](playbooks-and-knowledge.md) (the context layer skills sit beside)
- [Release notes — Nov 23, 2026](https://docs.devin.ai/release-notes/overview) — Offered plugins, session-scoped MCP approval, secret-bound API-key headers, Automatic auth default
