# 指南 3 — 定时哨兵 Bot

**目标：** 一个拥有某 recurring 质量检查的 Bot——按时间表运行它、分拣失败、追到根因、交付修复。
**级别：** 中级
**出处部署：** Cognition 的 **Layout Bot**——盯 Devin web app 的 layout-shift 回归。每 3 小时构建生产 `main`，模拟首次/重复/延迟请求三种访问，提交修复。**3 周 159 个 PR；卡顿 −70%。** 在野生环境里，同一形态已跑到最大规模：Grant Sanderson 的 **Manim 维护 Bot** 在 3Blue1Brown 背后的开源引擎上做 issue 预检——**96.6k stars、月下载 25 万**的维护量在维护者看到之前就被消化。
**来源：** [launch post](https://devin.ai/blog/introducing-devin-bots) · [Automations docs](https://docs.devin.ai/product-guides/automations)

## 模式

有些活永远干不完——它按时钟循环：性能预算、视觉回归、依赖保鲜、密钥扫描、可用性。哨兵 Bot 拥有的是*检查本身*，不只是修复：代码库变化时它维护检查持续有效、过滤噪声、只在回归为真时开修复 PR。

```text
cron ──► Bot wakes ──► run check under realistic conditions
                           │
              pass ────────┴──────── fail
               │                       │
             quiet            rerun to filter flakes
                                       │
                              trace to introducing PR
                                       │
                          fix PR + before/after evidence
```

## 前置条件

- 能在 Bot 机器上跑的检查（build、测试套件、Lighthouse、自定义脚本）
- 已建 Devin Bot（第 1 篇）或 Automation（第 6 篇）——两者都行；Bot 在两次运行之间多一层判断力

## 第 1 步 — outcome prompt

按 Layout Bot 的公开行为重构：

```text
Your job is to keep <surface> from <regressing>.

Watch <check/channel>, where <the check> posts every <interval>. Take over
that check and keep it working as the code changes. When something
regresses: rerun to rule out flakiness, trace the regression to the PR
that introduced it, and open a fix PR with before/after evidence.
```

`<check>` 槽位的真实部署示例：

- 跨首次/重复/延迟请求的 layout-shift 度量（Layout Bot）
- 你最慢 5 个端点的 p95 延迟（Latency Optimizer 模板）
- `npm audit`/CVE 扫描（Code Health Engineer 模板）
- 死代码检测（Code Reaper 模板）

## 第 2 步 — 排定周期

在聊天里对 Bot 说：

```text
Run this check every 3 hours on a schedule.
```

Bot 会提议一个 automation；你批准一次。（想自己配 cron 的话见第 6 篇手工 automation。）之后可在 Bot 的 Settings → Automations 管理。

## 第 3 步 — 真实条件才有意义

Layout Bot 的检查不是跑一次——它模拟**首次访问、重复访问、单独延迟请求**，因为它抓的回归只在特定负载形态下出现。编码你的等价条件：

- 哪个环境——Bot 在自己 VM 上构建生产 `main`，不是 dev server
- 哪些输入——冷/热缓存、种子数据、真实请求顺序
- 哪个阈值——一个数字，不是"感觉变慢"

## 第 4 步 — 噪声纪律

两条规则防哨兵喊狼来了：

1. **先重跑再行动**——Layout Bot 对疑似抖动结果先重跑。写进 prompt：*"rerun any failed check once before acting on it."*
2. **先溯源再修复**——每个回归都追到引入它的 PR。没有根因的修复是猜。

## 第 5 步 — 每个修复都带证据

159 个 PR 每个都带**前后对比视频**。你的检查的等价证据：

| 检查 | 修复 PR 里的证据 |
| --- | --- |
| Layout/视觉 | 录屏或截图，前 vs 后 |
| 延迟 | 时序数字，两次同口径测量 |
| 死代码 | 为什么这段代码不可达 |
| 依赖/CVE | 安全公告 + 解决它的 diff |

## Verify it

- [ ] automation 存在并按你设的 cron 触发（Settings → Automations 能看到运行记录）
- [ ] 人为埋的回归产出了带前后证据的修复 PR
- [ ] 疑似抖动的运行触发了重跑而不是修复
- [ ] 检查本身被维护——app 在它底下变化时 Bot 更新了检查

## 坑

- **拥有修复却没拥有检查。** 检查坏了一周没人发现，说明 Bot 拥有错了对象——prompt 必须把检查本身指派给它。
- **有 cron 没判断。** 裸定时 automation 能跑检查；Bot 决定失败是否真实。只有完全不需要分拣的检查才用裸 automation（第 6 篇）。
- **只报警不修复。** 往频道里发"发现回归"的哨兵是在给人类造活。这个部署的价值在于它*修*——按这个标准要它。

## 自检

1. 为什么哨兵按计划构建生产 `main`，而不是等故障被人报上来？*（目标是「没有回归」而不是「修已报 bug」——所有权意味着在人发现问题之前先发现。）*
2. Layout Bot 修 PR 时附 before/after 视频——这给 reviewer 带来了什么？*（不用本地复现就有合并信心；证据随 PR 走。）*
3. 为什么回归要追到引入它的那个 PR 而不是只修症状？*（拥有检查意味着拥有其历史——修复落在根因上，知识留下来。）*

## Sources

- [Introducing Devin Bots](https://devin.ai/blog/introducing-devin-bots) — Layout Bot 机制与数字
- [Automations — docs](https://docs.devin.ai/product-guides/automations) — 排程、触发器、条件
- 相关：[第 6 篇 — 事件驱动的 Automations](automations-101-event-driven.md)（这个循环的非 Bot 版本）
