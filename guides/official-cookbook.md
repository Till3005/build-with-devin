# Guide 13 — The official use-case cookbook

**Goal:** the proven usage patterns from Cognition's own docs, organized as a cookbook — what to slice for Devin, and 40+ documented recipes with prompts to copy.
**Level:** start here for breadth
**Sources:** [Best Practices](https://docs.devin.ai/use-cases/best-practices.md) · [Use-case gallery](https://docs.devin.ai/use-cases/gallery/index.md) · [use-case tutorials](https://docs.devin.ai/use-cases/index.md)

## The one rule behind all of it

Official guidance, verbatim logic: pick work that is **wide & shallow** — a large backlog of simple, horizontally-scalable tasks beats complex net-new builds, every time.

| Ideal task | Anti-task |
| --- | --- |
| Repetitive subtasks at junior-engineer complexity | Net-new complex features |
| < 90 minutes of manual work per slice | Anything unsplittable |
| Objective pass/fail verification | "Looks right to me" |
| Isolated, backwards-compatible, parallelizable | Tangled dependencies |

Four great slice shapes from the docs: **migrations, refactors, modernizations, tech-debt backlogs.**

## The recipe catalog

Everything below is a documented use case in the official gallery — each ships with a copy-paste prompt. Organized by the job it removes from a human's week.

### Incidents & production health

| Recipe | Mechanism |
| --- | --- |
| Auto-investigate Datadog/PagerDuty alerts | Webhook/API trigger → session investigates on fire |
| Auto-generate postmortems | PagerDuty resolve → Devin drafts timeline, root cause, action items |
| Daily Sentry error fixes | Nightly cron pulls new errors → fix PRs by morning |
| Debug a bug report end-to-end | Hand Devin the report + Datadog logs + DB access → root cause |

### Scheduled hygiene (the highest-ROI page in the docs)

| Recipe | Cadence |
| --- | --- |
| Weekly dependency update PRs | Weekly: outdated packages → tested upgrade PRs |
| Nightly E2E on staging | Nightly: run suite, file tickets for failures |
| Weekly changelog from merged PRs | Friday: categorized changelog → Slack |
| Daily Datadog health digest | Daily: error scan → Slack digest |
| Daily design-system audit | Daily: flag hardcoded colors/missing tokens in merged PRs |
| Feature-flag cleanup | One-time session strips flag + dead code post-release |
| Weekly Notion status digest | Weekly: PR/commit summary → Notion |
| PRs from meeting transcripts | Hourly: poll Granola → extract eng tasks → child sessions |

### Code quality

| Recipe | Mechanism |
| --- | --- |
| Auto-fix PR bugs before merge | Devin reviews every PR, pushes fixes to the branch |
| Add unit tests to a service | Build a test-writing skill, apply to charge flows/refunds/webhooks |
| Catch visual regressions | Repo skill: screenshot every affected page before PR |
| Migration checklist on every PR | Repo skill catches destructive ops, validates schema changes |
| Split a monolithic router | 2,000-line Express router → domain routes with shared middleware |
| Raise code coverage | Devin analyzes the suite, writes tests to cover gaps |

### Migrations & feature work

| Recipe | Mechanism |
| --- | --- |
| 50-file REST→GraphQL | Scope → conflict-free packages → parallel (Guide 11) |
| React 18→19 upgrade skill | Turn the official upgrade guide into a phased skill for your codebase |
| OpenAPI spec → implementation | YAML spec → Express handlers + Zod validation + Supertest |
| Stripe checkout flow | Spec → working flow + tests + browser verification |
| i18n a Next.js app | next-i18next install, string extraction, 3-language browser check |
| Figma → pixel-perfect | Figma MCP → components from mockups |
| Dockerize a Django app | Multi-stage Dockerfile + compose for Django/Postgres/Redis |

### Project management & data

| Recipe | Mechanism |
| --- | --- |
| Auto-triage bugs via Linear | Label applied → Devin investigates |
| PRDs → sprint tickets | Notion PRD → scoped Linear tickets |
| Backlog implementation plans | Multi-select Linear tickets → confidence-scored plans |
| `/dana` data queries in Slack | Plain-English database queries from any channel |
| Custom API usage dashboard | Devin builds a tailored dashboard on the v3 API |

### Getting better at Devin itself ("Devin Optimization")

| Recipe | Lesson |
| --- | --- |
| Cut a feature prompt 42→12 ACUs | Autopsy a costly session: 3 root causes → rewrite the prompt |
| Race 3 sessions on one problem | Parallel sessions try competing optimization strategies; best ships |
| 8 parallel sessions overnight | 8 untested modules → unit-test PRs by morning |
| Evaluate 30 libraries | One session per library → scored, ranked comparison |
| Turn a hotfix into a skill | Extract a successful incident session into a reusable skill |
| Weekly knowledge dedup | Scheduled session merges/conflicts-cleans knowledge suggestions |
| Team onboarding guide | Devin reads its own docs → a getting-started guide for your stack |

## How to use this cookbook

1. Pick one recipe from **Scheduled hygiene** — it's the cheapest first win (a nightly/weekly loop you stop thinking about)
2. Add one from **Incidents** if you have PagerDuty/Datadog/Sentry
3. When a recipe works, freeze it as a **skill** (Guide 12) or a **Bot** (Guides 1–5) — every row above survives as either

## Sources

- [Use-case gallery](https://docs.devin.ai/use-cases/gallery/index.md) — all recipes above, each with copy-paste prompts
- [Best Practices](https://docs.devin.ai/use-cases/best-practices.md) — the slicing doctrine
- [Use-case tutorials](https://docs.devin.ai/use-cases/index.md) — API integration, code coverage, containerization, frontend components, MCP
- Related: [Guide 11 — Migrations at scale](migrations-at-scale.md) · [Guide 6 — Automations](automations-101-event-driven.md)
