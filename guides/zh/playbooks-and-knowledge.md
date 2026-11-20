# 指南 9 — Playbooks 与知识层：把组织约定写成代码

**目标：** 把你最强工程师脑子里默认的东西写下来，让 Devin 会话和 Bot 在组织规模上可靠——写成 playbooks（可重复流程）和 knowledge（常驻上下文）。
**级别：** 中级 · 每个大型公开部署共享的那一层
**来源：** [docs.devin.ai](https://docs.devin.ai) · [第 7 篇](enterprise-playbook.md)的部署教训

## 为什么这一层决定一切

每个公开的企业结果——Nubank 的 8–12×、EBANX 的 92% 署名 PR、Wayfair 的 1,600 席位——都建立在被编码的约定上。没有它，Devin 的产出随会话漂移：每个 session 重新发现你的技术栈、合并规则、测试习惯。有了它，第 500 个会话表现得像你最强工程师状态最好的那天。

两个互补的产物：

| 产物 | 是什么 | 类比 |
| --- | --- | --- |
| Knowledge | Devin 读取的常驻上下文——repo 事实、规范、环境坑 | 入职文档 |
| Playbook | 命名的可重复流程——触发条件、步骤、验收标准 | 人人可调用的 runbook |

## 第 1 步 — 从你自己的纠正里挖

最便宜的知识已经存在：翻最近 20 个 Devin 会话，收集你每次打出的纠正——*"we deploy via Cloud Run"*、*"never `git push --force`"*、*"tests need `npm run db:seed` first."* 每条纠正都是一条已被证明重要的知识条目。

还可以挖：
- 人类在 Devin PR 上反复写的评审意见
- 解释*为什么*改动做成那样的 PR 描述
- 入职文档——任何你会讲给新员工的东西

## 第 2 步 — 写钉得住的知识条目

好条目是一行、祈使句、有作用域：

```text
- Deploy only via `make deploy-cloudrun` — never run gcloud directly.
- Migrations require a matching rollback file in prisma/rollbacks/.
- The staging seed user is qa+admin@corp.io; never create real-looking users.
```

坏条目是散文、愿望（"write good tests"）、或秘密（凭证永远不进 knowledge——用 secrets store）。

## 第 3 步 — 给可重复工作写 playbook

> **平台更新（2026 年 11 月）：** Playbook 正在迁移到 **Skills**——各账号分批迁移，新账号只有 Skills（每个 playbook 会变成一个相同 org/enterprise 作用域的 skill）。本步所有内容对 skills 完全适用：skill 就是同样的、可调用的具名流程。

playbook 把流程打包，让任何会话（或 Bot）以同样方式执行。有效的结构：

```markdown
# <动词 + 宾语> — 例："Cut a release"
## When to use
<触发条件>
## Steps
1. <确定性步骤>
2. ...
## Acceptance
<通过/失败检查>
## Failure modes
- <已知故障 → 怎么处理>
```

发布到全组织，让会话、automation、Bot 都能调用——这就是把一次性成功的会话变成组织能力的那一步。

## 第 4 步 — 喂给 Bot

Bot 的 **Instructions**（第 1 篇）是 Bot 作用域的知识——每个会话启动时读的规则。岗位法放那里；组织法放 knowledge；流程放 playbook。分层让每个产物小而常新。

## 第 5 步 — 纠正回路

知识会腐烂。让它保鲜的回路：

1. 会话/Bot 犯错 → 你在聊天里纠正
2. Bot 把纠正写进记忆（或你加进 knowledge）
3. 每周复核：把 Bot 记忆里反复出现的条目晋升为组织知识；删掉一个月没人触发的条目

Devin Coach（官方 Bot 模板）就是为这个生的——每周汇报 Devin 在哪里卡住，并每次提一个修复：一条 note、一个 skill、或一项配置改动。

## Verify it

- [ ] 一个新会话在你的 repo 上零提问知识层已覆盖的问题
- [ ] 你给 Bot 的上一条纠正出现在它的记忆文件里
- [ ] 两个不同会话跑同一个 playbook 产出同样形态的结果

## 坑

- **写愿望。** "Follow best practices" 什么都改变不了；"run `npm run db:seed` before tests" 改变一切。
- **设了就忘。** 过期知识比没有更糟——Devin 会自信地照办。每月复核。
- **复制文档。** Knowledge 装的是 Devin *会错*或*不可能知道*的东西，不是你 wiki 的副本。

## 自检

1. playbook 和 knowledge 的区别？*（playbook 是具名任务的可重复规程；knowledge 是每个会话都该默认的常驻上下文。）*
2. 为什么「把最强工程师的默认假设写下来」才是真正的企业瓶颈？*（agent 质量从来不是上限——缺失的上下文才是；knowledge layer 是组织惯例的存放地。）*
3. 一条惯例什么时候该落成 playbook 而不是继续口口相传？*（第一次某个会话因为缺这一步而做错的时候。）*

## 实录演示 —— 写得下来的约定才管用，录于 Devin CLI v3000.14（swe-2-flash-medium）

组织级 playbook 在云端，但本篇的核心论点——*约定写一次，之后每个会话都遵守*——本地就能验证。`devin rules` 会把 `.windsurf/rules/*.md` 当作 always-on 上下文。我们把三条「过往纠正」挖成 `house-rules.md`（用 unittest 跑测试、永不提交、算金额必须复用 `total()`），然后开新会话只提需求、不提规矩。

**视频（30 秒，无声）：** 规则文件 → 没提规矩的新会话 → 三条全守住。

[![家规文件、一个不带提醒的需求、条条被遵守]({B}/walkthrough-poster.webp)]({B}/walkthrough.mp4)

![1. 挖出来的规则 + 光秃秃的 prompt——“加个 line_total(items)，再写个测试”]({B}/step1-rules-and-prompt.webp)
*1. 三条家规已入库；prompt 对约定一字未提*

![2. 它复用了 total()、跑的是 `python3 -m unittest`（不是 pytest）、3 个测试全过]({B}/step2-rules-obeyed.webp)
*2. 零提醒下条条遵守——这就是知识层在起作用*

![3. /exit 之后——`M orders.py`、`M tests/test_orders.py`，`git log` 只有 init 一个提交]({B}/step3-no-commits.webp)
*3. 连「永不提交」都守住了——用 git 验证，不是听它自己汇报*

## Sources

- [docs.devin.ai](https://docs.devin.ai) — knowledge、playbooks、Bot instructions/memory
- 相关：[第 7 篇 — 企业级铺开模式](enterprise-playbook.md)（这一层是大多数铺开跳过的一步）
