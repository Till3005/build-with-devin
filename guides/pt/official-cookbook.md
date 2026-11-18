# Guia 13 — O cookbook oficial de casos de uso

**Objetivo:** os padrões de uso comprovados dos próprios docs da Cognition, organizados como um cookbook — o que fatiar para o Devin, e mais de 40 receitas documentadas com prompts para copiar.
**Nível:** comece aqui para amplitude
**Fontes:** [Best Practices](https://docs.devin.ai/use-cases/best-practices.md) · [Use-case gallery](https://docs.devin.ai/use-cases/gallery/index.md) · [use-case tutorials](https://docs.devin.ai/use-cases/index.md)

## A única regra por trás de tudo

Orientação oficial, lógica literal: escolha trabalho **wide & shallow** — um backlog grande de tarefas simples e horizontalmente escaláveis vence builds complexos do zero, sempre.

| Tarefa ideal | Anti-tarefa |
| --- | --- |
| Subtarefas repetitivas em complexidade de engenheiro júnior | Features complexas net-new |
| < 90 minutos de trabalho manual por fatia | Qualquer coisa que não se divide |
| Verificação passa/falha objetiva | "Parece certo para mim" |
| Isolada, retrocompatível, paralelizável | Dependências emaranhadas |

Quatro ótimas formas de fatia dos docs: **migrações, refactors, modernizações, backlogs de tech debt.**

## O catálogo de receitas

Tudo abaixo é um caso de uso documentado na galeria oficial — cada um vem com um prompt pronto para copiar. Organizado pelo trabalho que tira da semana de um humano.

### Incidentes & saúde de produção

| Receita | Mecanismo |
| --- | --- |
| Auto-investigar alertas Datadog/PagerDuty | Gatilho webhook/API → sessão investiga no incêndio |
| Auto-gerar postmortems | PagerDuty resolve → Devin rascunha timeline, causa raiz, action items |
| Correções diárias de erros do Sentry | Cron noturno puxa erros novos → PRs de correção de manhã |
| Depurar um bug report ponta a ponta | Entregue o relato + logs Datadog + acesso ao DB → causa raiz |

### Higiene agendada (a página de maior ROI dos docs)

| Receita | Cadência |
| --- | --- |
| PRs semanais de update de dependências | Semanal: pacotes desatualizados → PRs de upgrade testados |
| E2E noturno em staging | Noturno: roda a suíte, abre tickets para falhas |
| Changelog semanal de PRs mergeados | Sexta: changelog categorizado → Slack |
| Digest diário de saúde Datadog | Diário: varredura de erros → digest no Slack |
| Auditoria diária do design system | Diário: sinaliza cores hardcoded/tokens faltando em PRs mergeados |
| Limpeza de feature flags | Uma sessão única remove flag + código morto pós-release |
| Digest semanal de status no Notion | Semanal: resumo de PR/commit → Notion |
| PRs a partir de transcrições de reunião | De hora em hora: poll Granola → extrai tarefas de eng → sessões filhas |

### Qualidade de código

| Receita | Mecanismo |
| --- | --- |
| Auto-corrigir bugs de PR antes do merge | Devin revisa todo PR, empurra correções para a branch |
| Adicionar testes unitários a um serviço | Construa um skill de escrita de testes, aplique a charge flows/refunds/webhooks |
| Pegar regressões visuais | Skill de repo: screenshot de cada página afetada antes do PR |
| Checklist de migração em todo PR | Skill de repo pega ops destrutivas, valida mudanças de schema |
| Dividir um router monolítico | Router Express de 2.000 linhas → rotas de domínio com middleware compartilhado |
| Subir cobertura de código | Devin analisa a suíte, escreve testes para cobrir as lacunas |
| Patchear CVEs conhecidas entre repos | Skills oficiais ([devin-vuln-fixes](https://github.com/cognitionai/devin-vuln-fixes)): inventário somente-leitura → gate de aprovação → patch em alvo confirmado → testes antes/depois → um PR por repo |

### Migrações & feature work

| Receita | Mecanismo |
| --- | --- |
| REST→GraphQL de 50 arquivos | Escopo → pacotes sem conflito → paralelo (Guia 11) |
| Skill de upgrade React 18→19 | Transforme o guia oficial de upgrade num skill em fases para seu codebase |
| Spec OpenAPI → implementação | YAML spec → handlers Express + validação Zod + Supertest |
| Fluxo de checkout Stripe | Spec → fluxo funcional + testes + verificação em browser |
| i18n num app Next.js | install next-i18next, extração de strings, checagem em browser em 3 idiomas |
| Figma → pixel-perfect | Figma MCP → componentes a partir de mockups |
| Dockerizar um app Django | Dockerfile multi-stage + compose para Django/Postgres/Redis |

### Gestão de projeto & dados

| Receita | Mecanismo |
| --- | --- |
| Auto-triage de bugs via Linear | Label aplicada → Devin investiga |
| PRDs → tickets de sprint | PRD no Notion → tickets Linear escopados |
| Planos de implementação de backlog | Multi-selecionar tickets Linear → planos com score de confiança |
| Consultas `/dana` no Slack | Consultas de banco de dados em linguagem natural de qualquer canal |
| Dashboard custom de uso de API | Devin constrói um dashboard sob medida na API v3 |

### Ficando melhor no próprio Devin ("Devin Optimization")

| Receita | Lição |
| --- | --- |
| Cortar um prompt de feature 42→12 ACUs | Autópsia de uma sessão cara: 3 causas raiz → reescrever o prompt |
| Corrida de 3 sessões num problema | Sessões paralelas tentam estratégias de otimização concorrentes; a melhor vence |
| 8 sessões paralelas de noite | 8 módulos sem testes → PRs de unit tests de manhã |
| Avaliar 30 bibliotecas | Uma sessão por biblioteca → comparação ranqueada com score |
| Transformar um hotfix em skill | Extraia uma sessão de incidente bem-sucedida num skill reutilizável |
| Dedup semanal de knowledge | Sessão agendada mergeia/limpa conflitos de sugestões de knowledge |
| Guia de onboarding de equipe | Devin lê seus próprios docs → um guia de primeiros passos para seu stack |

## Como usar este cookbook

1. Escolha uma receita de **Higiene agendada** — é a primeira vitória mais barata (um loop noturno/semanal sobre o qual você para de pensar)
2. Adicione uma de **Incidentes** se você tem PagerDuty/Datadog/Sentry
3. Quando uma receita funciona, congele-a como um **skill** (Guia 12) ou um **Bot** (Guias 1–5) — cada linha acima sobrevive como um dos dois

## Checklist de verificação

- [ ] Uma receita de higiene está rodando em agenda e produziu seu primeiro PR/relatório
- [ ] Sua saída está congelada como skill, playbook ou Bot — não morando na cabeça de alguém

## Armadilhas

- **Dez receitas, zero congeladas.** Uma receita que continua prompt manual é esquecida até sexta — operacionalize ou descarte.
- **Prompts copiados sem a verificação do seu repo.** Os prompts da galeria assumem que uma suíte de testes existe; adapte a *checagem*, não só a tarefa.

## Teste de conhecimento

1. Por que começar com uma receita de higiene agendada em vez de resposta a incidentes? *(A vitória mais barata possível — roda enquanto você dorme, e uma correção de lint noturna errada é recuperável; uma ação de incidente errada não é.)*
2. O que "congelar uma receita como skill ou Bot" realmente previne? *(Drift de prompt e dependência de pessoa única — a receita sobrevive a quem a escreveu.)*
3. Por que adaptar a parte de verificação de um prompt da galeria antes da parte da tarefa? *(A tarefa descreve intenção; a checagem é o que seu repo consegue provar — checagens erradas produzem lixo confiante.)*

## Fontes

- [Use-case gallery](https://docs.devin.ai/use-cases/gallery/index.md) — todas as receitas acima, cada uma com prompts prontos
- [Best Practices](https://docs.devin.ai/use-cases/best-practices.md) — a doutrina de fatiamento
- [Use-case tutorials](https://docs.devin.ai/use-cases/index.md) — integração de API, cobertura de código, containerização, componentes frontend, MCP
- Relacionado: [Guia 11 — Migrações em escala](migrations-at-scale.md) · [Guia 6 — Automações](automations-101-event-driven.md)
