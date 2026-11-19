# Guide 18 — Talking to Devin: the prompting doctrine

**Goal:** Write instructions Devin can't misread — the difference between a session that ships and one that wanders.
**Level:** Start here
**Sources:** [Coding Agents 101](https://devin.ai/agents101) (Cognition, June 2025) · [Instructing Devin Effectively](https://docs.devin.ai/essential-guidelines/instructing-devin-effectively) — both official, both distilled below with field notes

## Why this guide is first

Every other guide in this repo assumes one skill: you can tell Devin what you want in a way it can't misread. Cognition's own guidance — *Coding Agents 101* and the docs' *Instructing Devin Effectively* — says the same thing from two angles: **the engineers who get the most out of agents write like they're briefing a junior teammate, not like they're filing a wish.** This guide is that doctrine, condensed and wired to the rest of the curriculum.

## The four rules that carry everything else

**1. Say how, not just what.** "Fix the C++ bindings for our search module to pass the new unit tests — be careful, you'll need to recompile the bindings each time before testing." You know the traps in your codebase; name them. Open-ended briefs ("make the app look better", "improve database performance") return open-ended results.

**2. Tell it where to start.** Repo, directory, file, reference implementation, docs URL — anything you'd want if the task landed on *your* desk. "Use `authTemplate.rs` as a reference to maintain consistency in error handling" beats a style paragraph every time.

**3. Define success as something checkable.** Not "make sure it works" — a check Devin can run: *endpoint returns 200 with fields X/Y/Z*, *component renders with zero console errors at 1440px and 375px*, `npm test` green. Devin has a full machine — browser, shell, IDE. Tell it to verify its own work ("run `npm run dev` and confirm `/settings` renders") and it will QA before you ever see the PR.

**4. Give it feedback loops, not feedback vibes.** Type checkers, linters, tests, CI — the agent's superpower is iterating against error messages. If your repo can't tell it when it's wrong, you're the feedback loop, and that's the expensive configuration.

## The reference brief

Cognition's own model prompt, annotated:

> In the Devin repo, build a tool that monitors RAM and CPU usage of the remote machines Devin runs on. — *scope and purpose, one line*
>
> - Create a background task that launches when devin.rs starts — *step-by-step, not a blob*
> - It opens a connection to all forked remote machines and monitors usage — *mechanism named*
> - If usage exceeds 80%, emit a new type of Devin event (check how we use Kafka) — *success criterion + pointer to existing pattern*
> - Architect so it doesn't block other operations — *constraint the author already knows*

Notice what's absent: aesthetic opinions, hedging, "maybe", "if you think it's a good idea". Every line is a decision already made by a human who knows the system.

## Defense: what to keep for yourself

The 101 guide is blunt about the limit: **expect ~80% time savings on large tickets, not full automation.** For anything beyond a few files, plan for multiple feedback cycles. The winning posture is *architect reviewing a junior's draft PR* — you hold correctness, Devin holds keystrokes.

Practical consequences:

- **Scope hard.** "Do not merge, deploy, or touch billing without asking me" — write the fence explicitly, don't rely on implied sense.
- **Split big work into verifiable sub-tasks** — one session per sub-task, each with its own success check (this is also why Guide 11's migration pattern works: hundreds of small PRs, each verifiable).
- **Use Skills for the repeatable** — anything you'll ask more than twice goes in a `SKILL.md`; Devin invokes it automatically (Guide 16).

## From instructing to owning

A session instruction answers *"do this task well"*. A Bot outcome prompt answers *"own this area"*. The doctrine is the same — specificity, boundaries, checkable success — but the object changes from a task to a responsibility. Once you're fluent here, [the outcome-prompts reference](bot-outcome-prompts.md) shows how the same muscles produce the Android Bot's 1,134 PRs.

## Walkthrough — recorded on Devin CLI v3000.14 (swe-2-flash-medium)

The doctrine run live on a throwaway `demo-repo`: a four-line brief — scope + mechanism, named files, a checkable success line, an explicit boundary. One session, zero mid-flight clarifications, self-verified.

**Video (90 s, no audio):** brief → edits → permission prompts → self-check → boundary honored.

[![SWE-2 Flash Medium finishing the task — 5 unittest tests green, no commit made](https://till3005.github.io/built-with-devin/assets/guides/talking-to-devin/walkthrough-poster.webp)](https://till3005.github.io/built-with-devin/assets/guides/talking-to-devin/walkthrough.mp4)

![1. The CLI REPL on SWE-2 Flash Medium, composer ready in demo-repo](https://till3005.github.io/built-with-devin/assets/guides/talking-to-devin/step1-repl-flash.webp)
*1. The CLI REPL on SWE-2 Flash Medium — composer ready in demo-repo*

![2. The brief — four doctrine rules in four lines: how, where, success check, boundary](https://till3005.github.io/built-with-devin/assets/guides/talking-to-devin/step2-the-brief.webp)
*2. The brief — four doctrine rules in four lines: how, where, success check, boundary*

![3. Mid-run: writing test_app.py; the permission prompt offers Allow / accept-edits / bypass / deny](https://till3005.github.io/built-with-devin/assets/guides/talking-to-devin/step3-edits-approval.webp)
*3. Mid-run: writing test_app.py — the permission prompt offers Allow / accept-edits / bypass / deny*

![4. The agent requests exactly the named check: python3 -m unittest -v](https://till3005.github.io/built-with-devin/assets/guides/talking-to-devin/step4-self-check-prompt.webp)
*4. Self-verification: the agent requests exactly the named check — `python3 -m unittest -v`*

![5. Done — 5 tests all OK; the report itself says "No commit made."](https://till3005.github.io/built-with-devin/assets/guides/talking-to-devin/step5-tests-green.webp)
*5. Done — 5 tests all OK; the report itself confirms the boundary: "No commit made."*

![6. After /exit — `devin -r` resume hint; git status shows both files modified, zero new commits](https://till3005.github.io/built-with-devin/assets/guides/talking-to-devin/step6-no-commit.webp)
*6. After /exit — the `devin -r` resume hint, and `git status` proving the fence held: two modified files, no new commit*

## Verify it

- [ ] Given a real task from your backlog, you can write a brief with: named repo/files, a reference pattern, an explicit success check, and a stated boundary — in under 10 minutes.
- [ ] The resulting session completes without a mid-flight clarification you'd call obvious.
- [ ] Devin verifies its own work before the PR — you asked it to in the brief.

## Pitfalls

- **Prompts that encode your own confusion.** If you can't state the success check, the task isn't ready — co-develop a PRD with Devin first (the 101 guide endorses this) rather than hoping it intuits the goal.
- **Under-permissioned ambition.** "Fix CI" from an account that can't see CI produces confident wrongness. Match the brief to the access you actually granted.
- **Reviewing output, not correctness.** A green test run and a plausible diff are evidence of progress, not proof the behavior is right. You still own verification.

## Knowledge check

1. *"Add unit tests" fails where "add unit tests for the retry path in `poller.ts`, mocking `fetch`, covering timeout and 5xx" succeeds — why?* Because the second brief removes the agent's need to make judgment calls you'd want made your way: what to test, which edges matter, what to mock. Every unspecified decision is a coin flip you don't control.
2. *Devin opened a PR with a clean diff and green CI. Done?* Not yet — CI green means the checks passed, not that the intent is met. The last verification layer is still yours; that asymmetry is the deal (~80% savings, human on correctness).
3. *When do instructions graduate to Skills?* When you catch yourself re-typing them. A third occurrence is a SKILL.md — Guide 16 covers the format and discovery paths.

## Sources

- [Coding Agents 101](https://devin.ai/agents101) — Cognition's prompting doctrine: say-how, where-to-start, defensive prompting, feedback loops, the 80% rule
- [Instructing Devin Effectively](https://docs.devin.ai/essential-guidelines/instructing-devin-effectively) — the official do/don't list and the reference brief dissected above
- [Devin tutorial library](https://docs.devin.ai/tutorial-library) + [Devin University](https://devin.ai/university) — official videos and courses if you want the same material in another medium
- Field note: every report in [community field reports](community-field-reports.md) converges on the same conclusion — briefs, not wishes
- Next: [Guide 1 — Your first Bot](bots-101-first-bot.md) (same doctrine, bigger object) · [Outcome prompts reference](bot-outcome-prompts.md)
