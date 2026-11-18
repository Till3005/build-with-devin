# 指南 15 — 生产 trace 驱动的"活"评测集

**目标：** 一套自己会长大的 agent 评测集——一个定时 Devin 每周读生产环境的真实对话，在你系统的完整副本里复现每个失败，然后开 PR 把失败固化成回归测试。
**难度：** 进阶
**来源部署：** **Rox 的 Living Evals**——Rox 已经没人手写 eval。每周一个 Devin 读 Braintrust 里的生产 trace，在注入合成数据的 Rox 完整副本里复现每个失败、回放到 agent 犯同一个错，然后开 PR。评测集覆盖**真实使用量的 72%**（手写只有 43–57%），且逐周增长。
**来源：** [Living Evals 全文](https://www.rox.com/articles/living-evals-an-eval-suite-that-grows-from-production)（Brian Xu，2026 年 10 月）· [发布串](https://x.com/rox_ai/status/2110779380666617997)

## 模式

```text
生产 traces（可观测平台）
        │  每周抽样（~350 条对话）
        ▼
按行为分组（goal · output · mutation · target）
        │  数百条对话 → ~130 个行为
        ▼
对每个覆盖不足的行为：
   合成数据 → 完整副本 preview 环境 → 回放请求
   → 与生产 trace 对比 → 冻结为 eval → 开 PR
        ▼
人只 review PR，不写 eval
```

## 前置条件

- 生产环境有一个 agent 或 AI 功能，且具备**对话级 tracing**（Rox 用 Braintrust；LangSmith 或自建日志也行——需要请求 + 触碰过的记录 + 工具调用）
- 一个可部署的系统副本（preview env、staging 或 VM 里 `docker compose up`）——**不是 mock**
- 仓库里评测即代码，一条 eval 只是一个可提交的文件

## 第 1 步 — 先手动让一条 trace 可回放

上调度之前：挑一条你的 agent 失败过的真实对话。让 Devin 拉 trace、写出恰好覆盖请求所触数据的合成数据、拉起系统副本、回放请求直到同一个失败出现。手动都复现不了一个失败，周循环只会产出零。

## 第 2 步 — 冻结成 eval，而不是 bug 报告

产物是一条提交的 eval，不是一条 Slack 消息。Rox 的约定：请求**逐字**复制自生产；注入的数据复现精确条件（如"最新的会议没有 transcript"）。改数据的请求用代码断言；只回复的请求用 LLM judge 评分标准。

## 第 3 步 — 先按行为分组再上量

每条对话都跑循环是浪费——多数请求形状重复。Rox 用四个标签定义*行为*：**goal**（用户要什么）· **output**（返回什么）· **mutation**（不动/创建/编辑/发送）· **target**（指名 vs 推断对象）。每周 ~350 条对话收敛到 ~130 个行为；只为覆盖不足的行为造 eval。

## 第 4 步 — 把整个规程固化成一个 skill

trace→eval 循环活在 Devin 遵循的**一个 skill 文件**里：拉 trace → 合成 → preview env → 回放 → 对比 → 冻结 → PR。循环产出坏 eval 时，**改 skill**，绝不手改 eval——这才是复利动作。

## 第 5 步 — 每周定时跑

cron automation（指南 6）：拉本周 traces → 分组 → 对每个覆盖不足的行为跑循环 → 开一个 PR 装新 eval。人 review PR；Devin 拥有整个评测集。

## Verify it

- [ ] 一个真实生产失败在 preview env 里可确定性回放——同一用户请求，同一坏结果
- [ ] eval 文件在仓库里、跑在 CI 上、旧行为红新行为绿
- [ ] 覆盖率按*生产流量结构*测，而不是按你的猜测——像 Rox 的 72% 那样报出来
- [ ] 一条坏 eval 是通过改 skill 修好的，不是改 eval

## 常见陷阱

- **mock 回放。** Rox 早期用 mock 数据层回放——mock 会把它替换掉的代码里的 bug 藏起来。用完整副本；preview env 的意义就是保真度。
- **judge 抖动。** 即使不改代码，约每 8 条 eval 有 1 条时过时不过——agent 不是确定性的。失败要读过再信，单点抖动别报警。
- **评测口味。** 这套抓的是行为回归（工具路径死了、支持的请求不接了），不是风格——每个失败都该指向可修的缺陷。

## 自检

1. 为什么要在完整副本里回放而不是 mock 数据层？*（mock 会把它替换掉的代码里的 bug 藏住——agent 改的状态越多，mock 本身就成了你实际在测的东西。）*
2. 为什么先把对话按行为分组再写 eval？*（多数请求形状重复——goal/output/mutation/target 四个标签让一条 eval 覆盖多条对话，覆盖率才映射到真实用量。）*
3. 复利动作是改 eval 还是改 skill？*（skill——手改 eval 教不了 Devin 任何东西；改好的 skill 永远产出更好的 eval。）*

## 来源

- [Living Evals: an eval suite that grows from production](https://www.rox.com/articles/living-evals-an-eval-suite-that-grows-from-production)——完整方法论
- [Rox 发布串](https://x.com/rox_ai/status/2110779380666617997)
- 相关：[指南 13 — 官方 cookbook](official-cookbook.md) · [指南 6 — Automations](automations-101-event-driven.md)
