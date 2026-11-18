# Guía 12 — Devin CLI & extensibilidad

**Objetivo:** el Devin de terminal local — ejecuta el agente en tu máquina, pasa trabajo a Devin Cloud y extiéndelo con skills, rules, plugins, hooks y subagents.
**Nivel:** intermedio
**Fuentes:** [docs de Devin CLI](https://docs.devin.ai/cli/index.md) — [introducing](https://docs.devin.ai/cli/introducing-devin-cli.md), [essential commands](https://docs.devin.ai/cli/essential-commands.md), [extensibility](https://docs.devin.ai/cli/extensibility/index.md)

## Qué es

Devin CLI es un agente de código que vive en tu terminal y se conecta a Devin Cloud. Dos modos de trabajo, y el poder está en moverse entre ellos:

- **Local** — edita tu repo checked-out en tu máquina
- **Cloud** — `devin --cloud` crea/dirige/reanuda sesiones en la nube; `/handoff` manda una tarea local a un Devin en la nube, `/open` trae el PR de una sesión cloud de vuelta a tu máquina

```text
repo local ──/handoff──► sesión Devin Cloud ──PR──► /open ──► repo local
     ▲                          │
     └──── devin ssh / forward (inspeccionar su VM) ────┘
```

## Las piezas que importan

| Superficie | Qué hace |
| --- | --- |
| `devin ssh` / `devin forward` | SSH a la VM de una sesión cloud, forward de puertos, `scp` de archivos |
| Subagents | Delega a agentes independientes (foreground/background) con perfiles y permisos propios |
| Models | El adaptive routing elige el modelo por tarea; Fusion empareja un lead frontier + sidekick barato |
| ACP | Corre dentro de JetBrains, Zed, Xcode vía Agent Client Protocol |

## El stack de extensibilidad

Aquí es donde los equipos hacen el CLI *suyo* — mismo apilado que la Guía 9, aplicado localmente:

| Capa | Archivo/mecanismo | Sirve para |
| --- | --- | --- |
| Rules | `AGENTS.md` / archivos de rules | Instrucciones siempre activas que toda sesión lee |
| Skills | `SKILL.md` | Procedimientos reutilizables — invocados por slash o elegidos por el agente, con permisos/`allowed-tools` propios |
| Plugins | manifiesto de plugin | Empaqueta skills + rules + hooks + MCP servers; se comparte por un **team marketplace** |
| Hooks | lifecycle hooks | Lógica shell/LLM en `PreToolUse`, `PostToolUse`, `SessionStart`, `SessionEnd`… — bloquea o reescribe tool calls, inyecta contexto |
| MCP | config MCP | Servidores de herramientas externos (stdio / HTTP / SSE) |

**Ruta de importación:** `read_config_from` importa settings de Cursor, Windsurf, Claude Code, Copilot, Codex, Kiro, OpenCode, Zed — la migración es una flag, no una reescritura.

## Tres workflows que vale copiar

**1. Local → fan-out en la nube.** Empieza una tarea localmente, toca sus límites, `/handoff` a una sesión cloud que sigue en su propia máquina — trae el PR de vuelta con `/open`.

**2. Skills como memoria.** Convierte cualquier procedimiento repetido (el skill de migración de la Guía 11, un runbook de hotfix, un corte de release) en un `SKILL.md` — los docs del CLI notan alimentar *transcripciones de sesiones exitosas* de vuelta a los skills para cerrar huecos. Los plugins los empaquetan y comparten a todo el equipo.

**3. Guardrails vía hooks.** Un hook `PreToolUse` que bloquea patrones `rm -rf` o fuerza review en migraciones — la fiscalización vive en el hook, no en el comportamiento esperado del modelo.

## Checklist de verificación

- [ ] `devin` corre una sesión local; `devin --cloud` lista/crea sesiones cloud
- [ ] Una tarea enviada por `/handoff` se completó en la nube y su PR volvió vía `/open`
- [ ] Un `SKILL.md` invocado por slash command ejecutó tu procedimiento
- [ ] (Enterprise) el team marketplace sirve tu plugin a otro miembro

## Trampas

- **Local para trabajo paralelo.** El CLI es un agente en tu terminal — para porciones paralelas usa sesiones cloud o un Bot; el CLI es la superficie *hands-on*.
- **Dispersión de rules.** `AGENTS.md` + rules de proyecto + rules globales interactúan por precedencia — mantén cada regla en exactamente una capa o se pelean.

## Prueba de conocimiento

1. ¿Cuándo usar `/handoff` a Devin Cloud en vez de terminar localmente? *(Cuando el trabajo necesita paralelismo a escala de nube, herramientas de la org, o corre más de lo que tu portátil queda abierto.)*
2. ¿Cuál es la diferencia entre skill, rule y plugin? *(Un skill es un procedimiento de tarea, una rule es contexto permanente, un plugin es el paquete que envía ambos más hooks.)*
3. ¿Por qué hooks + subagents importan para la adopción en equipo? *(Los hooks imponen política de la org en cada sesión del CLI; los subagents dejan a un operador correr una flota — ambos escalan en direcciones opuestas.)*

## Fuentes

- [Docs de Devin CLI](https://docs.devin.ai/cli/index.md) — quickstart, comandos, integración cloud, extensibilidad, ACP, modelos
- Relacionado: [Guía 9 — Playbooks & knowledge](playbooks-and-knowledge.md) (misma capa de convenciones, a nivel org)
