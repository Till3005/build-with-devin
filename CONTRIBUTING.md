# Contributing

Contributions welcome — this collection is only as good as its sources.

## What belongs here

Guides that teach a **documented, reproducible** Devin usage:

- A pattern distilled from a named, published deployment (Cognition's own, a customer case, or a public write-up with verifiable numbers)
- An official product surface (Bots, Automations, Apps, Review, API) explained with working detail
- Corrections to existing guides when the product or a source changes

## What doesn't

- Hypothetical "how you could use Devin" with no documented deployment behind it
- Marketing content or unverifiable claims
- Content already covered by an existing guide — improve that guide instead

## Format

Follow the existing guide structure: goal/level/source header → pattern diagram → step-by-step → verbatim or reconstructed prompts (marked as such) → Verify it checklist → Pitfalls → Sources. The maintainer quality contract is in [`ops/curriculum/quality-bar.md`](ops/curriculum/quality-bar.md).

## Rules

- Every claim needs a source; every source needs a live link
- Numbers come from the cited deployment, not estimates
- One guide per PR
- After adding/removing a guide or editing `README.md`, run `python3 tools/sync.py` — it keeps the stats line and all six language READMEs in parity. CI fails on drift.

## Maintainer automation

The lean Devin Bot fleet that maintains this curriculum and the sister registry is defined in [`built-with-devin/ops/bot-fleet/`](https://github.com/Till3005/built-with-devin/tree/main/ops/bot-fleet). Curriculum-specific quality rules live in `ops/curriculum/`.

## License

Contributions are released under [CC0-1.0](LICENSE).
