# Guide 19 — The session loop: calibration run

## Goal

Research a sandbox repository, delegate a scoped change, independently review the result, and read the usage and feedback for the session.

## Plan/mode/version

Step 1 only: free Ask/DeepWiki equivalent via `devin_ask_wiki_question`. No new Devin session for this step.

## Baseline commit

- Guide repository: `f55cb53db2800d27a794bf939a35a36c156181e2`
- Sandbox: pending.

## Fixture

For step 1, used indexed `Till3005/built-with-devin` (the sister repository); `Till3005/build-with-devin` itself was not indexed.

## Exact prompts (verbatim)

Step 1: `Where does the registry entry validation live and what calls it?`

## Steps

| Step | Result | Evidence |
| --- | --- | --- |
| 1. Research in Ask/DeepWiki | Completed via the equivalent tool. The answer cited `tools/export_registry.py`, `tools/verify_sources.py`, and `tools/sync.py` for validation and where it is called. | [Ask result](https://app.devin.ai/search/api_6b98e2e9-fcce-4b56-b92a-60ffe66f4bfe) |
| 2. Scope the change in Plan mode | Pending sandbox repo | — |
| 3. Delegate the scoped change | Pending sandbox repo | — |
| 4. Review the sandbox PR independently | Pending sandbox repo | — |
| 5. Read Session Insights | Pending sandbox repo | — |

## Broken/blocked steps + fix

Ask/Plan mode toggles in the web UI are **BLOCKED** by the [login gate](../gate-web-login.png). The equivalent Ask result does not verify the web toggles or the Plan-to-session handoff.

## Human interventions

Pending. Record prompts, clarifications, approvals, and manual checks.

## Meter

| ACUs | Wall time | Start (UTC) | End (UTC) |
| --- | --- | --- | --- |
| Pending | Pending | Pending | Pending |

## Claims confirmed/refuted

Pending. Distinguish claims tested by an equivalent run from claims left unverified.

## Cleanup

Pending. Record how the session and any sandbox resources were closed.
