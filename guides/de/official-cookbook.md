# Leitfaden 13 — Das offizielle Use-Case-Kochbuch

**Ziel:** die bewährten Nutzungsmuster aus Cognitions eigener Doku, als Kochbuch organisiert — was für Devin zu schneiden ist, und 40+ dokumentierte Rezepte mit Prompts zum Kopieren.
**Level:** für die Breite hier beginnen
**Quellen:** [Best Practices](https://docs.devin.ai/use-cases/best-practices.md) · [Use-case gallery](https://docs.devin.ai/use-cases/gallery/index.md) · [use-case tutorials](https://docs.devin.ai/use-cases/index.md)

## Die eine Regel hinter allem

Offizielle Anleitung, wörtliche Logik: Wähle Arbeit, die **wide & shallow** ist — ein großer Backlog einfacher, horizontal skalierbarer Aufgaben schlägt komplexe Net-new-Builds, jedes Mal.

| Ideale Aufgabe | Anti-Aufgabe |
| --- | --- |
| Repetitive Subtasks auf Junior-Engineer-Komplexität | Net-new komplexe Features |
| < 90 Minuten manuelle Arbeit pro Slice | Alles Unteilbare |
| Objektive Pass/Fail-Verifikation | "Sieht für mich richtig aus" |
| Isoliert, rückwärtskompatibel, parallelisierbar | Verzahnte Abhängigkeiten |

Vier großartige Slice-Formen aus der Doku: **Migrationen, Refactors, Modernisierungen, Tech-Debt-Backlogs.**

## Der Rezeptkatalog

Alles unten ist ein dokumentierter Use Case in der offiziellen Galerie — jedes kommt mit einem Copy-Paste-Prompt. Organisiert nach der Arbeit, die es einem Menschen aus der Woche nimmt.

### Incidents & Produktions-Gesundheit

| Rezept | Mechanismus |
| --- | --- |
| Datadog/PagerDuty-Alerts auto-investigieren | Webhook/API-Trigger → Session untersucht im Feuer |
| Postmortems auto-generieren | PagerDuty resolve → Devin entwirft Timeline, Root Cause, Action Items |
| Tägliche Sentry-Error-Fixes | Nächtlicher Cron zieht neue Fehler → Fix-PRs bis morgens |
| Einen Bug-Report end-to-end debuggen | Gib Devin den Report + Datadog-Logs + DB-Zugang → Root Cause |

### Geplante Hygiene (die höchste-ROI-Seite der Doku)

| Rezept | Kadenz |
| --- | --- |
| Wöchentliche Dependency-Update-PRs | Wöchentlich: veraltete Pakete → getestete Upgrade-PRs |
| Nächtliches E2E auf Staging | Nächtlich: Suite laufen lassen, Tickets für Fehler anlegen |
| Wöchentlicher Changelog aus gemergten PRs | Freitag: kategorisierter Changelog → Slack |
| Täglicher Datadog-Health-Digest | Täglich: Error-Scan → Slack-Digest |
| Tägliches Design-System-Audit | Täglich: hardcodierte Farben/fehlende Tokens in gemergten PRs markieren |
| Feature-Flag-Cleanup | Einmal-Session entfernt Flag + Dead Code nach Release |
| Wöchentlicher Notion-Status-Digest | Wöchentlich: PR/Commit-Zusammenfassung → Notion |
| PRs aus Meeting-Transkripten | Stündlich: Granola pollen → Eng-Tasks extrahieren → Child-Sessions |

### Code-Qualität

| Rezept | Mechanismus |
| --- | --- |
| PR-Bugs vor dem Merge auto-fixen | Devin reviewt jeden PR, pusht Fixes auf den Branch |
| Unit-Tests zu einem Service hinzufügen | Einen Test-Schreib-Skill bauen, auf Charge-Flows/Refunds/Webhooks anwenden |
| Visuelle Regressionen fangen | Repo-Skill: Screenshot jeder betroffenen Seite vor dem PR |
| Migrations-Checklist auf jedem PR | Repo-Skill fängt destruktive Ops, validiert Schema-Änderungen |
| Einen monolithischen Router aufteilen | 2.000-Zeilen-Express-Router → Domain-Routen mit Shared Middleware |
| Code-Coverage erhöhen | Devin analysiert die Suite, schreibt Tests für die Lücken |
| Bekannte CVEs repo-übergreifend patchen | Offizielle Skills ([devin-vuln-fixes](https://github.com/cognitionai/devin-vuln-fixes)): Read-only-Inventar → Approval-Gate → Confirmed-Target-Patch → Vorher/Nachher-Tests → ein PR pro Repo |

### Migrationen & Feature-Arbeit

| Rezept | Mechanismus |
| --- | --- |
| 50-Datei-REST→GraphQL | Scope → konfliktfreie Pakete → parallel (Leitfaden 11) |
| React-18→19-Upgrade-Skill | Den offiziellen Upgrade-Guide in einen phasenweisen Skill für deine Codebase verwandeln |
| OpenAPI-Spec → Implementierung | YAML-Spec → Express-Handler + Zod-Validierung + Supertest |
| Stripe-Checkout-Flow | Spec → funktionierender Flow + Tests + Browser-Verifikation |
| i18n einer Next.js-App | next-i18next install, String-Extraktion, 3-sprachiger Browser-Check |
| Figma → pixel-perfect | Figma-MCP → Komponenten aus Mockups |
| Eine Django-App dockerisieren | Multi-Stage-Dockerfile + Compose für Django/Postgres/Redis |

### Projektmanagement & Daten

| Rezept | Mechanismus |
| --- | --- |
| Bugs via Linear auto-triagen | Label applied → Devin untersucht |
| PRDs → Sprint-Tickets | Notion-PRD → gescopte Linear-Tickets |
| Backlog-Implementierungspläne | Linear-Tickets multi-selecten → Confidence-scored Pläne |
| `/dana`-Datenabfragen in Slack | Plain-English-Datenbankabfragen aus jedem Channel |
| Custom-API-Usage-Dashboard | Devin baut ein maßgeschneidertes Dashboard auf der v3-API |

### Besser werden in Devin selbst ("Devin Optimization")

| Rezept | Lektion |
| --- | --- |
| Einen Feature-Prompt 42→12 ACUs kürzen | Autopsie einer teuren Session: 3 Root Causes → Prompt neu schreiben |
| 3 Sessions auf ein Problem hetzen | Parallele Sessions versuchen konkurrierende Optimierungsstrategien; die beste gewinnt |
| 8 parallele Sessions über Nacht | 8 ungetestete Module → Unit-Test-PRs bis morgens |
| 30 Libraries evaluieren | Eine Session pro Library → gescorter, gerankter Vergleich |
| Einen Hotfix in einen Skill verwandeln | Eine erfolgreiche Incident-Session in einen wiederverwendbaren Skill extrahieren |
| Wöchentlicher Knowledge-Dedup | Geplante Session merged/bereinigt Knowledge-Vorschläge |
| Team-Onboarding-Guide | Devin liest seine eigene Doku → ein Getting-Started-Guide für deinen Stack |

## Wie man dieses Kochbuch benutzt

1. Wähle ein Rezept aus **Geplante Hygiene** — es ist der billigste erste Sieg (ein Nächtlich-/Wöchentlich-Loop, über den du nicht mehr nachdenkst)
2. Füge eines aus **Incidents** hinzu, wenn du PagerDuty/Datadog/Sentry hast
3. Wenn ein Rezept funktioniert, friere es als **Skill** (Leitfaden 12) oder **Bot** (Leitfäden 1–5) ein — jede Zeile oben überlebt als eines davon

## Verifizieren

- [ ] Ein Hygiene-Rezept läuft im Zeitplan und hat seinen ersten PR/Bericht produziert
- [ ] Sein Output ist als Skill, Playbook oder Bot eingefroren — lebt nicht in jemandes Kopf

## Fallstricke

- **Zehn Rezepte, null eingefroren.** Ein Rezept, das ein manueller Prompt bleibt, ist bis Freitag vergessen — operationalisieren oder streichen.
- **Copy-Paste-Prompts ohne die Verifikation deines Repos.** Die Galerie-Prompts setzen eine Test-Suite voraus; passe den *Check* an, nicht nur die Aufgabe.

## Wissenscheck

1. Warum mit einem Hygiene-Rezept statt Incident Response beginnen? *(Der billigst mögliche Sieg — läuft, während du schläfst, und ein falscher nächtlicher Lint-Fix ist behebbar; eine falsche Incident-Aktion nicht.)*
2. Was verhindert "ein Rezept als Skill oder Bot einfrieren" wirklich? *(Prompt-Drift und Einzelpersonen-Abhängigkeit — das Rezept überlebt die Person, die es schrieb.)*
3. Warum den Verifikationsteil eines Galerie-Prompts vor dem Aufgabenteil anpassen? *(Die Aufgabe beschreibt Absicht; der Check ist, was dein Repo tatsächlich beweisen kann — falsche Checks produzieren selbstbewussten Müll.)*

## Quellen

- [Use-case gallery](https://docs.devin.ai/use-cases/gallery/index.md) — alle Rezepte oben, jeweils mit Copy-Paste-Prompts
- [Best Practices](https://docs.devin.ai/use-cases/best-practices.md) — die Slicing-Doktrin
- [Use-case tutorials](https://docs.devin.ai/use-cases/index.md) — API-Integration, Code-Coverage, Containerisierung, Frontend-Komponenten, MCP
- Verwandt: [Leitfaden 11 — Migrationen auf Skala](migrations-at-scale.md) · [Leitfaden 6 — Automations](automations-101-event-driven.md)
