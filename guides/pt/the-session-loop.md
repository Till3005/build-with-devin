# Guia 19 — O loop completo da sessão: pesquisar, delegar, revisar — e quanto custa

**Objetivo:** Rodar o loop completo do Devin de ponta a ponta — entender a codebase via índice antes de escrever o brief, delegar uma sessão com escopo, passar uma revisão independente no PR e ler o Session Insights para o próximo loop sair mais barato.
**Nível:** Inicial (par do [Guia 18](talking-to-devin.md))
**Fontes:** [Devin University — Cloud 101/103](https://learndevin.com) · [Docs do DeepWiki](https://docs.devin.ai/work-with-devin/deepwiki) · [Docs do Ask Devin](https://docs.devin.ai/work-with-devin/ask-devin) · [Docs do Devin Review](https://docs.devin.ai/work-with-devin/devin-review) · [Docs do Session Insights](https://docs.devin.ai/product-guides/session-insights)

## O loop que a maioria só roda pela metade

O Guia 18 ensina a escrever um brief que o Devin não consegue interpretar errado. A trilha Cloud da Devin University envolve esse brief no loop completo que o produz e consome o resultado:

```
Entender ──► Delegar ──► Revisar ──► Aprender
 DeepWiki     brief+          Devin Review    Session Insights
 Ask Devin    sessão          no PR           → próximo brief melhor
```

A maioria das sessões que falha morre nas pontas, não no meio: o brief foi escrito às cegas sobre a codebase, ou o PR foi mergeado no feeling. Este guia cobre as duas pontas e o medidor que corre por baixo de tudo.

## Entender: DeepWiki e Ask Devin antes de gastar o primeiro ACU

O **DeepWiki** indexa automaticamente seus repos conectados e gera uma wiki por repo — diagramas de arquitetura, resumos, links para o código-fonte, configurável via `.devin/wiki.json`. Ele responde as perguntas que você descobriria gastando tempo de sessão: onde mora esse módulo, quem o chama, qual é o padrão estabelecido.

- Os níveis de esforço são por org (com override por repo): **Low é grátis** e o padrão; Medium roda ~5–10 ACUs por wiki, High ~20–40. Low basta para apoiar briefs na maioria dos repos.
- O onboarding indexa os repos que você configurou automaticamente; adicione outros em **Settings → DeepWiki**.
- Para repos públicos existe o [deepwiki.com](https://deepwiki.com) gratuito — indexe qualquer repo público do GitHub e ganhe os mesmos diagramas e Q&A sem conta. Também há um MCP do DeepWiki para seus outros agentes.

O **Ask Devin** é a camada conversacional sobre esse índice — em [app.devin.ai/search](https://app.devin.ai/search):

- **Modo Ask**: perguntas sobre seu código respondidas com citações de código, ancoradas no índice — "como funciona o retry no billing poller" retorna o arquivo, os call sites, o padrão.
- **Modo Plan**: descreva a mudança e o Devin define o escopo com você — depois gera um prompt rico em contexto, pronto para entregar a uma sessão. É o jeito mais barato de cumprir as regras do Guia 18: o ponto de partida e o padrão de referência vêm do índice, não da sua memória.
- Inicie a sessão de dentro da conversa e o status dela fica visível ali — sem trocar de contexto.

O retorno é duplo: um brief informado por fatos indexados é mais específico *e* mais curto.

## Delegar — o passo que você já conhece

Entregue o prompt gerado pelo Ask Devin (ou seu próprio brief do [Guia 18](talking-to-devin.md)) como uma sessão com escopo. O que muda é que o brief já sabe tudo: os arquivos, o padrão, o check, o limite.

## Revisar: um segundo agente em todo PR

O **Devin Review** é um revisor independente, não um replay da autoavaliação da sessão:

- Disparo por PR: comente `/devin review` num PR do GitHub ou MR do GitLab, ou abra o PR no [Devin Review](https://app.devin.ai/review). Ele agrupa mudanças relacionadas, explica ao lado do diff e aponta bugs e achados de segurança que você pode citar no chat — inclusive pedindo ao Devin para corrigir na hora.
- Para a org: existem auto-review, instruções de revisão e controles de custo para rodar em todo PR. O Review 2.0 (nov/2026) cortou o custo por PR em **82%** — é o que torna o always-on economicamente viável.
- Use também nos PRs do próprio Devin. Escritor e revisor sendo agentes diferentes é o ponto — a mesma assimetria que o Guia 18 atribui a você versus a sessão.

## Aprender: Session Insights e o medidor de ACU

Toda sessão concluída ganha um **Session Insights** (menu **⋯ → Session insights**, grátis):

- **Indicador de tamanho da sessão** — a classificação XS–XL se baseia no consumo da sessão, não no número de mensagens do usuário. Sessões L/XL recebem uma análise completa automaticamente; nas menores, ela é gerada sob demanda.
- **Uso de ACU** (ou dólares on-demand em planos por quota) — compare tarefas semelhantes para achar sessões que queimaram computação em retries e becos sem saída.
- **Mensagens do usuário** — uma métrica separada. Uma contagem alta pode sinalizar correções de rota frequentes e ajudar a identificar que contexto incluir logo no início.
- A análise recomenda melhorias concretas — prompts mais firmes, knowledge faltando, escopo errado. A meta do Cloud 103 é a certa: *cada sessão mais barata que a anterior.*

Higiene de custo presente em todo field report: escopo estreito por sessão, mate sessões ociosas (pensar e esperar ambos cobram), cheque a quota antes de soltar uma frota — o operador do 100 Days queimou **33% da quota semanal em dois dias** de setup de Bots ([field reports](community-field-reports.md)). Ressalva reportada pela comunidade específica de Bots: plugar sua *própria* chave de modelo nas sessões-filho de um Bot **não** impede a quota semanal do plano de drenar — o raciocínio do próprio Bot mais a computação em nuvem ainda cobram do plano ([relato no linux.do](https://linux.do/t/topic/3225152), zh).

## Checklist de verificação

- [ ] Você responde "onde mora X e quem o chama" pelo DeepWiki/Ask Devin *sem* abrir sessão.
- [ ] Seu próximo brief contém pelo menos um fato vindo do índice, não da memória.
- [ ] O último PR que você tocou passou por um Devin Review — seu ou do Devin.
- [ ] Você lê o tamanho, os ACUs e a contagem de mensagens da última sessão, e cita um ponto que a análise marcou.

## Armadilhas

- **Briefar às cegas.** Escrever prompts pela memória de uma codebase que você não abre há meses — o índice sabe mais que você agora. Dois minutos no Ask Devin valem mais que uma correção no meio da sessão.
- **Pular revisão porque o CI está verde.** O CI verifica o que você lembrou de checar. O Review lê o próprio diff; são redes diferentes.
- **Ler Insights só nas falhas.** O padrão caro é a sessão medíocre que você repete toda semana. Revise sucessos também — é onde mora o brief reutilizável.
- **Gastar demais em nível de esforço.** Wikis em High para repos que você só toca uma vez por trimestre; o override por repo existe por isso.

## Teste de conhecimento

1. *Por que iniciar a sessão pelo Ask Devin e não pela sidebar do Devin?* Porque o modo Plan ancora o prompt no código indexado — o ponto de partida, o padrão existente e a superfície verificável vêm do próprio repo, então a sessão abre com o contexto que você digitaria ou descobriria no meio do caminho.
2. *O relatório da sessão diz que o trabalho está feito e testado. Por que rodar o Devin Review?* Independência. A sessão corrigiu a própria lição; o Review é outro agente lendo o diff com contexto novo — o mesmo motivo pelo qual o PR de um colega não é auto-aprovado.
3. *Uma sessão foi classificada como XL. O que conferir primeiro?* Veja o consumo e procure erros recorrentes ou novas tentativas na aba Issue Timeline do Session Insights. Muitas mensagens podem indicar que faltou contexto no brief, mas não afetam a classificação de tamanho.

## Fontes

- [Devin University](https://learndevin.com) — cursos Cloud 101 (este loop) e Cloud 103 (eficiência); aulas grátis, exames exigem assento Enterprise
- [DeepWiki](https://docs.devin.ai/work-with-devin/deepwiki) + [Ask Devin](https://docs.devin.ai/work-with-devin/ask-devin) — indexação, níveis de esforço, modo Plan, [deepwiki.com](https://deepwiki.com) para repos públicos
- [Devin Review](https://docs.devin.ai/work-with-devin/devin-review) — `/devin review`, auto-review, [corte de custo do Review 2.0](https://devin.ai/blog/devin-review-2)
- [Session Insights](https://docs.devin.ai/product-guides/session-insights) — dimensionamento XS–XL, métricas de ACU/mensagens, API
- Próximo: [Guia 18 — Falando com o Devin](talking-to-devin.md) se ainda não leu · [Guia 9 — Playbooks](playbooks-and-knowledge.md) para fixar o brief melhorado
