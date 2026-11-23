# 指南 18 — 跟 Devin 说话：提示词基本法

**目标：** 写出 Devin 不可能误读的指令——会话能交付与会话会跑偏的分水岭。
**级别：** 从这里开始
**来源：** [Coding Agents 101](https://devin.ai/agents101)（Cognition，2025 年 6 月）· [Instructing Devin Effectively](https://docs.devin.ai/essential-guidelines/instructing-devin-effectively)——两篇都是官方文档，以下是提炼 + 实战注解

## 为什么这篇排第一

这个仓库里的每篇指南都预设一项技能：你能把想要的东西说到 Devin 不可能理解歪。Cognition 自己的两份指导——*Coding Agents 101* 和文档站的 *Instructing Devin Effectively*——从两个角度说的是同一件事：**用 agent 用得最好的工程师，写得像在给初级同事布置任务，而不是在许愿。** 这篇就是这套教义的浓缩版，并接进课程体系的其他部分。

## 撑起其他一切的四条规则

**1. 说怎么做，不只说做什么。** "修 search 模块的 C++ bindings 让新单测通过——注意，每次改完都得重新编译 bindings 再测。"你 codebase 里的坑你自己最清楚，写出来。开放式指令（"让 app 好看点"、"优化数据库性能"）只会得到开放式的结果。

**2. 告诉它从哪开始。** 仓库、目录、文件、参考实现、文档链接——任何任务落到*你自己*桌上时你想要的东西。"用 `authTemplate.rs` 做参考保持错误处理风格一致"胜过一整段风格描述。

**3. 把成功定义成可以检查的东西。** 不是"确保能用"——而是 Devin 能跑的检查：*接口返回 200 且带 X/Y/Z 字段*、*组件在 1440px 和 375px 宽度下渲染且零 console 报错*、`npm test` 全绿。Devin 有一台完整的机器——浏览器、shell、IDE。叫它自己验证（"跑 `npm run dev` 确认 `/settings` 渲染正常"），它会在你看到 PR 之前就 QA 完。

**4. 给它反馈回路，不是反馈感觉。** 类型检查、linter、测试、CI——agent 的超能力是对着报错迭代。如果你的仓库没办法告诉它错了，那你就是反馈回路——而这是最贵的那种配置。

## 官方示范指令的解剖

Cognition 自己的样板 prompt，逐行注解：

> In the Devin repo, build a tool that monitors RAM and CPU usage of the remote machines Devin runs on.——*一行说清范围和目的*
>
> - Create a background task that launches when devin.rs starts——*分步骤，不是一大坨*
> - It opens a connection to all forked remote machines and monitors usage——*机制点名*
> - If usage exceeds 80%, emit a new type of Devin event (check how we use Kafka)——*成功标准 + 指向现有模式*
> - Architect so it doesn't block other operations——*只有作者知道的约束*

注意没有什么：审美意见、对冲、"也许"、"如果你觉得合适"。每一行都是懂系统的人已经做好的决定。

## 防线的另一边：什么留给自已

101 指南对上限说得很直白：**大任务上预期 ~80% 的时间节省，不是全自动。** 超过几个文件的活儿，就按多轮反馈来规划。赢的姿势是*架构师审初级工程师的 PR 草稿*——正确性归你，击键归 Devin。

实际推论：

- **边界写死。** "不要 merge、不要部署、不要碰 billing，除非先问我"——栅栏明写，别指望它的常识。
- **大活拆成可验证的子任务**——一个子任务一个会话，各自带成功检查（这也是为什么指南 11 的迁移模式有效：几百个小 PR，每个都可验证）。
- **重复三次就做成 Skill**——`SKILL.md` 写好一次，Devin 之后自动调用（指南 16）。

## 从"指令"到"所有权"

会话指令回答的是*"把这件事做好"*。Bot 的 outcome prompt 回答的是*"把这块地盘管好"*。教义相同——具体、边界、可检查的成功——只是对象从任务变成了责任。练熟了这里的写法，[outcome-prompts 参考](bot-outcome-prompts.md)会展示同一套肌肉怎么产出 Android Bot 的 1,134 个 PR。

## 实录演示 —— 录于 Devin CLI v3000.14（swe-2-flash-medium）

教义实盘跑在一个丢弃用的 `demo-repo` 上：四行 brief——做法+机制、点名文件、可检验的成功线、明确边界。一次会话，零中途澄清，自检通过。

**视频（90 秒，无声）：** brief → 改代码 → 权限提示 → 自检 → 边界被遵守。

[![SWE-2 Flash Medium 完成任务——5 个 unittest 全绿，未提交](https://till3005.github.io/built-with-devin/assets/guides/talking-to-devin/walkthrough-poster.webp)](https://till3005.github.io/built-with-devin/assets/guides/talking-to-devin/walkthrough.mp4)

![1. CLI REPL 在 demo-repo 里跑 SWE-2 Flash Medium，composer 就绪](https://till3005.github.io/built-with-devin/assets/guides/talking-to-devin/step1-repl-flash.webp)
*1. CLI REPL 在 demo-repo 里跑 SWE-2 Flash Medium——composer 就绪*

![2. 那份 brief——四行对应四条规则：怎么做、从哪开始、成功检查、边界](https://till3005.github.io/built-with-devin/assets/guides/talking-to-devin/step2-the-brief.webp)
*2. 那份 brief——四行对应四条规则：怎么做、从哪开始、成功检查、边界*

![3. 中途：正在写 test_app.py——权限提示给出 Allow / accept-edits / bypass / deny](https://till3005.github.io/built-with-devin/assets/guides/talking-to-devin/step3-edits-approval.webp)
*3. 中途：正在写 test_app.py——权限提示给出 Allow / accept-edits / bypass / deny*

![4. 自证：agent 请求跑的正是点名的检查——python3 -m unittest -v](https://till3005.github.io/built-with-devin/assets/guides/talking-to-devin/step4-self-check-prompt.webp)
*4. 自证：agent 请求跑的正是点名的检查——`python3 -m unittest -v`*

![5. 完成——5 个测试全过；汇报自己写明 "No commit made."](https://till3005.github.io/built-with-devin/assets/guides/talking-to-devin/step5-tests-green.webp)
*5. 完成——5 个测试全过；汇报自己写明边界已守："No commit made."*

![6. /exit 后——`devin -r` 恢复提示；git status 证明边界守住了：两个文件被改、零新提交](https://till3005.github.io/built-with-devin/assets/guides/talking-to-devin/step6-no-commit.webp)
*6. /exit 后——`devin -r` 恢复提示，`git status` 证明边界守住了：两个文件被改、零新提交*

## 验证一下

- [ ] 拿你 backlog 里的一个真实任务，你能在 10 分钟内写出含：点名的仓库/文件、参考模式、明确的验收检查、声明的边界的指令。
- [ ] 产出的会话没有中途问你一个"显而易见"的问题。
- [ ] Devin 在开 PR 前自己验证了——因为你在指令里要求了。

## 坑

- **指令里写着你的糊涂。** 验收检查说不出口，说明任务还没准备好——先跟 Devin 共创一份 PRD（101 指南也推荐），别指望它读懂你的心。
- **权限配不上野心。** 让看不到 CI 的账号去"修 CI"，产出的是自信的错。指令要匹配你实际给的权限。
- **审的是输出，不是正确性。** 测试全绿 + diff 看起来合理，是进展的证据，不是行为正确的证明。最后的验证层永远是你。

## 自测

1. *"写点单测"为什么败给"给 `poller.ts` 的重试路径写单测，mock `fetch`，覆盖超时和 5xx"？* 因为后者消除了 agent 替你拍板的必要：测什么、哪些边界重要、mock 什么。每个没写明的决定都是一次你不控制的掷硬币。
2. *Devin 开了个 PR，diff 干净、CI 全绿。完了吗？* 没完——CI 绿说明检查过了，不代表意图达成。最后一层验证还是你的；这个不对称就是交易本身（~80% 节省，正确性归人）。
3. *指令什么时候毕业成 Skill？* 当你发现自己在重打一遍的时候。第三次出现就该是 SKILL.md——指南 16 讲格式和发现路径。

## 来源

- [Coding Agents 101](https://devin.ai/agents101) — Cognition 的提示词教义：说怎么做、从哪开始、防御式提示、反馈回路、80% 规则
- [Instructing Devin Effectively](https://docs.devin.ai/essential-guidelines/instructing-devin-effectively) — 官方 do/don't 清单和上面解剖的示范指令
- [Devin 教程库](https://docs.devin.ai/tutorial-library) + [Devin University](https://learndevin.com) — 想要视频和课程形态的同类内容去这里
- 田野注：[社区实战报告](community-field-reports.md)里每一篇都收敛到同一个结论——要指令，不要许愿
- 下一篇：[指南 19 — 会话全环](the-session-loop.md)（简报之外的一整环）· [指南 1 — 你的第一个 Bot](bots-101-first-bot.md)（同一套教义，更大的对象）· [outcome prompts 参考](bot-outcome-prompts.md)
