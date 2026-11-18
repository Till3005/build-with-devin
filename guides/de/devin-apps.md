# Leitfaden 10 — Devin Apps: Live-Tools aus einem Chat

**Ziel:** ein internes Tool, Dashboard oder eine Staging-Kopie beschreiben — Devin baut es und serviert es unter einer stabilen URL, die dein Team per Sign-in öffnet.
**Level:** hier beginnen (Plattform-Leitfaden) · **Zeit:** ~10 Minuten bis zur ersten App
**Quelle:** [Introducing Devin Apps](https://devin.ai/blog/devin-apps) (13. Nov 2026)

## Was es ist

Eine Devin App ist eine live, private Webanwendung, die direkt auf Devins Cloud-Maschine gehostet wird. Du beschreibst das Tool, Devin baut es, dein Team öffnet es über einen Link — kein Hosting, keine Deploy-Pipeline. Weil sie *auf* Devins Maschine läuft, erreicht sie deine MCPs, Integrationen, Codebase und ihre eigene Datenbank (SQLite/Postgres auf derselben Box) und ruft die Devin-API selbst auf.

## Eine bauen

1. Sidebar → **Apps** → beschreiben, was die App tun soll (oder ein Prompt-Template wählen: Metrik-Dashboard, Projektstatus, Review-Queue) → **Build with Devin**
2. Devin stellt Klärungsfragen in der Session, baut und stellt online — die Apps-Seite zeigt die URL, Status `Building` bis v1 live ist
3. **Share** — Link kopieren; auf benannte Personen, deine Org oder dein Enterprise begrenzen. Apps sind nie öffentlich; das Öffnen erfordert einen Devin-Sign-in

Du kannst auch "publish this as an App" in jeder Session sagen, die ein Browser-Preview erzeugt hat.

## Update-Loop

- **Edit in session** auf der Seite der App → die Änderung beschreiben → Devin baut eine neue Version unter derselben URL. Jedes Update ist ein versioniertes Deployment; startet eine neue Version nicht, serviert die vorherige weiter.
- **Automation-frisch gehalten:** eine Automation (Leitfaden 6) verdrahten, um im Zeitplan oder bei Branch-Änderungen neu zu deployen — ein Dashboard, das jeden Morgen frische Daten zieht, ist der kanonische Einsatz.

## Wie sie laufen (die Teile, die zählen)

- **Hibernation:** Apps bauen auf Memory-Snapshots — die Maschine schläft bei Nichtnutzung, wacht beim Öffnen (erster Load kann ein paar Sekunden dauern). Die Abrechnung folgt der Wachzeit.
- **Stack:** alles, was HTTP auf einem Port serviert; DB auf derselben Maschine.
- **Skalierungsgrenze:** eine Maschine — super für interne Tools und Dashboards, **nicht** für hochfrequentierte Produktionsservices.

## Die drei bewährten Einsätze

| Einsatz | Beispiel |
| --- | --- |
| Interne Tools | Admin-Panels, Anfrageformulare, Approval-Queues — die Killer der geteilten Spreadsheet |
| Dashboards | Metrik-/Support-/Sales-Boards aus deinen Datenquellen, im Zeitplan aktualisiert |
| Beta-/Staging-Kopien | Dein echter Stack (Frontend+Backend+DB+Worker) auf Devins Maschine — Teamkollegen öffnen eine Staging-Kopie per Link |

## Verifizieren

- [ ] App lädt unter ihrer stabilen URL, nachdem die Maschine geschlafen hat (ein paar Sekunden Cold Start erwarten)
- [ ] Eine Edit-in-session-Änderung erzeugte eine neue Version unter derselben URL
- [ ] Der Share-Scope stimmt: ein Kollege ohne Zugriff wird am Sign-in gestoppt

## Fallstricke

- **Produktionstraffic.** Eine Maschine, schläft im Leerlauf — zeige nicht Nutzer darauf; zeige dein Team darauf.
- **Statisches Denken.** Die Kraft einer App ist, dass sie *in Devins Umgebung lebt* — verdrahte sie mit deinen Daten/MCPs, oder du hast eine schwächere Vercel gebaut.

## Wissenscheck

1. Was ist der Unterschied zwischen einer Devin App und einem PR-Preview? *(Die App wird live von Devins Maschine unter einer stabilen URL serviert — stateful, persistent, Sign-in-gated — kein Build-Artefakt.)*
2. Warum zählt "dein Team öffnet sie per Sign-in" für interne Tools? *(Auth wird von der Org geerbt — kein separates Login-System zu bauen oder abzusichern.)*
3. Welche Klasse interner Tools passt am besten zu Apps? *(Dashboards und Staging-Oberflächen, wo "gut genug jetzt" "perfekt später" schlägt — die Wartungskosten sind nahe null.)*

## Quellen

- [Introducing Devin Apps](https://devin.ai/blog/devin-apps)
- Verwandt: [Leitfaden 6 — Event-getriebene Automations](automations-101-event-driven.md) für geplantes Refresh
