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

18 个[市场模板](https://devin.ai/bots/templates)都遵循同一套语法。泛化后的可复用公式：

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

## 验证

- [ ] 从你仓库挑一个真实 backlog 项，改写成 outcome prompt——边界、可验证状态、常驻行为
- [ ] 拿给不熟悉代码库的人看：他能否从外部判断这个 Bot「做得好」？
- [ ] Bot 的第一条回复应该是计划或关于边界的澄清问题——如果它问「你想让我先做什么」，说明 prompt 没有赋予所有权

## 常见陷阱

- **披着 outcome 外衣的任务清单。**「先做 X 再做 Y 再做 Z」仍是 checklist——世界一变，Bot 就无法重新排序。
- **没有定义的「好」。**「让 app 保持好」无可验证状态，Bot 会替你选一个——而那不会是你想要的。
- **边界大于单一表面。**「负责工程」会失败；「负责 iOS app」能成。按一个外部人能完整观察到的范围切。

## 自检

1. 为什么「own the Android app」比「修 Android bug」有效？*（所有权意味着常驻判断——Bot 决定哪些 bug 重要，而不只是修不修。）*
2. 「让 CI 变快」错在哪？*（外部不可验证——没有阈值。「CI 低于 8 分钟」才有。）*
3. 「测试挂了发消息给我」回答了三问中的哪一问？*（常驻行为——它说了 Bot 对状态做什么，但没说什么边界、什么目标。）*

## 实录演示 —— outcome prompt 与 task prompt 正面对比，录于 Devin CLI v3000.14（swe-2-flash-medium）

Bot 需要 Max 或 Teams 方案——但本篇教的 prompt 机制与接入面无关，所以用 SWE-2 免费档 CLI 实录。同一个仓库（`orders.py`，基线只有 2 个测试），两个完全相同的副本，各喂一条 prompt：

- **任务式：** “给 apply_discount('SAVE10') → 90.0 和 total([]) → 0 各加一个测试……”
- **outcome 式：** “你的职责是管好 orders.py 的测试覆盖。好的标准：total、apply_discount、shipping_fee 每个分支都有测试，且 python3 -m unittest -v 全绿。”

**视频（64 秒，无声）：** 基线 → 任务式跑 → +6 行 → outcome 式跑 → 自己分解出覆盖图 → +37 行。

[![outcome 会话的汇报——13 个测试全绿，覆盖图是 agent 自己列的](https://till3005.github.io/built-with-devin/assets/guides/bot-outcome-prompts/walkthrough-poster.webp)](https://till3005.github.io/built-with-devin/assets/guides/bot-outcome-prompts/walkthrough.mp4)

![1. 基线上输入任务式 prompt——2 个测试，只点名条目](https://till3005.github.io/built-with-devin/assets/guides/bot-outcome-prompts/step1-task-prompt.webp)
*1. 基线上的任务式 prompt——给 agent 的是一张购物清单*

![2. 任务式跑完——恰好加了点名的 2 个测试、4 个全绿、“Nothing committed”，然后停住](https://till3005.github.io/built-with-devin/assets/guides/bot-outcome-prompts/step2-task-done.webp)
*2. 任务式：做完清单就停——这是个会话，不是个 owner*

![3. 相同副本上输入 outcome 式 prompt——角色、界面边界、可验证状态，没有任务清单](https://till3005.github.io/built-with-devin/assets/guides/bot-outcome-prompts/step3-outcome-prompt.webp)
*3. outcome 式：角色 + 有边界的管辖面 + “好”的定义——不给清单*

![4. outcome prompt 产出的 diff——每个分支都是 agent 自己枚举的](https://till3005.github.io/built-with-devin/assets/guides/bot-outcome-prompts/step4-outcome-diff.webp)
*4. 没人告诉它写哪些测试——+39 行，分支全是它自己列的*

![5. 汇报的是一个“状态”而不是“做完了”——“All 13 tests pass. Branch coverage: …”](https://till3005.github.io/built-with-devin/assets/guides/bot-outcome-prompts/step5-coverage-report.webp)
*5. 它对着“好”的定义自检，汇报的是覆盖图*

![6. 并排对比——任务式 +6 行；outcome 式 +37 行。同一模型、同一仓库](https://till3005.github.io/built-with-devin/assets/guides/bot-outcome-prompts/step6-side-by-side.webp)
*6. 同模型同仓库，只差 prompt 形状：+6 对 +37，4 个测试对 13 个*

## Sources

- [Introducing Devin Bots](https://devin.ai/blog/introducing-devin-bots) · [Bots docs](https://docs.devin.ai/work-with-devin/bots) · [Template marketplace](https://devin.ai/bots/templates)
- 实名部署报告见 [built-with-devin](https://github.com/Till3005/built-with-devin#documented-deployments)
