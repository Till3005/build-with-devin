# 指南 16 — Skills 与 plugins：playbook 之后的封装层

**目标：** 把组织里可重复的流程编码成 `SKILL.md` 文件，让每个会话和 Bot 都按它执行——并用 plugins 跨仓库打包分享。
**级别：** 中级 · 取代 playbook 的那一层
**来源：** [docs.devin.ai/product-guides/skills](https://docs.devin.ai/product-guides/skills) · [release notes](https://docs.devin.ai/release-notes/overview) · 配套 [指南 9](playbooks-and-knowledge.md)

## 为什么 skills 是现在最重要的那一层

Playbook 正在迁移到 Skills：账号分批迁移，2026-10-24 起的新账号只有 Skills——每个 playbook 会变成一个相同 org/enterprise 作用域的 skill。Skills 还遵循开放的 **Agent Skills** 标准，同样的文件可以在其他编码 agent 上使用。你写 playbook 的经验全部迁移得过来——变的是文件格式和发现机制。

| 产物 | 存放位置 | 最适合 |
| --- | --- | --- |
| Knowledge | Customize 页 / 仓库笔记 | 常驻上下文——Devin 无从得知的事实 |
| Bot instructions | Bot 本体 | 一个"员工"的岗位守则 |
| Skill | 仓库里的 `SKILL.md`，或 plugin | 一个具名、可调用的流程 |
| Rule | Plugin | 常驻约束（"never force-push"） |
| Hook | Plugin | 围绕工具调用的确定性执行 |

## 第 1 步 — skills 存放在哪

两个自动发现的来源：

1. **仓库** —— 提交 `SKILL.md` 文件；Devin 扫描每个已连接仓库的全部十个厂商路径：`.agents/skills/`（推荐）、`.devin/skills/`、`.github/skills/`、`.claude/skills/`、`.cognition/skills/`、`.windsurf/skills/`、`.cursor/skills/`、`.codex/skills/`、`.codeium/skills/`、`.kiro/skills/`。仓库 skill 跟随分支版本——会话中途 clone 的仓库在 clone 完成时就会被扫描。
2. **Plugins** —— 一个 plugin 打包 skills + rules + MCP servers + hooks，可装在 personal、organization 或 enterprise 作用域；其 skills 在任何仓库 clone 之前就进入上下文。

## 第 2 步 — SKILL.md 契约

```markdown
---
name: test-before-pr
description: Run the dev server and verify pages before any frontend PR.
argument-hint: <environment>
triggers: ["user"]
allowed-tools: read, grep, glob
permissions:
  allow: ["Exec(npm run *)"]
---

## Setup
1. `docker-compose up -d postgres` && `npm run dev`
## Verify
1. Open each page touched by the diff
2. Screenshot at 1280px and 375px
```

会改变行为的 frontmatter 字段：

- **`description`** —— 会话启动时 Devin 唯一看到的内容；它决定自动调用。写成触发条件（"verify pages before any frontend PR"），而不是摘要。
- **`triggers: ["user"]`** —— 关闭自动调用；一切破坏性操作（部署、迁移）都应该用它。
- **`argument-hint`** + `$ARGUMENTS`/`$1` —— 参数化：`@skills:deploy staging`。
- **`allowed-tools` / `permissions`** —— skill 激活期间预批准或设卡工具。

## 第 3 步 — 三种调用路径

- **自动：** Devin 用任务匹配 `description`，命中后把 skill 正文载入上下文，持续到会话结束。
- **显式：** 在会话或 Bot 消息里写 `@skills:<name> [args]`——跨团队共享流程的可靠方式。
- **建议产生：** Devin 学到东西后（比如怎么起你的技术栈），会在会话时间线里提议一个 `SKILL.md`，附 **Create PR** 按钮——接受它。skill 库就是这样不靠专门写作而长出来的。

## 第 4 步 — 养大这个库

- 用两个并行会话打一个新 skill，缺口几分钟就暴露。
- 会话中纠正了 Devin 什么，就把这条纠正写进 skill——下一个会话起步就更聪明。
- 在单个仓库验证过的 skill 提升为 org plugin，让每个仓库不复制就能用。

## 实录演示 —— 真调用一个 repo skill，录于 Devin CLI v3000.14（swe-2-flash-medium）

第 3 步的「显式调用」路径端到端：在演示仓库提交 `.devin/skills/coverage-check/SKILL.md`，然后在新会话里调用。发现机制和文档完全一致——输入 `/` 就按名字列出了这个 skill，`description` 就是补全栏里那行说明。

**视频（60 秒，无声）：** SKILL.md → 斜杠补全 → `Invoked skill coverage-check` → 审批 → 报告。

[![skill 产出的报告——app.py 和 orders.py 的逐函数覆盖表](https://till3005.github.io/built-with-devin/assets/guides/skills-and-plugins/walkthrough-poster.webp)](https://till3005.github.io/built-with-devin/assets/guides/skills-and-plugins/walkthrough.mp4)

![1. 磁盘上的 skill——frontmatter 的 name/description，下面是一编号的流程](https://till3005.github.io/built-with-devin/assets/guides/skills-and-plugins/step1-skill-file.webp)
*1. 磁盘上的 skill——`.devin/skills/coverage-check/SKILL.md`：frontmatter `name`/`description` + 编号流程*

![2. 输入 `/` 列出 skill——名字 + description 就是补全条目](https://till3005.github.io/built-with-devin/assets/guides/skills-and-plugins/step2-slash-autocomplete.webp)
*2. 输入 `/` 列出 skill——发现机制加载的正是 name + `description`*

![3. `Invoked skill coverage-check`——第一条命令也要等 Allow](https://till3005.github.io/built-with-devin/assets/guides/skills-and-plugins/step3-invoked.webp)
*3. `Invoked skill coverage-check`——skill 的第一条命令仍需 Allow*

![4. 流程按原文执行——跑 unittest，再逐个读源文件和测试文件](https://till3005.github.io/built-with-devin/assets/guides/skills-and-plugins/step4-coverage-report.webp)
*4. 流程按原文执行——`python3 -m unittest -v`，再读 app.py、orders.py 和两个测试文件*

![5. 结果：全覆盖——逐函数表列出每个分支；未改文件、零提交](https://till3005.github.io/built-with-devin/assets/guides/skills-and-plugins/step5-full-coverage.webp)
*5. 结果：全覆盖——每个分支都有交代，正是 SKILL.md 要求的报告*

## 验证清单

- [ ] 新会话能按名字列出你的 skill（启动时载入 name + description）
- [ ] `@skills:<name>` 逐字执行该流程，参数正常替换
- [ ] `triggers:["user"]` 的 skill 绝不自动触发
- [ ] plugin 装的 skill 在仓库 clone 完成前就可用

## 常见坑

- **过度规约。** 具体命令/flag/字符串才是重点；僵硬的长篇描述不是。把每个决策都写死的 skill 会剥夺 Devin 中途应变的能力。
- **只写正文不写 description。** 自动调用认的是 description；正文再好、description 含糊就永远不会被触发。
- **让破坏性 skill 自动触发。** 部署和迁移应该关在 `triggers:["user"]` 或显式的 `permissions.ask` 后面。
- **在 skill 里放 secret。** skill 会被作用域内每个会话读到——凭证放 secrets store，用 `$VAR` 引用。

## 理解度检查

1. 为什么 `description` 比 skill 正文更重要？*（它是会话启动时唯一载入的文本——驱动自动调用；正文只在 skill 被选中后才载入。）*
2. 什么时候流程应该做成 plugin skill 而不是仓库 skill？*（当作用域内每个仓库/会话都需要它时——plugin 在 clone 前就加载，且不会随分支漂移。）*
3. 怎么让含破坏性步骤的 skill 安全？*（`triggers:["user"]` 只允许显式调用，再给危险工具的 matcher 加 `permissions.ask`。）*

## 来源

- [Devin Skills 文档](https://docs.devin.ai/product-guides/skills) — 文件格式、发现路径、frontmatter
- [Release notes](https://docs.devin.ai/release-notes/overview) — playbooks→Skills 迁移、Customize 页
- 相关：[指南 9 — Playbooks & knowledge](playbooks-and-knowledge.md)（skills 旁边的上下文层）
