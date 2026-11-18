# Guia 9 — Playbooks & knowledge: codificando as convenções da sua org

**Objetivo:** tornar sessões e Bots Devin confiáveis em escala de organização, escrevendo o que seus melhores engenheiros presumem — como playbooks (procedimentos repetíveis) e knowledge (contexto permanente).
**Nível:** intermediário · a camada que toda implantação grande publicada compartilha
**Fontes:** [docs.devin.ai](https://docs.devin.ai) · lições de implantação do [Guia 7](enterprise-playbook.md)

## Por que esta camada decide tudo

Todo resultado enterprise publicado — o 8–12× da Nubank, os 92% de PRs autorais da EBANX, os 1.600 seats da Wayfair — repousa sobre convenções codificadas. Sem elas, a saída do Devin varia por sessão: cada uma redescobre seu stack, suas regras de merge, seus hábitos de teste. Com elas, a sessão nº 500 se comporta como seu melhor engenheiro no melhor dia.

Dois artefatos complementares:

| Artefato | O que é | Analogia |
| --- | --- | --- |
| Knowledge | Contexto permanente que o Devin lê — fatos do repo, convenções, pegadinhas do ambiente | Docs de onboarding |
| Playbook | Procedimento nomeado e repetível — gatilho, passos, critérios de aceite | Um runbook que qualquer um invoca |

## Passo 1 — Minere suas próprias correções

O conhecimento mais barato já existe: percorra suas últimas 20 sessões Devin e colete cada vez que você digitou uma correção — *"we deploy via Cloud Run,"* *"never `git push --force`,"* *"tests need `npm run db:seed` first."* Cada correção é uma entrada de knowledge com prova de que importou.

Minere também:
- Comentários de code review que humanos repetem em PRs do Devin
- Descrições de PR que explicam *por que* uma mudança foi moldada de certa forma
- Docs de onboarding — tudo que você contaria a um novo contratado

## Passo 2 — Escreva entradas de knowledge que pegam

Boas entradas são uma linha, imperativas e escopadas:

```text
- Deploy only via `make deploy-cloudrun` — never run gcloud directly.
- Migrations require a matching rollback file in prisma/rollbacks/.
- The staging seed user is qa+admin@corp.io; never create real-looking users.
```

Más entradas são ensaios, votos ("write good tests") ou segredos (nunca coloque credenciais no knowledge — use o secrets store).

## Passo 3 — Playbooks para trabalho repetível

Um playbook empacota um procedimento para que qualquer sessão (ou Bot) o execute da mesma forma. Estrutura que funciona:

```markdown
# <Verbo + objeto> — ex.: "Cut a release"
## When to use
<a condição gatilho>
## Steps
1. <passo determinístico>
2. ...
## Acceptance
<a checagem passa/falha>
## Failure modes
- <quebra conhecida → o que fazer>
```

Publique org-wide para que sessões, automações e Bots possam invocá-lo — é isso que transforma uma sessão bem-sucedida isolada em capacidade da organização.

## Passo 4 — Alimentando Bots

As **Instructions** do Bot (Guia 1) são a versão escopada ao Bot do knowledge — as regras lidas no início de cada sessão. Coloque lei-do-cargo ali; lei-da-org no knowledge; procedimentos em playbooks. O empilhamento mantém cada artefato pequeno e atual.

## Passo 5 — O loop de correção

Knowledge apodrece. O loop que o mantém verdadeiro:

1. Uma sessão/Bot erra → você corrige no chat
2. O Bot escreve a correção na memória (ou você adiciona ao knowledge)
3. Revisão semanal: promova itens repetidos da memória do Bot para o knowledge da org; delete entradas que ninguém disparou em um mês

O Devin Coach (um template oficial de Bot) existe exatamente para isso — reporta semanalmente onde o Devin travou e propõe uma correção por vez: uma nota, um skill ou uma mudança de setup.

## Checklist de verificação

- [ ] Uma sessão nova no seu repo faz zero perguntas que seu knowledge já responde
- [ ] A última correção que você deu a um Bot aparece nos arquivos de memória dele
- [ ] Duas sessões diferentes rodam o mesmo playbook e produzem resultado da mesma forma

## Armadilhas

- **Escrever votos.** "Follow best practices" não muda nada; "run `npm run db:seed` before tests" muda tudo.
- **Set-and-forget.** Knowledge velho é pior que nenhum — o Devin o segue confiante. Revise mensalmente.
- **Duplicar docs.** Knowledge deve guardar o que o Devin *erra* ou *não pode saber*, não uma cópia da sua wiki.

## Teste de conhecimento

1. Qual a diferença entre playbook e knowledge? *(Playbook é procedimento repetível para uma tarefa nomeada; knowledge é contexto permanente que toda sessão deve presumir.)*
2. Por que "escrever o que seus melhores engenheiros presumem" é o gargalo enterprise de verdade? *(Qualidade do agente nunca foi o limitante — contexto faltante é; a camada de knowledge é onde vivem as convenções da org.)*
3. Quando uma convenção vira playbook vs. permanece conhecimento tribal? *(Na primeira vez que uma sessão erra de um jeito que um passo escrito teria prevenido.)*

## Fontes

- [docs.devin.ai](https://docs.devin.ai) — knowledge, playbooks, instructions/memória de Bot
- Relacionado: [Guia 7 — Padrões de rollout enterprise](enterprise-playbook.md) (esta camada é o passo que a maioria dos rollouts pula)
