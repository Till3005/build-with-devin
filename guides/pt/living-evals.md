# Guia 15 — Living evals a partir de traces de produção

**Objetivo:** uma suíte de evals para *seu* agente que se escreve sozinha — um Devin agendado que lê conversas reais de produção, reconstrói cada falha numa cópia completa do seu sistema e abre PRs que adicionam a falha como teste de regressão.
**Nível:** avançado
**Implantação de origem:** **Living Evals da Rox** — ninguém na Rox escreve evals à mão mais. Um Devin semanal lê traces de produção no Braintrust, reconstrói cada falha numa cópia completa da Rox semeada com dados sintéticos, repete o request até o agente cometer o mesmo erro e abre um PR. A suíte cobre **72% do uso real vs. 43–57%** dos seus evals escritos à mão, e continua crescendo semana a semana.
**Fontes:** [write-up Living Evals](https://www.rox.com/articles/living-evals-an-eval-suite-that-grows-from-production) (Brian Xu, out 2026) · [thread de lançamento](https://x.com/rox_ai/status/2110779380666617997)

## O padrão

```text
traces de produção (plataforma de observabilidade)
        │  amostra semanal (~350 conversas)
        ▼
agrupar em comportamentos (goal · output · mutation · target)
        │  centenas de conversas → ~130 comportamentos
        ▼
para cada comportamento sub-coberto:
   sintetizar dados → preview env de cópia completa → replay do request
   → comparar com o trace de produção → congelar como eval → abrir PR
        ▼
humano revisa o PR, não a escrita do eval
```

## Pré-requisitos

- Um agente ou feature de IA em produção, com **tracing em nível de conversa** (a Rox usou Braintrust; LangSmith/logging self-hosted funcionam — você precisa do request + os registros + as tool calls tocadas)
- Uma cópia deployável do seu sistema (preview env, staging ou `docker compose up` numa VM) — **não mocks**
- Testes-como-código no seu repo para que um eval seja só um arquivo commitado

## Passo 1 — Torne um trace replayable à mão

Antes de agendar qualquer coisa: escolha uma conversa real onde seu agente falhou. Peça ao Devin para puxar o trace, escrever dados sintéticos cobrindo exatamente o que o request tocou, subir sua cópia do sistema e replayar o request até a mesma falha ocorrer. Se você não conseguir reproduzir uma falha manualmente, o loop semanal não produzirá nada.

## Passo 2 — Congele como eval, não como bug report

O artefato é um eval commitado, não uma mensagem no Slack. Convenção da Rox: o request é copiado **palavra por palavra** da produção; os dados semeados reproduzem as condições exatas (ex.: "a reunião mais nova não tem transcrição"). Requests que mudam dados ganham uma asserção de código; requests só de resposta ganham uma rubrica de LLM-judge.

## Passo 3 — Agrupe por comportamento antes de escalar

Rodar o loop em toda conversa é desperdício — a maioria dos requests repete as mesmas formas. Os quatro rótulos da Rox definem um *comportamento*: **goal** (o que o usuário quer) · **output** (o que volta) · **mutation** (nada/criar/editar/enviar) · **target** (objeto nomeado vs. inferido). ~350 conversas por semana colapsam para ~130 comportamentos; construa evals só para comportamentos sub-cobertos.

## Passo 4 — Encode o procedimento inteiro como um skill

O loop trace→eval vive em **um arquivo de skill** que o Devin segue: puxar trace → sintetizar → preview env → replay → comparar → congelar → PR. Quando o loop produz um eval ruim, **corrija o skill**, nunca patcheie o eval à mão — essa é a jogada que compõe.

## Passo 5 — Agende semanalmente

Automação cron (Guia 6): puxar os traces da semana → agrupar → para cada comportamento sub-coberto rodar o loop → abrir um PR com os novos evals. Humanos revisam o PR; o Devin é dono da suíte.

## Checklist de verificação

- [ ] Uma falha real de produção replaya deterministicamente no seu preview env — mesmo request do usuário, mesmo resultado ruim
- [ ] O arquivo de eval está no seu repo, roda na CI e falha no comportamento antigo / passa na correção
- [ ] A cobertura é medida contra o *mix de tráfego de produção*, não seus palpites — reporte como os 72% da Rox
- [ ] Um eval ruim foi corrigido editando o skill, não o eval

## Armadilhas

- **Replay mockado.** A abordagem anterior da Rox replayava através de uma camada de dados mockada — mocks podem esconder bugs justamente no código que substituem. Use uma cópia completa; o ponto de um preview env é fidelidade.
- **Julgamento flakey.** Mesmo sem mudança de código, ~1 em 8 evals passa em algumas execuções e falha em outras — agentes não são determinísticos. Leia uma falha antes de confiar nela; não alerte em flakes isolados.
- **Evals medindo gosto.** A suíte pega regressões comportamentais (um caminho de tool morto, um request suportado não tratado), não estilo — toda falha deve apontar para um defeito corrigível.

## Teste de conhecimento

1. Por que replayar numa cópia completa em vez de uma camada de dados mockada? *(Mocks podem esconder bugs no código que substituem — conforme o agente edita mais estado, o mock se torna a coisa que você está realmente testando.)*
2. Por que agrupar conversas em comportamentos antes de escrever evals? *(A maioria dos requests repete formas — rotular goal/output/mutation/target permite que um eval cubra muitas conversas, então a cobertura mapeia para uso real.)*
3. Qual é a jogada que compõe: corrigir evals ou corrigir o skill? *(O skill — um eval patcheado à mão não ensina nada ao Devin; um skill corrigido produz evals melhores para sempre.)*

## Fontes

- [Living Evals: an eval suite that grows from production](https://www.rox.com/articles/living-evals-an-eval-suite-that-grows-from-production) — a metodologia completa
- [Thread de lançamento da Rox](https://x.com/rox_ai/status/2110779380666617997)
- Relacionado: [Guia 13 — Cookbook oficial](official-cookbook.md) · [Guia 6 — Automações](automations-101-event-driven.md)
