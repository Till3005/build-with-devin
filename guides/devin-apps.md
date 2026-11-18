# Guide 10 — Devin Apps: ship live tools from a chat

**Goal:** describe an internal tool, dashboard, or staging copy — Devin builds it and serves it at a stable URL your team opens by signing in.
**Level:** start here (platform guide) · **Time:** ~10 minutes to first App
**Source:** [Introducing Devin Apps](https://devin.ai/blog/devin-apps) (Nov 13, 2026)

## What it is

A Devin App is a live, private web application hosted directly on Devin's cloud machine. You describe the tool, Devin builds it, your team opens it from a link — no hosting, no deploy pipeline. Because it runs *on* Devin's machine, it can reach your MCPs, integrations, codebase, and its own database (SQLite/Postgres on the same box), and call the Devin API itself.

## Build one

1. Sidebar → **Apps** → describe what the App should do (or pick a prompt template: metrics dashboard, project status, review queue) → **Build with Devin**
2. Devin asks clarifying questions in the session, builds, and puts it online — the Apps page shows its URL, status `Building` until v1 is live
3. **Share** — copy the link; scope it to named people, your org, or your enterprise. Apps are never public; opening one requires a Devin sign-in

You can also say "publish this as an App" inside any session that produced a browser preview.

## Update loop

- **Edit in session** on the App's page → describe the change → Devin builds a new version at the same URL. Every update is a versioned deployment; if a new version fails to start, the previous one keeps serving.
- **Automation-kept-fresh:** wire an automation (Guide 6) to redeploy on a schedule or on branch changes — a dashboard that pulls fresh data every morning is the canonical use.

## How they run (the parts that matter)

- **Hibernation:** Apps build on memory snapshots — the machine sleeps when unused, wakes on open (first load can take a few seconds). Billing follows awake-time.
- **Stack:** anything serving HTTP on a port; DB co-located on the machine.
- **Scale boundary:** one machine — great for internal tools and dashboards, **not** high-traffic production services.

## The three proven uses

| Use | Example |
| --- | --- |
| Internal tools | Admin panels, request forms, approval queues — the shared-spreadsheet killers |
| Dashboards | Metrics/support/sales boards pulling from your own data sources, refreshed on schedule |
| Beta/staging copies | Your real stack (frontend+backend+DB+workers) running on Devin's machine — teammates open a staging copy from a link |

## Verify it

- [ ] App loads at its stable URL after the machine slept (expect a few-second cold start)
- [ ] An edit-in-session change produced a new version at the same URL
- [ ] Share scope is right: a teammate without access is stopped at sign-in

## Pitfalls

- **Production traffic.** One machine, sleeps when idle — don't point users at it; point your team at it.
- **Static thinking.** An App's power is that it *lives in Devin's environment* — wire it to your data/MCPs, or you've built a weaker Vercel.

## Knowledge check

1. What's the difference between a Devin App and a PR preview? *(The App is served live from Devin's machine at a stable URL — stateful, persistent, sign-in gated — not a build artifact.)*
2. Why does 'your team opens it by signing in' matter for internal tools? *(Auth is inherited from the org — no separate login system to build or secure.)*
3. Which class of internal tool fits Apps best? *(Dashboards and staging surfaces where 'good enough now' beats 'perfect later' — the maintenance cost is near zero.)*

## Sources

- [Introducing Devin Apps](https://devin.ai/blog/devin-apps)
- Related: [Guide 6 — Event-driven automations](automations-101-event-driven.md) for scheduled refresh
