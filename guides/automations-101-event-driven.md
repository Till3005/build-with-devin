# Guide 6 — Event-driven automations

**Goal:** wire external events — Slack, Teams, GitHub, Linear, Jira, PagerDuty, cron, webhooks — to Devin sessions that start themselves.
**Level:** start here (platform guide) · **Time:** ~20 minutes
**Source:** [Automations docs](https://docs.devin.ai/product-guides/automations) · [official video walkthrough](https://www.youtube.com/watch?v=6xxKtIpgOyE)

## The anatomy

Every automation is four parts:

| Part | What it does |
| --- | --- |
| Trigger | The event that fires it — a Slack message, a failed CI run, a cron tick, an HTTP webhook |
| Conditions | Optional filters — only label `bug`, only this repo, only messages containing `/devin` |
| Preflight check | Optional LLM filter or script that runs *after* a match, before actions — can skip the event or split it into work items |
| Action | What runs: start a session, message an existing session, triage monitor, or email notification |

## Trigger catalog

| Source | Fires on | Canonical use |
| --- | --- | --- |
| Slack | New message, reaction added, user-group mention | Triage `#incidents`; 🚨 reaction → investigate |
| Microsoft Teams | Message, reaction | Answer bug reports in the thread they were posted |
| GitHub | Issue, issue comment, PR, PR review, check run, push | Auto-fix failing CI; `/devin` comment → session |
| GitLab | MR, MR comment, issue, push, pipeline | Fix failing pipelines |
| Linear | Issue created/labeled/status/priority/assigned/moved | Implement tickets when assigned to Devin |
| Jira | Issue created/updated/labeled/status/assigned/commented | Same, Jira-shaped |
| Pylon | Issue created/tagged/status | Customer-bug triage |
| PagerDuty | Incident triggered/acknowledged/resolved | Investigate high-urgency incidents on fire |
| Schedule | Cron or one-time | Daily Sentry sweep, weekly dep updates, nightly smoke tests |
| Webhook | Any HTTP POST | Anything else — Datadog, Sentry, your own systems |

Multiple triggers on one automation act as OR — e.g. fire on *either* a GitHub CI failure *or* a Slack reaction.

## Recipe 1 — `/devin` on any issue

The most-deployed trigger in the wild:

```text
Trigger:   GitHub → issue comment, repo = your/repo
Condition: comment body starts with "/devin"
Action:    Start session — prompt includes the event payload
```

Result: anyone on the team comments `/devin investigate this` on an issue, and a session picks it up with the full thread as context.

## Recipe 2 — CI failure self-repair

```text
Trigger:   GitHub → check run, repo = your/repo
Condition: conclusion = failure
Action:    Start session: "CI check <name> failed on this commit.
            Diagnose the failure from the logs, fix it, and push to
            the same branch."
```

The event payload carries the failing check + commit into the session — no human copy-paste.

## Recipe 3 — Scheduled sweep

```text
Trigger:   Schedule → daily 09:00
Action:    Start session: "Sweep yesterday's Sentry issues in
            <project>. File the top 3 by impact as tickets and
            start the most actionable one."
```

Daily hygiene loops (Sentry sweeps, dependency updates, smoke tests) are the highest-ROI automations — they turn "someone should check" into "it's checked."

## Action types, choosing between them

| Action | Use when |
| --- | --- |
| Start session | The default — each event gets a fresh machine and context |
| Message session | A long-lived session maintains state — feed events into it (the seed of a Bot) |
| Triage Devin | A persistent Devin watches a whole Slack channel and spawns child investigations (see Devin Oncall for incidents) |
| Email notification | Just tell you it ran |

**Automation vs. Bot:** automations are dumb pipes — event in, session out. A Bot adds memory, judgment, and multi-session planning around the same triggers. Start with automations; graduate to a Bot when the work needs follow-through (Guides 2–5).

## Build it

Three creation paths on the Automations page:

1. **Create** — the blank editor: pick trigger → conditions → action
2. **Template** — the gallery of pre-configured automations for common workflows
3. **Generate with Devin** — describe it in English (*"when a CI check fails on my-org/my-repo, have Devin fix it and push to the same branch"*), review the generated config

Notes that bite people:

- Slack triggers need Devin invited to the channel **and** your personal Slack connected in Settings → Connections
- Private Teams channels only fire on @mention
- A GitHub trigger must name a specific repo
- Manage automations declaratively with the **Terraform provider** if you're running many

## Verify it

- [ ] Fire the trigger manually once (comment `/devin test`, or push a failing commit) and watch a session start with the event payload
- [ ] A non-matching event (wrong label, wrong channel) does nothing
- [ ] The action's output lands where you expected (PR, Slack thread, ticket)

## Sources

- [Automations — docs](https://docs.devin.ai/product-guides/automations)
- [Devin Automations QuickStart (video)](https://www.youtube.com/watch?v=6xxKtIpgOyE)
- Related: [Guide 3 — Scheduled-sentinel Bot](bots-202-scheduled-sentinel.md) for adding Bot judgment on top of a cron
