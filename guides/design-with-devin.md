# Guide 8 — Design & visual work

**Goal:** use Devin as your art director and implementer for production visual design — generated imagery, animation systems, typography — through conversation alone.
**Level:** intermediate
**Source deployment:** the **Spraycash** landing page — a fintech site's entire visual system designed inside Devin chat with Kimi K3, every prompt published: hero imagery, layered cloud animations, SVG draw-on ring, three-font type system.
**Sources:** [full write-up with prompts](https://dev.to/ibrahimpima/designing-the-spraycash-ui-with-kimi-k3-in-devin-4l2f)

## The pattern

Design-via-agent fails when prompts describe *vibes* ("make it premium"). It works when you art-direct the way you'd brief a designer: **references, constraints, and a critique loop**. Devin's edge over a design tool is that it produces the *implementation* — the animation is code, the imagery is generated and placed, the type system is shipped CSS.

```text
brief + references ──► Devin produces visual assets + code
        ▲                     │
        └──── critique loop: "the ring animation draws too fast,
              slow the stroke-dashoffset easing to 1.4s" ──────┘
```

## Step 1 — Brief like a creative director

The Spraycash write-up's prompts share one shape — concrete nouns, no adjectives-of-taste:

```text
Hero section: dark navy (#0A1628) background, a circular progress ring
as the visual anchor — SVG stroke-dashoffset draw-on animation over
1.4s ease-out, layered clouds behind it drifting on separate
translateX loops at 40s/60s/90s periods so the parallax never repeats.
```

Give it: palette hexes, the animation mechanism (not "make it animate"), timing values, layer order.

## Step 2 — Fix the type system before the pixels

Spraycash locked a **three-font system** early — display, body, mono — before touching components. Do the same; it's the single highest-leverage visual decision:

```text
Type system: <display font> for hero + section heads, <body font> for
prose, <mono> for numbers/labels. Set the scale: 64/40/28/18/14.
Nothing else uses another size.
```

## Step 3 — Generate imagery inside the session

Devin generates and places assets — don't stock-photo a designed page. The write-up shows generated hero imagery matched to the brief's palette. Keep generated assets consistent by fixing the style directive once (palette, lighting, material) and reusing it for every asset request.

## Step 4 — Animate with mechanisms, not adjectives

| Vague (fails) | Mechanical (works) |
| --- | --- |
| "smooth entrance" | "stagger children 80ms, translateY(12px)→0, opacity 0→1, 400ms ease-out" |
| "subtle parallax" | "three layers, translateX loops at 40/60/90s periods" |
| "draw the ring" | "stroke-dasharray = circumference, animate dashoffset C→0 over 1.4s" |

Spraycash's ring, clouds, and staggered reveals were all specified at this level — and shipped as real CSS/SVG, not mockups.

## Step 5 — The critique loop is the craft

The write-up's real lesson: quality came from *iterations* — "the ring draws too fast," "clouds read as noise, drop opacity 30%," "mono font on the numbers." Budget 3–5 critique rounds per visual anchor. Devin holds the whole page in context; each round is a message, not a ticket.

## Verify it

- [ ] The page renders with *zero* stock imagery — all assets generated or coded
- [ ] Every animation is a named mechanism with timing values in the CSS
- [ ] One type system, one scale — no stray sizes
- [ ] Viewed at 3+ widths, nothing breaks or clips

## Pitfalls

- **Adjective prompts.** "Premium," "sleek," "modern" give slop. Mechanisms and values give craft.
- **One-shotting.** Accepting the first render is why agent-made pages look agent-made. The critique loop is where quality lives.
- **Missing the lock-down.** Set palette + type system as constraints *first*; assets generated before constraints are set never match after.

## Knowledge check

1. Why did the Spraycash author publish every prompt verbatim? *(The prompt sequence *is* the design artifact — art direction through conversation is reproducible only if the conversation is.)*
2. What does 'generated imagery + layered animation' require that a screenshot mock doesn't? *(Shippable assets and a working animation system — the verification is a rendered page, not a picture of one.)*
3. When is chat-direction better than a design tool for landing pages? *(When the output must be production code anyway — the design session *is* the implementation.)*

## Walkthrough — brief by mechanism, refine by critique, on Devin CLI v3000.14 (swe-2-flash-medium)

A bare fintech page (`index.html`, default sans-serif), one Spraycash-style brief with real mechanisms — hex palette, `stroke-dashoffset` ring over 1.4s ease-out, three cloud layers at 40/60/90s, a 3-font scale — then one critique round with exact corrections. Both rounds happened inside one session.

**Video (61 s, silent):** bare page → mechanism brief → implementation → rendered hero → critique → refined render.

[![From a bare HTML page to a designed hero — brief, render, critique, re-render](https://till3005.github.io/built-with-devin/assets/guides/design-with-devin/walkthrough-poster.webp)](https://till3005.github.io/built-with-devin/assets/guides/design-with-devin/walkthrough.mp4)

![1. The starting point — plain HTML, default styling](https://till3005.github.io/built-with-devin/assets/guides/design-with-devin/step1-bare-page.webp)
*1. Before: three lines of copy and a button, nothing else*

![2. The implementation report — every mechanism named: dashoffset 1131→203.6 over 1.4s, 40/60/90s layers, 56/28/16 scale](https://till3005.github.io/built-with-devin/assets/guides/design-with-devin/step2-brief-applied.webp)
*2. The brief's numbers landed verbatim in the code — plus a prefers-reduced-motion fallback it added itself*

![3. First render — navy hero, draw-on ring at 82%, drifting cloud layers, mono stat figures](https://till3005.github.io/built-with-devin/assets/guides/design-with-devin/step3-first-render.webp)
*3. Round 1 output — real CSS/SVG, not a mockup*

![4. The critique round applied — clouds to 12% opacity, ring muted to #3ECF8E, stats gap 48px; it even flagged the CTA still used the old green](https://till3005.github.io/built-with-devin/assets/guides/design-with-devin/step4-critique-applied.webp)
*4. Critique is where the craft lives: exact values in, exact diff out — and it caught a mismatch we didn't mention*

![5. Final render — same structure, muted and balanced](https://till3005.github.io/built-with-devin/assets/guides/design-with-devin/step5-final-render.webp)
*5. Round 2 output — the loop is a message, not a ticket*

## Sources

- [Designing the Spraycash UI with Kimi K3 in Devin](https://dev.to/ibrahimpima/designing-the-spraycash-ui-with-kimi-k3-in-devin-4l2f) — full prompts and iteration history
- Related: [built-with-devin — patterns](https://github.com/Till3005/built-with-devin#patterns--write-ups)
