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

## Sources

- [Designing the Spraycash UI with Kimi K3 in Devin](https://dev.to/ibrahimpima/designing-the-spraycash-ui-with-kimi-k3-in-devin-4l2f) — full prompts and iteration history
- Related: [built-with-devin — patterns](https://github.com/Till3005/built-with-devin#patterns--write-ups)
