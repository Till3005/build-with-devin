# Guia 11 — Migrações em escala

**Objetivo:** rodar uma migração grande (linguagem, framework, banco de dados, dependência, arquitetura) como centenas de PRs pequenos verificados em vez de uma reescrita heroica.
**Nível:** intermediário → avançado
**Fontes:** [Best Practices](https://docs.devin.ai/use-cases/best-practices.md) · [Migration & Modernization](https://docs.devin.ai/use-cases/migration-modernization.md) · exemplos de migração: [Java upgrades](https://docs.devin.ai/use-cases/examples/java-upgrades.md), [COBOL](https://docs.devin.ai/use-cases/examples/cobol-modernization.md), [SAS→PySpark](https://docs.devin.ai/use-cases/examples/sas-to-pyspark.md), [JS→TS](https://docs.devin.ai/use-cases/examples/javascript-to-typescript.md), [NoSQL→SQL](https://docs.devin.ai/use-cases/examples/nosql-to-sql.md) · caso Nubank

## O playbook oficial

Os docs do próprio Devin são diretos sobre o que escala: **wide & shallow** vence **tall & deep**. Uma migração é o trabalho wide-and-shallow canônico — a mesma pequena transformação aplicada a centenas de unidades independentes.

```text
migração ──► fatiar em unidades isoladas (<90 min cada)
                    │
           ┌────────┴────────┐
           ▼                 ▼
      skill para a      sessões paralelas,
      transformação     uma fatia cada
           │                 │
           └────► verificar por fatia (testes/build/CI)
                           │
                 revisão humana → merge → repete
```

## Passo 1 — Verifique se sua migração se qualifica

Dos critérios oficiais — a maioria deve valer:

- Alto volume de subtarefas repetitivas
- Complexidade de engenheiro júnior por fatia
- Mudanças isoladas, incrementais, retrocompatíveis
- **Verificação objetiva por fatia** (o requisito duro: testes, build, CI ou um script próprio)
- Dependências mínimas entre fatias

Não se qualifica: uma reescrita de repo inteiro onde tudo precisa aterrissar de uma vez.

## Passo 2 — Fatie

A fatia é a menor unidade atômica — um arquivo, um notebook, um módulo:

| Regra | Por quê |
| --- | --- |
| < 90 minutos de engenharia manual por fatia | A confiabilidade do Devin é por fatia |
| Independente + retrocompatível | Fatias rodam em paralelo e mergeiam em qualquer ordem |
| Cada fatia carrega sua própria verificação | Sem verificação, sem automação — este é o gate de falha |

Exemplo (oficial): uma migração REST→GraphQL de 50 arquivos → escopar, dividir em pacotes de trabalho sem conflitos, rodar em paralelo.

## Passo 3 — Escreva a transformação como um skill

Um skill = a receita repetível que toda sessão roda. Exemplo oficial (Java 7→8, abreviado):

```text
## Procedure
1. Verify the project is on Java 7
2. Install the Java 8 JDK
3. Update build configuration
4. Identify and replace deprecated Java 7 APIs
5. Analyze for Java 8 enhancement opportunities
6. Update unit tests
7. Test thoroughly
8. Update documentation
9. Build and verify
```

Escreva o seu com: passos explícitos, uma referência ponta a ponta (um guia ou vídeo) e **múltiplos exemplos de código antes/depois** — pares entrada/saída são o sinal de maior qualidade que você pode dar.

## Passo 4 — Rode sessões paralelas

Com o skill fixado, distribua fatias entre sessões — a [API](https://docs.devin.ai) ou as sessões filhas de um Bot (Guia 4). Cada fatia → uma sessão → um PR. A revisão humana faz o gate do merge em `main`.

Em escala os números compõem: a migração ETL de milhões de linhas da Nubank rodou esse loop até 8–12× de eficiência — e um Devin fine-tuned cortou o tempo por tarefa de ~40 → ~10 minutos.

## Passo 5 — Vigie a taxa de erro, não a barra de progresso

Taxas de erro pequenas compõem através de milhares de fatias. Opere num dashboard, não em vibes:

- Acompanhe a taxa de aprovação de fatia na primeira tentativa — o skill é seu ponto de correção, não as sessões
- Fatias falhas alimentam de volta o skill (o loop dos próprios docs: *"feed session links into Devin to patch the gaps"*)
- A ordem de merge é livre porque as fatias são isoladas — explore isso

## Checklist de verificação

- [ ] Toda fatia termina em ~90 min e mergeia independentemente
- [ ] Uma fatia que falha a verificação produz uma correção ou um ticket sinalizado — nunca um merge silencioso
- [ ] O skill melhorou mensuravelmente nas primeiras 20 fatias (menos correções humanas por fatia)
- [ ] O progresso é contável: N/M fatias migradas, taxa de aprovação visível

## Armadilhas

- **Migrações sem fatiar.** "Migrar o repo inteiro" é o anti-padrão oficial — sem isolamento, sem paralelismo, sem verificação por unidade.
- **Sem exemplos antes/depois.** O skill sem exemplos produz um estilo diferente por sessão.
- **Pular a revisão humana.** Paralelo ≠ sem supervisão — cada fatia ainda é revisada antes do `main`.

## Teste de conhecimento

1. Por que fatias "wide and shallow" em vez de "deep and complete"? *(Cada fatia precisa aterrissar verde — um PR verificado de 90 minutos compõe; um mega-branch de 3 dias apodrece contra o main.)*
2. Por que toda fatia precisa de sua própria verificação? *(Sem prova por fatia, uma migração de 500 PRs é 500 diffs não verificados — a superfície de falha multiplica em vez de dividir.)*
3. A Nubank reportou 8–12× de eficiência — o que tornou esse número crível e não marketing? *(Metodologia publicada: tempos de estágio medidos antes/depois em pipelines ETL reais, não uma projeção.)*

## Demonstração — o loop de migração executado em série, no Devin CLI v3000.14 (swe-2-flash-medium)

A parte de escala (centenas de sessões paralelas) precisa de cota de nuvem — o *loop* não, então rodamos serialmente na cota gratuita. `migrate-demo`: quatro CLIs em optparse (`greeter`, `calc`, `backup`, `report`), um teste de comportamento por ferramenta e a transformação escrita em `.devin/skills/optparse-to-argparse/SKILL.md`. Prompt: "migrate as independent slices … run the test suite, and only move to the next tool when it's green."

**Vídeo (41 s, sem som):** baseline → skill invocado → 4 fatias, suíte verde após cada uma → zero `optparse`.

[![O loop de fatias completo — cada ferramenta migrada, suíte verde após cada uma, resumo fiel à receita](https://till3005.github.io/built-with-devin/assets/guides/migrations-at-scale/walkthrough-poster.webp)](https://till3005.github.io/built-with-devin/assets/guides/migrations-at-scale/walkthrough.mp4)

![1. Baseline — 4 ferramentas optparse, 7 testes de comportamento verdes](https://till3005.github.io/built-with-devin/assets/guides/migrations-at-scale/step1-baseline.webp)
*1. Baseline: 4 ferramentas em OptionParser, 7 testes, uma receita-skill commitada*

![2. Skill invocado automaticamente de .devin/skills — primeiro lê todas as ferramentas e os testes](https://till3005.github.io/built-with-devin/assets/guides/migrations-at-scale/step2-skill-invoked.webp)
*2. `Invoked skill optparse-to-argparse` — a receita dirige a execução*

![3. O loop de fatias — "Green. Now calc.py — it relies on rest for positional args, so parse_known_args preserves that shape."](https://till3005.github.io/built-with-devin/assets/guides/migrations-at-scale/step3-slice-loop.webp)
*3. Verificação por fatia; ele mesmo notou que calc.py precisa de `parse_known_args` para manter operandos posicionais*

![4. Verificado após /exit — 4 arquivos migrados, +18/−18, nenhuma referência a optparse, nada commitado](https://till3005.github.io/built-with-devin/assets/guides/migrations-at-scale/step4-verify-diff.webp)
*4. Quatro diffs pequenos e verificados — a disciplina de fatias, sem a frota paralela*

## Fontes

- [Best Practices — docs.devin.ai](https://docs.devin.ai/use-cases/best-practices.md)
- [Migration & Modernization + 5 playbooks de exemplo](https://docs.devin.ai/use-cases/migration-modernization.md)
- [Use-case gallery — Migrations](https://docs.devin.ai/use-cases/gallery/index.md)
- [Playbook de migração .NET da Cognition](https://cognition.com/blog/dotnet-migration-with-devin) — Ask Devin ranqueia controllers por contexto, sessões coordenadas portam em paralelo: meses → semanas (publicado pelo fornecedor)
- Relacionado: [Guia 7 — Rollout enterprise](enterprise-playbook.md) (a Forma 1 é este guia em escala de org)
