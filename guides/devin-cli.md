# Guide 12 — Devin CLI & extensibility

**Goal:** the local-terminal Devin — run the agent on your machine, hand work to Devin Cloud, and extend it with skills, rules, plugins, hooks, and subagents.
**Level:** intermediate
**Sources:** [Devin CLI docs](https://docs.devin.ai/cli/index.md) — [introducing](https://docs.devin.ai/cli/introducing-devin-cli.md), [essential commands](https://docs.devin.ai/cli/essential-commands.md), [extensibility](https://docs.devin.ai/cli/extensibility/index.md)

## What it is

Devin CLI is a coding agent that lives in your terminal and connects to Devin Cloud. Two working modes, and the power is in moving between them:

- **Local** — it edits your checked-out repo on your machine
- **Cloud** — `devin --cloud` creates/steers/resumes cloud sessions. Run `/handoff` in a local session to send the task to Devin Cloud. Run it in the cloud session in the CLI to fetch its PR branch, switch your checkout to that branch, and start a local session on it. (`/open` opens the session in the web app or Devin Desktop.)

```text
local repo ──/handoff──► Devin Cloud session ──/handoff──► local repo
     ▲                        │
     └──── devin ssh / forward (inspect its VM) ────┘
```

## The pieces that matter

| Surface | What it does |
| --- | --- |
| `devin ssh` / `devin forward` | SSH into a cloud session's VM, forward its ports, `scp` files |
| Subagents | Delegate to independent agents (foreground/background) with own profiles and permissions |
| Models | Adaptive routing picks the model per task; Fusion pairs a frontier lead + cheap sidekick |
| ACP | Runs inside JetBrains, Zed, Xcode via the Agent Client Protocol |
| Daemon | Since v3000.13.4 local sessions run in a background process — close the app, reattach from any client (`devin daemon`, `devin ls` session monitor) |

The daemon also rewrote multi-client semantics: a session open in another terminal or editor is no longer locked — a second client *joins* it, and every client sees its output and questions. `devin daemon start|stop|status` manages the process (it exits ~10 min after the last session and client leave); `--process-model daemon|in-process` picks per launch, `process_model` in `config.json` or `/config` sets the default. One recorded exception: in our Desktop v3.14.30825 run a second Desktop window still got a lock banner with *Force open* — join held CLI-side (Guide 17, frame 9).

## The extensibility stack

This is where teams make the CLI *theirs* — same layering as Guide 9, applied locally:

| Layer | File/mechanism | Use for |
| --- | --- | --- |
| Rules | `AGENTS.md` / rules files | Always-on instructions every session reads |
| Skills | `SKILL.md` | Reusable procedures — slash-invoked or agent-chosen, with own permissions/`allowed-tools` |
| Plugins | plugin manifest | Bundle skills + rules + hooks + MCP servers; share through a **team marketplace** |
| Hooks | lifecycle hooks | Shell/LLM logic on `PreToolUse`, `PostToolUse`, `SessionStart`, `SessionEnd`… — block or rewrite tool calls, inject context |
| MCP | MCP config | External tool servers (stdio / HTTP / SSE) |

**Import path:** `read_config_from` imports settings from Cursor, Windsurf, Claude Code, Copilot, Codex, Kiro, OpenCode, Zed — migration is one flag, not a rewrite.

## Three workflows worth copying

**1. Local → cloud fan-out.** Start a task locally. When it needs the cloud, run `/handoff` to keep it going on Devin's machine. Once the cloud session has a PR, open or resume that session in the CLI and run `/handoff` there to continue locally on its PR branch.

**2. Skills as memory.** Turn any repeated procedure (Guide 11's migration skill, a hotfix runbook, a release cut) into a `SKILL.md` — the CLI docs note feeding *successful session transcripts* back into skills to close gaps. Plugins package and share them to the whole team.

**3. Guardrails via hooks.** `PreToolUse` hook that blocks `rm -rf` patterns or forces review on migrations — enforcement lives in the hook, not in hoped-for model behavior.

## Walkthrough — recorded on Devin CLI v3000.14

A real run, not a mock-up: Devin CLI `3000.14.30821` on Linux, Pro plan, a throwaway `demo-repo` with an `app.py`. Models: `swe-2-flash-high` for the edit task, `swe-2-high` for the skill run (both SWE-2 tiers are listed as **Free** in `devin models`).

**Video (67 s, no audio):** the whole session below, from login to the handoff error.

[![2. Prompt: add a subtract function and a test. Devin shows the diff and asks — Allow, Accept edits mode, Bypass mode or Deny](https://till3005.github.io/built-with-devin/assets/guides/devin-cli/walkthrough-poster.webp)](https://till3005.github.io/built-with-devin/assets/guides/devin-cli/walkthrough.mp4)

![1. devin --model swe-2-flash-high — login confirmed, then the workspace trust prompt](https://till3005.github.io/built-with-devin/assets/guides/devin-cli/step1-login-trust.webp)
*1. devin --model swe-2-flash-high — login confirmed, then the workspace trust prompt*

![2. Prompt: add a subtract function and a test. Devin shows the diff and asks — Allow, Accept edits mode, Bypass mode or Deny](https://till3005.github.io/built-with-devin/assets/guides/devin-cli/step3-permission-prompt.webp)
*2. Prompt: add a subtract function and a test. Devin shows the diff and asks — Allow, Accept edits mode, Bypass mode or Deny*

![3. Result: app.py edited, test_app.py written; pytest was missing, so Devin ran the tests with python -c and said so](https://till3005.github.io/built-with-devin/assets/guides/devin-cli/step4-task-done.webp)
*3. Result: app.py edited, test_app.py written; pytest was missing, so Devin ran the tests with python -c and said so*

![4. /model — Adaptive, Fusion (lead + sidekick) and model families; SWE-2 Flash shows FREE, no quota consumed](https://till3005.github.io/built-with-devin/assets/guides/devin-cli/step5-model-picker.webp)
*4. /model — Adaptive, Fusion (lead + sidekick) and model families; SWE-2 Flash shows FREE, no quota consumed*

![5. /exit prints a devin -r <slug> resume hint; devin ls is the local session monitor](https://till3005.github.io/built-with-devin/assets/guides/devin-cli/step6-devin-ls.webp)
*5. /exit prints a devin -r <slug> resume hint; devin ls is the local session monitor*

![6. devin --cloud, then /list-sessions — the account's cloud sessions, newest first](https://till3005.github.io/built-with-devin/assets/guides/devin-cli/step8-cloud-sessions.webp)
*6. devin --cloud, then /list-sessions — the account's cloud sessions, newest first*

![7. .devin/skills/review/SKILL.md runs as /review on swe-2-high and reviews the uncommitted changes](https://till3005.github.io/built-with-devin/assets/guides/devin-cli/step10-skill-result.webp)
*7. .devin/skills/review/SKILL.md runs as /review on swe-2-high and reviews the uncommitted changes*

![8. Pitfall: /handoff fails in a repo with no git remote — "Handoff only works from git repos with a remote configured"](https://till3005.github.io/built-with-devin/assets/guides/devin-cli/step11-handoff-no-remote.webp)
*8. Pitfall: /handoff fails in a repo with no git remote — "Handoff only works from git repos with a remote configured"*

The skill used in step 7, verbatim:

```markdown
---
name: review
description: Review recent changes in this repo and report issues
---

Review the working tree's uncommitted changes. List each changed file,
summarize what it does, and flag anything that looks wrong or risky.
Keep it under 10 lines.
```

## Verify it

- [ ] `devin` runs a local session; `devin --cloud` lists/creates cloud sessions
- [ ] A task sent to the cloud with `/handoff` produced a PR; running `/handoff` in that cloud session checked out the PR branch and started a local session
- [ ] A `SKILL.md` invoked by slash command ran your procedure
- [ ] (Enterprise) team marketplace serves your plugin to another member

## Pitfalls

- **Local for parallel work.** The CLI is one agent in your terminal — for parallel slices use cloud sessions or a Bot; the CLI is the *hands-on* surface.
- **Rules sprawl.** `AGENTS.md` + project rules + global rules interact by precedence — keep each rule in exactly one layer or they fight.
- **`/handoff` needs a remote.** In a repo with no git remote it fails immediately — push the repo somewhere Devin Cloud can clone first.

## Knowledge check

1. When do you use `/handoff` to Devin Cloud instead of finishing locally? *(When the work needs cloud-scale parallelism, org tools, or runs longer than your laptop stays open.)*
2. What's the difference between a skill, a rule, and a plugin? *(A skill is a task procedure, a rule is standing context, a plugin is the package that ships both plus hooks.)*
3. Why does hooks + subagents matter for team adoption? *(Hooks enforce org policy at every CLI session; subagents let one operator run a fleet — the two scale in opposite directions.)*

## Sources

- [Devin CLI docs](https://docs.devin.ai/cli/index.md) — quickstart, commands, cloud integration, extensibility, ACP, models
- Related: [Guide 9 — Playbooks & knowledge](playbooks-and-knowledge.md) (same conventions layer, org-wide)
