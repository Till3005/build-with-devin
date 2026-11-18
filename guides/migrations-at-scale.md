# Guide 11 — Migrations at scale

**Goal:** run a large migration (language, framework, database, dependency, architecture) as hundreds of small verified PRs instead of one heroic rewrite.
**Level:** intermediate → advanced
**Sources:** [Best Practices](https://docs.devin.ai/use-cases/best-practices.md) · [Migration & Modernization](https://docs.devin.ai/use-cases/migration-modernization.md) · migration examples: [Java upgrades](https://docs.devin.ai/use-cases/examples/java-upgrades.md), [COBOL](https://docs.devin.ai/use-cases/examples/cobol-modernization.md), [SAS→PySpark](https://docs.devin.ai/use-cases/examples/sas-to-pyspark.md), [JS→TS](https://docs.devin.ai/use-cases/examples/javascript-to-typescript.md), [NoSQL→SQL](https://docs.devin.ai/use-cases/examples/nosql-to-sql.md) · Nubank case study

## The official playbook

Devin's own docs are blunt about what scales: **wide & shallow** beats **tall & deep**. A migration is the canonical wide-and-shallow job — the same small transformation applied to hundreds of independent units.

```text
migration ──► slice into isolated units (<90 min each)
                 │
        ┌────────┴────────┐
        ▼                 ▼
   skill for the      parallel sessions,
   transformation     one slice each
        │                 │
        └────► verify per slice (tests/build/CI)
                        │
              human review → merge → repeat
```

## Step 1 — Check your migration qualifies

From the official criteria — most should hold:

- High volume of repetitive subtasks
- Junior-engineer complexity per slice
- Isolated, incremental, backwards-compatible changes
- **Objective verification per slice** (the hard requirement: tests, build, CI, or a custom script)
- Minimal cross-slice dependencies

Not qualifying: a full-repo rewrite where everything must land at once.

## Step 2 — Slice

The slice is the smallest atomic unit — a file, a notebook, a module:

| Rule | Why |
| --- | --- |
| < 90 minutes of manual engineering per slice | Devin's reliability is per-slice |
| Independent + backwards-compatible | Slices run in parallel and merge in any order |
| Each slice carries its own verification | No verification, no automation — this is the failure gate |

Example (official): a 50-file REST→GraphQL migration → scope it, split into conflict-free work packages, run in parallel.

## Step 3 — Write the transformation as a skill

One skill = the repeatable recipe every session runs. Official example (Java 7→8, abridged):

```text
## Procedure
1. Verify the project is on Java 7
2. Install the Java 8 JDK
3. Update build configuration
4. Identify and replace deprecated Java 7 APIs
5. Analyze for Java 8 enhancement opportunities
6. Update unit tests
7. Test thoroughly
8. Update documentation
9. Build and verify
```

Write yours with: explicit steps, an end-to-end reference (a guide or video), and **multiple before/after code examples** — input/output pairs are the highest-quality signal you can give.

## Step 4 — Run parallel sessions

With the skill fixed, fan slices out across sessions — the [API](https://docs.devin.ai) or a Bot's child sessions (Guide 4). Every slice → one session → one PR. Human review gates the merge into `main`.

At scale the numbers compound: Nubank's multi-million-line ETL migration ran this loop to 8–12× efficiency — and a fine-tuned Devin cut per-task time ~40 → ~10 minutes.

## Step 5 — Watch the error rate, not the progress bar

Small error rates compound across thousands of slices. Operate on a dashboard, not vibes:

- Track slice pass rate on first try — the skill is your fix point, not the sessions
- Failed slices feed back into the skill (the docs' own loop: *"feed session links into Devin to patch the gaps"*)
- Merge order is free because slices are isolated — exploit it

## Verify it

- [ ] Every slice finishes under ~90 min and merges independently
- [ ] A slice failing verification produces a fix or a flagged ticket — never a silent merge
- [ ] The skill improved measurably over the first 20 slices (fewer human corrections per slice)
- [ ] Progress is countable: N/M slices migrated, pass rate visible

## Pitfalls

- **Unsliced migrations.** "Migrate the whole repo" is the official anti-pattern — no isolation, no parallelism, no per-unit verification.
- **No before/after examples.** The skill without examples produces a different style per session.
- **Skipping human review.** Parallel ≠ unattended — each slice still gets reviewed before `main`.

## Knowledge check

1. Why 'wide and shallow' slices instead of 'deep and complete' ones? *(Each slice must land green — a 90-minute verified PR compounds; a 3-day mega-branch rots against main.)*
2. Why does every slice need its own verification? *(Without per-slice proof, a 500-PR migration is 500 unverified diffs — the failure surface multiplies instead of dividing.)*
3. Nubank reported 8–12× efficiency — what made that figure credible rather than marketing? *(Published methodology: measured stage times before/after on real ETL pipelines, not a projection.)*

## Sources

- [Best Practices — docs.devin.ai](https://docs.devin.ai/use-cases/best-practices.md)
- [Migration & Modernization + 5 example playbooks](https://docs.devin.ai/use-cases/migration-modernization.md)
- [Use-case gallery — Migrations](https://docs.devin.ai/use-cases/gallery/index.md)
- Related: [Guide 7 — Enterprise rollout](enterprise-playbook.md) (Shape 1 is this guide at org scale)
