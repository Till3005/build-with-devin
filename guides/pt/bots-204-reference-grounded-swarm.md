# Guia 5 — Enxame ancorado em referência

**Objetivo:** dirigir um enxame de agentes para escrever um sistema grande e *verificável* — onde a correção é checada continuamente contra uma referência confiável, não contra impressões.
**Nível:** avançado
**Implantação de origem:** o **"Phil"** da Harvey — segundo o relato direto de Gabe Pereyra, ~30 agentes escreveram um motor de editor colaborativo compatível com Word em Rust + TypeScript: **1M+ linhas em 3 semanas, zero engenheiros humanos**. Verificado continuamente contra o comportamento real do Microsoft Word e negociações de advogados simuladas. Humanos direcionaram via memória + logs de decisão, nunca lendo código.
**Fontes:** relato de lançamento de Gabe Pereyra ([post direto](https://x.com/gabepereyra/status/2122756324173992166)) · [post de lançamento](https://devin.ai/blog/introducing-devin-bots)

## O padrão

Um enxame falha quando ninguém consegue dizer se a saída está certa. O Phil funcionou porque cada linha podia ser checada contra uma **referência de verdade**: o Microsoft Word real. O trabalho do time de agentes era *igualar* — um alvo objetivo e continuamente verificável — não *inventar*.

```text
   sistema de referência (verdade)
            ▲ compara
            │
┌───────────┴────────────┐
│  enxame de ~30 agentes │──► 1M+ LOC (Rust + TypeScript)
└────────────────────────┘
            ▲ direciona
            │
   humanos: memória + logs de decisão
   (nunca lendo o código)
```

## Quando usar

| Boa aplicação | Má aplicação |
| --- | --- |
| Reimplementar uma spec (formato de arquivo, protocolo, editor, compilador) | Produtos greenfield sem resposta objetiva |
| Portabilidade/migração com oráculo (sistema legado ainda roda) | UX nova onde "certo" é questão de julgamento |
| Qualquer coisa difável contra um sistema funcionando | Sistemas onde correção precisa de usuários |

O teste de tornassol: **uma máquina consegue decidir "correto" sem você?** Se sim, um enxame escala; se não, use um Bot product-owner (Guia 2).

## Passo 1 — Garanta a referência primeiro

Antes de qualquer agente escrever código, a checagem deve existir:

- A referência da Harvey: **comportamento real do Microsoft Word** — documentos renderizados no editor do enxame tinham que igualar o Word
- A sua pode ser: o sistema legado ainda rodando, uma suíte de conformidade, golden files, um corpus de testes da spec, um contrato de API

Coloque a comparação no CI ou num script que o enxame roda constantemente — "a saída bate com a referência?" precisa ser barato e automático, ou os agentes desviam entre checagens.

## Passo 2 — Decomponha em fatias possuídas

~30 agentes não compartilhavam um backlog — o trabalho foi fatiado para que cada agente fosse dono de um subsistema (modelo de documento, motor de layout, protocolo de colaboração, …). Estruture como o organograma do Guia 4, exceto que cada "funcionário" é uma sessão de código apontada para uma fronteira de módulo:

```text
You own the <module>. Its contract is <interface/reference behavior>.
Your PRs are accepted when the reference checks pass — not when the
code looks done.
```

## Passo 3 — Humanos direcionam acima do código

Ninguém na Harvey leu o milhão de linhas. A direção aconteceu via:

- **Memória** — os fatos acumulados do Bot sobre decisões tomadas e por quê
- **Logs de decisão** — o que o enxame escolheu em cada bifurcação
- **Mensagens de direção** — "priorize fidelidade de track-changes sobre performance esta semana"

Sua superfície de revisão é a *trilha de decisões*, não o diff. Se você se pega lendo código gerado para saber o que está acontecendo, peça o log de decisões ao orquestrador.

## Passo 4 — Validação adversarial por cima

A Harvey adicionou uma segunda camada: **negociações de advogados simuladas** — uso realista que expõe o que uma suíte de conformidade perde. Seu equivalente: uma camada de cenários sobre o diff de referência — workflows reais, inputs adversariais, fuzzing. Checagens de referência pegam o *errado*; checagens de cenário pegam o *frágil*.

## Checklist de verificação

- [ ] Uma checagem de referência automatizada existe e roda contra cada mudança
- [ ] O critério de aceitação de cada agente é "a referência passa", nunca "código escrito"
- [ ] Você consegue responder "o que o enxame decidiu e por quê" a partir de logs/memória sem ler código
- [ ] Um módulo deliberadamente quebrado é pego pela checagem de referência, não por você

## Armadilhas

- **Escalar antes do oráculo.** Um enxame sem checagem só produz volume — o Phil funcionou porque o Word sempre foi o juiz.
- **Revisar diffs.** Não escala além de ~2 agentes; você vira o gargalo e perde a vantagem de velocidade do enxame.
- **Propriedade ambígua.** Dois agentes editando um módulo produzem inferno de merge — as fronteiras de propriedade são a arquitetura.

## Teste de conhecimento

1. Por que o enxame da Harvey funcionou onde a maioria das tentativas multi-agente colapsa? *(Uma referência externa confiável — o comportamento real do Word — tornou a correção verificável por máquina na velocidade do enxame.)*
2. Por que humanos direcionaram via memória e logs de decisão em vez de revisar código? *(1M+ LOC em 3 semanas excede qualquer capacidade humana de leitura; a direção acontece na camada de intenção.)*
3. Qual pré-requisito você checaria antes de tentar esse padrão? *(Se seu domínio tem uma referência contra a qual o enxame possa se checar — se não, construa o oráculo primeiro.)*

## Fontes

- [Post direto de Gabe Pereyra](https://x.com/gabepereyra/status/2122756324173992166) — relato do Phil da Harvey: ~30 agentes, 1M+ LOC, verificação por referência ao Word, simulações de advogados
- [Introducing Devin Bots](https://devin.ai/blog/introducing-devin-bots)
- Relacionado: [Guia 4 — Organização multi-Bot](bots-203-multi-bot-org.md) (mesma hierarquia, propósito diferente: operação vs. construção)
