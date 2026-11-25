# 指南 8 — 设计与视觉工作

**目标：** 把 Devin 当你的美术指导 + 实现者，纯靠对话完成生产级视觉设计——生成图像、动画系统、字体排印。
**级别：** 中级
**出处部署：** **Spraycash** 落地页——一个金融科技站的整套视觉系统在 Devin 聊天里用 Kimi K3 设计完成，prompt 全部公开：hero 图像、分层云朵动画、SVG 描边圆环、三字体体系。
**来源：** [含全部 prompt 的完整实录](https://dev.to/ibrahimpima/designing-the-spraycash-ui-with-kimi-k3-in-devin-4l2f)

## 模式

"让 agent 做设计"失败的原因是 prompt 描述的是*感觉*（"make it premium"）。有效的方式是像给设计师下 brief 一样做美术指导：**参考、约束、批评回路**。Devin 相对设计工具的胜势在于它产出的是*实现*——动画是代码、图像是生成并落位的、字体体系是交付的 CSS。

```text
brief + references ──► Devin produces visual assets + code
        ▲                     │
        └──── critique loop: "the ring animation draws too fast,
              slow the stroke-dashoffset easing to 1.4s" ──────┘
```

## 第 1 步 — 像创意总监一样下 brief

Spraycash 实录的 prompt 都是同一个形态——具体名词，零品味形容词：

```text
Hero section: dark navy (#0A1628) background, a circular progress ring
as the visual anchor — SVG stroke-dashoffset draw-on animation over
1.4s ease-out, layered clouds behind it drifting on separate
translateX loops at 40s/60s/90s periods so the parallax never repeats.
```

给它：色板 hex 值、动画*机制*（不是"让它动起来"）、时序数值、图层顺序。

## 第 2 步 — 先锁字体体系，再动像素

Spraycash 早早锁定了**三字体体系**——display、body、mono——之后才碰组件。照做；这是单个杠杆率最高的视觉决策：

```text
Type system: <display font> for hero + section heads, <body font> for
prose, <mono> for numbers/labels. Set the scale: 64/40/28/18/14.
Nothing else uses another size.
```

## 第 3 步 — 在会话内生成图像

Devin 会生成并落位素材——别给设计稿贴图库照片。实录里生成的 hero 图像与 brief 色板匹配。保持生成素材一致性的办法：风格指令只定一次（色板、光照、材质），之后每个素材请求复用它。

## 第 4 步 — 用机制写动画，不用形容词

| 模糊（会失败） | 机制化（有效） |
| --- | --- |
| "smooth entrance" | "stagger children 80ms, translateY(12px)→0, opacity 0→1, 400ms ease-out" |
| "subtle parallax" | "three layers, translateX loops at 40/60/90s periods" |
| "draw the ring" | "stroke-dasharray = circumference, animate dashoffset C→0 over 1.4s" |

Spraycash 的圆环、云层、交错入场全部按这个精度指定——交付的是真 CSS/SVG，不是 mockup。

## 第 5 步 — 批评回路才是手艺

实录的真正教训：质量来自*迭代*——"the ring draws too fast"、"clouds read as noise, drop opacity 30%"、"mono font on the numbers"。每个视觉锚点预算 3–5 轮批评。Devin 把整页留在上下文里；每一轮是一条消息，不是一张工单。

## Verify it

- [ ] 页面渲染*零*图库素材——全部生成或手写
- [ ] 每个动画在 CSS 里都是有名有值的机制
- [ ] 一套字体体系、一套字号阶梯——没有游离字号
- [ ] 3+ 种视口宽度下无破版、无裁切

## 坑

- **形容词 prompt。** "Premium"、"sleek"、"modern" 产出 slop。机制和数值才产出手艺。
- **一发入魂。** 接受第一版渲染是 agent 页面看起来像 agent 做的原因。质量活在批评回路里。
- **漏了锁定。** 色板 + 字体体系要*先*设成约束；约束之前生成的素材永远对不齐。

## 自检

1. Spraycash 作者为什么逐字公开每个 prompt？*（prompt 序列本身就是设计产物——对话式美术指导只有对话可复现才可复现。）*
2. 「生成图像 + 分层动画」需要什么是截图 mock 给不了的？*（可上线的资产和能跑的动画系统——验证是渲染出的页面，不是页面的图片。）*
3. 落地页什么时候对话式指导胜过设计工具？*（产出必须是生产代码时——设计会话本身就是实现。）*

## 实录演示 —— 用机制下 brief，靠 critique 精修，录于 Devin CLI v3000.14（swe-2-flash-medium）

一个裸 fintech 页面（`index.html`，默认字体）+ 一段 Spraycash 式机制 brief（hex 色板、`stroke-dashoffset` 1.4s 画环、40/60/90s 三层云、三字体比例）+ 一轮带精确数值的 critique——两轮都在同一个会话里完成。

**视频（61 秒，无声）：** 裸页 → 机制 brief → 实现 → 渲染 hero → critique → 精修渲染。

[![从裸 HTML 到设计完成的 hero——brief、渲染、critique、再渲染](https://till3005.github.io/built-with-devin/assets/guides/design-with-devin/walkthrough-poster.webp)](https://till3005.github.io/built-with-devin/assets/guides/design-with-devin/walkthrough.mp4)

![1. 起点——纯 HTML，默认样式](https://till3005.github.io/built-with-devin/assets/guides/design-with-devin/step1-bare-page.webp)
*1. 之前：三行文案一个按钮，仅此而已*

![2. 实现汇报——每个机制都具名：dashoffset 1131→203.6 / 1.4s、40/60/90s 云层、56/28/16 字阶](https://till3005.github.io/built-with-devin/assets/guides/design-with-devin/step2-brief-applied.webp)
*2. brief 里的数值原样落进代码——还自己加了 prefers-reduced-motion 兜底*

![3. 首次渲染——navy hero、82% 画环、漂移云层、等宽数字](https://till3005.github.io/built-with-devin/assets/guides/design-with-devin/step3-first-render.webp)
*3. 第一轮产出——是真 CSS/SVG，不是效果图*

![4. critique 落地——云层压到 12% 透明度、环色收到 #3ECF8E、数字区距 48px；它还主动指出 CTA 仍用旧绿](https://till3005.github.io/built-with-devin/assets/guides/design-with-devin/step4-critique-applied.webp)
*4. 手艺活在 critique 里：精确数值进、精确 diff 出——还抓住了我们没提的错配*

![5. 最终渲染——同结构，沉稳平衡](https://till3005.github.io/built-with-devin/assets/guides/design-with-devin/step5-final-render.webp)
*5. 第二轮产出——迭代是一句话，不是一张工单*

## Sources

- [Designing the Spraycash UI with Kimi K3 in Devin](https://dev.to/ibrahimpima/designing-the-spraycash-ui-with-kimi-k3-in-devin-4l2f) — 全部 prompt 与迭代记录
- 相关：[built-with-devin — patterns](https://github.com/Till3005/built-with-devin#patterns--write-ups)
