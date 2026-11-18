# Leitfaden 11 — Migrationen auf Skala

**Ziel:** eine große Migration (Sprache, Framework, Datenbank, Dependency, Architektur) als hunderte kleiner verifizierter PRs fahren statt als heroisches Rewrite.
**Level:** mittel → fortgeschritten
**Quellen:** [Best Practices](https://docs.devin.ai/use-cases/best-practices.md) · [Migration & Modernization](https://docs.devin.ai/use-cases/migration-modernization.md) · Migrations-Beispiele: [Java Upgrades](https://docs.devin.ai/use-cases/examples/java-upgrades.md), [COBOL](https://docs.devin.ai/use-cases/examples/cobol-modernization.md), [SAS→PySpark](https://docs.devin.ai/use-cases/examples/sas-to-pyspark.md), [JS→TS](https://docs.devin.ai/use-cases/examples/javascript-to-typescript.md), [NoSQL→SQL](https://docs.devin.ai/use-cases/examples/nosql-to-sql.md) · Nubank Case Study

## Das offizielle Playbook

Devins eigene Doku ist unverblümt, was skaliert: **wide & shallow** schlägt **tall & deep**. Eine Migration ist der kanonische wide-and-shallow-Job — dieselbe kleine Transformation auf hunderte unabhängiger Einheiten angewendet.

```text
Migration ──► in isolierte Einheiten schneiden (<90 Min. jede)
                      │
             ┌────────┴────────┐
             ▼                 ▼
        Skill für die     parallele Sessions,
        Transformation    ein Slice pro Session
             │                 │
             └────► pro Slice verifizieren (Tests/Build/CI)
                              │
                   Human Review → Merge → wiederholen
```

## Schritt 1 — Prüfe, ob deine Migration qualifiziert

Aus den offiziellen Kriterien — die meisten sollten gelten:

- Hohes Volumen repetitiver Subtasks
- Junior-Engineer-Komplexität pro Slice
- Isolierte, inkrementelle, rückwärtskompatible Änderungen
- **Objektive Verifikation pro Slice** (die harte Anforderung: Tests, Build, CI oder ein Custom-Skript)
- Minimale Cross-Slice-Abhängigkeiten

Qualifiziert nicht: ein Full-Repo-Rewrite, bei dem alles auf einmal landen muss.

## Schritt 2 — Schneiden

Der Slice ist die kleinste atomare Einheit — eine Datei, ein Notebook, ein Modul:

| Regel | Warum |
| --- | --- |
| < 90 Minuten manuelles Engineering pro Slice | Devins Zuverlässigkeit ist pro Slice |
| Unabhängig + rückwärtskompatibel | Slices laufen parallel und mergen in beliebiger Reihenfolge |
| Jeder Slice trägt eigene Verifikation | Keine Verifikation, keine Automatisierung — das ist das Failure-Gate |

Beispiel (offiziell): eine 50-Datei-REST→GraphQL-Migration → scopen, in konfliktfreie Arbeitspakete teilen, parallel laufen lassen.

## Schritt 3 — Die Transformation als Skill schreiben

Ein Skill = das wiederholbare Rezept, das jede Session ausführt. Offizielles Beispiel (Java 7→8, gekürzt):

```text
## Procedure
1. Verify the project is on Java 7
2. Install the Java 8 JDK
3. Update build configuration
4. Identify and replace deprecated Java 7 APIs
5. Analyze for Java 8 enhancement opportunities
6. Update unit tests
7. Test thoroughly
8. Update documentation
9. Build and verify
```

Schreibe deinen mit: expliziten Schritten, einer End-to-End-Referenz (ein Guide oder Video) und **mehreren Vorher/Nachher-Codebeispielen** — Input/Output-Paare sind das hochwertigste Signal, das du geben kannst.

## Schritt 4 — Parallele Sessions fahren

Mit dem Skill fixiert Slices über Sessions fächern — die [API](https://docs.devin.ai) oder Child-Sessions eines Bots (Leitfaden 4). Jeder Slice → eine Session → ein PR. Human Review gatet den Merge auf `main`.

Auf Skala akkumulieren die Zahlen: Nubanks Multi-Millionen-Zeilen-ETL-Migration fuhr diesen Loop auf 8–12× Effizienz — und ein feingetuntes Devin senkte die Zeit pro Task von ~40 → ~10 Minuten.

## Schritt 5 — Auf die Fehlerrate achten, nicht auf den Fortschrittsbalken

Kleine Fehlerraten akkumulieren über tausende Slices. Auf einem Dashboard operieren, nicht auf Bauchgefühl:

- Slice-Erfolgsrate beim ersten Versuch tracken — der Skill ist dein Fixpunkt, nicht die Sessions
- Fehlgeschlagene Slices fließen zurück in den Skill (der eigene Loop der Doku: *"feed session links into Devin to patch the gaps"*)
- Merge-Reihenfolge ist frei, weil Slices isoliert sind — ausnutzen

## Verifizieren

- [ ] Jeder Slice endet unter ~90 Min. und mergt unabhängig
- [ ] Ein Slice, der die Verifikation scheitert, erzeugt einen Fix oder ein markiertes Ticket — niemals einen stillen Merge
- [ ] Der Skill verbesserte sich messbar über die ersten 20 Slices (weniger menschliche Korrekturen pro Slice)
- [ ] Fortschritt ist zählbar: N/M Slices migriert, Erfolgsrate sichtbar

## Fallstricke

- **Ungeschnittene Migrationen.** "Migriere das ganze Repo" ist das offizielle Anti-Muster — keine Isolation, kein Parallelismus, keine Verifikation pro Einheit.
- **Keine Vorher/Nachher-Beispiele.** Der Skill ohne Beispiele produziert einen anderen Stil pro Session.
- **Human Review überspringen.** Parallel ≠ unbeaufsichtigt — jeder Slice wird vor `main` noch reviewt.

## Wissenscheck

1. Warum "wide and shallow"-Slices statt "deep and complete"? *(Jeder Slice muss grün landen — ein verifizierter 90-Minuten-PR akkumuliert; ein 3-Tage-Mega-Branch fault gegen main.)*
2. Warum braucht jeder Slice eigene Verifikation? *(Ohne Beweis pro Slice ist eine 500-PR-Migration 500 unverifizierte Diffs — die Fehlerfläche multipliziert statt zu dividieren.)*
3. Nubank meldete 8–12× Effizienz — was machte diese Zahl glaubwürdig statt Marketing? *(Veröffentlichte Methodik: gemessene Stufen-Zeiten vorher/nachher auf echten ETL-Pipelines, keine Projektion.)*

## Quellen

- [Best Practices — docs.devin.ai](https://docs.devin.ai/use-cases/best-practices.md)
- [Migration & Modernization + 5 Beispiel-Playbooks](https://docs.devin.ai/use-cases/migration-modernization.md)
- [Use-case gallery — Migrations](https://docs.devin.ai/use-cases/gallery/index.md)
- Verwandt: [Leitfaden 7 — Enterprise-Rollout](enterprise-playbook.md) (Form 1 ist dieser Leitfaden auf Org-Skala)
