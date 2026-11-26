# Guia 20 — Dynamic Workflows

**Objetivo:** orquestrar muitas sessões Devin com um script Python determinístico — distribuir trabalho independente, passar resultados estruturados entre estágios, retomar runs interrompidas e manter o custo em ACUs visível.
**Nível:** avançado · **Tempo:** cerca de 35 minutos para desenhar a primeira run; o custo depende do número de agents
**Fonte:** [documentação oficial de Dynamic Workflows](https://docs.devin.ai/work-with-devin/dynamic-workflows) · documentação oficial verificada em 26 de novembro de 2026

> **Estado da evidência:** este é um guia operacional baseado em fonte oficial, ainda não uma reprodução independente. Uma workflow real inicia várias sessões Devin e pode consumir muitas ACUs; por isso o exercício de reprodução abaixo é deliberadamente estreito e depende de aprovação.

## Quando usar

Use uma dynamic workflow quando o trabalho tiver estrutura real:

- **Fan-out amplo com etapa de combinação** — aproximadamente cinco ou mais arquivos, módulos, endpoints, tickets ou candidatos independentes, cada um exigindo julgamento ou verificação, seguidos de merge/deduplicação/recomendação.
- **Pipeline em estágios** — estágios posteriores consomem output estruturado dos anteriores, como *audit → fix → verify*.
- **Loop controlado** — repetir run/fix/check até uma condição de parada mensurável.

**Não** use quando:

- Um codemod, autofix de linter, gerador ou shell loop resolve mecanicamente.
- Apenas uma ou duas sessões independentes são necessárias e não há dados fluindo entre elas.
- O trabalho é fortemente acoplado por estado compartilhado, ou pequeno e sequencial.

Uma workflow não é “mais IA”. É orquestração como código: o script decide quais agents rodam, em que ordem, com quais prompts e quais dados estruturados avançam.

## Modelo mental

```text
Você descreve o resultado
        ↓
Devin escreve workflow.py
        ↓
o script chama agent(...) com prompt + JSON Schema
        ↓
cada agent retorna output estruturado
        ↓
prompts posteriores são construídos a partir de outputs anteriores
        ↓
a run é registrada e pode ser retomada
```

A sessão orquestradora continua interativa enquanto a workflow roda em segundo plano. O painel da workflow mostra fases, agents e status ao vivo; você pode abrir sessões individuais, pedir um resumo de progresso ou parar a run.

Em contas Enterprise, um admin pode precisar ativar **Dynamic workflows** em **Enterprise Settings → Devin** antes que qualquer organização da empresa possa usá-las.

## Contrato de autoria

Devin escreve o script, mas você deve revisá-lo como código de produção antes de aprovar a run.

| Primitive | Uso |
| --- | --- |
| `register_workflow(meta)` | Declara nome, descrição e fases antes dos agents rodarem |
| `agent(prompt, phase=..., schema=...)` | Executa um agent e retorna um dict no formato do JSON Schema |
| `pipeline(items, stage1, stage2, ...)` | Passa cada item pelos estágios independentemente, sem barreira entre eles |
| `parallel([...])` | Executa callables async concorrentemente e espera todas; use apenas quando todos os resultados são realmente necessários, como merge ou deduplicação |
| `log("message")` | Escreve progresso visível durante a run |

Regras de schema:

1. Mantenha schemas pequenos, planos e explícitos.
2. Retorne identificadores e evidência, não ensaios em prosa — nomes de branch, paths, contagens, status, findings de uma linha.
3. Use `None` ou um status explícito de falha quando não houver trabalho downstream.
4. Não coloque secrets em prompts ou schemas.
5. Trate output de agent como input não confiável para o próximo prompt; valide antes de agir.

## Determinismo é o preço do resume

Quando uma workflow é retomada, o script é executado novamente desde o início. Chamadas `agent()` concluídas fazem replay dos outputs registrados; chamadas incompletas ou falhas rodam de novo. Isso só funciona se o script fizer as mesmas chamadas todas as vezes.

Portanto, a lógica e os prompts da workflow não podem depender de:

- hora ou data atual
- aleatoriedade ou IDs gerados
- variáveis de ambiente
- estado do filesystem
- respostas de rede

Qualquer inspeção do mundo externo pertence a uma chamada `agent()`. O script consome o output registrado.

Duas consequências:

- Editar um prompt reexecuta aquele agent e tudo downstream dele.
- Uma run interrompida ou expirada pode ser retomada com seu run ID; o orçamento padrão e máximo de uma run é sete dias.

## Onde os agents rodam

| Modo | Quando usar | Handoff | Principal risco |
| --- | --- | --- | --- |
| Separate VM (padrão) | Agents precisam de máquinas isoladas ou setup normal de repo | push/read de branches git | Mais setup e custo por agent |
| Shared VM | Agents precisam ler ou editar a working tree atual | filesystem compartilhado | Contenção de CPU/memória e colisões de escrita |

Para fan-out em Shared VM, atribua a escritores paralelos arquivos ou diretórios estritamente não sobrepostos. Para pipelines em Separate VM, coloque nomes de branch no output estruturado.

Também é possível fixar agents em um modo Devin mais barato para estágios de alto volume e baixo julgamento, como classificação.

## Construa sua primeira workflow segura

Não aponte a primeira workflow para o repositório inteiro. Use uma fatia ampla o bastante para provar o padrão e pequena o bastante para pagar.

### 0. Escolha uma unidade estreita

Boas primeiras fatias:

- três componentes para auditoria de acessibilidade
- um diretório de queries SQL para problemas de paginação
- cinco tickets abertos para deduplicação e triagem de severidade
- três unidades de migração, cada uma em sua branch

Más primeiras fatias:

- “auditar todo o monorepo”
- “corrigir todos os flaky tests”
- “revisar todos os arquivos para sempre”

### 1. Escreva o resultado, não o script

Exemplo adaptado do padrão oficial de migração:

```text
Use a workflow to audit the auth, billing, and search modules for missing
pagination and N+1 query patterns. Run one analysis agent per module.
For each confirmed issue, run a fix agent on its own branch and verify the
fix with an EXPLAIN plan before and after. Roll up the confirmed fixes,
skipped items, and anything needing human review.
```

Observe o que esse prompt inclui: escopo, unidade de paralelização, estágios, verificação e formato de rollup.

### 2. Revise o script gerado antes de aprovar

Verifique exatamente estes pontos:

- `register_workflow()` é chamado antes dos agents.
- Cada `agent()` tem schema.
- O número de agents é limitado por uma lista explícita, não por crawl ilimitado.
- O comportamento de falha é explícito: retry, pular com status, substituir por default ou falhar a run.
- O script é determinístico.
- Agents em Separate VM passam código por branches; agents em Shared VM não podem sobrescrever uns aos outros.
- O rollup final inclui evidência e itens não resolvidos, não apenas “done”.

Runs são autoaprovadas por padrão. Se quiser um checkpoint antes de cada run, desative **Settings → Preferences → Auto-approve workflows**.

### 3. Execute, observe e pare corretamente

Durante a execução:

- Observe fases e status dos agents no painel.
- Abra uma sessão de agent e confira se prompt e schema correspondem à intenção.
- Peça um resumo de progresso à sessão orquestradora em vez de interromper manualmente cada agent.
- Se o design estiver errado, pare a run. Parar cancela o script e coloca as child sessions restantes em sleep; resultados concluídos permanecem registrados.

### 4. Retome somente preservando determinismo

Se uma run for interrompida, retome com o mesmo script e run ID. Se editar um prompt, entenda que o agent editado e seu downstream viram trabalho novo.

### 5. Salve a workflow comprovada

Depois que uma workflow funcionar, peça para Devin salvá-la como skill do repositório: um `workflow.py` ao lado de um `SKILL.md` descrevendo quando usá-la. Isso transforma orquestração pontual em capacidade organizacional reutilizável.

## Controle de custo

Cada agent de workflow é uma sessão Devin. O custo escala com a largura do fan-out e a profundidade das sessões.

Use esta sequência:

1. Prototipe com 3 itens.
2. Inspecione o uso de ACU por agent no painel.
3. Estime a run completa antes de ampliar.
4. Use modos mais baratos para classificação/extração.
5. Reserve julgamento caro para agents menos numerosos e posteriores.
6. Defina condições duras de parada para loops.

Um loop precisa de condição escrita de saída, como “passa três vezes consecutivas” ou “uma rodada não corrige nada novo”. Sem isso, a workflow pode queimar orçamento produzindo progresso tecnicamente real, mas inútil.

## Verify it

Uma primeira reprodução só é válida se todas estas condições forem verdadeiras:

- [ ] A workflow rodou em uma fatia limitada de 3–5 unidades, não no repo inteiro.
- [ ] O painel mostrou fases e status individual dos agents.
- [ ] Pelo menos um prompt downstream consumiu visivelmente output estruturado de um agent upstream.
- [ ] Uma sessão de agent foi aberta e inspecionada.
- [ ] O rollup final separou resultados verificados, itens pulados, falhas e itens para revisão humana.
- [ ] O uso de ACU foi registrado por agent e para a run.
- [ ] Se interrompida ou parada intencionalmente, a run retomou corretamente ou o motivo da falha foi documentado.

## Armadilhas

- **Usar agents para trabalho mecânico.** Se um script transforma o código deterministicamente, use o script como ferramenta e reserve agents para julgamento.
- **Schemas que retornam ensaios.** Prosa longa é difícil de consumir downstream; retorne fatos estruturados e compactos.
- **Dependência oculta de tempo.** “Hoje”, timestamps, IDs aleatórios ou verificações de rede ao vivo no script quebram a semântica de replay.
- **Colisões de escrita em Shared VM.** Dois agents editando o mesmo arquivo não são paralelismo; são uma fábrica de merge conflicts.
- **Fan-out ilimitado.** Um crawl que descobre mais trabalho dentro da workflow pode explodir o custo. Limite a descoberta ou transforme-a em input aprovado por humano.
- **Sem contrato de falha.** Decida antes de rodar se um agent falho será pulado, repetido, bloqueará o item ou falhará a run.
- **Reuso prematuro.** Não salve uma workflow como skill até ela rodar com sucesso em uma fatia real e seu custo ser compreendido.

## Exercícios

1. Escolha uma tarefa repetitiva de review no seu repo. Escreva o prompt da workflow e liste exatamente os itens do fan-out antes de pedir para Devin executá-la.
2. Desenhe um schema de dois estágios para *audit → fix*. Mantenha cada campo abaixo de 120 caracteres, exceto paths ou nomes de branch.
3. Para um agent falho, escreva três políticas de falha possíveis e escolha uma. Explique o que o rollup deve mostrar.
4. Estime o custo de um fan-out de 50 itens a partir de um protótipo de 3 itens. Que evidência torna a estimativa válida?

## Capstone

Construa uma workflow que audite cinco arquivos ou módulos contra um padrão escrito, corrija problemas confirmados em branches separadas, verifique cada correção com o check real mais estreito disponível e produza uma tabela final de evidências. Salve como skill somente depois de uma segunda execução bem-sucedida.

## Knowledge check

1. Por que prompts de workflow devem evitar “hoje” e IDs aleatórios? *(Uma run retomada reexecuta o script; inputs mutáveis mudam a identidade das chamadas de agent e quebram o replay determinístico.)*
2. Por que `parallel()` não é o primitive padrão de composição? *(A maioria dos pipelines deve fluir item a item; `parallel()` cria uma barreira e serve apenas para estágios que realmente precisam de todos os resultados.)*
3. Qual é o fan-out inicial mais seguro? *(Uma fatia limitada de cerca de 3–5 unidades — grande o suficiente para provar a orquestração, pequena o suficiente para medir custo e inspecionar comportamento.)*
4. Quando uma workflow merece virar skill? *(Depois de ter sucesso em trabalho real, com custo e comportamento de falha conhecidos, e com probabilidade de reúso.)*

## Fontes

- [Dynamic Workflows — documentação oficial](https://docs.devin.ai/work-with-devin/dynamic-workflows)
- [Advanced capabilities — managed Devins](https://docs.devin.ai/work-with-devin/advanced-capabilities)
- [Skills — documentação oficial](https://docs.devin.ai/product-guides/skills)
- [Devin MCP — documentação oficial](https://docs.devin.ai/work-with-devin/devin-mcp)

## Changelog

- 2026-11-26 — Versão inicial baseada na documentação oficial. Evidência independente de reprodução pendente; não trate o exercício como verificado até uma run real ser registrada.
