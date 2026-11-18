# Bot outcome prompts, dissected

**Goal:** write outcome prompts the way the documented deployments actually did — ownership of an area, not a task list.
**Level:** intermediate · **Time:** 20 min to draft, a week to calibrate

Every public bot deployment that produced big numbers started with a short prompt assigning an *outcome*. This guide collects the real ones and reverse-engineers why they work.

## The exemplar

> *"your job is to product manage the android app"*

The Android Bot's entire assignment. One sentence produced 44 days of self-directed work: the bot decomposed the outcome into tickets it wrote itself, ran a Devin session per ticket, and shipped 1,134 merged PRs ([launch post](https://devin.ai/blog/introducing-devin-bots)). Note what the prompt does **not** contain: no ticket list, no acceptance criteria, no schedule. The outcome itself implies all of them.

## The anatomy of a working outcome prompt

| Element | What it does | Example |
| --- | --- | --- |
| **A role** | Tells the bot how to *behave*, not just what to produce | "product manage", "own the QA of onboarding flows" |
| **A bounded surface** | A scope the bot can fully see — an app, a check, a data source | "the android app", "layout regressions", "30+ onboarding flows" |
| **An implicit definition of done** | A state the bot can verify itself against | "feature parity with iOS", "no layout-shift regressions", "every flow green" |
| **Standing authority** | The bot decides *when* and *what next* — that's what makes it a bot, not a script | "your job is to…", "keep…", "watch for…" |

## Patterns from the official template marketplace

The 16 [marketplace templates](https://devin.ai/bots/templates) all follow the same grammar. Reusable formulations, generalized:

**Ownership of a domain** — "Find bugs, improvements, performance and refactoring work in a named product area; open one small PR at a time with proof it works." (Software Factory)

**Ownership of a check** — "Every 3 hours, build production main, simulate first/repeat/deferred visits, and file fixes with before/after videos for any regression you introduce—or find." (Layout Bot pattern)

**Ownership of a lifecycle stage** — "Take a ticket or an ask to a tested PR and through review." (Product Engineer)

**Ownership of a cadence** — "Weekly: remove dead code, one safe PR per round." (Code Reaper) — scheduled outcomes are stated as a rhythm, not a trigger.

**Ownership of team metabolism** — "Watch the channels, post updates, hand work to the right teammate, follow up until done." (Chief of Staff)

**Ownership of hygiene** — "Old flags, stale deps, CVEs — turned into small safe PRs." (Code Health Engineer)

## Multi-bot orgs: prompts that grant authority

In fleets (SuperJennyStack, Frankie, tigsbot) the chief bot's prompt contains the *routing contract*: which bot owns which surface, and when to escalate upward instead of sideways. The human's real prompt is the roll-up spec: "bring me every open decision in one thread." See [Guide 4](bots-203-multi-bot-org.md) for the full org chart.

## Anti-patterns

- **Task-shaped prompts.** "Fix these 12 issues" — the bot finishes and idles; you get a session, not a bot.
- **Unverifiable outcomes.** "Make the app better" — no self-check means the bot's only exit is Needs-you spam.
- **Hidden scope.** If the outcome requires systems the bot can't see (a staging env it can't reach, a dashboard it can't read), it will either stall or hallucinate progress. Give it the surface or shrink the outcome.
- **No merge authority story.** The 88% self-merge rate exists because CI and review gates were pre-configured for autonomous merges. State it: "merge when CI is green and diff < N lines" or "always open as draft for human review."

## Drafting yours — the three-line test

A good outcome prompt answers, in order:

1. **What is yours?** — the surface
2. **What does good look like?** — the verifiable state
3. **What do you do about it?** — the standing behavior

If a stranger couldn't check line 2's truth from outside, tighten it.

## Verify it

- [ ] Take a real backlog item from your repo and rewrite it as an outcome prompt — surface, verifiable state, standing behavior
- [ ] Show it to someone who doesn't know the codebase: could they tell from outside when the Bot is "winning"?
- [ ] The Bot's first reply should be a plan or clarifying questions about scope — if it asks "what do you want me to do first," the prompt didn't assign ownership

## Pitfalls

- **A task list wearing an outcome costume.** "Do X, then Y, then Z" is still a checklist — the Bot can't re-prioritize when the world changes.
- **"Keep the app good" with no definition of good.** Without a verifiable state, the Bot picks one — and it won't be yours.
- **Scope wider than one surface.** "Own engineering" fails; "own the iOS app" ships. Split by what a single outsider could fully observe.

## Knowledge check

1. Why does "own the Android app" work better than "fix Android bugs"? *(Ownership implies standing judgment — the Bot decides which bugs matter, not just whether to fix.)*
2. What's wrong with "make the CI fast"? *(Not verifiable from outside — no threshold. "CI under 8 minutes" is.)*
3. Which of the three questions does "text me if tests fail" answer? *(Standing behavior — it says what the Bot does about the state, nothing about the surface or the goal.)*

## Sources

- [Introducing Devin Bots](https://devin.ai/blog/introducing-devin-bots) · [Bots docs](https://docs.devin.ai/work-with-devin/bots) · [Template marketplace](https://devin.ai/bots/templates)
- Deployment reports linked in [built-with-devin](https://github.com/Till3005/built-with-devin#documented-deployments)
