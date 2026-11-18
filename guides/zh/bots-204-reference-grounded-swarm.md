# 指南 5 — 参考基准锚定的 swarm

**目标：** 指挥一个 agent swarm 写出大型且*可验证*的系统——正确性持续对照可信基准检验，而不是对照感觉。
**级别：** 高级
**出处部署：** Harvey 的 **"Phil"**——~30 个 agent 写出协作式、Word 兼容的编辑器引擎（Rust + TypeScript）：**3 周 100 万+ 行，零人类工程师**。持续对照真实 Microsoft Word 行为和模拟律师谈判验证。人类通过记忆 + 决策日志掌舵，从不读代码。
**来源：** Gabe Pereyra 的发布实录（[via @gabepereyra](https://x.com/gabepereyra)）· [launch post](https://devin.ai/blog/introducing-devin-bots)

## 模式

swarm 失败的原因是没人能判断输出对不对。Phil 成功是因为每一行都能对照一个**真值基准**检验：真实的 Microsoft Word。agent 团队的工作是*对齐*——一个客观的、可持续检验的目标——而不是*发明*。

```text
   reference system (truth)
            ▲ compare
            │
┌───────────┴────────────┐
│  swarm of ~30 agents   │──► 1M+ LOC (Rust + TypeScript)
└────────────────────────┘
            ▲ steer
            │
   humans: memory + decision logs
   (never reading the code)
```

## 何时用

| 适合 | 不适合 |
| --- | --- |
| 按规范重实现（文件格式、协议、编辑器、编译器） | 没有客观答案的绿地产品 |
| 带 oracle 的移植/迁移（旧系统还能跑） | "对不对"要靠判断的新 UX |
| 任何能与工作系统 diff 的东西 | 正确性需要用户验证的系统 |

试金石：**机器能不能不靠你判定"正确"？** 能，swarm 就可扩展；不能，改用产品所有制 Bot（第 2 篇）。

## 第 1 步 — 先锁定基准

任何 agent 写码之前，检查必须已存在：

- Harvey 的基准：**真实 Microsoft Word 行为**——swarm 编辑器渲染的文档必须与 Word 一致
- 你的基准可能是：仍在运行的旧系统、一致性测试套件、golden files、规范测试集、API 契约

把对比放进 CI 或 swarm 高频运行的脚本——"输出是否匹配基准"必须廉价且自动，否则 agent 在两次检查之间漂移。

## 第 2 步 — 拆成各有归属的切片

~30 个 agent 不共享同一个 backlog——工作按子系统切分，每个 agent 拥有一个（文档模型、排版引擎、协作协议……）。结构同第 4 篇的组织架构，只是每个"员工"都是对准模块边界的编码会话：

```text
You own the <module>. Its contract is <interface/reference behavior>.
Your PRs are accepted when the reference checks pass — not when the
code looks done.
```

## 第 3 步 — 人类在代码之上掌舵

Harvey 没人读过那百万行。掌舵靠三层：

- **Memory** —— Bot 积累的"做过什么决定、为什么"
- **决策日志** —— swarm 在每个岔口选了什么
- **方向消息** —— "prioritize track-changes fidelity over performance this week"（本周优先级：修订追踪保真度高于性能）

你的评审面是*决策轨迹*，不是 diff。如果你发现自己在读生成代码来弄清发生了什么，去问编排者要决策日志。

## 第 4 步 — 顶层叠加对抗验证

Harvey 叠了第二层检查：**模拟律师谈判**——真实使用场景，抓一致性套件漏掉的东西。你的等价物：基准 diff 之上的场景层——真实工作流、对抗输入、fuzzing。基准检查抓*错*，场景检查抓*脆*。

## Verify it

- [ ] 存在自动化基准检查，且对每个变更运行
- [ ] 每个 agent 的验收标准是"基准通过"，永远不是"代码写了"
- [ ] 不读代码就能从日志/记忆回答"swarm 决定了什么、为什么"
- [ ] 故意弄坏的模块被基准检查抓住，而不是被你抓住

## 坑

- **先有 oracle 再扩规模。** 没有检查的 swarm 只产出体积——Phil 成功是因为 Word 永远是裁判。
- **审 diff。** 超过 ~2 个 agent 就不可扩展；你会成为瓶颈并失去 swarm 的速度优势。
- **归属模糊。** 两个 agent 改同一个模块就是合并地狱——归属边界就是架构。

## 自检

1. 为什么 Harvey 的 swarm 能成而多数多 agent 尝试崩溃？*（可信的外部参照——真实 Word 行为——让正确性在 swarm 速度下仍可机器检查。）*
2. 为什么人类通过 memory 和 decision log 引导而不是 review 代码？*（3 周 1M+ 行超出任何人阅读量；引导发生在意图层。）*
3. 采用此模式前要先验证的前提是什么？*（你的领域有没有 swarm 可以自我核对的参照——没有就先建 oracle。）*

## Sources

- [@gabepereyra](https://x.com/gabepereyra) — Harvey Phil 实录：~30 agent、1M+ 行、Word 基准验证、律师模拟
- [Introducing Devin Bots](https://devin.ai/blog/introducing-devin-bots)
- 相关：[第 4 篇 — 多 Bot 组织](bots-203-multi-bot-org.md)（同一套层级，不同目的：运营 vs 构建）
