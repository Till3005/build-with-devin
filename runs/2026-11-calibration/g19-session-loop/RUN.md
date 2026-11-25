# Guide 19 — The session loop: calibration run

## Goal

Research a sandbox repository, delegate a scoped change, independently review the result, and read the usage and feedback for the session.

## Plan/mode/version

Step 1 used the free Ask/DeepWiki equivalent via `devin_ask_wiki_question`. Step 5 used the Insights API on the existing Guide 18 Lite child. No new Devin session was started.

## Baseline commit

- Guide repository: `f55cb53db2800d27a794bf939a35a36c156181e2`
- Sandbox: not created; owner approval pending.

## Fixture

For step 1, used indexed `Till3005/built-with-devin` (the sister repository); `Till3005/build-with-devin` itself was not indexed.

## Exact prompts (verbatim)

Step 1: `Where does the registry entry validation live and what calls it?`

## Steps

| Step | Result | Evidence |
| --- | --- | --- |
| 1. Research in Ask/DeepWiki | Completed via the equivalent tool. The answer cited `tools/export_registry.py`, `tools/verify_sources.py`, and `tools/sync.py` for validation and where it is called. | [Ask result](https://app.devin.ai/search/api_6b98e2e9-fcce-4b56-b92a-60ffe66f4bfe) |
| 2. Scope the change in Plan mode | **BLOCKED:** no scratch repo or signed-in web UI | [Login gate](../gate-web-login.png); owner card pending |
| 3. Delegate the scoped change and open a sandbox PR | **BLOCKED:** no scratch repo or signed-in web UI | [Login gate](../gate-web-login.png); owner card pending |
| 4. Review the sandbox PR independently | **BLOCKED:** no sandbox PR or signed-in web UI | [Login gate](../gate-web-login.png); owner card pending |
| 5. Read Session Insights | **PARTIAL:** API returned size, usage and message counters for the Guide 18 child. Analysis was requested around 14:39Z and still returned “none yet” around 14:48Z. No Guide 19 session was available. | [Guide 18 child](https://app.devin.ai/sessions/f419ede4e96d482eb388b97ce8692e7b) |

## Broken/blocked steps + fix

- Ask/Plan web toggles are blocked by the login gate. The owner card “Create the private rerun sandbox repo” had not been approved after about 25 minutes. Once approved, create the private sandbox and rerun steps 2–4 with one Lite/default child for the change and a separate, independent review on its unmerged PR. The native UI handoff also needs an already signed-in web surface.
- The Insights API returned `acus_consumed=0.0`, `num_user_messages=0`, `num_devin_messages=0`, and `session_size=xs`. Both counters read zero even though the child exchanged three visible messages (prompt, acknowledgment, result); the reason for the discrepancy is unknown.
- **Suggested guide fix:** Tell learners to request analysis on demand for smaller sessions and check back if it isn’t ready. This rerun observed no analysis about nine minutes after the request; it did not measure completion time.

## Human interventions

One Ask query, one analysis request, and an Insights recheck. No child interventions.

## Meter

| ACUs | Wall time | Start (UTC) | End (UTC) |
| --- | --- | --- | --- |
| No additional child usage; Ask was free | Ask duration not captured; ~9 min between analysis request and recheck | Insights request ~14:39Z | Insights recheck ~14:48Z |

## Claims confirmed/refuted

- Confirmed via Ask equivalent: code-location and caller research without starting a session.
- Confirmed via Insights API: the existing child returned size, usage and message fields. The zero message counts did not match the transcript; an analysis recommendation was not available.
- Not verified: native Ask/Plan UI, indexed brief handed off to a session, sandbox PR and independent review.

## Cleanup

No new session, scratch repo, or sandbox PR. The reused Guide 18 child was already terminated.
