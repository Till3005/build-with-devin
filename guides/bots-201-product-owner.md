# Guide 2 — Product-owner Bot

**Goal:** a Bot that product-manages an entire app surface — files its own tickets, builds them, merges, and reports daily.
**Level:** intermediate · **Human load after setup:** ~1 message per 6 merged PRs
**Source deployment:** Cognition's **Android Bot** — shipped the Devin Android app to Google Play open beta in **44 days**: 1,134 merged PRs, 344,651 lines of Kotlin, 2,841 screenshot tests, 1,217 tickets. Its human sent **183 messages total** (22 days of silence). It now owns ongoing Android development and updates the app as iOS features land.
**Sources:** [launch post](https://devin.ai/blog/introducing-devin-bots) · [Fortune](https://fortune.com/2026/11/17/exclusive-cognition-bets-on-devin-bots-coding-agents-in-challenge-to-anthropics-duet-and-openais-dots/)

## The pattern

One Bot owns a *surface* — an app, a site, a service — the way a PM owns it: it decides what to build, turns that into tickets, runs a session per ticket, and keeps the surface alive indefinitely. The human acts as the executive it reports to.

```text
Bot ──► files tickets ──► session per ticket ──► PR ──► CI + Devin Review ──► merge
 │                                                                           │
 └──────────── daily report + Needs-you decisions ◄──────────────────────────┘
```

## Prerequisites

- A repository the Bot can fully own (app repo with CI, review, and a merge path)
- Devin Review enabled on the repo, and CI checks wired
- A Slack app for the Bot (recommended — every documented deployment reports in Slack)

## Step 1 — The outcome prompt

The real one, verbatim from Cognition:

```text
your job is to product manage the android app. Basically, you're going to
autonomously create the entire thing, but we need to figure out what the
blockers are for you doing that first.
```

Reconstructed template for your surface:

```text
Your job is to product manage <surface>. You're going to autonomously
<build / keep parity with <reference>>, but first enumerate the blockers
to you doing that — where the code lives, how to build and test it, and
how changes merge — then start working through them.
```

Note the shape: **ownership + autonomy + blockers-first**. Don't hand it a backlog; hand it a mandate and make it surface what it needs.

## Step 2 — Phase one: unblock, don't build

The Android Bot didn't write code first — it enumerated blockers: repo access, build commands, how to test on a device/emulator, the merge path. Your version of that list:

- Can it build the project on its machine? (Blueprint/snapshot dependencies)
- Can it produce installable artifacts (APK/TestFlight/preview deploy)?
- Does it know the merge policy — which checks must pass, who reviews?
- Does it have the credentials it needs (store keys, signing) — or a documented grant request for them?

Let it finish this audit before it files product tickets. Every blocker it resolves here is a stalled session you won't see later.

## Step 3 — The working loop

Once unblocked, the steady state is:

1. Bot files a ticket for the next unit of work it decides on
2. A child session implements it and opens a PR — small, with proof it works
3. CI + Devin Review gate the merge
4. Bot merges (or asks you when judgment is needed — it landed in Needs you)
5. Daily report lands in Slack — the Android Bot's reports include a **screen recording** of what changed

Set up the reporting in the Bot's Instructions, not chat:

```text
Every day, post a report in #<channel>: what shipped, what's in flight,
what needs a human. Include a screen recording of visible changes.
```

## Step 4 — Your job as its executive

The 183 messages over 44 days fell into two buckets:

- **Judgment calls** — security review sign-off, a design trade-off, an approval card
- **Direction** — "be more ambitious" is the documented example

Everything else — tickets, implementation, fixes, self-merges — is the Bot's job. If you're answering implementation questions, you're managing too low. Correct once → it lands in memory → next session inherits it.

## Steady state

After the initial build, the same Bot switches to *owning* the surface:

- Keeps parity with a reference project (Android Bot now tracks iOS features)
- Triages incoming reports (it fields Google Play beta feedback)
- Catches cross-surface regressions — the Android Bot autonomously found and fixed an iOS/web-side break caused by someone else's change

## Verify it

- [ ] Bot's first act was a blocker audit, not a PR
- [ ] It files and works its own ticket queue without being asked
- [ ] PRs are small and carry proof (tests, screenshots, recordings)
- [ ] Daily report posts to Slack with visible evidence
- [ ] You went a full day sending zero messages and PRs still merged

## Pitfalls

- **Skipping the blocker phase.** A product-owner Bot that starts coding before it can build/test/merge produces orphaned PRs.
- **Big PRs.** The deployment's safety comes from small, verifiable units. If PRs balloon, instruct: *"one ticket, one concern, one PR."*
- **Reviewing code instead of direction.** At 30+ PRs/week you can't review each diff — gate on CI + Devin Review + the Bot's evidence, and spend your messages on direction.

## Knowledge check

1. Android Bot merged PRs itself — what made that safe enough to allow? *(Only PRs that passed CI and Devin Review merged; 2,841 screenshot tests made 'done' machine-checkable, and ambiguous judgment escalated to the human.)*
2. Why file tickets instead of just prompting sessions directly? *(Tickets create an auditable queue the Bot triages by priority — and the human reviews one queue, not 50 sessions.)*
3. What does '22 days of silence' tell you about the control model? *(Escalation-by-exception works only when the Bot's definition of done is verifiable; silence is the feature, not neglect.)*

## Sources

- [Introducing Devin Bots](https://devin.ai/blog/introducing-devin-bots) — Android Bot numbers and prompt
- [Fortune exclusive](https://fortune.com/2026/11/17/exclusive-cognition-bets-on-devin-bots-coding-agents-in-challenge-to-anthropics-duet-and-openais-dots/) — independent launch reporting on Bots, access controls, and the operating model
- [Russell Kaplan on Android/iOS parity](https://x.com/russelljkaplan/status/2122771093920653493) — maintained at parity with zero Android engineers
- [Russell Kaplan on regression catching](https://x.com/russelljkaplan/status/2122803486198988970) — Android Bot catching an iOS/web-side regression
- Related: [Guide 4 — Multi-Bot organization](bots-203-multi-bot-org.md) when one surface becomes a business
