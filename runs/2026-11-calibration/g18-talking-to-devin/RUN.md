# Guide 18 — Talking to Devin: calibration run

## Goal

Use a scoped brief to reproduce the guide’s change in a synthetic repository, verify it with the named command, and check that no commit was made.

## Plan/mode/version

[Devin child session](https://app.devin.ai/sessions/f419ede4e96d482eb388b97ce8692e7b), Lite mode via API. Plan tier and model/version were not recorded. This was not the guide’s CLI v3000.14 / `swe-2-flash-medium` run.

## Baseline commit

- Guide repository: `f55cb53db2800d27a794bf939a35a36c156181e2`
- Sandbox: `63863124c167d057942f33d2116aeae6775b9f3e`

## Fixture

Reconstructed synthetic baseline: [app.py](fixture/app.py) and [test_app.py](fixture/test_app.py), supplied as [demo-repo.tgz](https://app.devin.ai/attachments/00d41a4e-c883-4609-8e77-d2e2c5e2e1be/demo-repo.tgz).

## Exact prompts (verbatim)

The setup instructed the child to fetch and extract the fixture archive; setup preamble not reproduced verbatim. The guide’s brief was sent verbatim:

```text
Add divide(a, b) to app.py: returns a / b, and raises ValueError('division by zero') when b == 0 — follow the style of multiply().
Rewrite test_app.py as unittest (pytest isn't installed on this machine) covering all four functions, including the zero-division case.
Success check: `python3 -m unittest -v` passes — run it yourself before reporting done.
Do not commit.
```

## Steps

| Step | Result | Evidence |
| --- | --- | --- |
| Open CLI REPL, submit brief, handle edit/test approval prompts, and exit | BLOCKED: no signed-in CLI on the rerun VM | [Web login gate](../gate-web-login.png) shows the browser gate; browser sign-in was unavailable too. |
| Run brief via Lite API session | Completed without clarification; rewrote tests and added divide | [Session](https://app.devin.ai/sessions/f419ede4e96d482eb388b97ce8692e7b) · [result log](child-result.txt) |
| Check tests, diff and HEAD | Five tests passed; two tracked files modified, one untracked cache directory, no new commit | [Result log](child-result.txt) |

## Broken/blocked steps + fix

- CLI-specific behavior remains unverified. Repeat on an already authenticated CLI when available; no login or new access was requested.
- `python3 -m unittest -v` left untracked `__pycache__/`. The no-commit boundary still held. The guide could document the cache and, if it wants to avoid it, suggest `PYTHONDONTWRITEBYTECODE=1`.
- Following the `multiply()` style also added a non-numeric-input `TypeError` guard to `divide()`. This is a plausible reading; clarify in the guide whether to copy the guard or only the formatting.

## Human interventions

0 mid-run interventions or clarifications after the initial brief.

## Meter

| ACUs | Wall time | Start (UTC) | End (UTC) |
| --- | --- | --- | --- |
| 0.0 shown, pending meter settle | ~30 s to result; 44 s to termination | 2026-11-25 14:25:45Z | Result 14:26:15Z; terminated 14:26:29Z |

## Claims confirmed/refuted

| Claim | Verdict |
| --- | --- |
| Devin runs the named success check before its report, with five tests passing | Confirmed in the equivalent run: `python3 -m unittest -v` ended `OK`. |
| `divide()` returns the quotient and raises the named `ValueError` on zero; `unittest` covers all four functions | Confirmed. The rewritten tests also check the exact `ValueError` message. |
| Only `app.py` and `test_app.py` are modified in the tracked diff; no commit is made | Confirmed: +38/−5 across those files; HEAD matches the baseline. |
| “Two modified files,” if read as the entire workspace status | Refuted for this fixture: `git status` also lists untracked `__pycache__/`. The guide’s promise of no commit is unaffected. |
| One scoped session, no obvious mid-flight clarification | Confirmed in Lite mode; drafting time against the guide’s under-10-minute target was not measured. |
| CLI-specific edit/test approvals, `/exit`, and `devin -r` hint | Not testable on the equivalent API surface. |

## Cleanup

Child terminated at 14:26:29Z. No sandbox PR was opened.
