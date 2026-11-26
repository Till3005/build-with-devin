<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/cover-dark.png">
  <img src="assets/cover-light.png" alt="Build with Devin" width="100%">
</picture>

<br/>

[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![License: CC0-1.0](https://img.shields.io/badge/License-CC0_1.0-lightgrey.svg)](LICENSE)

<sub>Curated by [@darega0mae](https://x.com/darega0mae) · Sister registry: [built-with-devin](https://github.com/Till3005/built-with-devin) · [Improve a guide](CONTRIBUTING.md) · [Read on the site](https://till3005.github.io/built-with-devin/guides/)</sub>

<sub>**22** guides · **4** stages · every pattern reverse-engineered from a named, documented deployment</sub>

<sub>English · [简体中文](README.zh.md) · [日本語](README.ja.md) · [Português](README.pt.md)</sub>

</div>

> *Unofficial community project — not affiliated with, endorsed by, or sponsored by Cognition AI. "Devin" is a trademark of Cognition AI. Brand assets are used under the official kit at [devin.ai/brand](https://devin.ai/brand) — "ready for whatever you're making." Official docs: [docs.devin.ai](https://docs.devin.ai).*

**Build with Devin** is a tutorial collection: every guide takes a *documented, real-world* Devin deployment — from Cognition's own launch fleet to published customer cases — and reverse-engineers it into steps you can reproduce on your own account. No hypothetical demos; every pattern here is backed by a named deployment with reported numbers.

**Pair it with [built-with-devin](https://github.com/Till3005/built-with-devin)** — the companion registry of everything the community and Cognition have shipped. Registry answers *what exists*; this repo answers *how to build it*.

## Contents

- [Stage 0 — Foundations](#stage-0--foundations) — talking to Devin, the surfaces, your first Bot, the cookbook
- [Stage 1 — Operate](#stage-1--operate) — outcome prompts, automations, playbooks, skills, Apps, design
- [Stage 2 — Scale](#stage-2--scale) — one Bot to an org, migrations, evals, enterprise rollout
- [Stage 3 — Field wisdom](#stage-3--field-wisdom) — what real teams learned
- [How to use this repo](#how-to-use-this-repo) · [Conventions](#conventions) · [Contributing](#contributing)

```mermaid
flowchart LR
    subgraph S0["Stage 0 · Foundations"]
      G18["18 · Talking to Devin"] --> G17["17 · Desktop"]
      G18 --> G12["12 · CLI"]
      G18 --> G19["19 · The session loop"]
      G19 --> G1
      G17 --> G1["1 · Your first Bot"]
      G12 --> G1
      G1 --> G13["13 · Official cookbook"]
    end
    subgraph S1["Stage 1 · Operate"]
      GP["ref · Outcome prompts"] --> G6["6 · Automations"]
      G6 --> G9["9 · Playbooks"]
      G9 --> G16["16 · Skills & plugins"]
      G10["10 · Devin Apps"]
      G8["8 · Design work"]
    end
    subgraph S2["Stage 2 · Scale"]
      G2["2 · Product-owner"] --> G4["4 · Multi-Bot org"]
      G3["3 · Sentinel"] --> G4
      G4 --> G5["5 · Swarm"]
      G11["11 · Migrations"] --> G15["15 · Living evals"]
      G7["7 · Enterprise rollout"]
      G4 --> G20["20 · Dynamic Workflows"]
      G7 --> G21["21 · Security & OIDC"]
    end
    subgraph S3["Stage 3 · Field wisdom"]
      G14["14 · Field reports"]
    end
    S0 --> S1 --> S2
```

## Guides

### Stage 0 · Foundations

*From zero to a task that ships. Everyone starts here — these four guides and one reference teach the two surfaces, the prompting doctrine, and the first ownership.*

| # | Guide | You'll build | Based on | Level |
| --- | --- | --- | --- | --- |
| 18 | [Talking to Devin](guides/talking-to-devin.md) | Briefs Devin can't misread — say-how, checkable success, the 80% rule | [Coding Agents 101](https://devin.ai/agents101) + [official prompting docs](https://docs.devin.ai/essential-guidelines/instructing-devin-effectively) | Start here |
| 19 | [The session loop](guides/the-session-loop.md) | Understand → delegate → review → learn: DeepWiki, Ask Devin, Devin Review, Session Insights + the ACU meter | [Devin University](https://learndevin.com) + official product docs | Start here |
| 17 | [Devin Desktop](guides/devin-desktop.md) | The agent-native editor: Command Center, durable local sessions, Bots — one window | [Desktop changelog](https://docs.devin.ai/desktop/changelog) | Start here |
| 12 | [Devin CLI & extensibility](guides/devin-cli.md) | The local agent: daemon sessions, cloud handoff, skills, hooks | [CLI docs](https://docs.devin.ai/cli/index.md) | Intermediate |
| 1 | [Your first Bot](guides/bots-101-first-bot.md) | A Bot that owns an outcome — chat, sessions, Needs-you, memory, surfaces | [Official docs](https://docs.devin.ai/work-with-devin/bots) + launch post | Start here |
| 13 | [Official use-case cookbook](guides/official-cookbook.md) | 40+ documented recipes — hygiene loops, incidents, quality | [Use-case gallery](https://docs.devin.ai/use-cases/gallery/index.md) | Start here |

### Stage 1 · Operate

*The daily loop delegated: a Bot that knows the standard, sessions that fire on events, conventions encoded once, tools served live.*

| # | Guide | You'll build | Based on | Level |
| --- | --- | --- | --- | --- |
| — | [Bot outcome prompts, dissected](guides/bot-outcome-prompts.md) | Outcome prompts that assign ownership, not tasks — the real ones, reverse-engineered | Android Bot prompt + all 16 marketplace templates | Reference |
| 6 | [Event-driven automations](guides/automations-101-event-driven.md) | Sessions that fire on Slack, GitHub, Linear, cron, webhooks | [Automations docs](https://docs.devin.ai/product-guides/automations) | Start here |
| 9 | [Playbooks & knowledge](guides/playbooks-and-knowledge.md) | Encoding org conventions so every session inherits them | The layer behind every enterprise result | Intermediate |
| 16 | [Skills & plugins](guides/skills-and-plugins.md) | The post-playbook layer — SKILL.md contract, discovery, packaging as plugins | [Skills docs](https://docs.devin.ai/product-guides/skills) | Intermediate |
| 10 | [Devin Apps](guides/devin-apps.md) | Live internal tools and dashboards served from Devin's machine | [Devin Apps launch](https://devin.ai/blog/devin-apps) | Start here |
| 8 | [Design & visual work](guides/design-with-devin.md) | Art-directing production UI through Devin chat | Spraycash landing page write-up | Intermediate |

### Stage 2 · Scale

*One Bot to an organization: the four named-deployment archetypes, then the heavy machinery — migrations, evals, the enterprise rollout.*

| # | Guide | You'll build | Based on | Level |
| --- | --- | --- | --- | --- |
| 2 | [Product-owner Bot](guides/bots-201-product-owner.md) | A Bot that product-manages a whole app surface | Android Bot — 44 days, 1,134 PRs | Intermediate |
| 3 | [Scheduled-sentinel Bot](guides/bots-202-scheduled-sentinel.md) | A cron Bot that watches a check and fixes regressions | Layout Bot — 159 PRs/3wks | Intermediate |
| 4 | [Multi-Bot organization](guides/bots-203-multi-bot-org.md) | A Bot hierarchy with grants and roll-up reporting | SuperJennyStack — ~20 Bots, 1,900 PRs/wk | Advanced |
| 5 | [Reference-grounded swarm](guides/bots-204-reference-grounded-swarm.md) | A directed swarm writing a verified system | Harvey "Phil" — ~30 agents, 1M+ LOC | Advanced |
| 11 | [Migrations at scale](guides/migrations-at-scale.md) | A migration as hundreds of small verified PRs | Official playbook + Nubank | Intermediate |
| 15 | [Living evals from production traces](guides/living-evals.md) | A self-growing eval suite replaying production failures | Rox — 72% usage coverage vs 43–57% hand-written | Advanced |
| 7 | [Enterprise rollout patterns](guides/enterprise-playbook.md) | The six deployment shapes behind the biggest customer results | Nubank, Gumroad, EBANX, Modal, Airbyte… | Intermediate |
| 20 | [Dynamic Workflows](guides/dynamic-workflows.md) | Deterministic multi-agent orchestration with structured handoffs and resumable runs | [Dynamic Workflows docs](https://docs.devin.ai/work-with-devin/dynamic-workflows) | Advanced |
| 21 | [Security Profiles & Cloud OIDC](guides/security-profiles-cloud-oidc.md) | Least-privilege session envelopes plus keyless cloud authentication | [Security Profiles](https://docs.devin.ai/product-guides/security-profiles) + [Cloud OIDC](https://docs.devin.ai/product-guides/oidc) | Advanced/admin |

### Stage 3 · Field wisdom

*What teams actually learned — wins, failures, and the numbers they published.*

| # | Guide | You'll build | Based on | Level |
| --- | --- | --- | --- | --- |
| 14 | [Community field reports](guides/community-field-reports.md) | What real teams learned — wins, failures, and named deployments with numbers | 15+ published hands-on accounts | Start here |

<p align="right"><a href="#readme">back to top</a></p>

---

## How to use this repo

Read stages in order the first time; after that, jump.

- **Solo developer, first contact:** 18 → 17 (or 12 if you live in a terminal) → 1 → 13. That's a weekend.
- **Want quick wins?** Guide 13's scheduled-hygiene recipes are the cheapest first deployment.
- **Team lead:** add 6, 9, 16 — the loop, the conventions, the reuse layer.
- **Running an org?** All of Stage 2, then 7 — and read 14 for what other teams actually hit.
- Every guide ends with **Sources** — official docs *and* the community/field account the pattern was distilled from — and **Verify it**, the check that tells you the reproduction worked.

<p align="right"><a href="#readme">back to top</a></p>

---

## Conventions

- Each guide is self-contained: goal → prerequisites → the build, step by step → operating the result → pitfalls.
- Prompts are quoted verbatim where a source published them; otherwise they're reconstructed and marked as such.
- Numbers in a guide come from the cited deployment, not from our guesses.

## Watchlist

Curriculum gaps found by the steward and Source Scout — each needs a fix in all 4 languages.

Open (triaged Nov 25, 2026 — verified Grade A official docs unless noted):

- **72h watchlist (existing-guide updates):**
  - [Nov 23 release notes](https://docs.devin.ai/release-notes/overview) — side-by-side session panes (`Option/Alt+click`), `Cmd/Ctrl+K` session search, Preflight secret delete warning, Offered vs Required plugins, MCP `Allow for this session`, API-key MCP secret binding, custom MCP Automatic auth, Automations right-click `Run now` → Guides 19, 16, 6.
  - [SWE-2.1 launch](https://cognition.ai/blog/swe-2-1) (Nov 24, 2026) — Grade A for availability (`SWE-2.1`, `SWE-2.1 Ultrafast`, `SWE-2.1 Cyber`; free on Desktop/CLI through 2026-12-08), Grade C for vendor self-reported benchmarks (do not cite as independent proof) → Guides 17, 12.
  - [Local Hands](https://docs.devin.ai/work-with-devin/local-hands) — cloud-to-local execution via Desktop Approve / `devin connect` / `devin --cloud` (distinct from Devin Connect) → Guides 17, 12.
  - [Stacked PRs](https://docs.devin.ai/work-with-devin/stacked-prs) — GitHub.com-only atomic bottom-up stacks → Guides 19, 11.
  - [Devin Memory & Dreaming](https://docs.devin.ai/product-guides/memory) — Git-backed personal memory vs Bot shared memory, daily Dreaming opt-out, org/enterprise admin locks → Guides 1, 9.
  - [Devin Outposts](https://docs.devin.ai/cloud/outposts/overview) — summary pointer for self-hosted execution → Guide 7.
- **Proposed new guide (pending approval/budget):** [Outposts + Modal GPU post-training](https://docs.devin.ai/tutorial-library/post-training-modal) (budget-gated).
- **Evidence-boundary cleanup (from Registry Maintainer audit):** downgrade/re-source hold-list claims in Guides 2, 4, 5, 7, 14 (SupaSEO 404 link/numbers, Super Jenny 6× revenue, Android Bot 88% self-merge/GA, Harvey "Phil" 1M LOC/3 wks, Zeb vs unnamed customer 142 objects/8 days).

Resolved Nov 26: Dynamic Workflows and Security Profiles & Cloud OIDC added as Guides 20 and 21 in all 4 languages. They are official-source-backed; independent reproduction evidence is still pending and must not be overstated.

Resolved Nov 22: Access & Sharing launch (Nov 20 release) — user groups + per-session sharing + granular secrets + repo sync added to Guide 1's sharing section (4 langs).

Resolved in the Nov 20 drift pass (all 4 languages): CLI daemon deep-dive + multi-client join semantics (Guide 12, with our recorded Desktop lock exception), Bot template mechanics — library/marketplace/empty-start/Share-as-template (Guide 1), `memory_enabled: false` on session create (Guide 6), *Mark done* vs Archive + subscribers/Phonebook (Guide 17), `DetectProxy` policy (Guide 17).

## Contributing

Found a better recipe, or reproduced one and have numbers? See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[CC0-1.0](LICENSE) — dedicated to the public domain.
