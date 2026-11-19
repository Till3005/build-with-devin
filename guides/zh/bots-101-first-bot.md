# 指南 1 — 你的第一个 Bot

**目标：** 创建一个拥有结果的 Devin Bot，并学会后面每篇指南都要用的六个机制。
**级别：** 从这里开始 · **用时：** ~15 分钟
**来源：** [官方 Bots docs](https://docs.devin.ai/work-with-devin/bots)、[launch post](https://devin.ai/blog/introducing-devin-bots)

## Bot 是什么

一个 session 完成一个请求。一个 Bot *拥有一个结果*：你在它的聊天里说一次目标，它规划工作、为每一块启动子 Devin 会话、盯着它们，只把需要你判断的东西带给你。它是持久的——记忆、会话、automation 跨周存续。

六个机制，按你会遇到它们的顺序：

| 机制 | 是什么 | 在哪里碰它 |
| --- | --- | --- |
| Chat | Bot 所拥有的一切共用的一条 thread——目标、汇报、提问 | Bot 页面 / Slack / iMessage |
| Sessions | 每块工作作为独立 Devin 会话跑在独立机器上 | 由 Bot 启动和监控 |
| Needs you | 决策、PR 评审、权限请求、汇报——一个列表 | Bot 聊天顶部 |
| Memory | Bot 学到的东西，存成文件，每次会话启动时读 | Settings → Memory |
| Instructions | 人写的常驻规则，每次会话启动时读 | Settings → General |
| Access | Bot 自己的连接/密钥，外加 Bot 之间的 grant | Settings → Access |

## 第 1 步 — 创建

侧栏 → **Bots** → *Create new Bot* → 选模板或 *Start from scratch* → 命名。

新 Bot 默认私密，分享前只有你能用。它的用量像普通会话一样计入你的方案。

> 提示：模板自带某一岗位的指令（QA Engineer、Data Analyst……）。本仓库的指南适合 *Start from scratch*——outcome prompt 你自己写。

## 第 2 步 — 指派结果

第一条消息是 Bot 收到的最重要的输入。给*目标*，不是任务：

```text
You own the Android app now. Keep it at feature parity with iOS.
```

这是 Cognition Android Bot 的原话。对比：

| 弱（任务） | 强（结果） |
| --- | --- |
| "Fix the checkout button" | "You own checkout. Keep it fast, correct, and covered by tests." |
| "Update the docs" | "You own the docs. Keep them in step with `main`." |
| "Watch CI" | "You own build health on `main`. When a check regresses, find the cause and fix it." |

任务做完就结束；结果让 Bot 永远重新规划。

### 有界的第一个任务

"所有权"是对的*形状*，但第一次跑要把*面*收窄：一条流程、一个环境、一个审阅人——你。ANO 实战指南的模式是最稳的起点：

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

承重的那几行：旅程的定义（表单 → 邮件 → 链接，不只是"表单能用"）、*先跑一次再谈排程*、明写的禁 merge/禁部署边界、以及点名要的证据。Bot 连续两次交回可信证据之后，再扩大任务面。

## 第 3 步 — 与它协作

结果设定后，你的消息大多是查岗：

```text
anything waiting on me?
```

Bot 标记事项时打开 **Needs you**（聊天顶部）：

| 条目 | 你的动作 |
| --- | --- |
| Decision | 选一个——Bot 会标出它的推荐 |
| Review PR / Merge PR | 审或合并 |
| Permission request | 批准或拒绝新权限、automation、网络主机或用量上限提升 |
| Report / FYI | 读它 |

每条都可以用自己的话回复、稍后处理或忽略。

## 第 4 步 — 用记忆掌舵，别微操

- **Instructions**（Settings → General）：你的常驻规则——Bot 跑的每个会话启动时都会读。持久策略放这里，不放聊天。
- **Memory**（Settings → Memory）：Bot 自己写的文件——偏好、纠正、项目事实。要改它的记忆，直接在聊天里说（"remember: we deploy via Cloud Run, never bare VMs"）。能用这个 Bot 的人都能读它的记忆——共享 Bot 的记忆按共享对待。

可扩展的模式：纠正 Bot 一次，让它把纠正写进记忆，之后每个会话都继承。Cognition 就靠这个循环每周合并 2,000+ PR。

## 共享之前——权限与用量

发布帖不会讲但文档写明了两件事：

- **私有 Bot 会不打招呼继承你的资源。** 你已有的权限可以不经新的确认就被记录成 grants——私有 Bot 不是沙箱。共享之前打开 Settings → Access，摘掉任务不需要的 grants。如果想让队友抄方法但看不到你的对话和凭证，共享*模板*，不是 Bot 本体。
- **Bot 的用量 = 它的聊天 + 它起的全部会话。** Max：先用你的包含额度再用按需付费——没有单独的 Bot 上限。Teams：你的额度然后团队点数，管理员可以设 Bot 专属按需上限。Enterprise：默认计入创建者上限，除非单独分配。聊天里写的花费指令不是配置好的上限——上限在 Settings 里设，别用自然语言描述。

## 第 5 步 — 放到你工作的地方

- **Slack：** 给 Bot 配自己的 Slack app，团队就能 @ 或私信它（Settings → Slack）。所有公开的团队部署都这么跑——Bot 变成频道里一个有名有姓的队友。
- **iMessage：** 手机上直接给 Bot 发短信。
- **Web：** 侧栏 Bots 区列出你的和共享给你的。

## 第 6 步 — 排程与模式

- **Automations：** 在聊天里说——*"run a summary of open PRs every weekday morning"*——Bot 会提议一个 automation 等你一次性批准。之后在 Settings → Automations 管理（暂停/恢复/删除）。
- **Modes：** Bot 有自己的模式，外加它派生会话用的 **Child Capability** 默认值（聊天里模式选择器的 `Normal / Ultra` 等）。也可以对任何单个会话临时换模式。

## 生命周期

| 动作 | 效果 |
| --- | --- |
| Recycle | 终止当前会话；下次打开时启新会话。在聊天菜单里。 |
| Archive | 停止响应、从 Bot 列表移除、移除其 Slack app 和 Bot 间 grant（取消归档不会恢复这些——要重新配）。 |
| Delete | 永久：设置、会话、记忆、automation。不可撤销。 |

只有创建者和带 Manage Bots 权限的角色能看到 Archive/Delete。企业版里 `Use Bots` / `Manage Bots` / `Manage Bots across the enterprise` 是自定义角色里的独立权限。

## Verify it

- [ ] Bot 已创建并命名；outcome prompt 已在聊天里发出
- [ ] Bot 没有被催第二次就启动了至少一个子会话
- [ ] **Needs you** 里出现了决策/PR/权限请求且你已处理
- [ ] 你在聊天里给的一条纠正出现在 Settings → Memory 的记忆文件里
- [ ]（可选）Slack 里 @ 它能够得到响应

## 坑

- **任务形 prompt。** "Fix X" 产出的是会话，不是 Bot。如果 Bot 干完就安静了，说明 prompt 是任务——改成所有权表述。
- **把策略写进聊天。** 聊天里的规则会滚走；Instructions 里的规则每个会话都读。聊天 = 方向与答复；Instructions = 法。
- **不看 Needs you。** Bot 的设计就是攒判断题——每天看一两次就行，不用盯。

## 自检

1. 一次性会话结束之后，Bot 还保留了什么？*（记忆——加上常驻的目标、计划和各个 surface。）*
2. 为什么 Bot 是「needs-you」而不是会话中途问你？*（判断进入一条异步线程；人不是循环里的阻塞调用。）*
3. 哪个机制把「聪明的会话」变成了「员工」？*（对结果的所有权——任何单个会话结束后目标仍在。）*

## Sources

- [Devin Bots — docs](https://docs.devin.ai/work-with-devin/bots) —— 机制、权限、用量上限
- [Introducing Devin Bots](https://devin.ai/blog/introducing-devin-bots) —— 发布帖，Android Bot 的原话 prompt
- [AI Native Operators — Devin Bots: give an agent a job to own](https://ainativeoperators.ai/blog/devin-bots-guide) —— 社区实战指南；上面的有界首个任务和权限/用量提醒出自此
- 上一篇：[指南 18 — 跟 Devin 说话](talking-to-devin.md)（outcome prompt 底下的基本法）· 下一篇：[第 2 篇 — 产品所有制 Bot](bots-201-product-owner.md)
