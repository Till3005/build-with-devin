# 指南 6 — 事件驱动的 Automations

**目标：** 把外部事件——Slack、Teams、GitHub、Linear、Jira、PagerDuty、cron、webhook——接到会自己启动的 Devin 会话上。
**级别：** 入门（平台篇）· **用时：** ~20 分钟
**来源：** [Automations docs](https://docs.devin.ai/product-guides/automations) · [官方视频演示](https://www.youtube.com/watch?v=6xxKtIpgOyE)

## 解剖

每个 automation 都是四个部分：

| 部分 | 作用 |
| --- | --- |
| Trigger | 触发它的事件——一条 Slack 消息、一次失败的 CI、一次 cron 跳动、一个 HTTP webhook |
| Conditions | 可选过滤——只要 `bug` label、只要这个 repo、只要含 `/devin` 的消息 |
| Preflight check | 可选 LLM 过滤或脚本，在命中*之后*、动作之前跑——可跳过事件或拆成工作项 |
| Action | 跑什么：启动会话、给现有会话发消息、triage monitor、或邮件通知 |

## 触发器目录

| 来源 | 触发于 | 典型用途 |
| --- | --- | --- |
| Slack | 新消息、新增 reaction、用户组提及 | 分拣 `#incidents`；🚨 reaction → 调查 |
| Microsoft Teams | 消息、reaction | 在 bug 报告所在的 thread 里作答 |
| GitHub | Issue、issue 评论、PR、PR 评审、check run、push | 自动修失败 CI；`/devin` 评论 → 会话 |
| GitLab | MR、MR 评论、issue、push、pipeline | 修失败 pipeline |
| Linear | Issue 创建/标记/状态/优先级/指派/移动 | 工单指派给 Devin 时实现它 |
| Jira | Issue 创建/更新/标记/状态/指派/评论 | 同上，Jira 形态 |
| Pylon | Issue 创建/标记/状态 | 客户 bug 分拣 |
| PagerDuty | 事故触发/确认/解决 | 高优事故触发即查 |
| Schedule | Cron 或一次性 | 每日 Sentry 清扫、每周依赖更新、每晚冒烟 |
| Webhook | 任意 HTTP POST | 其它一切——Datadog、Sentry、你自己的系统 |

一个 automation 上的多个触发器按 OR 生效——例如 GitHub CI 失败*或* Slack reaction 任一即触发。

## 配方 1 — 任意 issue 上 `/devin`

野外部署最多的触发器：

```text
Trigger:   GitHub → issue comment, repo = your/repo
Condition: comment body starts with "/devin"
Action:    Start session — prompt includes the event payload
```

效果：团队任何人在 issue 评论 `/devin investigate this`，会话就带着完整 thread 上下文接单。

## 配方 2 — CI 失败自修复

```text
Trigger:   GitHub → check run, repo = your/repo
Condition: conclusion = failure
Action:    Start session: "CI check <name> failed on this commit.
            Diagnose the failure from the logs, fix it, and push to
            the same branch."
```

事件载荷把失败的 check + commit 带进会话——零人工复制粘贴。

## 配方 3 — 定时清扫

```text
Trigger:   Schedule → daily 09:00
Action:    Start session: "Sweep yesterday's Sentry issues in
            <project>. File the top 3 by impact as tickets and
            start the most actionable one."
```

每日卫生循环（Sentry 清扫、依赖更新、冒烟测试）是 ROI 最高的 automation——它们把"该有人看看"变成"已经看了"。

## 动作类型怎么选

| 动作 | 何时用 |
| --- | --- |
| Start session | 默认——每个事件得到全新机器和上下文 |
| Message session | 一个长驻会话持有状态——把事件喂进去（Bot 的种子形态） |
| Triage Devin | 一个常驻 Devin 盯整个 Slack 频道并派生子调查（事故场景见 Devin Oncall） |
| Email notification | 只是告诉你它跑了 |

**Automation vs Bot：** automation 是哑管道——事件进、会话出。Bot 在同一批触发器外加记忆、判断和跨会话规划。先用 automation；当工作需要跟进到底时再升级成 Bot（第 2–5 篇）。

## 动手建

Automations 页面上三条创建路径：

1. **Create** —— 空白编辑器：选 trigger → conditions → action
2. **Template** —— 常见工作流的预配 automation 画廊
3. **Generate with Devin** —— 用英文描述（*"when a CI check fails on my-org/my-repo, have Devin fix it and push to the same branch"*），复核生成的配置

咬过人的细节：

- Slack 触发器需要把 Devin 拉进频道**并且**在 Settings → Connections 连上你个人的 Slack
- Teams 私有频道只在 @mention 时触发
- GitHub 触发器必须指定具体 repo
- automation 多了用 **Terraform provider** 声明式管理

## Verify it

- [ ] 手动触发一次（评论 `/devin test` 或推一个失败 commit），看到会话带着事件载荷启动
- [ ] 不匹配的事件（错 label、错频道）什么都不发生
- [ ] 动作产出落在你预期的位置（PR、Slack thread、工单）

## Sources

- [Automations — docs](https://docs.devin.ai/product-guides/automations)
- [Devin Automations QuickStart (video)](https://www.youtube.com/watch?v=6xxKtIpgOyE)
- 相关：[第 3 篇 — 定时哨兵 Bot](bots-202-scheduled-sentinel.md)（在 cron 之上加 Bot 判断）
