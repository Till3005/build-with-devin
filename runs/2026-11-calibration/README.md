# Core guide calibration reruns — November 2026

> *Unofficial community project — not affiliated with, endorsed by, or sponsored by Cognition AI. "Devin" is a trademark of Cognition AI. Official docs: [docs.devin.ai](https://docs.devin.ai).*

This is the calibration tranche for the [audit’s core rerun plan](https://app.devin.ai/attachments/05cc485e-7402-4d6d-94c8-f545a0a8fa32/report.md): Guides 18, 19, and 1, run one at a time with scratch repositories and synthetic data. The approved budget is 5–11 ACUs. Stop and report before exceeding 11 ACUs; sessions started for the tranche count toward that ceiling.

The guides are run as a learner via equivalent Devin sessions/tools because the rerun VM had no signed-in web/CLI login — UI-only steps are marked **BLOCKED** with the [web login gate screenshot](gate-web-login.png). Equivalent runs do not verify behavior specific to the unavailable UI. Use existing access only; do not merge sandbox PRs or post externally.

| Guide | Status | Sessions | ACUs | Wall time | Interventions | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| 18 — Talking to Devin | Equivalent run completed; CLI blocked | 1 Lite child | 0.0 shown at exit; may lag | 30 s to result; 44 s through teardown | 0 after initial brief | [Run](g18-talking-to-devin/RUN.md) · [prompt](g18-talking-to-devin/prompt.txt) · [result](g18-talking-to-devin/child-result.txt) |
| 19 — The session loop | Mostly ran via equivalents; sandbox PR and Review completed; native Ask/Plan handoff blocked; Insights partial | 1 Lite child | 0.0 shown at exit; Ask was free | 114 s to sandbox result | 0 in sandbox child; Ask query and Insights checks outside it | [Run](g19-session-loop/RUN.md) · [sandbox PR](https://github.com/Till3005/bwd-rerun-sandbox/pull/1) |
| 1 — Your first Bot | Blocked; scratch repo available, but no Bot created | 0 | 0 | Not run | None in a Bot run | [Block and repair path](g01-first-bot/RUN.md) · [login gate](gate-web-login.png) |

**Tranche total:** 2 Lite children (of 4 planned) plus one free DeepWiki Ask query. Both children showed **0.0 ACUs at exit** (0.0 metered total); the lead orchestration session also read 0.0 ACUs when checked in the initial pass. The meter may lag or round; these readings do not establish that execution cost nothing.

**Remaining nine core guides:** Retain the audit’s **21–47 ACU / 20 session** budget. The two short Lite children both read 0.0 ACUs, so there is no usable consumption measurement to revise the budget. Their 30 s and 114 s results support using sequential Lite children for guides whose core step is one bounded brief.
