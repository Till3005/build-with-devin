# 指南 19 — 会话全环：研究、委托、审查，以及成本

**目标：** 跑通 Devin 全环——写简报前先用索引理解代码库，委托一个有边界的会话，让独立审查过一遍 PR，再读 Session Insights 让下一环更便宜。
**级别：** 入门（与[指南 18](talking-to-devin.md) 配套）
**来源：** [Devin University — Cloud 101/103](https://learndevin.com) · [DeepWiki 文档](https://docs.devin.ai/work-with-devin/deepwiki) · [Ask Devin 文档](https://docs.devin.ai/work-with-devin/ask-devin) · [Devin Review 文档](https://docs.devin.ai/work-with-devin/devin-review) · [Session Insights 文档](https://docs.devin.ai/product-guides/session-insights)

## 大多数人只做了一半的环

指南 18 教你写一条 Devin 不会误读的简报。Devin University 的 Cloud 系列把这条简报放进了产生它、消费它的完整环路：

```
理解 ──► 委托 ──► 审查 ──► 复盘
 DeepWiki    简报+会话      Devin Review    Session Insights
 Ask Devin                  在 PR 上        → 更好的下一条简报
```

多数失败的会话死在两端而不是中间：写简报时对代码库一无所知，或者凭感觉合并了 PR。本指南讲这两端，以及贯穿全程的那台计费器。

## 理解：在烧第一个 ACU 之前用 DeepWiki 和 Ask Devin

**DeepWiki** 会自动索引你连通的仓库，为每个仓库生成 wiki——架构图、摘要、源码链接，可用 `.devin/wiki.json` 配置。它回答那些否则要花会话时间才发现的问题：这个模块在哪、谁在调它、既有模式是什么。

- 力度档位按组织设置（可按仓库覆盖）：**Low 免费**且是默认；Medium 每个 wiki 约 5–10 ACU，High 约 20–40。大多数仓库 Low 就够支撑写简报。
- 入门引导会自动索引你配置的仓库；其余在 **Settings → DeepWiki** 下补加。
- 公开仓库有免费版 [deepwiki.com](https://deepwiki.com)——索引任何公开 GitHub 仓库，拿到同样的架构图和问答，不需要账号。另有 DeepWiki MCP 可供你的其他 agent 使用。

**Ask Devin** 是索引之上的对话层——在 [app.devin.ai/search](https://app.devin.ai/search)：

- **Ask 模式**：就代码提问，答案带代码引用、基于索引——"billing poller 的重试逻辑怎么跑"会返回文件、调用点和模式。
- **Plan 模式**：描述改动，Devin 和你一起圈定范围——然后生成一条上下文充足的提示词，直接交给会话。这是满足指南 18 规则最便宜的方式：从哪里下手、参照什么模式，都从索引里来，而不是凭你的记忆。
- 在对话里直接开会话，状态也留在对话里——不用切窗口。

这里的回报是双份的：基于索引事实写出的简报既更精确*又*更短。

## 委托——你已经会的那一步

把 Ask Devin 生成的提示词（或你按[指南 18](talking-to-devin.md) 写的简报）作为一个有边界的会话交出去。变化只在于简报已经知道一切：文件、模式、验收检查、边界。

## 审查：每个 PR 上的第二个 agent

**Devin Review** 是独立审查者，不是会话自评的重播：

- 按 PR 触发：在 GitHub PR 或 GitLab MR 上评论 `/devin review`，或在 [Devin Review](https://app.devin.ai/review) 里打开 PR。它把相关改动分组、贴着 diff 解释，并指出 bug 和安全发现——可以引用进聊天，包括让 Devin 就地修复。
- 组织级：有自动审查、审查指令和成本控制，可以在每个 PR 上跑。Review 2.0（2026 年 11 月）把单 PR 审查成本砍了 **82%**——常开在经济上才成立。
- Devin 自己的 PR 也用。写的人和审的人是不同 agent，这正是要点——和指南 18 分派给你的不对称是同一个。

## 复盘：Session Insights 和 ACU 计费器

每个完成的会话都有一份 **Session Insights**（菜单 **⋯ → Session insights**，免费）：

- **会话尺寸标签**——XS–XL 自动分类在拆除时生成；L/XL 会话自动生成完整分析，较小的可手动触发。
- **ACU 用量**（按量计划显示美元）——横向对比同类任务，找出把算力烧在重试和死胡同上的会话。
- **用户消息数**——数高说明简报缺上下文；每条消息都是本可在开头写明的纠偏。
- 分析会给出具体改进建议——更紧的提示词、缺的 knowledge、错误的范围。Cloud 103 的那句话是对的：*让每个会话都比上一个便宜。*

每份实战报告里都会出现的成本纪律：会话范围收窄、空闲会话杀掉（思考和等待都计费）、开舰队前查额度——100 Days 那位操盘手在 Bot 搭建两天里烧掉了**每周额度的 33%**（[实战报告](community-field-reports.md)）。社区实测的一条 Bots 专属提醒：给 Bot 的子会话接上*自己的*模型 key **并不能**阻止套餐周额度消耗——Bot 本体推理加云端算力仍然记在你的套餐上（[linux.do 实测](https://linux.do/t/topic/3225152)）。

## 验收清单

- [ ] 不开会话，你就能从 DeepWiki/Ask Devin 答出"X 在哪、谁调它"。
- [ ] 你的下一条简报里至少有一个来自索引而非记忆的事实。
- [ ] 你碰的上一个 PR 跑过 Devin Review——你的或 Devin 的。
- [ ] 你能读出上个会话的尺寸、ACU、消息数，并说出一项分析标记。

## 常见坑

- **盲写简报。** 凭几个月没碰的代码库记忆写提示词——索引现在比你懂。Ask Devin 两分钟好过会话中途纠偏。
- **CI 绿了就跳过审查。** CI 检查的是你想起来要查的东西；Review 读的是 diff 本身。两张网不同。
- **只在失败时看 Insights。** 最贵的模式是那个你每周重复的平庸会话。成功的也要复盘——可复用的简报就藏在那里。
- **力度档位超支。** 对每季度才碰一次的仓库开 High 级 wiki；按仓库覆盖就是为此存在。

## 自测

1. *为什么从 Ask Devin 开会话而不是从 Devin 侧栏？* 因为 Plan 模式把提示词扎进索引过的代码——从哪里下手、既有模式、可验收的覆盖面都来自仓库本身，会话一开始就带着你否则要手打或中途才发现的上下文。
2. *会话自己的报告说做完且测过了，为什么还要跑 Devin Review？* 独立性。会话给自己的作业打了分；Review 是另一个 agent 用全新上下文读 diff——和队友的 PR 不能自我批准是同一个道理。
3. *ACU 是固定费率，一个会话跑成了 XL，先查什么？* Session Insights 里的用户消息数——一个被大量小纠偏驱动的大会话是简报问题，不是任务体量问题。先拆分或重写简报，再假设活本来就大。

## 来源

- [Devin University](https://learndevin.com)——Cloud 101（本环）和 Cloud 103（效率）课程；课程免费，考试需 Enterprise 席位
- [DeepWiki](https://docs.devin.ai/work-with-devin/deepwiki) + [Ask Devin](https://docs.devin.ai/work-with-devin/ask-devin)——索引、力度档位、Plan 模式，公开仓库用 [deepwiki.com](https://deepwiki.com)
- [Devin Review](https://docs.devin.ai/work-with-devin/devin-review)——`/devin review`、自动审查、[Review 2.0 降价](https://devin.ai/blog/devin-review-2)
- [Session Insights](https://docs.devin.ai/product-guides/session-insights)——XS–XL 分档、ACU/消息指标、API
- 下一条：[指南 18 — 和 Devin 说话](talking-to-devin.md) 如果还没读 · [指南 9 — Playbooks](playbooks-and-knowledge.md) 把改好的简报固化下来
