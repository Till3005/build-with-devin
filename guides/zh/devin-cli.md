# 指南 12 — Devin CLI 与可扩展性

**目标：** 终端里的本地 Devin——在你机器上跑 agent、把活交给 Devin Cloud，并用 skills、rules、plugins、hooks、subagents 扩展它。
**级别：** 中级
**来源：** [Devin CLI docs](https://docs.devin.ai/cli/index.md) — [introducing](https://docs.devin.ai/cli/introducing-devin-cli.md)、[essential commands](https://docs.devin.ai/cli/essential-commands.md)、[extensibility](https://docs.devin.ai/cli/extensibility/index.md)

## 它是什么

Devin CLI 是住在你终端里、连着 Devin Cloud 的编码 agent。两种工作模式，威力在两者之间移动：

- **本地** —— 直接编辑你机器上已检出的 repo
- **云端** —— `devin --cloud` 创建/操控/恢复云会话；`/handoff` 把本地任务交给云端 Devin，`/open` 把云会话的 PR 拉回你机器

```text
local repo ──/handoff──► Devin Cloud session ──PR──► /open ──► local repo
     ▲                        │
     └──── devin ssh / forward (inspect its VM) ────┘
```

## 关键组件

| 面 | 作用 |
| --- | --- |
| `devin ssh` / `devin forward` | SSH 进云会话的 VM、转发端口、`scp` 文件 |
| Subagents | 委派给独立 agent（前台/后台），各自带配置和权限 |
| Models | 自适应路由按任务挑模型；Fusion 是前沿主力 + 廉价副手 |
| ACP | 通过 Agent Client Protocol 跑在 JetBrains、Zed、Xcode 里 |
| Daemon | v3000.13.4 起本地会话跑在后台进程——关掉应用不停会话，任何客户端可接回（`devin daemon`、`devin ls` 会话监视器） |

## 可扩展性栈

团队在这里把 CLI 变成*自己的*——和第 9 篇同样的分层，应用在本地：

| 层 | 文件/机制 | 用途 |
| --- | --- | --- |
| Rules | `AGENTS.md` / rules 文件 | 每个会话都会读的常驻指令 |
| Skills | `SKILL.md` | 可复用流程——斜杠调用或 agent 自选，可带独立权限/`allowed-tools` |
| Plugins | plugin manifest | 打包 skills + rules + hooks + MCP servers；经**团队 marketplace**分发 |
| Hooks | 生命周期 hooks | 在 `PreToolUse`、`PostToolUse`、`SessionStart`、`SessionEnd`… 上跑 shell/LLM 逻辑——拦截或改写工具调用、注入上下文 |
| MCP | MCP 配置 | 外部工具服务器（stdio / HTTP / SSE） |

**导入路径：** `read_config_from` 可从 Cursor、Windsurf、Claude Code、Copilot、Codex、Kiro、OpenCode、Zed 导入配置——迁移是一个开关，不是重写。

## 三个值得抄的工作流

**1. 本地 → 云端扇出。** 本地起任务、触到上限、`/handoff` 给一个在自己机器上继续跑的云会话——PR 用 `/open` 拉回来。

**2. Skills 当记忆。** 把任何重复流程（第 11 篇的迁移 skill、hotfix runbook、发版切割）写成 `SKILL.md`——CLI docs 建议把*成功会话的记录*回灌进 skill 来补缺。plugins 把它们打包分发给全团队。

**3. Hooks 当护栏。** 一个 `PreToolUse` hook 拦截 `rm -rf` 模式或对迁移强制评审——执行发生在 hook 里，而不是指望模型自觉。

## Verify it

- [ ] `devin` 能跑本地会话；`devin --cloud` 能列出/创建云会话
- [ ] 一个 `/handoff` 的任务在云端完成、PR 经 `/open` 拉回来了
- [ ] 斜杠命令调用 `SKILL.md` 跑通了你的流程
- [ ] （企业版）团队 marketplace 能把你的 plugin 发给另一个成员

## 坑

- **并行活用云端。** CLI 是终端里的单个 agent——并行切片请用云会话或 Bot；CLI 是*亲手干*的那一面。
- **Rules 蔓延。** `AGENTS.md` + 项目 rules + 全局 rules 按优先级相互作用——每条规则只放一层，否则会打架。

## 自检

1. 什么时候用 `/handoff` 上云而不是本地跑完？*（工作需要云端并行、组织工具，或跑得比你笔记本开着的时间还长。）*
2. skill、rule、plugin 三者的区别？*（skill 是任务规程，rule 是常驻上下文，plugin 是打包两者的容器外加 hooks。）*
3. 为什么 hooks + subagents 对团队采用重要？*（hooks 在每个 CLI 会话强制执行组织策略；subagents 让一个操作员开一队 agent——两个方向同时扩。）*

## Sources

- [Devin CLI docs](https://docs.devin.ai/cli/index.md) — quickstart、命令、云集成、可扩展性、ACP、模型
- 相关：[第 9 篇 — Playbooks 与知识层](playbooks-and-knowledge.md)（同一套约定层，组织级）
