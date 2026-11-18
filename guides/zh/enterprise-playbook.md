# 指南 7 — 企业级铺开模式

**目标：** 用已经产出公开数字的部署形态，把 Devin 铺到组织规模——不是试验，是已验证的打法。
**级别：** 中级（写给工程负责人）
**来源：** 已公开客户案例，[devin.ai/customers](https://devin.ai/customers)

六种部署形态，蒸馏自公布了结果的公司。成功的铺开大多用其中两三种，不是六种全上。

## 形态 1 — 遗留迁移引擎（Nubank、Comarch）

| | |
| --- | --- |
| 部署 | Nubank：数百万行、8 年 ETL 单体 → 子模块。Comarch：20 年、千万行 ERP 重建 |
| 结果 | 工程效率 8–12×、成本节省 20×（Nubank） |
| 机制 | 在*你的*代码库上 fine-tune Devin（Nubank 把 ~40 分钟/任务压到 ~10），然后把迁移当持续项目交给它——可追踪的小 PR，不是重写 |

**怎么抄：** 挑一个有边界的遗留系统；fine-tune 或用 playbook 教；跑 Migration Engineer 式循环——一次大迁移切成带进度面的小 PR。胜利是复利的：每个迁完的模块都让下一个 session 更聪明。

## 形态 2 — 主作者仓库（EBANX、Gumroad、Finch）

| | |
| --- | --- |
| 部署 | EBANX：**92% 已合并 PR 由 Devin 写**。Gumroad：Devin 是 repo **第一贡献者**（1,500+ PR）。Finch：3,000 PR，省 ~20 工程师月 |
| 机制 | Devin 在这些 repo 上不是助手——是默认作者。人类评审和指挥 |

**怎么抄：** 挑一个高吞吐 repo；ticket 默认路由给 Devin 会话；人类评审。要盯的指标是 authored-PR 占比——超过 ~50% 你就在这个形态里了；低于它，你还在试点期。

## 形态 3 — 常驻一线响应（Modal、Reducto、AngelList）

| | |
| --- | --- |
| 部署 | Modal：**80% 事故在工程师打开 thread 前已被调查**。Reducto：Devin Oncall 是一线；工程师几乎不再被 page。AngelList：Devin 在人工前定位 70% 事故根因 |
| 机制 | PagerDuty/Slack 触发 → 会话带日志/repo 权限调查 → 人醒来前报告已落地 |

**怎么抄：** [Devin Oncall](https://docs.devin.ai) 或 PagerDuty 触发的 automation（第 6 篇，配方：事故 → 调查）。度量"事故预调查占比"——每一点都是换回来的睡眠。

## 形态 4 — 维护舰队（Airbyte、Melius）

| | |
| --- | --- |
| 部署 | Airbyte：维持 **700+ connector** 运转。Melius：~100 PR/天 |
| 机制 | 没人想要的长尾——connector 腐化、依赖漂移、过期 flag——路由给持续吞吐的 Bot/automation |

**怎么抄：** 盘点你的维护积压（工程师躲着走的活）；用 Code Health Engineer / Code Reaper 式官方模板 Bot 包起来，按周节奏跑。

## 形态 5 — 全员席位（Wayfair、The Access Group、Citi）

| | |
| --- | --- |
| 部署 | Wayfair：1,600+ 工程师全上。Access Group：Devin 覆盖 250 个产品、2,000+ 工程师 → 产出 5×。Citi：40,000 开发者铺开，技术供应商支出砍 30% |
| 机制 | 不是更多 agent——是*席位*：每个工程师都有 Devin 访问权、共享 playbook、组织级知识 |

**怎么抄：** 公开案例里的铺开顺序高度一致——试点团队 → 量化结果 → playbook/知识标准化 → 席位扩张。跳过知识层是席位铺开卡死的原因：见 [playbooks 篇](playbooks-and-knowledge.md)。

## 形态 6 — 流程闸门（Hamming、Litera、Eight Sleep）

| | |
| --- | --- |
| 部署 | Hamming：Devin 写 25% 代码量。Litera：回归周期缩短 90%。Eight Sleep：交付量 8× |
| 机制 | Devin 拥有管线的一个阶段——回归测试、QA——而不是整个产品 |

**怎么抄：** 找人力成本最痛的那个管线阶段（回归周期、QA）；指派给 Bot 或 automation；量这个阶段的前后周期时间。

## 案例隐含的反面教材

- **是同事，不是工具。** 数字大的部署都给 Devin 所有权（repo、面、阶段），不是派活——和第 1–5 篇同一个教训。
- **永远试点。** 公开结果共享一个特征：一个*毕了业*的可量化试点。事先定好毕业标准（PR 占比、事故覆盖、节省工时）。
- **没有知识层。** 每个大部署都把规范编码在某处——fine-tune、playbook、bot 指令。没有它，质量随会话漂移。

## Sources

- [devin.ai/customers](https://devin.ai/customers) — 引用的全部案例与数字
- [built-with-devin — 企业索引](https://github.com/Till3005/built-with-devin#enterprise-deployments) — 登记表里的已核验案例表
