# Guia 6 — Automações orientadas a eventos

**Objetivo:** ligar eventos externos — Slack, Teams, GitHub, Linear, Jira, PagerDuty, cron, webhooks — a sessões Devin que se iniciam sozinhas.
**Nível:** comece aqui (guia de plataforma) · **Tempo:** ~20 minutos
**Fonte:** [docs de Automations](https://docs.devin.ai/product-guides/automations) · [walkthrough oficial em vídeo](https://www.youtube.com/watch?v=6xxKtIpgOyE)

## A anatomia

Toda automação tem quatro partes:

| Parte | O que faz |
| --- | --- |
| Trigger | O evento que a dispara — uma mensagem de Slack, um CI que falhou, um tick de cron, um webhook HTTP |
| Conditions | Filtros opcionais — só a label `bug`, só este repo, só mensagens contendo `/devin` |
| Preflight check | Filtro LLM ou script opcional que roda *após* o match, antes das ações — pode pular o evento ou dividi-lo em itens de trabalho |
| Action | O que roda: iniciar uma sessão, mandar mensagem a uma sessão existente, monitor de triagem ou notificação por email |

## Catálogo de triggers

| Fonte | Dispara em | Uso canônico |
| --- | --- | --- |
| Slack | Nova mensagem, reação adicionada, menção a user-group | Triagem de `#incidents`; reação 🚨 → investigar |
| Microsoft Teams | Mensagem, reação | Responder a bug reports na thread onde foram postados |
| GitHub | Issue, comentário em issue, PR, review de PR, check run, push | Auto-corrigir CI falhando; comentário `/devin` → sessão |
| GitLab | MR, comentário em MR, issue, push, pipeline | Corrigir pipelines falhando |
| Linear | Issue criada/etiquetada/status/prioridade/atribuída/movida | Implementar tickets quando atribuídos ao Devin |
| Jira | Issue criada/atualizada/etiquetada/status/atribuída/comentada | O mesmo, em formato Jira |
| Pylon | Issue criada/etiquetada/status | Triagem de bugs de clientes |
| PagerDuty | Incidente disparado/reconhecido/resolvido | Investigar incidentes de alta urgência na hora |
| Schedule | Cron ou único | Varredura diária do Sentry, updates semanais de deps, smoke tests noturnos |
| Webhook | Qualquer POST HTTP | Todo o resto — Datadog, Sentry, seus próprios sistemas |

Múltiplos triggers numa automação funcionam como OU — ex.: disparar *ou* num CI falhando do GitHub *ou* numa reação de Slack.

## Receita 1 — `/devin` em qualquer issue

O trigger mais implantado no mundo:

```text
Trigger:   GitHub → issue comment, repo = your/repo
Condition: comment body starts with "/devin"
Action:    Start session — prompt includes the event payload
```

Resultado: qualquer pessoa da equipe comenta `/devin investigate this` numa issue, e uma sessão assume com a thread inteira como contexto.

## Receita 2 — Auto-reparo de falha de CI

```text
Trigger:   GitHub → check run, repo = your/repo
Condition: conclusion = failure
Action:    Start session: "CI check <name> failed on this commit.
            Diagnose the failure from the logs, fix it, and push to
            the same branch."
```

O payload do evento carrega o check que falhou + commit para dentro da sessão — sem copiar e colar.

## Receita 3 — Varredura agendada

```text
Trigger:   Schedule → daily 09:00
Action:    Start session: "Sweep yesterday's Sentry issues in
            <project>. File the top 3 by impact as tickets and
            start the most actionable one."
```

Loops de higiene diários (varreduras do Sentry, updates de dependências, smoke tests) são as automações de maior ROI — transformam "alguém devia checar" em "está checado".

## Tipos de ação, como escolher

| Ação | Use quando |
| --- | --- |
| Start session | O padrão — cada evento ganha uma máquina e contexto novos |
| Message session | Uma sessão de longa vida mantém estado — alimente eventos nela (a semente de um Bot) |
| Triage Devin | Um Devin persistente vigia um canal inteiro de Slack e cria investigações filhas (ver Devin Oncall para incidentes) |
| Email notification | Só avisar que rodou |

**Automação vs. Bot:** automações são canos burros — evento entra, sessão sai. Um Bot adiciona memória, julgamento e planejamento multi-sessão em volta dos mesmos triggers. Comece com automações; formate para um Bot quando o trabalho precisar de continuidade (Guias 2–5).

## Construir

Quatro caminhos de criação na página de Automations, no dropdown **Create automation**:

1. **Create manually** — o editor em branco: escolha trigger → conditions → action
2. **Create from template** — a galeria de automações pré-configuradas para workflows comuns
3. **Create with Devin** — descreva em linguagem simples (*"when a CI check fails on my-org/my-repo, have Devin fix it and push to the same branch"*); uma sessão pergunta a configuração e apresenta a automação montada para aprovação
4. **Ask Devin for suggestions** — Devin escaneia seus repos e propõe automações que valem a pena

Notas que mordem as pessoas:

- Triggers de Slack precisam do Devin convidado para o canal **e** seu Slack pessoal conectado em Settings → Connections
- Canais privados do Teams só disparam em @menção
- Um trigger de GitHub precisa nomear um repo específico
- Gerencie automações declarativamente com o **provider Terraform** se você roda muitas
- A API v3 de criação de sessão aceita `memory_enabled: false` — a sessão criada (e suas filhas) roda com memória desligada, para automações que não devem carregar contexto aprendido entre execuções

## Passo a passo real — uma automação criada, disparada e verificada no Devin Desktop v3.14 (plano Pro)

O caminho *Create with Devin* de ponta a ponta: descrever uma varredura semanal de changelog em linguagem simples → responder às perguntas de configuração → aprovar a automação gerada → disparar manualmente → e ver um relatório real chegar.

**Vídeo (5 min, sem áudio, 4× velocidade):** página de Automations → sessão geradora → cartões de aprovação → disparo manual → relatório.

[![O cartão de opções da sessão geradora — ela já conhece as automações existentes da conta](https://till3005.github.io/built-with-devin/assets/guides/automations-101-event-driven/walkthrough-poster.webp)](https://till3005.github.io/built-with-devin/assets/guides/automations-101-event-driven/walkthrough.mp4)

![1. A página Automations — automações existentes e o dropdown Create automation](https://till3005.github.io/built-with-devin/assets/guides/automations-101-event-driven/step1-automations-page.webp)
*1. A página Automations — automações existentes e o dropdown Create automation*

![2. Quatro caminhos de criação — Create manually / from template / with Devin / ask for suggestions](https://till3005.github.io/built-with-devin/assets/guides/automations-101-event-driven/step2-create-options.webp)
*2. Quatro caminhos de criação — Create manually / from template / with Devin / ask for suggestions*

![3. A sessão geradora faz perguntas certeiras — já lista suas automações existentes](https://till3005.github.io/built-with-devin/assets/guides/automations-101-event-driven/step3-generate-options.webp)
*3. A sessão geradora faz perguntas certeiras — já conhece suas automações existentes*

![4. Toda criação passa por um cartão de aprovação — trigger, escopo, run-as e política de rede à mostra](https://till3005.github.io/built-with-devin/assets/guides/automations-101-event-driven/step4-approve-card.webp)
*4. Toda criação passa por um cartão de aprovação — trigger, escopo, run-as e política de rede à mostra*

![5. Automação criada — semanal sexta 10:00 CST, relatório somente-leitura, notificação por email](https://till3005.github.io/built-with-devin/assets/guides/automations-101-event-driven/step5-created.webp)
*5. Automação criada — semanal sexta 10:00 CST, relatório somente-leitura, notificação por email*

![6. O disparo manual — mesmo portão de cartão de aprovação; a sessão gerada aparece na barra lateral](https://till3005.github.io/built-with-devin/assets/guides/automations-101-event-driven/step6-manual-run.webp)
*6. O disparo manual — mesmo portão de cartão de aprovação; a sessão gerada aparece na barra lateral*

![7. Um tropeço honesto — o clone via proxy git da sessão gerada retornou 403 (duas vezes); adicionar github.com à política de rede + fallback de clone anônimo resolveu](https://till3005.github.io/built-with-devin/assets/guides/automations-101-event-driven/step7-403-fix.webp)
*7. Um tropeço honesto — o clone via proxy git da sessão gerada retornou 403 (duas vezes); a correção foi adicionar github.com à política de rede + fallback de clone anônimo — sessões de automação não herdam automaticamente o acesso git do seu shell*

![8. A saída verificada — um changelog categorizado real dos 103 commits da semana, entregue como artifact](https://till3005.github.io/built-with-devin/assets/guides/automations-101-event-driven/step8-report.webp)
*8. A saída verificada — um changelog categorizado real dos 103 commits da semana, entregue como artifact*

## Checklist de verificação

- [ ] Dispare o trigger manualmente uma vez (comente `/devin test`, ou faça push de um commit que falha) e veja uma sessão iniciar com o payload do evento
- [ ] Um evento que não bate (label errada, canal errado) não faz nada
- [ ] A saída da ação cai onde você esperava (PR, thread de Slack, ticket)

## Armadilhas

- **Loops.** Uma automação cuja saída pode re-disparar a si mesma (o Devin comenta num PR, o trigger vigia "novo comentário") queimará sessões para sempre. Filtre por autor, label ou subtipo de evento.
- **Tempestades de trigger.** Um webhook que dispara por commit em vez de por PR pode criar 50 sessões num dia movimentado. Controle: uma automação por *unidade reivindicável* de trabalho, não por evento bruto.
- **Sem gate de aprovação.** Auto-mergear ou auto-deployar num trigger pula o ponto de controle humano — mantenha o padrão "a sessão abre um PR, uma pessoa mergeia" a menos que tenha motivo medido para não ter.

## Teste de conhecimento

1. Um colega quer que o Devin "vigie toda notificação do GitHub" — o que você pede para ele estreitar primeiro? *(Qual subtipo de evento realmente implica trabalho acionável — uma label aplicada, uma review solicitada — não toda notificação.)*
2. Por que um evento que não bate deve produzir *nenhuma* sessão em vez de uma sessão que decide fazer no-op? *(Sessões custam ACUs; filtrar upstream é grátis, filtrar dentro da sessão não é.)*
3. Quando uma automação precisa de um Bot? *(Quando o trabalho disparado precisa de julgamento acumulado ao longo do tempo — memória, prioridades, um resultado permanente.)*

## Fontes

- [Automations — docs](https://docs.devin.ai/product-guides/automations)
- [Devin Automations QuickStart (vídeo)](https://www.youtube.com/watch?v=6xxKtIpgOyE)
- Relacionado: [Guia 3 — Bot sentinela agendado](bots-202-scheduled-sentinel.md) para adicionar julgamento de Bot em cima de um cron
