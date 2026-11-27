# 指南 10 — Devin Apps：从聊天里交付一个活工具

**目标：** 描述一个内部工具、仪表盘或 staging 副本——Devin 把它建出来并托管在一个稳定 URL 上，团队成员登录即可打开。
**级别：** 入门（平台篇）· **用时：** ~10 分钟出第一个 App
**来源：** [Introducing Devin Apps](https://devin.ai/blog/devin-apps)（2026-11-13）

## 它是什么

Devin App 是一个直接托管在 Devin 云机器上的私密 web 应用。你描述工具，Devin 建出来，团队从链接打开——没有部署管线、没有运维。因为它跑在 Devin 的机器上，所以能直连你的 MCP、集成、代码库和它自己的数据库（同机的 SQLite/Postgres），还能回调 Devin API 自身。

## 建一个

1. 侧栏 → **Apps** → 描述这个 App 要做什么（或选模板：指标仪表盘、项目状态、评审队列）→ **Build with Devin**
2. Devin 会在会话里问澄清问题、构建并上线——Apps 页显示其 URL，v1 上线前状态为 `Building`
3. **Share** — 复制链接；范围可限定到指定人员、你的组织或整个企业。App 永不公开；打开需要 Devin 登录

也可以在任何一个产出了浏览器预览的会话里说 "publish this as an App"。

## 更新循环

- App 页面上 **Edit in session** → 描述改动 → Devin 在同一个 URL 构建新版本。每次更新都是一次带版本的部署；新版本启动失败时旧版本继续服务。
- 自 11 月 25 日起，Apps 会出现在网页版左栏；Browser 标签页的 element picker 让你直接指向视觉元素，而不是用文字描述它。
- **Automation 保鲜：** 接一个 automation（第 6 篇）按定时或分支变更重新部署——"每天早上拉新数据的仪表盘"是最典型的用法。

## 运行机制（要点）

- **休眠：** App 构建在内存快照上——机器闲置时休眠、打开时唤醒（首次加载可能有几秒）。计费按唤醒时间。
- **技术栈：** 任何能在端口上提供 HTTP 的东西；数据库同机部署。
- **规模边界：** 一台机器——非常适合内部工具和仪表盘，**不适合**高并发生产服务。

## 三种已验证用法

| 用途 | 例子 |
| --- | --- |
| 内部工具 | 管理面板、申请表单、审批队列——共享表格杀手 |
| 仪表盘 | 从自家数据源拉数的指标/客服/销售看板，定时刷新 |
| Beta/staging 副本 | 你的真实技术栈（前端+后端+DB+worker）跑在 Devin 机器上——队友从链接打开一个 staging 副本 |

## Verify it

- [ ] 机器休眠后 App 仍能在稳定 URL 加载（预期几秒冷启动）
- [ ] 一次 edit-in-session 改动在同一 URL 产出了新版本
- [ ] 分享范围正确：无权限的队友被拦在登录页

## 坑

- **生产流量。** 一台机器、闲时休眠——别把用户导给它，把团队导给它。
- **静态思维。** App 的威力在于它*活在 Devin 的环境里*——接上你的数据/MCP，否则你只是造了个低配 Vercel。

## 自检

1. Devin App 和 PR preview 的区别是什么？*（App 从 Devin 的机器上常驻服务于稳定 URL——有状态、持久、登录门控——不是构建产物。）*
2. 「团队登录后打开」对内部工具意味着什么？*（鉴权继承自组织——不用再自建登录体系。）*
3. 哪类内部工具最适合 Apps？*（dashboard 和 staging 类——「现在够用」胜过「以后完美」——维护成本近零。）*

## Sources

- [Introducing Devin Apps](https://devin.ai/blog/devin-apps)
- [Devin Apps 教程 — 用提示词建私有内部应用](https://lightmind24.blogspot.com/2026/11/devin-apps-tutorial-build-private.html) —— 第三方最完整的实操：第一条 prompt 该放什么、App 如何继承你的设计体系、哪里是 Apps 的边界
- 相关：[第 6 篇 — 事件驱动的 Automations](automations-101-event-driven.md)（定时刷新）
