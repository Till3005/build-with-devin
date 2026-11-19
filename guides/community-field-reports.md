# Guide 14 — Community field reports

**Goal:** what engineers who ran Devin on real work actually learned — including the failures. Distilled from published hands-on accounts, both glowing and hostile.
**Level:** start here for judgment
**Sources:** linked per report below

This guide is deliberately balanced: where Devin reliably wins, where it burns money, and the working style that separates the two outcomes.

## The pattern that repeats across every report

Users who get results treat Devin as an **asynchronous junior engineer**, not a code generator. Scott Wu (Cognition CEO) describes the internal workflow in [Lenny's Newsletter](https://www.lennysnewsletter.com/p/how-devin-replaces-your-junior-engineers): delegate well-scoped tasks, let them run while you do meetings, review PRs. [Every's account](https://every.to/chain-of-thought/coding-with-devin-my-new-ai-programming-agent) lands on the same frame — it requires a *skill set*: learning what it's good at, writing tasks it understands, knowing when to step in, and learning to trust work done differently than you'd do it.

## Where Devin won, documented

**End-to-end prototyping.** From a blank repo, Devin scaffolded a FastAPI + React "City Explorer" (images/weather/news integrations), ran it locally, opened a PR, and deployed a public URL — ~90 minutes, ~2 human interventions ([Medium hands-on](https://medium.com/@sambhavgaur_70582/copilot-cursor-or-devin-my-hands-on-weekend-with-ai-that-codes-and-deploys-acc708e802b3)). [Scott Logic](https://blog.scottlogic.com/2025/10/20/rapid-development-with-devin.html) reports the same arc on a real client prototype — with a crucial iteration lesson below.

**Work that needs a runtime.** In a [head-to-head with Claude Code](https://web.archive.org/web/20260718112612/https://mohitkhare.me/blog/devin-vs-claude-code/), Devin lost on fitting-into-your-conventions tasks but won clearly where a machine helps: memory-leak hunting where it profiled, took heap snapshots under load, and produced a report — the agent's own VM is the feature.

**Live troubleshooting.** [Faros](https://www.faros.ai/blog/how-to-use-devin-ai-troubleshooting) used Devin *during a customer call*: it read the introspection API code and generated a working `curl` in seconds — collapsing a 1–2 day follow-up loop into the call itself.

**Real migrations with fresh docs.** A Tailwind 3→4 + DaisyUI 4→5 upgrade on a gnarly Vue→React codebase worked when the team fed Devin current docs via the Context7 MCP — the prompt carried the *context*, not just the task ([Bootcamp write-up](https://medium.com/design-bootcamp/day-7-of-30-getting-to-know-devon-ai-and-working-with-him-743c351cd0c4)).

**Self-verification.** A [year-long practitioner comparison](https://architecttocto.substack.com/p/the-only-coding-agent-worth-paying) marks Devin's browser-driven e2e testing as the threshold moment: it navigates to what it built and checks it — a feedback loop that resembles engineering, not generation.

**Beyond code.** A Cognition researcher reports Devin rebuilt — and finished — a Lean formalization that had taken him much of a semester nine years earlier, in **under 15 minutes** ([post](https://x.com/penlume/status/2115806616796921885)). Math formalization rewards the same trait as migrations: a machine-checkable definition of done.

**Wired into observability.** [Dynatrace MCP + Devin](https://medium.com/lets-code-future/how-i-turned-devin-into-a-performance-analysis-agent-with-dynatrace-mcp-753d3f4790a2) turns Devin into a performance-analysis agent: it queries live metrics and traces, then diagnoses — the MCP server carries production context the repo can't (Medium). See also [Devin: from bug report to pull request](https://medium.com/@winter.inc/devin-from-bug-report-to-pull-request-25-days-of-ai-day-18-b158daa20f23) for the plain ticket→PR loop end-to-end.

## Where it failed, documented

- **Vague or over-broad prompts.** Scott Logic's first prompt produced an unusable scaffold; narrowing the stack and the ask ("just the models") fixed it. Devin over-builds — tell it what *not* to build.
- **Convention-fitting tasks.** "Add pagination to this endpoint" came back misaligned with codebase conventions in two independent reports ([amillionmonkeys](https://www.amillionmonkeys.co.uk/blog/ai-coding-tools-small-studios), [mohitkhare](https://web.archive.org/web/20260718112612/https://mohitkhare.me/blog/devin-vs-claude-code/)) — Devin builds in isolation unless you carry the conventions to it (→ Guide 9).
- **Uncheckable work.** [expectedwrong](https://expectedwrong.com/devin-appraised) and [alanwest's 10-task test](https://dev.to/alanwest/i-gave-devin-10-real-tasks-it-completed-3-3063) document the failure mode: confident output that's broken or absent, credit burned in loops. Their tasks skewed to work with no clear verification — the same gate the official playbook makes mandatory (Guide 11).

## Named team deployments (community, with numbers)

Real orgs publishing their Devin operating data — mostly from Japan's engineering community, which documents unusually well:

| Team | Deployment | Reported result |
| --- | --- | --- |
| rakko_inc | Devin auto code-review via Playbooks + GitHub Actions + Devin API — pre-digests every PR before human review | **65 → 184 reviewed PRs/month (2.8×)**; humans start from Devin's summary ([report](https://zenn.dev/rakko_inc/articles/00cc5a5a679971), JP) |
| Skillnote (QA) | PR → Actions → Devin generates test-design drafts (CSV/Excel, incl. "why this case") posted to the PR | ~**35 min saved per 10 test cases**; Devin-designed cases caught bugs humans missed ([report](https://zenn.dev/skillnote/articles/5ba429ca249801), JP) |
| arufian | Serverless GitHub-event automation (no standing server): labels `devin:fix`/`devin:plan` drive Devin sessions, with a **priority × complexity policy table** and a plan-first approval flow | Safety scans gate risky PRs; high-complexity work gets plan → human approve → `run that plan` ([report](https://zenn.dev/arufian/articles/f80a62f5217cee), JP) |
| Leverages (levtech) | Org rollout: 14 teams / ~30 people | **177 merged PRs** in ~2.5 months; they measure ROI as `ACU cost − hours saved × wage` and track task-type mix ([report](https://zenn.dev/levtech/articles/9c869303820844), JP) |
| Decagon | AutoResearch on Devin Cloud: one orchestrator Devin + parallel subagents competing hypotheses; every idea verified against replayed production traffic on Modal GPUs | **up to 2.5× more throughput per GPU** on support traffic ([writeup](https://x.com/DecagonAI/article/2115511110120120437)) |
| Nader Dabit | Personal 5-bot org — **CTO** (all sessions/repos, iMessage VIP), **Auto(mation)Bot** (runs his automations, perf reports), **DevCommunityBot** (ambassador program data → mini-apps), **DevRelBot** (docs + tutorial videos with *its own computer, own Devin/GitHub/Linear accounts, ElevenLabs voice clone*) | Plus **Windfable**: ~10 SuperJennyStack Bots on a Unity iOS RPG, each with own macOS+Xcode+Unity, testing iPhone Duo folded/unfolded modes with screenshot/video diffs ([primer](https://x.com/dabit3/status/2122755275182469515)) |
| Mark Fenner | Solo operator running four job-specific Bots under a coordinating Chief Agent Bot ("Frankie") | Consolidated updates via one decision surface — the multi-Bot org shape works without a team ([walkthrough](https://x.com/markfenner/status/2122740244328145211)) |
| hubble | Two standing loops: every Dependabot PR gets a Devin investigation before a human reads it — a GREEN/YELLOW/RED risk label **plus the reasoning in a comment**; a weekly Datadog CCM loop picks a cost candidate, digs in, and hands back a decision-ready report | Review material is already assembled when the human opens the PR; the reasoning, not the label, is the deliverable ([Dependabot loop](https://zenn.dev/hubble/articles/88429bd24db476), [cost loop](https://zenn.dev/hubble/articles/091e29a0c86ec3), JP) |
| SMARTCAMP | Standing security pipeline: scheduled GitHub Actions pull ECS images → Trivy scan (HIGH/CRITICAL) → file issues → Devin remediates; AWS creds and scanner jobs split so only artifacts cross; hash-pinning + 7-day release grace guard against scanner lag | Vulnerability remediation as a pipeline, not a session ([report](https://zenn.dev/smartcamp/articles/97ac804043530e), JP) |
| canly | Devin as analyst, not coder: classified ~700 historical support tickets to find what "cause unidentified" actually was | Over half weren't bugs; choosing what context to give the AI (DB? docs?) mattered more than the model ([report](https://zenn.dev/canly/articles/9c19bb123e208c), JP) |

The reusable ideas inside: **policy-table gating** (arufian: only auto-PR low-risk work, plan-first for complex), **fixed-output prompting** (Skillnote: fixed CSV format + inline Python for conversion kills output variance), **reviewer-pre-digest** (rakko: Devin summarizes + flags before the human reads), **reason-first triage** (hubble: the label is a pointer; the comment carrying the evidence is the deliverable), **pipeline-shaped remediation** (SMARTCAMP: scan → issue → fix as one CI-shaped loop with credentialed and unprivileged stages separated), and **accounting for it honestly** (levtech's ACU-vs-wages ROI formula).

**The org-management fine print** (from Leverages' ~30-user rollout, same report):

- One Slack workspace can bind to only **one** Devin organization — check whether another department already claimed yours before planning Slack-driven sessions.
- There's no per-team ACU quota; they aggregate usage by listing sessions via the API and scraping each session's ACU from the web UI — budget by visibility, not enforcement.
- Silent ACU burn: by default every comment on a Devin-authored PR wakes a session. They switched on **"Only respond to PR comments that mention Devin"** so people can discuss PRs freely.
- Repo onboarding is serial — one repository mid-setup blocks the next; schedule it.
- Their ROI split: high on PR pre-review (~1–2 ACU each via a `devin-review` label → Actions → API Playbook), scheduled library-upgrade risk assessments, and legacy work fed a *similar existing PR*; low on wide refactors and tasks too small to matter.

## The distilled lessons

1. **Scope the slice, not the project.** The successes are all bounded units; the failures are "go build/fix this broadly." (Official doctrine: Guide 13.)
2. **Verify or don't delegate.** Give Devin work where a machine can check "done" — tests, builds, a working `curl`, a rendered page.
3. **Carry context, not assumptions.** Conventions, current docs (via MCP), your stack's shape — the failures are context failures, not capability failures.
4. **Delegate; don't watch.** The ROI in every positive report is *asynchrony* — tasks run while you do something else. Watching it type is how you decide it's "slow."
5. **Iterate the prompt, not the tool.** Scott Logic's fix wasn't a different agent — it was a narrower prompt. Treat a failed first run as a prompt bug.
6. **Ship evidence, not verdicts.** hubble rewrote their Dependabot skill's last step from "decide whether to merge" to "assess the risk" — the agent assembles the case, the human keeps the decision.

## Scott Wu's internal top-5 (from the Lenny's interview)

The tasks Cognition itself delegates most: **frontend fixes, version upgrades, documentation, incident response, testing** — plus a "first line of defense" pattern where Devin analyzes crashes before humans engage, and DeepWiki research to *write better prompts*.

## Deep dives — what to copy, what to watch

**hubble's Dependabot loop.** Every Dependabot PR triggers a Devin session driven by a Skill file: it reads the diff, lockfile changes, release notes and CI state, then comments a GREEN/YELLOW/RED risk label *plus the evidence* — updated libs and update type, risk class with rationale, compat findings, CI status, and what a human should still check by hand. Why it works: the Skill encodes "what risk means here" (which gems are critical, what to verify even on green CI) — tacit reviewer knowledge, now in a file the whole team can read and grow. They deliberately deleted the "decide whether to merge" step in favor of "assess the risk." Copy: write your review procedure as a Skill first — if you can't write the procedure, the automation can't run it. Watch: labels alone decay; without the reasoning comment the system teaches nothing.

**hubble's weekly cost loop.** A weekly Datadog CCM pass: Devin picks one cost-reduction candidate, digs into config and usage, and hands back a decision-ready report. The loop's product is a *candidate with a recommendation*, not a bill. Copy: "pick one candidate, dig, hand over" generalizes to any standing hygiene queue. Watch: first-party tools (AWS cost tooling) overlap — this wins when your cost data lives in Datadog and the fix needs repo context.

**SMARTCAMP's scan→fix pipeline.** Scheduled GitHub Actions pull ECS images → Trivy scan (HIGH/CRITICAL, OS packages) → file issues → Devin remediates. The details worth stealing are the hardening, not the arrow: the AWS-credentialed pull job and the unprivileged scanner job are split so only artifacts cross; they wait ~7 days after a release before trusting results (scanner databases lag fresh packages); image digests are hash-pinned with a PR check that flags stale hashes. Watch: this is defense-in-depth against the scanner itself as supply-chain surface — copying only "scan → Devin" misses the point.

**canly's analyst deployment.** Devin classified ~700 historical support tickets stuck in the "cause unidentified" bucket. Over half weren't bugs at all — and the exercise's real output was a map of what context the AI still needs (docs, DB visibility, ticket metadata), not the labels. Copy: Devin-as-analyst is a first-class use — point it at the pile nobody ever classified before buying tooling. Watch: the bottleneck is context selection, not model quality.

## Verify it

- [ ] Pick one report closest to your own stack and re-read the original, not the distillation — does the number still hold in context?
- [ ] Write down the one lesson you'd bet money on reproducing in your org; if you can't name it, pick another report

## Pitfalls

- **Survivorship bias.** The glowing reports publish numbers; the quiet failures publish nothing. Read the failures in this collection as the median experience, the wins as the ceiling.
- **Cargo-culting.** Scott Logic's prompt iteration worked *because* they iterated — copying their final prompt without their loop gets you their start, not their result.

## Knowledge check

1. What do the failure reports have in common that the success reports lack? *(Unverifiable delegation — the failures gave Devin work where nobody could check 'done'; every success defined a check.)*
2. Why is Faros's 'debugging on a customer call' a deployment lesson, not an anecdote? *(It shows the live-triage motion: the agent as first responder while the human keeps the customer relationship.)*
3. Why does this guide count a hostile report as a source on equal footing? *(Adversarial reports surface the boundary conditions — you learn the map's edges from people who walked off them.)*

## Sources

- [Scott Logic — Rapid development with Devin](https://blog.scottlogic.com/2025/10/20/rapid-development-with-devin.html)
- [Lenny's Newsletter — Scott Wu on Cognition's internal Devin usage](https://www.lennysnewsletter.com/p/how-devin-replaces-your-junior-engineers)
- [Every — Coding with Devin](https://every.to/chain-of-thought/coding-with-devin-my-new-ai-programming-agent)
- [dev>notes — Devin vs Claude Code](https://web.archive.org/web/20260718112612/https://mohitkhare.me/blog/devin-vs-claude-code/)
- [Faros — Devin for live troubleshooting](https://www.faros.ai/blog/how-to-use-devin-ai-troubleshooting)
- [Medium — Copilot, Cursor or Devin weekend](https://medium.com/@sambhavgaur_70582/copilot-cursor-or-devin-my-hands-on-weekend-with-ai-that-codes-and-deploys-acc708e802b3)
- [Bootcamp — Day 7 with Devin (Tailwind/DaisyUI migration)](https://medium.com/design-bootcamp/day-7-of-30-getting-to-know-devon-ai-and-working-with-him-743c351cd0c4)
- [architect to CTO — The only coding agent worth paying for](https://architecttocto.substack.com/p/the-only-coding-agent-worth-paying)
- [expectedwrong — Devin, appraised](https://expectedwrong.com/devin-appraised) · [dev.to — 10 real tasks, 3 completed](https://dev.to/alanwest/i-gave-devin-10-real-tasks-it-completed-3-3063) · [amillionmonkeys](https://www.amillionmonkeys.co.uk/blog/ai-coding-tools-small-studios)
- [Signadot — Testing Devin's changes end to end](https://dev.to/signadot/test-devins-changes-end-to-end-with-signadot-a0)
- [hubble — Dependabot PRs investigated by Devin first](https://zenn.dev/hubble/articles/88429bd24db476) · [hubble — Datadog CCM × Devin weekly cost ops](https://zenn.dev/hubble/articles/091e29a0c86ec3) (JP)
- [SMARTCAMP — Trivy scan → Devin remediation pipeline](https://zenn.dev/smartcamp/articles/97ac804043530e) (JP)
- [canly — Classifying ~700 support inquiries with Devin](https://zenn.dev/canly/articles/9c19bb123e208c) (JP)
- [smasato — Maximizing Devin: tips for success](https://zenn.dev/smasato/articles/6aebb0da2f56eb) (JP/EN)
