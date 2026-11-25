# Guide 1 — Your first Bot: calibration run

## Goal

Test a bounded ownership prompt with one synthetic newsletter signup run and record which Bot-specific behaviors were observable.

## Plan/mode/version

**BLOCKED.** Neither the web UI nor the Bot-creation API was run. The API path (`devin_bot_create`) uses an owner approval card.

## Baseline commit

- Guide repository: `f55cb53db2800d27a794bf939a35a36c156181e2`
- Sandbox: `Till3005/bwd-rerun-sandbox` now exists; no Bot run used it.

## Fixture

The guide’s signup → welcome email → resource link journey needs a staging URL and test mailbox; neither was available. Planned equivalent: a bounded documentation check on a private scratch repo with synthetic Markdown fixtures. This would test Bot ownership mechanics, not email delivery.

## Exact prompts (verbatim)

No prompts were submitted. The guide’s bounded learner prompt is:

```text
Own the newsletter signup check for [project] on staging.
Use [repository], [staging URL] and the test mailbox I provide.
Check the journey from submitting the form to receiving the
correct welcome email and opening its resource link.

Start with one run. Show me the result before proposing a schedule.
If you find a defect, reproduce it, make the smallest suitable fix,
and open a pull request with the evidence.

Do not merge, deploy, email real subscribers, change billing,
or connect another service without asking me.

Return: what passed/failed, screenshots or a short recording,
the PR if a fix was needed, anything you could not verify,
and any decision you need from me.
```

Other guide prompts: check in with `anything waiting on me?`. The guide’s memory example is `remember: we deploy via Cloud Run, never bare VMs`; its schedule example is `run a summary of open PRs every weekday morning`. The Android ownership prompt is a historical example, not the learner assignment.

Planned replacement outcome (not sent):

```text
Own the README's relative links in the private calibration sandbox. Start with one run: check the synthetic README's relative links against the repository files and report each broken link. If a fix is needed, open a small sandbox PR with the check output. Do not merge, deploy, contact anyone, add access, or schedule another run. Return what passed or failed, the evidence, any PR, and any decision you need from me.
```

Use the guide’s check-in unchanged. For Memory, give a real sandbox-specific correction rather than the Cloud Run example. Do not activate a schedule or add integrations.

## Steps

| Step | Result | Evidence |
| --- | --- | --- |
| 1. Create a private Bot | **BLOCKED:** web requires login; API still needs separate Bot-creation approval | [Login gate](../gate-web-login.png) |
| 2. Assign a bounded outcome | **BLOCKED:** no Bot, staging URL, or test mailbox | Planned synthetic substitute above |
| 3. Observe child dispatch and Needs you | **BLOCKED:** no Bot or child | No run |
| 4. Set standing instructions and verify a Memory correction | **BLOCKED:** no Bot | No run |
| 5. Reach the Bot via web or optional Slack/iMessage | **BLOCKED:** no Bot or signed-in web UI; no integrations added | [Login gate](../gate-web-login.png) |
| 6. Inspect automations and modes | **BLOCKED:** no Bot | No run |

## Broken/blocked steps + fix

The scratch repo is available, but that does not unblock Bot creation. Dirtboi declined a dedicated test login, and a staging URL and test mailbox are still unavailable. The repair path is unchanged: obtain separate Bot-creation approval, run one child on the synthetic outcome with existing access only, capture Needs you and Memory evidence, then stop the child and archive the Bot. A native newsletter check still needs an already authorized staging URL and synthetic mailbox; the native UI needs an already signed-in web surface.

## Human interventions

None in a Bot run. Bot-creation approval is still required.

## Meter

| ACUs | Wall time | Start (UTC) | End (UTC) |
| --- | --- | --- | --- |
| 0 (0 sessions) | Not run | — | — |

## Claims confirmed/refuted

No Bot behavior was confirmed or refuted. Bot creation, autonomous dispatch, Needs you, Memory, and the optional Slack check are unverified.

## Cleanup

No Bot, child, automation, or sandbox PR was created.
