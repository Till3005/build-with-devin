# 指南 13 — 官方用例食谱

**目标：** Cognition 官方文档里已验证的用法模式，整理成食谱——什么活该切给 Devin，以及 40+ 个带可复制 prompt 的文档化配方。
**级别：** 入门（广度篇）
**来源：** [Best Practices](https://docs.devin.ai/use-cases/best-practices.md) · [Use-case gallery](https://docs.devin.ai/use-cases/gallery/index.md) · [use-case tutorials](https://docs.devin.ai/use-cases/index.md)

## 统领一切的那条规则

官方指导，原话逻辑：挑 **wide & shallow**（宽而浅）的活——一大池简单、可水平扩展的任务永远胜过复杂的全新构建。

| 理想任务 | 反面任务 |
| --- | --- |
| 初级工程师复杂度的重复性子任务 | 全新的复杂功能 |
| 每片 < 90 分钟人工量 | 拆不开的东西 |
| 客观的通过/失败验证 | "看着对就行" |
| 隔离、向后兼容、可并行 | 纠缠的依赖 |

文档点名的四种最佳切片形态：**迁移、重构、现代化、技术债积压。**

## 食谱目录

以下全部是官方 gallery 里的文档化用例——每个都带可复制 prompt。按"它从人一周里拿走什么活"组织。

### 事故与生产健康

| 配方 | 机制 |
| --- | --- |
| 自动调查 Datadog/PagerDuty 告警 | Webhook/API 触发 → 会话起火即查 |
| 自动生成 postmortem | PagerDuty 关闭 → Devin 起草时间线、根因、行动项 |
| 每日修 Sentry 新错误 | 每晚 cron 拉新错误 → 早上有修复 PR |
| 端到端调试 bug 报告 | 把报告 + Datadog 日志 + DB 权限交给 Devin → 根因 |

### 定时卫生（文档里 ROI 最高的一页）

| 配方 | 节奏 |
| --- | --- |
| 每周依赖更新 PR | 每周：过期包 → 已测试升级 PR |
| 每晚跑 staging E2E | 每晚：跑套件、失败建工单 |
| 每周从已合并 PR 生成 changelog | 周五：分类 changelog → Slack |
| 每日 Datadog 健康摘要 | 每日：错误扫描 → Slack 摘要 |
| 每日设计系统审计 | 每日：标记已合并 PR 里的硬编码颜色/缺失 token |
| Feature-flag 清理 | 发布后一次性会话剥掉 flag + 死代码 |
| 每周 Notion 状态摘要 | 每周：PR/commit 汇总 → Notion |
| 从会议记录生成 PR | 每小时：轮询 Granola → 提取工程任务 → 子会话 |

### 代码质量

| 配方 | 机制 |
| --- | --- |
| 合并前自动修 PR bug | Devin 审每个 PR，把修复推到分支 |
| 给服务补单测 | 建一个写测试 skill，套用到收费/退款/webhook 流程 |
| 抓视觉回归 | repo skill：PR 前对每个受影响页面截图 |
| 每个 PR 跑迁移检查清单 | repo skill 抓破坏性操作、校验 schema 变更 |
| 拆巨型 router | 2,000 行 Express router → 按域拆路由共享中间件 |
| 提覆盖率 | Devin 分析测试套件、写测试补缺口 |
| 跨 repo 修已知 CVE | 官方 skills（[devin-vuln-fixes](https://github.com/cognitionai/devin-vuln-fixes)）：只读盘点 → 审批门 → 确认版本补丁 → 前后测试 → 每 repo 一个 PR |

### 迁移与功能开发

| 配方 | 机制 |
| --- | --- |
| 50 文件 REST→GraphQL | 定范围 → 无冲突工作包 → 并行（第 11 篇） |
| React 18→19 升级 skill | 把官方升级指南变成适配你代码库的分阶段 skill |
| OpenAPI spec → 实现 | YAML spec → Express handler + Zod 校验 + Supertest |
| Stripe checkout 流程 | spec → 能跑的流程 + 测试 + 浏览器验证 |
| Next.js 应用 i18n | 装 next-i18next、抽字符串、3 语言浏览器检查 |
| Figma → 像素级还原 | Figma MCP → 从 mockup 生成组件 |
| Django 应用 docker 化 | 多阶段 Dockerfile + Django/Postgres/Redis compose |

### 项目管理与数据

| 配方 | 机制 |
| --- | --- |
| Linear 自动分拣 bug | 打 label → Devin 调查 |
| PRD → sprint 工单 | Notion PRD → 切成 Linear ticket |
| 积压任务实施方案 | 多选 Linear ticket → 带置信度评分的方案 |
| Slack 里 `/dana` 查数据 | 任意频道用自然语言查数据库 |
| 定制 API 用量仪表盘 | Devin 在 v3 API 上建定制看板 |

### 让 Devin 自己变更好（"Devin Optimization"）

| 配方 | 教训 |
| --- | --- |
| 功能 prompt 从 42→12 ACU | 解剖一个昂贵会话：3 个根因 → 重写 prompt |
| 3 个会话赛跑一个问题 | 并行会话竞速不同优化策略；最好的上线 |
| 一夜 8 个并行会话 | 8 个无测试模块 → 早上有单测 PR |
| 评估 30 个库 | 每库一个会话 → 打分排序对比 |
| 把 hotfix 提炼成 skill | 从一次成功的事故会话抽出可复用 skill |
| 每周知识去重 | 定时会话合并/清理知识建议 |
| 团队上手指南 | Devin 读自己的文档 → 按你技术栈写入门指南 |

## 怎么用这本食谱

1. 从**定时卫生**挑一个——最便宜的首胜（一个你不用再过脑的每晚/每周循环）
2. 有 PagerDuty/Datadog/Sentry 就加一个**事故**配方
3. 某个配方起效后，冻结成 **skill**（第 12 篇）或 **Bot**（第 1–5 篇）——上表每一行都能以这两种形态存续

## Sources

- [Use-case gallery](https://docs.devin.ai/use-cases/gallery/index.md) — 以上全部配方，每个带可复制 prompt
- [Best Practices](https://docs.devin.ai/use-cases/best-practices.md) — 切片教条
- [Use-case tutorials](https://docs.devin.ai/use-cases/index.md) — API 集成、覆盖率、容器化、前端组件、MCP
- 相关：[第 11 篇 — 规模化迁移](migrations-at-scale.md) · [第 6 篇 — Automations](automations-101-event-driven.md)
