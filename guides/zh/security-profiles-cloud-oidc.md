# 指南 21 — Security Profiles 与 Cloud OIDC

**目标：** 用两层机制给 Devin 最小权限访问：可复用的 Security Profiles 限制 session 能接触和操作什么；Cloud OIDC 用短期 workload identity 替代长期云凭证。
**难度：** 高级 / 管理员 · **时间：** 第一个受治理 profile 约 45–90 分钟；云服务配置取决于你的 provider
**来源：** [Security Profiles 官方文档](https://docs.devin.ai/product-guides/security-profiles) · [Cloud OIDC 官方文档](https://docs.devin.ai/product-guides/oidc) · 官方文档已于 2026-11-26 核验

> **证据状态：** 本指南基于官方来源，但尚未在真实云 provider 上独立复现。验证部分区分了能在 Devin 内完成的检查和需要 AWS/GCP/Vault/管理员资源的检查。

## 两层心智模型

Security Profiles 和 Cloud OIDC 解决的是不同问题：

| 层 | 回答的问题 | 机制 |
| --- | --- | --- |
| Security Profile | 这个 Devin session 可以接触或操作什么？ | 网络 allowlist、MCP allowlist、Devin MCP read-only、git access level、移除 GitHub CLI token |
| Cloud OIDC | 这个 session 如何向云服务证明自己是谁？ | 由 Devin 签发的短期 identity token，由云服务验证并换成临时、有限权限凭证 |

两者应该一起用。Profile 可以阻止 session 接触或操作不该碰的系统；OIDC 则在访问确实合法时，避免存放云端密钥。

Security Profiles 和 **Devin Security**（漏洞扫描产品面）不是一回事。Profile 不会配置安全扫描。

## Security Profile 能限制什么

Profile 是一组可选限制的命名集合。它只约束自己显式配置的设置。

| 限制 | 控制内容 | 关键细节 |
| --- | --- | --- |
| Network policy | session 机器允许访问的 outbound destinations | hostname 支持 `*` wildcard；支持 IPv4/IPv6 CIDR |
| MCP access | session 可以使用哪些已安装 MCP servers | 独立于 network policy；被允许的 MCP servers 自动可达 |
| Devin MCP access | 内置 Devin 管理工具是否可写 | read-only 仍可 list/inspect，但不能创建 sessions 或编辑 knowledge 等写操作 |
| Git access | 只能 clone/fetch，还是完整 push/PR 能力 | read-only 会阻止 push 和创建 PR |
| GitHub CLI token | 机器上是否携带可直接调用 GitHub API 的 `gh` token | 保留它要求 full git access；若设置 network policy，还必须允许 `api.github.com` |

Devin 自身运行必需的目的地（例如连接仓库使用的 git proxy）会自动允许。

## Profile 绑定到哪里

Profile 通过层级绑定生效。更具体的绑定优先，除非上层有 mandatory profile 形成底线：

1. Enterprise default
2. Organization default
3. Automations default
4. 特定 automation
5. 单个 session
6. Bot security profile（作用于该 Bot 启动的 sessions）

每一层都可以选择 inherit、pin 一个 profile，或显式选择 no profile。Child sessions 遵循和 parent 相同的治理链，所以不能通过委派工作绕过限制。

运行中的 session 会在 boot 或 wake 时解析自己的 profile。编辑 profile 或 binding 不会 retroactively 改变已经运行的 session；它会立即影响新 session，并在现有 session 下次 resume 时生效。

## Recommended 与 mandatory

 rollout 初期用 **recommended**。Recommended profile 是默认值，下层可以替换或 opt out。

当你理解 allowlist 后，再切换到 **mandatory**。Mandatory profile 是底线：

- 下层的 “no profile” 会被忽略。
- 下层 profile 只能收紧，不能放宽。
- Network 和 MCP allowlists 取交集。
- Git access 取最低级别。
- 任一侧要求 read-only，Devin MCP 就是 read-only。
- 任一侧移除 GitHub CLI token，token 就被移除。
- 即使 session 中临时批准新的 network access，也会被 mandatory policy 夹住。

所以，mandatory 是企业级边界的正确 primitive；recommended 是团队级 rollout 的正确 primitive。

## Cloud OIDC 改变了什么

没有 OIDC 时，session 要访问 AWS、GCP、Vault、JFrog、Databricks 或内部 API，通常需要保存 key 或 token。使用 OIDC 后：

1. 每个 Devin session 自动获得由 Devin 签发的短期 identity token。
2. 你的云或服务根据 Devin 的公共 OIDC issuer 验证 token。
3. 服务把 token 换成临时、有限范围的凭证。
4. token 自动过期；没有静态凭证需要轮换或吊销。

Token 可以携带 `org_id`、`account_id`、`devin_id`、`devin_trigger`、`requesting_user_id`、`requesting_user_email`、`service_user_id` 等 claims。因此 trust policy 可以授权给整个组织、特定用户，甚至特定 session。

Issuer 默认是 `https://app.devin.ai`；企业自定义域名部署时，issuer 是那个自定义 Devin URL。

## 先设计访问模型

不要先写 YAML。先写清信任边界：

- 哪些 sessions 或 automations 真的需要云访问
- 需要哪个 provider、project/account
- 需要 read-only 还是 write access
- 合法需要哪些 network destinations
- 应该使用哪些 MCP servers
- 是否应该创建 child sessions 或管理 Devin resources
- 是否需要超出普通 git 操作的 GitHub API 访问

然后按真实工作类型创建小 profile，而不是给所有人一个巨大的 profile。

可参考的起始 profiles：

| Profile | 典型用途 | 建议姿态 |
| --- | --- | --- |
| `research-readonly` | 证据收集、文档、只读 review | 网络限于所需 docs/repos，git read-only，Devin MCP read-only，无 `gh` token |
| `automation-pr-writer` | CI 修复、依赖更新、卫生循环 | 网络限于 repo/package APIs，full git，无无关 MCP，只有必要时保留 `gh` |
| `cloud-operator` | 基础设施检查或受控操作 | 网络收窄到 cloud endpoints，启用 OIDC，云角色严格收窄，不给宽泛 MCP |
| `incident-hotfix` | 人工监督的事故响应 | 限时使用，full git，只允许事故相关 network/MCP，merge/deploy 前必须人工 review |

## 构建第一个 Security Profile

你需要专门的 **Manage security profiles** 权限。Organization admins 默认有组织级权限；enterprise admins 默认有企业级权限。两者都可以通过 custom roles 委派。

1. 组织级 profile 进入 **Settings → Customization → Security profiles**；企业级 profile 进入 **Enterprise settings → Devin → Security profiles**。
2. 创建命名窄而明确的 profile，例如 `automation-pr-writer`，不要叫 `default-secure`。
3. 只配置你理解的限制。
4. 初期保持 **recommended**。
5. 绑定为 organization default，或 pin 到一个低风险 automation。
6. 扩大 rollout 前测试正向和反向访问。
7. 随时间收紧；只有合法 destinations 和 workflows 都覆盖后，才切换为 mandatory。

### 正向和反向测试

正向测试证明允许的工作仍能进行：

- clone/fetch 目标仓库
- 安装目标 package 或访问目标 API
- 使用被允许的 MCP server
- 在预期 full git 时推送 branch

反向测试证明边界确实存在：

- 不允许的 domain 失败
- 不允许的 MCP server 不可用
- read-only git 不能 push
- read-only 模式下 Devin MCP 写操作失败
- token 被移除后，直接 `gh api` 调用失败

两类都要记录。“session 启动了”不是安全验证。

## Automations 与 snapshot builds

Automations 可以携带自己的 network policy 和 MCP 选择，但它们只是 restriction-only layers。Automation 永远不能放宽 governing profile；session 只得到 automation 和 profile 两边都允许的内容。

Snapshot builds 不同：只有 profile 的 network policy 会作用于 builds 和 blueprint author sessions。MCP、git access、GitHub CLI 限制不适用。因为 builds 常需要 session 不需要的 package registries，应使用单独的 **Default profile for snapshot builds** 设置，而不是放宽 session profiles。

## Outposts 警告

在 Devin 管理的 VM 上，Devin 在机器层执行 network policy。在 Outposts 上，执行责任在你的基础设施。

Devin 会把每个排队 session 的有效 network policy 通过 Outposts API 发布为 `spec.network_policy`。你的 orchestrator 必须用 egress proxy、Kubernetes `NetworkPolicy`、VM firewall rules 或等价控制执行它。否则，“mandatory” 网络边界在 outpost 基础设施上并不是真正的硬边界。

session 被排队或重新排队时要重新读取 `spec.network_policy`；不要假设它不变。

## 配置 Cloud OIDC

Cloud OIDC 需要两边都配置：

- 云服务必须信任 Devin issuer，并定义哪些 token claims 可以代入哪个 role 或 identity
- Devin environment blueprint 必须安装对应 setup action

把相关 action 加入 `initialize`：

| 服务 | Blueprint action |
| --- | --- |
| AWS | `github.com/CognitionAI/actions/setup-aws-oidc@main` |
| GCP | `github.com/CognitionAI/actions/setup-gcp-oidc@main` |
| Vault | `github.com/CognitionAI/actions/setup-vault-oidc@main` |
| JFrog | `github.com/CognitionAI/actions/setup-jfrog-oidc@main` |
| 自定义服务 | `github.com/CognitionAI/actions/setup-devin-oidc@main` |

AWS 示例：

```yaml
initialize:
  - uses: github.com/CognitionAI/actions/setup-aws-oidc@main
    with:
      role-arn: "arn:aws:iam::123456789012:role/devin-sessions"
      region: "us-east-1"
```

GCP 示例：

```yaml
initialize:
  - uses: github.com/CognitionAI/actions/setup-gcp-oidc@main
    with:
      workload-identity-provider: "projects/123456789/locations/global/workloadIdentityPools/devin/providers/devin-oidc"
      service-account: "devin@my-project.iam.gserviceaccount.com"
      project: "my-project"
```

自定义服务可以为服务接受的 audience 请求 token：

```bash
devin-oidc token --audience my-api --subject-keys "org_id"
```

你的服务要在正确 issuer 下，根据 Devin 发布在 `/.well-known/jwks.json` 的 JWKS 验证 token。

## 编写最小权限 trust policies

优先使用窄 claims 和窄 roles：

- 组织级 automation identity 使用 `org_id`。
- 只允许特定发起人时，加上 `requesting_user_email` 或 `service_user_id`。
- `devin_id` 只用于严格收窄的一次性或调试访问；对可复用 automation 通常太窄。
- assumed role 只给这项工作所需权限。
- 分开 read-only 和 write-capable roles，不要把一个 role 放宽。

使用 OIDC 后，云审计日志更有价值，因为操作可以归因到具体 Devin session 和 requesting user，而不是共享静态 key。

## Verify it

Devin 侧检查：

- [ ] 测试 session 解析到预期 profile。
- [ ] 被允许的 network、MCP、git、Devin MCP 操作仍可执行。
- [ ] 每个已配置类别中，至少一个不允许的操作失败。
- [ ] 确认 profile 或 binding 编辑影响的是新 session 或 resume 后的 session，而不是假设它会改变正在运行的 session。
- [ ] automation 触发的 sessions 继承了 automation 和 profile 限制的预期交集。

云侧检查（当你控制 provider 时）：

- [ ] `aws sts get-caller-identity` 或对应 provider 命令在没有存储 key 的情况下成功。
- [ ] 代入的 identity 是预期的最小权限 role/service account。
- [ ] 云审计日志显示你预期的 Devin session/user identity claims。
- [ ] 错误 audience 或 trust subject 的 token 被拒绝。
- [ ] Devin secrets 或环境中没有长期云凭证。

## 常见坑

- **把 profile 当扫描器。** 它是访问控制边界，不是漏洞检测。
- **第一个 profile 就 mandatory。** 你会在理解合法 destinations 前阻断真实工作。
- **一个巨大 profile。** 按工作形状划分的 profile 才可审计；通用 profile 会变成无意义妥协。
- **忘记 `api.github.com`。** 如果设置 network policy 却不允许 `api.github.com`，profile 不能保留 GitHub CLI token。
- **假设运行中的 session 立即更新。** 它在 boot/wake 时解析 profile。
- **假设 Outposts 会自己执行。** operator 必须在 Devin 管理之外的基础设施执行 `spec.network_policy`。
- **用了 OIDC 却不收窄云 trust。** 无 key 不等于安全，如果 role 很宽或 trust policy 接受范围太大。
- **旧静态 key 仍保留。** 只有移除或禁用静态 keys，OIDC 才真正降低凭证风险。

## 练习

1. 给依赖更新 automation 写一份 profile 规格：network destinations、git access、MCP 需求，以及是否需要 `gh`。
2. 为这个 profile 的每项限制写一个正向测试和一个反向测试。
3. 给一个项目的只读访问设计 cloud trust policy。哪些 token claims 足够，哪些太窄？
4. 解释 mandatory enterprise profile 和更严格的 organization profile 如何取交集。

## Capstone

为一个低风险仓库维护任务构建受治理 automation 路径：创建 recommended profile，pin 到 automation，验证正向/反向行为；如条件允许，再给一个云只读操作配置 OIDC，并记录确切证据。只有完成这些后，才提出是否切换为 mandatory。

## Knowledge check

1. 为什么 Security Profiles 和 OIDC 是互补而不是替代？*（Profiles 限制 session 能接触或操作什么；OIDC 在不存长期凭证的情况下向服务证明 session 身份。）*
2. 为什么从 recommended enforcement 开始？*（它让你观察合法访问需求，避免在 allowlist 完整前阻断团队。）*
3. 为什么 child-session 委派不能绕过 profile？*（children 继承 parent 的同一治理链。）*
4. 为什么 OIDC 提高可审计性？*（云日志可以把操作归因到 session、organization 和 requesting-user claims，而不是共享静态 key。）*

## Sources

- [Security Profiles — 官方文档](https://docs.devin.ai/product-guides/security-profiles)
- [Cloud Authentication with OIDC — 官方文档](https://docs.devin.ai/product-guides/oidc)
- [Security Profiles API — 官方 reference](https://docs.devin.ai/api-reference/v3/security-profiles/list-organizations-security-profiles)
- [CognitionAI actions repository](https://github.com/CognitionAI/actions)
- [Devin Outposts overview](https://docs.devin.ai/cloud/outposts/overview)

## Changelog

- 2026-11-26 — 根据官方文档创建初版。云 provider 复现证据仍待补；验证命令已给出，但尚未在这里独立执行。
