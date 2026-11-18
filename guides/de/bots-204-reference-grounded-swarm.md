# Leitfaden 5 — Referenz-verankerter Schwarm

**Ziel:** einen Schwarm von Agenten dirigieren, um ein großes, *verifizierbares* System zu schreiben — bei dem Korrektheit laufend gegen eine vertrauenswürdige Referenz geprüft wird, nicht gegen Bauchgefühl.
**Level:** fortgeschritten
**Quell-Deployment:** Harveys **"Phil"** — ~30 Agenten schrieben eine kollaborative, Word-kompatible Editor-Engine in Rust + TypeScript: **über 1 Mio. Zeilen in 3 Wochen, null menschliche Ingenieure**. Laufend gegen echtes Microsoft-Word-Verhalten und simulierte Anwaltsverhandlungen verifiziert. Menschen steuerten über Memory + Entscheidungslogs, nie durch Code-Lesen.
**Quellen:** Gabe Pereyras Launch-Bericht ([via @gabepereyra](https://x.com/gabepereyra)) · [Launch-Post](https://devin.ai/blog/introducing-devin-bots)

## Das Muster

Ein Schwarm scheitert, wenn niemand sagen kann, ob der Output stimmt. Phil funktionierte, weil jede Zeile gegen eine **Referenz der Wahrheit** prüfbar war: das echte Microsoft Word. Die Aufgabe des Agenten-Teams war das *Abgleichen* — ein objektives, fortlaufend prüfbares Ziel — nicht das *Erfinden*.

```text
   Referenzsystem (Wahrheit)
            ▲ vergleicht
            │
┌───────────┴────────────┐
│  Schwarm von ~30 Agenten│──► 1M+ LOC (Rust + TypeScript)
└────────────────────────┘
            ▲ steuert
            │
   Menschen: Memory + Entscheidungslogs
   (lesen nie den Code)
```

## Wann einsetzen

| Gute Passform | Schlechte Passform |
| --- | --- |
| Eine Spec reimplementieren (Dateiformat, Protokoll, Editor, Compiler) | Greenfield-Produkte ohne objektive Antwort |
| Portierung/Migration mit Orakel (Altsystem läuft noch) | Neue UX, bei der "richtig" eine Urteilsfrage ist |
| Alles gegen ein laufendes System Diffbare | Systeme, deren Korrektheit Nutzer braucht |

Der Lackmustest: **Kann eine Maschine "korrekt" ohne dich entscheiden?** Wenn ja, skaliert ein Schwarm; wenn nein, nutze einen Product-owner-Bot (Leitfaden 2).

## Schritt 1 — Zuerst die Referenz sichern

Bevor irgendein Agent Code schreibt, muss die Prüfung existieren:

- Harveys Referenz: **echtes Microsoft-Word-Verhalten** — Dokumente, die der Editor des Schwarms renderte, mussten Word entsprechen
- Deine könnte sein: das noch laufende Legacy-System, eine Conformance-Suite, Golden Files, ein Spec-Testkorpus, ein API-Vertrag

Lege den Vergleich in CI oder ein Skript, das der Schwarm ständig ausführt — "entspricht der Output der Referenz?" muss billig und automatisch sein, sonst driften Agenten zwischen den Prüfungen auseinander.

## Schritt 2 — In besessene Slices zerlegen

~30 Agenten teilten sich nicht ein Backlog — die Arbeit wurde so zerschnitten, dass jeder Agent ein Subsystem besaß (Dokumentenmodell, Layout-Engine, Kollaborationsprotokoll, …). Strukturiere es wie das Organigramm aus Leitfaden 4, nur dass jeder "Mitarbeiter" eine Coding-Session ist, die auf eine Modulgrenze zeigt:

```text
You own the <module>. Its contract is <interface/reference behavior>.
Your PRs are accepted when the reference checks pass — not when the
code looks done.
```

## Schritt 3 — Menschen steuern oberhalb des Codes

Niemand bei Harvey las die Million Zeilen. Die Steuerung lief über:

- **Memory** — die angesammelten Fakten des Bots über getroffene Entscheidungen und deren Warum
- **Entscheidungslogs** — was der Schwarm an jeder Weggabelung wählte
- **Richtungs-Nachrichten** — "priorisiere Track-Changes-Treue über Performance diese Woche"

Deine Review-Fläche ist der *Entscheidungspfad*, nicht der Diff. Wenn du dich dabei ertappst, generierten Code zu lesen, um zu wissen, was passiert, frag den Orchestrator stattdessen nach dem Entscheidungslog.

## Schritt 4 — Adversariale Validierung obendrauf

Harvey legte eine zweite Prüfung darüber: **simulierte Anwaltsverhandlungen** — realistische Nutzung, die sichtbar macht, was eine Conformance-Suite verfehlt. Dein Äquivalent: eine Szenario-Schicht über dem Referenz-Diff — echte Workflows, adversariale Inputs, Fuzzing. Referenz-Checks fangen *Falsches*; Szenario-Checks fangen *Brüchiges*.

## Verifizieren

- [ ] Ein automatisierter Referenz-Check existiert und läuft gegen jede Änderung
- [ ] Das Akzeptanzkriterium jedes Agenten ist "Referenz besteht", niemals "Code geschrieben"
- [ ] Du kannst "was hat der Schwarm entschieden und warum" aus Logs/Memory beantworten, ohne Code zu lesen
- [ ] Ein absichtlich gebrochenes Modul wird vom Referenz-Check gefangen, nicht von dir

## Fallstricke

- **Skalieren vor dem Orakel.** Ein Schwarm ohne Prüfung produziert nur Volumen — Phil funktionierte, weil Word immer der Richter war.
- **Diffs reviewen.** Skaliert nicht über ~2 Agenten hinaus; du wirst zum Engpass und verlierst den Geschwindigkeitsvorteil des Schwarms.
- **Mehrdeutige Ownership.** Zwei Agenten, die ein Modul bearbeiten, erzeugen Merge-Hölle — Ownership-Grenzen sind die Architektur.

## Wissenscheck

1. Warum funktionierte Harveys Schwarm, wo die meisten Multi-Agenten-Versuche kollabieren? *(Eine vertrauenswürdige externe Referenz — echtes Word-Verhalten — machte Korrektheit in Schwarm-Geschwindigkeit maschinell prüfbar.)*
2. Warum steuerten Menschen über Memory und Entscheidungslogs statt über Code-Review? *(1M+ LOC in 3 Wochen übersteigt jede menschliche Lesekapazität; Steuerung passiert auf der Intentions-Ebene.)*
3. Welche Voraussetzung würdest du vor diesem Muster prüfen? *(Ob deine Domäne eine Referenz hat, gegen die sich der Schwarm selbst prüfen kann — falls nicht, baue zuerst das Orakel.)*

## Quellen

- [@gabepereyra](https://x.com/gabepereyra) — Harveys Phil-Bericht: ~30 Agenten, 1M+ LOC, Word-Referenz-Verifikation, Anwaltssimulationen
- [Introducing Devin Bots](https://devin.ai/blog/introducing-devin-bots)
- Verwandt: [Leitfaden 4 — Multi-Bot-Organisation](bots-203-multi-bot-org.md) (gleiche Hierarchie, anderer Zweck: Betrieb vs. Konstruktion)
