# Guide 7 — Enterprise rollout patterns

**Goal:** deploy Devin at org scale using the shapes that already produced published numbers — not experimentation, the proven motions.
**Level:** intermediate (written for eng leads)
**Source:** published customer cases, [devin.ai/customers](https://devin.ai/customers)

Six deployment shapes, distilled from the companies that published results. Most successful rollouts use two or three of these, not all six.

## Shape 1 — The legacy-migration engine (Nubank, Comarch)

| | |
| --- | --- |
| Deployment | Nubank: multi-million-line, 8-year-old ETL monolith → sub-modules. Comarch: 20-year, 10M-line ERP rebuild. Odyssey Logistics (Cognizant): Access/VBA TMS → cloud-native, **37% net cost saving** |
| Result | 8–12× engineering efficiency, 20× cost savings (Nubank) |
| Mechanism | Fine-tune Devin on *your* codebase (Nubank cut ~40 min/task to ~10), then point it at the migration as a continuous program — tracked small PRs, not a rewrite |

**How to copy:** pick one bounded legacy system; fine-tune or teach via playbook; run Migration Engineer-style loop — one big migration as small tracked PRs with a progress surface. The win compounds: each migrated module makes the next session smarter.

## Shape 2 — The primary-author repo (EBANX, Gumroad, Finch)

| | |
| --- | --- |
| Deployment | EBANX: **92% of merged PRs Devin-authored**. Gumroad: Devin is the repo's **#1 contributor** (1,500+ PRs). Finch: 3,000 PRs, ~20 engineer-months saved. Gamma: ~10-agent fleet + 3 engineers rebuilt PowerPoint import — **3,500+ merges** on a job sized at 5–10 engineers × a year |
| Mechanism | Devin isn't an assistant on these repos — it's the default author. Humans review and direct |

**How to copy:** pick one high-velocity repo; route tickets to Devin sessions by default; humans review. The metric to watch is authored-PR share — above ~50%, you're in this shape; below it, you're still in pilot mode.

## Shape 3 — The always-on first responder (Modal, Reducto, AngelList)

| | |
| --- | --- |
| Deployment | Modal: **80% of incidents investigated before an engineer opens the thread**. Reducto: Devin Oncall is first responder; engineers rarely paged. AngelList: Devin root-causes 70% of incidents pre-engineer |
| Mechanism | PagerDuty/Slack trigger → session investigates with logs/repo access → report lands before the human wakes |

**How to copy:** [Devin Oncall](https://docs.devin.ai) or a PagerDuty-triggered automation (Guide 6, recipe: incident → investigate). Measure % of incidents pre-investigated — every point of it is human sleep recovered.

## Shape 4 — The maintenance fleet (Airbyte, Melius)

| | |
| --- | --- |
| Deployment | Airbyte: keeps **700+ connectors** running. Melius: ~100 PRs/day |
| Mechanism | The long tail nobody wants — connector rot, dependency drift, stale flags — routed to Bots/automations that churn through it continuously |

**How to copy:** enumerate your maintenance backlog (the work engineers avoid); wrap it in Code Health Engineer / Code Reaper-style Bots (official templates) with weekly cadence.

## Shape 5 — The org-wide seat (Wayfair, The Access Group, Citi)

| | |
| --- | --- |
| Deployment | Wayfair: 1,600+ engineers all-in. Access Group: Devin across 250 products, 2,000+ engineers → 5× output. Citi: 40,000-developer rollout, 30% tech-vendor spend cut |
| Mechanism | Not more agents — the *seat*: every engineer has Devin access, shared playbooks, org-level knowledge |

**How to copy:** the rollout order in the published cases is consistent — pilot team → measured results → playbook/knowledge standardization → seat expansion. Skipping the knowledge step is why seat rollouts stall: see [playbooks guide](playbooks-and-knowledge.md).

## Shape 6 — The process gate (Hamming, Litera, Eight Sleep)

| | |
| --- | --- |
| Deployment | Hamming: Devin writes 25% of code volume. Litera: regression cycles cut 90%. Eight Sleep: 8× more shipped. Zeb: NetSuite→Databricks migration **4 weeks → 2.5 weeks**; separately, an unnamed Fortune 500 energy customer migrated a **142-object** platform to Databricks Unity Catalog in **8 days** ([Cognition Databricks blog](https://devin.ai/blog/devin-for-databricks-migrations)) |
| Mechanism | Devin owns a stage of the pipeline — regression testing, QA — not the whole product |

**How to copy:** find the pipeline stage with the worst human cost (regression cycles, QA); assign it to a Bot or automation; measure the stage's cycle time before/after.

## Anti-patterns the cases imply

- **Tool, not colleague.** The high-number deployments give Devin ownership (repos, surfaces, stages), not assignments — same lesson as Guides 1–5.
- **Pilot forever.** Published results all share one trait: a measured pilot that *graduated*. Set the graduation criterion upfront (PR share, incidents covered, hours saved).
- **No knowledge layer.** Every big deployment encodes conventions somewhere — fine-tunes, playbooks, Bot instructions. Without it, quality varies by session.

## Verify it

- [ ] Your rollout doc names one pipeline stage, one metric, and a graduation criterion — before the first session
- [ ] Week-2 checkpoint: can you state Devin's merged-PR share on that stage without querying anyone?

## Pitfalls

- **Scaling the pilot that never graduated.** Every big number here came after a measured pilot with an exit criterion.
- **License-first thinking.** Buying seats before naming the owned stage produces shelfware — the pattern is stage → pilot → metric → then seats.

## Knowledge check

1. Why do all six deployment shapes share 'an owned stage' as their atom? *(Every published number came from a bounded, measurable surface — orgs that deployed 'everywhere' published nothing.)*
2. What's the graduation criterion and why set it before the pilot? *(A metric + threshold that flips pilot → production; without it, pilots drift forever or get killed by vibes.)*
3. Why does the knowledge layer appear in every large deployment? *(Consistency at scale requires shared context — the alternative is N different-quality sessions.)*

## Sources

- [devin.ai/customers](https://devin.ai/customers) — customer cases and reported numbers
- [Devin for Databricks migrations](https://devin.ai/blog/devin-for-databricks-migrations) — Zeb (4 weeks → 2.5 weeks) and unnamed Fortune 500 energy customer (142 objects in 8 days)
- [built-with-devin — enterprise index](https://github.com/Till3005/built-with-devin#enterprise-deployments) — the registry's verified case table
- [Devin for Admins](https://learndevin.com/course/devin-for-admins) — the official 11-lesson admin course: blueprint hierarchy, secrets posture, ACU governance, rollout analytics (free lessons; exam needs Enterprise)
