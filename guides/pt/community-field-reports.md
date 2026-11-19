# Guia 14 — Relatos de campo da comunidade

**Objetivo:** o que engenheiros que rodaram o Devin em trabalho real aprenderam — incluindo as falhas. Destilado de relatos hands-on publicados, tanto elogiosos quanto hostis.
**Nível:** comece aqui para julgamento
**Fontes:** linkadas por relato abaixo

Este guia é deliberadamente equilibrado: onde o Devin vence com confiabilidade, onde queima dinheiro, e o estilo de trabalho que separa os dois resultados.

## O padrão que se repete em todo relato

Usuários que obtêm resultados tratam o Devin como um **engenheiro júnior assíncrono**, não um gerador de código. Scott Wu (CEO da Cognition) descreve o workflow interno no [Lenny's Newsletter](https://www.lennysnewsletter.com/p/how-devin-replaces-your-junior-engineers): delegar tarefas bem escopadas, deixá-las rodar durante reuniões, revisar PRs. [O relato da Every](https://every.to/chain-of-thought/coding-with-devin-my-new-ai-programming-agent) chega ao mesmo enquadramento — exige um *skill set*: aprender no que ele é bom, escrever tarefas que ele entende, saber quando intervir, e aprender a confiar em trabalho feito diferente do seu.

## Onde o Devin venceu, documentado

**Prototipagem ponta a ponta.** De um repo em branco, o Devin scaffolded um "City Explorer" FastAPI + React (integrações de imagens/clima/notícias), rodou localmente, abriu um PR e deployou uma URL pública — ~90 minutos, ~2 intervenções humanas ([hands-on no Medium](https://medium.com/@sambhavgaur_70582/copilot-cursor-or-devin-my-hands-on-weekend-with-ai-that-codes-and-deploys-acc708e802b3)). A [Scott Logic](https://blog.scottlogic.com/2025/10/20/rapid-development-with-devin.html) reporta o mesmo arco num protótipo de cliente real — com uma lição crucial de iteração abaixo.

**Trabalho que precisa de runtime.** Num [head-to-head com Claude Code](https://web.archive.org/web/20260718112612/https://mohitkhare.me/blog/devin-vs-claude-code/), o Devin perdeu em tarefas de encaixar nas suas convenções mas venceu claramente onde uma máquina ajuda: caça a memory leak onde ele profiled, tirou heap snapshots sob carga e produziu um relatório — a VM própria do agente é a feature.

**Troubleshooting ao vivo.** A [Faros](https://www.faros.ai/blog/how-to-use-devin-ai-troubleshooting) usou o Devin *durante uma call com cliente*: ele leu o código da introspection API e gerou um `curl` funcional em segundos — colapsando um loop de follow-up de 1–2 dias dentro da própria call.

**Migrações reais com docs frescas.** Um upgrade Tailwind 3→4 + DaisyUI 4→5 num codebase Vue→React complicado funcionou quando o time alimentou o Devin com docs atuais via o MCP Context7 — o prompt carregava o *contexto*, não só a tarefa ([write-up no Bootcamp](https://medium.com/design-bootcamp/day-7-of-30-getting-to-know-devon-ai-and-working-with-him-743c351cd0c4)).

**Auto-verificação.** Uma [comparação de praticante de um ano](https://architecttocto.substack.com/p/the-only-coding-agent-worth-paying) marca o e2e testing dirigido por browser do Devin como o momento-limiar: ele navega até o que construiu e checa — um loop de feedback que parece engenharia, não geração.

**Além de código.** Um pesquisador da Cognition relata que o Devin reconstruiu — e terminou — uma formalização em Lean que lhe tomou boa parte de um semestre nove anos antes, em **menos de 15 minutos** ([post](https://x.com/penlume/status/2115806616796921885)). Formalização matemática recompensa o mesmo traço das migrações: uma definição de pronto verificável por máquina.

**Ligado à observabilidade.** [Dynatrace MCP + Devin](https://medium.com/lets-code-future/how-i-turned-devin-into-a-performance-analysis-agent-with-dynatrace-mcp-753d3f4790a2) transforma o Devin num agente de análise de performance: ele consulta métricas e traces ao vivo, depois diagnostica — o servidor MCP carrega contexto de produção que o repo não pode (Medium). Veja também [Devin: do bug report ao pull request](https://medium.com/@winter.inc/devin-from-bug-report-to-pull-request-25-days-of-ai-day-18-b158daa20f23) para o loop ticket→PR simples ponta a ponta.

## Onde falhou, documentado

- **Prompts vagos ou amplos demais.** O primeiro prompt da Scott Logic produziu um scaffold inutilizável; estreitar o stack e o pedido ("just the models") resolveu. O Devin super-constrói — diga a ele o que *não* construir.
- **Tarefas de encaixar em convenções.** "Add pagination to this endpoint" voltou desalinhado das convenções do codebase em dois relatos independentes ([amillionmonkeys](https://www.amillionmonkeys.co.uk/blog/ai-coding-tools-small-studios), [mohitkhare](https://web.archive.org/web/20260718112612/https://mohitkhare.me/blog/devin-vs-claude-code/)) — o Devin constrói em isolamento a menos que você carregue as convenções até ele (→ Guia 9).
- **Trabalho não verificável.** [expectedwrong](https://expectedwrong.com/devin-appraised) e o [teste de 10 tarefas de alanwest](https://dev.to/alanwest/i-gave-devin-10-real-tasks-it-completed-3-3063) documentam o modo de falha: saída confiante que está quebrada ou ausente, créditos queimados em loops. Suas tarefas penderam para trabalho sem verificação clara — o mesmo gate que o playbook oficial torna obrigatório (Guia 11).

## Implantações de times nomeados (comunidade, com números)

Orgs reais publicando seus dados operacionais de Devin — majoritariamente da comunidade de engenharia do Japão, que documenta excepcionalmente bem:

| Time | Implantação | Resultado reportado |
| --- | --- | --- |
| rakko_inc | Code review automático via Playbooks + GitHub Actions + Devin API — pré-digere todo PR antes da revisão humana | **65 → 184 PRs revisados/mês (2.8×)**; humanos partem do resumo do Devin ([relato](https://zenn.dev/rakko_inc/articles/00cc5a5a679971), JP) |
| Skillnote (QA) | PR → Actions → Devin gera rascunhos de design de testes (CSV/Excel, incl. "por que este caso") postados no PR | ~**35 min economizados por 10 casos de teste**; casos desenhados pelo Devin pegaram bugs que humanos perderam ([relato](https://zenn.dev/skillnote/articles/5ba429ca249801), JP) |
| arufian | Automação serverless de eventos GitHub (sem servidor fixo): labels `devin:fix`/`devin:plan` dirigem sessões Devin, com **tabela de política prioridade × complexidade** e fluxo de aprovação plan-first | Safety scans fazem gate de PRs arriscados; trabalho de alta complexidade ganha plano → aprovação humana → `run that plan` ([relato](https://zenn.dev/arufian/articles/f80a62f5217cee), JP) |
| Leverages (levtech) | Rollout de org: 14 times / ~30 pessoas | **177 PRs mergeados** em ~2.5 meses; medem ROI como `custo ACU − horas poupadas × salário` e acompanham o mix por tipo de tarefa ([relato](https://zenn.dev/levtech/articles/9c869303820844), JP) |
| Decagon | AutoResearch no Devin Cloud: um Devin orquestrador + subagentes paralelos competindo hipóteses; toda ideia verificada contra tráfego de produção replicado em GPUs da Modal | **até 2.5× mais throughput por GPU** no tráfego de suporte ([writeup](https://x.com/DecagonAI/article/2115511110120120437)) |
| Nader Dabit | Org pessoal de 5 bots — **CTO** (todas as sessões/repos, iMessage VIP), **Auto(mation)Bot** (roda suas automações, relatórios de perf), **DevCommunityBot** (dados do programa de embaixadores → mini-apps), **DevRelBot** (docs + vídeos-tutoriais com *seu próprio computador, contas próprias de Devin/GitHub/Linear, voz clonada ElevenLabs*) | Mais **Windfable**: ~10 Bots SuperJennyStack num RPG iOS Unity, cada um com macOS+Xcode+Unity próprios, testando iPhone Duo nos modos dobrado/aberto com diffs de screenshot/vídeo ([primer](https://x.com/dabit3/status/2122755275182469515)) |
| Mark Fenner | Operador solo rodando quatro Bots de cargos sob um Chief Agent Bot coordenador ("Frankie") | Updates consolidados numa superfície de decisão única — a forma multi-Bot funciona sem time ([walkthrough](https://x.com/markfenner/status/2122740244328145211)) |
| hubble | Dois loops permanentes: todo PR do Dependabot recebe uma investigação do Devin antes de um humano ler — rótulo de risco GREEN/YELLOW/RED **mais o raciocínio num comentário**; um loop semanal de Datadog CCM escolhe um candidato de custo, aprofunda e devolve um relatório pronto para decisão | O material de revisão já está montado quando o humano abre o PR; o entregável é o raciocínio, não o rótulo ([loop Dependabot](https://zenn.dev/hubble/articles/88429bd24db476), [loop de custo](https://zenn.dev/hubble/articles/091e29a0c86ec3), JP) |
| SMARTCAMP | Pipeline de segurança permanente: GitHub Actions agendado puxa imagens ECS → scan Trivy (HIGH/CRITICAL) → abre issues → Devin remedia; credenciais AWS e jobs do scanner separados para que só artefatos cruzem; pin de hash + carência de 7 dias após release contra atraso do scanner | Remediação de vulnerabilidades como pipeline, não como sessão ([relato](https://zenn.dev/smartcamp/articles/97ac804043530e), JP) |
| canly | Devin como analista, não codificador: classificou ~700 tickets históricos de suporte para descobrir o que "causa não identificada" realmente era | Mais da metade não era bug; escolher o que mostrar à IA (DB? docs?) importou mais que o modelo ([relato](https://zenn.dev/canly/articles/9c19bb123e208c), JP) |

As ideias reutilizáveis dentro: **gating por tabela de política** (arufian: só auto-PR em trabalho de baixo risco, plan-first para complexo), **prompting de saída fixa** (Skillnote: formato CSV fixo + Python inline para conversão mata a variância da saída), **pré-digest para o revisor** (rakko: o Devin resume + sinaliza antes do humano ler), **triagem com razão primeiro** (hubble: o rótulo é um ponteiro; o comentário com a evidência é o entregável), **remediação em forma de pipeline** (SMARTCAMP: scan → issue → correção num loop estilo CI com estágios credenciados e sem privilégio separados) e **contabilidade honesta** (a fórmula ROI ACU-vs-salários da levtech).

**As miudezas da gestão em org** (do rollout de ~30 usuários da Leverages, mesmo relato):

- Um workspace de Slack só pode vincular a **uma** organização Devin — verifique se outro departamento já reivindicou o seu antes de planejar sessões via Slack.
- Não há quota de ACU por time; eles agregam uso listando sessões via API e raspando o ACU de cada sessão na web UI — orçamento por visibilidade, não por imposição.
- Gasto invisível de ACU: por padrão, todo comentário num PR do Devin acorda uma sessão. Ativaram **"Only respond to PR comments that mention Devin"** para as pessoas discutirem PRs livremente.
- Onboarding de repositórios é serial — um repo em setup bloqueia o próximo; agende.
- O split de ROI deles: alto em pré-revisão de PR (~1–2 ACU cada via rótulo `devin-review` → Actions → Playbook de API), avaliações de risco agendadas de upgrade de libs, e trabalho em legado alimentado com um *PR existente similar*; baixo em refactors amplos e tarefas pequenas demais para importar.

## As lições destiladas

1. **Escopo na fatia, não no projeto.** Os sucessos são todos unidades delimitadas; as falhas são "construa/conserte isso amplamente." (Doutrina oficial: Guia 13.)
2. **Verifique ou não delegue.** Dê ao Devin trabalho onde uma máquina possa checar "pronto" — testes, builds, um `curl` funcional, uma página renderizada.
3. **Carregue contexto, não suposições.** Convenções, docs atuais (via MCP), a forma do seu stack — as falhas são falhas de contexto, não de capacidade.
4. **Delegue; não assista.** O ROI em todo relato positivo é *assincronia* — as tarefas rodam enquanto você faz outra coisa. Assistir ele digitar é como você decide que ele é "lento".
5. **Itere o prompt, não a ferramenta.** A correção da Scott Logic não foi outro agente — foi um prompt mais estreito. Trate uma primeira execução falha como bug do prompt.
6. **Entregue evidência, não vereditos.** A hubble reescreveu o último passo do seu skill de Dependabot de "decidir se mergeia" para "avaliar o risco" — o agente monta o caso, o humano fica com a decisão.

## O top-5 interno de Scott Wu (da entrevista do Lenny's)

As tarefas que a própria Cognition mais delega: **correções de frontend, upgrades de versão, documentação, resposta a incidentes, testes** — mais um padrão de "primeira linha de defesa" onde o Devin analisa crashes antes dos humanos engajarem, e pesquisa no DeepWiki para *escrever prompts melhores*.

## Análises a fundo — o que copiar, o que observar

**O loop de Dependabot da hubble.** Todo PR do Dependabot dispara uma sessão Devin guiada por um arquivo Skill: ela lê o diff, as mudanças do lockfile, as release notes e o estado do CI, e comenta um rótulo de risco GREEN/YELLOW/RED *mais a evidência* — libs atualizadas e tipo de update, classe de risco com justificativa, achados de compatibilidade, estado do CI e o que um humano ainda deve checar à mão. Por que funciona: a Skill codifica "o que risco significa aqui" (quais gems são críticas, o que verificar mesmo com CI verde) — conhecimento tácito do revisor agora num arquivo que o time inteiro lê e cultiva. Eles apagaram de propósito o passo "decidir se mergeia" em favor de "avaliar o risco". Copie: escreva seu procedimento de revisão como Skill primeiro — se você não consegue escrever o procedimento, a automação não consegue rodá-lo. Atenção: rótulos sozinhos decaem; sem o comentário com o raciocínio, o sistema não ensina nada.

**O loop semanal de custos da hubble.** Uma passada semanal pelo Datadog CCM: o Devin escolhe um candidato de redução de custo, investiga configuração e uso, e devolve um relatório pronto para decisão. O produto do loop é um *candidato com recomendação*, não uma fatura. Copie: "escolha um candidato, aprofunde, entregue" generaliza para qualquer fila permanente de higiene. Atenção: ferramentas de primeira mão (custo da AWS) se sobrepõem — vence quando seus dados de custo vivem no Datadog e a correção precisa de contexto do repo.

**O pipeline scan→fix da SMARTCAMP.** GitHub Actions agendado puxa imagens ECS → scan Trivy (HIGH/CRITICAL, pacotes OS) → abre issues → Devin remedia. O que vale copiar é o endurecimento, não a seta: o job de pull com credenciais AWS e o job do scanner sem privilégios são separados para que só artefatos cruzem; esperam ~7 dias após um release para confiar no resultado (as bases do scanner atrasam para pacotes novos); digests de imagem são pinados por hash, com um check de PR que sinaliza hashes velhos. Atenção: é defesa em profundidade contra o próprio scanner como superfície de supply chain — copiar só "scan → Devin" perde o ponto.

**A implantação-analista da canly.** O Devin classificou ~700 tickets históricos de suporte presos no balde "causa não identificada". Mais da metade não era bug — e a saída real do exercício foi um mapa do contexto que a IA ainda precisa (docs, visibilidade do DB, metadados do ticket), não os rótulos. Copie: Devin-como-analista é um uso de primeira classe — aponte para a pilha que ninguém nunca classificou antes de comprar ferramentas. Atenção: o gargalo é a seleção de contexto, não a qualidade do modelo.

## Checklist de verificação

- [ ] Escolha o relato mais próximo do seu stack e releia o original, não a destilação — o número ainda se sustenta em contexto?
- [ ] Anote a única lição na qual você apostaria dinheiro reproduzindo na sua org; se não conseguir nomeá-la, escolha outro relato

## Armadilhas

- **Viés de sobrevivência.** Os relatos brilhantes publicam números; as falhas silenciosas não publicam nada. Leia as falhas desta coleção como a experiência mediana, as vitórias como o teto.
- **Cargo cult.** A iteração de prompt da Scott Logic funcionou *porque* eles iteraram — copiar o prompt final deles sem o loop deles te dá o começo deles, não o resultado.

## Teste de conhecimento

1. O que os relatos de falha têm em comum que os de sucesso não têm? *(Delegação não verificável — as falhas deram ao Devin trabalho onde ninguém podia checar "pronto"; todo sucesso definiu uma checagem.)*
2. Por que o "debugging numa call de cliente" da Faros é uma lição de implantação, não uma anedota? *(Mostra a manobra de triagem ao vivo: o agente como primeiro respondedor enquanto o humano mantém o relacionamento com o cliente.)*
3. Por que este guia conta um relato hostil como fonte em pé de igualdade? *(Relatos adversariais expõem as condições de fronteira — você aprende as bordas do mapa com quem saiu delas.)*

## Fontes

- [Scott Logic — Rapid development with Devin](https://blog.scottlogic.com/2025/10/20/rapid-development-with-devin.html)
- [Lenny's Newsletter — Scott Wu on Cognition's internal Devin usage](https://www.lennysnewsletter.com/p/how-devin-replaces-your-junior-engineers)
- [Every — Coding with Devin](https://every.to/chain-of-thought/coding-with-devin-my-new-ai-programming-agent)
- [dev>notes — Devin vs Claude Code](https://web.archive.org/web/20260718112612/https://mohitkhare.me/blog/devin-vs-claude-code/)
- [Faros — Devin for live troubleshooting](https://www.faros.ai/blog/how-to-use-devin-ai-troubleshooting)
- [Medium — Copilot, Cursor or Devin weekend](https://medium.com/@sambhavgaur_70582/copilot-cursor-or-devin-my-hands-on-weekend-with-ai-that-codes-and-deploys-acc708e802b3)
- [Bootcamp — Day 7 with Devin (Tailwind/DaisyUI migration)](https://medium.com/design-bootcamp/day-7-of-30-getting-to-know-devon-ai-and-working-with-him-743c351cd0c4)
- [architect to CTO — The only coding agent worth paying for](https://architecttocto.substack.com/p/the-only-coding-agent-worth-paying)
- [expectedwrong — Devin, appraised](https://expectedwrong.com/devin-appraised) · [dev.to — 10 real tasks, 3 completed](https://dev.to/alanwest/i-gave-devin-10-real-tasks-it-completed-3-3063) · [amillionmonkeys](https://www.amillionmonkeys.co.uk/blog/ai-coding-tools-small-studios)
- [Signadot — Testing Devin's changes end to end](https://dev.to/signadot/test-devins-changes-end-to-end-with-signadot-a0)
- [hubble — PRs do Dependabot investigados pelo Devin primeiro](https://zenn.dev/hubble/articles/88429bd24db476) · [hubble — Datadog CCM × Devin, ops de custo semanal](https://zenn.dev/hubble/articles/091e29a0c86ec3) (JP)
- [SMARTCAMP — pipeline Trivy scan → remediação pelo Devin](https://zenn.dev/smartcamp/articles/97ac804043530e) (JP)
- [canly — Classificando ~700 tickets de suporte com o Devin](https://zenn.dev/canly/articles/9c19bb123e208c) (JP)
- [smasato — Maximizando o Devin: dicas de sucesso](https://zenn.dev/smasato/articles/6aebb0da2f56eb) (JP/EN)
