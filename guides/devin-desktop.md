# Guide 17 — Devin Desktop

**Goal:** the agent-native editor — every surface of Devin in one window: cloud sessions, local sessions (Devin Local), Bots, and a real IDE around them.
**Level:** start here
**Sources:** [Desktop changelog](https://docs.devin.ai/desktop/changelog) · [CLI changelog](https://docs.devin.ai/cli/changelog/stable)

## What it is

Devin Desktop is the Windsurf-based editor where all of Devin's surfaces live side by side. Three things to tell apart:

| Surface | Where it runs | Use it for |
| --- | --- | --- |
| Cloud session | Devin's machine, in your org | Unattended tasks, parallel work, PRs for review |
| Devin Local | A background process on your machine | Hands-on edits in your checked-out repo |
| Bot | Persistent agent (see guides 1–5) | An outcome to own — available in Desktop since v3.14 |

## Agent Command Center

The Command Center is the session hub — not an editor:

- **Tabs** (v3.13.4): several sessions and pages open in one window, each tab with its own Back/Forward history — treat it like a browser for your fleet.
- **Session header "..." menu**: the session's MCP servers — toggle one, or re-authenticate it, per session.
- **Devin Review**: the PR walkthrough (diff, bugs, test recording) opens as a page in the same window.

## Devin Local — the daemon change

Since v3.13.4 (Desktop) / v3000.13.4 (CLI), a local session runs in a **background process**, not inside the window that started it:

- Closing or reopening Devin Desktop — or the CLI — does **not** stop a session.
- The same session opens in **several clients at once**: desktop window and terminal both attached, each showing output and questions.
- `devin daemon` starts/stops/checks the process; it exits ~10 min after its last session and client leave.
- `--process-model` chooses `daemon` vs `in-process`; `process_model` in `config.json` or `/config` sets the default.
- `devin ls`, `devin -r` and `/resume` open a **session monitor** — sessions by last update, with status, directory and message count.

The practical consequence: local work is now durable. Start a long task, close the laptop, reattach from another client — the session kept going.

## IDE mode

- The embedded IDE saves on **Cmd/Ctrl+S** (no auto-save); unsaved tabs show a dot.
- In a Devin Local browser preview, **picking a page element or console output adds it to the composer** — point at the bug instead of describing it.
- The Files tab previews PDFs, renders CSV/TSV as tables, and plays media.

## Two workflows worth copying

**1. Local → cloud → local.** Work in Devin Local, hit the wall (needs org tools, more parallelism, longer than your laptop stays open), `/handoff` to cloud, review the PR back home. The daemon makes both halves resumable.

**2. One window, many surfaces.** Command Center for the fleet view, Local for the repo you're in, a Bot for the outcome you don't want to babysit — Desktop is the only place all three share a window.

## Verify it

- [ ] A Devin Local session survives closing and reopening Desktop
- [ ] The same local session attached from Desktop and from `devin` CLI at once
- [ ] `devin ls` opened the session monitor and joined a running session
- [ ] A Bot created from its Desktop chat answered in that chat

## Pitfalls

- **"Not authorized to use the CLI"** — accounts with Desktop access but no CLI access hit this on Devin Local sign-in (fixed in v3.14.30825; update if you see it).
- **Tabs are per-window state.** An action in a session page only acts on its tab — but the *session* is shared, so a second client attaching sees the same live session, not a copy.
- **Managed machines:** enterprise admins control Desktop settings via device policies (e.g. `DetectProxy` for the language server) — check with IT before debugging the network yourself.

## Knowledge check

1. What changed about local sessions in v3.13.4? *(They run in a background process — closing the app no longer stops them, and multiple clients can attach to the same session.)*
2. When do you pick Devin Local over a cloud session? *(When you want hands-on edits in your checked-out repo with your local context; hand off to cloud for scale or org integrations.)*
3. What lives in the session header's "..." menu? *(The session's MCP servers — toggle or re-authenticate them per session.)*

## Sources

- [Devin Desktop changelog](https://docs.devin.ai/desktop/changelog) — v3.13.4 (tabs, background local sessions), v3.14 (Bots in Desktop)
- [Devin CLI changelog](https://docs.devin.ai/cli/changelog/stable) — v3000.13.4: `devin daemon`, `--process-model`, session monitor
- Related: [Guide 12 — Devin CLI & extensibility](devin-cli.md) · [Guide 1 — Your first Bot](bots-101-first-bot.md)
