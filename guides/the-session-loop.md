# Guide 19 — The session loop: research, delegate, review, and what it costs

**Goal:** Run the full Devin loop end to end — understand the codebase before you brief, delegate a scoped session, get an independent review on the PR, and read Session Insights so the next loop is cheaper.
**Level:** Start here (pairs with [Guide 18](talking-to-devin.md))
**Sources:** [Devin University — Cloud 101/103](https://learndevin.com) · [DeepWiki docs](https://docs.devin.ai/work-with-devin/deepwiki) · [Ask Devin docs](https://docs.devin.ai/work-with-devin/ask-devin) · [Devin Review docs](https://docs.devin.ai/work-with-devin/devin-review) · [Session Insights docs](https://docs.devin.ai/product-guides/session-insights)

## The loop most people skip half of

Guide 18 teaches you to write a brief Devin can't misread. Devin University's Cloud track wraps that brief in the loop that produces it and consumes its output:

```
Understand ──► Delegate ──► Review ──► Learn
 DeepWiki      brief+session   Devin Review   Session Insights
 Ask Devin                      on the PR     → better next brief
```

Most failed sessions fail at the ends, not the middle: the brief was written blind about the codebase, or the PR was merged on vibes. This guide covers the two ends and the meter that runs under all of it.

## Understand: DeepWiki and Ask Devin before you spend an ACU

**DeepWiki** auto-indexes your connected repos and generates a wiki per repo — architecture diagrams, summaries, source links, configurable via `.devin/wiki.json`. It answers the questions you'd otherwise spend session time discovering: where does this module live, what calls it, what's the established pattern.

- Effort levels are set per org (overridable per repo): **Low is free** and the default; Medium runs ~5–10 ACUs per wiki, High ~20–40. Low is enough for briefing support in most repos.
- Onboarding indexes repos you set up automatically; add others under **Settings → DeepWiki**.
- For public repos, [deepwiki.com](https://deepwiki.com) is the free version — index any public GitHub repo, get the same diagrams and Q&A, no account. There is also a DeepWiki MCP for your other agents.

**Ask Devin** is the conversational layer on top of that index — at [app.devin.ai/search](https://app.devin.ai/search):

- **Ask mode**: questions about your code answered with code citations, grounded in the index — "how does retry work in the billing poller" returns the file, the call sites, the pattern.
- **Plan mode**: describe the change, and Devin scopes it with you — then generates a context-rich prompt ready to hand to a session. This is the single cheapest way to satisfy Guide 18's rules: the where-to-start and the reference pattern come out of the index instead of your memory.
- Start the session from inside the conversation, and its status stays visible there — no context switch.

The doctrine pays off twice here: a brief informed by indexed facts is both more specific *and* shorter.

## Delegate — the step you already know

Hand off the Ask-Devin-generated prompt (or your own brief per [Guide 18](talking-to-devin.md)) as a scoped session. Everything that changes is what the brief already knows: the files, the pattern, the check, the boundary.

## Review: a second agent on every PR

**Devin Review** is an independent reviewer, not a rerun of the session's own opinion:

- Trigger per-PR: comment `/devin review` on a GitHub PR or GitLab MR, or open the PR in [Devin Review](https://app.devin.ai/review). It groups related changes, explains them alongside the diff, and surfaces bugs and security findings you can quote into chat — including asking Devin to fix in place.
- Org-wide: auto-review, review instructions, and cost controls exist for running it on every PR. Review 2.0 (Nov 2026) cut per-PR cost **82%**, which is what makes always-on economically sane.
- Use it on Devin's own PRs too. The writer and the reviewer being different agents is the point — the same asymmetry Guide 18 assigns you vs. the session.

## Learn: Session Insights and the ACU meter

Every completed session gets a **Session Insights** read (menu **⋯ → Session insights**, free):

- **Session size chip** — XS–XL classification auto-generated at teardown; L/XL sessions get a full analysis automatically, smaller ones on demand.
- **ACU usage** (or on-demand dollars on quota plans) — compare similar tasks to spot sessions that burned compute on retries and dead ends.
- **User messages** — a high count means the brief lacked context; each message is a course correction you could have written upfront.
- The analysis recommends concrete improvements — tighter prompts, missing knowledge, wrong scope. The goal stated in Cloud 103 is the right one: *make every session cheaper than the last.*

Cost hygiene that shows up in every field report: scope sessions narrowly, kill idle ones (thinking and waiting both bill), and check quota before kicking off a fleet — the 100 Days operator burned **33% of his weekly quota in two days** of Bot setup ([field reports](community-field-reports.md)). Community-reported caveat on Bots specifically: wiring your *own* model key into a Bot's child sessions does **not** stop the plan's weekly quota from draining — the Bot's own reasoning plus cloud compute still bill to the plan ([linux.do report](https://linux.do/t/topic/3225152), zh).

## Verify it

- [ ] You can answer "where does X live and what calls it" from DeepWiki/Ask Devin *without* starting a session.
- [ ] Your next brief contains at least one fact you learned from the index, not from memory.
- [ ] A Devin Review ran on the last PR you touched — yours or Devin's.
- [ ] You can read your last session's size, ACUs, and message count, and name one thing the analysis flagged.

## Pitfalls

- **Briefing blind.** Writing prompts from memory of the codebase you haven't opened in months — the index knows more than you do now. Two minutes in Ask Devin beats a mid-session correction.
- **Skipping review because CI is green.** CI checks what you thought to check. Review reads the diff itself; they're different nets.
- **Reading Insights only on failures.** The expensive pattern is the mediocre session you repeat every week. Review successes too — that's where the repeatable brief lives.
- **Effort-level overspend.** High-effort wikis on repos you only touch quarterly; per-repo override exists for a reason.

## Knowledge check

1. *Why start a session from Ask Devin instead of the Devin sidebar?* Because Plan mode grounds the prompt in indexed code — the where-to-start, the existing pattern, and the checkable surface all come from the repo itself, so the session opens with the context you'd otherwise type or discover mid-run.
2. *The session's own report says the work is done and tested. Why run Devin Review?* Independence. The session graded its own homework; Review is a different agent reading the diff with fresh context — same reason a teammate's PR doesn't get self-approved.
3. *ACUs are flat and a session came in at XL. What do you check first?* User-messages count in Session Insights — a large session driven by many small corrections is a briefing problem, not a task-size problem. Split or re-brief before assuming the work was just big.

## Sources

- [Devin University](https://learndevin.com) — Cloud 101 (this loop) and Cloud 103 (efficiency) courses; free lessons, exams need an Enterprise seat
- [DeepWiki](https://docs.devin.ai/work-with-devin/deepwiki) + [Ask Devin](https://docs.devin.ai/work-with-devin/ask-devin) — indexing, effort levels, Plan mode, [deepwiki.com](https://deepwiki.com) for public repos
- [Devin Review](https://docs.devin.ai/work-with-devin/devin-review) — `/devin review`, auto-review, [Review 2.0 cost cut](https://devin.ai/blog/devin-review-2)
- [Session Insights](https://docs.devin.ai/product-guides/session-insights) — XS–XL sizing, ACU/message metrics, API
- Next: [Guide 18 — Talking to Devin](talking-to-devin.md) if you haven't · [Guide 9 — Playbooks](playbooks-and-knowledge.md) to make the improved brief permanent
