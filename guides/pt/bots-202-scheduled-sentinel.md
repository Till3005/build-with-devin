# Guia 3 — Bot sentinela agendado

**Objetivo:** um Bot dono de uma checagem de qualidade recorrente — roda no horário, tria falhas, rastreia até a causa e envia correções.
**Nível:** intermediário
**Implantação de origem:** o **Layout Bot** da Cognition — vigia regressões de layout-shift no app web do Devin. A cada 3 horas builda o `main` de produção, simula visitas de primeira/repetida/requisições atrasadas, e envia correções. **159 PRs em 3 semanas; lag −70%.**
**Fontes:** [post de lançamento](https://devin.ai/blog/introducing-devin-bots) · [docs de Automations](https://docs.devin.ai/product-guides/automations)

## O padrão

Algum trabalho nunca termina — recorre no relógio: orçamentos de performance, regressão visual, frescor de dependências, scans de segredos, uptime. Um Bot sentinela é dono *da própria checagem*, não só das correções: mantém a checagem funcionando conforme o código muda, filtra ruído e só abre correção quando a regressão é real.

```text
cron ──► Bot acorda ──► roda a checagem sob condições realistas
                              │
                 pass ────────┴──────── fail
                  │                       │
                quieto          reexecuta para filtrar flakes
                                          │
                                rastreia até o PR que introduziu
                                          │
                             PR de correção + evidência antes/depois
```

## Pré-requisitos

- Uma checagem que rode na máquina do Bot (build, suite de testes, Lighthouse, script custom)
- Devin Bot criado (Guia 1) ou uma Automation (Guia 6) — ambos funcionam; um Bot adiciona julgamento entre execuções

## Passo 1 — O prompt de resultado

Reconstruído do comportamento documentado do Layout Bot:

```text
Your job is to keep <surface> from <regressing>.

Watch <check/channel>, where <the check> posts every <interval>. Take over
that check and keep it working as the code changes. When something
regresses: rerun to rule out flakiness, trace the regression to the PR
that introduced it, and open a fix PR with before/after evidence.
```

Exemplos para o slot `<check>`, todos vistos em implantações reais:

- medição de layout-shift em requisições primeiras/repetidas/atrasadas (Layout Bot)
- latência p95 nos seus 5 endpoints mais lentos (template Latency Optimizer)
- varredura `npm audit`/CVE (template Code Health Engineer)
- detecção de código morto (template Code Reaper)

## Passo 2 — Agendar

Peça ao Bot no chat:

```text
Run this check every 3 hours on a schedule.
```

O Bot propõe uma automação; você aprova uma vez. (O Guia 6 cobre automações feitas à mão, se preferir ligar o cron você mesmo.) Gerencie depois em Settings → Automations do Bot.

## Passo 3 — Condições realistas importam

A checagem do Layout Bot não é uma execução — simula **primeira visita, visita repetida e requisições individualmente atrasadas**, porque a regressão que ele caça só aparece sob formas de carga específicas. Codifique seu equivalente:

- Qual ambiente — o Bot builda o `main` de produção na própria VM, não num dev server
- Quais inputs — cache frio vs. quente, dados semeados, ordenação realista de requisições
- Qual limiar — um número, não "parece mais lento"

## Passo 4 — Disciplina de ruído

Duas regras impedem um sentinela de gritar lobo:

1. **Reexecutar antes de agir** — o Layout Bot reexecuta resultados que parecem flaky antes de tratá-los como reais. Escreva no prompt: *"rerun any failed check once before acting on it."*
2. **Rastrear antes de corrigir** — cada regressão é rastreada até o PR que a introduziu. Uma correção sem causa é um palpite.

## Passo 5 — Evidência em cada correção

Cada um dos 159 PRs carrega **vídeo antes/depois**. Evidência equivalente para sua checagem:

| Checagem | Evidência no PR de correção |
| --- | --- |
| Layout/visual | Gravação de tela ou screenshots, antes vs. depois |
| Latência | Números de tempo, mesma medição nos dois sentidos |
| Código morto | Por que o código é inalcançável |
| Dependências/CVEs | O advisory + o diff que o resolve |

## Checklist de verificação

- [ ] Automação existe e dispara no cron definido (Settings → Automations mostra execuções)
- [ ] Uma regressão semeada produz um PR de correção com evidência antes/depois
- [ ] Uma execução flaky produz uma reexecução, não uma correção
- [ ] A própria checagem é mantida — quando o app mudou embaixo dela, o Bot atualizou a checagem

## Armadilhas

- **Ser dono das correções mas não da checagem.** Se sua checagem quebra e ninguém nota por uma semana, o Bot era dono da coisa errada — o prompt deve atribuir a própria checagem.
- **Cron sem julgamento.** Uma automação agendada simples consegue rodar a checagem; um Bot decide se a falha é real. Use automação simples só para checagens sem triagem (Guia 6).
- **Saída só de alerta.** Um sentinela que reporta "regressão encontrada" num canal cria trabalho para humanos. O valor da implantação é que ela *corrige* — cobre isso dela.

## Teste de conhecimento

1. Por que o sentinela builda o `main` de produção em cron em vez de esperar falhas serem reportadas? *(O resultado é "sem regressões", não "consertar bugs reportados" — propriedade significa achar problemas antes dos humanos.)*
2. O Layout Bot envia correções com vídeos antes/depois — que decisão isso habilita para o revisor? *(Confiança para mergear sem reproduzir localmente; a prova viaja com o PR.)*
3. Por que rastrear uma regressão até o PR que a introduziu em vez de corrigir o sintoma? *(Ser dono de uma checagem é ser dono do seu histórico — a correção cai na causa e o conhecimento persiste.)*

## Fontes

- [Introducing Devin Bots](https://devin.ai/blog/introducing-devin-bots) — mecânica e números do Layout Bot
- [Automations — docs](https://docs.devin.ai/product-guides/automations) — agendamentos, triggers, condições
- Relacionado: [Guia 6 — Automações orientadas a eventos](automations-101-event-driven.md) para a versão sem Bot desse loop
