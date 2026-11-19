# 指南 17 — Devin Desktop

**目标：** 面向 agent 的原生编辑器——Devin 的所有面集中在一个窗口：云会话、本地会话（Devin Local）、Bots，外加一个完整的 IDE。
**级别：** 入门
**来源：** [Desktop changelog](https://docs.devin.ai/desktop/changelog) · [CLI changelog](https://docs.devin.ai/cli/changelog/stable)

## 它是什么

Devin Desktop 是基于 Windsurf 的编辑器，Devin 的各个面并排住在里面。先分清三样东西：

| 面 | 在哪跑 | 适合干什么 |
| --- | --- | --- |
| 云会话 | Devin 的机器上、你的组织里 | 无人值守任务、并行工作、等待 review 的 PR |
| Devin Local | 你机器上的后台进程 | 在你已检出的 repo 里动手改 |
| Bot | 常驻 agent（见指南 1–5） | 一个要负责的产出——v3.14 起进了 Desktop |

## Agent Command Center

Command Center 是会话中枢，不是编辑器：

- **标签页**（v3.13.4）：一个窗口里开多个会话和页面，每个标签有自己的前进/后退历史——当成你舰队的浏览器用。
- **会话头部 "..." 菜单**：该会话的 MCP servers——按会话开关某一个、或重新授权。
- **Devin Review**：PR 走查（diff、bug、测试录像）以页面形式开在同一个窗口。

## Devin Local —— daemon 变化

自 v3.13.4（Desktop）/ v3000.13.4（CLI）起，本地会话跑在**后台进程**里，而不是开在启动它的窗口里：

- 关掉或重开 Devin Desktop——或 CLI——**不会**停掉会话。
- 同一会话可以**同时挂在多个客户端**：Desktop 窗口和终端一起连着，各自都能看到输出和提问。
- `devin daemon` 启动/停止/查看这个进程；最后一个会话和客户端都离开后约 10 分钟它自己退出。
- `--process-model` 在 `daemon` 和 `in-process` 之间选；`config.json` 里的 `process_model` 或 `/config` 设默认值。
- `devin ls`、`devin -r`、`/resume` 打开**会话监视器**——按最近更新排序的会话列表，带状态、目录和消息数。

实际后果：本地工作变成持久的了。开个长任务，合上电脑，从另一个客户端接回来——会话一直在跑。

## IDE 模式

- 内嵌 IDE 用 **Cmd/Ctrl+S** 手动保存（不再自动保存）；未保存标签带个点。
- 在 Devin Local 的浏览器预览里，**点选一个页面元素或 console 输出会直接放进 composer**——指着 bug 而不是描述 bug。
- Files 标签能预览 PDF、把 CSV/TSV 渲染成表格、播放媒体。

## 两个值得抄的工作流

**1. 本地 → 云端 → 本地。** 在 Devin Local 干活，碰到瓶颈（需要组织工具、更大并行、比笔记本开着的时间还长），`/handoff` 到云端，review 完把 PR 拉回来。daemon 让两段都能断点续接。

**2. 一个窗口，所有面。** Command Center 看舰队全局，Local 处理手头这个 repo，Bot 负责你不想盯的产出——Desktop 是唯一让三者共享一个窗口的地方。

## 验证它

- [ ] 一个 Devin Local 会话在关掉再打开 Desktop 后仍在跑
- [ ] 同一个本地会话同时从 Desktop 和 `devin` CLI 连上
- [ ] `devin ls` 打开了会话监视器并接进一个正在跑的会话
- [ ] 从 Desktop 聊天里建的 Bot 在同一个聊天里回话

## 坑

- **"Not authorized to use the CLI"** —— 有 Desktop 权限但没 CLI 权限的账号在 Devin Local 登录会撞这个错（v3.14.30825 已修；见到就升级）。
- **标签页是窗口级状态。** 会话页面里的操作只作用于自己的标签——但*会话*是共享的，第二个客户端连上看到的是同一个活会话，不是副本。
- **受管机器：** 企业管理员通过设备策略控制 Desktop 设置（如语言服务器的 `DetectProxy`）——网络出问题先问 IT，别自己瞎调。

## 自测

1. v3.13.4 里本地会话变了什么？（改跑在后台进程里——关应用不再停会话，多个客户端可同时挂同一会话。）
2. 什么时候选 Devin Local 而不是云会话？（想在你的检出 repo 里带本地上下文亲手改时；要规模或组织集成时交给云端。）
3. 会话头部 "..." 菜单里有什么？（该会话的 MCP servers——按会话开关或重新授权。）

## 来源

- [Devin Desktop changelog](https://docs.devin.ai/desktop/changelog) —— v3.13.4（标签页、后台本地会话）、v3.14（Bots 进 Desktop）
- [Devin CLI changelog](https://docs.devin.ai/cli/changelog/stable) —— v3000.13.4：`devin daemon`、`--process-model`、会话监视器
- 相关：[指南 12 — Devin CLI 与可扩展性](devin-cli.md) · [指南 1 — 你的第一个 Bot](bots-101-first-bot.md)
