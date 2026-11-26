# Guide 20 — Dynamic Workflows

**Goal:** orchestrate many Devin sessions with a deterministic Python script — fan out independent work, pass structured results between stages, resume interrupted runs, and keep the ACU cost visible.
**Level:** advanced · **Time:** ~35 minutes to design a first run; cost depends on the number of agents
**Source:** [Dynamic Workflows docs](https://docs.devin.ai/work-with-devin/dynamic-workflows) · official docs verified November 26, 2026

> **Evidence status:** this guide is a source-backed operating guide, not yet an independent reproduction. A real workflow spawns multiple Devin sessions and can consume significant ACUs, so the reproduction exercise below is deliberately narrow and approval-gated.

## When to use it

Use a dynamic workflow when the work has real structure:

- **Wide fan-out with a combine step** — roughly five or more independent files, modules, endpoints, tickets, or candidates that each need judgment or verification, followed by a merge/dedup/recommendation step.
- **A staged pipeline** — later stages consume structured output from earlier stages, such as *audit → fix → verify*.
- **A controlled loop** — repeat a run/fix/check cycle until a measurable stop condition is met.

Do **not** use one when:

- A codemod, linter autofix, generator, or shell loop can do the work mechanically.
- Only one or two independent sessions are needed and no data flows between them.
- The work is tightly coupled through shared state or is small and sequential.

A workflow is not “more AI.” It is orchestration as code: the script decides which agents run, in what order, with what prompts, and what structured data passes forward.

## The mental model

```text
You describe the outcome
        ↓
Devin authors workflow.py
        ↓
the script calls agent(...) with a prompt + JSON Schema
        ↓
each agent returns structured output
        ↓
later prompts are built from earlier outputs
        ↓
the run is recorded and resumable
```

The orchestrating session stays interactive while the workflow runs in the background. The workflow panel shows phases, agents, and live status; you can open individual agent sessions, ask for a progress summary, or stop the run.

Enterprise accounts may need an admin to enable **Dynamic workflows** under **Enterprise Settings → Devin** before any organization in the enterprise can use them.

## The authoring contract

Devin writes the script, but you should review it like production code before approving a run.

| Primitive | Use |
| --- | --- |
| `register_workflow(meta)` | Declares name, description, and phases before agents run |
| `agent(prompt, phase=..., schema=...)` | Runs one agent and returns a dict shaped by the JSON Schema |
| `pipeline(items, stage1, stage2, ...)` | Runs each item through stages independently, without a barrier between stages |
| `parallel([...])` | Runs async callables concurrently and waits for all; use only where every result is genuinely needed, such as merge or dedup |
| `log("message")` | Writes progress visible during the run |

Schema design rules:

1. Keep schemas small, flat, and explicit.
2. Return identifiers and evidence, not prose essays — branch names, file paths, counts, statuses, one-line findings.
3. Use `None` or an explicit failure status when no downstream work is needed.
4. Do not put secrets in prompts or schemas.
5. Treat agent output as untrusted input to the next prompt; validate before acting on it.

## Determinism is the price of resume

A resumed workflow is re-executed from the top. Completed `agent()` calls replay their recorded outputs; unfinished or failed calls run again. That only works if the script makes the same calls every time.

Therefore workflow logic and prompts must not depend on:

- current time or date
- randomness or generated IDs
- environment variables
- filesystem state
- network responses

Anything that inspects the outside world belongs inside an `agent()` call. The script consumes the recorded output.

Two consequences:

- Editing a prompt re-runs that agent and everything downstream of it.
- An interrupted or timed-out run can resume with its run ID; the default and maximum run budget is seven days.

## Where agents run

| Mode | Use when | Handoff | Main risk |
| --- | --- | --- | --- |
| Separate VM (default) | Agents need isolated machines or normal repo setup | Push/read git branches | More setup and cost per agent |
| Shared VM | Agents must inspect or edit the current working tree | Shared filesystem | CPU/memory contention and write collisions |

For shared-VM fan-out, give parallel writers strictly non-overlapping files or directories. For separate-VM pipelines, make branch names part of the structured output.

Agents can also be pinned to a cheaper Devin mode for high-volume, low-judgment stages such as classification.

## Build your first safe workflow

Do not point your first workflow at an entire repository. Use a slice that is wide enough to prove the pattern and small enough to afford.

### 0. Choose a narrow unit

Good first slices:

- three components for an accessibility audit
- one directory of SQL queries for pagination issues
- five open tickets for deduplication and severity triage
- three migration units, each on its own branch

Bad first slices:

- “audit the whole monorepo”
- “fix all flaky tests”
- “review every file forever”

### 1. Write the outcome, not the script

Example, adapted from the official migration pattern:

```text
Use a workflow to audit the auth, billing, and search modules for missing
pagination and N+1 query patterns. Run one analysis agent per module.
For each confirmed issue, run a fix agent on its own branch and verify the
fix with an EXPLAIN plan before and after. Roll up the confirmed fixes,
skipped items, and anything needing human review.
```

Notice what this prompt includes: scope, unit of parallelization, stages, verification, and rollup shape.

### 2. Review the generated script before approval

Check these exact points:

- `register_workflow()` is called before agents.
- Each `agent()` has a schema.
- The number of agents is bounded by an explicit list, not an unbounded crawl.
- Failure behavior is explicit: retry, skip with status, substitute a default, or fail the run.
- The script is deterministic.
- Separate-VM agents hand off code through branches; shared-VM agents cannot overwrite one another.
- The final rollup includes evidence and unresolved items, not just “done.”

Runs are auto-approved by default. If you want a checkpoint before each run, turn off **Settings → Preferences → Auto-approve workflows**.

### 3. Run, observe, and stop correctly

While the run executes:

- Watch the workflow panel for phase and agent status.
- Open one agent session and inspect whether its prompt and schema match the intent.
- Ask the orchestrating session for a progress summary instead of interrupting every agent manually.
- If the design is wrong, stop the run. Stopping cancels the script and sleeps remaining child sessions; completed results stay recorded.

### 4. Resume only after preserving determinism

If a run is interrupted, resume it with the same script and run ID. If you edit a prompt, understand that the edited agent and its downstream work become new work.

### 5. Save the proven workflow

Once a workflow works, ask Devin to save it as a repo skill: a `workflow.py` beside a `SKILL.md` describing when to use it. This turns a one-off orchestration into a reusable organizational capability.

## Cost control

Every workflow agent is a Devin session. Cost therefore scales with both fan-out width and session depth.

Use this sequence:

1. Prototype on 3 items.
2. Inspect ACU usage per agent in the workflow panel.
3. Estimate the full run before widening it.
4. Use cheaper modes for classification/extraction stages.
5. Keep expensive judgment in fewer, later-stage agents.
6. Set hard stop conditions for loops.

A loop must have a written exit condition, such as “passes three consecutive runs” or “a round fixes nothing new.” Without one, the workflow can burn budget while making technically real but useless progress.

## Verify it

A first reproduction is valid only if all of these are true:

- [ ] The workflow ran on a bounded slice of 3–5 units, not the whole repo.
- [ ] The workflow panel showed phases and individual agent status.
- [ ] At least one downstream prompt visibly consumed structured output from an upstream agent.
- [ ] One agent session was opened and inspected.
- [ ] The final rollup separated verified results, skipped items, failures, and human-review items.
- [ ] ACU usage was recorded per agent and for the run.
- [ ] If interrupted or intentionally stopped, the run either resumed correctly or the reason it could not was documented.

## Pitfalls

- **Using agents for mechanical work.** If a script can transform the code deterministically, use the script as the tool and reserve agents for judgment.
- **Schemas that return essays.** Long prose is hard to consume downstream; return compact structured facts.
- **Hidden time dependence.** “Today,” timestamps, random IDs, or live network checks in the script break replay semantics.
- **Shared-VM write collisions.** Two agents editing the same file are not parallelism; they are a merge conflict generator.
- **Unbounded fan-out.** A crawl that discovers more work inside the workflow can explode cost. Bound discovery or make it an upstream human-approved input.
- **No failure contract.** Decide before running whether a failed agent skips, retries, blocks its item, or fails the run.
- **Premature reuse.** Do not save a workflow as a skill until it has run successfully on a real slice and its cost is understood.

## Exercises

1. Take a repetitive review task in your repo. Write the workflow prompt, then list the exact items in the fan-out before asking Devin to run it.
2. Design a two-stage schema for *audit → fix*. Keep each field under 120 characters unless it is a path or branch name.
3. Given a failing agent, write three possible failure policies and choose one. Explain what the rollup should show.
4. Estimate the cost of a 50-item fan-out from a 3-item prototype. What evidence makes the estimate valid?

## Capstone

Build a workflow that audits five files or modules against a written standard, fixes confirmed issues on separate branches, verifies each fix with the narrowest real check available, and produces a final evidence table. Save it as a skill only after a second successful run.

## Knowledge check

1. Why must workflow prompts avoid “today” and random IDs? *(A resumed run re-executes the script; changing inputs changes agent-call identity and breaks deterministic replay.)*
2. Why is `parallel()` not the default composition primitive? *(Most pipelines should stream item-by-item; `parallel()` creates a barrier and is only for stages that truly need every result.)*
3. What is the safest first fan-out size? *(A bounded slice of about 3–5 units — large enough to prove orchestration, small enough to measure cost and inspect behavior.)*
4. When does a workflow deserve to become a skill? *(After it succeeds on real work, has known cost and failure behavior, and is likely to be reused.)*

## Sources

- [Dynamic Workflows — official docs](https://docs.devin.ai/work-with-devin/dynamic-workflows)
- [Advanced capabilities — managed Devins](https://docs.devin.ai/work-with-devin/advanced-capabilities)
- [Skills — official docs](https://docs.devin.ai/product-guides/skills)
- [Devin MCP — official docs](https://docs.devin.ai/work-with-devin/devin-mcp)

## Changelog

- 2026-11-26 — Initial guide from official documentation. Independent reproduction evidence pending; do not treat the exercise as verified until a real run is recorded.
