# Guia 18 — Falando com Devin: a doutrina do prompt

**Objetivo:** Escrever instruções que Devin não pode interpretar errado — a linha entre uma sessão que entrega e uma que vagueia.
**Nível:** Comece aqui
**Fontes:** [Coding Agents 101](https://devin.ai/agents101) (Cognition, junho de 2025) · [Instructing Devin Effectively](https://docs.devin.ai/essential-guidelines/instructing-devin-effectively) — ambas oficiais, destiladas abaixo com notas de campo

## Por que este guia vem primeiro

Todo guia deste repositório presume uma habilidade: você consegue dizer a Devin o que quer de um jeito que ela não pode entender errado. As duas orientações da própria Cognition — *Coding Agents 101* e *Instructing Devin Effectively* — dizem a mesma coisa por ângulos diferentes: **os engenheiros que mais aproveitam os agentes escrevem como quem briefa um colega júnior, não como quem faz um pedido.** Este guia é essa doutrina condensada, ligada ao resto do currículo.

## As quatro regras que sustentam tudo

**1. Diga como, não só o quê.** "Corrige os bindings C++ do nosso módulo de busca para passar nos novos testes — atenção, vai precisar recompilar os bindings a cada mudança antes de testar." Você conhece as armadilhas do seu codebase; nomeie-as. Briefs abertos ("deixe o app mais bonito", "melhore a performance do banco") devolvem resultados abertos.

**2. Diga por onde começar.** Repositório, diretório, arquivo, implementação de referência, URL de docs — tudo que você quereria se a tarefa caísse na *sua* mesa. "Use `authTemplate.rs` como referência para manter consistência no tratamento de erros" vence um parágrafo de estilo sempre.

**3. Defina sucesso como algo verificável.** Não "garanta que funciona" — um check que Devin pode rodar: *endpoint retorna 200 com campos X/Y/Z*, *componente renderiza sem erros de console em 1440px e 375px*, `npm test` verde. Devin tem uma máquina completa — browser, shell, IDE. Mande-o verificar o próprio trabalho ("rode `npm run dev` e confirme que `/settings` renderiza") e ele faz QA antes de você ver o PR.

**4. Dê loops de feedback, não vibrações de feedback.** Type checkers, linters, testes, CI — o superpoder do agente é iterar contra mensagens de erro. Se seu repo não consegue dizer quando ele erra, você é o loop de feedback — a configuração mais cara que existe.

## O brief de referência

O prompt-modelo da própria Cognition, anotado:

> In the Devin repo, build a tool that monitors RAM and CPU usage of the remote machines Devin runs on. — *escopo e propósito em uma linha*
>
> - Create a background task that launches when devin.rs starts — *passo a passo, não um bloco*
> - It opens a connection to all forked remote machines and monitors usage — *mecanismo nomeado*
> - If usage exceeds 80%, emit a new type of Devin event (check how we use Kafka) — *critério de sucesso + ponteiro para padrão existente*
> - Architect so it doesn't block other operations — *restrição que só o autor conhecia*

Repare no que falta: opiniões estéticas, hedging, "talvez", "se achar bom". Cada linha é uma decisão já tomada por alguém que conhece o sistema.

## Defesa: o que fica com você

O guia 101 é direto sobre o limite: **espere ~80% de economia de tempo em tickets grandes, não automação total.** Além de alguns arquivos, planeje vários ciclos de feedback. A postura vencedora é *arquiteto revisando o PR de rascunho de um júnior* — você fica com a correção, Devin fica com as teclas.

Consequências práticas:

- **Escopo duro.** "Não faça merge, deploy ou toque em billing sem me perguntar" — escreva a cerca explicitamente, não confie em bom senso implícito.
- **Divida trabalho grande em sub-tarefas verificáveis** — uma sessão por sub-tarefa, cada uma com seu check de sucesso (é também por isso que o padrão de migração do Guia 11 funciona: centenas de PRs pequenos, todos verificáveis).
- **Skills para o repetitivo** — qualquer coisa que você vai pedir mais de duas vezes vira `SKILL.md`; Devin invoca automaticamente (Guia 16).

## De instruir para delegar posse

Uma instrução de sessão responde *"faça esta tarefa bem"*. Um outcome prompt de Bot responde *"assuma esta área"*. A doutrina é a mesma — especificidade, limites, sucesso verificável — mas o objeto muda de tarefa para responsabilidade. Fluente aqui, a [referência de outcome-prompts](bot-outcome-prompts.md) mostra como os mesmos músculos produzem os 1.134 PRs do Android Bot.

## Passo a passo real — gravado no Devin CLI v3000.14 (swe-2-flash-medium)

A doutrina executada num `demo-repo` descartável: um brief de quatro linhas — escopo + mecanismo, arquivos nomeados, linha de sucesso verificável, fronteira explícita. Uma sessão, zero esclarecimentos no meio, auto-verificado.

**Vídeo (90 s, sem áudio):** brief → edições → prompts de permissão → auto-checagem → fronteira honrada.

[![SWE-2 Flash Medium concluindo a tarefa — 5 testes unittest verdes, nenhum commit](https://till3005.github.io/built-with-devin/assets/guides/talking-to-devin/walkthrough-poster.webp)](https://till3005.github.io/built-with-devin/assets/guides/talking-to-devin/walkthrough.mp4)

![1. O REPL do CLI em SWE-2 Flash Medium — composer pronto no demo-repo](https://till3005.github.io/built-with-devin/assets/guides/talking-to-devin/step1-repl-flash.webp)
*1. O REPL do CLI em SWE-2 Flash Medium — composer pronto no demo-repo*

![2. O brief — quatro regras em quatro linhas: como, onde, critério de sucesso, fronteira](https://till3005.github.io/built-with-devin/assets/guides/talking-to-devin/step2-the-brief.webp)
*2. O brief — quatro regras em quatro linhas: como, onde, critério de sucesso, fronteira*

![3. No meio: escrevendo test_app.py — o prompt de permissão oferece Allow / accept-edits / bypass / deny](https://till3005.github.io/built-with-devin/assets/guides/talking-to-devin/step3-edits-approval.webp)
*3. No meio: escrevendo test_app.py — o prompt de permissão oferece Allow / accept-edits / bypass / deny*

![4. Auto-verificação: o agente pede exatamente a checagem nomeada — python3 -m unittest -v](https://till3005.github.io/built-with-devin/assets/guides/talking-to-devin/step4-self-check-prompt.webp)
*4. Auto-verificação: o agente pede exatamente a checagem nomeada — `python3 -m unittest -v`*

![5. Feito — 5 testes OK; o próprio relatório confirma a fronteira: "No commit made."](https://till3005.github.io/built-with-devin/assets/guides/talking-to-devin/step5-tests-green.webp)
*5. Feito — 5 testes OK; o próprio relatório confirma a fronteira: "No commit made."*

![6. Depois de /exit — a dica `devin -r` e o `git status` provando a cerca: dois arquivos modificados, nenhum commit novo](https://till3005.github.io/built-with-devin/assets/guides/talking-to-devin/step6-no-commit.webp)
*6. Depois de /exit — a dica `devin -r` e o `git status` provando que a cerca segurou: dois arquivos modificados, nenhum commit novo*

## Verifique

- [ ] Dada uma tarefa real do seu backlog, você escreve em menos de 10 minutos um brief com: repo/arquivos nomeados, padrão de referência, check de sucesso explícito e limite declarado.
- [ ] A sessão resultante termina sem uma pergunta no meio do caminho que você chamaria de óbvia.
- [ ] Devin verificou o próprio trabalho antes do PR — porque você pediu no brief.

## Armadilhas

- **Prompts que codificam sua própria confusão.** Se você não consegue enunciar o check de sucesso, a tarefa ainda não está pronta — co-desenvolva um PRD com Devin primeiro (o 101 endossa) em vez de esperar que ela intua o objetivo.
- **Ambição sem permissão.** "Conserte o CI" de uma conta que não vê o CI produz erro confiante. O brief deve corresponder ao acesso que você realmente concedeu.
- **Revisar output, não correção.** Teste verde e diff plausível são evidência de progresso, não prova de que o comportamento está certo. A camada final de verificação continua sua.

## Cheque de conhecimento

1. *Por que "adicione testes unitários" perde para "adicione testes para o retry path em `poller.ts`, mockando `fetch`, cobrindo timeout e 5xx"?* Porque o segundo brief elimina a necessidade de o agente fazer julgamentos que você queria fazer: o que testar, quais bordas importam, o que mockar. Toda decisão não especificada é um cara-ou-coroa fora do seu controle.
2. *Devin abriu um PR com diff limpo e CI verde. Acabou?* Ainda não — CI verde significa que os checks passaram, não que a intenção foi atendida. A última camada de verificação ainda é sua; essa assimetria é o acordo (~80% de economia, correção com o humano).
3. *Quando instruções viram Skills?* Quando você se pega redigitando. A terceira ocorrência é um SKILL.md — o Guia 16 cobre formato e caminhos de descoberta.

## Fontes

- [Coding Agents 101](https://devin.ai/agents101) — a doutrina de prompting da Cognition: say-how, ponto de partida, prompting defensivo, feedback loops, a regra dos 80%
- [Instructing Devin Effectively](https://docs.devin.ai/essential-guidelines/instructing-devin-effectively) — a lista oficial de do/don't e o brief de referência dissecado acima
- [Biblioteca de tutoriais](https://docs.devin.ai/tutorial-library) + [Devin University](https://devin.ai/university) — o mesmo material em vídeo e curso
- Nota de campo: todos os relatos em [community field reports](community-field-reports.md) convergem para a mesma conclusão — briefs, não desejos
- Próximo: [Guia 1 — Seu primeiro Bot](bots-101-first-bot.md) (mesma doutrina, objeto maior) · [referência de outcome prompts](bot-outcome-prompts.md)
