# Leitfaden 1 — Dein erster Bot

**Ziel:** einen Devin Bot erstellen, der ein Ergebnis besitzt, und die sechs Mechaniken lernen, auf denen alle folgenden Leitfäden aufbauen.
**Level:** hier beginnen · **Zeit:** ~15 Minuten
**Quelle:** [offizielle Bots-Doku](https://docs.devin.ai/work-with-devin/bots), [Launch-Post](https://devin.ai/blog/introducing-devin-bots)

## Was ein Bot ist

Eine Session erledigt eine Anfrage. Ein Bot *besitzt ein Ergebnis*: Du formulierst das Ziel einmal in seinem Chat, er plant die Arbeit, startet für jedes Teil eine eigene Devin-Session, überwacht sie und bringt dir nur, was dein Urteil braucht. Er persistiert — Memory, Sessions und Automations überdauern Wochen.

Die sechs Mechaniken, in der Reihenfolge, in der du ihnen begegnen wirst:

| Mechanik | Was sie ist | Wo du sie anfasst |
| --- | --- | --- |
| Chat | Ein Thread für alles, was der Bot besitzt — Ziele, Berichte, Fragen | Die Seite des Bots / Slack / iMessage |
| Sessions | Jede Arbeitseinheit läuft als eigene Devin-Session auf eigener Maschine | Vom Bot erzeugt und überwacht |
| Needs you | Entscheidungen, PR-Reviews, Berechtigungsanfragen, Berichte — eine Liste | Oben im Chat des Bots |
| Memory | Was der Bot lernt, als Dateien gespeichert, bei jedem Session-Start gelesen | Settings → Memory |
| Instructions | Dauerregeln von Menschen, bei jedem Session-Start gelesen | Settings → General |
| Access | Die eigenen Verbindungen/Secrets des Bots, plus Grants zwischen Bots | Settings → Access |

## Schritt 1 — Erstellen

Sidebar → **Bots** → *Create new Bot* → Template wählen oder *Start from scratch* → benennen.

Ein neuer Bot ist privat für dich, bis du ihn teilst. Seine Nutzung zählt auf deinen Plan wie jede Session.

> Tipp: Ein Template bringt Instructions für einen Job mit (QA Engineer, Data Analyst, …). *Start from scratch* ist die richtige Wahl für die Leitfäden in diesem Repo — du schreibst den Outcome-Prompt selbst.

## Schritt 2 — Das Ergebnis zuweisen

Die erste Nachricht ist der wichtigste Input, den ein Bot je bekommt. Gib ihm ein *Ziel*, keine Aufgabe:

```text
You own the Android app now. Keep it at feature parity with iOS.
```

Das ist der wörtliche Prompt, mit dem Cognitions Android Bot gestartet ist. Vergleiche:

| Schwach (eine Aufgabe) | Stark (ein Ergebnis) |
| --- | --- |
| "Fix the checkout button" | "You own checkout. Keep it fast, correct, and covered by tests." |
| "Update the docs" | "You own the docs. Keep them in step with `main`." |
| "Watch CI" | "You own build health on `main`. When a check regresses, find the cause and fix it." |

Eine Aufgabe endet, wenn sie fertig ist; ein Ergebnis lässt den Bot für immer neu planen.

## Schritt 3 — Mit ihm arbeiten

Nachdem das Ergebnis gesetzt ist, sind die meisten deiner Nachrichten Check-ins:

```text
anything waiting on me?
```

Öffne **Needs you** (oben im Chat), wenn der Bot etwas markiert:

| Eintrag | Dein Zug |
| --- | --- |
| Decision | Eine Option wählen — der Bot markiert seine Empfehlung |
| Review PR / Merge PR | Reviewen oder mergen |
| Permission request | Neuen Zugriff, eine Automation, einen Netzwerk-Host oder eine Nutzungserhöhung genehmigen oder ablehnen |
| Report / FYI | Lesen |

Du kannst jeden Eintrag in eigenen Worten beantworten, snoozen oder verwerfen.

## Schritt 4 — Über Memory steuern, nicht über Mikromanagement

- **Instructions** (Settings → General): deine Dauerregeln — werden am Anfang jeder Session gelesen, die der Bot ausführt. Dauerhafte Policy gehört hierhin, nicht in den Chat.
- **Memory** (Settings → Memory): Dateien, die der Bot selbst schreibt — Präferenzen, Korrekturen, Projektfakten. Um zu ändern, woran er sich erinnert, sag es ihm im Chat ("remember: we deploy via Cloud Run, never bare VMs"). Jeder, der den Bot nutzen kann, kann sein Memory lesen — behandle das Memory eines geteilten Bots als geteilt.

Das skalierende Muster: Korrigiere den Bot einmal, lass ihn die Korrektur ins Memory schreiben, und jede künftige Session erbt sie. Cognition merged über 2.000 PRs/Woche in diesem Loop.

## Schritt 5 — Dort platzieren, wo du arbeitest

- **Slack:** Gib dem Bot eine eigene Slack-App, damit dein Team ihn @-erwähnen oder per DM erreichen kann (Settings → Slack). Jede berichtete Team-Deployment läuft so — der Bot wird ein benannter Teamkollege in einem Channel.
- **iMessage:** Schreib dem Bot vom Handy.
- **Web:** Der Bots-Abschnitt der Sidebar listet deine und die mit dir geteilten.

## Schritt 6 — Zeitpläne und Modi

- **Automations:** Im Chat fragen — *"run a summary of open PRs every weekday morning"* — und der Bot schlägt die Automation zur einmaligen Genehmigung vor. Verwalte sie unter Settings → Automations (pausieren/fortsetzen/entfernen).
- **Modes:** Der Bot hat einen eigenen Modus plus einen **Child-Capability**-Default für die von ihm erzeugten Sessions (z. B. `Normal / Ultra` im Modus-Picker des Chats). Du kannst auch für jede einzelne Session einen anderen Modus verlangen.

## Lebenszyklus

| Aktion | Wirkung |
| --- | --- |
| Recycle | Beendet die aktuelle Session; beim nächsten Öffnen startet eine frische. Im Chat-Menü. |
| Archive | Stoppt Antworten, entfernt ihn aus Bot-Listen, entfernt seine Slack-App und Inter-Bot-Grants (Unarchivieren stellt diese nicht wieder her — du richtest sie neu ein). |
| Delete | Endgültig: Einstellungen, Sessions, Memory, Automations. Kann nicht rückgängig gemacht werden. |

Nur der Ersteller und Rollen mit Manage Bots sehen Archive/Delete. In Enterprise-Plänen sind `Use Bots` / `Manage Bots` / `Manage Bots across the enterprise` separate Berechtigungen in Custom Roles.

## Verifizieren

- [ ] Bot erstellt und benannt; Outcome-Prompt im Chat gesendet
- [ ] Bot hat mindestens eine Child-Session gestartet, ohne zweimal gefragt zu werden
- [ ] Eine Entscheidung/ein PR/eine Berechtigungsanfrage erschien in **Needs you** und du hast sie gelöst
- [ ] Eine Korrektur, die du im Chat gegeben hast, erscheint als Memory-Datei unter Settings → Memory
- [ ] (Optional) Bot per @-Erwähnung in Slack erreichbar

## Fallstricke

- **Task-förmige Prompts.** "Fix X" erzeugt eine Session, keinen Bot. Wenn der Bot fertig ist und schweigt, war der Prompt eine Aufgabe — formuliere ihn als Ownership neu.
- **Chat für Policy.** Im Chat getippte Regeln scrollen weg; Regeln in Instructions werden jede Session gelesen. Chat = Richtung und Antworten; Instructions = Gesetz.
- **Needs you ignorieren.** Bots sind dafür gebaut, Urteilsaufrufe zu bündeln — ein- bis zweimal täglich prüfen, nicht dauerhaft.

## Wissenscheck

1. Was überlebt zwischen den Sessions eines Bots, was eine Einmal-Session nicht hat? *(Memory — plus das bestehende Ergebnis, Zeitpläne und Oberflächen.)*
2. Warum meldet ein Bot "needs-you" statt mitten in der Session zu fragen? *(Urteil geht asynchron in einen Thread; der Mensch ist kein blockierender Aufruf im Loop.)*
3. Welche Mechanik macht aus "einer schlauen Session" "einen Mitarbeiter"? *(Ownership eines Ergebnisses — das Ziel bleibt bestehen, nachdem jede einzelne Session endet.)*

## Quellen

- [Devin Bots — Docs](https://docs.devin.ai/work-with-devin/bots)
- [Introducing Devin Bots](https://devin.ai/blog/introducing-devin-bots)
- Weiter: [Leitfaden 2 — Product-owner-Bot](bots-201-product-owner.md)
