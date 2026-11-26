# Guia 2 — Bot product-owner

**Objetivo:** um Bot que gere um produto inteiro — abre os próprios tickets, os constrói, mergeia e reporta diariamente.
**Nível:** intermediário · **Carga humana após setup:** ~1 mensagem a cada 6 PRs mergeados
**Implantação de origem:** o **Android Bot** da Cognition — lançou o app Android do Devin no beta aberto do Google Play em **44 dias**: 1.134 PRs mergeados, 344.651 linhas de Kotlin, 2.841 testes de screenshot, 1.217 tickets. Seu humano enviou **183 mensagens no total** (22 dias de silêncio). Hoje é dono do desenvolvimento contínuo do Android e atualiza o app conforme novas features chegam ao iOS.
**Fontes:** [post de lançamento](https://devin.ai/blog/introducing-devin-bots) · [Fortune](https://fortune.com/2026/11/17/exclusive-cognition-bets-on-devin-bots-coding-agents-in-challenge-to-anthropics-duet-and-openais-dots/)

## O padrão

Um Bot é dono de uma *superfície* — um app, um site, um serviço — como um PM a possuiria: decide o que construir, transforma isso em tickets, roda uma sessão por ticket e mantém a superfície viva indefinidamente. O humano atua como o executivo a quem ele se reporta.

```text
Bot ──► abre tickets ──► sessão por ticket ──► PR ──► CI + Devin Review ──► merge
 │                                                                            │
 └──────────── relatório diário + decisões Needs-you ◄────────────────────────┘
```

## Pré-requisitos

- Um repositório que o Bot possa possuir totalmente (repo de app com CI, review e caminho de merge)
- Devin Review habilitado no repo, e checks de CI ligados
- Um app Slack para o Bot (recomendado — toda implantação documentada reporta no Slack)

## Passo 1 — O prompt de resultado

O real, verbatim da Cognition:

```text
your job is to product manage the android app. Basically, you're going to
autonomously create the entire thing, but we need to figure out what the
blockers are for you doing that first.
```

Template reconstruído para sua superfície:

```text
Your job is to product manage <surface>. You're going to autonomously
<build / keep parity with <reference>>, but first enumerate the blockers
to you doing that — where the code lives, how to build and test it, and
how changes merge — then start working through them.
```

Note a forma: **propriedade + autonomia + bloqueadores primeiro**. Não entregue um backlog; entregue um mandato e faça-o trazer à tona o que precisa.

## Passo 2 — Fase um: desbloquear, não construir

O Android Bot não escreveu código primeiro — enumerou bloqueadores: acesso ao repo, comandos de build, como testar num dispositivo/emulador, o caminho de merge. Sua versão dessa lista:

- Ele consegue buildar o projeto na máquina dele? (Dependências de blueprint/snapshot)
- Consegue produzir artefatos instaláveis (APK/TestFlight/deploy de preview)?
- Sabe a política de merge — quais checks devem passar, quem revisa?
- Tem as credenciais necessárias (chaves de loja, assinatura) — ou um pedido de grant documentado para elas?

Deixe-o terminar essa auditoria antes de abrir tickets de produto. Cada bloqueador resolvido aqui é uma sessão travada que você não verá depois.

## Passo 3 — O loop de trabalho

Desbloqueado, o estado estacionário é:

1. O Bot abre um ticket para a próxima unidade de trabalho que decidir
2. Uma sessão filha implementa e abre um PR — pequeno, com prova de que funciona
3. CI + Devin Review fazem o gate do merge
4. O Bot mergeia (ou pergunta quando julgamento é necessário — cai em Needs you)
5. Relatório diário cai no Slack — os relatórios do Android Bot incluem uma **gravação de tela** do que mudou

Configure o reporting nas Instructions do Bot, não no chat:

```text
Every day, post a report in #<channel>: what shipped, what's in flight,
what needs a human. Include a screen recording of visible changes.
```

## Passo 4 — Seu papel como executivo

As 183 mensagens em 44 dias caíram em dois baldes:

- **Chamadas de julgamento** — sign-off de revisão de segurança, um trade-off de design, um cartão de aprovação
- **Direção** — "be more ambitious" é o exemplo documentado

Todo o resto — tickets, implementação, correções, auto-merges — é trabalho do Bot. Se você está respondendo perguntas de implementação, está gerenciando baixo demais. Corrija uma vez → cai na memória → a próxima sessão herda.

## Estado estacionário

Depois do build inicial, o mesmo Bot passa a *possuir* a superfície:

- Mantém paridade com um projeto de referência (o Android Bot hoje acompanha features do iOS)
- Triagem de reports que chegam (atende o feedback do beta do Google Play)
- Captura regressões entre superfícies — o Android Bot achou e corrigiu autonomamente uma quebra no iOS/web causada pela mudança de outra pessoa

## Checklist de verificação

- [ ] A primeira ação do Bot foi uma auditoria de bloqueadores, não um PR
- [ ] Ele abre e trabalha sua própria fila de tickets sem ser pedido
- [ ] PRs são pequenos e carregam prova (testes, screenshots, gravações)
- [ ] Relatório diário posta no Slack com evidência visível
- [ ] Você passou um dia inteiro mandando zero mensagens e PRs ainda mergearam

## Armadilhas

- **Pular a fase de bloqueadores.** Um Bot product-owner que começa a codar antes de conseguir buildar/testar/mergear produz PRs órfãos.
- **PRs grandes.** A segurança da implantação vem de unidades pequenas e verificáveis. Se os PRs incharem, instrua: *"one ticket, one concern, one PR."*
- **Revisar código em vez de direção.** A 30+ PRs/semana você não revisa cada diff — faça gate com CI + Devin Review + a evidência do Bot, e gaste suas mensagens em direção.

## Teste de conhecimento

1. O Android Bot mergeou os próprios PRs — o que tornou isso seguro o bastante? *(Somente PRs aprovados em CI e Devin Review eram mergeados; 2.841 testes de screenshot tornaram "pronto" verificável por máquina, e decisões ambíguas escalavam para o humano.)*
2. Por que abrir tickets em vez de só disparar sessões direto? *(Tickets criam uma fila auditável que o Bot tria por prioridade — e o humano revisa uma fila, não 50 sessões.)*
3. O que "22 dias de silêncio" diz sobre o modelo de controle? *(Escalonamento-por-exceção só funciona quando a definição de pronto do Bot é verificável; o silêncio é a feature, não negligência.)*

## Fontes

- [Introducing Devin Bots](https://devin.ai/blog/introducing-devin-bots) — números e prompt do Android Bot
- [Exclusivo Fortune](https://fortune.com/2026/11/17/exclusive-cognition-bets-on-devin-bots-coding-agents-in-challenge-to-anthropics-duet-and-openais-dots/) — cobertura independente do lançamento sobre Bots, controles de acesso e modelo operacional
- [Russell Kaplan sobre paridade Android/iOS](https://x.com/russelljkaplan/status/2122771093920653493) — paridade mantida sem engenheiros Android
- [Russell Kaplan sobre captura de regressões](https://x.com/russelljkaplan/status/2122803486198988970) — Android Bot detectando regressão no lado iOS/web
- Relacionado: [Guia 4 — Organização multi-Bot](bots-203-multi-bot-org.md) quando uma superfície vira um negócio
