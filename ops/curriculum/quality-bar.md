# Curriculum quality bar

This is the quality contract for `build-with-devin`. It exists so a learner can trust the curriculum as a system, not as a collection of notes.

## What "best" means

A guide is excellent when it is:

1. **Correct.** It matches current official documentation or clearly states the observed exception.
2. **Evidence-backed.** Every non-obvious claim links to official documentation, a named deployment, or a reproducible artifact.
3. **Reproducible.** A learner can follow the steps and know what evidence should appear.
4. **Bounded.** It states prerequisites, cost, risk, and what not to do.
5. **Useful in sequence.** It names what to read before and what the learner can do next.
6. **Native in each language.** The Chinese, Japanese, and Portuguese versions are written for their readers, not translated word for word.

## Required guide shape

Each guide should contain these parts in this order when the topic allows:

1. Title and stable guide number.
2. Goal, level, estimated time, and source header.
3. What the learner will build or be able to do.
4. Prerequisites.
5. The mental model or pattern diagram.
6. Exact steps.
7. Prompts, marked as verbatim or reconstructed.
8. What the learner should see.
9. Verify-it checklist.
10. Pitfalls and failure modes.
11. Cost or usage guidance when relevant.
12. Knowledge check or scenario exercise.
13. Sources.
14. Changelog or freshness note when the product area changes often.

## Freshness labels

Use these labels in curriculum maintenance notes:

- `verified`: a maintainer recently followed the guide or checked it against current official docs.
- `docs-checked`: the guide is aligned with current docs but has not been reproduced end to end.
- `stale-risk`: the product behavior moved or the source material changed.
- `unverified`: the guide cannot currently be trusted without manual checking.

## Coverage statuses

`ops/curriculum/coverage.json` uses four statuses:

- `covered`: a learner can complete the outcome from current guides.
- `partial`: useful material exists, but the full outcome is not covered.
- `gap`: no adequate coverage exists.
- `watch`: the product behavior is changing too fast for a stable guide.

A `partial` or `gap` row is not a failure. Hiding it is.

## Change rules

- Do not renumber guides without owner approval.
- Do not add a new stage without owner approval.
- Mirror every guide change into English, Chinese, Japanese, and Portuguese in the same PR.
- Mark uncertain claims as uncertain or remove them.
- Prefer editing an existing guide over adding a overlapping guide.
- Run `python3 tools/sync.py` and `python3 tools/audit_curriculum.py` before opening a PR.
