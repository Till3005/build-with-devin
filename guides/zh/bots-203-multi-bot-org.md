# 指南 4 — 多 Bot 组织

**目标：** 一个跑整个业务单元的 Bot 层级——一个编排者向专家 Bot 委派，一个人类通过单一每日 thread 做决策。
**级别：** 高级
**出处部署：** Jenny Xu 的 **SuperJennyStack**——~20 个 Bot 运营一家手游工作室。~50 → **1,900 PR/周**，每周发版，工作室收入 ×6。已作为社区模板上架 [Bot 市场](https://devin.ai/bots/templates)。官方的 **bot 间 grant 交接**（QA → Developer → 复测 → PM 汇报）用的是同一套机制、更小规模。
**来源：** Jenny Xu 公开的栈（[via 发布报道](https://x.com/cognition/status/2122737511684587551)）· [Bots docs](https://docs.devin.ai/work-with-devin/bots)

## 模式

别建一个什么都会的 Bot——建一家小公司：

```text
                    ┌─────────────┐
              ┌────►│ Orchestrator │◄──── one roll-up thread
              │     └──────┬──────┘      (4×/day, emoji answers)
              │            │ grants: read + message
     ┌────────┼────────┬───┴─────┬──────────┐
     ▼        ▼        ▼         ▼          ▼
  SuperPM  SuperDev  SuperQA  SuperRelease  SuperSupport
  (what)   (build)   (verify) (ship)        (users)
```

人类是 CEO：编排者把每个下级 Bot 的待决事项收进**一个 Slack thread，每天 4 次**，用 emoji 回答。

这个形态最小的有据版本已经出了真产品：Noah Zixin Zhang 用 **Chief-of-Staff → 产品负责 Bot → 专家 Bot** 的约 8 Bot 链路，~48 小时端到端建成 [SupaSEO](https://supaseo.dev)（~951 commits；人类只写了落地页）。他的两条实战笔记在任何规模都适用：**一个跨项目共享的专家 Bot 胜过每项目各建一个**，且提示词保持细粒度——组织架构替代不了简报。

## 前置条件

- 完成第 1 篇——会创建和指挥 Bot
- 已连 Slack——这个模式活在 Slack 里；编排者的汇总 thread 就是全部 UX
- 一个有边界、岗位可分的领域（一个产品、一间工作室、一块服务区）

## 第 1 步 — 先画组织架构

Jenny 公开的栈——抄*形态*，不抄名字：

| Bot | 拥有 |
| --- | --- |
| Orchestrator (SuperJenny) | 向所有其它 Bot 委派；把它们的请求汇编成一个 thread；按她的性格/习惯训练 |
| PM (SuperPM) | 从指标 + 商店评论 + 趋势排出每日修复清单 |
| Release (SuperRelease) | 每周构建，周五可提商店 |
| QA (SuperQA) | 真机测试，带视频证据 |
| Support (SuperSupport) | 起草每条商店评论回复待批准；夜里帮玩家 |

其余 ~15 个 Bot 覆盖开发、Unity、UI、iOS、Android、分析。来自该部署的经验法则：**组织架构图上叫得出名字的岗位各配一个 Bot**——不是按任务，按*职责*。

## 第 2 步 — 建专家 Bot

每个岗位一个 Bot，配收窄的 outcome prompt：

```text
You own QA for <product>. Test every release candidate on real devices,
post video proof, and block release on failures. Report what needs a
decision to the orchestrator.
```

每个 Bot 的 Instructions 只写它岗位的规则；共享知识（品牌、发布流程、谁批什么）放进各 Bot 的 instructions 或共享资源——Bot 之间没有全局记忆，所以编排者的 prompt 承载着结缔组织。

## 第 3 步 — 接 grants

一个 grant 给 Bot A 对 Bot B 的读/发消息权限——Bot 间交接工作就靠它（Bot 会发起 grant 申请；你批一次卡片）。编排者需要能到达每个专家。

文档化的官方变体——更小、同机制：

```text
QA Bot finds a bug ──grant──► Developer Bot fixes ──► QA retests on
staging ──► PM Bot reports status in channel
```

grant 按窄批准：编排者能读和发消息给专家；专家之间不必互达。

**11/20 权限模型。** 共享 Bot 和 service user 现在只能看到你显式授予的资源——repo、密钥、plugin、playbook、skill 和 MCP server 都按 Bot 逐个授权，session 也带自己的分享/隐私开关。接线前先读[访问与安全文档](https://docs.devin.ai/work-with-devin/bots/access-and-security)：能给专家发消息却读不到它 repo 的 Bot，实际上接不住交接。

## 第 4 步 — 汇总 thread

这是最重要的一条指令——它把 20 个 Bot 的打扰折算成一个习惯：

```text
Collect every pending decision from the Bots you work with into one
Slack thread, posted at <times> daily. For each item: what's blocked,
the options, your recommendation. I answer in replies/emoji; treat my
replies as decisions and relay them.
```

Jenny **每天 4 次**跑这个、**用 emoji** 回答。纪律：你从不直接和专家说话——编排者转达你的决定并跟进到完成。

## 第 5 步 — 节奏 = 组织的心跳

| 节奏 | 谁跑 |
| --- | --- |
| 每日排序修复清单 | PM Bot（指标 + 评论 + 趋势） |
| 每周发布候选 | Release Bot → QA Bot 签字 |
| 每日 4 次决策 thread | Orchestrator |
| 夜间玩家支持 | Support Bot（起草回复等早晨批准） |

每个 Bot 拥有自己的循环；编排者拥有循环的排程。

每个 Bot 有自己的循环；orchestrator 掌管循环的日程。

## 第 6 步 — Bot 间协议（BotSpeak）

没人提醒你的规模问题：Jenny 的 20+ Bot 每天发 **700+ 条消息**——她根本看不过来。她的解法是 **BotSpeak**：Bot 之间专用的省 token 简语协议（[原推](https://x.com/xujennyc/status/2123111543105868166)）：

| 规则 | 含义 |
| --- | --- |
| 简语 | 用 `ACK` 之类的代号代替完整回复 |
| ASD-STE100 | 简化英语语法——航空文档标准，无歧义且省 token |
| emoji 回执 | 用 ✅ 表情代替「收到，谢谢」 |
| 无寒暄 | Bot 之间只发对方需要的信息 |
| 对人用完整句 | 汇总 thread 仍是带决策上下文的完整句子 |

切换后 6 天：Bot 无需她自主决策 **12×**、重复提问 −50%、Bot 间澄清帖 −12%。协议存在的原因不是省 token——是省*注意力*：bot 间消息变短，人的那一条 thread 才可读。

## Verify it

- [ ] 每个专家 Bot 有收窄的 outcome prompt 和生效中的 grants
- [ ] 编排者按时发布合并决策 thread
- [ ] 你用 emoji 答的一个决策被转达并由对应专家解决
- [ ] 一次跨 Bot 交接端到端完成（发现 → 修复 → 验证 → 汇报）
- [ ] 今天你发的消息数 < 已合并 PR 数

## 坑

- **会话追踪先崩。** [100 Days of Devin](https://www.raijuna.com/blog/devin-100-day-challenge-day-1) 实录发现舰队先垮在「哪个 Bot 出了这个 PR？哪个在等我？」——光是搭建就吃掉了周配额约 18%。第一天就把舰队可观测性算进预算。
- **跳过编排者。** N 个 Bot 各自 DM 你就是 N 倍噪声。判断必须汇入单一 thread 组织才成立。
- **岗位边界模糊。** "Dev Bot" 和 "Fix Bot" 会打架。边界按组织架构走——QA *验证*、Release *发布*、PM *排优先级*。
- **过度 grant。** 网状 grant（人人可达人人）复刻混乱。经编排者走星型拓扑。
- **Bot 间写长文。** Bot 互相写段落就是每天 700 条消息的来源——上 BotSpeak 式协议：简语 + emoji 回执 + 无寒暄；只有对人用完整句。

## 自检

1. 为什么 SuperJennyStack 把所有人机交互汇成一条线程？*（注意力才是瓶颈，不是算力——20 个 Bot 发 20 条线程，等于又是 20 份工作。）*
2. 什么时候用 grant 比「问 orchestrator」强？*（需要的能力已经归另一个 Bot 所有——grant 借所有权而不是复制所有权。）*
3. 「每天 4 次、用 emoji 回复」说明了什么委托深度？*（Bot 替代的是决策带宽不是人头——人留下判断层，丢掉了打字层。）*

## Sources

- [Introducing Devin Bots](https://devin.ai/blog/introducing-devin-bots) — SuperJennyStack 数字、grant 交接变体
- [Bot marketplace](https://devin.ai/bots/templates) — SuperJennyStack 社区模板 + 16 个官方模板
- [Bots docs](https://docs.devin.ai/work-with-devin/bots) — grants、memory、[access & security](https://docs.devin.ai/work-with-devin/bots/access-and-security)
- 相关：[第 5 篇 — 参考基准锚定的 swarm](bots-204-reference-grounded-swarm.md)（*构建*而非*运营*的 swarm）
