# Leitfaden 9 — Playbooks & Knowledge: Die Konventionen deiner Org codieren

**Ziel:** Devin-Sessions und Bots auf Org-Ebene verlässlich machen, indem du aufschreibst, was deine besten Engineers voraussetzen — als Playbooks (wiederholbare Prozeduren) und Knowledge (permanenter Kontext).
**Level:** mittel · die Schicht, die jedes große veröffentlichte Deployment teilt
**Quellen:** [docs.devin.ai](https://docs.devin.ai) · Deployment-Lektionen aus [Leitfaden 7](enterprise-playbook.md)

## Warum diese Schicht alles entscheidet

Jedes veröffentlichte Enterprise-Ergebnis — Nubanks 8–12×, EBANX' 92 % authored-PRs, Wayfairs 1.600 Seats — ruht auf codierten Konventionen. Ohne sie variiert Devins Output je nach Session: Jede entdeckt deinen Stack, deine Merge-Regeln, deine Test-Gewohnheiten neu. Mit ihnen verhält sich Session Nr. 500 wie dein bester Engineer an seinem besten Tag.

Zwei komplementäre Artefakte:

| Artefakt | Was es ist | Analogie |
| --- | --- | --- |
| Knowledge | Permanenter Kontext, den Devin liest — Repo-Fakten, Konventionen, Umgebungs-Gotchas | Onboarding-Docs |
| Playbook | Eine benannte, wiederholbare Prozedur — Auslöser, Schritte, Akzeptanzkriterien | Ein Runbook, das jeder aufrufen kann |

## Schritt 1 — Deine eigenen Korrekturen schürfen

Das billigste Wissen existiert schon: Scrolle deine letzten 20 Devin-Sessions durch und sammle jede getippte Korrektur — *"we deploy via Cloud Run,"* *"never `git push --force`,"* *"tests need `npm run db:seed` first."* Jede Korrektur ist ein Knowledge-Eintrag mit Beweis, dass sie zählte.

Schürfe außerdem:
- Code-Review-Kommentare, die Menschen auf Devin-PRs wiederholen
- PR-Beschreibungen, die erklären, *warum* eine Änderung so geformt wurde
- Onboarding-Docs — alles, was du einem Neuling sagen würdest

## Schritt 2 — Knowledge-Einträge schreiben, die haften

Gute Einträge sind eine Zeile, imperativisch und abgegrenzt:

```text
- Deploy only via `make deploy-cloudrun` — never run gcloud directly.
- Migrations require a matching rollback file in prisma/rollbacks/.
- The staging seed user is qa+admin@corp.io; never create real-looking users.
```

Schlechte Einträge sind Aufsätze, Wünsche ("write good tests") oder Secrets (nie Credentials in Knowledge — nutze den Secrets-Store).

## Schritt 3 — Playbooks für wiederholbare Arbeit

> **Plattform-Hinweis (Nov 2026):** Playbooks wandern zu **Skills** — Accounts werden nacheinander migriert, neue Accounts bekommen nur Skills (jedes Playbook wird ein Skill mit demselben Org-/Enterprise-Scope). Alles in diesem Schritt gilt wortwörtlich für Skills: ein Skill ist dieselbe benannte, aufrufbare Prozedur.


Ein Playbook paketiert eine Prozedur, sodass jede Session (oder Bot) sie gleich ausführt. Struktur, die funktioniert:

```markdown
# <Verb + Objekt> — z. B. "Cut a release"
## When to use
<die Auslösebedingung>
## Steps
1. <deterministischer Schritt>
2. ...
## Acceptance
<der Pass/Fail-Check>
## Failure modes
- <bekannter Bruch → was tun>
```

Veröffentliche es org-weit, sodass Sessions, Automations und Bots es aufrufen können — das macht aus einer einmalig erfolgreichen Session eine Org-Fähigkeit.

## Schritt 4 — Bots füttern

Bot-**Instructions** (Leitfaden 1) sind die bot-bezogene Version von Knowledge — die Regeln, die bei jedem Session-Start gelesen werden. Stellen-Gesetz gehört dorthin; Org-Gesetz ins Knowledge; Prozeduren in Playbooks. Die Schichtung hält jedes Artefakt klein und aktuell.

## Schritt 5 — Der Korrektur-Loop

Knowledge fault. Der Loop, der es wahr hält:

1. Eine Session/ein Bot macht einen Fehler → du korrigierst im Chat
2. Der Bot schreibt die Korrektur ins Memory (oder du fügst sie dem Knowledge hinzu)
3. Wöchentliches Review: wiederholte Bot-Memory-Einträge ins Org-Knowledge befördern; Einträge löschen, die einen Monat niemand ausgelöst hat

Devin Coach (ein offizielles Bot-Template) existiert genau dafür — es berichtet wöchentlich, wo Devin festhing, und schlägt jedes Mal einen Fix vor: eine Notiz, einen Skill oder eine Setup-Änderung.

## Verifizieren

- [ ] Eine frische Session auf deinem Repo stellt null Fragen, die dein Knowledge schon beantwortet
- [ ] Die letzte Korrektur, die du einem Bot gegeben hast, erscheint in seinen Memory-Dateien
- [ ] Zwei verschiedene Sessions führen dasselbe Playbook aus und produzieren ein gleich geformtes Ergebnis

## Fallstricke

- **Wünsche schreiben.** "Follow best practices" ändert nichts; "run `npm run db:seed` before tests" ändert alles.
- **Set-and-forget.** Veraltetes Knowledge ist schlimmer als keins — Devin folgt ihm selbstbewusst. Monatlich reviewen.
- **Docs duplizieren.** Knowledge sollte enthalten, was Devin *falsch macht* oder *nicht wissen kann* — keine Kopie deines Wikis.

## Wissenscheck

1. Was ist der Unterschied zwischen Playbook und Knowledge? *(Ein Playbook ist eine wiederholbare Prozedur für eine benannte Aufgabe; Knowledge ist permanenter Kontext, den jede Session voraussetzen sollte.)*
2. Warum ist "aufschreiben, was deine besten Engineers voraussetzen" der eigentliche Enterprise-Engpass? *(Agenten-Qualität war nie der Limiter — fehlender Kontext ist es; die Knowledge-Schicht ist, wo Org-Konventionen leben.)*
3. Wann wird eine Konvention zum Playbook statt tribalem Wissen zu bleiben? *(Beim ersten Mal, wenn eine Session sie auf eine Weise falsch macht, die ein geschriebener Schritt verhindert hätte.)*

## Quellen

- [docs.devin.ai](https://docs.devin.ai) — Knowledge, Playbooks, Bot-Instructions/Memory
- Verwandt: [Leitfaden 7 — Enterprise-Rollout-Muster](enterprise-playbook.md) (diese Schicht ist der Schritt, den die meisten Rollouts überspringen)
