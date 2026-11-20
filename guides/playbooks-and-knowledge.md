# Guide 9 — Playbooks & knowledge: encoding your org's conventions

**Goal:** make Devin sessions and Bots reliable at org scale by writing down what your best engineers assume — as playbooks (repeatable procedures) and knowledge (standing context).
**Level:** intermediate · the layer every big published deployment shares
**Sources:** [docs.devin.ai](https://docs.devin.ai) · deployment lessons from [Guide 7](enterprise-playbook.md)

## Why this layer decides everything

Every published enterprise result — Nubank's 8–12×, EBANX's 92% authored-PRs, Wayfair's 1,600 seats — rests on encoded conventions. Without them, Devin's output varies by session: each one rediscovers your stack, your merge rules, your test habits. With them, session #500 behaves like your best engineer on their best day.

Two complementary artifacts:

| Artifact | What it is | Analogy |
| --- | --- | --- |
| Knowledge | Standing context Devin reads — repo facts, conventions, environment gotchas | Onboarding docs |
| Playbook | A named, repeatable procedure — trigger, steps, acceptance criteria | A runbook anyone can invoke |

## Step 1 — Mine your own corrections

The cheapest knowledge already exists: scroll your last 20 Devin sessions and collect every time you typed a correction — *"we deploy via Cloud Run,"* *"never `git push --force`,"* *"tests need `npm run db:seed` first."* Each correction is a knowledge entry with proof it mattered.

Also mine:
- Code review comments humans keep repeating on Devin PRs
- PR descriptions that explain *why* a change was shaped a certain way
- Onboarding docs — anything you'd tell a new hire

## Step 2 — Write knowledge entries that stick

Good entries are one line, imperative, and scoped:

```text
- Deploy only via `make deploy-cloudrun` — never run gcloud directly.
- Migrations require a matching rollback file in prisma/rollbacks/.
- The staging seed user is qa+admin@corp.io; never create real-looking users.
```

Bad entries are essays, wishes ("write good tests"), or secrets (never put credentials in knowledge — use the secrets store).

## Step 3 — Playbooks for repeatable work

> **Platform note (Nov 2026):** Playbooks are moving to **Skills** — accounts are migrating one at a time and new accounts get Skills only (each playbook becomes a skill with the same org/enterprise scope). Everything in this step applies verbatim to skills: a skill is the same named, invocable procedure.

A playbook packages a procedure so any session (or Bot) runs it the same way. Structure that works:

```markdown
# <Verb + object> — e.g. "Cut a release"
## When to use
<the trigger condition>
## Steps
1. <deterministic step>
2. ...
## Acceptance
<the pass/fail check>
## Failure modes
- <known break → what to do>
```

Publish it org-wide so sessions, automations, and Bots can all invoke it — this is what turns a one-off successful session into an org capability.

## Step 4 — Feeding Bots

Bot **Instructions** (Guide 1) are the Bot-scoped version of knowledge — the rules read at every session start. Put job-law there; put org-law in knowledge; put procedures in playbooks. The layering keeps each artifact small and current.

## Step 5 — The correction loop

Knowledge rots. The loop that keeps it true:

1. A session/Bot makes a mistake → you correct it in chat
2. The Bot writes the correction to memory (or you add it to knowledge)
3. Weekly review: promote repeated Bot-memory items into org knowledge; delete entries nobody's triggered in a month

Devin Coach (an official Bot template) exists for exactly this — it reports weekly where Devin got stuck and proposes one fix each time: a note, a skill, or a setup change.

## Verify it

- [ ] A fresh session on your repo asks zero questions your knowledge already answers
- [ ] The last correction you gave a Bot appears in its memory files
- [ ] Two different sessions run the same playbook and produce the same-shaped result

## Pitfalls

- **Writing wishes.** "Follow best practices" changes nothing; "run `npm run db:seed` before tests" changes everything.
- **Set-and-forget.** Stale knowledge is worse than none — Devin follows it confidently. Review monthly.
- **Duplicating docs.** Knowledge should hold what Devin *gets wrong* or *can't know*, not a copy of your wiki.

## Knowledge check

1. What's the difference between a playbook and knowledge? *(A playbook is a repeatable procedure for a named task; knowledge is standing context every session should assume.)*
2. Why is 'write down what your best engineers assume' the actual enterprise bottleneck? *(Agent quality was never the limiter — missing context is; the knowledge layer is where org conventions live.)*
3. When does a convention become a playbook vs. staying tribal knowledge? *(The first time a session gets it wrong in a way a written step would have prevented.)*

## Walkthrough — knowledge that sticks, on Devin CLI v3000.14 (swe-2-flash-medium)

Org playbooks live in the cloud, but the core claim of this guide — *write the convention once and every session follows it* — is testable locally. `devin rules` reads always-on context blobs from `.windsurf/rules/*.md`. We mined three "past corrections" into `house-rules.md` — run tests with unittest (never pytest), never commit, reuse `total()` for item math — then opened a fresh session and asked only for a feature.

**Video (30 s, silent):** the rule file → an unprompted session → all three rules obeyed.

[![House rules file, one unprompted feature request, every rule followed]({B}/walkthrough-poster.webp)]({B}/walkthrough.mp4)

![1. The mined rules and the bare prompt — "Add a line_total(items) function … Write a test for it too."]({B}/step1-rules-and-prompt.webp)
*1. Three house rules committed; the prompt says nothing about conventions*

![2. It reused total(), ran `python3 -m unittest` (not pytest), all 3 tests pass]({B}/step2-rules-obeyed.webp)
*2. Every rule obeyed with zero reminders — that is the knowledge layer working*

![3. After /exit — `M orders.py`, `M tests/test_orders.py`, and `git log` shows only the init commit]({B}/step3-no-commits.webp)
*3. Even "never commit" held — verified from git, not from its report*

## Sources

- [docs.devin.ai](https://docs.devin.ai) — knowledge, playbooks, Bot instructions/memory
- Related: [Guide 7 — Enterprise rollout patterns](enterprise-playbook.md) (this layer is the step most rollouts skip)
