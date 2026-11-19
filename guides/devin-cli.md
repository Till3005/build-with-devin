# Guide 12 — Devin CLI & extensibility

**Goal:** the local-terminal Devin — run the agent on your machine, hand work to Devin Cloud, and extend it with skills, rules, plugins, hooks, and subagents.
**Level:** intermediate
**Sources:** [Devin CLI docs](https://docs.devin.ai/cli/index.md) — [introducing](https://docs.devin.ai/cli/introducing-devin-cli.md), [essential commands](https://docs.devin.ai/cli/essential-commands.md), [extensibility](https://docs.devin.ai/cli/extensibility/index.md)

## What it is

Devin CLI is a coding agent that lives in your terminal and connects to Devin Cloud. Two working modes, and the power is in moving between them:

- **Local** — it edits your checked-out repo on your machine
- **Cloud** — `devin --cloud` creates/steers/resumes cloud sessions; `/handoff` sends a local task to a cloud Devin, `/open` pulls a cloud session's PR back to your machine

```text
local repo ──/handoff──► Devin Cloud session ──PR──► /open ──► local repo
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

**1. Local → cloud fan-out.** Start a task locally, hit its limits, `/handoff` to a cloud session that keeps going on its own machine — pull the PR back with `/open`.

**2. Skills as memory.** Turn any repeated procedure (Guide 11's migration skill, a hotfix runbook, a release cut) into a `SKILL.md` — the CLI docs note feeding *successful session transcripts* back into skills to close gaps. Plugins package and share them to the whole team.

**3. Guardrails via hooks.** `PreToolUse` hook that blocks `rm -rf` patterns or forces review on migrations — enforcement lives in the hook, not in hoped-for model behavior.

## Verify it

- [ ] `devin` runs a local session; `devin --cloud` lists/creates cloud sessions
- [ ] A `/handoff`'d task completed in the cloud and its PR came back via `/open`
- [ ] A `SKILL.md` invoked by slash command ran your procedure
- [ ] (Enterprise) team marketplace serves your plugin to another member

## Pitfalls

- **Local for parallel work.** The CLI is one agent in your terminal — for parallel slices use cloud sessions or a Bot; the CLI is the *hands-on* surface.
- **Rules sprawl.** `AGENTS.md` + project rules + global rules interact by precedence — keep each rule in exactly one layer or they fight.

## Knowledge check

1. When do you use `/handoff` to Devin Cloud instead of finishing locally? *(When the work needs cloud-scale parallelism, org tools, or runs longer than your laptop stays open.)*
2. What's the difference between a skill, a rule, and a plugin? *(A skill is a task procedure, a rule is standing context, a plugin is the package that ships both plus hooks.)*
3. Why does hooks + subagents matter for team adoption? *(Hooks enforce org policy at every CLI session; subagents let one operator run a fleet — the two scale in opposite directions.)*

## Sources

- [Devin CLI docs](https://docs.devin.ai/cli/index.md) — quickstart, commands, cloud integration, extensibility, ACP, models
- Related: [Guide 9 — Playbooks & knowledge](playbooks-and-knowledge.md) (same conventions layer, org-wide)
