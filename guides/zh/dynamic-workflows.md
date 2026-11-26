# 指南 20 — Dynamic Workflows

**目标：** 用一个确定性的 Python 脚本编排多个 Devin sessions——把独立工作扇出，把结构化结果传给后续阶段，在中断后恢复运行，并始终看清 ACU 成本。
**难度：** 高级 · **时间：** 设计第一次运行约 35 分钟；实际成本取决于 agent 数量
**来源：** [Dynamic Workflows 官方文档](https://docs.devin.ai/work-with-devin/dynamic-workflows) · 官方文档已于 2026-11-26 核验

> **证据状态：** 这是一篇基于官方来源的操作指南，尚未做独立复现。真实 workflow 会启动多个 Devin sessions，可能消耗大量 ACU，所以下面的复现练习故意收窄，并应经过批准。

## 什么时候用

当工作本身有真实结构时，使用 dynamic workflow：

- **宽扇出 + 汇总步骤**——大约 5 个或更多相互独立的文件、模块、接口、工单或候选方案，每个都需要判断或验证，最后还要合并、去重或做推荐。
- **分阶段流水线**——后续阶段消费前一阶段的结构化输出，例如 *audit → fix → verify*。
- **受控循环**——重复 run/fix/check，直到达到一个可测量的停止条件。

以下情况**不要**用：

- codemod、linter autofix、生成器或 shell 循环已经能机械完成。
- 只需要一两个独立 session，而且它们之间没有数据流动。
- 工作通过共享状态紧耦合，或者本来就很小、很顺序。

Workflow 不是“更多 AI”。它是把编排写成代码：脚本决定哪些 agent 运行、按什么顺序运行、收到什么 prompt，以及什么结构化数据继续向后传。

## 心智模型

```text
你描述结果
        ↓
Devin 编写 workflow.py
        ↓
脚本用 prompt + JSON Schema 调用 agent(...)
        ↓
每个 agent 返回结构化输出
        ↓
后续 prompt 由前面的输出构造
        ↓
运行被记录，可以恢复
```

Workflow 在后台运行时，编排 session 仍然可以交互。workflow 面板会显示阶段、agent 和实时状态；你可以打开单个 agent session、要求进度摘要，或停止运行。

企业账号可能需要管理员先在 **Enterprise Settings → Devin** 下启用 **Dynamic workflows**，否则企业内任何组织都不能使用。

## 编写契约

脚本由 Devin 写，但你在批准运行前应该像审查生产代码一样审查它。

| Primitive | 用途 |
| --- | --- |
| `register_workflow(meta)` | 在 agent 运行前声明名称、描述和阶段 |
| `agent(prompt, phase=..., schema=...)` | 运行一个 agent，并返回符合 JSON Schema 的 dict |
| `pipeline(items, stage1, stage2, ...)` | 让每个 item 独立流经各阶段，阶段之间没有屏障 |
| `parallel([...])` | 并发运行 async callables 并等待全部结果；只用于确实需要所有结果的阶段，如合并或去重 |
| `log("message")` | 写入运行期间可见的进度信息 |

Schema 设计规则：

1. 保持小、扁平、明确。
2. 返回标识符和证据，而不是长篇散文——branch 名、文件路径、数量、状态、单行发现。
3. 不需要下游工作时，返回 `None` 或显式失败状态。
4. 不把 secret 放进 prompt 或 schema。
5. 把 agent 输出当作进入下一个 prompt 的不可信输入；先验证，再行动。

## 确定性是 resume 的代价

恢复 workflow 时会从头重新执行脚本。已完成的 `agent()` 调用会回放记录输出；未完成或失败的调用会重新运行。这只有在脚本每次发出相同调用时才成立。

因此，workflow 逻辑和 prompt 不能依赖：

- 当前时间或日期
- 随机数或生成的 ID
- 环境变量
- 文件系统状态
- 网络响应

任何需要观察外部世界的事情都应该放进 `agent()` 调用。脚本只消费已记录的输出。

两个直接后果：

- 修改 prompt 会重新运行该 agent 以及它下游的所有工作。
- 中断或超时的运行可以用 run ID 恢复；默认和最大运行预算都是 7 天。

## Agent 在哪里运行

| 模式 | 什么时候用 | 交接方式 | 主要风险 |
| --- | --- | --- | --- |
| Separate VM（默认） | agent 需要隔离机器或正常 repo 环境 | 通过 git branch 推送/读取 | 每个 agent 的 setup 和成本更高 |
| Shared VM | agent 必须读取或修改当前工作树 | 共享文件系统 | CPU/内存竞争和写入冲突 |

对 shared-VM 扇出，必须给并行写作者严格不重叠的文件或目录。对 separate-VM pipeline，要把 branch 名放进结构化输出。

也可以把高容量、低判断强度的阶段（例如分类）固定到更便宜的 Devin mode。

## 构建第一个安全 workflow

第一次不要指向整个仓库。选一个足够证明模式、又小到负担得起的切片。

### 0. 选择收窄的单元

好的第一批切片：

- 3 个组件的无障碍审计
- 一个目录里的 SQL 查询分页问题
- 5 个开放工单的去重和严重性分诊
- 3 个迁移单元，各自独立 branch

坏的第一批切片：

- “审计整个 monorepo”
- “修掉所有 flaky tests”
- “永远审查每个文件”

### 1. 写结果，不写脚本

示例，改编自官方 migration 模式：

```text
Use a workflow to audit the auth, billing, and search modules for missing
pagination and N+1 query patterns. Run one analysis agent per module.
For each confirmed issue, run a fix agent on its own branch and verify the
fix with an EXPLAIN plan before and after. Roll up the confirmed fixes,
skipped items, and anything needing human review.
```

注意这个 prompt 包含了什么：范围、并行单元、阶段、验证方式和汇总形态。

### 2. 批准前审查生成的脚本

逐项检查：

- `register_workflow()` 在 agent 前调用。
- 每个 `agent()` 都有 schema。
- agent 数量由明确列表限制，而不是无界爬取。
- 失败行为明确：重试、带状态跳过、使用默认值，或让运行失败。
- 脚本是确定性的。
- separate-VM agents 通过 branch 交接代码；shared-VM agents 不会互相覆盖。
- 最终汇总包含证据和未解决项，而不是只写 “done”。

运行默认自动批准。如果希望每次运行前都有检查点，关闭 **Settings → Preferences → Auto-approve workflows**。

### 3. 运行、观察、正确停止

运行中：

- 在 workflow 面板看阶段和 agent 状态。
- 打开一个 agent session，检查它的 prompt 和 schema 是否符合意图。
- 向编排 session 要进度摘要，不要手动打断每个 agent。
- 如果设计错了，停止运行。停止会取消脚本并让剩余 child sessions 睡眠；已完成结果仍保留记录。

### 4. 只有在保持确定性后才恢复

如果运行中断，用同一个脚本和 run ID 恢复。如果修改了 prompt，要理解被修改的 agent 及其下游都会变成新工作。

### 5. 保存已验证的 workflow

workflow 跑通后，让 Devin 把它保存成 repo skill：`workflow.py` 放在描述何时使用的 `SKILL.md` 旁边。一次性编排由此变成可复用的组织能力。

## 成本控制

每个 workflow agent 都是一个 Devin session。成本同时随扇出宽度和 session 深度增长。

按这个顺序做：

1. 用 3 个 item 做原型。
2. 在 workflow 面板查看每个 agent 的 ACU 用量。
3. 扩大规模前先估算完整运行成本。
4. 分类/抽取阶段使用更便宜的 mode。
5. 把昂贵判断留给更少、更靠后的阶段。
6. 给循环设置硬停止条件。

循环必须有写清楚的退出条件，例如“连续 3 次通过”或“本轮没有修出新东西”。否则 workflow 可能持续消耗预算，产生技术上真实但无用的进展。

## Verify it

第一次复现只有全部满足以下条件才有效：

- [ ] workflow 在 3–5 个单元的有界切片上运行，而不是整个 repo。
- [ ] workflow 面板显示了阶段和单个 agent 状态。
- [ ] 至少一个下游 prompt 明确消费了上游 agent 的结构化输出。
- [ ] 打开并检查过一个 agent session。
- [ ] 最终汇总区分了已验证结果、跳过项、失败项和需要人工审查的项。
- [ ] 记录了每个 agent 和整个运行的 ACU 用量。
- [ ] 如果中断或主动停止，运行能正确恢复；否则记录了不能恢复的原因。

## 常见坑

- **用 agent 做机械工作。** 如果脚本可以确定性转换代码，就把脚本当工具，agent 只负责判断。
- **Schema 返回散文。** 长文本很难被下游消费；返回紧凑的结构化事实。
- **隐藏时间依赖。** 脚本里的“今天”、时间戳、随机 ID 或实时网络检查会破坏 replay 语义。
- **Shared-VM 写入冲突。** 两个 agent 编辑同一个文件不是并行，而是在制造 merge conflict。
- **无界扇出。** 在 workflow 内发现更多工作的 crawl 可能让成本爆炸。要么限制发现，要么把它变成上游人工批准的输入。
- **没有失败契约。** 运行前就决定失败 agent 是跳过、重试、阻塞该 item，还是让整个运行失败。
- **过早复用。** 在真实切片上成功运行并理解成本前，不要把 workflow 保存成 skill。

## 练习

1. 找一个仓库里的重复审查任务。写出 workflow prompt，然后在要求 Devin 运行前列出确切的扇出 items。
2. 为 *audit → fix* 设计两阶段 schema。除路径或 branch 名外，每个字段控制在 120 字符以内。
3. 给定一个失败 agent，写出三种失败策略并选择一种。说明汇总里应该显示什么。
4. 用 3-item 原型估算 50-item 扇出的成本。什么证据能让这个估算成立？

## Capstone

构建一个 workflow：按书面标准审计 5 个文件或模块，在独立 branch 上修复确认的问题，用最窄的真实检查验证每个修复，并输出最终证据表。第二次成功运行后，才把它保存为 skill。

## Knowledge check

1. 为什么 workflow prompt 不能用“今天”和随机 ID？*（恢复运行时会重新执行脚本；输入变化会改变 agent 调用身份，破坏确定性 replay。）*
2. 为什么 `parallel()` 不是默认组合 primitive？*（多数 pipeline 应该按 item 流动；`parallel()` 会形成屏障，只适用于确实需要所有结果的阶段。）*
3. 最安全的第一次扇出规模是什么？*（约 3–5 个单元的有界切片——足够证明编排，又足够小以便测量成本和检查行为。）*
4. 什么时候 workflow 值得变成 skill？*（在真实工作上成功、成本和失败行为已知、并且很可能复用之后。）*

## Sources

- [Dynamic Workflows — 官方文档](https://docs.devin.ai/work-with-devin/dynamic-workflows)
- [Advanced capabilities — managed Devins](https://docs.devin.ai/work-with-devin/advanced-capabilities)
- [Skills — 官方文档](https://docs.devin.ai/product-guides/skills)
- [Devin MCP — 官方文档](https://docs.devin.ai/work-with-devin/devin-mcp)

## Changelog

- 2026-11-26 — 根据官方文档创建初版。独立复现证据仍待补；在记录真实运行前，不要把练习视为已验证。
