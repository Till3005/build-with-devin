# Guide 3 — Scheduled-sentinel Bot

**Goal:** a Bot that owns a recurring quality check — runs it on a schedule, triages failures, traces them to the cause, and ships fixes.
**Level:** intermediate
**Source deployment:** Cognition's **Layout Bot** — watches layout-shift regression on the Devin web app. Every 3 hours it builds production `main`, simulates first/repeat/delayed-request visits, and ships fixes. **159 PRs in 3 weeks; lag −70%.**
**Sources:** [launch post](https://devin.ai/blog/introducing-devin-bots) · [Automations docs](https://docs.devin.ai/product-guides/automations)

## The pattern

Some work is never done — it recurs on a clock: performance budgets, visual regression, dependency freshness, secret scans, uptime. A sentinel Bot owns *the check itself*, not just the fixes: it keeps the check working as the codebase changes, filters noise, and opens a fix only when the regression is real.

```text
cron ──► Bot wakes ──► run check under realistic conditions
                           │
              pass ────────┴──────── fail
               │                       │
             quiet            rerun to filter flakes
                                       │
                              trace to introducing PR
                                       │
                          fix PR + before/after evidence
```

## Prerequisites

- A check that can run on the Bot's machine (build, test suite, Lighthouse, custom script)
- Devin Bot created (Guide 1) or an Automation (Guide 6) — both work; a Bot adds judgment between runs

## Step 1 — The outcome prompt

Reconstructed from the Layout Bot's documented behavior:

```text
Your job is to keep <surface> from <regressing>.

Watch <check/channel>, where <the check> posts every <interval>. Take over
that check and keep it working as the code changes. When something
regresses: rerun to rule out flakiness, trace the regression to the PR
that introduced it, and open a fix PR with before/after evidence.
```

Examples of the `<check>` slot, all seen in real deployments:

- layout-shift measurement across first/repeat/delayed requests (Layout Bot)
- p95 latency on your 5 slowest endpoints (Latency Optimizer template)
- `npm audit`/CVE sweep (Code Health Engineer template)
- dead-code detection (Code Reaper template)

## Step 2 — Schedule it

Ask the Bot in chat:

```text
Run this check every 3 hours on a schedule.
```

The Bot proposes an automation; you approve once. (Guide 6 covers hand-built automations if you'd rather wire the cron yourself.) Manage it later under the Bot's Settings → Automations.

## Step 3 — Realistic conditions matter

The Layout Bot's check isn't one run — it simulates **first visit, repeat visit, and individually delayed requests**, because the regression it hunts only shows under specific load shapes. Encode your equivalent:

- Which environment — the Bot builds production `main` on its own VM, not a dev server
- Which inputs — cold vs. warm cache, seeded data, realistic request ordering
- Which threshold — a number, not "feels slower"

## Step 4 — Noise discipline

Two rules keep a sentinel from crying wolf:

1. **Rerun before acting** — the Layout Bot reruns flaky-looking results before treating them as real. Write it into the prompt: *"rerun any failed check once before acting on it."*
2. **Trace before fixing** — each regression gets traced to the introducing PR. A fix without a cause is a guess.

## Step 5 — Evidence in every fix

Each of the 159 PRs carries **before/after video**. Equivalent evidence for your check:

| Check | Evidence in the fix PR |
| --- | --- |
| Layout/visual | Screen recording or screenshots, before vs. after |
| Latency | Timing numbers, same measurement both ways |
| Dead code | Why the code is unreachable |
| Dependencies/CVEs | The advisory + the diff that resolves it |

## Verify it

- [ ] Automation exists and fires on the cron you set (Settings → Automations shows runs)
- [ ] A seeded regression produces a fix PR with before/after evidence
- [ ] A flaky run produces a rerun, not a fix
- [ ] The check itself gets maintained — when the app changed under it, the Bot updated the check

## Pitfalls

- **Owning fixes but not the check.** If your check breaks and nobody notices for a week, the Bot owned the wrong thing — the prompt must assign the check itself.
- **Cron without judgment.** A bare scheduled automation can run the check; a Bot decides whether a failure is real. Use a bare automation only for checks that need zero triage (Guide 6).
- **Alert-only output.** A sentinel that reports "regression found" to a channel creates work for humans. The deployment's value is that it *fixes* — hold it to that.

## Sources

- [Introducing Devin Bots](https://devin.ai/blog/introducing-devin-bots) — Layout Bot mechanics and numbers
- [Automations — docs](https://docs.devin.ai/product-guides/automations) — schedules, triggers, conditions
- Related: [Guide 6 — Event-driven automations](automations-101-event-driven.md) for the non-Bot version of this loop
