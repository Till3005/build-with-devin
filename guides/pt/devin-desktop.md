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
- **Devin Review**: o walkthrough do PR (diff, bugs, gravação do teste) abre como página na mesma janela — a etapa de revisão do loop do [Guia 19](the-session-loop.md).
- **Paines lado a lado** (23/11): `Option/Alt+clique` num link de sessão abre em split pane — compare duas execuções ou monitore uma sessão longa enquanto inicia outra.
- **Busca de sessões em `Cmd/Ctrl+K`**: a busca mudou para a command palette; a busca inline da barra Sessions foi removida.

## Devin Local — a mudança do daemon

Desde a v3.13.4 (Desktop) / v3000.13.4 (CLI), uma sessão local roda num **processo em background**, não dentro da janela que a iniciou:

- Fechar ou reabrir o Devin Desktop — ou o CLI — **não** para a sessão.
- A mesma sessão é **visível a todos os clientes** (`devin ls`, a lista do Desktop), mas a anexação é exclusiva: o segundo cliente vê um banner de trava e o force-open para o primeiro e transfere a sessão.
- `devin daemon` inicia/para/verifica o processo; ele sai ~10 min depois que a última sessão e o último cliente saem.
- `--process-model` escolhe `daemon` vs `in-process`; `process_model` no `config.json` ou `/config` define o padrão.
- `devin ls`, `devin -r` e `/resume` abrem um **monitor de sessões** — sessões por última atualização, com status, diretório e contagem de mensagens.

Consequência prática: trabalho local agora é durável. Comece uma tarefa longa, feche o laptop, reconecte de outro cliente — a sessão continuou rodando.

## Local Hands — uma sessão cloud alcança sua máquina

Local Hands é diferente de Devin Local. Devin Local *é* uma sessão rodando na sua máquina; Local Hands mantém a sessão cloud e a VM dela, e adiciona um segundo conjunto de ferramentas aprovadas no seu computador para arquivos, comandos ou recursos atrás da VPN.

- No Desktop, aprove o cartão de acesso da sessão.
- No app web, rode o comando `devin connect` mostrado no cartão e deixe em execução.
- Se a sessão começou com `devin --cloud`, o CLI conecta sua máquina automaticamente.
- Só o dono da sessão pode conectar uma máquina; sessões agendadas sem humano, automations e sessões API de service user não podem pedir isso.

Local Hands **não é Devin Connect** (o recurso de rede privada). Use quando o agente cloud precisa de estado local; trate cada cópia de arquivo e comando como travessia de fronteira.

## Modo IDE

- O IDE embutido salva com **Cmd/Ctrl+S** (sem auto-save); abas não salvas mostram um ponto.
- No preview do navegador do Devin Local, **selecionar um elemento da página ou saída do console adiciona ao composer** — aponte o bug em vez de descrevê-lo.
- A aba Files pré-visualiza PDFs, renderiza CSV/TSV como tabelas e toca mídia.

## Notas de modelo — SWE-2.1

SWE-2.1 está disponível no Devin Desktop, Cloud e CLI. Segundo a Cognition, é grátis no Desktop/CLI até 8 de dezembro de 2026 e tem preço promocional até 30 de janeiro de 2027. **SWE-2.1 Ultrafast** serve o mesmo modelo a 10× velocidade de tokens via Cerebras; **SWE-2.1 Cyber** está sendo lançado no Devin Security com salvaguardas mais permissivas para trabalho defensivo. Trate os benchmarks publicados como autorrelato do fornecedor, não verificação independente.

## Dois fluxos que valem copiar

**1. Local → cloud → local.** Trabalhe no Devin Local, bata no limite (precisa de ferramentas da org, mais paralelismo, mais tempo que o laptop fica aberto), `/handoff` pro cloud, revise o PR de volta em casa. O daemon torna as duas metades retomáveis.

**2. Uma janela, todas as superfícies.** Command Center para a visão da frota, Local para o repo em que você está, um Bot para o resultado que você não quer cuidar — Desktop é o único lugar onde os três dividem uma janela.

## Passo a passo real — gravado no Devin Desktop v3.14.30825

Uma execução de verdade, não uma montagem: macOS, plano Pro. Uma sessão Devin Local edita um `demo-repo` descartável em SWE-2 High, sobrevive ao fechamento do app e é passada entre o CLI e o Desktop.

**Vídeo (91 s, sem áudio):** Command Center → abas → Bots → Devin Local → prova do daemon → IDE view.

[![Sessão Devin Local terminando em SWE-2 High — 2 arquivos alterados no demo-repo](https://till3005.github.io/built-with-devin/assets/guides/devin-desktop/walkthrough-poster.webp)](https://till3005.github.io/built-with-devin/assets/guides/devin-desktop/walkthrough.mp4)

![1. Command Center Home — sessões recentes, Your Bots, alternador Cloud/Local no composer](https://till3005.github.io/built-with-devin/assets/guides/devin-desktop/step1-command-center.webp)
*1. Command Center Home — sessões recentes, Your Bots e o alternador Cloud/Local no composer*

![2. O seletor de modelo do composer — níveis de capacidade e previews de modelos](https://till3005.github.io/built-with-devin/assets/guides/devin-desktop/step2-model-picker.webp)
*2. O seletor de modelo do composer: níveis de capacidade (Fusion → Free) e previews incl. SWE-2 Lightning/Flash*

![3. Uma sessão em nuvem abre como aba; a barra direita tem Computer, Files, Changes, Terminal](https://till3005.github.io/built-with-devin/assets/guides/devin-desktop/step3-session-tab.webp)
*3. Uma sessão em nuvem abre como aba — a barra direita tem Computer, Files, Changes, Terminal*

![4. O menu "..." do cabeçalho da sessão — uso, arquivar, config de rede, criar automation/skill da sessão](https://till3005.github.io/built-with-devin/assets/guides/devin-desktop/step4-session-menu.webp)
*4. O menu "..." do cabeçalho da sessão; servidores MCP aparecem aqui quando a sessão os tem (esta não tem)*

![5. Bots no Desktop — a página Bots abre, mas enviar mensagens exige Max ou Teams](https://till3005.github.io/built-with-devin/assets/guides/devin-desktop/step5-bots-gate.webp)
*5. Bots no Desktop: a página abre, mas este plano não envia mensagens a um Bot — "Bots require Max or Teams" (lacuna honesta)*

![6. Devin Local pede aprovação antes de rodar comandos — Allow ou Reject, um a um](https://till3005.github.io/built-with-devin/assets/guides/devin-desktop/step6-local-approval.webp)
*6. Devin Local pede aprovação antes de rodar comandos — Allow ou Reject, um a um*

![7. A sessão Local terminou em SWE-2 High — 2 arquivos alterados, com diff de revisão rápida](https://till3005.github.io/built-with-devin/assets/guides/devin-desktop/step7-local-done.webp)
*7. A sessão Local terminou em SWE-2 High — 2 arquivos alterados, com diff de revisão rápida*

![8. Prova do daemon: ao sair do Desktop, `devin ls` ainda lista a sessão; retomar anexa com o transcript completo](https://till3005.github.io/built-with-devin/assets/guides/devin-desktop/step8-cli-attached.webp)
*8. Prova do daemon: ao sair do Desktop, `devin ls` ainda lista a sessão — retomar anexa com o transcript completo*

![9. O segundo cliente vê banner de trava; Force open transfere a sessão, o primeiro desconecta](https://till3005.github.io/built-with-devin/assets/guides/devin-desktop/step9-force-open.webp)
*9. Dois clientes não co-pilotam: o segundo vê banner de trava, Force open transfere a sessão, o primeiro desconecta*

![10. IDE view: Source Control lista as edições da sessão; abas não salvas mostram um ponto até Cmd+S](https://till3005.github.io/built-with-devin/assets/guides/devin-desktop/step10-ide-view.webp)
*10. IDE view: um editor real em volta da mesma sessão — Source Control lista suas edições; abas não salvas mostram um ponto até Cmd+S*

## Verifique

- [ ] Uma sessão Devin Local sobrevive a fechar e reabrir o Desktop
- [ ] `devin ls` viu uma sessão criada no Desktop e `devin -r` a retomou com o transcript completo
- [ ] `devin ls` abriu o monitor de sessões e entrou numa sessão em execução
- [ ] Um Bot criado no chat do Desktop respondeu nesse chat

## Armadilhas

- **"Not authorized to use the CLI"** — contas com acesso ao Desktop mas sem acesso ao CLI batem nisso no sign-in do Devin Local (corrigido na v3.14.30825; atualize se aparecer).
- **Abas são estado da janela.** Uma ação numa página de sessão só atua na própria aba — mas a *sessão* é compartilhada, então um segundo cliente anexando vê a mesma sessão viva, não uma cópia.
- **Máquinas gerenciadas:** admins de enterprise controlam as configurações do Desktop via políticas de dispositivo (ex.: `DetectProxy` para o language server) — confira com o TI antes de depurar a rede sozinho.
- **"Archive" vs "Mark done".** O menu "..." do Desktop (frame 4) ainda diz *Archive*, mas o webapp renomeou para *Mark done* (16/11): a sessão vai para a pasta Done mas continua rodando e visível aos demais assinantes — a barra lateral agora lista as sessões que você assina, então não "limpe" uma sessão da qual outros dependem. Relacionado: o novo **Phonebook** vincula as identidades de cada membro entre Devin/Slack/Teams/git/Jira/Linear.

## Teste rápido

1. O que mudou nas sessões locais na v3.13.4? *(Passaram a rodar num processo em background — fechar o app não as interrompe mais, e qualquer cliente pode ver e assumir a sessão.)*
2. Quando escolher Devin Local em vez de sessão cloud? *(Quando você quer edições práticas no repo checked-out com contexto local; delegue ao cloud para escala ou integrações da org.)*
3. O que há no menu "..." do cabeçalho da sessão? *(Os MCP servers da sessão — liga/desliga ou reautentica por sessão.)*

## Fontes

- [Changelog do Devin Desktop](https://docs.devin.ai/desktop/changelog) — v3.13.4 (abas, sessões locais em background), v3.14 (Bots no Desktop, política `DetectProxy`)
- [Release notes do Devin](https://docs.devin.ai/release-notes/2026) — 16/23 de nov.: *Mark done*, barra de assinaturas, Phonebook, split panes, busca Cmd/Ctrl+K
- [Docs de Local Hands](https://docs.devin.ai/work-with-devin/local-hands) — acesso de sessão cloud à sua máquina via Desktop, `devin connect` ou `devin --cloud`
- [Introducing SWE-2.1](https://cognition.ai/blog/swe-2-1) — disponibilidade e claims de modelo autorrelatados
- [Changelog do Devin CLI](https://docs.devin.ai/cli/changelog/stable) — v3000.13.4: `devin daemon`, `--process-model`, monitor de sessões
- Relacionado: [Guia 12 — Devin CLI e extensibilidade](devin-cli.md) · [Guia 1 — Seu primeiro Bot](bots-101-first-bot.md)
