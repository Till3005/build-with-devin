# Leitfaden 7 — Enterprise-Rollout-Muster

**Ziel:** Devin auf Org-Ebene ausrollen mit den Formen, die bereits veröffentlichte Zahlen produziert haben — nicht Experimentieren, die bewährten Bewegungen.
**Level:** mittel (für Eng-Leads geschrieben)
**Quelle:** veröffentlichte Kunden-Cases, [devin.ai/customers](https://devin.ai/customers)

Sechs Deployment-Formen, destilliert aus den Firmen, die Ergebnisse veröffentlicht haben. Die meisten erfolgreichen Rollouts nutzen zwei oder drei davon, nicht alle sechs.

## Form 1 — Die Legacy-Migrationsmaschine (Nubank, Comarch)

| | |
| --- | --- |
| Deployment | Nubank: mehrere Millionen Zeilen, 8 Jahre alter ETL-Monolith → Sub-Module. Comarch: 20 Jahre, 10M-Zeilen-ERP-Neuaufbau |
| Ergebnis | 8–12× Engineering-Effizienz, 20× Kostenersparnis (Nubank) |
| Mechanismus | Devin auf *deinem* Codebase fine-tunen (Nubank senkte ~40 Min/Aufgabe auf ~10), dann als kontinuierliches Programm auf die Migration richten — kleine getrackte PRs, kein Rewrite |

**Wie kopieren:** ein begrenztes Legacy-System wählen; fine-tunen oder per Playbook lehren; Migration-Engineer-artigen Loop fahren — eine große Migration als kleine getrackte PRs mit Fortschrittsfläche. Der Gewinn akkumuliert: Jedes migrierte Modul macht die nächste Session klüger.

## Form 2 — Das Primary-Author-Repo (EBANX, Gumroad, Finch)

| | |
| --- | --- |
| Deployment | EBANX: **92 % der gemergten PRs Devin-verfasst**. Gumroad: Devin ist der **#1-Contributor** des Repos (1.500+ PRs). Finch: 3.000 PRs, ~20 Engineer-Monate gespart |
| Mechanismus | Devin ist auf diesen Repos kein Assistent — es ist der Default-Autor. Menschen reviewen und dirigieren |

**Wie kopieren:** ein hochfrequentes Repo wählen; Tickets defaultmäßig an Devin-Sessions routen; Menschen reviewen. Die zu beobachtende Metrik ist der Authored-PR-Anteil — über ~50 % bist du in dieser Form; darunter noch im Pilotmodus.

## Form 3 — Der Always-on-First-Responder (Modal, Reducto, AngelList)

| | |
| --- | --- |
| Deployment | Modal: **80 % der Incidents untersucht, bevor ein Engineer den Thread öffnet**. Reducto: Devin Oncall ist First Responder; Engineers werden selten gepagt. AngelList: Devin findet die Ursache von 70 % der Incidents vor dem Engineer |
| Mechanismus | PagerDuty/Slack-Trigger → Session untersucht mit Logs/Repo-Zugriff → Bericht landet, bevor der Mensch aufwacht |

**Wie kopieren:** [Devin Oncall](https://docs.devin.ai) oder eine PagerDuty-getriggerte Automation (Leitfaden 6, Rezept: Incident → untersuchen). Miss den % der vor-untersuchten Incidents — jeder Punkt davon ist zurückgewonnener menschlicher Schlaf.

## Form 4 — Die Wartungsflotte (Airbyte, Melius)

| | |
| --- | --- |
| Deployment | Airbyte: hält **700+ Connectoren** am Laufen. Melius: ~100 PRs/Tag |
| Mechanismus | Der Long-Tail, den niemand will — Connector-Fäulnis, Dependency-Drift, veraltete Flags — an Bots/Automations geroutet, die ihn kontinuierlich abarbeiten |

**Wie kopieren:** dein Wartungs-Backlog enumerieren (die Arbeit, die Engineers vermeiden); in Code-Health-Engineer-/Code-Reaper-artige Bots (offizielle Templates) mit wöchentlicher Kadenz verpacken.

## Form 5 — Der Org-weite Seat (Wayfair, The Access Group, Citi)

| | |
| --- | --- |
| Deployment | Wayfair: 1.600+ Engineers all-in. Access Group: Devin über 250 Produkte, 2.000+ Engineers → 5× Output. Citi: 40.000-Dev-Rollout, 30 % Tech-Vendor-Ausgaben gekürzt |
| Mechanismus | Nicht mehr Agenten — der *Seat*: Jeder Engineer hat Devin-Zugriff, geteilte Playbooks, Knowledge auf Org-Ebene |

**Wie kopieren:** die Rollout-Reihenfolge in den veröffentlichten Cases ist konsistent — Pilot-Team → gemessene Ergebnisse → Playbook-/Knowledge-Standardisierung → Seat-Expansion. Das Überspringen des Knowledge-Schritts ist, warum Seat-Rollouts stecken bleiben: siehe [Playbooks-Leitfaden](playbooks-and-knowledge.md).

## Form 6 — Das Prozess-Gate (Hamming, Litera, Eight Sleep)

| | |
| --- | --- |
| Deployment | Hamming: Devin schreibt 25 % des Code-Volumens. Litera: Regressionszyklen um 90 % gekürzt. Eight Sleep: 8× mehr geliefert |
| Mechanismus | Devin besitzt eine Pipeline-Stufe — Regressionstests, QA — nicht das ganze Produkt |

**Wie kopieren:** die Pipeline-Stufe mit den schlechtesten menschlichen Kosten finden (Regressionszyklen, QA); einem Bot oder einer Automation zuweisen; Zykluszeit der Stufe vorher/nachher messen.

## Anti-Muster, die die Cases implizieren

- **Werkzeug, nicht Kollege.** Die High-Number-Deployments geben Devin Ownership (Repos, Oberflächen, Stufen), nicht Zuweisungen — dieselbe Lektion wie Leitfäden 1–5.
- **Ewiger Pilot.** Alle veröffentlichten Ergebnisse teilen einen Zug: ein gemessener Pilot, der *graduiert* ist. Setze das Graduierungskriterium vorab (PR-Anteil, abgedeckte Incidents, gesparte Stunden).
- **Keine Knowledge-Schicht.** Jedes große Deployment codiert Konventionen irgendwo — Fine-Tunes, Playbooks, Bot-Instructions. Ohne sie variiert die Qualität je nach Session.

## Verifizieren

- [ ] Dein Rollout-Dokument benennt eine Pipeline-Stufe, eine Metrik und ein Graduierungskriterium — vor der ersten Session
- [ ] Woche-2-Checkpoint: Kannst du Devins Merged-PR-Anteil auf dieser Stufe nennen, ohne jemanden zu fragen?

## Fallstricke

- **Den nie graduierten Piloten skalieren.** Jede große Zahl hier kam nach einem gemessenen Piloten mit Exit-Kriterium.
- **Lizenz-zuerst-Denken.** Seats kaufen, bevor die besessene Stufe benannt ist, produziert Shelfware — das Muster ist Stufe → Pilot → Metrik → dann Seats.

## Wissenscheck

1. Warum teilen alle sechs Deployment-Formen "eine besessene Stufe" als Atom? *(Jede veröffentlichte Zahl kam von einer begrenzten, messbaren Oberfläche — Orgs, die "überall" deployten, veröffentlichten nichts.)*
2. Was ist das Graduierungskriterium und warum vor dem Piloten setzen? *(Eine Metrik + Schwelle, die Pilot → Produktion kippt; ohne sie driften Piloten ewig oder werden aus dem Bauch heraus getötet.)*
3. Warum erscheint die Knowledge-Schicht in jedem großen Deployment? *(Konsistenz auf Skala braucht geteilten Kontext — die Alternative sind N Sessions unterschiedlicher Qualität.)*

## Quellen

- [devin.ai/customers](https://devin.ai/customers) — alle zitierten Cases und Zahlen
- [built-with-devin — Enterprise-Index](https://github.com/Till3005/built-with-devin#enterprise-deployments) — die verifizierte Case-Tabelle des Registries
