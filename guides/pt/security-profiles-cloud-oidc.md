# Guia 21 — Security Profiles e Cloud OIDC

**Objetivo:** dar à Devin acesso de menor privilégio em duas camadas: Security Profiles reutilizáveis que limitam o que sessões podem alcançar e operar, e Cloud OIDC que substitui credenciais cloud de longa duração por workload identity de curta duração.
**Nível:** avançado / administrador · **Tempo:** cerca de 45–90 minutos para um primeiro profile governado; a configuração cloud depende do provedor
**Fonte:** [documentação oficial de Security Profiles](https://docs.devin.ai/product-guides/security-profiles) · [documentação oficial de Cloud OIDC](https://docs.devin.ai/product-guides/oidc) · documentação oficial verificada em 26 de novembro de 2026

> **Estado da evidência:** este guia é baseado em fonte oficial, mas ainda não foi reproduzido independentemente contra um provedor cloud. A seção de verificação separa checks possíveis dentro da Devin de checks que exigem recursos de AWS/GCP/Vault/admin.

## Modelo mental de duas camadas

Security Profiles e Cloud OIDC resolvem problemas diferentes:

| Camada | Pergunta respondida | Mecanismo |
| --- | --- | --- |
| Security Profile | O que esta sessão Devin pode alcançar ou operar? | Network allowlist, MCP allowlist, Devin MCP read-only, git access level, remoção do token do GitHub CLI |
| Cloud OIDC | Como esta sessão prova quem é para um serviço cloud? | Identity token de curta duração emitido pela Devin, verificado pela cloud e trocado por credenciais temporárias e escopadas |

Use as duas juntas. Um profile pode impedir que uma sessão alcance ou opere sistemas que não deveria; OIDC remove a necessidade de armazenar chaves cloud quando o acesso é legítimo.

Security Profiles são separados do **Devin Security**, a superfície de scanning de vulnerabilidades. Um profile não configura scan.

## O que um Security Profile pode restringir

Um profile é um conjunto nomeado de restrições opcionais. Ele só restringe as configurações que define.

| Restrição | O que controla | Detalhe importante |
| --- | --- | --- |
| Network policy | Destinos outbound permitidos a partir da máquina da sessão | Hostnames aceitam wildcard `*`; IPv4/IPv6 CIDR são suportados |
| MCP access | Quais MCP servers instalados a sessão pode usar | Independente da network policy; MCP servers permitidos ficam automaticamente alcançáveis |
| Devin MCP access | Se as ferramentas internas de gestão da Devin podem escrever | Read-only ainda permite listar/inspecionar, mas bloqueia writes como criar sessões ou editar knowledge |
| Git access | Apenas clone/fetch ou capacidade completa de push/PR | Read-only bloqueia pushes e criação de PRs |
| GitHub CLI token | Se a máquina carrega um token `gh` para chamadas diretas à API do GitHub | Manter exige full git access e, quando há network policy, `api.github.com` |

Destinos necessários para a própria Devin funcionar, como o git proxy dos repositórios conectados, são permitidos automaticamente.

## Onde profiles são vinculados

Profiles passam a valer por uma hierarquia. O binding mais específico vence, a menos que um profile mandatory superior imponha um piso:

1. Enterprise default
2. Organization default
3. Automations default
4. Automation específica
5. Sessão individual
6. Security profile do Bot, para sessões iniciadas por aquele Bot

Em cada nível é possível herdar, fixar um profile ou escolher explicitamente nenhum profile. Child sessions seguem a mesma cadeia de governança do parent, então delegar trabalho não escapa das restrições.

Uma sessão em execução resolve seu profile ao bootar ou acordar. Editar um profile ou binding não muda retroativamente uma sessão em execução; afeta novas sessões imediatamente e sessões existentes na próxima retomada.

## Recommended vs mandatory

Comece com **recommended** no rollout. Um profile recommended é um default que níveis inferiores podem substituir ou recusar.

Mude para **mandatory** quando as allowlists forem compreendidas. Profiles mandatory são pisos:

- Escolhas “no profile” em níveis inferiores são ignoradas.
- Profiles inferiores só podem apertar restrições, nunca afrouxar.
- Network e MCP allowlists são intersectadas.
- Git access usa o nível mínimo.
- Devin MCP fica read-only se qualquer lado exigir read-only.
- O token do GitHub CLI é removido se qualquer lado o remover.
- Mesmo aprovações de rede feitas durante a sessão são limitadas pela policy mandatory.

Assim, mandatory é o primitive correto para limites enterprise-wide, e recommended é o primitive correto para rollout por equipe.

## O que Cloud OIDC muda

Sem OIDC, uma sessão que precisa de AWS, GCP, Vault, JFrog, Databricks ou API interna normalmente depende de uma key ou token armazenado. Com OIDC:

1. Cada sessão Devin recebe automaticamente um identity token curto assinado pela Devin.
2. Sua cloud ou serviço verifica o token contra o OIDC issuer público da Devin.
3. O serviço troca o token por credenciais temporárias e escopadas.
4. O token expira automaticamente; não há nada estático para rotacionar ou revogar.

Tokens podem carregar claims como `org_id`, `account_id`, `devin_id`, `devin_trigger`, `requesting_user_id`, `requesting_user_email` e `service_user_id`. Trust policies podem assim conceder acesso a uma organização inteira, a um usuário específico ou até a uma sessão específica.

O issuer é `https://app.devin.ai`, exceto em deployments enterprise com domínio customizado, caso em que o issuer é a URL customizada da Devin.

## Desenhe o modelo de acesso primeiro

Não comece pelo YAML. Comece pelos trust boundaries.

Escreva:

- quais sessões ou automations realmente precisam de acesso cloud
- qual provedor e project/account elas precisam
- se precisam de read-only ou write access
- quais network destinations são legítimos
- quais MCP servers devem usar
- se devem criar child sessions ou gerenciar recursos Devin
- se precisam de acesso direto à API do GitHub além das operações git normais

Depois crie profiles pequenos para tipos reais de trabalho, não um profile gigante para todos.

Profiles iniciais úteis:

| Profile | Uso típico | Postura sugerida |
| --- | --- | --- |
| `research-readonly` | Coleta de evidência, docs, review read-only | Network limitado a docs/repos necessários, git read-only, Devin MCP read-only, sem token `gh` |
| `automation-pr-writer` | CI repair, dependency updates, hygiene loops | Network para APIs de repo/packages, full git, sem MCP irrelevante, `gh` só se necessário |
| `cloud-operator` | Inspeção de infraestrutura ou operações controladas | Network restrito a cloud endpoints, OIDC habilitado, role cloud estritamente escopada, sem MCP amplo |
| `incident-hotfix` | Incident response supervisionado | Uso por tempo limitado, full git, apenas network/MCP do incidente, review humano antes de merge/deploy |

## Construa um primeiro Security Profile

Você precisa da permissão dedicada **Manage security profiles**. Organization admins têm a permissão no nível da organização por padrão; enterprise admins têm no nível enterprise. Ambas podem ser delegadas por custom roles.

1. Vá a **Settings → Customization → Security profiles** para profile de organização, ou **Enterprise settings → Devin → Security profiles** para profile enterprise.
2. Crie um profile com nome estreito, como `automation-pr-writer`, não `default-secure`.
3. Configure apenas as restrições que você entende.
4. Mantenha **recommended** inicialmente.
5. Vincule como organization default ou pin em uma automation de baixo risco.
6. Teste acesso positivo e negativo antes de ampliar o rollout.
7. Aperte com o tempo; mude para mandatory somente depois que destinos e workflows legítimos estiverem cobertos.

### Testes positivos e negativos

Testes positivos provam que o trabalho permitido ainda funciona:

- clone/fetch do repositório pretendido
- instalação do package ou acesso à API pretendida
- uso de um MCP server permitido
- push de branch quando full git é esperado

Testes negativos provam que a fronteira existe:

- um domínio não permitido falha
- um MCP server não permitido fica indisponível
- git read-only não consegue push
- operações write do Devin MCP falham em read-only
- chamadas diretas `gh api` falham quando o token é removido

Registre ambos. “A sessão iniciou” não é verificação de segurança.

## Automations e snapshot builds

Automations podem ter network policy e seleção MCP próprias, mas essas são camadas apenas restritivas. Uma automation nunca pode ampliar o profile governante; sessões recebem apenas o que automation e profile permitem.

Snapshot builds são diferentes: apenas a network policy de um profile se aplica a builds e blueprint author sessions. Restrições de MCP, git access e GitHub CLI não se aplicam. Como builds frequentemente precisam de package registries que sessões não precisam, use a configuração separada **Default profile for snapshot builds** em vez de afrouxar profiles de sessão.

## Aviso sobre Outposts

Em VMs gerenciadas pela Devin, a Devin enforce network policy no nível da máquina. Em Outposts, sua infraestrutura faz o enforcement.

A Devin publica a network policy efetiva de cada sessão enfileirada na Outposts API como `spec.network_policy`. Seu orchestrator deve enforce isso com egress proxy, Kubernetes `NetworkPolicy`, firewall de VM ou controle equivalente. Caso contrário, uma fronteira “mandatory” de rede não é realmente rígida na infraestrutura outpost.

Releia `spec.network_policy` quando a sessão for enfileirada ou reenfileirada; não assuma que é estática.

## Configure Cloud OIDC

Cloud OIDC exige configuração dos dois lados:

- a cloud/serviço deve confiar no issuer da Devin e definir quais token claims podem assumir qual role ou identity
- o environment blueprint da Devin deve instalar a action correspondente

Adicione a action relevante em `initialize`:

| Serviço | Blueprint action |
| --- | --- |
| AWS | `github.com/CognitionAI/actions/setup-aws-oidc@main` |
| GCP | `github.com/CognitionAI/actions/setup-gcp-oidc@main` |
| Vault | `github.com/CognitionAI/actions/setup-vault-oidc@main` |
| JFrog | `github.com/CognitionAI/actions/setup-jfrog-oidc@main` |
| Serviços customizados | `github.com/CognitionAI/actions/setup-devin-oidc@main` |

Exemplo AWS:

```yaml
initialize:
  - uses: github.com/CognitionAI/actions/setup-aws-oidc@main
    with:
      role-arn: "arn:aws:iam::123456789012:role/devin-sessions"
      region: "us-east-1"
```

Exemplo GCP:

```yaml
initialize:
  - uses: github.com/CognitionAI/actions/setup-gcp-oidc@main
    with:
      workload-identity-provider: "projects/123456789/locations/global/workloadIdentityPools/devin/providers/devin-oidc"
      service-account: "devin@my-project.iam.gserviceaccount.com"
      project: "my-project"
```

Para um serviço customizado, solicite um token para a audience aceita pelo serviço:

```bash
devin-oidc token --audience my-api --subject-keys "org_id"
```

Seu serviço verifica o token contra o JWKS publicado pela Devin em `/.well-known/jwks.json` sob o issuer correto.

## Escreva trust policies de menor privilégio

Prefira claims e roles estreitos:

- Use `org_id` para identidade de automation em toda a organização.
- Adicione `requesting_user_email` ou `service_user_id` quando apenas certos iniciadores devem receber acesso.
- Use `devin_id` apenas para acesso one-off ou debugging muito restrito; normalmente é estreito demais para automations reutilizáveis.
- Dê à role assumida apenas as permissões necessárias ao trabalho.
- Separe roles read-only e write-capable em vez de ampliar uma única role.

Cloud audit logs ficam mais úteis com OIDC porque ações podem ser atribuídas a uma sessão Devin e usuário solicitante específicos, em vez de uma key estática compartilhada.

## Verify it

Checks no lado Devin:

- [ ] Uma sessão de teste resolve o profile pretendido.
- [ ] Operações permitidas de network, MCP, git e Devin MCP ainda funcionam.
- [ ] Pelo menos uma operação não permitida em cada categoria configurada falha.
- [ ] Foi confirmado que edição de profile/binding afeta sessões novas ou retomadas, não uma sessão já em execução.
- [ ] Sessões disparadas por automation herdam a interseção esperada das restrições da automation e do profile.

Checks no lado cloud, quando você controla o provedor:

- [ ] `aws sts get-caller-identity` ou comando equivalente funciona sem key armazenada.
- [ ] A identity assumida é a role/service account de menor privilégio pretendida.
- [ ] Cloud audit logs mostram os claims de sessão/usuário Devin esperados.
- [ ] Um token com audience ou trust subject errado é rejeitado.
- [ ] Não há credencial cloud de longa duração em secrets ou ambiente da Devin.

## Armadilhas

- **Tratar profile como scan.** É um envelope de controle de acesso, não detecção de vulnerabilidades.
- **Tornar o primeiro profile mandatory.** Você bloqueará trabalho legítimo antes de entender os destinos necessários.
- **Um profile gigante.** Profiles por tipo de trabalho são auditáveis; um universal vira compromisso sem sentido.
- **Esquecer `api.github.com`.** Sob network policy, um profile não pode manter o token do GitHub CLI sem permitir `api.github.com`.
- **Assumir que sessões em execução atualizam imediatamente.** Elas resolvem profile no boot/wake.
- **Assumir que Outposts se enforce sozinho.** O operador deve enforce `spec.network_policy` fora da infraestrutura gerenciada pela Devin.
- **Usar OIDC sem estreitar trust cloud.** Keyless não significa seguro se a role for ampla ou a trust policy aceitar demais.
- **Deixar keys estáticas antigas.** OIDC só reduz risco de credenciais se as keys estáticas forem removidas ou desativadas.

## Exercícios

1. Escreva uma especificação de profile para uma automation de dependency update. Inclua network destinations, git access, necessidades MCP e se `gh` é necessário.
2. Escreva um teste positivo e um negativo para cada restrição desse profile.
3. Desenhe uma cloud trust policy para acesso read-only a um projeto. Quais token claims são suficientes e quais são estreitos demais?
4. Explique como um mandatory enterprise profile e um organization profile mais restrito se intersectam.

## Capstone

Construa um caminho de automation governado para uma tarefa de manutenção de repo de baixo risco: crie um profile recommended, pin na automation, verifique comportamento positivo/negativo, configure OIDC para uma operação cloud read-only se disponível e documente a evidência exata. Só então proponha se o profile deve virar mandatory.

## Knowledge check

1. Por que Security Profiles e OIDC são complementares, não alternativas? *(Profiles restringem o que uma sessão pode alcançar ou operar; OIDC prova identidade da sessão a um serviço sem armazenar credenciais longas.)*
2. Por que começar com enforcement recommended? *(Ele permite observar necessidades legítimas de acesso e evita bloquear equipes antes das allowlists estarem completas.)*
3. Por que delegação para child sessions não escapa de um profile? *(Children herdam a mesma cadeia governante do parent.)*
4. Por que OIDC melhora auditabilidade? *(Logs cloud podem atribuir ações a claims de sessão, organização e usuário solicitante, em vez de uma key estática compartilhada.)*

## Fontes

- [Security Profiles — documentação oficial](https://docs.devin.ai/product-guides/security-profiles)
- [Cloud Authentication with OIDC — documentação oficial](https://docs.devin.ai/product-guides/oidc)
- [Security Profiles API — referência oficial](https://docs.devin.ai/api-reference/v3/security-profiles/list-organizations-security-profiles)
- [CognitionAI actions repository](https://github.com/CognitionAI/actions)
- [Devin Outposts overview](https://docs.devin.ai/cloud/outposts/overview)

## Changelog

- 2026-11-26 — Versão inicial baseada na documentação oficial. Evidência de reprodução em provedor cloud pendente; os comandos de verificação estão incluídos, mas ainda não foram executados independentemente aqui.
