# Guide 4 — Multi-Bot organization

**Goal:** a hierarchy of Bots that runs an entire business unit — one orchestrator delegating to specialist Bots, one human deciding through a single daily thread.
**Level:** advanced
**Source deployment:** Jenny Xu's **SuperJennyStack** — ~20 Bots running a mobile game studio. ~50 → **1,900 PRs/week**, weekly releases, studio revenue 6×'d. Published as a community template in the [Bot marketplace](https://devin.ai/bots/templates). The official **bot-to-bot grant handoff** (QA → Developer → retest → PM report) uses the same mechanics at smaller scale.
**Sources:** Jenny Xu's published stack ([via launch coverage](https://x.com/cognition/status/2122737511684587551)) · [Bots docs](https://docs.devin.ai/work-with-devin/bots) · [BotSpeak post](https://x.com/xujennyc/status/2123111543105868166)

## The pattern

Don't build one Bot that does everything — build a small company:

```text
                    ┌─────────────┐
              ┌────►│ Orchestrator │◄──── one roll-up thread
              │     └──────┬──────┘      (4×/day, emoji answers)
              │            │ grants: read + message
     ┌────────┼────────┬───┴─────┬──────────┐
     ▼        ▼        ▼         ▼          ▼
  SuperPM  SuperDev  SuperQA  SuperRelease  SuperSupport
  (what)   (build)   (verify) (ship)        (users)
```

The human is the CEO: the orchestrator collects every subordinate Bot's pending decisions into **one Slack thread, 4×/day**, answered with emoji.

## Prerequisites

- Guide 1 done — you can create and instruct a Bot
- Slack connected — this pattern lives in Slack; the orchestrator's roll-up thread is the whole UX
- A bounded domain with separable jobs (a product, a studio, a service area)

## Step 1 — Design the org chart first

Jenny's published stack — copy the *shape*, not the names:

| Bot | Owns |
| --- | --- |
| Orchestrator (SuperJenny) | Delegation to every other Bot; compiles their asks into one thread; trained on her personality/quirks |
| PM (SuperPM) | Ranked daily fix list from metrics + store reviews + trends |
| Release (SuperRelease) | Weekly build, ready for store submission Friday |
| QA (SuperQA) | Real-device tests with video proof |
| Support (SuperSupport) | Drafts every store-review reply for approval; helps players overnight |

Remaining ~15 Bots cover development, Unity, UI, iOS, Android, analytics. Rule of thumb from the deployment: **one Bot per job you could name on an org chart** — not per task, per *responsibility*.

## Step 2 — Create the specialists

For each job, a Bot with a scoped outcome prompt:

```text
You own QA for <product>. Test every release candidate on real devices,
post video proof, and block release on failures. Report what needs a
decision to the orchestrator.
```

Keep each Bot's Instructions focused on its job's rules; shared knowledge (brand, deploy process, who approves what) goes in each Bot's instructions or a shared resource — there is no global memory across Bots, so the orchestrator's prompts carry the connective tissue.

## Step 3 — Wire grants

A grant gives Bot A read/message access to Bot B — this is how Bots hand work to each other (the Bots ask for the grant; you approve the card once). The orchestrator needs access to every specialist.

The documented official variant — smaller, same mechanics:

```text
QA Bot finds a bug ──grant──► Developer Bot fixes ──► QA retests on
staging ──► PM Bot reports status in channel
```

Approve grants narrowly: the orchestrator reads and messages specialists; specialists don't all need to reach each other.

## Step 4 — The roll-up thread

This is the single most important instruction — it converts 20 Bots' worth of interruptions into one habit:

```text
Collect every pending decision from the Bots you work with into one
Slack thread, posted at <times> daily. For each item: what's blocked,
the options, your recommendation. I answer in replies/emoji; treat my
replies as decisions and relay them.
```

Jenny runs this **4×/day** and answers **with emoji**. The discipline: you never talk to the specialists — the orchestrator relays your decision and follows it to done.

## Step 5 — Cadence = the org's heartbeat

| Cadence | Who runs it |
| --- | --- |
| Daily ranked fix list | PM Bot (metrics + reviews + trends) |
| Weekly release candidate | Release Bot → QA Bot sign-off |
| 4×/day decision thread | Orchestrator |
| Overnight player help | Support Bot (drafts replies for morning approval) |

Each Bot owns its loop; the orchestrator owns the schedule of loops.

## Step 6 — Inter-bot protocol (BotSpeak)

The scale problem nobody warns you about: Jenny's 20+ Bots were sending **700+ messages/day** — she couldn't keep up. Her fix was **BotSpeak**, a token-saving shorthand Bots use *with each other* ([her writeup](https://x.com/xujennyc/status/2123111543105868166)):

| Rule | What it means |
| --- | --- |
| Shorthand | `ACK` and friends instead of full replies |
| ASD-STE100 | Simplified English grammar — the aviation doc standard, unambiguous and cheap in tokens |
| Emoji receipts | React ✅ instead of "got it, thanks" |
| No niceties | Bots send each other only what the other needs |
| Human gets prose | The roll-up thread stays full sentences with decision context |

Six days after switching: decisions made by Bots without her **12×'d**, repeated asks −50%, inter-bot clarifying posts −12%. The protocol exists because token waste isn't the real cost — *attention* waste is: shorter bot-to-bot messages mean the human's one thread stays readable.

## Verify it

- [ ] Every specialist Bot has a scoped outcome prompt and active grants
- [ ] The orchestrator posts the consolidated decision thread on schedule
- [ ] A decision you answered via emoji got relayed and resolved by the right specialist
- [ ] A cross-Bot handoff completed end-to-end (find → fix → verify → report)
- [ ] Total human messages today < number of merged PRs

## Pitfalls

- **Skipping the orchestrator.** N Bots each DMing you is N× noise. The org only works if judgment funnels through one thread.
- **Vague job boundaries.** "Dev Bot" and "Fix Bot" will collide. Boundaries follow the org chart — QA *verifies*, Release *ships*, PM *prioritizes*.
- **Over-granting.** Mesh grants (everyone can reach everyone) recreate chaos. Hub-and-spoke through the orchestrator.
- **Prose between Bots.** Bots writing paragraphs to each other is how you get 700 messages/day — adopt a BotSpeak-style protocol: shorthand + emoji receipts + no niceties; full sentences only for the human.
**Session tracking is the first thing that doesn't scale.** The [100 Days of Devin](https://www.raijuna.com/blog/devin-100-day-challenge-day-1) field log found fleet ops break on 'which Bot produced this PR? which one needs me?' — and setup alone consumed ~18% of weekly quota. Budget for fleet observability from day one.

## Knowledge check

1. Why does SuperJennyStack route all human contact through *one* consolidated thread? *(Attention is the bottleneck, not compute — 20 Bots generating 20 threads is just 20 jobs again.)*
2. When does a grant beat 'ask the orchestrator'? *(When the needed capability is already owned by another Bot — grants borrow ownership instead of duplicating it.)*
3. What does the human's '4×/day with emoji' cadence imply about delegation depth? *(Decision bandwidth, not headcount, is what Bots replace — the human kept the judgment layer and lost the typing layer.)*

## Sources

- [Introducing Devin Bots](https://devin.ai/blog/introducing-devin-bots) — SuperJennyStack numbers, grant-handoff variant
- [Bot marketplace](https://devin.ai/bots/templates) — SuperJennyStack community template + 16 official templates
- [Bots docs](https://docs.devin.ai/work-with-devin/bots) — grants, memory, access
- Related: [Guide 5 — Reference-grounded swarm](bots-204-reference-grounded-swarm.md) for swarms that *write* rather than *operate*
