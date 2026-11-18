# Guia 4 — Organização multi-Bot

**Objetivo:** uma hierarquia de Bots que roda uma unidade de negócio inteira — um orquestrador delegando para Bots especialistas, um humano decidindo por uma única thread diária.
**Nível:** avançado
**Implantação de origem:** o **SuperJennyStack** de Jenny Xu — ~20 Bots rodando um estúdio de jogos mobile. ~50 → **1.900 PRs/semana**, releases semanais, receita do estúdio 6×. Publicado como template comunitário no [Bot marketplace](https://devin.ai/bots/templates). O **handoff por grant bot-para-bot** oficial (QA → Developer → reteste → relatório do PM) usa a mesma mecânica em escala menor.
**Fontes:** stack publicado de Jenny Xu ([via cobertura do lançamento](https://x.com/cognition/status/2122737511684587551)) · [docs de Bots](https://docs.devin.ai/work-with-devin/bots) · [post do BotSpeak](https://x.com/xujennyc/status/2123111543105868166)

## O padrão

Não construa um Bot que faz tudo — construa uma pequena empresa:

```text
                    ┌─────────────┐
              ┌────►│ Orquestrador │◄──── uma thread consolidada
              │     └──────┬──────┘      (4×/dia, respostas emoji)
              │            │ grants: leitura + mensagem
     ┌────────┼────────┬───┴─────┬──────────┐
     ▼        ▼        ▼         ▼          ▼
  SuperPM  SuperDev  SuperQA  SuperRelease  SuperSupport
  (o quê)  (constrói)(verifica)(envia)      (usuários)
```

O humano é o CEO: o orquestrador coleta todas as decisões pendentes dos Bots subordinados em **uma thread de Slack, 4×/dia**, respondida com emoji.

## Pré-requisitos

- Guia 1 feito — você sabe criar e instruir um Bot
- Slack conectado — esse padrão vive no Slack; a thread consolidada do orquestrador é toda a UX
- Um domínio delimitado com trabalhos separáveis (um produto, um estúdio, uma área de serviço)

## Passo 1 — Desenhe o organograma primeiro

O stack publicado da Jenny — copie a *forma*, não os nomes:

| Bot | Possui |
| --- | --- |
| Orquestrador (SuperJenny) | Delegação para todos os outros Bots; compila os pedidos deles numa thread; treinada na personalidade/maneirismos dela |
| PM (SuperPM) | Lista diária ranqueada de correções a partir de métricas + reviews da loja + tendências |
| Release (SuperRelease) | Build semanal, pronto para submissão na loja na sexta |
| QA (SuperQA) | Testes em dispositivo real com prova em vídeo |
| Support (SuperSupport) | Rascunha cada resposta a review de loja para aprovação; ajuda jogadores durante a noite |

Os ~15 Bots restantes cobrem desenvolvimento, Unity, UI, iOS, Android, analytics. Regra prática da implantação: **um Bot por cargo que você nomearia num organograma** — não por tarefa, por *responsabilidade*.

## Passo 2 — Crie os especialistas

Para cada cargo, um Bot com prompt de resultado escopado:

```text
You own QA for <product>. Test every release candidate on real devices,
post video proof, and block release on failures. Report what needs a
decision to the orchestrator.
```

Mantenha as Instructions de cada Bot focadas nas regras do seu cargo; conhecimento compartilhado (marca, processo de deploy, quem aprova o quê) vai nas instructions de cada Bot ou num recurso compartilhado — não há memória global entre Bots, então os prompts do orquestrador carregam o tecido conectivo.

## Passo 3 — Ligue os grants

Um grant dá ao Bot A acesso de leitura/mensagem ao Bot B — é assim que Bots passam trabalho entre si (os Bots pedem o grant; você aprova o cartão uma vez). O orquestrador precisa de acesso a todos os especialistas.

A variante oficial documentada — menor, mesma mecânica:

```text
QA Bot acha um bug ──grant──► Developer Bot corrige ──► QA retesta no
staging ──► PM Bot reporta status no canal
```

Aprove grants de forma estreita: o orquestrador lê e manda mensagem aos especialistas; especialistas não precisam todos se alcançar.

## Passo 4 — A thread consolidada

Esta é a instrução mais importante — converte interrupções de 20 Bots num hábito só:

```text
Collect every pending decision from the Bots you work with into one
Slack thread, posted at <times> daily. For each item: what's blocked,
the options, your recommendation. I answer in replies/emoji; treat my
replies as decisions and relay them.
```

Jenny roda isso **4×/dia** e responde **com emoji**. A disciplina: você nunca fala com os especialistas — o orquestrador retransmite sua decisão e a leva até o fim.

## Passo 5 — Cadência = o batimento da org

| Cadência | Quem roda |
| --- | --- |
| Lista diária ranqueada de correções | Bot PM (métricas + reviews + tendências) |
| Release candidate semanal | Bot Release → sign-off do Bot QA |
| Thread de decisões 4×/dia | Orquestrador |
| Ajuda a jogadores durante a noite | Bot Support (rascunha respostas para aprovação matinal) |

Cada Bot é dono do seu loop; o orquestrador é dono da agenda dos loops.

## Passo 6 — Protocolo inter-bot (BotSpeak)

O problema de escala que ninguém te avisa: os 20+ Bots da Jenny mandavam **700+ mensagens/dia** — ela não dava conta. A correção foi o **BotSpeak**, uma linguagem abreviada que economiza tokens e que os Bots usam *entre si* ([o relato dela](https://x.com/xujennyc/status/2123111543105868166)):

| Regra | O que significa |
| --- | --- |
| Abreviações | `ACK` e afins em vez de respostas completas |
| ASD-STE100 | Gramática inglesa simplificada — o padrão de documentação de aviação, sem ambiguidade e barato em tokens |
| Confirmações emoji | Reagir ✅ em vez de "entendi, obrigado" |
| Sem cerimônias | Bots mandam entre si só o que o outro precisa |
| Humano recebe prosa | A thread consolidada continua em frases completas com contexto de decisão |

Seis dias após a troca: decisões tomadas por Bots sem ela **12×**, pedidos repetidos −50%, posts de esclarecimento entre bots −12%. O protocolo existe porque desperdício de tokens não é o custo real — desperdício de *atenção* é: mensagens bot-para-bot mais curtas mantêm a única thread do humano legível.

## Checklist de verificação

- [ ] Todo Bot especialista tem prompt de resultado escopado e grants ativos
- [ ] O orquestrador posta a thread de decisões consolidada no horário
- [ ] Uma decisão que você respondeu por emoji foi retransmitida e resolvida pelo especialista certo
- [ ] Um handoff entre Bots completou ponta a ponta (achar → corrigir → verificar → reportar)
- [ ] Mensagens humanas de hoje < número de PRs mergeados

## Armadilhas

- **Pular o orquestrador.** N Bots cada um te mandando DM é N× ruído. A org só funciona se o julgamento passa por uma thread.
- **Fronteiras de cargo vagas.** "Dev Bot" e "Fix Bot" vão colidir. Fronteiras seguem o organograma — QA *verifica*, Release *envia*, PM *prioriza*.
- **Over-granting.** Grants em malha (todos alcançam todos) recriam o caos. Hub-and-spoke pelo orquestrador.
- **Prosa entre Bots.** Bots escrevendo parágrafos entre si é como se chega a 700 mensagens/dia — adote um protocolo estilo BotSpeak: abreviações + confirmações emoji + sem cerimônias; frases completas só para o humano.

## Teste de conhecimento

1. Por que o SuperJennyStack roteia todo contato humano por *uma* thread consolidada? *(Atenção é o gargalo, não computação — 20 Bots gerando 20 threads são 20 empregos de novo.)*
2. Quando um grant vence "perguntar ao orquestrador"? *(Quando a capacidade necessária já é possuída por outro Bot — grants emprestam propriedade em vez de duplicá-la.)*
3. O que a cadência "4×/dia com emoji" do humano implica sobre a profundidade da delegação? *(Banda de decisão, não headcount, é o que Bots substituem — o humano manteve a camada de julgamento e perdeu a camada de digitação.)*

## Fontes

- [Introducing Devin Bots](https://devin.ai/blog/introducing-devin-bots) — números do SuperJennyStack, variante grant-handoff
- [Bot marketplace](https://devin.ai/bots/templates) — template comunitário SuperJennyStack + 16 templates oficiais
- [Docs de Bots](https://docs.devin.ai/work-with-devin/bots) — grants, memória, acesso
- Relacionado: [Guia 5 — Enxame ancorado em referência](bots-204-reference-grounded-swarm.md) para enxames que *escrevem* em vez de *operar*
