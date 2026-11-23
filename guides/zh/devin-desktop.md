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
- **Devin Review**：PR 走查（diff、bug、测试录像）以页面形式开在同一个窗口——即[指南 19](the-session-loop.md) 环路里的审查一环。

## Devin Local —— daemon 变化

自 v3.13.4（Desktop）/ v3000.13.4（CLI）起，本地会话跑在**后台进程**里，而不是开在启动它的窗口里：

- 关掉或重开 Devin Desktop——或 CLI——**不会**停掉会话。
- 同一会话**对所有客户端可见**（`devin ls`、Desktop 列表），但挂接是独占的：第二个客户端会看到锁定横幅，Force open 会踢掉第一个客户端、把会话抢过来。
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

## 实录演示 —— 录于 Devin Desktop v3.14.30825

真跑了一遍，不是拼出来的图：macOS、Pro 方案。一次 Devin Local 会话在一个丢弃用的 `demo-repo` 里用 SWE-2 High 改代码，Desktop 退出后它还在跑，还在 CLI 和 Desktop 之间换手。

**视频（91 秒，无声）：** Command Center → 标签页 → Bots → Devin Local → daemon 实证 → IDE 视图。

[![Devin Local 会话在 SWE-2 High 上收尾——demo-repo 里改了 2 个文件](https://till3005.github.io/built-with-devin/assets/guides/devin-desktop/walkthrough-poster.webp)](https://till3005.github.io/built-with-devin/assets/guides/devin-desktop/walkthrough.mp4)

![1. Command Center 首页——最近会话、Your Bots、输入框上的 Cloud/Local 开关](https://till3005.github.io/built-with-devin/assets/guides/devin-desktop/step1-command-center.webp)
*1. Command Center 首页——最近会话、Your Bots，以及输入框上的 Cloud/Local 开关*

![2. 输入框的模型选择器——能力档位加模型预览](https://till3005.github.io/built-with-devin/assets/guides/devin-desktop/step2-model-picker.webp)
*2. 输入框的模型选择器：能力档位（Fusion → Free）和预览模型（含 SWE-2 Lightning/Flash）*

![3. 云端会话以标签页打开；右栏是 Computer、Files、Changes、Terminal](https://till3005.github.io/built-with-devin/assets/guides/devin-desktop/step3-session-tab.webp)
*3. 云端会话以标签页打开——右栏是 Computer、Files、Changes、Terminal*

![4. 会话顶栏 "..." 菜单——用量、归档、网络配置、从会话建 automation/skill](https://till3005.github.io/built-with-devin/assets/guides/devin-desktop/step4-session-menu.webp)
*4. 会话顶栏 "..." 菜单；会话配有 MCP 服务器时它会出现在这里（这个没有）*

![5. Desktop 里的 Bots——Bots 页面能打开，但发消息要 Max 或 Teams](https://till3005.github.io/built-with-devin/assets/guides/devin-desktop/step5-bots-gate.webp)
*5. Desktop 里的 Bots：页面能开，但这个方案给 Bot 发消息要 Max 或 Teams（如实记录）*

![6. Devin Local 执行命令前要批准——逐条 Allow 或 Reject](https://till3005.github.io/built-with-devin/assets/guides/devin-desktop/step6-local-approval.webp)
*6. Devin Local 执行命令前要批准——逐条 Allow 或 Reject*

![7. Local 会话在 SWE-2 High 上跑完——改了 2 个文件，带快速 diff 预览](https://till3005.github.io/built-with-devin/assets/guides/devin-desktop/step7-local-done.webp)
*7. Local 会话在 SWE-2 High 上跑完——改了 2 个文件，带快速 diff 预览*

![8. daemon 实证：退出 Desktop，`devin ls` 仍列着会话；resume 接上，完整记录都在](https://till3005.github.io/built-with-devin/assets/guides/devin-desktop/step8-cli-attached.webp)
*8. daemon 实证：退出 Desktop，`devin ls` 仍列着这个会话——resume 接上，完整记录都在*

![9. 第二个客户端看到锁定横幅；Force open 抢过会话，第一个客户端断开](https://till3005.github.io/built-with-devin/assets/guides/devin-desktop/step9-force-open.webp)
*9. 双客户端不能共驾：第二个看到锁定横幅，Force open 抢过会话，第一个断开*

![10. IDE 视图：Source Control 列出会话的改动；未保存标签页有圆点，Cmd+S 保存](https://till3005.github.io/built-with-devin/assets/guides/devin-desktop/step10-ide-view.webp)
*10. IDE 视图：同一会话外裹着一个真编辑器——Source Control 列出它的改动；未保存标签页显示圆点，Cmd+S 保存*

## 验证它

- [ ] 一个 Devin Local 会话在关掉再打开 Desktop 后仍在跑
- [ ] `devin ls` 看到了 Desktop 开的会话，`devin -r` 带完整记录把它接了回来
- [ ] `devin ls` 打开了会话监视器并接进一个正在跑的会话
- [ ] 从 Desktop 聊天里建的 Bot 在同一个聊天里回话

## 坑

- **"Not authorized to use the CLI"** —— 有 Desktop 权限但没 CLI 权限的账号在 Devin Local 登录会撞这个错（v3.14.30825 已修；见到就升级）。
- **标签页是窗口级状态。** 会话页面里的操作只作用于自己的标签——但*会话*是共享的，第二个客户端连上看到的是同一个活会话，不是副本。
- **受管机器：** 企业管理员通过设备策略控制 Desktop 设置（如语言服务器的 `DetectProxy`）——网络出问题先问 IT，别自己瞎调。
- **"Archive" 与 "Mark done" 之别。** Desktop 的 "..." 菜单（第 4 帧）仍写 *Archive*，但 webapp 已改名 *Mark done*（11 月 16 日）：会话进你的 Done 文件夹但继续运行，对其他订阅者仍可见——侧栏现在列出你订阅的会话，别把别人还依赖的会话「清理」掉。相关新增：**Phonebook** 把每位成员在 Devin/Slack/Teams/git/Jira/Linear 上的身份关联起来。

## 自测

1. v3.13.4 里本地会话变了什么？（改跑在后台进程里——关应用不再停会话，任何客户端都能看到并接管同一会话。）
2. 什么时候选 Devin Local 而不是云会话？（想在你的检出 repo 里带本地上下文亲手改时；要规模或组织集成时交给云端。）
3. 会话头部 "..." 菜单里有什么？（该会话的 MCP servers——按会话开关或重新授权。）

## 来源

- [Devin Desktop changelog](https://docs.devin.ai/desktop/changelog) —— v3.13.4（标签页、后台本地会话）、v3.14（Bots 进 Desktop、`DetectProxy` 策略）
- [Devin release notes](https://docs.devin.ai/release-notes/2026) —— 11 月 16 日：*Mark done* 取代 Archive、订阅侧栏、Phonebook
- [Devin CLI changelog](https://docs.devin.ai/cli/changelog/stable) —— v3000.13.4：`devin daemon`、`--process-model`、会话监视器
- 相关：[指南 12 — Devin CLI 与可扩展性](devin-cli.md) · [指南 1 — 你的第一个 Bot](bots-101-first-bot.md)
