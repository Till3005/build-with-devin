# Leitfaden 4 — Multi-Bot-Organisation

**Ziel:** eine Bot-Hierarchie, die eine ganze Geschäftseinheit betreibt — ein Orchestrator, der an Spezialisten-Bots delegiert, ein Mensch, der über einen einzigen Tages-Thread entscheidet.
**Level:** fortgeschritten
**Quell-Deployment:** Jenny Xus **SuperJennyStack** — ~20 Bots betreiben ein Mobile-Game-Studio. ~50 → **1.900 PRs/Woche**, wöchentliche Releases, Studio-Umsatz ×6. Als Community-Template im [Bot-Marketplace](https://devin.ai/bots/templates) veröffentlicht. Der offizielle **Bot-zu-Bot-Grant-Handoff** (QA → Developer → Retest → PM-Report) nutzt dieselbe Mechanik in kleinerem Maßstab.
**Quellen:** Jenny Xus veröffentlichter Stack ([via Launch-Bericht](https://x.com/cognition/status/2122737511684587551)) · [Bots-Doku](https://docs.devin.ai/work-with-devin/bots) · [BotSpeak-Post](https://x.com/xujennyc/status/2123111543105868166)

## Das Muster

Baue nicht einen Bot, der alles macht — baue eine kleine Firma:

```text
                    ┌─────────────┐
              ┌────►│ Orchestrator │◄──── ein Roll-up-Thread
              │     └──────┬──────┘      (4×/Tag, Emoji-Antworten)
              │            │ Grants: Lesen + Nachrichten
     ┌────────┼────────┬───┴─────┬──────────┐
     ▼        ▼        ▼         ▼          ▼
  SuperPM  SuperDev  SuperQA  SuperRelease  SuperSupport
  (das Was)(baut)    (prüft)  (liefert)     (Nutzer)
```

Der Mensch ist der CEO: Der Orchestrator sammelt alle ausstehenden Entscheidungen der untergeordneten Bots in **einen Slack-Thread, 4×/Tag**, beantwortet per Emoji.

## Voraussetzungen

- Leitfaden 1 fertig — du kannst einen Bot erstellen und instruieren
- Slack verbunden — dieses Muster lebt in Slack; der Roll-up-Thread des Orchestrators ist die gesamte UX
- Eine begrenzte Domäne mit trennbaren Aufgaben (ein Produkt, ein Studio, ein Service-Bereich)

## Schritt 1 — Zuerst das Organigramm entwerfen

Jennys veröffentlichter Stack — kopiere die *Form*, nicht die Namen:

| Bot | Besitzt |
| --- | --- |
| Orchestrator (SuperJenny) | Delegation an jeden anderen Bot; kompiliert deren Anliegen in einen Thread; auf ihre Persönlichkeit/Eigenheiten trainiert |
| PM (SuperPM) | Täglich gerankte Fix-Liste aus Metriken + Store-Reviews + Trends |
| Release (SuperRelease) | Wöchentlicher Build, freitags bereit für Store-Einreichung |
| QA (SuperQA) | Tests auf echten Geräten mit Video-Beweis |
| Support (SuperSupport) | Entwirft jede Store-Review-Antwort zur Genehmigung; hilft Spielern über Nacht |

Die übrigen ~15 Bots decken Entwicklung, Unity, UI, iOS, Android, Analytics ab. Faustregel aus dem Deployment: **ein Bot pro Stelle, die du in einem Organigramm benennen könntest** — nicht pro Aufgabe, pro *Verantwortung*.

## Schritt 2 — Die Spezialisten erstellen

Für jede Stelle ein Bot mit abgegrenztem Outcome-Prompt:

```text
You own QA for <product>. Test every release candidate on real devices,
post video proof, and block release on failures. Report what needs a
decision to the orchestrator.
```

Halte die Instructions jedes Bots auf die Regeln seiner Stelle fokussiert; geteiltes Wissen (Marke, Deploy-Prozess, wer was genehmigt) geht in die Instructions jedes Bots oder in eine geteilte Ressource — es gibt kein globales Memory über Bots hinweg, also tragen die Prompts des Orchestrators das Bindegewebe.

## Schritt 3 — Grants verdrahten

Ein Grant gibt Bot A Lese-/Nachrichtenzugriff auf Bot B — so reichen sich Bots Arbeit zu (die Bots fragen den Grant an; du genehmigst die Card einmal). Der Orchestrator braucht Zugriff auf jeden Spezialisten.

Die dokumentierte offizielle Variante — kleiner, gleiche Mechanik:

```text
QA Bot findet einen Bug ──grant──► Developer Bot fixt ──► QA testet auf
Staging nach ──► PM Bot meldet Status im Channel
```

Genehmige Grants eng: Der Orchestrator liest und schreibt den Spezialisten; die Spezialisten müssen nicht alle einander erreichen.

## Schritt 4 — Der Roll-up-Thread

Das ist die wichtigste einzelne Instruktion — sie verwandelt Unterbrechungen von 20 Bots in eine Gewohnheit:

```text
Collect every pending decision from the Bots you work with into one
Slack thread, posted at <times> daily. For each item: what's blocked,
the options, your recommendation. I answer in replies/emoji; treat my
replies as decisions and relay them.
```

Jenny fährt das **4×/Tag** und antwortet **per Emoji**. Die Disziplin: Du sprichst nie mit den Spezialisten — der Orchestrator leitet deine Entscheidung weiter und verfolgt sie bis zum Ende.

## Schritt 5 — Kadenz = der Herzschlag der Org

| Kadenz | Wer sie fährt |
| --- | --- |
| Täglich gerankte Fix-Liste | PM-Bot (Metriken + Reviews + Trends) |
| Wöchentlicher Release Candidate | Release-Bot → Sign-off des QA-Bots |
| Entscheidungs-Thread 4×/Tag | Orchestrator |
| Spielerhilfe über Nacht | Support-Bot (entwirft Antworten für morgendliche Genehmigung) |

Jeder Bot besitzt seinen Loop; der Orchestrator besitzt den Zeitplan der Loops.

## Schritt 6 — Inter-Bot-Protokoll (BotSpeak)

Das Skalierungsproblem, vor dem dich niemand warnt: Jennys 20+ Bots schickten **700+ Nachrichten/Tag** — sie kam nicht hinterher. Ihre Lösung war **BotSpeak**, eine token-sparende Kurzsprache, die Bots *untereinander* nutzen ([ihr Bericht](https://x.com/xujennyc/status/2123111543105868166)):

| Regel | Was sie bedeutet |
| --- | --- |
| Kürzel | `ACK` und Konsorten statt ganzer Antworten |
| ASD-STE100 | Vereinfachte englische Grammatik — der Luftfahrt-Doku-Standard, eindeutig und billig in Tokens |
| Emoji-Quittungen | ✅ reagieren statt "verstanden, danke" |
| Keine Floskeln | Bots schicken einander nur, was der andere braucht |
| Mensch bekommt Prosa | Der Roll-up-Thread bleibt in ganzen Sätzen mit Entscheidungskontext |

Sechs Tage nach der Umstellung: von Bots ohne sie getroffene Entscheidungen **×12**, wiederholte Anfragen −50 %, Inter-Bot-Klärungs-Posts −12 %. Das Protokoll existiert, weil Token-Verschwendung nicht die wahren Kosten sind — *Aufmerksamkeits*-Verschwendung ist es: kürzere Bot-zu-Bot-Nachrichten halten den einen Thread des Menschen lesbar.

## Verifizieren

- [ ] Jeder Spezialisten-Bot hat einen abgegrenzten Outcome-Prompt und aktive Grants
- [ ] Der Orchestrator postet den konsolidierten Entscheidungs-Thread im Zeitplan
- [ ] Eine Entscheidung, die du per Emoji beantwortet hast, wurde vom richtigen Spezialisten weitergeleitet und gelöst
- [ ] Ein Cross-Bot-Handoff wurde Ende-zu-Ende abgeschlossen (finden → fixen → verifizieren → berichten)
- [ ] Menschliche Nachrichten heute < Anzahl gemergter PRs

## Fallstricke

- **Den Orchestrator überspringen.** N Bots, die dich per DM anschreiben, sind N× Lärm. Die Org funktioniert nur, wenn Urteil durch einen Thread fließt.
- **Vage Stellen-Grenzen.** "Dev Bot" und "Fix Bot" werden kollidieren. Grenzen folgen dem Organigramm — QA *verifiziert*, Release *liefert*, PM *priorisiert*.
- **Over-Granting.** Mesh-Grants (jeder erreicht jeden) stellen das Chaos wieder her. Hub-and-Spoke über den Orchestrator.
- **Prosa zwischen Bots.** Bots, die einander Absätze schreiben — so entstehen 700 Nachrichten/Tag. Übernimm ein BotSpeak-artiges Protokoll: Kürzel + Emoji-Quittungen + keine Floskeln; ganze Sätze nur für den Menschen.

## Wissenscheck

1. Warum routet SuperJennyStack allen Menschenkontakt über *einen* konsolidierten Thread? *(Aufmerksamkeit ist der Engpass, nicht Compute — 20 Bots mit 20 Threads sind wieder 20 Jobs.)*
2. Wann schlägt ein Grant "den Orchestrator fragen"? *(Wenn die benötigte Fähigkeit schon einem anderen Bot gehört — Grants leihen Ownership statt sie zu duplizieren.)*
3. Was sagt die Kadenz "4×/Tag mit Emoji" des Menschen über Delegationstiefe aus? *(Entscheidungsbandbreite, nicht Headcount, ist es, was Bots ersetzen — der Mensch behielt die Urteilschicht und verlor die Tipp-Schicht.)*

## Quellen

- [Introducing Devin Bots](https://devin.ai/blog/introducing-devin-bots) — SuperJennyStack-Zahlen, Grant-Handoff-Variante
- [Bot-Marketplace](https://devin.ai/bots/templates) — SuperJennyStack-Community-Template + 16 offizielle Templates
- [Bots-Doku](https://docs.devin.ai/work-with-devin/bots) — Grants, Memory, Zugriff
- Verwandt: [Leitfaden 5 — Referenz-verankerter Schwarm](bots-204-reference-grounded-swarm.md) für Schwärme, die *schreiben* statt *betreiben*
