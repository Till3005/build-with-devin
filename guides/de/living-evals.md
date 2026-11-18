# Leitfaden 15 — Living Evals aus Produktions-Traces

**Ziel:** eine Eval-Suite für *deinen* Agenten, die sich selbst schreibt — ein geplantes Devin, das echte Produktionsgespräche liest, jeden Fehlschlag in einer vollen Kopie deines Systems nachbaut und PRs öffnet, die den Fehlschlag als Regressionstest hinzufügen.
**Level:** fortgeschritten
**Quell-Deployment:** **Rox' Living Evals** — bei Rox schreibt niemand mehr Evals per Hand. Ein wöchentliches Devin liest Produktions-Traces in Braintrust, baut jeden Fehlschlag in einer mit synthetischen Daten geimpften Vollkopie von Rox nach, replayed, bis der Agent denselben Fehler macht, und öffnet einen PR. Die Suite deckt **72 % der echten Nutzung vs. 43–57 %** ihrer handgeschriebenen Evals ab und wächst Woche für Woche weiter.
**Quellen:** [Living-Evals-Write-up](https://www.rox.com/articles/living-evals-an-eval-suite-that-grows-from-production) (Brian Xu, Okt 2026) · [Launch-Thread](https://x.com/rox_ai/status/2110779380666617997)

## Das Muster

```text
Produktions-Traces (Observability-Plattform)
        │  wöchentliche Stichprobe (~350 Gespräche)
        ▼
zu Verhaltensweisen gruppieren (goal · output · mutation · target)
        │  hunderte Gespräche → ~130 Verhaltensweisen
        ▼
für jede unterversorgte Verhaltensweise:
   Daten synthetisieren → Vollkopie-Preview-Env → Request replayen
   → gegen Produktions-Trace vergleichen → als Eval einfrieren → PR öffnen
        ▼
Mensch reviewt den PR, nicht das Eval-Schreiben
```

## Voraussetzungen

- Ein Agent oder AI-Feature in Produktion, mit **Tracing auf Gesprächsebene** (Rox nutzte Braintrust; LangSmith/Self-hosted-Logging funktioniert — du brauchst den Request + die Records + die berührten Tool Calls)
- Eine deploybare Kopie deines Systems (Preview-Env, Staging oder `docker compose up` in einer VM) — **keine Mocks**
- Tests-as-Code in deinem Repo, damit ein Eval nur eine committete Datei ist

## Schritt 1 — Einen Trace per Hand replaybar machen

Vor jedem Scheduling: wähl ein echtes Gespräch, in dem dein Agent scheiterte. Lass Devin den Trace ziehen, synthetische Daten schreiben, die exakt abdecken, was der Request berührte, deine Systemkopie hochfahren und den Request replayen, bis derselbe Fehlschlag auftritt. Kannst du einen Fehlschlag nicht manuell reproduzieren, produziert der Wochen-Loop nichts.

## Schritt 2 — Als Eval einfrieren, nicht als Bug-Report

Das Artefakt ist ein committetes Eval, keine Slack-Nachricht. Rox' Konvention: Der Request wird **wortwörtlich** aus der Produktion kopiert; die geimpften Daten reproduzieren die exakten Bedingungen (z. B. "das neueste Meeting hat kein Transkript"). Daten-ändernde Requests bekommen eine Code-Assertion; reine Antwort-Requests bekommen eine LLM-Judge-Rubric.

## Schritt 3 — Vor dem Skalieren nach Verhalten gruppieren

Den Loop auf jedes Gespräch zu fahren ist Verschwendung — die meisten Requests wiederholen dieselben Formen. Rox' vier Labels definieren eine *Verhaltensweise*: **goal** (was der Nutzer will) · **output** (was zurückkommt) · **mutation** (nichts/erstellen/bearbeiten/senden) · **target** (benanntes vs. inferiertes Objekt). ~350 Gespräche pro Woche kollabieren zu ~130 Verhaltensweisen; baue Evals nur für unterversorgte.

## Schritt 4 — Die ganze Prozedur als Skill encodieren

Der Trace→Eval-Loop lebt in **einer Skill-Datei**, der Devin folgt: Trace ziehen → synthetisieren → Preview-Env → replayen → vergleichen → einfrieren → PR. Produziert der Loop ein schlechtes Eval, **fixe den Skill**, patche nie das Eval per Hand — das ist der Zug, der sich akkumuliert.

## Schritt 5 — Wöchentlich schedulen

Cron-Automation (Leitfaden 6): Traces der Woche ziehen → gruppieren → für jede unterversorgte Verhaltensweise den Loop fahren → einen PR mit den neuen Evals öffnen. Menschen reviewen den PR; Devin besitzt die Suite.

## Verifizieren

- [ ] Ein echter Produktionsfehlschlag replayed deterministisch in deiner Preview-Env — gleicher User-Request, gleiches schlechtes Ergebnis
- [ ] Die Eval-Datei ist in deinem Repo, läuft in CI und schlägt im alten Verhalten fehl / besteht mit dem Fix
- [ ] Coverage wird gegen den *echten Traffic-Mix* gemessen, nicht deine Vermutungen — melde sie wie Rox' 72 %
- [ ] Ein schlechtes Eval wurde durch Editieren des Skills gefixt, nicht des Evals

## Fallstricke

- **Gemocktes Replay.** Rox' früherer Ansatz replayed durch eine gemockte Datenschicht — Mocks können Bugs genau in dem Code verstecken, den sie ersetzen. Nutze eine Vollkopie; der Sinn einer Preview-Env ist Fidelity.
- **Flaky Judging.** Selbst ohne Code-Änderung besteht ~1 von 8 Evals manche Runs und fällt in anderen — Agents sind nicht deterministisch. Lies einen Fehlschlag, bevor du ihm traust; alarmiere nicht bei Einzel-Flakes.
- **Evals, die Geschmack messen.** Die Suite fängt verhaltensbezogene Regressionen (ein toter Tool-Pfad, ein unterstützter Request unhandled), nicht Stil — jeder Fehlschlag sollte auf einen fixbaren Defekt zeigen.

## Wissenscheck

1. Warum in einer Vollkopie replayen statt in einer gemockten Datenschicht? *(Mocks können Bugs in dem Code verstecken, den sie ersetzen — je mehr State der Agent editiert, desto mehr wird der Mock zu dem, was du eigentlich testest.)*
2. Warum Gespräche zu Verhaltensweisen gruppieren, bevor man Evals schreibt? *(Die meisten Requests wiederholen Formen — goal/output/mutation/target zu labeln lässt ein Eval viele Gespräche abdecken, so mappt Coverage auf echte Nutzung.)*
3. Was ist der akkumulierende Zug: Evals fixen oder den Skill fixen? *(Den Skill — ein handgepatchtes Eval lehrt Devin nichts; ein gefixter Skill produziert für immer bessere Evals.)*

## Quellen

- [Living Evals: an eval suite that grows from production](https://www.rox.com/articles/living-evals-an-eval-suite-that-grows-from-production) — die volle Methodik
- [Rox-Launch-Thread](https://x.com/rox_ai/status/2110779380666617997)
- Verwandt: [Leitfaden 13 — Offizielles Kochbuch](official-cookbook.md) · [Leitfaden 6 — Automations](automations-101-event-driven.md)
