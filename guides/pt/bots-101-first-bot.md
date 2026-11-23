# Guia 1 — Seu primeiro Bot

**Objetivo:** criar um Devin Bot que assume um resultado e aprender as seis mecânicas nas quais todos os guias seguintes se apoiam.
**Nível:** comece aqui · **Tempo:** ~15 minutos
**Fonte:** [documentação oficial de Bots](https://docs.devin.ai/work-with-devin/bots), [post de lançamento](https://devin.ai/blog/introducing-devin-bots)

## O que é um Bot

Uma sessão atende a um pedido. Um Bot *é dono de um resultado*: você declara a meta uma vez no chat dele, ele planeja o trabalho, inicia uma sessão Devin filha para cada parte, monitora todas e só traz até você o que exige seu julgamento. Ele persiste — memória, sessões e automações sobrevivem por semanas.

As seis mecânicas, na ordem em que você vai encontrá-las:

| Mecânica | O que é | Onde você a usa |
| --- | --- | --- |
| Chat | Uma thread para tudo que o Bot possui — metas, relatórios, perguntas | A página do Bot / Slack / iMessage |
| Sessions | Cada parte do trabalho roda como sua própria sessão Devin em sua própria máquina | Criadas e monitoradas pelo Bot |
| Needs you | Decisões, revisões de PR, pedidos de permissão, relatórios — uma única lista | No topo do chat do Bot |
| Memory | O que o Bot aprende, salvo como arquivos, lido no início de cada sessão | Settings → Memory |
| Instructions | Regras permanentes escritas por pessoas, lidas no início de cada sessão | Settings → General |
| Access | As conexões/segredos do próprio Bot, além de grants entre Bots | Settings → Access |

## Passo 1 — Criar

Sidebar → **Bots** → *Create new Bot* → escolha um template ou *Start from scratch* → dê um nome.

Um Bot novo é privado para você até ser compartilhado. Seu uso conta no seu plano como qualquer sessão.

> Dica: a **Template library** (barra lateral → Bots) lista os templates da Cognition — QA Engineer, Migration Engineer, Data Analyst, … — além dos compartilhados na sua org; o mesmo conjunto dá para explorar sem login no [Bot marketplace](https://devin.ai/bots/templates) público. *Start from scratch* continua sendo a escolha certa para os guias deste repositório — você vai escrever o prompt de resultado você mesmo.

Um Bot criado de template recebe o prompt e **mais nada** — é privado, sem connections, secrets ou memory. Diga no chat do que ele é dono (repositório, projeto, canal), configure as connections como em qualquer Bot novo e, se o template roda num gatilho, o Bot se oferece para configurá-lo no primeiro contato. Ele guarda a própria cópia do prompt — edições posteriores no template não chegam até ele. (*Add to a current Bot* manda o prompt do template para um Bot que você já tem, em vez de criar um novo.)

## Passo 2 — Atribuir o resultado

A primeira mensagem é o input mais importante que um Bot já recebeu. Dê a ele uma *meta*, não uma tarefa:

```text
You own the Android app now. Keep it at feature parity with iOS.
```

Esse é o prompt literal com que o Android Bot da Cognition começou. Compare:

| Fraco (uma tarefa) | Forte (um resultado) |
| --- | --- |
| "Fix the checkout button" | "You own checkout. Keep it fast, correct, and covered by tests." |
| "Update the docs" | "You own the docs. Keep them in step with `main`." |
| "Watch CI" | "You own build health on `main`. When a check regresses, find the cause and fix it." |

Uma tarefa acaba quando termina; um resultado faz o Bot re-planejar para sempre.

### Uma primeira atribuição limitada

"Propriedade" é a *forma* certa, mas delimite a *superfície* na primeira rodada: um fluxo, um ambiente, um revisor — você. O padrão do guia de campo ANO é o ponto de partida confiável:

```text
Own the newsletter signup check for [project] on staging.
Use [repository], [staging URL] and the test mailbox I provide.
Check the journey from submitting the form to receiving the
correct welcome email and opening its resource link.

Start with one run. Show me the result before proposing a schedule.
If you find a defect, reproduce it, make the smallest suitable fix,
and open a pull request with the evidence.

Do not merge, deploy, email real subscribers, change billing,
or connect another service without asking me.

Return: what passed/failed, screenshots or a short recording,
the PR if a fix was needed, anything you could not verify,
and any decision you need from me.
```

As linhas estruturais: a definição da jornada (formulário → email → link, não só "o form funciona"), *uma execução antes do agendamento*, a cerca explícita de não-merge/não-deploy, e a evidência nomeada que você espera. Amplie a atribuição só depois que o Bot devolver evidência confiável duas vezes.

## Passo 3 — Trabalhar com ele

Depois que o resultado está definido, a maioria das suas mensagens são check-ins:

```text
anything waiting on me?
```

Abra **Needs you** (topo do chat) quando o Bot sinalizar algo:

| Item | Sua ação |
| --- | --- |
| Decision | Escolha uma opção — o Bot marca sua recomendação |
| Review PR / Merge PR | Revisar ou mergear |
| Permission request | Aprovar ou rejeitar novo acesso, uma automação, um host de rede ou aumento de limite de uso |
| Report / FYI | Leia |

Você pode responder com suas próprias palavras, adiar ou descartar qualquer item.

## Passo 4 — Direcionar pela memória, não por microgestão

- **Instructions** (Settings → General): suas regras permanentes — lidas no início de cada sessão que o Bot roda. Coloque política duradoura aqui, não no chat.
- **Memory** (Settings → Memory): arquivos que o próprio Bot escreve — preferências, correções, fatos do projeto. Para mudar o que ele lembra, basta dizer no chat ("remember: we deploy via Cloud Run, never bare VMs"). Todo mundo que pode usar o Bot pode ler sua memória — trate a memória de um Bot compartilhado como compartilhada.

O padrão que escala: corrija o Bot uma vez, deixe-o gravar a correção na memória, e toda sessão futura a herda. A Cognition mergeia mais de 2.000 PRs/semana nesse loop.

## Antes de compartilhar — acesso e uso

Duas coisas que os posts de lançamento pulam e a documentação explicita:

- **Um Bot privado herda seus recursos sem perguntar.** O acesso que você já tem pode ser registrado como grants sem novo prompt de permissão — um Bot privado não é uma sandbox. Antes de compartilhar, abra Settings → Access e remova grants que a tarefa não precisa. Se colegas devem copiar o método sem ver sua conversa ou credenciais, compartilhe um *template*, não o Bot: menu do Bot na barra lateral → *Share as template* — ele rascunha nome, descrição de uma linha e um prompt limpo, publicando na Template library da org (Teams/Enterprise) ou como link público (Pro+). O link embute o template inteiro assinado na URL — não dá para editar nem revogar e qualquer um lê o prompt completo, então remova nomes internos antes de copiar.
- **20 de nov de 2026 — Access & Sharing muda a superfície de compartilhamento** ([release notes](https://docs.devin.ai/release-notes/2026)): rollout gradual, opt-in enterprise. Cada sessão tem sua própria configuração de compartilhamento (só você / grupos de usuários / org); grupos de usuários podem ser escolhidos em todo Manage access — secrets, environments, sessions, automations, plugins, skills, MCP servers, knowledge. Admins também ganham relatório de divergência de acesso SCM e repo sync (espelha repos do GitHub/GitLab no seletor).
- **O uso de um Bot cobre o chat dele mais toda sessão que ele dispara.** Max: consome sua cota incluída e depois on-demand — sem cap separado de Bot. Teams: sua cota e depois créditos do time; um admin pode definir cap on-demand específico do Bot. Enterprise: conta no limite do criador, a menos que receba um próprio. Uma instrução de gasto no chat não é um cap configurado — defina o limite em Settings, não o descreva em prosa.

## Passo 5 — Colocar onde você trabalha

- **Slack:** dê ao Bot seu próprio app Slack para que sua equipe possa @-mencionar ou mandar DM (Settings → Slack). Toda implantação de equipe reportada roda assim — o Bot vira um colega nomeado num canal.
- **iMessage:** mande mensagem ao Bot do seu celular.
- **Web:** a seção Bots da sidebar lista os seus e os compartilhados com você.

## Passo 6 — Agendamentos e modos

- **Automations:** peça no chat — *"run a summary of open PRs every weekday morning"* — e o Bot propõe a automação para sua aprovação única. Gerencie em Settings → Automations (pausar/retomar/remover).
- **Modes:** o Bot tem seu próprio modo mais um padrão de **Child Capability** para as sessões que ele cria (ex.: `Normal / Ultra` no seletor de modo do chat). Você também pode pedir um modo diferente em qualquer sessão individual.

## Ciclo de vida

| Ação | Efeito |
| --- | --- |
| Recycle | Termina a sessão atual; uma nova começa na próxima abertura. No menu do chat. |
| Archive | Para as respostas, remove das listas de Bots, remove seu app Slack e grants entre Bots (desarquivar não os restaura — você os configura de novo). |
| Delete | Permanente: configurações, sessões, memória, automações. Não pode ser desfeito. |

Apenas o criador e papéis com Manage Bots veem Archive/Delete. Em planos Enterprise, `Use Bots` / `Manage Bots` / `Manage Bots across the enterprise` são permissões separadas em papéis personalizados.

## Checklist de verificação

- [ ] Bot criado e nomeado; prompt de resultado enviado no chat
- [ ] Bot iniciou pelo menos uma sessão filha sem ser pedido duas vezes
- [ ] Uma decisão/PR/pedido de permissão apareceu em **Needs you** e você resolveu
- [ ] Uma correção que você deu no chat aparece como arquivo de memória em Settings → Memory
- [ ] (Opcional) Bot alcançável via @-menção no Slack

## Armadilhas

- **Prompts em formato de tarefa.** "Fix X" produz uma sessão, não um Bot. Se o Bot termina e fica quieto, o prompt era uma tarefa — reformule como propriedade de resultado.
- **Chat para política.** Regras digitadas no chat somem no scroll; regras em Instructions são lidas em toda sessão. Chat = direção e respostas; Instructions = lei.
- **Ignorar Needs you.** Bots são desenhados para agrupar chamadas de julgamento — cheque uma ou duas vezes ao dia, não continuamente.

## Teste de conhecimento

1. O que sobrevive entre as sessões de um Bot que uma sessão avulsa não tem? *(Memória — mais o resultado permanente, agendamentos e superfícies.)*
2. Por que um Bot usa "needs-you" em vez de perguntar no meio da sessão? *(O julgamento vai para uma thread assíncrona; o humano não é uma chamada bloqueante no loop.)*
3. Qual mecânica transforma "uma sessão esperta" em "um funcionário"? *(A propriedade de um resultado — a meta persiste depois que qualquer sessão termina.)*

## Fontes

- [AI Native Operators — Devin Bots: give an agent a job to own](https://ainativeoperators.ai/blog/devin-bots-guide) —— guia de campo da comunidade; o padrão de primeira atribuição limitada e os avisos de acesso/uso acima vêm daqui
- Anterior: [Guia 18 — Falando com Devin](talking-to-devin.md) (a doutrina sob o outcome prompt)

- [Devin Bots — docs](https://docs.devin.ai/work-with-devin/bots)
- [Introducing Devin Bots](https://devin.ai/blog/introducing-devin-bots)
- Próximo: [Guia 2 — Bot product-owner](bots-201-product-owner.md) · Ver também: [Guia 19 — O loop da sessão](the-session-loop.md) (pesquisar → delegar → revisar → aprender)
