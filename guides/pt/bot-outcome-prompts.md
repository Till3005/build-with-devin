# Prompts de resultado para Bots, dissecados

**Objetivo:** escrever prompts de resultado do jeito que as implantações documentadas realmente fizeram — propriedade de uma área, não uma lista de tarefas.
**Nível:** intermediário · **Tempo:** 20 min para rascunhar, uma semana para calibrar
**Fonte:** [Introducing Devin Bots](https://devin.ai/blog/introducing-devin-bots) + [documentação de Bots](https://docs.devin.ai/work-with-devin/bots) + relatórios de implantação em [built-with-devin](https://github.com/Till3005/built-with-devin#documented-deployments)

Toda implantação pública de bot que produziu números grandes começou com um prompt curto atribuindo um *resultado*. Este guia coleta os reais e faz engenharia reversa do porquê funcionam.

## O exemplar

> *"your job is to product manage the android app"*

Toda a atribuição do Android Bot. Uma frase produziu 44 dias de trabalho auto-dirigido: o bot decompôs o resultado em tickets que ele mesmo escreveu, rodou uma sessão Devin por ticket e entregou 1.134 PRs mergeados ([post de lançamento](https://devin.ai/blog/introducing-devin-bots)). Note o que o prompt **não** contém: sem lista de tickets, sem critérios de aceite, sem agenda. O resultado em si implica todos eles.

## A anatomia de um prompt de resultado que funciona

| Elemento | O que faz | Exemplo |
| --- | --- | --- |
| **Um papel** | Diz ao bot como *se comportar*, não só o que produzir | "product manage", "own the QA of onboarding flows" |
| **Uma superfície delimitada** | Um escopo que o bot consegue ver por inteiro — um app, uma checagem, uma fonte de dados | "the android app", "layout regressions", "30+ onboarding flows" |
| **Uma definição de pronto implícita** | Um estado contra o qual o bot pode se verificar | "feature parity with iOS", "no layout-shift regressions", "every flow green" |
| **Autoridade permanente** | O bot decide *quando* e *o que depois* — é isso que o torna um bot, não um script | "your job is to…", "keep…", "watch for…" |

## Padrões do marketplace oficial de templates

Os 18 [templates do marketplace](https://devin.ai/bots/templates) seguem todos a mesma gramática. Formulações reutilizáveis, generalizadas:

**Propriedade de um domínio** — "Find bugs, improvements, performance and refactoring work in a named product area; open one small PR at a time with proof it works." (Software Factory)

**Propriedade de uma checagem** — "Every 3 hours, build production main, simulate first/repeat/deferred visits, and file fixes with before/after videos for any regression you introduce—or find." (padrão Layout Bot)

**Propriedade de um estágio do ciclo de vida** — "Take a ticket or an ask to a tested PR and through review." (Product Engineer)

**Propriedade de uma cadência** — "Weekly: remove dead code, one safe PR per round." (Code Reaper) — resultados agendados são declarados como ritmo, não como gatilho.

**Propriedade do metabolismo do time** — "Watch the channels, post updates, hand work to the right teammate, follow up until done." (Chief of Staff)

**Propriedade da higiene** — "Old flags, stale deps, CVEs — turned into small safe PRs." (Code Health Engineer)

## Orgs multi-bot: prompts que concedem autoridade

Em frotas (SuperJennyStack, Frankie, tigsbot) o prompt do bot chefe contém o *contrato de roteamento*: qual bot possui qual superfície, e quando escalar para cima em vez de para o lado. O verdadeiro prompt do humano é a spec da thread consolidada: "bring me every open decision in one thread." Veja o [Guia 4](bots-203-multi-bot-org.md) para o organograma completo.

## Anti-padrões

- **Prompts em formato de tarefa.** "Fix these 12 issues" — o bot termina e fica ocioso; você ganha uma sessão, não um bot.
- **Resultados não verificáveis.** "Make the app better" — sem auto-checagem, a única saída do bot é spam de Needs-you.
- **Escopo oculto.** Se o resultado exige sistemas que o bot não vê (um staging que não alcança, um dashboard que não lê), ele ou trava ou alucina progresso. Dê a superfície ou encolha o resultado.
- **Sem história de autoridade de merge.** Os 88% de auto-merge existem porque CI e gates de review foram pré-configurados para merges autônomos. Declare: "merge when CI is green and diff < N lines" ou "always open as draft for human review."

## Redigindo o seu — o teste das três linhas

Um bom prompt de resultado responde, em ordem:

1. **O que é seu?** — a superfície
2. **Como é "bom"?** — o estado verificável
3. **O que você faz a respeito?** — o comportamento permanente

Se um estranho não conseguisse checar a verdade da linha 2 de fora, aperte-a.

## Checklist de verificação

- [ ] Pegue um item real do backlog do seu repo e reescreva como prompt de resultado — superfície, estado verificável, comportamento permanente
- [ ] Mostre a alguém que não conhece o codebase: conseguiria dizer de fora quando o Bot está "vencendo"?
- [ ] A primeira resposta do Bot deve ser um plano ou perguntas de esclarecimento sobre escopo — se perguntar "o que você quer que eu faça primeiro", o prompt não atribuiu propriedade

## Armadilhas

- **Uma lista de tarefas vestindo fantasia de resultado.** "Do X, then Y, then Z" ainda é checklist — o Bot não pode repriorizar quando o mundo muda.
- **"Keep the app good" sem definição de bom.** Sem estado verificável, o Bot escolhe uma — e não será a sua.
- **Escopo mais largo que uma superfície.** "Own engineering" falha; "own the iOS app" entrega. Divida pelo que um único estranho conseguiria observar por inteiro.

## Teste de conhecimento

1. Por que "own the Android app" funciona melhor que "fix Android bugs"? *(Propriedade implica julgamento permanente — o Bot decide quais bugs importam, não só se deve corrigir.)*
2. O que há de errado com "make the CI fast"? *(Não verificável de fora — sem limiar. "CI under 8 minutes" é.)*
3. Qual das três perguntas "text me if tests fail" responde? *(Comportamento permanente — diz o que o Bot faz sobre o estado, nada sobre a superfície ou a meta.)*

## Demonstração — prompt de resultado vs prompt de tarefa, lado a lado, no Devin CLI v3000.14 (swe-2-flash-medium)

Bots exigem plano Max ou Teams — mas a *mecânica de prompt* deste guia independe da superfície, então gravamos na cota gratuita do CLI SWE-2. Mesmo repositório (`orders.py` com uma suíte-base de 2 testes), dois checkouts idênticos, um prompt em cada:

- **Em forma de tarefa:** "Add a test for apply_discount('SAVE10') returning 90.0 and one for total([]) returning 0 …"
- **Em forma de resultado:** "Your job is to own the test coverage of orders.py. Good looks like: every branch … has a test, and python3 -m unittest -v is all green."

**Vídeo (64 s, sem som):** baseline → execução por tarefa → +6 linhas → execução por resultado → mapa de cobertura decomposto pelo agente → +37 linhas.

[![Relatório da execução por resultado — 13 testes verdes, cobertura de branches enumerada pelo agente](https://till3005.github.io/built-with-devin/assets/guides/bot-outcome-prompts/walkthrough-poster.webp)](https://till3005.github.io/built-with-devin/assets/guides/bot-outcome-prompts/walkthrough.mp4)

![1. Prompt em forma de tarefa na baseline — 2 testes, só itens nomeados](https://till3005.github.io/built-with-devin/assets/guides/bot-outcome-prompts/step1-task-prompt.webp)
*1. Prompt-tarefa — o agente recebe uma lista de compras*

![2. Execução-tarefa concluída — exatamente os 2 testes nomeados, 4 verdes, "Nothing committed", e parou](https://till3005.github.io/built-with-devin/assets/guides/bot-outcome-prompts/step2-task-done.webp)
*2. Tarefa: fez a lista e parou — uma sessão, não um dono*

![3. Prompt em forma de resultado numa cópia idêntica — papel, superfície delimitada, estado verificável, sem lista](https://till3005.github.io/built-with-devin/assets/guides/bot-outcome-prompts/step3-outcome-prompt.webp)
*3. Resultado: papel + superfície delimitada + definição de "bom" — sem checklist*

![4. O diff produzido pelo prompt de resultado — o agente enumerou sozinho cada branch](https://till3005.github.io/built-with-devin/assets/guides/bot-outcome-prompts/step4-outcome-diff.webp)
*4. +39 linhas sem ninguém dizer quais testes — ele nomeou cada branch sozinho*

![5. O relatório é um estado, não um checklist — "All 13 tests pass. Branch coverage: …"](https://till3005.github.io/built-with-devin/assets/guides/bot-outcome-prompts/step5-coverage-report.webp)
*5. Ele verifica contra a definição de "bom" e reporta o mapa de cobertura*

![6. Lado a lado — prompt-tarefa: +6 linhas; prompt-resultado: +37. Mesmo modelo, mesmo repo](https://till3005.github.io/built-with-devin/assets/guides/bot-outcome-prompts/step6-side-by-side.webp)
*6. Mesmo modelo, mesmo repo, só muda a forma do prompt: +6 vs +37 — e 4 vs 13 testes*

## Fontes

- [Introducing Devin Bots](https://devin.ai/blog/introducing-devin-bots) · [Docs de Bots](https://docs.devin.ai/work-with-devin/bots) · [Marketplace de templates](https://devin.ai/bots/templates)
- Relatos de implantação ligados no [built-with-devin](https://github.com/Till3005/built-with-devin#documented-deployments)
