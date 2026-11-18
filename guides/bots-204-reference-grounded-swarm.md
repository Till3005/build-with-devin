# Guide 5 — Reference-grounded swarm

**Goal:** direct a swarm of agents to write a large, *verifiable* system — where correctness is checked continuously against a trusted reference, not against vibes.
**Level:** advanced
**Source deployment:** Harvey's **"Phil"** — ~30 agents wrote a collaborative, Word-compatible editor engine in Rust + TypeScript: **1M+ lines in 3 weeks, zero human engineers**. Verified continuously against real Microsoft Word behavior and simulated lawyer negotiations. Humans steered through memory + decision logs, never by reading code.
**Sources:** Gabe Pereyra's launch write-up ([via @gabepereyra](https://x.com/gabepereyra)) · [launch post](https://devin.ai/blog/introducing-devin-bots)

## The pattern

A swarm fails when nobody can tell whether the output is right. Phil worked because every line could be checked against a **reference of truth**: real Microsoft Word. The agent team's job was *matching* — an objective, continuously checkable target — not *inventing*.

```text
   reference system (truth)
            ▲ compare
            │
┌───────────┴────────────┐
│  swarm of ~30 agents   │──► 1M+ LOC (Rust + TypeScript)
└────────────────────────┘
            ▲ steer
            │
   humans: memory + decision logs
   (never reading the code)
```

## When to use it

| Good fit | Bad fit |
| --- | --- |
| Reimplementing a spec (file format, protocol, editor, compiler) | Greenfield products with no objective answer |
| Porting/migration with an oracle (old system still runs) | Novel UX where "right" is a judgment call |
| Anything diff-able against a working system | Systems where correctness needs users |

The litmus test: **can a machine decide "correct" without you?** If yes, a swarm can scale; if no, use a product-owner Bot (Guide 2) instead.

## Step 1 — Secure the reference first

Before any agent writes code, the check must exist:

- Harvey's reference: **real Microsoft Word behavior** — documents rendered in the swarm's editor had to match Word
- Yours might be: the legacy system still running, a conformance suite, golden files, a spec test corpus, an API contract

Put the comparison in CI or a script the swarm runs constantly — "does output match reference" must be cheap and automatic, or agents drift between checks.

## Step 2 — Decompose into owned slices

~30 agents didn't share one backlog — the work was sliced so each agent owned a subsystem (document model, layout engine, collab protocol, …). Structure it like Guide 4's org chart, except every "employee" is a coding session pointed at a module boundary:

```text
You own the <module>. Its contract is <interface/reference behavior>.
Your PRs are accepted when the reference checks pass — not when the
code looks done.
```

## Step 3 — Humans steer above the code

Nobody at Harvey read the million lines. Steering happened through:

- **Memory** — the Bot's accumulated facts about decisions made and why
- **Decision logs** — what the swarm chose at each fork
- **Direction messages** — "prioritize track-changes fidelity over performance this week"

Your review surface is the *decision trail*, not the diff. If you find yourself reading generated code to know what's happening, ask the orchestrator for the decision log instead.

## Step 4 — Adversarial validation on top

Harvey layered a second check: **simulated lawyer negotiations** — realistic use that surfaces what a conformance suite misses. Your equivalent: a scenario layer above the reference diff — real workflows, adversarial inputs, fuzzing. Reference checks catch *wrong*; scenario checks catch *brittle*.

## Verify it

- [ ] An automated reference check exists and runs against every change
- [ ] Each agent's acceptance criterion is "reference passes," never "code written"
- [ ] You can answer "what did the swarm decide and why" from logs/memory without reading code
- [ ] A deliberately broken module is caught by the reference check, not by you

## Pitfalls

- **Scaling before the oracle.** A swarm without a check just produces volume — Phil worked because Word was always the judge.
- **Reviewing diffs.** It doesn't scale past ~2 agents; you'll become the bottleneck and lose the swarm's speed advantage.
- **Ambiguous ownership.** Two agents editing one module produce merge hell — ownership boundaries are the architecture.

## Sources

- [@gabepereyra](https://x.com/gabepereyra) — Harvey's Phil write-up: ~30 agents, 1M+ LOC, Word-reference verification, lawyer simulations
- [Introducing Devin Bots](https://devin.ai/blog/introducing-devin-bots)
- Related: [Guide 4 — Multi-Bot organization](bots-203-multi-bot-org.md) (same hierarchy, different purpose: operations vs. construction)
