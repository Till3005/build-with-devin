# Guide 21 — Security Profiles & Cloud OIDC

**Goal:** give Devin least-privilege access in two layers: reusable Security Profiles that constrain what sessions can reach and do, plus Cloud OIDC that replaces long-lived cloud credentials with short-lived workload identity.
**Level:** advanced / admin · **Time:** ~45–90 minutes for a first governed profile; cloud setup depends on your provider
**Source:** [Security Profiles docs](https://docs.devin.ai/product-guides/security-profiles) · [Cloud OIDC docs](https://docs.devin.ai/product-guides/oidc) · official docs verified November 26, 2026

> **Evidence status:** this guide is source-backed but not yet independently reproduced against a cloud provider. The verification section separates checks you can do in Devin from checks that require AWS/GCP/Vault/admin resources.

## The two-layer mental model

Security Profiles and Cloud OIDC solve different problems:

| Layer | Question it answers | Mechanism |
| --- | --- | --- |
| Security Profile | What may this Devin session reach or operate? | Network allowlist, MCP allowlist, Devin MCP read-only, git access level, GitHub CLI token removal |
| Cloud OIDC | How does this session prove who it is to a cloud service? | Short-lived identity token issued by Devin, exchanged by the cloud for temporary scoped credentials |

Use them together. A profile can prevent a session from reaching or operating systems it should not touch; OIDC removes the need to store cloud keys when access is legitimate.

Security Profiles are separate from **Devin Security**, the vulnerability-scanning product surface. A profile does not configure a scan.

## What a Security Profile can restrict

A profile is a named bundle of optional restrictions. It only constrains the settings it configures.

| Restriction | What it controls | Important detail |
| --- | --- | --- |
| Network policy | Outbound destinations allowed from the session machine | Hostnames support `*` wildcards; IPv4/IPv6 CIDR ranges are supported |
| MCP access | Which installed MCP servers the session may use | Independent of network policy; allowed MCP servers are reachable automatically |
| Devin MCP access | Whether built-in Devin management tools are write-capable | Read-only still allows listing/inspection but blocks writes such as creating sessions or editing knowledge |
| Git access | Clone/fetch only, or full push/PR capability | Read-only blocks pushes and PR creation |
| GitHub CLI token | Whether the machine carries a `gh` token for direct GitHub API calls | Keeping it requires full git access and, when a network policy exists, `api.github.com` |

Destinations required for Devin itself to function, such as the git proxy for connected repositories, are allowed automatically.

## Where profiles bind

Profiles take effect through a hierarchy. The most specific binding wins unless a mandatory profile higher up imposes a floor:

1. Enterprise default
2. Organization default
3. Automations default
4. Specific automation
5. Individual session
6. Bot security profile, for sessions started by that Bot

At each level you can inherit, pin a profile, or explicitly choose no profile. Child sessions follow the same governing chain as their parent, so delegating work cannot escape restrictions.

A running session resolves its profile when it boots or wakes. Editing a profile or binding does not retroactively change a running session; it affects new sessions immediately and existing sessions the next time they resume.

## Recommended vs mandatory

Start with **recommended** when rolling out. A recommended profile is a default that lower levels can replace or opt out of.

Switch to **mandatory** when the allowlists are understood. Mandatory profiles are floors:

- Lower-level “no profile” choices are ignored.
- Lower-level profiles can only tighten restrictions, never loosen them.
- Network and MCP allowlists intersect.
- Git access takes the minimum level.
- Devin MCP is read-only if either side says read-only.
- The GitHub CLI token is removed if either side removes it.
- Even mid-session network approvals are clamped by the mandatory policy.

This makes mandatory profiles the correct primitive for enterprise-wide boundaries, and recommended profiles the correct primitive for team-level rollout.

## What Cloud OIDC changes

Without OIDC, a session that needs AWS, GCP, Vault, JFrog, Databricks, or an internal API usually needs a stored key or token. With OIDC:

1. Every Devin session automatically receives a short-lived identity token signed by Devin.
2. Your cloud or service verifies that token against Devin's public OIDC issuer.
3. The service exchanges it for temporary, scoped credentials.
4. The token expires automatically; there is nothing static to rotate or revoke.

Tokens can carry claims such as `org_id`, `account_id`, `devin_id`, `devin_trigger`, `requesting_user_id`, `requesting_user_email`, and `service_user_id`. Trust policies can therefore grant access to an entire organization, a specific user, or even a specific session.

The issuer is `https://app.devin.ai` unless your enterprise uses a custom domain, in which case the issuer is that custom Devin URL.

## Design the access model first

Do not start by writing YAML. Start with the trust boundaries.

Write down:

- which sessions or automations need cloud access at all
- which provider and project/account they need
- whether they need read-only or write access
- which network destinations they legitimately need
- which MCP servers they should use
- whether they should create child sessions or manage Devin resources
- whether they need direct GitHub API access beyond normal git operations

Then create small profiles for real job types, not one huge profile for everyone.

Useful starting profiles:

| Profile | Typical use | Suggested posture |
| --- | --- | --- |
| `research-readonly` | Evidence gathering, docs, read-only review | Network limited to required docs/repos, git read-only, Devin MCP read-only, no `gh` token |
| `automation-pr-writer` | CI repair, dependency updates, hygiene loops | Network for repo/package APIs, full git, no unrelated MCP, `gh` only if required |
| `cloud-operator` | Infrastructure inspection or controlled operations | Network narrowed to cloud endpoints, OIDC-enabled, tightly scoped cloud role, no broad MCP |
| `incident-hotfix` | Human-supervised incident response | Time-bound use, full git, only incident-relevant network/MCP, mandatory human review before merge/deploy |

## Build a first Security Profile

You need the dedicated **Manage security profiles** permission. Organization admins have the organization-level permission by default; enterprise admins have the enterprise-level permission. Both can be delegated through custom roles.

1. Go to **Settings → Customization → Security profiles** for an organization profile, or **Enterprise settings → Devin → Security profiles** for an enterprise profile.
2. Create a narrowly named profile, such as `automation-pr-writer`, not `default-secure`.
3. Configure only the restrictions you understand.
4. Keep it **recommended** at first.
5. Bind it as an organization default or pin it to one low-risk automation.
6. Test positive and negative access before widening the rollout.
7. Tighten over time; switch to mandatory only after legitimate destinations and workflows are covered.

### Positive and negative tests

Positive tests prove allowed work still works:

- clone/fetch the intended repository
- install the intended package or reach the intended API
- use an allowed MCP server
- push a branch when full git is expected

Negative tests prove the boundary exists:

- a disallowed domain fails
- a disallowed MCP server is unavailable
- read-only git cannot push
- Devin MCP write operations fail under read-only mode
- direct `gh api` calls fail when the token is removed

Record both. “It launched” is not a security verification.

## Automations and snapshot builds

Automations can carry their own network policy and MCP selection, but those are restriction-only layers. An automation can never widen the governing profile; sessions receive only what both layers allow.

Snapshot builds are different: only a profile's network policy applies to builds and blueprint author sessions. MCP, git access, and GitHub CLI restrictions do not apply there. Because builds often need package registries that sessions do not, use the separate **Default profile for snapshot builds** setting rather than loosening session profiles.

## Outposts warning

On Devin-managed VMs, Devin enforces network policy at the machine level. On Outposts, your infrastructure does the enforcement.

Devin publishes each queued session's effective network policy to the Outposts API as `spec.network_policy`. Your orchestrator must enforce it with an egress proxy, Kubernetes `NetworkPolicy`, VM firewall rules, or equivalent controls. If it does not, a “mandatory” network boundary is not actually a hard boundary on outpost infrastructure.

Re-read `spec.network_policy` when a session is queued or re-queued; do not assume it is static.

## Set up Cloud OIDC

Cloud OIDC requires configuration on both sides:

- the cloud/service must trust Devin's issuer and define which token claims may assume which role or identity
- the Devin environment blueprint must install the relevant setup action

Add the relevant action to `initialize`:

| Service | Blueprint action |
| --- | --- |
| AWS | `github.com/CognitionAI/actions/setup-aws-oidc@main` |
| GCP | `github.com/CognitionAI/actions/setup-gcp-oidc@main` |
| Vault | `github.com/CognitionAI/actions/setup-vault-oidc@main` |
| JFrog | `github.com/CognitionAI/actions/setup-jfrog-oidc@main` |
| Custom services | `github.com/CognitionAI/actions/setup-devin-oidc@main` |

AWS example:

```yaml
initialize:
  - uses: github.com/CognitionAI/actions/setup-aws-oidc@main
    with:
      role-arn: "arn:aws:iam::123456789012:role/devin-sessions"
      region: "us-east-1"
```

GCP example:

```yaml
initialize:
  - uses: github.com/CognitionAI/actions/setup-gcp-oidc@main
    with:
      workload-identity-provider: "projects/123456789/locations/global/workloadIdentityPools/devin/providers/devin-oidc"
      service-account: "devin@my-project.iam.gserviceaccount.com"
      project: "my-project"
```

For a custom service, request a token for the audience your service accepts:

```bash
devin-oidc token --audience my-api --subject-keys "org_id"
```

Your service verifies the token against Devin's published JWKS at `/.well-known/jwks.json` under the correct issuer.

## Write least-privilege trust policies

Prefer narrow claims and narrow roles:

- Use `org_id` for organization-wide automation identity.
- Add `requesting_user_email` or `service_user_id` when only certain initiators should receive access.
- Use `devin_id` only for tightly scoped one-off or debugging access; it is usually too narrow for reusable automation.
- Give the assumed role only the permissions the job needs.
- Separate read-only and write-capable roles instead of broadening one role.

Cloud audit logs become more useful with OIDC because actions can be attributed to a specific Devin session and requesting user rather than to a shared static key.

## Verify it

Devin-side checks:

- [ ] A test session resolves the intended profile.
- [ ] Allowed network, MCP, git, and Devin MCP operations still work.
- [ ] At least one disallowed operation in each configured category fails.
- [ ] A profile or binding edit is confirmed to affect a new or resumed session, not assumed to mutate an already-running session.
- [ ] Automation-triggered sessions inherit the intended intersection of automation and profile restrictions.

Cloud-side checks, when you control the provider:

- [ ] `aws sts get-caller-identity` or the equivalent provider command succeeds without a stored key.
- [ ] The assumed identity is the intended least-privilege role/service account.
- [ ] Cloud audit logs show the Devin session/user identity claims you expect.
- [ ] A token for the wrong audience or trust subject is rejected.
- [ ] No long-lived cloud credential is present in Devin secrets or the environment.

## Pitfalls

- **Treating a profile as a scan.** It is an access-control envelope, not vulnerability detection.
- **Making the first profile mandatory.** You will block legitimate work before you understand the required destinations.
- **One giant profile.** Job-shaped profiles are auditable; a universal profile becomes a meaningless compromise.
- **Forgetting `api.github.com`.** A profile cannot keep the GitHub CLI token under a network policy unless `api.github.com` is allowed.
- **Assuming running sessions update immediately.** They resolve the profile at boot/wake.
- **Assuming Outposts enforce themselves.** The operator must enforce `spec.network_policy` outside Devin-managed infrastructure.
- **Using OIDC without narrowing cloud trust.** Keyless does not mean safe if the role is broad or the trust policy accepts too much.
- **Leaving old static keys in place.** OIDC only reduces credential risk if the static keys are removed or disabled.

## Exercises

1. Write a profile specification for a dependency-update automation. Include network destinations, git access, MCP needs, and whether `gh` is necessary.
2. Write one positive and one negative test for each restriction in that profile.
3. Design a cloud trust policy for read-only access to one project. Which token claims are sufficient, and which are too narrow?
4. Explain how a mandatory enterprise profile and a stricter organization profile intersect.

## Capstone

Build a governed automation path for one low-risk repo maintenance task: create a recommended profile, pin it to the automation, verify positive/negative behavior, configure OIDC for one cloud read-only operation if available, and document the exact evidence. Only then propose whether the profile should become mandatory.

## Knowledge check

1. Why are Security Profiles and OIDC complementary rather than alternatives? *(Profiles restrict what a session can reach or operate; OIDC proves session identity to a service without storing long-lived credentials.)*
2. Why start with recommended enforcement? *(It lets you observe legitimate access needs and avoid blocking teams before the allowlists are complete.)*
3. Why does child-session delegation not escape a profile? *(Children inherit the same governing chain as the parent.)*
4. Why is OIDC valuable for auditability? *(Cloud logs can attribute actions to session, organization, and requesting-user claims instead of a shared static key.)*

## Sources

- [Security Profiles — official docs](https://docs.devin.ai/product-guides/security-profiles)
- [Cloud Authentication with OIDC — official docs](https://docs.devin.ai/product-guides/oidc)
- [Security Profiles API — official reference](https://docs.devin.ai/api-reference/v3/security-profiles/list-organizations-security-profiles)
- [CognitionAI actions repository](https://github.com/CognitionAI/actions)
- [Devin Outposts overview](https://docs.devin.ai/cloud/outposts/overview)

## Changelog

- 2026-11-26 — Initial guide from official documentation. Cloud-provider reproduction evidence pending; verification commands are provided but not yet independently executed here.
