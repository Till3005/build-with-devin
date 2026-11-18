# Leitfaden 6 — Event-getriebene Automations

**Ziel:** externe Events — Slack, Teams, GitHub, Linear, Jira, PagerDuty, Cron, Webhooks — an Devin-Sessions verdrahten, die sich selbst starten.
**Level:** hier beginnen (Plattform-Leitfaden) · **Zeit:** ~20 Minuten
**Quelle:** [Automations-Doku](https://docs.devin.ai/product-guides/automations) · [offizieller Video-Walkthrough](https://www.youtube.com/watch?v=6xxKtIpgOyE)

## Die Anatomie

Jede Automation hat vier Teile:

| Teil | Was er tut |
| --- | --- |
| Trigger | Das Event, das sie auslöst — eine Slack-Nachricht, ein fehlgeschlagener CI-Lauf, ein Cron-Tick, ein HTTP-Webhook |
| Conditions | Optionale Filter — nur Label `bug`, nur dieses Repo, nur Nachrichten mit `/devin` |
| Preflight Check | Optionaler LLM-Filter oder Skript, das *nach* einem Match und vor den Aktionen läuft — kann das Event überspringen oder in Arbeitspakete teilen |
| Action | Was läuft: Session starten, einer bestehenden Session eine Nachricht senden, Triage-Monitor oder E-Mail-Benachrichtigung |

## Trigger-Katalog

| Quelle | Feuert bei | Kanonischer Einsatz |
| --- | --- | --- |
| Slack | Neue Nachricht, Reaktion hinzugefügt, User-Group-Erwähnung | Triage von `#incidents`; 🚨-Reaktion → untersuchen |
| Microsoft Teams | Nachricht, Reaktion | Bug-Reports in dem Thread beantworten, in dem sie gepostet wurden |
| GitHub | Issue, Issue-Kommentar, PR, PR-Review, Check-Run, Push | Fehlschlagenden CI selbst reparieren; `/devin`-Kommentar → Session |
| GitLab | MR, MR-Kommentar, Issue, Push, Pipeline | Fehlschlagende Pipelines fixen |
| Linear | Issue erstellt/gelabelt/Status/Priorität/zugewiesen/verschoben | Tickets implementieren, wenn Devin zugewiesen |
| Jira | Issue erstellt/aktualisiert/gelabelt/Status/zugewiesen/kommentiert | Dasselbe, Jira-förmig |
| Pylon | Issue erstellt/getaggt/Status | Customer-Bug-Triage |
| PagerDuty | Incident ausgelöst/bestätigt/gelöst | Hochdringende Incidents sofort untersuchen |
| Schedule | Cron oder einmalig | Täglicher Sentry-Sweep, wöchentliche Dep-Updates, nächtliche Smoke-Tests |
| Webhook | Jeder HTTP-POST | Alles andere — Datadog, Sentry, deine eigenen Systeme |

Mehrere Trigger an einer Automation wirken als ODER — z. B. feuern bei *entweder* einem GitHub-CI-Fehlschlag *oder* einer Slack-Reaktion.

## Rezept 1 — `/devin` auf jedem Issue

Der meistgenutzte Trigger in freier Wildbahn:

```text
Trigger:   GitHub → issue comment, repo = your/repo
Condition: comment body starts with "/devin"
Action:    Start session — prompt includes the event payload
```

Ergebnis: Jeder im Team kommentiert `/devin investigate this` auf einem Issue, und eine Session nimmt es mit dem ganzen Thread als Kontext auf.

## Rezept 2 — CI-Fehler-Selbstreparatur

```text
Trigger:   GitHub → check run, repo = your/repo
Condition: conclusion = failure
Action:    Start session: "CI check <name> failed on this commit.
            Diagnose the failure from the logs, fix it, and push to
            the same branch."
```

Das Event-Payload trägt den fehlgeschlagenen Check + Commit in die Session — ohne Copy-Paste.

## Rezept 3 — Geplanter Sweep

```text
Trigger:   Schedule → daily 09:00
Action:    Start session: "Sweep yesterday's Sentry issues in
            <project>. File the top 3 by impact as tickets and
            start the most actionable one."
```

Tägliche Hygiene-Loops (Sentry-Sweeps, Dependency-Updates, Smoke-Tests) sind die Automations mit dem höchsten ROI — sie machen aus "jemand sollte prüfen" ein "ist geprüft".

## Aktions-Typen, wie man wählt

| Aktion | Verwenden wenn |
| --- | --- |
| Start session | Der Default — jedes Event bekommt eine frische Maschine und Kontext |
| Message session | Eine langlebige Session hält Zustand — Events hinein füttern (der Samen eines Bots) |
| Triage Devin | Ein persistenter Devin wacht über einen ganzen Slack-Channel und erzeugt Kind-Untersuchungen (siehe Devin Oncall für Incidents) |
| Email notification | Nur informieren, dass es lief |

**Automation vs. Bot:** Automations sind dumme Rohre — Event rein, Session raus. Ein Bot fügt Memory, Urteil und Multi-Session-Planung um dieselben Trigger hinzu. Starte mit Automations; wechsle zu einem Bot, wenn die Arbeit Durchhaltevermögen braucht (Leitfäden 2–5).

## Bauen

Drei Erstellungspfade auf der Automations-Seite:

1. **Create** — der leere Editor: Trigger → Conditions → Action wählen
2. **Template** — die Galerie vorkonfigurierter Automations für gängige Workflows
3. **Generate with Devin** — auf Englisch beschreiben (*"when a CI check fails on my-org/my-repo, have Devin fix it and push to the same branch"*), generierte Config prüfen

Notizen, die Leute beißen:

- Slack-Trigger brauchen Devin im Channel eingeladen **und** dein persönliches Slack in Settings → Connections verbunden
- Private Teams-Channel feuern nur bei @Erwähnung
- Ein GitHub-Trigger muss ein konkretes Repo nennen
- Verwalte Automations deklarativ mit dem **Terraform-Provider**, wenn du viele betreibst

## Verifizieren

- [ ] Feuere den Trigger einmal manuell (kommentiere `/devin test` oder pushe einen fehlschlagenden Commit) und beobachte, wie eine Session mit dem Event-Payload startet
- [ ] Ein nicht-matchendes Event (falsches Label, falscher Channel) tut nichts
- [ ] Der Output der Aktion landet, wo du ihn erwartet hast (PR, Slack-Thread, Ticket)

## Fallstricke

- **Loops.** Eine Automation, deren Output sie selbst erneut auslösen kann (Devin kommentiert einen PR, der Trigger wacht auf "neuer Kommentar"), verbrennt Sessions für immer. Gate über Autor, Label oder Event-Subtyp.
- **Trigger-Stürme.** Ein Webhook, der pro Commit statt pro PR feuert, kann an einem hektischen Tag 50 Sessions erzeugen. Drosseln: eine Automation pro *claimbarer* Arbeitseinheit, nicht pro rohem Event.
- **Kein Approval-Gate.** Auto-Mergen oder Auto-Deployen auf einen Trigger überspringt den menschlichen Kontrollpunkt — behalte das Muster "Session öffnet PR, Mensch mergt" bei, es sei denn, du hast einen gemessenen Grund dagegen.

## Wissenscheck

1. Ein Kollege will, dass Devin "jede GitHub-Benachrichtigung beobachtet" — was bittest du ihn zuerst einzugrenzen? *(Welcher Event-Subtyp tatsächlich umsetzbare Arbeit impliziert — ein Label angewendet, ein Review angefragt — nicht jede Benachrichtigung.)*
2. Warum muss ein nicht-matchendes Event *keine* Session erzeugen statt einer Session, die No-op entscheidet? *(Sessions kosten ACUs; Upstream-Gating ist gratis, Gating in einer Session nicht.)*
3. Wann braucht eine Automation stattdessen einen Bot? *(Wenn die getriggerte Arbeit über die Zeit angesammeltes Urteil braucht — Memory, Prioritäten, ein dauerhaftes Ergebnis.)*

## Quellen

- [Automations — Docs](https://docs.devin.ai/product-guides/automations)
- [Devin Automations QuickStart (Video)](https://www.youtube.com/watch?v=6xxKtIpgOyE)
- Verwandt: [Leitfaden 3 — Scheduled-Sentinel-Bot](bots-202-scheduled-sentinel.md) für Bot-Urteil über einem Cron
