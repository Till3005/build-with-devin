# Guia 17 — Devin Desktop

**Objetivo:** o editor nativo de agentes — todas as superfícies do Devin numa janela: sessões cloud, sessões locais (Devin Local), Bots e um IDE de verdade em volta.
**Nível:** comece aqui
**Fontes:** [Changelog do Desktop](https://docs.devin.ai/desktop/changelog) · [Changelog do CLI](https://docs.devin.ai/cli/changelog/stable)

## O que é

Devin Desktop é o editor baseado em Windsurf onde todas as superfícies do Devin vivem lado a lado. Três coisas para distinguir:

| Superfície | Onde roda | Use para |
| --- | --- | --- |
| Sessão cloud | Máquina do Devin, na sua org | Tarefas autônomas, trabalho em paralelo, PRs para revisão |
| Devin Local | Processo em background na sua máquina | Edições práticas no repo que você tem aberto |
| Bot | Agente persistente (ver guias 1–5) | Um resultado para assumir — no Desktop desde a v3.14 |

## Agent Command Center

O Command Center é o hub de sessões — não é um editor:

- **Abas** (v3.13.4): várias sessões e páginas abertas numa janela, cada aba com histórico próprio de voltar/avançar — trate como o navegador da sua frota.
- **Menu "..." do cabeçalho da sessão**: os MCP servers da sessão — liga/desliga um, ou reautentica, por sessão.
- **Devin Review**: o walkthrough do PR (diff, bugs, gravação do teste) abre como página na mesma janela.

## Devin Local — a mudança do daemon

Desde a v3.13.4 (Desktop) / v3000.13.4 (CLI), uma sessão local roda num **processo em background**, não dentro da janela que a iniciou:

- Fechar ou reabrir o Devin Desktop — ou o CLI — **não** para a sessão.
- A mesma sessão abre em **vários clientes ao mesmo tempo**: janela do desktop e terminal anexados, cada um mostrando saída e perguntas.
- `devin daemon` inicia/para/verifica o processo; ele sai ~10 min depois que a última sessão e o último cliente saem.
- `--process-model` escolhe `daemon` vs `in-process`; `process_model` no `config.json` ou `/config` define o padrão.
- `devin ls`, `devin -r` e `/resume` abrem um **monitor de sessões** — sessões por última atualização, com status, diretório e contagem de mensagens.

Consequência prática: trabalho local agora é durável. Comece uma tarefa longa, feche o laptop, reconecte de outro cliente — a sessão continuou rodando.

## Modo IDE

- O IDE embutido salva com **Cmd/Ctrl+S** (sem auto-save); abas não salvas mostram um ponto.
- No preview do navegador do Devin Local, **selecionar um elemento da página ou saída do console adiciona ao composer** — aponte o bug em vez de descrevê-lo.
- A aba Files pré-visualiza PDFs, renderiza CSV/TSV como tabelas e toca mídia.

## Dois fluxos que valem copiar

**1. Local → cloud → local.** Trabalhe no Devin Local, bata no limite (precisa de ferramentas da org, mais paralelismo, mais tempo que o laptop fica aberto), `/handoff` pro cloud, revise o PR de volta em casa. O daemon torna as duas metades retomáveis.

**2. Uma janela, todas as superfícies.** Command Center para a visão da frota, Local para o repo em que você está, um Bot para o resultado que você não quer cuidar — Desktop é o único lugar onde os três dividem uma janela.

## Verifique

- [ ] Uma sessão Devin Local sobrevive a fechar e reabrir o Desktop
- [ ] A mesma sessão local anexada do Desktop e do `devin` CLI ao mesmo tempo
- [ ] `devin ls` abriu o monitor de sessões e entrou numa sessão em execução
- [ ] Um Bot criado no chat do Desktop respondeu nesse chat

## Armadilhas

- **"Not authorized to use the CLI"** — contas com acesso ao Desktop mas sem acesso ao CLI batem nisso no sign-in do Devin Local (corrigido na v3.14.30825; atualize se aparecer).
- **Abas são estado da janela.** Uma ação numa página de sessão só atua na própria aba — mas a *sessão* é compartilhada, então um segundo cliente anexando vê a mesma sessão viva, não uma cópia.
- **Máquinas gerenciadas:** admins de enterprise controlam as configurações do Desktop via políticas de dispositivo (ex.: `DetectProxy` para o language server) — confira com o TI antes de depurar a rede sozinho.

## Teste rápido

1. O que mudou nas sessões locais na v3.13.4? *(Passaram a rodar num processo em background — fechar o app não as interrompe mais, e vários clientes podem anexar à mesma sessão.)*
2. Quando escolher Devin Local em vez de sessão cloud? *(Quando você quer edições práticas no repo checked-out com contexto local; delegue ao cloud para escala ou integrações da org.)*
3. O que há no menu "..." do cabeçalho da sessão? *(Os MCP servers da sessão — liga/desliga ou reautentica por sessão.)*

## Fontes

- [Changelog do Devin Desktop](https://docs.devin.ai/desktop/changelog) — v3.13.4 (abas, sessões locais em background), v3.14 (Bots no Desktop)
- [Changelog do Devin CLI](https://docs.devin.ai/cli/changelog/stable) — v3000.13.4: `devin daemon`, `--process-model`, monitor de sessões
- Relacionado: [Guia 12 — Devin CLI e extensibilidade](devin-cli.md) · [Guia 1 — Seu primeiro Bot](bots-101-first-bot.md)
