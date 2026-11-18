# Bot outcome prompts，逐句拆解

**目标：** 按已公开部署的真实写法写 outcome prompt——授予一个领域的所有权，而不是派任务清单。
**级别：** 中级 · **用时：** 起草 20 分钟，校准一周

每个产出大数字的公开 bot 部署，开头都是一条指派*结果*的简短 prompt。本篇收集真实案例并反向拆解它们为什么有效。

## 范本

> *"your job is to product manage the android app"*

Android Bot 的全部任务书。一句话产生了 44 天的自主工作：bot 把这个结果自行拆解成它自己写的 ticket，每个 ticket 跑一个 Devin session，交付 1,134 个已合并 PR（[launch post](https://devin.ai/blog/introducing-devin-bots)）。注意这条 prompt **没有**包含什么：没有 ticket 列表、没有验收标准、没有排期——结果本身就隐含了这一切。

## 有效 outcome prompt 的解剖

| 要素 | 作用 | 示例 |
| --- | --- | --- |
| **一个角色** | 规定 bot 如何*行事*，而不只是产出什么 | "product manage"、"own the QA of onboarding flows" |
| **有边界的面** | bot 能完整看见的范围——一个 app、一项检查、一个数据源 | "the android app"、"layout regressions"、"30+ onboarding flows" |
| **隐含的完成定义** | bot 能自我核验的状态 | "feature parity with iOS"、"no layout-shift regressions"、"every flow green" |
| **常驻授权** | bot 自己决定*何时*以及*下一步做什么*——这才是 bot 而不是脚本 | "your job is to…"、"keep…"、"watch for…" |

## 官方模板市场的句式

16 个[市场模板](https://devin.ai/bots/templates)都遵循同一套语法。泛化后的可复用公式：

**拥有一个领域** —— "Find bugs, improvements, performance and refactoring work in a named product area; open one small PR at a time with proof it works."（Software Factory：在指定产品域找 bug/改进/性能/重构工作，每次开一个小 PR 并附上能跑通的证据）

**拥有一项检查** —— "Every 3 hours, build production main, simulate first/repeat/deferred visits, and file fixes with before/after videos for any regression you introduce—or find."（Layout Bot 模式：每 3 小时构建生产 main、模拟三种访问、对任何回归提交带前后对比视频的修复）

**拥有一个生命周期阶段** —— "Take a ticket or an ask to a tested PR and through review."（Product Engineer：把工单或请求推进到已测试 PR 并过评审）

**拥有一个节奏** —— "Weekly: remove dead code, one safe PR per round."（Code Reaper：定时结果以节奏陈述，而非触发器）

**拥有团队代谢** —— "Watch the channels, post updates, hand work to the right teammate, follow up until done."（Chief of Staff）

**拥有卫生** —— "Old flags, stale deps, CVEs — turned into small safe PRs."（Code Health Engineer）

## 多 bot 组织：带授权的 prompt

在 bot 舰队里（SuperJennyStack、Frankie、tigsbot），chief bot 的 prompt 里写的是*路由契约*：哪个 bot 拥有哪个面、何时向上升级而不是横向委派。人类真正的那条 prompt 是汇总规格："bring me every open decision in one thread"（把所有待决事项汇总到一个 thread 给我）。完整组织架构见[第 4 篇](bots-203-multi-bot-org.md)。

## 反模式

- **任务形 prompt。** "Fix these 12 issues"——bot 干完就闲置；你得到的是一个 session，不是 bot。
- **不可验证的结果。** "Make the app better"——没有自检手段，bot 唯一的出口就是 Needs-you 刷屏。
- **看不见的域。** 如果结果需要 bot 接触不到的系统（够不着的 staging、读不了的仪表盘），它会卡住或编造进度。给它那个面，或者缩小结果。
- **没有合并授权故事。** 88% 的自合并率存在的前提是 CI 和评审门已按自动合并配置好。写明规则："merge when CI is green and diff < N lines"或"always open as draft for human review"。

## 起草你自己的——三行测试

一条好的 outcome prompt 依次回答：

1. **什么是你的？** —— 那个面
2. **什么叫好？** —— 可验证的状态
3. **你为此做什么？** —— 常驻行为

如果一个陌生人无法从外部核验第 2 行的真伪，就收紧它。

## Sources

- [Introducing Devin Bots](https://devin.ai/blog/introducing-devin-bots) · [Bots docs](https://docs.devin.ai/work-with-devin/bots) · [Template marketplace](https://devin.ai/bots/templates)
- 实名部署报告见 [built-with-devin](https://github.com/Till3005/built-with-devin#documented-deployments)
