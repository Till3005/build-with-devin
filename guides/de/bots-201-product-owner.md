# Leitfaden 2 — Product-owner-Bot

**Ziel:** ein Bot, der eine komplette App-Oberfläche product-managet — stellt eigene Tickets, baut sie, mergt und berichtet täglich.
**Level:** mittel · **Menschliche Last nach Setup:** ~1 Nachricht pro 6 gemergten PRs
**Quell-Deployment:** Cognitions **Android Bot** — hat die Devin-Android-App in **44 Tagen** in die Google-Play-Open-Beta gebracht: 1.134 gemergte PRs, 344.651 Zeilen Kotlin, 2.841 Screenshot-Tests, 1.217 Tickets. Sein Mensch schickte **183 Nachrichten insgesamt** (22 Tage Schweigen), und **88 % der PRs wurden selbst gemergt**. Er besitzt jetzt die Feature-Parität Android/iOS.
**Quellen:** [Launch-Post](https://devin.ai/blog/introducing-devin-bots) · [Fortune](https://fortune.com/2026/11/17/exclusive-cognition-bets-on-devin-bots-coding-agents-in-challenge-to-anthropics-duet-and-openais-dots/) · Russell Kaplans Dogfooding-Notizen

## Das Muster

Ein Bot besitzt eine *Oberfläche* — eine App, eine Website, einen Service — so wie ein PM sie besitzt: Er entscheidet, was gebaut wird, macht daraus Tickets, führt eine Session pro Ticket aus und hält die Oberfläche auf unbestimmte Zeit lebendig. Der Mensch agiert als die Führungskraft, an die er berichtet.

```text
Bot ──► stellt Tickets ──► Session pro Ticket ──► PR ──► CI + Devin Review ──► Merge
 │                                                                             │
 └──────────── Tagesbericht + Needs-you-Entscheidungen ◄──────────────────────┘
```

## Voraussetzungen

- Ein Repository, das der Bot vollständig besitzen kann (App-Repo mit CI, Review und Merge-Pfad)
- Devin Review auf dem Repo aktiviert und CI-Checks verdrahtet
- Eine Slack-App für den Bot (empfohlen — jedes dokumentierte Deployment berichtet in Slack)

## Schritt 1 — Der Outcome-Prompt

Der echte, wörtlich von Cognition:

```text
your job is to product manage the android app. Basically, you're going to
autonomously create the entire thing, but we need to figure out what the
blockers are for you doing that first.
```

Rekonstruiertes Template für deine Oberfläche:

```text
Your job is to product manage <surface>. You're going to autonomously
<build / keep parity with <reference>>, but first enumerate the blockers
to you doing that — where the code lives, how to build and test it, and
how changes merge — then start working through them.
```

Beachte die Form: **Ownership + Autonomie + Blocker zuerst**. Gib ihm kein Backlog; gib ihm ein Mandat und lass ihn ans Licht bringen, was er braucht.

## Schritt 2 — Phase eins: entsperren, nicht bauen

Der Android Bot hat nicht zuerst Code geschrieben — er hat Blocker enumeriert: Repo-Zugriff, Build-Befehle, wie man auf Gerät/Emulator testet, den Merge-Pfad. Deine Version dieser Liste:

- Kann er das Projekt auf seiner Maschine bauen? (Blueprint-/Snapshot-Abhängigkeiten)
- Kann er installierbare Artefakte erzeugen (APK/TestFlight/Preview-Deploy)?
- Kennt er die Merge-Policy — welche Checks bestehen müssen, wer reviewt?
- Hat er die nötigen Credentials (Store-Keys, Signing) — oder eine dokumentierte Grant-Anfrage dafür?

Lass ihn dieses Audit beenden, bevor er Produkt-Tickets anlegt. Jeder hier gelöste Blocker ist eine festgefahrene Session, die du später nie siehst.

## Schritt 3 — Der Arbeits-Loop

Einmal entsperrt, ist der stationäre Zustand:

1. Der Bot legt ein Ticket für die nächste Arbeitseinheit an, die er entscheidet
2. Eine Child-Session implementiert sie und öffnet einen PR — klein, mit Beweis, dass es funktioniert
3. CI + Devin Review gaten den Merge
4. Der Bot mergt (oder fragt dich, wenn Urteil nötig ist — landet in Needs you)
5. Tagesbericht landet in Slack — die Berichte des Android Bot enthalten eine **Bildschirmaufnahme** dessen, was sich geändert hat

Richte das Reporting in den Instructions des Bots ein, nicht im Chat:

```text
Every day, post a report in #<channel>: what shipped, what's in flight,
what needs a human. Include a screen recording of visible changes.
```

## Schritt 4 — Deine Rolle als Führungskraft

Die 183 Nachrichten über 44 Tage fielen in zwei Kategorien:

- **Urteilsaufrufe** — Security-Review-Freigabe, ein Design-Trade-off, eine Approval-Card
- **Richtung** — "be more ambitious" ist das dokumentierte Beispiel

Alles andere — Tickets, Implementierung, Fixes, Self-Merges — ist Aufgabe des Bots. Wenn du Implementierungsfragen beantwortest, managst du zu tief. Einmal korrigieren → landet im Memory → nächste Session erbt es.

## Stationärer Zustand

Nach dem initialen Build wechselt derselbe Bot zum *Besitzen* der Oberfläche:

- Hält Parität mit einem Referenzprojekt (der Android Bot trackt jetzt iOS-Features)
- Triagiert eingehende Meldungen (er bearbeitet Google-Play-Beta-Feedback)
- Fängt Cross-Surface-Regressionen — der Android Bot fand und fixte autonom einen iOS-/Web-Bruch, der durch die Änderung eines anderen verursacht wurde

## Verifizieren

- [ ] Die erste Amtshandlung des Bots war ein Blocker-Audit, kein PR
- [ ] Er legt an und arbeitet seine eigene Ticket-Queue ab, ohne gefragt zu werden
- [ ] PRs sind klein und tragen Beweise (Tests, Screenshots, Aufnahmen)
- [ ] Tagesbericht postet mit sichtbarer Evidenz in Slack
- [ ] Du hast einen ganzen Tag null Nachrichten geschickt und PRs wurden trotzdem gemergt

## Fallstricke

- **Die Blocker-Phase überspringen.** Ein Product-owner-Bot, der codet, bevor er bauen/testen/mergen kann, produziert verwaiste PRs.
- **Große PRs.** Die Sicherheit des Deployments kommt von kleinen, verifizierbaren Einheiten. Wenn PRs anschwellen, instruiere: *"one ticket, one concern, one PR."*
- **Code reviewen statt Richtung geben.** Bei 30+ PRs/Woche kannst du nicht jeden Diff reviewen — gate über CI + Devin Review + die Evidenz des Bots, und investiere deine Nachrichten in Richtung.

## Wissenscheck

1. Der Android Bot mergte 88 % seiner eigenen PRs — was machte Self-Merge sicher genug? *(Verifikation existierte: 2.841 Screenshot-Tests plus Review-Gates; Ownership funktionierte, weil "fertig" maschinell prüfbar war.)*
2. Warum Tickets anlegen statt einfach Sessions zu starten? *(Tickets erzeugen eine auditierbare Queue, die der Bot nach Priorität triagiert — und der Mensch reviewt eine Queue, nicht 50 Sessions.)*
3. Was sagen "22 Tage Schweigen" über das Kontrollmodell? *(Eskalation-nach-Ausnahme funktioniert nur, wenn die Definition-of-done des Bots verifizierbar ist; Schweigen ist das Feature, nicht Vernachlässigung.)*

## Quellen

- [Introducing Devin Bots](https://devin.ai/blog/introducing-devin-bots) — Android-Bot-Zahlen und Prompt
- [Fortune-Exklusiv](https://fortune.com/2026/11/17/exclusive-cognition-bets-on-devin-bots-coding-agents-in-challenge-to-anthropics-duet-and-openais-dots/) — 183 Nachrichten, 88 % Self-Merge, Dogfooding-Notizen
- Verwandt: [Leitfaden 4 — Multi-Bot-Organisation](bots-203-multi-bot-org.md), wenn eine Oberfläche zum Geschäft wird
