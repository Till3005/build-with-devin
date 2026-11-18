# Guide 15 — Living evals from production traces

**Goal:** an eval suite for *your* agent that writes itself — a scheduled Devin that reads real production conversations, rebuilds each failure in a full copy of your system, and opens PRs that add the failure as a regression test.
**Level:** advanced
**Source deployment:** **Rox's Living Evals** — nobody at Rox hand-writes evals anymore. A weekly Devin reads production traces in Braintrust, rebuilds each failure in a full copy of Rox seeded with synthetic data, replays until the agent makes the same mistake, and opens a PR. The suite covers **72% of real usage vs. 43–57%** for their hand-written evals, and keeps growing week over week.
**Sources:** [Living Evals write-up](https://www.rox.com/articles/living-evals-an-eval-suite-that-grows-from-production) (Brian Xu, Oct 2026) · [launch thread](https://x.com/rox_ai/status/2110779380666617997)

## The pattern

```text
production traces (observability platform)
        │  weekly sample (~350 conversations)
        ▼
group into behaviors (goal · output · mutation · target)
        │  hundreds of conversations → ~130 behaviors
        ▼
for each under-covered behavior:
   synthesize data → full-copy preview env → replay request
   → compare vs. production trace → freeze as eval → open PR
        ▼
human reviews the PR, not the eval-writing
```

## Prerequisites

- An agent or AI feature in production, with **conversation-level tracing** (Rox used Braintrust; LangSmith/self-hosted logging works — you need the request + the records + tool calls touched)
- A deployable copy of your system (preview env, staging, or `docker compose up` in a VM) — **not mocks**
- Tests-as-code in your repo so an eval is just a committed file

## Step 1 — Make one trace replayable by hand

Before scheduling anything: pick one real conversation where your agent failed. Have Devin pull the trace, write synthetic data covering exactly what the request touched, bring up your system copy, and replay the request until the same failure occurs. If you can't reproduce one failure manually, the weekly loop will produce nothing.

## Step 2 — Freeze it as an eval, not a bug report

The artifact is a committed eval, not a Slack message. Rox's convention: the request is copied **word for word** from production; seeded data reproduces the exact conditions (e.g. "the newest meeting has no transcript"). Data-changing requests get a code assertion; reply-only requests get an LLM-judge rubric.

## Step 3 — Group by behavior before scaling

Running the loop on every conversation is wasteful — most requests repeat the same shapes. Rox's four labels define a *behavior*: **goal** (what the user wants) · **output** (what comes back) · **mutation** (nothing/create/edit/send) · **target** (named vs. inferred object). ~350 conversations a week collapse to ~130 behaviors; build evals for under-covered behaviors only.

## Step 4 — Encode the whole procedure as a skill

The trace→eval loop lives in **one skill file** Devin follows: pull trace → synthesize → preview env → replay → compare → freeze → PR. When the loop produces a bad eval, **fix the skill**, never hand-patch the eval — that's the compounding move.

## Step 5 — Schedule it weekly

Cron automation (Guide 6): pull the week's traces → group → for each under-covered behavior run the loop → open one PR with the new evals. Humans review the PR; Devin owns the suite.

## Verify it

- [ ] A real production failure replays deterministically in your preview env — same user request, same bad outcome
- [ ] The eval file is in your repo, runs in CI, and fails on the old behavior / passes on the fix
- [ ] Coverage is measured against *production traffic mix*, not your guesses — report it like Rox's 72%
- [ ] A bad eval got fixed by editing the skill, not the eval

## Pitfalls

- **Mocked replay.** Rox's earlier approach replayed through a mocked data layer — mocks can hide bugs in the very code they replace. Use a full copy; the point of a preview env is fidelity.
- **Flaky judging.** Even with no code change, ~1 in 8 evals passes some runs and fails others — agents aren't deterministic. Read a failure before trusting it; don't alert on single flakes.
- **Evals measuring taste.** The suite catches behavioral regressions (a tool path dead, a supported request unhandled), not style — every failure should point at a fixable defect.

## Knowledge check

1. Why replay in a full copy instead of a mocked data layer? *(Mocks can hide bugs in the code they replace — as the agent edits more state, the mock becomes the thing you're actually testing.)*
2. Why group conversations into behaviors before writing evals? *(Most requests repeat shapes — labeling goal/output/mutation/target lets one eval cover many conversations, so coverage maps to real usage.)*
3. What's the compounding move: fixing evals, or fixing the skill? *(The skill — a hand-patched eval teaches Devin nothing; a fixed skill produces better evals forever.)*

## Sources

- [Living Evals: an eval suite that grows from production](https://www.rox.com/articles/living-evals-an-eval-suite-that-grows-from-production) — the full methodology
- [Rox launch thread](https://x.com/rox_ai/status/2110779380666617997)
- Related: [Guide 13 — Official cookbook](official-cookbook.md) · [Guide 6 — Automations](automations-101-event-driven.md)
