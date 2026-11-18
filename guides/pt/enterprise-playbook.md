# Guia 7 — Padrões de rollout enterprise

**Objetivo:** implantar Devin em escala organizacional usando as formas que já produziram números publicados — não experimentação, as manobras comprovadas.
**Nível:** intermediário (escrito para líderes de engenharia)
**Fonte:** casos de clientes publicados, [devin.ai/customers](https://devin.ai/customers)

Seis formas de implantação, destiladas das empresas que publicaram resultados. A maioria dos rollouts bem-sucedidos usa duas ou três delas, não todas as seis.

## Forma 1 — O motor de migração de legado (Nubank, Comarch)

| | |
| --- | --- |
| Implantação | Nubank: monólito ETL de 8 anos e milhões de linhas → sub-módulos. Comarch: reconstrução de ERP de 20 anos e 10M linhas |
| Resultado | 8–12× eficiência de engenharia, 20× economia de custo (Nubank) |
| Mecanismo | Fazer fine-tune do Devin no *seu* codebase (Nubank cortou ~40 min/tarefa para ~10), depois apontá-lo para a migração como programa contínuo — PRs pequenos rastreados, não uma reescrita |

**Como copiar:** escolha um sistema legado delimitado; faça fine-tune ou ensine via playbook; rode o loop estilo Migration Engineer — uma grande migração como PRs pequenos rastreados com superfície de progresso. O ganho compõe: cada módulo migrado torna a próxima sessão mais esperta.

## Forma 2 — O repo de autor primário (EBANX, Gumroad, Finch)

| | |
| --- | --- |
| Implantação | EBANX: **92% dos PRs mergeados autoria do Devin**. Gumroad: Devin é o **contribuidor nº 1** do repo (1.500+ PRs). Finch: 3.000 PRs, ~20 engenheiro-meses economizados |
| Mecanismo | O Devin não é assistente nesses repos — é o autor padrão. Humanos revisam e direcionam |

**Como copiar:** escolha um repo de alta velocidade; roteie tickets para sessões Devin por padrão; humanos revisam. A métrica a vigiar é a fatia de PRs autorais — acima de ~50%, você está nesta forma; abaixo, ainda em modo piloto.

## Forma 3 — O primeiro respondedor sempre ativo (Modal, Reducto, AngelList)

| | |
| --- | --- |
| Implantação | Modal: **80% dos incidentes investigados antes de um engenheiro abrir a thread**. Reducto: Devin Oncall é o primeiro respondedor; engenheiros raramente paginados. AngelList: Devin acha a causa raiz de 70% dos incidentes antes do engenheiro |
| Mecanismo | Trigger PagerDuty/Slack → sessão investiga com acesso a logs/repo → relatório cai antes do humano acordar |

**Como copiar:** [Devin Oncall](https://docs.devin.ai) ou uma automação disparada por PagerDuty (Guia 6, receita: incidente → investigar). Meça o % de incidentes pré-investigados — cada ponto dele é sono humano recuperado.

## Forma 4 — A frota de manutenção (Airbyte, Melius)

| | |
| --- | --- |
| Implantação | Airbyte: mantém **700+ conectores** rodando. Melius: ~100 PRs/dia |
| Mecanismo | A cauda longa que ninguém quer — podridão de conectores, drift de dependências, flags velhas — roteada a Bots/automações que processam continuamente |

**Como copiar:** enumere seu backlog de manutenção (o trabalho que engenheiros evitam); embrulhe em Bots estilo Code Health Engineer / Code Reaper (templates oficiais) com cadência semanal.

## Forma 5 — O seat org-wide (Wayfair, The Access Group, Citi)

| | |
| --- | --- |
| Implantação | Wayfair: 1.600+ engenheiros all-in. Access Group: Devin em 250 produtos, 2.000+ engenheiros → 5× output. Citi: rollout para 40.000 devs, 30% de corte em gasto com fornecedores de tech |
| Mecanismo | Não mais agentes — o *seat*: todo engenheiro tem acesso ao Devin, playbooks compartilhados, knowledge em nível de org |

**Como copiar:** a ordem de rollout nos casos publicados é consistente — time piloto → resultados medidos → padronização de playbook/knowledge → expansão de seats. Pular a etapa de knowledge é por que rollouts de seat travam: veja o [guia de playbooks](playbooks-and-knowledge.md).

## Forma 6 — O gate de processo (Hamming, Litera, Eight Sleep)

| | |
| --- | --- |
| Implantação | Hamming: Devin escreve 25% do volume de código. Litera: ciclos de regressão cortados em 90%. Eight Sleep: 8× mais entregue |
| Mecanismo | O Devin é dono de um estágio do pipeline — testes de regressão, QA — não do produto inteiro |

**Como copiar:** ache o estágio do pipeline com o pior custo humano (ciclos de regressão, QA); atribua a um Bot ou automação; meça o tempo de ciclo do estágio antes/depois.

## Anti-padrões que os casos implicam

- **Ferramenta, não colega.** As implantações de números altos dão ao Devin propriedade (repos, superfícies, estágios), não atribuições — mesma lição dos Guias 1–5.
- **Piloto eterno.** Todo resultado publicado compartilha um traço: um piloto medido que *se formou*. Defina o critério de formatura antes (fatia de PRs, incidentes cobertos, horas poupadas).
- **Sem camada de knowledge.** Toda implantação grande codifica convenções em algum lugar — fine-tunes, playbooks, instructions de Bot. Sem isso, a qualidade varia por sessão.

## Checklist de verificação

- [ ] Seu doc de rollout nomeia um estágio de pipeline, uma métrica e um critério de formatura — antes da primeira sessão
- [ ] Checkpoint da semana 2: consegue dizer a fatia de PRs mergeados do Devin nesse estágio sem perguntar a ninguém?

## Armadilhas

- **Escalar o piloto que nunca se formou.** Todo número grande aqui veio depois de um piloto medido com critério de saída.
- **Pensar em licença primeiro.** Comprar seats antes de nomear o estágio possuído produz shelfware — o padrão é estágio → piloto → métrica → então seats.

## Teste de conhecimento

1. Por que todas as seis formas compartilham "um estágio possuído" como átomo? *(Todo número publicado veio de uma superfície delimitada e mensurável — orgs que implantaram "em todo lugar" não publicaram nada.)*
2. O que é o critério de formatura e por que defini-lo antes do piloto? *(Uma métrica + limiar que vira piloto → produção; sem ele, pilotos derivam para sempre ou são mortos por impressões.)*
3. Por que a camada de knowledge aparece em toda implantação grande? *(Consistência em escala exige contexto compartilhado — a alternativa é N sessões de qualidade diferente.)*

## Fontes

- [devin.ai/customers](https://devin.ai/customers) — todos os casos e números citados
- [built-with-devin — índice enterprise](https://github.com/Till3005/built-with-devin#enterprise-deployments) — a tabela de casos verificada do registry
