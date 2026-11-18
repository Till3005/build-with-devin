# 指南 2 — 产品所有制 Bot

**目标：** 一个像产品经理一样拥有整个 app 面的 Bot——自己建 ticket、实现、合并、每日汇报。
**级别：** 中级 · **建好后的人类负载：** 约每 6 个已合并 PR 1 条消息
**出处部署：** Cognition 的 **Android Bot**——**44 天**把 Devin 安卓 app 送上 Google Play 开放 beta：1,134 个已合并 PR、344,651 行 Kotlin、2,841 个截图测试、1,217 张 ticket。人类**总共发了 183 条消息**（其中 22 天零消息），**88% 的 PR 自合并**。它现在负责 Android/iOS 功能对齐。
**来源：** [launch post](https://devin.ai/blog/introducing-devin-bots) · [Fortune](https://fortune.com/2026/11/17/exclusive-cognition-bets-on-devin-bots-coding-agents-in-challenge-to-anthropics-duet-and-openais-dots/) · Russell Kaplan 的 dogfooding 笔记

## 模式

一个 Bot 拥有一个*面*——一个 app、一个站、一个服务——就像 PM 拥有它：它决定建什么、拆成 ticket、每张 ticket 跑一个会话、让这个面无限期活下去。人类扮演它汇报的高管。

```text
Bot ──► files tickets ──► session per ticket ──► PR ──► CI + Devin Review ──► merge
 │                                                                           │
 └──────────── daily report + Needs-you decisions ◄──────────────────────────┘
```

## 前置条件

- 一个 Bot 能完全拥有的 repo（带 CI、评审、合并路径的 app repo）
- repo 上启用 Devin Review 并接好 CI 检查
- 给 Bot 配 Slack app（推荐——所有公开部署都在 Slack 汇报）

## 第 1 步 — outcome prompt

Cognition 原话，一字未改：

```text
your job is to product manage the android app. Basically, you're going to
autonomously create the entire thing, but we need to figure out what the
blockers are for you doing that first.
```

泛化到你的面的模板：

```text
Your job is to product manage <surface>. You're going to autonomously
<build / keep parity with <reference>>, but first enumerate the blockers
to you doing that — where the code lives, how to build and test it, and
how changes merge — then start working through them.
```

注意形态：**所有权 + 自主权 + 先列阻塞**。别递 backlog；给授权，让它自己暴露需要什么。

## 第 2 步 — 第一阶段：先解阻塞，不写码

Android Bot 第一件事不是写码——是枚举阻塞：repo 访问、构建命令、怎么在设备/模拟器上测、合并路径。你的版本清单：

- 它能在自己机器上构建项目吗？（blueprint/snapshot 依赖）
- 它能产出可安装产物吗（APK/TestFlight/preview deploy）？
- 它知道合并策略吗——必须过哪些检查、谁审？
- 它有需要的凭证吗（商店密钥、签名）——或有书面的 grant 申请路径？

让它先做完这份审计再建产品 ticket。这里解掉的每个阻塞都是你以后看不到的卡死会话。

## 第 3 步 — 工作循环

解阻塞后的稳态：

1. Bot 为它决定的下一单元工作建 ticket
2. 子会话实现并开 PR——小、带可运行证据
3. CI + Devin Review 把合并门
4. Bot 合并（需要判断时进 Needs you 问你）
5. 日报落到 Slack——Android Bot 的日报带改动的**录屏**

汇报写在 Bot 的 Instructions 里，不靠聊天：

```text
Every day, post a report in #<channel>: what shipped, what's in flight,
what needs a human. Include a screen recording of visible changes.
```

## 第 4 步 — 你作为它的高管的工作

44 天 183 条消息就两类：

- **判断题** —— 安全评审签字、设计取舍、审批卡
- **方向** —— 文档原例是 "be more ambitious"（更有野心一点）

其它一切——ticket、实现、修复、自合并——都是 Bot 的活。如果你在答实现问题，说明你管得太低。纠正一次 → 落进记忆 → 下个会话继承。

## 稳态

初始构建完成后，同一个 Bot 切换成*拥有*这个面：

- 与参照项目保持对齐（Android Bot 现在追踪 iOS 功能）
- 分拣进来的反馈（它处理 Google Play beta 反馈）
- 抓跨面回归——Android Bot 自主发现并修复了别人改动造成的 iOS/web 侧破坏

## Verify it

- [ ] Bot 的第一动作是阻塞审计，不是 PR
- [ ] 它不被催也会自己建并消化 ticket 队列
- [ ] PR 都小且带证据（测试、截图、录屏）
- [ ] 日报带可见证据发到 Slack
- [ ] 你一整天零消息，PR 照样合并

## 坑

- **跳过阻塞阶段。** 还不会构建/测试/合并就开始写码的产品 Bot 只会产出孤儿 PR。
- **大 PR。** 这个部署的安全性来自小而可验证的单元。PR 变大就下指令：*"one ticket, one concern, one PR."*
- **审代码而不是审方向。** 每周 30+ PR 时你审不完每个 diff——靠 CI + Devin Review + Bot 的证据把门，把你的消息花在方向上。

## Sources

- [Introducing Devin Bots](https://devin.ai/blog/introducing-devin-bots) — Android Bot 数字与 prompt
- [Fortune exclusive](https://fortune.com/2026/11/17/exclusive-cognition-bets-on-devin-bots-coding-agents-in-challenge-to-anthropics-duet-and-openais-dots/) — 183 条消息、88% 自合并、dogfooding 笔记
- 相关：[第 4 篇 — 多 Bot 组织](bots-203-multi-bot-org.md)（当一个面变成一门生意）
