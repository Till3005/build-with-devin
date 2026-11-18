<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/cover-dark.svg">
  <img src="assets/cover-light.svg" alt="Build with Devin" width="100%">
</picture>

<br/>

[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![License: CC0-1.0](https://img.shields.io/badge/License-CC0_1.0-lightgrey.svg)](LICENSE)

<sub>Curado por [@darega0mae](https://x.com/darega0mae) · Registro irmão: [built-with-devin](https://github.com/Till3005/built-with-devin) · [Melhore um guia](CONTRIBUTING.md)</sub>

<sub>**16** guias · **3** trilhas · todo padrão derivado de uma implantação nomeada e documentada</sub>

<sub>[English](README.md) · [简体中文](README.zh.md) · [日本語](README.ja.md) · Português</sub>

</div>

> *Projeto comunitário não oficial — sem afiliação, endosso ou patrocínio da Cognition AI. "Devin" é marca registrada da Cognition AI. Recursos de marca usados conforme o kit oficial em [devin.ai/brand](https://devin.ai/brand). Documentação oficial: [docs.devin.ai](https://docs.devin.ai).*

**Build with Devin** é uma coleção de tutoriais: cada guia pega uma implantação *real e documentada* do Devin — da frota de lançamento da própria Cognition a casos de clientes publicados — e a decompõe em passos reproduzíveis na sua própria conta. Sem demos hipotéticos; todo padrão aqui tem uma implantação nomeada e números publicados por trás.

**Use junto com [built-with-devin](https://github.com/Till3005/built-with-devin)** — o registro irmão de tudo que a comunidade e a Cognition já entregaram. O registro responde *o que existe*; este repo responde *como construir*.

```mermaid
flowchart LR
    subgraph Bots
      G1["1 · Seu primeiro Bot"] --> G2["2 · Bot dono de produto"]
      G1 --> G3["3 · Bot sentinela"]
      G2 --> G4["4 · Organização multi-Bot"]
      G3 --> G4
      G4 --> G5["5 · Swarm ancorado"]
    end
    subgraph Plataforma
      G6["6 · Automations"] --> G7["7 · Rollout corporativo"]
      G8["8 · Trabalho de design"]
      G9["9 · Playbooks & conhecimento"]
      G10["10 · Devin Apps"]
    end
    subgraph Workflows
      G11["11 · Migrações em escala"]
      G12["12 · CLI & extensibilidade"]
      G13["13 · Cookbook oficial"]
      G14["14 · Relatos de campo"]
      G15["15 · Living evals"]
    end
    G7 --> G9
    G11 --> G9
```

## Guias

### Devin Bots

| # | Guia | Você vai construir | Baseado em | Nível |
| --- | --- | --- | --- | --- |
| 1 | [Seu primeiro Bot](guides/pt/bots-101-first-bot.md) | Um Bot dono de um resultado — chat, sessões, Needs-you, memória, superfícies | [Documentação oficial](https://docs.devin.ai/work-with-devin/bots) | Comece aqui |
| 2 | [Bot dono de produto](guides/pt/bots-201-product-owner.md) | Um Bot que gerencia como produto uma superfície inteira de app | Android Bot — 44 dias, 1.134 PRs | Intermediário |
| 3 | [Bot sentinela agendado](guides/pt/bots-202-scheduled-sentinel.md) | Um Bot em cron que vigia uma checagem e corrige regressões | Layout Bot — 159 PRs/3 sem. | Intermediário |
| 4 | [Organização multi-Bot](guides/pt/bots-203-multi-bot-org.md) | Uma hierarquia de Bots com grants e relatórios consolidados | SuperJennyStack — ~20 Bots, 1.900 PRs/sem | Avançado |
| 5 | [Swarm ancorado em referência](guides/pt/bots-204-reference-grounded-swarm.md) | Um swarm dirigido escrevendo um sistema verificado | Harvey "Phil" — ~30 agentes, 1M+ linhas | Avançado |
| — | [Prompts de outcome de Bots, dissecados](guides/pt/bot-outcome-prompts.md) | Prompts de outcome que atribuem propriedade, não tarefas — os reais, por engenharia reversa | Prompt do Android Bot + os 16 templates do marketplace | Referência |

### Plataforma

| # | Guia | Você vai construir | Baseado em | Nível |
| --- | --- | --- | --- | --- |
| 6 | [Automations orientadas a eventos](guides/pt/automations-101-event-driven.md) | Sessões disparadas por Slack, GitHub, Linear, cron, webhooks | [Docs de Automations](https://docs.devin.ai/product-guides/automations) | Comece aqui |
| 7 | [Padrões de rollout corporativo](guides/pt/enterprise-playbook.md) | As seis formas de implantação por trás dos maiores resultados | Nubank, Gumroad, EBANX, Modal, Airbyte… | Intermediário |
| 8 | [Trabalho de design & visual](guides/pt/design-with-devin.md) | Direção de arte de UI de produção via chat do Devin | Relato da landing page Spraycash | Intermediário |
| 9 | [Playbooks & conhecimento](guides/pt/playbooks-and-knowledge.md) | Codificar as convenções da org para toda sessão herdá-las | A camada por trás de todo resultado corporativo | Intermediário |
| 10 | [Devin Apps](guides/pt/devin-apps.md) | Ferramentas internas e dashboards ao vivo servidos da máquina do Devin | [Lançamento Devin Apps](https://devin.ai/blog/devin-apps) | Comece aqui |

### Workflows

| # | Guia | Você vai construir | Baseado em | Nível |
| --- | --- | --- | --- | --- |
| 11 | [Migrações em escala](guides/pt/migrations-at-scale.md) | Uma migração como centenas de PRs pequenos e verificados | Playbook oficial + Nubank | Intermediário |
| 12 | [Devin CLI & extensibilidade](guides/pt/devin-cli.md) | O agente local: handoff para a nuvem, skills, plugins, hooks | [Docs do CLI](https://docs.devin.ai/cli/index.md) | Intermediário |
| 13 | [Cookbook oficial de casos de uso](guides/pt/official-cookbook.md) | 40+ receitas documentadas — loops de higiene, incidentes, qualidade | [Galeria de casos de uso](https://docs.devin.ai/use-cases/gallery/index.md) | Comece aqui |
| 14 | [Relatos de campo da comunidade](guides/pt/community-field-reports.md) | O que times reais aprenderam — vitórias, falhas e implantações nomeadas com números | 15+ relatos hands-on publicados | Comece aqui |
| 15 | [Living evals de traces de produção](guides/pt/living-evals.md) | Uma suite de evals autocrescente: Devin reproduz falhas de produção numa cópia completa do sistema | Rox — 72% de cobertura de uso vs 43–57% escrito à mão | Avançado |

<p align="right"><a href="#readme">back to top</a></p>

---

## Como usar este repositório

- **Novo em Bots?** Faça o guia 1, depois escolha 2 ou 3 — são os mais reproduzíveis.
- **Quer vitórias rápidas?** As receitas de higiene agendada do guia 13 são a implantação inicial mais barata.
- **Gerenciando um time?** Os guias 4, 7 e 9 foram escritos para você.
- Todo guia termina com **Sources** — o post de lançamento, página de docs ou relato do qual o padrão foi destilado — e **Verify it**, a checagem que confirma que a reprodução funcionou.

<p align="right"><a href="#readme">back to top</a></p>

---

## Convenções

- Cada guia é autocontido: objetivo → pré-requisitos → a construção, passo a passo → operar o resultado → armadilhas.
- Prompts são citados literalmente quando a fonte os publicou; caso contrário são reconstruções, marcadas como tal.
- Os números de um guia vêm da implantação citada, não de suposições nossas.

## Contribuindo

Encontrou uma receita melhor, ou reproduziu uma e tem números? Veja [CONTRIBUTING.md](CONTRIBUTING.md).

## Licença

[CC0-1.0](LICENSE) — dedicado ao domínio público.
