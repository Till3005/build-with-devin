---
name: bwd-curriculum-steward
description: Maintain build-with-devin as a systematic, source-backed, four-language curriculum. Use for curriculum coverage audits, guide corrections, translation parity, official-docs drift, and quality-bar work.
---

# Build with Devin curriculum steward

Use this skill when working in `Till3005/build-with-devin` on curriculum structure, coverage, or guide quality.

## Required reading

Before editing, read:

1. `ops/curriculum/quality-bar.md`
2. `ops/curriculum/coverage.json`
3. `README.md`
4. The target guide in every language that the edit touches

## Required checks

Run before opening a PR:

```bash
python3 tools/sync.py
python3 tools/audit_curriculum.py
```

If `tools/sync.py --write` was needed, rerun `python3 tools/sync.py` after writing.

## Editing rules

- `README.md` is the curriculum source of truth.
- Guide numbers are stable IDs. Do not renumber without explicit owner approval.
- Do not add stages or restructure learning paths without explicit owner approval.
- Mirror guide edits in `guides/`, `guides/zh/`, `guides/ja/`, and `guides/pt/` in the same PR.
- Write Chinese for Chinese readers. Do not use literal translationese.
- Mark prompts as verbatim or reconstructed.
- Every claim needs official documentation, a named deployment, or a reproducible artifact.
- Prefer a small correction to an existing guide over a new overlapping guide.

## Coverage work

When official docs, Devin University, or a guide changes:

1. Identify the affected row in `ops/curriculum/coverage.json`.
2. Update only the rows whose evidence changed.
3. Keep `partial` and `gap` rows visible. Do not hide them to make the dashboard look clean.
4. Open one small PR per coherent correction unit.

## Escalate instead of editing

Escalate when the work requires:

- curriculum restructuring
- guide renumbering
- new capstone projects or companion repositories
- expensive reproduction runs
- publishing claims supported only by weak evidence
- external posting or public messaging
