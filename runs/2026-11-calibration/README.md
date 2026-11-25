# Core guide calibration reruns — November 2026

> *Unofficial community project — not affiliated with, endorsed by, or sponsored by Cognition AI. "Devin" is a trademark of Cognition AI. Official docs: [docs.devin.ai](https://docs.devin.ai).*

This is the calibration tranche for the [audit’s core rerun plan](https://app.devin.ai/attachments/05cc485e-7402-4d6d-94c8-f545a0a8fa32/report.md): Guides 18, 19, and 1, run one at a time with scratch repositories and synthetic data. The approved budget is 5–11 ACUs. Stop and report before exceeding 11 ACUs; sessions started for the tranche count toward that ceiling.

The guides are run as a learner via equivalent Devin sessions/tools because the rerun VM had no signed-in web/CLI login — UI-only steps are marked **BLOCKED** with the [web login gate screenshot](gate-web-login.png). Equivalent runs do not verify behavior specific to the unavailable UI. Use existing access only; do not merge sandbox PRs or post externally.

| Guide | Status | Sessions | ACUs | Wall time | Interventions | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| 18 — Talking to Devin | Equivalent run completed; CLI blocked | 1 Lite child | 0.0 shown at exit; may lag | 30 s to result; 44 s through teardown | 0 after initial brief | [Run](g18-talking-to-devin/RUN.md) · [prompt](g18-talking-to-devin/prompt.txt) · [result](g18-talking-to-devin/child-result.txt) |
| 19 — The session loop | Ask completed via equivalent tool; Insights partial; steps 2–4 blocked | 0 new | Free Ask; no new child | Ask not timed; analysis still unavailable at ~9 min | Ask query, analysis request and recheck | [Run](g19-session-loop/RUN.md) · [Ask result](https://app.devin.ai/search/api_6b98e2e9-fcce-4b56-b92a-60ffe66f4bfe) |
| 1 — Your first Bot | Blocked; no Bot created | 0 | 0 | Not run | None in a Bot run | [Block and repair path](g01-first-bot/RUN.md) · [login gate](gate-web-login.png) |

**Tranche total:** 1 Lite child (of 4 planned) plus one free DeepWiki Ask query. The child showed **0.0 ACUs at exit** and the lead orchestration session also read **0.0 ACUs**. The meter may lag or round; these readings do not establish that execution cost nothing.

**Remaining nine core guides:** Retain the audit’s **21–47 ACU / 20 session** budget. One measured child below meter resolution is not enough to revise it. The brief-driven Lite child returned a result in 30 seconds, so use sequential Lite children for guides whose core step is one bounded brief to aim for the low end of that budget.
