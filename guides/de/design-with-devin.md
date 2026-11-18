# Leitfaden 8 — Design & visuelle Arbeit

**Ziel:** Devin als Art Director und Implementierer für Produktions-Visualdesign nutzen — generierte Bilder, Animations-Systeme, Typografie — nur durch Konversation.
**Level:** mittel
**Quell-Deployment:** die **Spraycash**-Landing-Page — das gesamte visuelle System einer Fintech-Site wurde im Devin-Chat mit Kimi K3 entworfen, alle Prompts veröffentlicht: Hero-Imagery, geschichtete Wolken-Animationen, SVG-Draw-on-Ring, Drei-Font-Typosystem.
**Quellen:** [vollständiger Bericht mit Prompts](https://dev.to/ibrahimpima/designing-the-spraycash-ui-with-kimi-k3-in-devin-4l2f)

## Das Muster

Design-via-Agent scheitert, wenn Prompts *Vibes* beschreiben ("mach es premium"). Es funktioniert, wenn du Art Direction machst wie ein Creative Director: **Referenzen, Constraints und ein Kritik-Loop**. Devins Vorteil gegenüber einem Design-Tool ist, dass es die *Implementierung* produziert — die Animation ist Code, die Bilder sind generiert und platziert, das Typosystem ist ausgeliefertes CSS.

```text
Brief + Referenzen ──► Devin produziert visuelle Assets + Code
        ▲                         │
        └──── Kritik-Loop: "die Ring-Animation zeichnet zu schnell,
              verlangsame das stroke-dashoffset-Easing auf 1.4s" ────┘
```

## Schritt 1 — Briefen wie ein Creative Director

Die Prompts des Spraycash-Berichts teilen eine Form — konkrete Substantive, keine Geschmacks-Adjektive:

```text
Hero section: dark navy (#0A1628) background, a circular progress ring
as the visual anchor — SVG stroke-dashoffset draw-on animation over
1.4s ease-out, layered clouds behind it drifting on separate
translateX loops at 40s/60s/90s periods so the parallax never repeats.
```

Gib ihm: Paletten-Hexes, den Animations-Mechanismus (nicht "mach es animiert"), Timing-Werte, Layer-Reihenfolge.

## Schritt 2 — Das Typosystem vor den Pixeln fixieren

Spraycash legte früh ein **Drei-Font-System** fest — Display, Body, Mono — bevor Komponenten angefasst wurden. Mach es genauso; es ist die visuelle Entscheidung mit der größten Hebelwirkung:

```text
Type system: <display font> for hero + section heads, <body font> for
prose, <mono> for numbers/labels. Set the scale: 64/40/28/18/14.
Nothing else uses another size.
```

## Schritt 3 — Bilder innerhalb der Session generieren

Devin generiert und platziert Assets — benutze keine Stockfotos auf einer designten Seite. Der Bericht zeigt generierte Hero-Imagery, die zur Palette des Briefs passt. Halte generierte Assets konsistent, indem du die Stil-Direktive einmal festlegst (Palette, Licht, Material) und für jede Asset-Anfrage wiederverwendest.

## Schritt 4 — Mit Mechanismen animieren, nicht mit Adjektiven

| Vage (scheitert) | Mechanisch (funktioniert) |
| --- | --- |
| "sanfter Eingang" | "stagger children 80ms, translateY(12px)→0, opacity 0→1, 400ms ease-out" |
| "subtiler Parallax" | "drei Layer, translateX-Loops mit 40/60/90s-Perioden" |
| "zeichne den Ring" | "stroke-dasharray = Umfang, dashoffset C→0 über 1.4s animieren" |

Spraycashs Ring, Wolken und gestaffelte Reveals wurden alle auf diesem Level spezifiziert — und als echtes CSS/SVG ausgeliefert, nicht als Mockups.

## Schritt 5 — Der Kritik-Loop ist das Handwerk

Die eigentliche Lektion des Berichts: Qualität kam von *Iterationen* — "der Ring zeichnet zu schnell", "die Wolken lesen sich als Rauschen, Opazität um 30 % senken", "Mono-Font auf den Zahlen". Plane 3–5 Kritikrunden pro visuellem Anker ein. Devin hält die ganze Seite im Kontext; jede Runde ist eine Nachricht, kein Ticket.

## Verifizieren

- [ ] Die Seite rendert mit *null* Stock-Imagery — alle Assets generiert oder codiert
- [ ] Jede Animation ist ein benannter Mechanismus mit Timing-Werten im CSS
- [ ] Ein Typosystem, eine Skala — keine streunenden Größen
- [ ] Bei 3+ Breiten betrachtet bricht oder clippt nichts

## Fallstricke

- **Adjektiv-Prompts.** "Premium", "sleek", "modern" erzeugen Slop. Mechanismen und Werte erzeugen Handwerk.
- **One-shotting.** Die erste Renderung zu akzeptieren ist, warum agent-gemachte Seiten agent-gemacht aussehen. Der Kritik-Loop ist, wo Qualität wohnt.
- **Das Lock-down verpassen.** Palette + Typosystem *zuerst* als Constraints setzen; Assets, die vor den Constraints generiert wurden, passen danach nie zusammen.

## Wissenscheck

1. Warum veröffentlichte der Spraycash-Autor jeden Prompt wörtlich? *(Die Prompt-Sequenz *ist* das Design-Artefakt — Art Direction durch Konversation ist nur reproduzierbar, wenn die Konversation es ist.)*
2. Was braucht "generierte Imagery + geschichtete Animation", was ein Screenshot-Mock nicht braucht? *(Auslieferbare Assets und ein funktionierendes Animations-System — die Verifikation ist eine gerenderte Seite, nicht das Bild einer.)*
3. Wann ist Chat-Direktion besser als ein Design-Tool für Landing-Pages? *(Wenn der Output ohnehin Produktionscode sein muss — die Design-Session *ist* die Implementierung.)*

## Quellen

- [Designing the Spraycash UI with Kimi K3 in Devin](https://dev.to/ibrahimpima/designing-the-spraycash-ui-with-kimi-k3-in-devin-4l2f) — vollständige Prompts und Iterations-Historie
- Verwandt: [built-with-devin — Patterns](https://github.com/Till3005/built-with-devin#patterns--write-ups)
