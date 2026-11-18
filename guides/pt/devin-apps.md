# Guia 10 — Devin Apps: ferramentas ao vivo a partir de um chat

**Objetivo:** descrever uma ferramenta interna, dashboard ou cópia de staging — o Devin a constrói e serve numa URL estável que sua equipe abre fazendo sign-in.
**Nível:** comece aqui (guia de plataforma) · **Tempo:** ~10 minutos até a primeira App
**Fonte:** [Introducing Devin Apps](https://devin.ai/blog/devin-apps) (13 nov 2026)

## O que é

Uma Devin App é uma aplicação web ao vivo e privada hospedada diretamente na máquina cloud do Devin. Você descreve a ferramenta, o Devin a constrói, sua equipe a abre por um link — sem hosting, sem pipeline de deploy. Como roda *na* máquina do Devin, ela alcança seus MCPs, integrações, codebase e seu próprio banco de dados (SQLite/Postgres na mesma box), e chama a própria API do Devin.

## Construir uma

1. Sidebar → **Apps** → descreva o que a App deve fazer (ou escolha um template de prompt: dashboard de métricas, status de projeto, fila de review) → **Build with Devin**
2. O Devin faz perguntas de esclarecimento na sessão, constrói e põe online — a página de Apps mostra sua URL, status `Building` até a v1 estar no ar
3. **Share** — copie o link; escopo para pessoas nomeadas, sua org ou sua enterprise. Apps nunca são públicas; abrir uma exige sign-in no Devin

Você também pode dizer "publish this as an App" dentro de qualquer sessão que produziu um browser preview.

## Loop de atualização

- **Edit in session** na página da App → descreva a mudança → o Devin constrói uma nova versão na mesma URL. Toda atualização é um deployment versionado; se uma versão nova falhar ao iniciar, a anterior continua servindo.
- **Mantida fresca por automação:** ligue uma automação (Guia 6) para re-deployar em agenda ou em mudanças de branch — um dashboard que puxa dados frescos toda manhã é o uso canônico.

## Como rodam (as partes que importam)

- **Hibernação:** Apps são construídas sobre snapshots de memória — a máquina dorme quando não usada, acorda ao abrir (primeira carga pode levar alguns segundos). A cobrança segue o tempo acordado.
- **Stack:** qualquer coisa servindo HTTP numa porta; DB co-localizado na máquina.
- **Fronteira de escala:** uma máquina — ótimo para ferramentas internas e dashboards, **não** para serviços de produção de alto tráfego.

## Os três usos comprovados

| Uso | Exemplo |
| --- | --- |
| Ferramentas internas | Painéis admin, formulários de pedido, filas de aprovação — os matadores de planilha compartilhada |
| Dashboards | Boards de métricas/suporte/vendas puxando de suas fontes de dados, atualizados em agenda |
| Cópias beta/staging | Seu stack real (frontend+backend+DB+workers) rodando na máquina do Devin — colegas abrem uma cópia de staging por um link |

## Checklist de verificação

- [ ] A App carrega na sua URL estável depois de a máquina dormir (espere cold start de alguns segundos)
- [ ] Uma mudança por edit-in-session produziu nova versão na mesma URL
- [ ] O escopo de compartilhamento está certo: um colega sem acesso é barrado no sign-in

## Armadilhas

- **Tráfego de produção.** Uma máquina, dorme quando ociosa — não aponte usuários para ela; aponte sua equipe.
- **Pensamento estático.** O poder de uma App é que ela *vive no ambiente do Devin* — ligue-a aos seus dados/MCPs, ou você construiu uma Vercel mais fraca.

## Teste de conhecimento

1. Qual a diferença entre uma Devin App e um PR preview? *(A App é servida ao vivo da máquina do Devin numa URL estável — stateful, persistente, com gate de sign-in — não um artefato de build.)*
2. Por que "sua equipe abre fazendo sign-in" importa para ferramentas internas? *(A autenticação é herdada da org — sem sistema de login separado para construir ou proteger.)*
3. Que classe de ferramenta interna encaixa melhor em Apps? *(Dashboards e superfícies de staging onde "bom o bastante agora" vence "perfeito depois" — o custo de manutenção é quase zero.)*

## Fontes

- [Introducing Devin Apps](https://devin.ai/blog/devin-apps)
- Relacionado: [Guia 6 — Automações orientadas a eventos](automations-101-event-driven.md) para refresh agendado
