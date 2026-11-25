# Guide 19 — The session loop: calibration run

## Goal

Research a sandbox repository, delegate a scoped change, independently review the result, and read the usage and feedback for the session.

## Plan/mode/version

The initial pass used the free Ask/DeepWiki equivalent via `devin_ask_wiki_question` and the Insights API on the existing Guide 18 Lite child. The sandbox follow-up used a new Lite child with origin `api`.

## Baseline commit

- Guide repository: `f55cb53db2800d27a794bf939a35a36c156181e2`
- Sandbox: `Till3005/bwd-rerun-sandbox` at `9c73372b54819c4dfd16c208e78f07ac95823705`.

## Fixture

The initial Ask query used indexed `Till3005/built-with-devin` (the sister repository); `Till3005/build-with-devin` itself was not indexed. The follow-up used the private sandbox’s synthetic billing poller.

## Exact prompts (verbatim)

- Initial Ask query: `Where does the registry entry validation live and what calls it?`
- Sandbox follow-up: [exact child prompt](sandbox-prompt.txt).

## Steps

| Step | Result | Evidence |
| --- | --- | --- |
| 1. Research in Ask/DeepWiki | Completed via the equivalent tool on the sister repo. The answer cited `tools/export_registry.py`, `tools/verify_sources.py`, and `tools/sync.py`. The sandbox child separately answered the guide’s billing poller question before editing. | [Ask result](https://app.devin.ai/search/api_6b98e2e9-fcce-4b56-b92a-60ffe66f4bfe) · [Sandbox child](https://app.devin.ai/sessions/b7baf3e0d7bc49a1bbdb1a2e0b88fc8b) |
| 2. Scope the change in Plan mode | A learner-authored brief scoped the sandbox change. The native Ask/Plan toggles and Plan-to-session handoff remain **BLOCKED**. | [Brief](sandbox-prompt.txt) · [Login gate](../gate-web-login.png) |
| 3. Delegate the scoped change and open a sandbox PR | Completed with one Lite API child; four tests passed. | [Sandbox PR #1](https://github.com/Till3005/bwd-rerun-sandbox/pull/1) |
| 4. Review the sandbox PR independently | Completed via existing Devin auto-review: “No Issues Found.” | [Sandbox Devin Review](https://app.devin.ai/review/till3005/bwd-rerun-sandbox/pull/1) |
| 5. Read Session Insights | **PARTIAL:** API returned size, usage and counters for the sandbox child; analysis was requested but not yet available. | [Sandbox child](https://app.devin.ai/sessions/b7baf3e0d7bc49a1bbdb1a2e0b88fc8b) |

## Sandbox run (Plan-mode equivalent via API child)

- **Baseline:** `Till3005/bwd-rerun-sandbox` at `9c73372b54819c4dfd16c208e78f07ac95823705`. The synthetic poller capped retries but not total backoff: six retries scheduled 1 + 2 + 4 + 8 + 16 + 32 = 63 seconds of sleeps.
- **Session:** [Lite child](https://app.devin.ai/sessions/b7baf3e0d7bc49a1bbdb1a2e0b88fc8b), origin `api`. Created at 15:27:46Z on 2026-11-25; reported done at 15:29:40Z (114 seconds), with zero human interventions. `acus_consumed=0.0` at exit. [Exact prompt](sandbox-prompt.txt).
- **Research answer:** Correct for the baseline. `poll_invoices()` lives in `billing/poller.py`, catches `TransientBillingError`, and waits `backoff * 2**retries` via the injectable `wait` function. `run_nightly()` in `jobs/nightly.py` calls it.
- **Result:** [Sandbox PR #1](https://github.com/Till3005/bwd-rerun-sandbox/pull/1) (head `e19efa2`, unmerged) adds `max_total_backoff=30.0`. It re-raises the existing error if the next delay would exceed the cap. A new test injects a no-sleep wait function.
- **Review:** Existing [Devin Review](https://app.devin.ai/review/till3005/bwd-rerun-sandbox/pull/1) posted “No Issues Found” at 15:29:21Z, 47 seconds after the PR’s 15:28:34Z monitoring comment. Separately, auto-review on the evidence [PR #4](https://app.devin.ai/review/till3005/build-with-devin/pull/4) reported “No Issues Found” at 14:51:43Z for `0196187`; that earlier result did not substitute for sandbox review.
- **Insights:** `acus_consumed=0.0`, `num_user_messages=0`, `num_devin_messages=0`, `session_size=xs`. Analysis generation was requested; no analysis was available at capture.

`python3 -m unittest -v` output from the sandbox PR description:

```text
test_nightly_fetches_invoices (test_billing.BillingPollerTests.test_nightly_fetches_invoices) ... ok
test_raises_when_retry_budget_is_exhausted (test_billing.BillingPollerTests.test_raises_when_retry_budget_is_exhausted) ... ok
test_raises_when_total_backoff_cap_is_exceeded (test_billing.BillingPollerTests.test_raises_when_total_backoff_cap_is_exceeded) ... ok
test_retries_with_exponential_backoff (test_billing.BillingPollerTests.test_retries_with_exponential_backoff) ... ok

----------------------------------------------------------------------
Ran 4 tests in 0.000s

OK
```

## Broken/blocked steps + fix

- The sandbox approval gate was resolved. The native Ask/Plan toggles and Plan handoff are still blocked by the [login gate](../gate-web-login.png); Dirtboi declined a dedicated test login. The API route does not verify those UI steps. A native rerun needs an already signed-in web surface.
- In the initial pass, both Insights message counters for the Guide 18 child still read zero around 15:00Z despite three visible messages (prompt, acknowledgment, result); the reason is unknown. The sandbox child likewise showed 0/0 at capture.
- **Suggested guide fix:** Tell learners to request analysis on demand for smaller sessions and check back if it isn’t ready. The Guide 18 child’s analysis was requested around 14:39Z and still returned “none yet” around 14:48Z and 15:00Z. Completion time was not measured.

## Human interventions

Zero human interventions in the sandbox child. Outside the child: one initial Ask query, Insights analysis requests and rechecks. No review intervention.

## Meter

| ACUs | Wall time | Start (UTC) | End (UTC) |
| --- | --- | --- | --- |
| Initial Ask was free; reused the Guide 18 child for the first Insights check | Ask duration not captured; ~21 min from analysis request to latest recheck | Insights request ~14:39Z | Insights rechecks ~14:48Z and ~15:00Z |
| Sandbox child: 0.0 shown at exit | 114 s to result | 15:27:46Z | 15:29:40Z |

## Claims confirmed/refuted

- Confirmed via Ask equivalent: code-location and caller research without starting a session.
- Confirmed via Insights API: the existing child returned size, usage and message fields. The zero message counts did not match the transcript; an analysis recommendation was not available.
- Confirmed in the sandbox: the scoped brief produced a tested PR, and independent Devin Review ran on that sandbox PR.
- Not verified: native Ask/Plan UI, Plan-generated brief and its UI handoff, and any Insights analysis recommendation for the sandbox child.

## Cleanup

The Guide 18 child reused for the initial Insights check was already terminated. The sandbox PR remains open and unmerged.
