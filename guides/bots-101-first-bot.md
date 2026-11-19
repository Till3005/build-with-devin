# Guide 1 — Your first Bot

**Goal:** create a Devin Bot that owns an outcome, and learn the six mechanics every later guide builds on.
**Level:** start here · **Time:** ~15 minutes
**Source:** [official Bots docs](https://docs.devin.ai/work-with-devin/bots), [launch post](https://devin.ai/blog/introducing-devin-bots)

## What a Bot is

A session does one request. A Bot *owns an outcome*: you state the goal once in its chat, it plans the work, starts a child Devin session for each piece, monitors them, and only brings you what needs your judgment. It persists — memory, sessions, and automations survive across weeks.

The six mechanics, in the order you'll meet them:

| Mechanic | What it is | Where you touch it |
| --- | --- | --- |
| Chat | One thread for everything the Bot owns — goals, reports, questions | The Bot's page / Slack / iMessage |
| Sessions | Each piece of work runs as its own Devin session on its own machine | Spawned and monitored by the Bot |
| Needs you | Decisions, PR reviews, permission requests, reports — one list | Top of the Bot's chat |
| Memory | What the Bot learns, saved as files, read at every session start | Settings → Memory |
| Instructions | Standing rules people write, read at every session start | Settings → General |
| Access | The Bot's own connections/secrets, plus grants between Bots | Settings → Access |

## Step 1 — Create it

Sidebar → **Bots** → *Create new Bot* → pick a template or *Start from scratch* → name it.

A new Bot is private to you until you share it. Its usage counts against your plan like any session.

> Tip: a template ships with instructions for one job (QA Engineer, Data Analyst, …). *Start from scratch* is the right choice for the guides in this repo — you'll write the outcome prompt yourself.

## Step 2 — Assign the outcome

The first message is the most important input a Bot ever gets. Give it a *goal*, not a task:

```text
You own the Android app now. Keep it at feature parity with iOS.
```

That's the verbatim prompt Cognition's Android Bot started from. Compare:

| Weak (a task) | Strong (an outcome) |
| --- | --- |
| "Fix the checkout button" | "You own checkout. Keep it fast, correct, and covered by tests." |
| "Update the docs" | "You own the docs. Keep them in step with `main`." |
| "Watch CI" | "You own build health on `main`. When a check regresses, find the cause and fix it." |

A task ends when it's done; an outcome makes the Bot re-plan forever.

### A bounded first assignment

Ownership is the right *shape*, but bound the *surface* on the first run: one flow, one environment, one reviewer — you. The ANO field guide's pattern is the reliable starter:

```text
Own the newsletter signup check for [project] on staging.
Use [repository], [staging URL] and the test mailbox I provide.
Check the journey from submitting the form to receiving the
correct welcome email and opening its resource link.

Start with one run. Show me the result before proposing a schedule.
If you find a defect, reproduce it, make the smallest suitable fix,
and open a pull request with the evidence.

Do not merge, deploy, email real subscribers, change billing,
or connect another service without asking me.

Return: what passed/failed, screenshots or a short recording,
the PR if a fix was needed, anything you could not verify,
and any decision you need from me.
```

The load-bearing lines: the journey definition (form → email → link, not just "form works"), *one run before a schedule*, the explicit no-merge/no-deploy fence, and the named evidence you expect back. Expand the assignment only after the Bot returns evidence you can trust twice.

## Step 3 — Work with it

After the outcome is set, most of your messages are check-ins:

```text
anything waiting on me?
```

Open **Needs you** (top of the chat) when the Bot flags something:

| Item | Your move |
| --- | --- |
| Decision | Pick an option — the Bot marks its recommendation |
| Review PR / Merge PR | Review or merge |
| Permission request | Approve or reject new access, an automation, a network host, or a usage-limit increase |
| Report / FYI | Read it |

You can reply in your own words, snooze, or dismiss any item.

## Step 4 — Steer through memory, not micromanagement

- **Instructions** (Settings → General): your standing rules — read at the start of every session the Bot runs. Put enduring policy here, not chat.
- **Memory** (Settings → Memory): files the Bot writes itself — preferences, corrections, project facts. To change what it remembers, just tell it in chat ("remember: we deploy via Cloud Run, never bare VMs"). Everyone who can use the Bot can read its memory — treat shared-Bot memory as shared.

The pattern that scales: correct the Bot once, let it write the correction to memory, and every future session inherits it. Cognition merges 2,000+ PRs/week on this loop.

## Before you share it — access and usage

Two things the launch posts skip that the docs spell out:

- **A private Bot inherits your resources without asking.** Access you already have can be recorded as grants with no new permission prompt — a private Bot is not a sandbox. Before sharing, open Settings → Access and strip grants the job doesn't need. If teammates should copy the method without seeing your conversation or credentials, share a *template*, not the Bot.
- **A Bot's usage covers its chat plus every session it spawns.** Max: draws your included quota then on-demand — no separate Bot cap. Teams: your quota then team credits, an admin can set a Bot-specific on-demand cap. Enterprise: counts against the creator's limit unless assigned its own. A spending instruction in chat is not a configured cap — set the limit in Settings, don't describe it in prose.

## Step 5 — Put it where you work

- **Slack:** give the Bot its own Slack app so your team can @-mention or DM it (Settings → Slack). Every reported team deployment runs this way — the Bot becomes a named teammate in a channel.
- **iMessage:** text the Bot from your phone.
- **Web:** the sidebar's Bots section lists yours and the ones shared with you.

## Step 6 — Schedules and modes

- **Automations:** ask in chat — *"run a summary of open PRs every weekday morning"* — and the Bot proposes the automation for your one-time approval. Manage them under Settings → Automations (pause/resume/remove).
- **Modes:** the Bot has its own mode plus a **Child Capability** default for the sessions it spawns (e.g. `Normal / Ultra` in the chat's mode picker). You can also ask for a different mode on any single session.

## Lifecycle

| Action | Effect |
| --- | --- |
| Recycle | Terminates the current session; a fresh one starts next open. In the chat menu. |
| Archive | Stops responses, removes it from Bot lists, removes its Slack app and inter-Bot grants (unarchiving doesn't restore those — you set them up again). |
| Delete | Permanent: settings, sessions, memory, automations. Cannot be undone. |

Only the creator and roles with Manage Bots see Archive/Delete. On Enterprise plans, `Use Bots` / `Manage Bots` / `Manage Bots across the enterprise` are separate permissions in custom roles.

## Verify it

- [ ] Bot created and named; outcome prompt sent in chat
- [ ] Bot started at least one child session without being asked twice
- [ ] A decision/PR/permission request appeared in **Needs you** and you resolved it
- [ ] One correction you gave in chat shows up as a memory file under Settings → Memory
- [ ] (Optional) Bot reachable via @-mention in Slack

## Pitfalls

- **Task-shaped prompts.** "Fix X" produces a session, not a Bot. If the Bot finishes and goes quiet, the prompt was a task — restate it as ownership.
- **Chat for policy.** Rules typed in chat scroll away; rules in Instructions are read every session. Chat = direction and answers; Instructions = law.
- **Ignoring Needs you.** Bots are designed to batch judgment calls — check once or twice a day, not continuously.

## Knowledge check

1. What survives between a Bot's sessions that a one-off session doesn't have? *(Memory — plus the standing outcome, schedules, and surfaces.)*
2. Why does a Bot "needs-you" instead of asking mid-session? *(Judgment goes to one thread asynchronously; the human isn't a blocking call in the loop.)*
3. Which mechanic turns "a smart session" into "an employee"? *(Ownership of an outcome — the goal persists after any single session ends.)*

## Sources

- [Devin Bots — docs](https://docs.devin.ai/work-with-devin/bots) — mechanics, access, usage limits
- [Introducing Devin Bots](https://devin.ai/blog/introducing-devin-bots) — launch post, the Android Bot prompt
- [AI Native Operators — Devin Bots: give an agent a job to own](https://ainativeoperators.ai/blog/devin-bots-guide) — community field guide; the bounded-first-assignment pattern and access/usage caveats above
- Back: [Guide 18 — Talking to Devin](talking-to-devin.md) (the doctrine under the outcome prompt) · Next: [Guide 2 — Product-owner Bot](bots-201-product-owner.md)
