# Guia 17 — Skills e plugins: a camada de empacotamento pós-playbook

**Objetivo:** codificar os procedimentos repetíveis da sua org como `SKILL.md` para que toda sessão e Bot os siga — e empacotar/compartilhar entre repositórios com plugins.
**Nível:** intermediário · a camada que substituiu os playbooks
**Fontes:** [docs.devin.ai/product-guides/skills](https://docs.devin.ai/product-guides/skills) · [release notes](https://docs.devin.ai/release-notes/overview) · complementa o [Guia 9](playbooks-and-knowledge.md)

## Por que skills são a camada que importa agora

Os Playbooks estão migrando para Skills: as contas migram uma a uma e contas novas (a partir de 24-out-2026) só têm Skills — cada playbook vira um skill com o mesmo escopo org/enterprise. Skills também seguem o padrão aberto **Agent Skills**, então os mesmos arquivos funcionam em outros agentes de código. Tudo que você sabia sobre escrever playbooks continua valendo; o que mudou é o formato do arquivo e o modelo de descoberta.

| Artefato | Onde vive | Melhor uso |
| --- | --- | --- |
| Knowledge | Página Customize / notas do repo | Contexto permanente — fatos que Devin não consegue saber |
| Bot instructions | O Bot | Regra do cargo para um "funcionário" |
| Skill | `SKILL.md` no repo, ou num plugin | Um procedimento nomeado e invocável |
| Rule | Plugin | Restrição permanente ("never force-push") |
| Hook | Plugin | Execução determinística em torno de chamadas de ferramenta |

## Passo 1 — Onde os skills ficam

Duas fontes de descoberta, ambas automáticas:

1. **Repositórios** — faça commit de `SKILL.md`; Devin varre os dez caminhos de vendor em todo repo conectado: `.agents/skills/` (recomendado), `.devin/skills/`, `.github/skills/`, `.claude/skills/`, `.cognition/skills/`, `.windsurf/skills/`, `.cursor/skills/`, `.codex/skills/`, `.codeium/skills/`, `.kiro/skills/`. Skills de repo seguem a versão da branch — um clone no meio da sessão é varrido ao terminar.
2. **Plugins** — um plugin empacota skills + rules + MCP servers + hooks, instalado no escopo personal, organization ou enterprise; seus skills entram no contexto antes de qualquer clone.

## Passo 2 — O contrato do SKILL.md

```markdown
---
name: test-before-pr
description: Run the dev server and verify pages before any frontend PR.
argument-hint: <environment>
triggers: ["user"]
allowed-tools: read, grep, glob
permissions:
  allow: ["Exec(npm run *)"]
---

## Setup
1. `docker-compose up -d postgres` && `npm run dev`
## Verify
1. Open each page touched by the diff
2. Screenshot at 1280px and 375px
```

Campos de frontmatter que mudam o comportamento:

- **`description`** — a única coisa que Devin vê no início da sessão; decide a invocação automática. Escreva como gatilho ("verify pages before any frontend PR"), não como resumo.
- **`triggers: ["user"]`** — desativa a invocação automática; use em tudo que é destrutivo (deploys, migrations).
- **`argument-hint`** + `$ARGUMENTS`/`$1` — parametrização: `@skills:deploy staging`.
- **`allowed-tools` / `permissions`** — pré-aprova ou bloqueia ferramentas enquanto o skill está ativo.

## Passo 3 — Três caminhos de invocação

- **Automática:** Devin casa a tarefa com a `description` e carrega o corpo no contexto pelo resto da sessão.
- **Explícita:** `@skills:<nome> [args]` numa sessão ou mensagem ao Bot — o jeito confiável de compartilhar um procedimento com o time.
- **Sugerida:** depois que Devin aprende algo (como subir sua stack), ele propõe um `SKILL.md` na timeline da sessão com botão **Create PR** — aceite. É assim que bibliotecas de skills crescem sem sessões de escrita.

## Passo 4 — Crescendo a biblioteca

- Rode duas sessões em paralelo contra um skill novo; as lacunas aparecem em minutos.
- Quando você corrige Devin no meio da sessão, adicione a correção ao skill — a próxima sessão já começa mais esperta.
- Promova skills provados num repo para um plugin da org — todo repo passa a tê-los sem copiar.

## Passo a passo real — uma skill de repositório invocada de verdade, no Devin CLI v3000.14 (swe-2-flash-medium)

O caminho *explícito* do Passo 3, de ponta a ponta: uma skill `coverage-check` commitada em `.devin/skills/coverage-check/SKILL.md` num repositório demo, depois invocada numa sessão nova. A descoberta funciona como documentado — digitar `/` listou a skill pelo nome, com a `description` como texto do autocomplete.

**Vídeo (60 s, sem áudio):** SKILL.md → autocomplete de barra → `Invoked skill coverage-check` → aprovação → relatório.

[![O relatório da skill — tabelas de cobertura por função de app.py e orders.py](https://till3005.github.io/built-with-devin/assets/guides/skills-and-plugins/walkthrough-poster.webp)](https://till3005.github.io/built-with-devin/assets/guides/skills-and-plugins/walkthrough.mp4)

![1. A skill no disco — name/description no frontmatter, depois um procedimento numerado](https://till3005.github.io/built-with-devin/assets/guides/skills-and-plugins/step1-skill-file.webp)
*1. A skill no disco — `.devin/skills/coverage-check/SKILL.md`: `name`/`description` no frontmatter + procedimento numerado*

![2. Digitar `/` lista a skill — nome + description são a entrada do autocomplete](https://till3005.github.io/built-with-devin/assets/guides/skills-and-plugins/step2-slash-autocomplete.webp)
*2. Digitar `/` lista a skill — a descoberta carrega exatamente nome + `description`*

![3. `Invoked skill coverage-check` — até o primeiro comando espera um Allow](https://till3005.github.io/built-with-devin/assets/guides/skills-and-plugins/step3-invoked.webp)
*3. `Invoked skill coverage-check` — o primeiro comando já precisa de Allow*

![4. O procedimento roda literalmente — unittest, depois lê cada arquivo-fonte e de teste](https://till3005.github.io/built-with-devin/assets/guides/skills-and-plugins/step4-coverage-report.webp)
*4. O procedimento roda literalmente — `python3 -m unittest -v`, depois lê app.py, orders.py e os dois arquivos de teste*

![5. Resultado: cobertura total — tabelas por função citando cada branch; nenhum arquivo modificado, sem commits](https://till3005.github.io/built-with-devin/assets/guides/skills-and-plugins/step5-full-coverage.webp)
*5. Resultado: cobertura total — cada branch contabilizada, exatamente o relatório que a SKILL.md pediu*

## Governar plugins e acesso MCP

- **Offered versus Required é uma escolha do admin.** Admins de organização e enterprise podem marcar um plugin do marketplace como **Offered** em vez de **Required**. Required faz parte da base administrada; Offered é opcional para membros. Não marque um pacote de conveniência como Required — isso amplia a base administrada herdada por todos os membros.
- **Use a aprovação MCP mais estreita.** Os cartões de aprovação de ferramentas MCP agora incluem **Allow for this session**. Prefira essa opção quando a tarefa precisa repetir a ferramenta, mas a permissão deve morrer com a sessão; deixe aprovações mais amplas para ferramentas já auditadas.
- **API keys ficam em secrets.** Headers em branco em servidores MCP de marketplace com API key são vinculados a secrets, e secrets não usados são sinalizados. Mantenha chaves cruas fora de configuração de plugin, prompts e chat.
- **Automatic não significa sem autenticação.** Novos servidores MCP customizados começam com autenticação **Automatic** selecionada. Verifique o que o servidor realmente negocia antes de conectá-lo a escopos de produção.

## Checklist de verificação

- [ ] Uma sessão nova lista seu skill pelo nome (name + description carregam no início)
- [ ] `@skills:<nome>` executa o procedimento literalmente, com argumentos substituídos
- [ ] Um skill `triggers:["user"]` nunca dispara sozinho
- [ ] Um skill de plugin está disponível antes do repo terminar de clonar

## Armadilhas

- **Especificar demais.** Comandos/flags/strings específicos são o ponto; prosa rígida não é. Skills que narram cada decisão tiram a capacidade do Devin de se adaptar no meio do caminho.
- **Escrever o corpo e esquecer a description.** A invocação automática depende da description; um corpo ótimo com description vaga nunca dispara.
- **Deixar skills destrutivos auto-invocarem.** Deploys e migrations ficam atrás de `triggers:["user"]` ou de um `permissions.ask` explícito.
- **Guardar segredos em skills.** Um skill é lido por toda sessão no escopo — credenciais vão no secrets store, referenciadas como `$VAR`.

## Teste de conhecimento

1. Por que a `description` importa mais que o corpo do skill? *(É o único texto carregado no início da sessão — dirige a auto-invocação; o corpo só carrega depois que o skill é escolhido.)*
2. Quando um procedimento deve ser um plugin skill e não um repo skill? *(Quando todo repo/sessão do escopo precisa dele — plugins carregam antes do clone e não derivam por branch.)*
3. Como tornar seguro um skill com passos destrutivos? *(`triggers:["user"]` para invocação só explícita, mais `permissions.ask` nos matchers das ferramentas perigosas.)*

## Fontes

- [Docs de Devin Skills](https://docs.devin.ai/product-guides/skills) — formato, caminhos de descoberta, frontmatter
- [Release notes](https://docs.devin.ai/release-notes/overview) — migração playbooks→Skills, página Customize
- Relacionado: [Guia 9 — Playbooks & knowledge](playbooks-and-knowledge.md) (a camada de contexto ao lado dos skills)
- [Release notes — 23 nov 2026](https://docs.devin.ai/release-notes/overview) — plugins Offered, aprovação MCP por sessão, headers de API key ligados a secrets, padrão Automatic auth
