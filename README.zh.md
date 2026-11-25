<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/cover-dark.svg">
  <img src="assets/cover-light.svg" alt="Build with Devin" width="100%">
</picture>

<br/>

[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![License: CC0-1.0](https://img.shields.io/badge/License-CC0_1.0-lightgrey.svg)](LICENSE)

<sub>维护者 [@darega0mae](https://x.com/darega0mae) · 姊妹登记库：[built-with-devin](https://github.com/Till3005/built-with-devin) · [改进指南](CONTRIBUTING.md) · [站点阅读（目录/筛选/四语）](https://till3005.github.io/built-with-devin/guides/zh/index.html)</sub>

<sub>**20** 篇指南 · **4** 个阶段 · 每个模式都逆向自实名、有据可查的部署</sub>

<sub>[English](README.md) · 简体中文 · [日本語](README.ja.md) · [Português](README.pt.md)</sub>

</div>

> *非官方社区项目 —— 与 Cognition AI 无关联、未获其背书或赞助。"Devin" 是 Cognition AI 的商标。品牌素材依照 [devin.ai/brand](https://devin.ai/brand) 官方品牌包使用。官方文档：[docs.devin.ai](https://docs.devin.ai)。*

**Build with Devin** 是一套教程集：每篇指南拿一个*有据可查的真实* Devin 部署 —— 从 Cognition 自己的首发舰队到公开客户案例 —— 逆向成你可以在自己账号上复现的步骤。没有假想 demo；这里的每个模式都有实名部署和公开数字背书。

**搭配 [built-with-devin](https://github.com/Till3005/built-with-devin)** —— 收录社区与 Cognition 全部交付物的姊妹登记库。登记库回答*有什么*；本库回答*怎么造*。

```mermaid
flowchart LR
    subgraph S0["零阶 · 起步"]
      G18["18 · 跟 Devin 说话"] --> G17["17 · Devin Desktop"]
      G18 --> G12["12 · Devin CLI"]
      G18 --> G19["19 · 会话全环"]
      G19 --> G1
      G17 --> G1["1 · 第一个 Bot"]
      G12 --> G1
      G1 --> G13["13 · 官方食谱"]
    end
    subgraph S1["一阶 · 运转"]
      GP["ref · outcome prompts"] --> G6["6 · Automations"]
      G6 --> G9["9 · Playbooks 与知识"]
      G9 --> G16["16 · Skills 与 plugins"]
      G10["10 · Devin Apps"]
      G8["8 · 设计工作"]
    end
    subgraph S2["二阶 · 规模化"]
      G2["2 · 产品负责人"] --> G4["4 · 多 Bot 组织"]
      G3["3 · 定时哨兵"] --> G4
      G4 --> G5["5 · 基准 swarm"]
      G11["11 · 大规模迁移"] --> G15["15 · 活评测集"]
      G7["7 · 企业级铺开"]
    end
    subgraph S3["三阶 · 田野"]
      G14["14 · 实战报告"]
    end
    S0 --> S1 --> S2
```

## 指南

### 零阶 · 起步

*从零到一个能交付的任务。所有人都从这开始——两个接入面、一套提示词基本法、第一次"所有权"、一本官方食谱。*

| # | 指南 | 你将做出 | 基于 | 难度 |
| --- | --- | --- | --- | --- |
| 18 | [跟 Devin 说话：提示词基本法](guides/zh/talking-to-devin.md) | Devin 不可能误读的指令——说怎么做、可检查的成功、80% 规则 | [Coding Agents 101](https://devin.ai/agents101) + [官方提示词文档](https://docs.devin.ai/essential-guidelines/instructing-devin-effectively) | 从这里开始 |
| 19 | [会话全环](guides/zh/the-session-loop.md) | 理解 → 委托 → 审查 → 复盘：DeepWiki、Ask Devin、Devin Review、Session Insights + ACU 计费 | [Devin University](https://learndevin.com) + 官方产品文档 | 从这里开始 |
| 17 | [Devin Desktop](guides/zh/devin-desktop.md) | 面向 agent 的原生编辑器：Command Center、持久本地会话、Bots——一个窗口 | [Desktop changelog](https://docs.devin.ai/desktop/changelog) | 从这里开始 |
| 12 | [Devin CLI 与扩展性](guides/zh/devin-cli.md) | 本地 agent：daemon 会话、云端交接、skills、hooks | [CLI 文档](https://docs.devin.ai/cli/index.md) | 进阶 |
| 1 | [你的第一个 Bot](guides/zh/bots-101-first-bot.md) | 一个对结果负责的 Bot——chat、sessions、Needs-you、记忆、接入面 | [官方文档](https://docs.devin.ai/work-with-devin/bots) + 发布帖 | 从这里开始 |
| 13 | [官方用例食谱](guides/zh/official-cookbook.md) | 40+ 个有据可查的配方——卫生循环、事故响应、质量 | [用例 gallery](https://docs.devin.ai/use-cases/gallery/index.md) | 从这里开始 |

### 一阶 · 运转

*把日常循环交出去：懂规范的 Bot、事件触发的会话、一次编码永久继承的约定、在线服务的工具。*

| # | 指南 | 你将做出 | 基于 | 难度 |
| --- | --- | --- | --- | --- |
| — | [Bot outcome prompts 逐句拆解](guides/zh/bot-outcome-prompts.md) | 授予所有权而非派任务的 outcome prompt——真实案例反向拆解 | Android Bot 原话 prompt + 全部 16 个官方模板 | 参考 |
| 6 | [事件驱动 automations](guides/zh/automations-101-event-driven.md) | 由 Slack、GitHub、Linear、cron、webhook 触发的会话 | [Automations 文档](https://docs.devin.ai/product-guides/automations) | 从这里开始 |
| 9 | [Playbooks 与知识](guides/zh/playbooks-and-knowledge.md) | 把团队规范编码下来，让每个 session 继承 | 每个企业级结果背后的那一层 | 进阶 |
| 16 | [Skills 与 plugins](guides/zh/skills-and-plugins.md) | playbook 之后的那一层——SKILL.md 契约、发现机制、plugin 打包 | [Skills 文档](https://docs.devin.ai/product-guides/skills) | 中级 |
| 10 | [Devin Apps](guides/zh/devin-apps.md) | 从 Devin 的机器上提供的 live 内部工具和看板 | [Devin Apps 发布](https://devin.ai/blog/devin-apps) | 从这里开始 |
| 8 | [设计与视觉工作](guides/zh/design-with-devin.md) | 通过 Devin 对话给生产 UI 做美术指导 | Spraycash 落地页实录 | 进阶 |

### 二阶 · 规模化

*从一个 Bot 到一个组织：四种实名部署原型，然后是重机器——迁移、评测、企业落地。*

| # | 指南 | 你将做出 | 基于 | 难度 |
| --- | --- | --- | --- | --- |
| 2 | [产品负责人 Bot](guides/zh/bots-201-product-owner.md) | 一个产品管理整个应用表面的 Bot | Android Bot —— 44 天，1,134 个 PR | 进阶 |
| 3 | [定时哨兵 Bot](guides/zh/bots-202-scheduled-sentinel.md) | 一个按 cron 盯检查项、自己修回归的 Bot | Layout Bot —— 3 周 159 个 PR | 进阶 |
| 4 | [多 Bot 组织](guides/zh/bots-203-multi-bot-org.md) | 带 grants 和汇总上报的 Bot 层级 | SuperJennyStack —— ~20 个 Bot，每周 1,900 PR | 高级 |
| 5 | [基准锚定 swarm](guides/zh/bots-204-reference-grounded-swarm.md) | 一个写出可验证系统的受指挥 swarm | Harvey "Phil" 模式（具体原帖待补，规模数字暂不引用） | 高级 |
| 11 | [大规模迁移](guides/zh/migrations-at-scale.md) | 拆成数百个可验证小 PR 的迁移 | 官方 playbook + Nubank | 进阶 |
| 15 | [生产 trace 驱动的活评测集](guides/zh/living-evals.md) | 自我增长的评测集：Devin 在你系统的完整副本里回放生产失败 | Rox —— 覆盖率 72%（手写 43–57%） | 高级 |
| 7 | [企业级铺开模式](guides/zh/enterprise-playbook.md) | 最大客户结果背后的六种部署形态 | Nubank、Gumroad、EBANX、Modal、Airbyte…… | 进阶 |

### 三阶 · 田野

*团队们真实学到的东西——赢的、败的、他们公布的数字。*

| # | 指南 | 你将做出 | 基于 | 难度 |
| --- | --- | --- | --- | --- |
| 14 | [社区实战报告](guides/zh/community-field-reports.md) | 真实团队的经验——赢的、败的、带数字的实名部署 | 15+ 篇已发布实操记述 | 从这里开始 |

<p align="right"><a href="#readme">back to top</a></p>

---

## 从哪开始

第一次来按阶段顺序读；之后随便跳。

- **个人开发者，第一次接触：** 18 → 17（住终端里的换 12）→ 1 → 13。一个周末的量。
- **想快速见效：** 指南 13 的定时卫生配方是最便宜的第一个部署。
- **团队 lead：** 在起步线之上加 6、9、16——循环、规范、复用层。
- **管一个组织：** 整个二阶，然后 7——再看 14 里其他团队真实踩过的坑。
- 每篇指南以 **Sources** 收尾——既有官方文档，也有模式蒸馏自的社区/田野记述——以及 **Verify it**，告诉你复现是否成功的检查项。

<p align="right"><a href="#readme">back to top</a></p>

---

## 约定

- 每篇指南自足：目标 → 前置条件 → 逐步搭建 → 运营结果 → 坑。
- 出处公开过的 prompt 逐字引用；其余为重写并注明。
- 指南里的数字来自所引用的部署，不是我们的估计。

## 贡献

找到错误，或有更好的复现路径？见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 许可证

[CC0-1.0](LICENSE) —— 贡献给公共领域。
