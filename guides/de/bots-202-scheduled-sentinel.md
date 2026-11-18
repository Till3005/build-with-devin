# Leitfaden 3 — Scheduled-sentinel-Bot

**Ziel:** ein Bot, der eine wiederkehrende Qualitätsprüfung besitzt — läuft sie im Zeitplan, triagiert Fehler, verfolgt sie zur Ursache und liefert Fixes.
**Level:** mittel
**Quell-Deployment:** Cognitions **Layout Bot** — wacht über Layout-Shift-Regressionen in der Devin-Webapp. Alle 3 Stunden baut er das Produktions-`main`, simuliert Erst-/Wiederholungs-/verzögerte Requests und liefert Fixes. **159 PRs in 3 Wochen; Lag −70 %.**
**Quellen:** [Launch-Post](https://devin.ai/blog/introducing-devin-bots) · [Automations-Doku](https://docs.devin.ai/product-guides/automations)

## Das Muster

Manche Arbeit ist nie fertig — sie kehrt im Takt wieder: Performance-Budgets, visuelle Regression, Frische der Dependencies, Secret-Scans, Uptime. Ein Sentinel-Bot besitzt *die Prüfung selbst*, nicht nur die Fixes: Er hält die Prüfung am Laufen, während sich der Code ändert, filtert Rauschen und öffnet einen Fix nur, wenn die Regression echt ist.

```text
cron ──► Bot wacht ──► führt Prüfung unter realistischen Bedingungen aus
                              │
                pass ─────────┴──────── fail
                 │                          │
               ruhig              erneuter Lauf filtert Flakes
                                            │
                               zurückverfolgt zum einführenden PR
                                            │
                            Fix-PR + Vorher/Nachher-Evidenz
```

## Voraussetzungen

- Eine Prüfung, die auf der Maschine des Bots laufen kann (Build, Testsuite, Lighthouse, Custom-Skript)
- Devin Bot erstellt (Leitfaden 1) oder eine Automation (Leitfaden 6) — beide funktionieren; ein Bot fügt Urteil zwischen den Läufen hinzu

## Schritt 1 — Der Outcome-Prompt

Aus dem dokumentierten Verhalten des Layout Bot rekonstruiert:

```text
Your job is to keep <surface> from <regressing>.

Watch <check/channel>, where <the check> posts every <interval>. Take over
that check and keep it working as the code changes. When something
regresses: rerun to rule out flakiness, trace the regression to the PR
that introduced it, and open a fix PR with before/after evidence.
```

Beispiele für den `<check>`-Slot, alle aus echten Deployments:

- Layout-Shift-Messung über erste/wiederholte/verzögerte Requests (Layout Bot)
- p95-Latenz auf deinen 5 langsamsten Endpunkten (Template Latency Optimizer)
- `npm audit`-/CVE-Sweep (Template Code Health Engineer)
- Dead-Code-Erkennung (Template Code Reaper)

## Schritt 2 — Einplanen

Dem Bot im Chat sagen:

```text
Run this check every 3 hours on a schedule.
```

Der Bot schlägt eine Automation vor; du genehmigst einmal. (Leitfaden 6 behandelt handgebaute Automations, falls du den Cron lieber selbst verdrahtest.) Später unter Settings → Automations des Bots verwalten.

## Schritt 3 — Realistische Bedingungen zählen

Die Prüfung des Layout Bot ist nicht ein Lauf — sie simuliert **Erstbesuch, Wiederholungsbesuch und einzeln verzögerte Requests**, weil die Regression, die er jagt, nur unter bestimmten Lastformen auftritt. Codiere dein Äquivalent:

- Welche Umgebung — der Bot baut Produktions-`main` auf eigener VM, kein Dev-Server
- Welche Inputs — kalter vs. warmer Cache, geseedete Daten, realistische Request-Reihenfolge
- Welcher Schwellenwert — eine Zahl, nicht "fühlt sich langsamer an"

## Schritt 4 — Rauschdisziplin

Zwei Regeln verhindern, dass ein Sentinel Alarm schreit:

1. **Erneut laufen, bevor gehandelt wird** — der Layout Bot lässt flaky aussehende Ergebnisse erneut laufen, bevor er sie als echt behandelt. Schreib es in den Prompt: *"rerun any failed check once before acting on it."*
2. **Verfolgen vor dem Fixen** — jede Regression wird zum einführenden PR zurückverfolgt. Ein Fix ohne Ursache ist eine Vermutung.

## Schritt 5 — Evidenz in jedem Fix

Jeder der 159 PRs trägt **Vorher/Nachher-Video**. Äquivalente Evidenz für deine Prüfung:

| Prüfung | Evidenz im Fix-PR |
| --- | --- |
| Layout/visuell | Bildschirmaufnahme oder Screenshots, vorher vs. nachher |
| Latenz | Zeitmessungen, gleiche Messung in beide Richtungen |
| Dead Code | Warum der Code unerreichbar ist |
| Dependencies/CVEs | Das Advisory + der Diff, der es löst |

## Verifizieren

- [ ] Automation existiert und feuert im gesetzten Cron (Settings → Automations zeigt Läufe)
- [ ] Eine geseedete Regression erzeugt einen Fix-PR mit Vorher/Nachher-Evidenz
- [ ] Ein flaky Lauf erzeugt einen erneuten Lauf, keinen Fix
- [ ] Die Prüfung selbst wird gepflegt — als sich die App darunter änderte, hat der Bot die Prüfung aktualisiert

## Fallstricke

- **Fixes besitzen, aber nicht die Prüfung.** Wenn deine Prüfung bricht und eine Woche niemand merkt, besaß der Bot das Falsche — der Prompt muss die Prüfung selbst zuweisen.
- **Cron ohne Urteil.** Eine schlichte geplante Automation kann die Prüfung ausführen; ein Bot entscheidet, ob ein Fehlschlag echt ist. Nutze schlichte Automation nur für Prüfungen ohne Triage (Leitfaden 6).
- **Nur-Alarm-Output.** Ein Sentinel, der "Regression gefunden" in einen Channel meldet, schafft Arbeit für Menschen. Der Wert des Deployments ist, dass es *fixt* — halte es daran fest.

## Wissenscheck

1. Warum baut der Sentinel Produktions-`main` im Cron statt auf gemeldete Fehler zu warten? *(Das Ergebnis ist "keine Regressionen", nicht "gemeldete Bugs fixen" — Ownership heißt, Probleme vor den Menschen zu finden.)*
2. Der Layout Bot liefert Fixes mit Vorher/Nachher-Videos — welche Entscheidung ermöglicht das dem Reviewer? *(Merge-Vertrauen ohne lokale Reproduktion; der Beweis reist mit dem PR.)*
3. Warum eine Regression zum einführenden PR zurückverfolgen statt das Symptom zu fixen? *(Ownership einer Prüfung heißt Ownership ihrer Geschichte — der Fix landet auf der Ursache und das Wissen bleibt.)*

## Quellen

- [Introducing Devin Bots](https://devin.ai/blog/introducing-devin-bots) — Layout-Bot-Mechanik und Zahlen
- [Automations — Docs](https://docs.devin.ai/product-guides/automations) — Zeitpläne, Trigger, Bedingungen
- Verwandt: [Leitfaden 6 — Event-getriebene Automations](automations-101-event-driven.md) für die Bot-freie Version dieses Loops
