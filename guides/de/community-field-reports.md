# Leitfaden 14 — Community-Feldberichte

**Ziel:** was Engineers, die Devin auf echter Arbeit laufen ließen, tatsächlich lernten — inklusive der Fehlschläge. Destilliert aus veröffentlichten Hands-on-Berichten, sowohl lobenden als auch feindlichen.
**Level:** für Urteilsvermögen hier beginnen
**Quellen:** je Bericht unten verlinkt

Dieser Leitfaden ist bewusst ausgewogen: wo Devin zuverlässig gewinnt, wo es Geld verbrennt, und der Arbeitsstil, der die beiden Ergebnisse trennt.

## Das Muster, das sich in jedem Bericht wiederholt

Nutzer, die Ergebnisse bekommen, behandeln Devin als **asynchronen Junior-Engineer**, nicht als Code-Generator. Scott Wu (Cognition-CEO) beschreibt den internen Workflow in [Lenny's Newsletter](https://www.lennysnewsletter.com/p/how-devin-replaces-your-junior-engineers): gut geschnittene Aufgaben delegieren, sie während Meetings laufen lassen, PRs reviewen. [Everys Bericht](https://every.to/chain-of-thought/coding-with-devin-my-new-ai-programming-agent) landet auf demselben Rahmen — es erfordert ein *Skill Set*: lernen, wozu es taugt, Tasks schreiben, die es versteht, wissen, wann einzugreifen, und lernen, Arbeit zu vertrauen, die anders gemacht ist als du es tätest.

## Wo Devin gewann, dokumentiert

**End-to-End-Prototyping.** Aus einem leeren Repo scaffoldete Devin einen "City Explorer" aus FastAPI + React (Bilder/Wetter/News-Integrationen), lief lokal, öffnete einen PR und deployte eine öffentliche URL — ~90 Minuten, ~2 menschliche Eingriffe ([Hands-on auf Medium](https://medium.com/@sambhavgaur_70582/copilot-cursor-or-devin-my-hands-on-weekend-with-ai-that-codes-and-deploys-acc708e802b3)). [Scott Logic](https://blog.scottlogic.com/2025/10/20/rapid-development-with-devin.html) berichtet denselben Bogen auf einem echten Kunden-Prototyp — mit einer entscheidenden Iterations-Lektion unten.

**Arbeit, die eine Runtime braucht.** In einem [Head-to-Head mit Claude Code](https://web.archive.org/web/20260718112612/https://mohitkhare.me/blog/devin-vs-claude-code/) verlor Devin bei Aufgaben, die in deine Konventionen passen mussten, gewann aber klar dort, wo eine Maschine hilft: Memory-Leak-Jagd, bei der es profiled, Heap-Snapshots unter Last nahm und einen Bericht produzierte — die eigene VM des Agenten ist das Feature.

**Live-Troubleshooting.** [Faros](https://www.faros.ai/blog/how-to-use-devin-ai-troubleshooting) benutzte Devin *während eines Kundenanrufs*: es las den Introspection-API-Code und generierte ein funktionierendes `curl` in Sekunden — ein 1–2-Tage-Follow-up-Loop kollabierte in den Anruf selbst.

**Echte Migrationen mit frischen Docs.** Ein Tailwind-3→4 + DaisyUI-4→5-Upgrade auf einem kniffligen Vue→React-Codebase funktionierte, als das Team Devin aktuelle Docs über den Context7-MCP fütterte — der Prompt trug den *Kontext*, nicht nur die Aufgabe ([Bootcamp-Write-up](https://medium.com/design-bootcamp/day-7-of-30-getting-to-know-devon-ai-and-working-with-him-743c351cd0c4)).

**Selbst-Verifikation.** Ein [Jahres-Praktiker-Vergleich](https://architecttocto.substack.com/p/the-only-coding-agent-worth-paying) markiert Devins browsergetriebenes e2e-Testing als Schwellenmoment: Es navigiert zu dem, was es gebaut hat, und prüft es — ein Feedback-Loop, der Engineering ähnelt, nicht Generation.

**Jenseits von Code.** Ein Cognition-Forscher berichtet, Devin habe eine Lean-Formalization neu gebaut — und beendet — die ihn neun Jahre zuvor einen Großteil eines Semesters gekostet hatte, in **unter 15 Minuten** ([Post](https://x.com/penlume/status/2115806616796921885)). Mathe-Formalization belohnt dieselbe Eigenschaft wie Migrationen: eine maschinell prüfbare Definition von fertig.

**An Observability verdrahtet.** [Dynatrace MCP + Devin](https://medium.com/lets-code-future/how-i-turned-devin-into-a-performance-analysis-agent-with-dynatrace-mcp-753d3f4790a2) macht Devin zu einem Performance-Analyse-Agenten: Es fragt Live-Metriken und Traces ab, dann diagnostiziert es — der MCP-Server trägt Produktionskontext, den das Repo nicht kann (Medium). Siehe auch [Devin: vom Bug-Report zum Pull Request](https://medium.com/@winter.inc/devin-from-bug-report-to-pull-request-25-days-of-ai-day-18-b158daa20f23) für den schlichten Ticket→PR-Loop end-to-end.

## Wo es scheiterte, dokumentiert

- **Vage oder zu breite Prompts.** Scott Logics erster Prompt produzierte ein unbrauchbares Scaffold; Stack und Auftrag verengen ("just the models") fixte es. Devin überbaut — sag ihm, was es *nicht* bauen soll.
- **Konventions-Anpassungs-Tasks.** "Add pagination to this endpoint" kam in zwei unabhängigen Berichten fehlausgerichtet zu den Codebase-Konventionen zurück ([amillionmonkeys](https://www.amillionmonkeys.co.uk/blog/ai-coding-tools-small-studios), [mohitkhare](https://web.archive.org/web/20260718112612/https://mohitkhare.me/blog/devin-vs-claude-code/)) — Devin baut isoliert, es sei denn, du trägst die Konventionen zu ihm (→ Leitfaden 9).
- **Nicht prüfbare Arbeit.** [expectedwrong](https://expectedwrong.com/devin-appraised) und [alanwests 10-Task-Test](https://dev.to/alanwest/i-gave-devin-10-real-tasks-it-completed-3-3063) dokumentieren den Fehlermodus: selbstbewusster Output, der kaputt oder abwesend ist, Credits in Loops verbrannt. Ihre Tasks neigten zu Arbeit ohne klare Verifikation — dasselbe Gate, das das offizielle Playbook verpflichtend macht (Leitfaden 11).

## Benannte Team-Deployments (Community, mit Zahlen)

Echte Orgs, die ihre Devin-Betriebsdaten veröffentlichen — meist aus Japans Engineering-Community, die ungewöhnlich gut dokumentiert:

| Team | Deployment | Berichtetes Ergebnis |
| --- | --- | --- |
| rakko_inc | Auto-Code-Review via Playbooks + GitHub Actions + Devin API — verdaut jeden PR vor dem menschlichen Review | **65 → 184 reviewte PRs/Monat (2.8×)**; Menschen starten von Devins Zusammenfassung ([Bericht](https://zenn.dev/rakko_inc/articles/00cc5a5a679971), JP) |
| Skillnote (QA) | PR → Actions → Devin generiert Testdesign-Entwürfe (CSV/Excel, inkl. "warum dieser Fall") gepostet in den PR | ~**35 Min. gespart pro 10 Testfälle**; Devin-entworfene Fälle fingen Bugs, die Menschen verpassten ([Bericht](https://zenn.dev/skillnote/articles/5ba429ca249801), JP) |
| arufian | Serverless GitHub-Event-Automation (kein stehender Server): Labels `devin:fix`/`devin:plan` steuern Devin-Sessions, mit **Priorität-×-Komplexität-Policy-Tabelle** und Plan-first-Approval-Flow | Safety-Scans gaten riskante PRs; hochkomplexe Arbeit bekommt Plan → menschliches Approve → `run that plan` ([Bericht](https://zenn.dev/arufian/articles/f80a62f5217cee), JP) |
| Leverages (levtech) | Org-Rollout: 14 Teams / ~30 Personen | **177 gemergte PRs** in ~2.5 Monaten; sie messen ROI als `ACU-Kosten − gesparte Stunden × Lohn` und tracken den Task-Typ-Mix ([Bericht](https://zenn.dev/levtech/articles/9c869303820844), JP) |
| Decagon | AutoResearch auf Devin Cloud: ein Orchestrator-Devin + parallele Subagents mit konkurrierenden Hypothesen; jede Idee gegen replayten Produktionstraffic auf Modal-GPUs verifiziert | **bis zu 2.5× mehr Throughput pro GPU** auf Support-Traffic ([Writeup](https://x.com/DecagonAI/article/2115511110120120437)) |
| Nader Dabit | Persönliche 5-Bot-Org — **CTO** (alle Sessions/Repos, iMessage VIP), **Auto(mation)Bot** (fährt seine Automations, Perf-Reports), **DevCommunityBot** (Ambassador-Programm-Daten → Mini-Apps), **DevRelBot** (Docs + Tutorial-Videos mit *eigenem Computer, eigenen Devin/GitHub/Linear-Accounts, ElevenLabs-Voice-Clone*) | Plus **Windfable**: ~10 SuperJennyStack-Bots auf einem Unity-iOS-RPG, jeder mit eigenem macOS+Xcode+Unity, testet iPhone Duo folded/unfolded mit Screenshot-/Video-Diffs ([Primer](https://x.com/dabit3/status/2122755275182469515)) |
| Mark Fenner | Solo-Operator mit vier berufsspezifischen Bots unter einem koordinierenden Chief Agent Bot ("Frankie") | Konsolidierte Updates über eine Entscheidungsoberfläche — die Multi-Bot-Org-Form funktioniert ohne Team ([Walkthrough](https://x.com/markfenner/status/2122740244328145211)) |

Die wiederverwendbaren Ideen darin: **Policy-Tabellen-Gating** (arufian: nur risikoarme Arbeit auto-PR-en, plan-first bei komplexem), **Fixed-Output-Prompting** (Skillnote: festes CSV-Format + Inline-Python für Konversion tötet Output-Varianz), **Reviewer-Pre-Digest** (rakko: Devin fasst zusammen + markiert, bevor der Mensch liest) und **ehrliches Accounting** (levtechs ACU-vs-Löhne-ROI-Formel).

## Die destillierten Lektionen

1. **Scope den Slice, nicht das Projekt.** Die Erfolge sind alle begrenzte Einheiten; die Fehlschläge sind "bau/fix das mal breit." (Offizielle Doktrin: Leitfaden 13.)
2. **Verifiziere oder delegiere nicht.** Gib Devin Arbeit, bei der eine Maschine "fertig" prüfen kann — Tests, Builds, ein funktionierendes `curl`, eine gerenderte Seite.
3. **Trage Kontext, nicht Annahmen.** Konventionen, aktuelle Docs (via MCP), die Form deines Stacks — die Fehlschläge sind Kontextfehler, keine Fähigkeitsfehler.
4. **Delegiere; schau nicht zu.** Der ROI in jedem positiven Bericht ist *Asynchronität* — Tasks laufen, während du anderes tust. Ihm beim Tippen zuzusehen ist, wie du entscheidest, es sei "langsam".
5. **Iteriere den Prompt, nicht das Tool.** Scott Logics Fix war kein anderer Agent — sondern ein engerer Prompt. Behandle einen fehlgeschlagenen ersten Lauf als Prompt-Bug.

## Scott Wus internes Top-5 (aus dem Lenny's-Interview)

Die Tasks, die Cognition selbst am meisten delegiert: **Frontend-Fixes, Versions-Upgrades, Dokumentation, Incident Response, Testing** — plus ein "first line of defense"-Muster, wo Devin Crashes analysiert, bevor Menschen eingreifen, und DeepWiki-Recherche, um *bessere Prompts zu schreiben*.

## Verifizieren

- [ ] Wähl den Bericht, der deinem Stack am nächsten ist, und lies das Original, nicht die Destillation — hält die Zahl im Kontext stand?
- [ ] Schreib die eine Lektion auf, bei deren Reproduktion in deiner Org du Geld wetten würdest; kannst du sie nicht nennen, wähl einen anderen Bericht

## Fallstricke

- **Survivorship-Bias.** Die leuchtenden Berichte publizieren Zahlen; die stillen Fehlschläge publizieren nichts. Lies die Fehlschläge dieser Sammlung als das mediane Erlebnis, die Gewinne als die Decke.
- **Cargo-Culting.** Scott Logics Prompt-Iteration funktionierte *weil* sie iterierten — ihren finalen Prompt ohne ihren Loop zu kopieren bringt dir ihren Anfang, nicht ihr Ergebnis.

## Wissenscheck

1. Was haben die Fehlschlag-Berichte gemeinsam, das den Erfolgs-Berichten fehlt? *(Nicht verifizierbare Delegation — die Fehlschläge gaben Devin Arbeit, bei der niemand "fertig" prüfen konnte; jeder Erfolg definierte einen Check.)*
2. Warum ist Faros' "Debuggen im Kundenanruf" eine Deployment-Lektion, keine Anekdote? *(Es zeigt die Live-Triage-Bewegung: der Agent als First Responder, während der Mensch die Kundenbeziehung hält.)*
3. Warum zählt dieser Leitfaden einen feindlichen Bericht gleichwertig als Quelle? *(Adversariale Berichte legen die Randbedingungen offen — du lernst die Kartenränder von Leuten, die darüber hinausgingen.)*

## Quellen

- [Scott Logic — Rapid development with Devin](https://blog.scottlogic.com/2025/10/20/rapid-development-with-devin.html)
- [Lenny's Newsletter — Scott Wu on Cognition's internal Devin usage](https://www.lennysnewsletter.com/p/how-devin-replaces-your-junior-engineers)
- [Every — Coding with Devin](https://every.to/chain-of-thought/coding-with-devin-my-new-ai-programming-agent)
- [dev>notes — Devin vs Claude Code](https://web.archive.org/web/20260718112612/https://mohitkhare.me/blog/devin-vs-claude-code/)
- [Faros — Devin for live troubleshooting](https://www.faros.ai/blog/how-to-use-devin-ai-troubleshooting)
- [Medium — Copilot, Cursor or Devin weekend](https://medium.com/@sambhavgaur_70582/copilot-cursor-or-devin-my-hands-on-weekend-with-ai-that-codes-and-deploys-acc708e802b3)
- [Bootcamp — Day 7 with Devin (Tailwind/DaisyUI migration)](https://medium.com/design-bootcamp/day-7-of-30-getting-to-know-devon-ai-and-working-with-him-743c351cd0c4)
- [architect to CTO — The only coding agent worth paying for](https://architecttocto.substack.com/p/the-only-coding-agent-worth-paying)
- [expectedwrong — Devin, appraised](https://expectedwrong.com/devin-appraised) · [dev.to — 10 real tasks, 3 completed](https://dev.to/alanwest/i-gave-devin-10-real-tasks-it-completed-3-3063) · [amillionmonkeys](https://www.amillionmonkeys.co.uk/blog/ai-coding-tools-small-studios)
- [Signadot — Testing Devin's changes end to end](https://dev.to/signadot/test-devins-changes-end-to-end-with-signadot-a0)
