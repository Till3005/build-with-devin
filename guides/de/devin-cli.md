# Leitfaden 12 — Devin CLI & Erweiterbarkeit

**Ziel:** das lokale Terminal-Devin — den Agenten auf deiner Maschine laufen lassen, Arbeit an Devin Cloud übergeben und mit Skills, Rules, Plugins, Hooks und Subagents erweitern.
**Level:** mittel
**Quellen:** [Devin-CLI-Doku](https://docs.devin.ai/cli/index.md) — [introducing](https://docs.devin.ai/cli/introducing-devin-cli.md), [essential commands](https://docs.devin.ai/cli/essential-commands.md), [extensibility](https://docs.devin.ai/cli/extensibility/index.md)

## Was es ist

Devin CLI ist ein Coding-Agent, der in deinem Terminal lebt und sich mit Devin Cloud verbindet. Zwei Arbeitsmodi, und die Kraft liegt im Wechsel zwischen ihnen:

- **Lokal** — bearbeitet dein ausgechecktes Repo auf deiner Maschine
- **Cloud** — `devin --cloud` erstellt/steuert/nimmt Cloud-Sessions wieder auf; `/handoff` schickt eine lokale Aufgabe an ein Cloud-Devin, `/open` holt den PR einer Cloud-Session zurück auf deine Maschine

```text
lokales Repo ──/handoff──► Devin-Cloud-Session ──PR──► /open ──► lokales Repo
      ▲                            │
      └──── devin ssh / forward (ihre VM inspizieren) ────┘
```

## Die Teile, die zählen

| Oberfläche | Was sie tut |
| --- | --- |
| `devin ssh` / `devin forward` | SSH in die VM einer Cloud-Session, Ports forwarden, `scp` von Dateien |
| Subagents | An unabhängige Agenten (Vordergrund/Hintergrund) mit eigenen Profilen und Berechtigungen delegieren |
| Models | Adaptive Routing wählt das Modell pro Aufgabe; Fusion paart einen Frontier-Lead + billigen Sidekick |
| ACP | Läuft in JetBrains, Zed, Xcode über das Agent Client Protocol |

## Der Erweiterbarkeits-Stack

Hier machen Teams das CLI zu *ihrem* — dieselbe Schichtung wie Leitfaden 9, lokal angewendet:

| Schicht | Datei/Mechanismus | Verwendung |
| --- | --- | --- |
| Rules | `AGENTS.md` / Rules-Dateien | Always-on-Instructions, die jede Session liest |
| Skills | `SKILL.md` | Wiederverwendbare Prozeduren — per Slash aufgerufen oder vom Agenten gewählt, mit eigenen Permissions/`allowed-tools` |
| Plugins | Plugin-Manifest | Bündelt Skills + Rules + Hooks + MCP-Server; geteilt über einen **Team-Marketplace** |
| Hooks | Lifecycle-Hooks | Shell/LLM-Logik auf `PreToolUse`, `PostToolUse`, `SessionStart`, `SessionEnd`… — blockiert oder schreibt Tool-Calls um, injiziert Kontext |
| MCP | MCP-Config | Externe Tool-Server (stdio / HTTP / SSE) |

**Importpfad:** `read_config_from` importiert Settings aus Cursor, Windsurf, Claude Code, Copilot, Codex, Kiro, OpenCode, Zed — Migration ist ein Flag, kein Rewrite.

## Drei Workflows, die sich lohnen zu kopieren

**1. Lokal → Cloud-Fan-out.** Eine Aufgabe lokal starten, an ihre Grenzen stoßen, per `/handoff` an eine Cloud-Session, die auf eigener Maschine weiterläuft — den PR mit `/open` zurückholen.

**2. Skills als Memory.** Jede wiederholte Prozedur (der Migrations-Skill aus Leitfaden 11, ein Hotfix-Runbook, ein Release-Cut) in ein `SKILL.md` verwandeln — die CLI-Doku empfiehlt, *erfolgreiche Session-Transkripte* zurück in Skills zu füttern, um Lücken zu schließen. Plugins paketieren und teilen sie ans ganze Team.

**3. Guardrails via Hooks.** Ein `PreToolUse`-Hook, der `rm -rf`-Muster blockiert oder Review bei Migrationen erzwingt — die Durchsetzung lebt im Hook, nicht im erhofften Modellverhalten.

## Verifizieren

- [ ] `devin` führt eine lokale Session aus; `devin --cloud` listet/erstellt Cloud-Sessions
- [ ] Eine per `/handoff` übergebene Aufgabe wurde in der Cloud fertig und ihr PR kam via `/open` zurück
- [ ] Ein per Slash-Command aufgerufenes `SKILL.md` hat deine Prozedur ausgeführt
- [ ] (Enterprise) der Team-Marketplace liefert dein Plugin an ein anderes Mitglied

## Fallstricke

- **Lokal für parallele Arbeit.** Das CLI ist ein Agent in deinem Terminal — für parallele Slices nutze Cloud-Sessions oder einen Bot; das CLI ist die *Hands-on*-Oberfläche.
- **Rules-Wildwuchs.** `AGENTS.md` + Projekt-Rules + globale Rules interagieren per Präzedenz — halte jede Regel in genau einer Schicht, sonst bekämpfen sie sich.

## Wissenscheck

1. Wann nutzt du `/handoff` an Devin Cloud statt lokal fertig zu werden? *(Wenn die Arbeit Cloud-Parallelismus, Org-Tools braucht oder länger läuft, als dein Laptop offen bleibt.)*
2. Was ist der Unterschied zwischen Skill, Rule und Plugin? *(Ein Skill ist eine Aufgaben-Prozedur, eine Rule ist permanenter Kontext, ein Plugin ist das Paket, das beides plus Hooks liefert.)*
3. Warum sind Hooks + Subagents für Team-Adoption wichtig? *(Hooks setzen Org-Policy in jeder CLI-Session durch; Subagents lassen einen Operator eine Flotte fahren — die beiden skalieren in entgegengesetzte Richtungen.)*

## Quellen

- [Devin-CLI-Doku](https://docs.devin.ai/cli/index.md) — Quickstart, Befehle, Cloud-Integration, Erweiterbarkeit, ACP, Modelle
- Verwandt: [Leitfaden 9 — Playbooks & Knowledge](playbooks-and-knowledge.md) (dieselbe Konventions-Schicht, org-weit)
