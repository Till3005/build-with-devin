# Guia 12 — Devin CLI & extensibilidade

**Objetivo:** o Devin de terminal local — rode o agente na sua máquina, passe trabalho para o Devin Cloud e estenda-o com skills, rules, plugins, hooks e subagents.
**Nível:** intermediário
**Fontes:** [docs do Devin CLI](https://docs.devin.ai/cli/index.md) — [introducing](https://docs.devin.ai/cli/introducing-devin-cli.md), [essential commands](https://docs.devin.ai/cli/essential-commands.md), [extensibility](https://docs.devin.ai/cli/extensibility/index.md)

## O que é

O Devin CLI é um agente de código que vive no seu terminal e se conecta ao Devin Cloud. Dois modos de trabalho, e o poder está em mover entre eles:

- **Local** — edita seu repo checked-out na sua máquina
- **Cloud** — `devin --cloud` cria/dirige/retoma sessões na nuvem; `/handoff` manda uma tarefa local para um Devin na nuvem, `/open` puxa o PR de uma sessão cloud de volta para sua máquina

```text
repo local ──/handoff──► sessão Devin Cloud ──PR──► /open ──► repo local
     ▲                          │
     └──── devin ssh / forward (inspecionar a VM) ────┘
```

## As peças que importam

| Superfície | O que faz |
| --- | --- |
| `devin ssh` / `devin forward` | SSH na VM de uma sessão cloud, forward de portas, `scp` de arquivos |
| Subagents | Delega a agentes independentes (foreground/background) com perfis e permissões próprios |
| Models | Adaptive routing escolhe o modelo por tarefa; Fusion emparelha um lead frontier + sidekick barato |
| ACP | Roda dentro de JetBrains, Zed, Xcode via Agent Client Protocol |

## O stack de extensibilidade

É aqui que equipes tornam o CLI *delas* — mesmo empilhamento do Guia 9, aplicado localmente:

| Camada | Arquivo/mecanismo | Serve para |
| --- | --- | --- |
| Rules | `AGENTS.md` / arquivos de rules | Instruções sempre ativas que toda sessão lê |
| Skills | `SKILL.md` | Procedimentos reutilizáveis — invocados por slash ou escolhidos pelo agente, com permissões/`allowed-tools` próprios |
| Plugins | manifest de plugin | Empacota skills + rules + hooks + MCP servers; compartilha por um **team marketplace** |
| Hooks | lifecycle hooks | Lógica shell/LLM em `PreToolUse`, `PostToolUse`, `SessionStart`, `SessionEnd`… — bloqueia ou reescreve tool calls, injeta contexto |
| MCP | config MCP | Servidores de ferramentas externos (stdio / HTTP / SSE) |

**Caminho de importação:** `read_config_from` importa settings de Cursor, Windsurf, Claude Code, Copilot, Codex, Kiro, OpenCode, Zed — migração é uma flag, não uma reescrita.

## Três workflows que valem copiar

**1. Local → fan-out na cloud.** Comece uma tarefa localmente, bata nos limites, `/handoff` para uma sessão cloud que continua na própria máquina — puxe o PR de volta com `/open`.

**2. Skills como memória.** Transforme qualquer procedimento repetido (o skill de migração do Guia 11, um runbook de hotfix, um corte de release) num `SKILL.md` — os docs do CLI notam alimentar *transcrições de sessões bem-sucedidas* de volta em skills para fechar lacunas. Plugins empacotam e compartilham para o time todo.

**3. Guardrails via hooks.** Hook `PreToolUse` que bloqueia padrões `rm -rf` ou força review em migrações — a fiscalização vive no hook, não no comportamento esperado do modelo.

## Checklist de verificação

- [ ] `devin` roda uma sessão local; `devin --cloud` lista/cria sessões cloud
- [ ] Uma tarefa enviada por `/handoff` completou na nuvem e seu PR voltou via `/open`
- [ ] Um `SKILL.md` invocado por slash command rodou seu procedimento
- [ ] (Enterprise) o team marketplace serve seu plugin a outro membro

## Armadilhas

- **Local para trabalho paralelo.** O CLI é um agente no seu terminal — para fatias paralelas use sessões cloud ou um Bot; o CLI é a superfície *hands-on*.
- **Dispersão de rules.** `AGENTS.md` + rules de projeto + rules globais interagem por precedência — mantenha cada regra em exatamente uma camada ou elas brigam.

## Teste de conhecimento

1. Quando usar `/handoff` para o Devin Cloud em vez de terminar localmente? *(Quando o trabalho precisa de paralelismo em escala de nuvem, ferramentas da org, ou roda mais que seu laptop fica aberto.)*
2. Qual a diferença entre skill, rule e plugin? *(Skill é procedimento de tarefa, rule é contexto permanente, plugin é o pacote que envia os dois mais hooks.)*
3. Por que hooks + subagents importam para adoção em equipe? *(Hooks impõem política da org em toda sessão CLI; subagents deixam um operador rodar uma frota — os dois escalam em direções opostas.)*

## Fontes

- [Docs do Devin CLI](https://docs.devin.ai/cli/index.md) — quickstart, comandos, integração cloud, extensibilidade, ACP, modelos
- Relacionado: [Guia 9 — Playbooks & knowledge](playbooks-and-knowledge.md) (mesma camada de convenções, org-wide)
