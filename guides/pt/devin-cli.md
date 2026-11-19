# Guia 12 — Devin CLI & extensibilidade

**Objetivo:** o Devin de terminal local — rode o agente na sua máquina, passe trabalho para o Devin Cloud e estenda-o com skills, rules, plugins, hooks e subagents.
**Nível:** intermediário
**Fontes:** [docs do Devin CLI](https://docs.devin.ai/cli/index.md) — [introducing](https://docs.devin.ai/cli/introducing-devin-cli.md), [essential commands](https://docs.devin.ai/cli/essential-commands.md), [extensibility](https://docs.devin.ai/cli/extensibility/index.md)

## O que é

O Devin CLI é um agente de código que vive no seu terminal e se conecta ao Devin Cloud. Dois modos de trabalho, e o poder está em mover entre eles:

- **Local** — edita seu repo checked-out na sua máquina
- **Cloud** — `devin --cloud` cria/dirige/retoma sessões na nuvem; `/handoff` manda uma tarefa local para um Devin na nuvem, `/pickup` traz uma sessão cloud de volta para sua máquina (`/open` abre no web app ou no Devin Desktop)

```text
repo local ──/handoff──► sessão Devin Cloud ──/pickup──► repo local
     ▲                          │
     └──── devin ssh / forward (inspecionar a VM) ────┘
```

## As peças que importam

| Superfície | O que faz |
| --- | --- |
| `devin ssh` / `devin forward` | SSH na VM de uma sessão cloud, forward de portas, `scp` de arquivos |
| Subagents | Delega a agentes independentes (foreground/background) com perfis e permissões próprios |
| Models | Adaptive routing escolhe o modelo por tarefa; Fusion emparelha um lead frontier + sidekick barato |
| Daemon | Desde a v3000.13.4 sessões locais rodam num processo em background — fechar o app não interrompe, qualquer cliente reconecta (`devin daemon`, monitor `devin ls`) |
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

**1. Local → fan-out na cloud.** Comece uma tarefa localmente, bata nos limites, `/handoff` para uma sessão cloud que continua na própria máquina — traga o trabalho de volta com `/pickup`.

**2. Skills como memória.** Transforme qualquer procedimento repetido (o skill de migração do Guia 11, um runbook de hotfix, um corte de release) num `SKILL.md` — os docs do CLI notam alimentar *transcrições de sessões bem-sucedidas* de volta em skills para fechar lacunas. Plugins empacotam e compartilham para o time todo.

**3. Guardrails via hooks.** Hook `PreToolUse` que bloqueia padrões `rm -rf` ou força review em migrações — a fiscalização vive no hook, não no comportamento esperado do modelo.

## Passo a passo — gravado no Devin CLI v3000.14

Execução real, não maquete: Devin CLI `3000.14.30821` no Linux, plano Pro, um `demo-repo` descartável com um `app.py`. Modelos: `swe-2-flash-high` para a edição, `swe-2-high` para a skill (os dois tiers SWE-2 aparecem como **Free** em `devin models`).

**Vídeo (67 s, sem áudio):** a sessão inteira abaixo, do login ao erro do handoff.

[![2. Prompt: adicionar uma função subtract e um teste. O Devin mostra o diff e pede permissão — Allow, Accept edits mode, Bypass mode ou Deny](https://till3005.github.io/built-with-devin/assets/guides/devin-cli/walkthrough-poster.webp)](https://till3005.github.io/built-with-devin/assets/guides/devin-cli/walkthrough.mp4)

![1. devin --model swe-2-flash-high — login confirmado e o prompt de confiança no diretório](https://till3005.github.io/built-with-devin/assets/guides/devin-cli/step1-login-trust.webp)
*1. devin --model swe-2-flash-high — login confirmado e o prompt de confiança no diretório*

![2. Prompt: adicionar uma função subtract e um teste. O Devin mostra o diff e pede permissão — Allow, Accept edits mode, Bypass mode ou Deny](https://till3005.github.io/built-with-devin/assets/guides/devin-cli/step3-permission-prompt.webp)
*2. Prompt: adicionar uma função subtract e um teste. O Devin mostra o diff e pede permissão — Allow, Accept edits mode, Bypass mode ou Deny*

![3. Resultado: app.py editado, test_app.py criado; sem pytest, o Devin rodou os testes com python -c e avisou](https://till3005.github.io/built-with-devin/assets/guides/devin-cli/step4-task-done.webp)
*3. Resultado: app.py editado, test_app.py criado; sem pytest, o Devin rodou os testes com python -c e avisou*

![4. /model — Adaptive, Fusion (lead + sidekick) e famílias de modelos; SWE-2 Flash aparece como FREE, sem consumir cota](https://till3005.github.io/built-with-devin/assets/guides/devin-cli/step5-model-picker.webp)
*4. /model — Adaptive, Fusion (lead + sidekick) e famílias de modelos; SWE-2 Flash aparece como FREE, sem consumir cota*

![5. /exit imprime a dica devin -r <slug> para retomar; devin ls é o monitor de sessões locais](https://till3005.github.io/built-with-devin/assets/guides/devin-cli/step6-devin-ls.webp)
*5. /exit imprime a dica devin -r <slug> para retomar; devin ls é o monitor de sessões locais*

![6. devin --cloud e depois /list-sessions — as sessões cloud da conta, mais recentes primeiro](https://till3005.github.io/built-with-devin/assets/guides/devin-cli/step8-cloud-sessions.webp)
*6. devin --cloud e depois /list-sessions — as sessões cloud da conta, mais recentes primeiro*

![7. .devin/skills/review/SKILL.md roda como /review no swe-2-high e revisa as mudanças não commitadas](https://till3005.github.io/built-with-devin/assets/guides/devin-cli/step10-skill-result.webp)
*7. .devin/skills/review/SKILL.md roda como /review no swe-2-high e revisa as mudanças não commitadas*

![8. Armadilha: /handoff falha num repo sem git remote — "Handoff only works from git repos with a remote configured"](https://till3005.github.io/built-with-devin/assets/guides/devin-cli/step11-handoff-no-remote.webp)
*8. Armadilha: /handoff falha num repo sem git remote — "Handoff only works from git repos with a remote configured"*

A skill usada no passo 7, na íntegra:

```markdown
---
name: review
description: Review recent changes in this repo and report issues
---

Review the working tree's uncommitted changes. List each changed file,
summarize what it does, and flag anything that looks wrong or risky.
Keep it under 10 lines.
```

## Checklist de verificação

- [ ] `devin` roda uma sessão local; `devin --cloud` lista/cria sessões cloud
- [ ] Uma tarefa enviada por `/handoff` completou na nuvem e voltou para sua máquina via `/pickup`
- [ ] Um `SKILL.md` invocado por slash command rodou seu procedimento
- [ ] (Enterprise) o team marketplace serve seu plugin a outro membro

## Armadilhas

- **Local para trabalho paralelo.** O CLI é um agente no seu terminal — para fatias paralelas use sessões cloud ou um Bot; o CLI é a superfície *hands-on*.
- **Dispersão de rules.** `AGENTS.md` + rules de projeto + rules globais interagem por precedência — mantenha cada regra em exatamente uma camada ou elas brigam.
- **`/handoff` precisa de remote.** Num repo sem git remote ele falha na hora — antes, faça push para um lugar que o Devin Cloud consiga clonar.

## Teste de conhecimento

1. Quando usar `/handoff` para o Devin Cloud em vez de terminar localmente? *(Quando o trabalho precisa de paralelismo em escala de nuvem, ferramentas da org, ou roda mais que seu laptop fica aberto.)*
2. Qual a diferença entre skill, rule e plugin? *(Skill é procedimento de tarefa, rule é contexto permanente, plugin é o pacote que envia os dois mais hooks.)*
3. Por que hooks + subagents importam para adoção em equipe? *(Hooks impõem política da org em toda sessão CLI; subagents deixam um operador rodar uma frota — os dois escalam em direções opostas.)*

## Fontes

- [Docs do Devin CLI](https://docs.devin.ai/cli/index.md) — quickstart, comandos, integração cloud, extensibilidade, ACP, modelos
- Relacionado: [Guia 9 — Playbooks & knowledge](playbooks-and-knowledge.md) (mesma camada de convenções, org-wide)
