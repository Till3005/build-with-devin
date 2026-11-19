# 指南 14 — 社区实战报告

**目标：** 工程师把 Devin 用在真实工作上后实际学到了什么——包括失败。蒸馏自已发表的 hands-on 记录，好评和恶评都有。
**级别：** 入门（判断力篇）
**来源：** 各条报告下方逐一标注

本篇刻意保持平衡：Devin 在哪里稳赢、在哪里烧钱、以及区分两种结果的工作方式。

## 每篇报告都在重复的模式

拿到结果的人把 Devin 当作**异步初级工程师**，而不是代码生成器。Scott Wu（Cognition CEO）在 [Lenny's Newsletter](https://www.lennysnewsletter.com/p/how-devin-replaces-your-junior-engineers) 里描述了内部工作流：委派边界清晰的任务、让它在你开会时跑、审 PR。[Every 的记录](https://every.to/chain-of-thought/coding-with-devin-my-new-ai-programming-agent)落到了同一个框架——它需要一套*技能*：学会它擅长什么、写它懂的任务、知道何时介入、学会信任以不同于你的方式完成的活。

## 有据可查的成功场景

**端到端原型。** 从空 repo 起步，Devin 搭了一个 FastAPI + React 的 "City Explorer"（图片/天气/新闻集成）、本地跑起来、开 PR、部署公开 URL——~90 分钟，~2 次人工介入（[Medium hands-on](https://medium.com/@sambhavgaur_70582/copilot-cursor-or-devin-my-hands-on-weekend-with-ai-that-codes-and-deploys-acc708e802b3)）。[Scott Logic](https://blog.scottlogic.com/2025/10/20/rapid-development-with-devin.html) 在真实客户原型上报告了同样的弧线——外加下方一条关键迭代教训。

**需要运行时的活。** 在[与 Claude Code 的对决](https://web.archive.org/web/20260718112612/https://mohitkhare.me/blog/devin-vs-claude-code/)中，Devin 在贴合既有规范的任务上输了，但在有机器加成的地方赢得很清楚：内存泄漏排查——它做 profile、在负载下抓堆快照、产出报告。agent 自带 VM 就是卖点。

**现场排障。** [Faros](https://www.faros.ai/blog/how-to-use-devin-ai-troubleshooting) 在*客户电话上*用 Devin：它读了 introspection API 代码、几秒内生成可用 `curl`——把 1-2 天的跟进循环压缩进电话本身。

**有新文档加持的真实迁移。** 在一个难啃的 Vue→React 代码库上做 Tailwind 3→4 + DaisyUI 4→5 升级成功了——团队通过 Context7 MCP 给 Devin 喂了最新文档：prompt 携带的是*上下文*，不只是任务（[Bootcamp write-up](https://medium.com/design-bootcamp/day-7-of-30-getting-to-know-devon-ai-and-working-with-him-743c351cd0c4)）。

**自我验证。** 一篇[一年期实践者对比](https://architecttocto.substack.com/p/the-only-coding-agent-worth-paying)把 Devin 的浏览器驱动 e2e 测试标记为分水岭时刻：它走到自己造的东西那里亲自检查——这个反馈回路像工程，不像生成。

**代码之外。** 一位 Cognition 研究员报告 Devin 重建——并完成——了他九年前花了一整个学期没做完的 Lean 形式化证明，用时**不到 15 分钟**（[post](https://x.com/penlume/status/2115806616796921885)）。数学形式化和迁移奖励同一种特质：机器可检验的完成定义。

**接入可观测性。** [Dynatrace MCP + Devin](https://medium.com/lets-code-future/how-i-turned-devin-into-a-performance-analysis-agent-with-dynatrace-mcp-753d3f4790a2) 把 Devin 变成性能分析 agent：它查询实时指标和 trace 然后诊断——MCP server 带来了 repo 里没有的生产上下文（Medium）。另见 [Devin: from bug report to pull request](https://medium.com/@winter.inc/devin-from-bug-report-to-pull-request-25-days-of-ai-day-18-b158daa20f23) 的完整 ticket→PR 循环。

## 有据可查的失败场景

- **模糊或过宽的 prompt。** Scott Logic 的第一条 prompt 产出了不可用的脚手架；收窄技术栈和诉求（"just the models"）后解决。Devin 会过度构建——告诉它*不要*建什么。
- **贴合既有规范的任务。** "Add pagination to this endpoint" 在两份独立报告里都返回了不符合代码库惯例的实现（[amillionmonkeys](https://www.amillionmonkeys.co.uk/blog/ai-coding-tools-small-studios)、[mohitkhare](https://web.archive.org/web/20260718112612/https://mohitkhare.me/blog/devin-vs-claude-code/)）——除非你把规范带给它，Devin 是在真空中构建（→ 第 9 篇）。
- **不可检验的活。** [expectedwrong](https://expectedwrong.com/devin-appraised) 和 [alanwest 的 10 任务测试](https://dev.to/alanwest/i-gave-devin-10-real-tasks-it-completed-3-3063)记录了失败模式：自信但坏掉或缺失的输出、credit 在循环中烧掉。他们的任务偏向没有明确验证的活——正是官方 playbook 强制要求的那道闸（第 11 篇）。

## 实名团队部署（社区、带数字）

公开运营数据的真实组织——大多来自日本工程社区，那里的记录异常详尽：

| 团队 | 部署 | 报告结果 |
| --- | --- | --- |
| rakko_inc | Devin 自动代码评审：Playbooks + GitHub Actions + Devin API——每个 PR 在人看之前先被预消化 | **月评审 PR 65 → 184（2.8×）**；人从 Devin 的摘要开始看（[report](https://zenn.dev/rakko_inc/articles/00cc5a5a679971)，JP） |
| Skillnote (QA) | PR → Actions → Devin 生成测试设计草稿（CSV/Excel，含"为什么是这个用例"）回贴 PR | **每 10 个用例省 ~35 分钟**；Devin 设计的用例抓到过人漏掉的 bug（[report](https://zenn.dev/skillnote/articles/5ba429ca249801)，JP） |
| arufian | Serverless GitHub 事件自动化（无常驻服务器）：`devin:fix`/`devin:plan` label 驱动 Devin 会话，配**优先级×复杂度策略表**和 plan-first 审批流 | 安全扫描拦截高风险 PR；高复杂度走 plan → 人批准 → `run that plan`（[report](https://zenn.dev/arufian/articles/f80a62f5217cee)，JP） |
| Leverages (levtech) | 组织级铺开：14 个团队 / ~30 人 | ~2.5 个月 **177 个已合并 PR**；ROI 按 `ACU 成本 − 节省工时 × 工资` 计量并跟踪任务类型占比（[report](https://zenn.dev/levtech/articles/9c869303820844)，JP） |
| Decagon | Devin Cloud 上的 AutoResearch：一个编排者 Devin + 并行子 agent 竞争假设；每个想法用 Modal GPU 上回放的生产流量验证 | 支持类流量上 **GPU 吞吐最高 2.5×**（[writeup](https://x.com/DecagonAI/article/2115511110120120437)） |
| Nader Dabit | 个人 5-Bot 组织——**CTO**（全会话/全仓库，iMessage VIP 通道）、**Auto(mation)Bot**（代管 automations、性能报告）、**DevCommunityBot**（大使计划数据 → 迷你应用）、**DevRelBot**（文档 + 教程视频，*有自己的电脑、自己的 Devin/GitHub/Linear 账号、ElevenLabs 声纹克隆*） | 另有 **Windfable**：~10 个 SuperJennyStack Bot 跑 Unity iOS RPG，每 bot 配独立 macOS+Xcode+Unity，测 iPhone Duo 折叠/展开双态，前后截图+实机视频对比（[primer](https://x.com/dabit3/status/2122755275182469515)） |
| Mark Fenner | 单人操作者跑 4 个分工 Bot，由一个协调者 Chief Agent Bot（"Frankie"）统领 | 经单一决策面汇总汇报——多 Bot 组织形态不需要团队就能跑（[walkthrough](https://x.com/markfenner/status/2122740244328145211)） |
| hubble | 两条常驻回路：每个 Dependabot PR 在人看之前先由 Devin 调查——打 GREEN/YELLOW/RED 风险标签**并把依据写进评论**；每周 Datadog CCM 回路挑一个成本候选、深挖、交回可直接决策的报告 | 人打开 PR 时评审材料已经备好；交付物是依据而非标签（[Dependabot 回路](https://zenn.dev/hubble/articles/88429bd24db476)、[成本回路](https://zenn.dev/hubble/articles/091e29a0c86ec3)，JP） |
| SMARTCAMP | 常驻安全流水线：定时 GitHub Actions 拉 ECS 镜像 → Trivy 扫（HIGH/CRITICAL）→ 建 issue → Devin 修复；AWS 凭证与扫描任务隔离只让产物跨边界；hash 固定 + 发布后 7 天宽限期防扫描器滞后 | 漏洞修复做成流水线，不是一次性会话（[report](https://zenn.dev/smartcamp/articles/97ac804043530e)，JP） |
| canly | Devin 当分析师而非码农：把 ~700 条历史工单分类，弄清「原因未特定」到底是什么 | 过半根本不是 bug；给 AI 喂什么上下文（DB？文档？）比选哪个模型更关键（[report](https://zenn.dev/canly/articles/9c19bb123e208c)，JP） |

其中可复用的思想：**策略表门控**（arufian：只自动 PR 低风险活、复杂的走 plan-first）、**定式输出 prompt**（Skillnote：固定 CSV 格式 + 内联 Python 转换消除输出抖动）、**评审预消化**（rakko：人看之前 Devin 先摘要+标记）、**理由先行分诊**（hubble：标签只是指针，带着证据的评论才是交付物）、**流水线化修复**（SMARTCAMP：扫描 → issue → 修复一条 CI 式回路，带凭证与免凭证的段分开）、**诚实记账**（levtech 的 ACU-vs-工资 ROI 公式）。

**组织运营的细账**（来自 Leverages ~30 人的铺开，同一篇报告）：

- 一个 Slack workspace 只能绑**一个** Devin 组织——规划 Slack 驱动会话前，先查有没有别的部门已经占了坑。
- 没有按团队限 ACU 的配额功能；他们用 API 列会话、再抓网页拿每个会话的 ACU 来汇总——预算靠可视化，不靠硬限制。
- 隐形 ACU 消耗：默认 Devin 开的 PR 上每条评论都会唤醒会话。他们打开了 **"Only respond to PR comments that mention Devin"**，让人随便讨论。
- 仓库 onboarding 是串行的——一个在 setup 中就卡住下一个，得排期。
- 他们的 ROI 分布：高的在 PR 预评审（`devin-review` 标签 → Actions → API Playbook，每次 ~1–2 ACU）、定期库升级风险评估、以及喂了*相似既有 PR* 的遗留代码活；低的在大范围重构和小到不值得的任务。

## 蒸馏出的教训

1. **切的是片，不是项目。** 成功全是有边界的单元；失败都是"去把这个大致建/修一下"。（官方教条：第 13 篇。）
2. **能验证才委派。** 给 Devin 机器能判定"完成"的活——测试、构建、能跑的 `curl`、渲染出来的页面。
3. **带上下文，不带假设。** 规范、最新文档（经 MCP）、你的技术栈形态——失败都是上下文失败，不是能力失败。
4. **委派；别盯着。** 每篇正面报告里的 ROI 都来自*异步*——任务在你干别的时跑。盯着它打字是你觉得它"慢"的原因。
5. **迭代 prompt，不是迭代工具。** Scott Logic 的修复不是换 agent——是收窄 prompt。把第一次失败当 prompt bug 处理。
6. **交付证据，不交付判决。** hubble 把 Dependabot skill 的最后一步从「决定是否合并」改成「评估风险」——agent 组装案情，人保留决定权。

## Scott Wu 的内部 top-5（来自 Lenny's 访谈）

Cognition 自己委派最多的任务：**前端修复、版本升级、文档、事故响应、测试**——外加"第一道防线"模式（Devin 在人介入前先分析 crash），以及用 DeepWiki 调研来*写出更好的 prompt*。

## 验证

- [ ] 挑一篇和你技术栈最接近的报告，去读原文而不是这份蒸馏——那个数字放回上下文里还成立吗？
- [ ] 写下你敢赌钱复现到自己团队的一条教训；说不出来就换一篇

## 常见陷阱

- **幸存者偏差。** 叫好的报告发数字，无声的失败什么都不发。把本合集里的失败当作中位体验，把胜利当作天花板。
- **东施效颦。** Scott Logic 的 prompt 迭代有效是因为*他们迭代了*——只抄最终 prompt 不抄循环，你得到的是他们的起点而不是结果。

## 自检

1. 失败报告有什么共性是成功报告没有的？*（不可验证的委托——失败案例把工作交给 Devin 却没人能检查「完成」；每个成功都定义了检查。）*
2. 为什么 Faros「在客户电话上排障」是部署经验而不是轶事？*（它展示了实时分诊范式：agent 做第一响应，人守住客户关系。）*
3. 为什么这篇把敌对报告和正面报告等量收录？*（对抗性报告暴露边界条件——地图的边缘是从走出去的人那里学来的。）*

## Sources

- [Scott Logic — Rapid development with Devin](https://blog.scottlogic.com/2025/10/20/rapid-development-with-devin.html)
- [Lenny's Newsletter — Scott Wu on Cognition's internal Devin usage](https://www.lennysnewsletter.com/p/how-devin-replaces-your-junior-engineers)
- [Every — Coding with Devin](https://every.to/chain-of-thought/coding-with-devin-my-new-ai-programming-agent)
- [dev>notes — Devin vs Claude Code](https://web.archive.org/web/20260718112612/https://mohitkhare.me/blog/devin-vs-claude-code/)
- [Faros — Devin for live troubleshooting](https://www.faros.ai/blog/how-to-use-devin-ai-troubleshooting)
- [Medium — Copilot, Cursor or Devin weekend](https://medium.com/@sambhavgaur_70582/copilot-cursor-or-devin-my-hands-on-weekend-with-ai-that-codes-and-deploys-acc708e802b3)
- [Bootcamp — Day 7 with Devin (Tailwind/DaisyUI migration)](https://medium.com/design-bootcamp/day-7-of-30-getting-to-know-devon-ai-and-working-with-him-743c351cd0c4)
- [architect to CTO — The only coding agent worth paying for](https://architecttocto.substack.com/p/the-only-coding-agent-worth-paying)
- [expectedwrong — Devin, appraised](https://expectedwrong.com/devin-appraised) · [dev.to — 10 real tasks, 3 completed](https://dev.to/alanwest/i-gave-devin-10-real-tasks-it-completed-3-3063) · [amillionmonkeys](https://www.amillionmonkeys.co.uk/blog/ai-coding-tools-small-studios)
- [Signadot — Testing Devin's changes end to end](https://dev.to/signadot/test-devins-changes-end-to-end-with-signadot-a0)
- [hubble — Dependabot PRs investigated by Devin first](https://zenn.dev/hubble/articles/88429bd24db476) · [hubble — Datadog CCM × Devin weekly cost ops](https://zenn.dev/hubble/articles/091e29a0c86ec3)（日语）
- [SMARTCAMP — Trivy scan → Devin remediation pipeline](https://zenn.dev/smartcamp/articles/97ac804043530e)（日语）
- [canly — Classifying ~700 support inquiries with Devin](https://zenn.dev/canly/articles/9c19bb123e208c)（日语）
- [smasato — Maximizing Devin: tips for success](https://zenn.dev/smasato/articles/6aebb0da2f56eb)（日语/英译版）
- [掘金 — Devin vs Cursor：个人开发者和中小项目怎么选](https://juejin.cn/post/7689030315844026414)（中文）
