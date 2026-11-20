# 指南 11 — 规模化迁移

**目标：** 把大型迁移（语言、框架、数据库、依赖、架构）跑成几百个已验证的小 PR，而不是一次英雄式重写。
**级别：** 中级 → 高级
**来源：** [Best Practices](https://docs.devin.ai/use-cases/best-practices.md) · [Migration & Modernization](https://docs.devin.ai/use-cases/migration-modernization.md) · 迁移示例：[Java upgrades](https://docs.devin.ai/use-cases/examples/java-upgrades.md)、[COBOL](https://docs.devin.ai/use-cases/examples/cobol-modernization.md)、[SAS→PySpark](https://docs.devin.ai/use-cases/examples/sas-to-pyspark.md)、[JS→TS](https://docs.devin.ai/use-cases/examples/javascript-to-typescript.md)、[NoSQL→SQL](https://docs.devin.ai/use-cases/examples/nosql-to-sql.md) · Nubank 案例

## 官方 playbook

Devin 自己的文档对什么能扩展说得很直白：**wide & shallow**（宽而浅）胜过 **tall & deep**（高而深）。迁移就是典型的宽而浅工作——同一个小变换施加到几百个相互独立的单元上。

```text
migration ──► slice into isolated units (<90 min each)
                 │
        ┌────────┴────────┐
        ▼                 ▼
   skill for the      parallel sessions,
   transformation     one slice each
        │                 │
        └────► verify per slice (tests/build/CI)
                        │
              human review → merge → repeat
```

## 第 1 步 — 确认你的迁移够格

官方标准——大部分应满足：

- 大量重复性子任务
- 每片复杂度属初级工程师水平
- 隔离的、增量的、向后兼容的变更
- **每片有客观验证**（硬性要求：测试、构建、CI 或自定义脚本）
- 片间依赖最小

不够格的：必须一次性整体落地的全 repo 重写。

## 第 2 步 — 切片

切片是最小原子单元——一个文件、一个 notebook、一个模块：

| 规则 | 为什么 |
| --- | --- |
| 每片 < 90 分钟人工工程量 | Devin 的可靠性是按片计的 |
| 独立 + 向后兼容 | 各片可并行、任意顺序合并 |
| 每片自带验证 | 没验证就没自动化——这是失败闸门 |

官方示例：50 文件的 REST→GraphQL 迁移 → 定范围、拆成无冲突的工作包、并行跑。

## 第 3 步 — 把变换写成 skill

一个 skill = 每个会话都跑的同一个配方。官方示例（Java 7→8，节选）：

```text
## Procedure
1. Verify the project is on Java 7
2. Install the Java 8 JDK
3. Update build configuration
4. Identify and replace deprecated Java 7 APIs
5. Analyze for Java 8 enhancement opportunities
6. Update unit tests
7. Test thoroughly
8. Update documentation
9. Build and verify
```

写你自己的：明确步骤、一个端到端参照（指南或视频）、**多个 before/after 代码示例**——输入/输出对是最高质量的信号。

## 第 4 步 — 并行会话

skill 定稿后，把切片扇出到各会话——走 [API](https://docs.devin.ai) 或 Bot 的子会话（第 4 篇）。每片 → 一个会话 → 一个 PR。人工评审把关合入 `main`。

规模上来后数字复利：Nubank 的数百万行 ETL 迁移跑这套循环到了 8–12× 效率——fine-tuned Devin 把单任务时间从 ~40 分钟压到 ~10。

## 第 5 步 — 盯错误率，不盯进度条

小错误率会在几千片上复利。按仪表盘运营，不凭感觉：

- 跟踪每片一次通过率——skill 才是你的修复点，不是会话
- 失败的片回灌进 skill（文档自己的回路：*"feed session links into Devin to patch the gaps"*——把会话链接喂给 Devin 修补缺口）
- 片是隔离的所以合并顺序自由——利用它

## Verify it

- [ ] 每片 ~90 分钟内完成且可独立合并
- [ ] 验证失败的片产出修复或被标记的工单——绝不静默合入
- [ ] skill 在前 20 片上可度量地变好（每片人工纠正减少）
- [ ] 进度可数：已迁 N/M 片、通过率可见

## 坑

- **没切片的迁移。** "Migrate the whole repo" 是官方反面教材——无隔离、无并行、无单元验证。
- **没有 before/after 示例。** 没示例的 skill 让每个会话产出不同风格。
- **跳过人工评审。** 并行 ≠ 无人值守——每片进 `main` 前仍要过审。

## 自检

1. 为什么「广而浅」切片好过「深而全」？*（每片必须落地为绿——90 分钟的已验证 PR 会复利；3 天大分支会被 main 甩烂。）*
2. 为什么每片都要自带验证？*（没有逐片证明，500 个 PR 的迁移就是 500 个未验证 diff——失败面是乘出来的不是除出来的。）*
3. Nubank 报 8–12× 效率——为什么这数字可信而非营销？*（公开方法论：真实 ETL 管线前后阶段耗时实测，不是推算。）*

## 实录演示 —— 迁移回路串行跑一遍，录于 Devin CLI v3000.14（swe-2-flash-medium）

「几百个并行会话」那部分要云端额度，但*回路本身*不需要——所以用免费档串行演示。`migrate-demo`：4 个 optparse CLI（greeter/calc/backup/report），每个工具一个行为测试，变换配方写成 `.devin/skills/optparse-to-argparse/SKILL.md`。prompt：“按独立 slice 迁移……每迁一个工具跑测试，绿了才动下一个。”

**视频（41 秒，无声）：** 基线 → skill 被调用 → 4 片各绿 → optparse 残留为零。

[![完整切片回路——每个工具迁完都跑测试，逐 skill 配方的收尾汇报]({B}/walkthrough-poster.webp)]({B}/walkthrough.mp4)

![1. 基线——4 个 optparse 工具，7 个行为测试全绿]({B}/step1-baseline.webp)
*1. 基线：4 个 OptionParser 工具、7 个测试、一个已提交的 skill 配方*

![2. skill 从 .devin/skills 自动调用——先读全部工具和测试文件再动手]({B}/step2-skill-invoked.webp)
*2. `Invoked skill optparse-to-argparse`——配方驱动整轮*

![3. 切片回路——“Green. Now calc.py——它靠 rest 读位置参数，所以用 parse_known_args 保持形状。”]({B}/step3-slice-loop.webp)
*3. 逐片验证；它甚至自己发现 calc.py 需要 `parse_known_args` 保位置参数*

![4. /exit 后验证——4 个文件迁完，+18/−18，optparse 引用清零，零提交]({B}/step4-verify-diff.webp)
*4. 四个各自验证过的小 diff——这就是切片纪律，只是没有并行舰队*

## Sources

- [Best Practices — docs.devin.ai](https://docs.devin.ai/use-cases/best-practices.md)
- [Migration & Modernization + 5 个示例 playbook](https://docs.devin.ai/use-cases/migration-modernization.md)
- [Use-case gallery — Migrations](https://docs.devin.ai/use-cases/gallery/index.md)
- 相关：[第 7 篇 — 企业级铺开](enterprise-playbook.md)（形态 1 就是本篇的组织级版本）
