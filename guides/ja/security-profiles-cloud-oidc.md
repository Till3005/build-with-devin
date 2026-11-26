# ガイド 21 — Security Profiles と Cloud OIDC

**目標：** 2 層で Devin に最小権限アクセスを与える——再利用可能な Security Profiles で session が到達・操作できる範囲を制限し、Cloud OIDC で長期クラウド認証情報を短期 workload identity に置き換える。
**レベル：** 上級 / 管理者 · **時間：** 初回の governed profile に約 45–90 分。クラウド設定は provider に依存
**ソース：** [Security Profiles 公式ドキュメント](https://docs.devin.ai/product-guides/security-profiles) · [Cloud OIDC 公式ドキュメント](https://docs.devin.ai/product-guides/oidc) · 2026-11-26 に公式ドキュメントを確認

> **エビデンス状態：** このガイドは公式ソースに基づきますが、実際のクラウド provider での独立再現はまだです。検証セクションでは、Devin 内でできる確認と、AWS/GCP/Vault/管理者リソースが必要な確認を分けています。

## 2 層のメンタルモデル

Security Profiles と Cloud OIDC は別の問題を解決します。

| 層 | 答える問い | 仕組み |
| --- | --- | --- |
| Security Profile | この Devin session は何に到達し、何を操作できるか | Network allowlist、MCP allowlist、Devin MCP read-only、git access level、GitHub CLI token removal |
| Cloud OIDC | この session はクラウドサービスに対して自分が誰かをどう証明するか | Devin が発行する短期 identity token をクラウドが検証し、一時的で scoped な認証情報に交換 |

両方を併用してください。Profile は session が触れるべきでないシステムへの到達や操作を防ぎ、OIDC は正当なアクセスにクラウドキーを保存しない方法を与えます。

Security Profiles は、脆弱性スキャン製品である **Devin Security** とは別物です。Profile はスキャンを設定しません。

## Security Profile が制限できるもの

Profile は optional restrictions をまとめた名前付きの束です。設定した項目だけを制約します。

| 制限 | 制御対象 | 重要な詳細 |
| --- | --- | --- |
| Network policy | session machine から許可される outbound destinations | hostname は `*` wildcard をサポート。IPv4/IPv6 CIDR も可 |
| MCP access | session が使える installed MCP servers | network policy から独立。許可された MCP servers は自動的に到達可能 |
| Devin MCP access | 組み込み Devin 管理ツールが write 可能か | read-only でも list/inspect は可能だが、session 作成や knowledge 編集などの write は不可 |
| Git access | clone/fetch のみか、full push/PR capability か | read-only は push と PR 作成を防ぐ |
| GitHub CLI token | machine が GitHub API を直接呼べる `gh` token を持つか | 保持には full git access が必要。network policy がある場合は `api.github.com` も必要 |

接続リポジトリ用 git proxy など、Devin の動作に必要な destinations は自動で許可されます。

## Profile の binding 先

Profile は hierarchy 経由で効果を持ちます。上位に mandatory profile が floor を課していない限り、より具体的な binding が勝ちます。

1. Enterprise default
2. Organization default
3. Automations default
4. 個別 automation
5. 個別 session
6. Bot security profile（その Bot が開始する sessions に適用）

各レベルでは inherit、profile pin、または明示的な no profile を選べます。Child sessions は parent と同じ governing chain に従うため、作業を委譲しても制限を逃れられません。

実行中の session は boot または wake のたびに profile を解決します。Profile や binding の編集は、実行中 session を遡って変更しません。新しい session には即時反映され、既存 session には次回 resume 時に反映されます。

## Recommended と mandatory

rollout 初期は **recommended** から始めます。Recommended profile は default であり、下位レベルが別 profile を選んだり opt out したりできます。

Allowlist を理解した後で **mandatory** に切り替えます。Mandatory profile は floor です。

- 下位の “no profile” は無視される。
- 下位 profile は tighten だけでき、loosen できない。
- Network/MCP allowlist は intersection になる。
- Git access は最小レベルになる。
- どちらかが read-only なら Devin MCP は read-only。
- どちらかが GitHub CLI token を削除すれば削除される。
- session 中に承認された network access も mandatory policy で clamp される。

したがって、mandatory は enterprise-wide boundary の primitive、recommended は team-level rollout の primitive です。

## Cloud OIDC が変えるもの

OIDC がない場合、AWS、GCP、Vault、JFrog、Databricks、内部 API にアクセスする session には通常、保存済み key や token が必要です。OIDC では：

1. 各 Devin session が Devin 署名の短期 identity token を自動的に受け取る。
2. クラウドまたはサービスが Devin の公開 OIDC issuer に対して token を検証する。
3. サービスが token を一時的で scoped な認証情報に交換する。
4. token は自動的に期限切れになり、 rotate や revoke すべき静的なものは残らない。

Token には `org_id`、`account_id`、`devin_id`、`devin_trigger`、`requesting_user_id`、`requesting_user_email`、`service_user_id` などの claims を含められます。したがって trust policy は organization 全体、特定 user、さらには特定 session にアクセスを制限できます。

Issuer は通常 `https://app.devin.ai` です。enterprise の custom domain deployment では、その custom Devin URL が issuer です。

## 先に access model を設計する

YAML から始めないでください。trust boundaries から始めます。

次を書き出します。

- どの sessions/automations が cloud access を本当に必要とするか
- どの provider、project/account が必要か
- read-only か write access か
- 正当に必要な network destinations は何か
- 使うべき MCP servers は何か
- child sessions や Devin resources の管理が必要か
- 通常の git operations を超える GitHub API access が必要か

その後、全員向けの巨大な profile ではなく、実際の job type に合わせた小さな profile を作ります。

初期 profile の例：

| Profile | 典型用途 | 推奨 posture |
| --- | --- | --- |
| `research-readonly` | evidence gathering、docs、read-only review | 必要な docs/repos に network を限定、git read-only、Devin MCP read-only、`gh` token なし |
| `automation-pr-writer` | CI repair、dependency updates、hygiene loops | repo/package APIs に network を限定、full git、無関係な MCP なし、必要時のみ `gh` |
| `cloud-operator` | infrastructure inspection または controlled operations | cloud endpoints に network を限定、OIDC 有効、cloud role を厳密化、広い MCP なし |
| `incident-hotfix` | human-supervised incident response | 時間限定、full git、incident 関連の network/MCP のみ、merge/deploy 前に human review |

## 初めての Security Profile を作る

専用の **Manage security profiles** permission が必要です。Organization admins には organization-level permission、enterprise admins には enterprise-level permission が既定であり、custom roles で委譲もできます。

1. Organization profile なら **Settings → Customization → Security profiles**、enterprise profile なら **Enterprise settings → Devin → Security profiles** に移動。
2. `default-secure` ではなく、`automation-pr-writer` のような狭い名前で profile を作成。
3. 理解している制限だけを設定。
4. 最初は **recommended** のままにする。
5. Organization default に bind するか、低リスク automation に pin する。
6. Rollout を広げる前に positive/negative access をテストする。
7. 徐々に tighten し、正当な destinations/workflows をカバーできた後にだけ mandatory へ切り替える。

### Positive/negative tests

Positive tests は許可された作業がまだ動くことを証明します。

- 対象 repo を clone/fetch できる
- 対象 package install または API に到達できる
- 許可された MCP server を使える
- full git が期待される場合 branch を push できる

Negative tests は boundary が存在することを証明します。

- 許可されていない domain が失敗する
- 許可されていない MCP server が使えない
- read-only git が push できない
- read-only mode で Devin MCP write operations が失敗する
- token が削除された状態で直接 `gh api` が失敗する

両方を記録してください。「session が起動した」は security verification ではありません。

## Automations と snapshot builds

Automations は独自の network policy と MCP selection を持てますが、それらは restriction-only layers です。Automation は governing profile を広げられません。session は automation と profile の両方が許可したものだけを得ます。

Snapshot builds は異なります。Profile の network policy だけが builds と blueprint author sessions に適用されます。MCP、git access、GitHub CLI restrictions は適用されません。Builds は sessions が必要としない package registries を必要とすることが多いため、session profiles を緩めるのではなく、別設定の **Default profile for snapshot builds** を使ってください。

## Outposts 警告

Devin-managed VMs では、Devin が machine level で network policy を enforce します。Outposts では、enforce するのはあなたのインフラです。

Devin は queued session の effective network policy を Outposts API に `spec.network_policy` として公開します。Orchestrator は egress proxy、Kubernetes `NetworkPolicy`、VM firewall rules などでそれを enforce しなければなりません。そうでなければ、“mandatory” network boundary は outpost infrastructure 上で hard boundary ではありません。

Session が queued/re-queued されるたびに `spec.network_policy` を再読込してください。固定と仮定しないでください。

## Cloud OIDC を設定する

Cloud OIDC には両側の設定が必要です。

- cloud/service が Devin issuer を信頼し、どの token claims がどの role/identity を assume できるか定義する
- Devin environment blueprint が対応する setup action を install する

関連 action を `initialize` に追加します。

| サービス | Blueprint action |
| --- | --- |
| AWS | `github.com/CognitionAI/actions/setup-aws-oidc@main` |
| GCP | `github.com/CognitionAI/actions/setup-gcp-oidc@main` |
| Vault | `github.com/CognitionAI/actions/setup-vault-oidc@main` |
| JFrog | `github.com/CognitionAI/actions/setup-jfrog-oidc@main` |
| Custom services | `github.com/CognitionAI/actions/setup-devin-oidc@main` |

AWS の例：

```yaml
initialize:
  - uses: github.com/CognitionAI/actions/setup-aws-oidc@main
    with:
      role-arn: "arn:aws:iam::123456789012:role/devin-sessions"
      region: "us-east-1"
```

GCP の例：

```yaml
initialize:
  - uses: github.com/CognitionAI/actions/setup-gcp-oidc@main
    with:
      workload-identity-provider: "projects/123456789/locations/global/workloadIdentityPools/devin/providers/devin-oidc"
      service-account: "devin@my-project.iam.gserviceaccount.com"
      project: "my-project"
```

Custom service では、サービスが受け付ける audience の token を要求します。

```bash
devin-oidc token --audience my-api --subject-keys "org_id"
```

サービスは正しい issuer の下で、Devin が `/.well-known/jwks.json` に公開する JWKS を使って token を検証します。

## 最小権限 trust policies を書く

狭い claims と狭い roles を優先します。

- Organization-wide automation identity には `org_id` を使う。
- 特定 initiator のみに許可する場合は `requesting_user_email` または `service_user_id` を追加する。
- `devin_id` は厳しく限定された one-off/debug access にだけ使う。再利用 automation には通常狭すぎる。
- Assumed role には job に必要な permission だけを与える。
- Read-only と write-capable roles を分け、1 つの role を広げない。

OIDC により、cloud audit logs は shared static key ではなく特定の Devin session/requesting user に帰属させられるため、監査性が向上します。

## Verify it

Devin 側チェック：

- [ ] テスト session が意図した profile を解決する。
- [ ] 許可された network、MCP、git、Devin MCP operations が動く。
- [ ] 設定した各カテゴリで、少なくとも 1 つの disallowed operation が失敗する。
- [ ] Profile/binding 編集が、実行中 session を変えると仮定せず、new/resumed session に影響することを確認した。
- [ ] Automation-triggered sessions が automation/profile restrictions の意図した intersection を継承する。

Cloud 側チェック（provider を管理できる場合）：

- [ ] 保存済み key なしで `aws sts get-caller-identity` または相当コマンドが成功する。
- [ ] Assumed identity が意図した least-privilege role/service account である。
- [ ] Cloud audit logs に期待する Devin session/user identity claims が出る。
- [ ] 誤った audience または trust subject の token が拒否される。
- [ ] Devin secrets または環境に長期 cloud credential がない。

## 落とし穴

- **Profile を scan として扱う。** これは access-control envelope であり、脆弱性検出ではない。
- **最初の profile を mandatory にする。** 必要な destinations を理解する前に正当な作業を止める。
- **巨大な profile を 1 つ作る。** Job-shaped profiles は audit できるが、universal profile は意味のない妥協になる。
- **`api.github.com` を忘れる。** Network policy がある場合、`api.github.com` を許可しなければ profile は GitHub CLI token を保持できない。
- **実行中 session がすぐ更新されると思う。** Profile は boot/wake 時に解決される。
- **Outposts が自動 enforcement すると思う。** Operator が Devin-managed infrastructure の外で `spec.network_policy` を enforce する必要がある。
- **Cloud trust を狭めずに OIDC を使う。** Keyless でも、role が広く trust policy が緩ければ安全ではない。
- **古い static keys を残す。** Static keys を削除または無効化して初めて、OIDC は credential risk を下げる。

## 演習

1. Dependency-update automation の profile specification を書く。Network destinations、git access、MCP needs、`gh` の必要性を含める。
2. その profile の各 restriction について positive/negative test を 1 つずつ書く。
3. 1 プロジェクトへの read-only access 用 cloud trust policy を設計する。どの token claims が十分で、どれが狭すぎるか。
4. Mandatory enterprise profile と、より厳しい organization profile がどう intersect するか説明する。

## Capstone

低リスクな repo maintenance task について governed automation path を作ります。Recommended profile を作り、automation に pin し、positive/negative behavior を検証し、可能なら 1 つの cloud read-only operation に OIDC を設定して、正確な evidence を記録します。これらが完了して初めて、mandatory にするかを提案します。

## Knowledge check

1. Security Profiles と OIDC が代替ではなく補完なのはなぜか。*（Profiles は session が到達・操作できるものを制限し、OIDC は長期認証情報を保存せずに service へ session identity を証明するため。）*
2. Recommended enforcement から始める理由は？*（正当なアクセス需要を観察し、allowlist が揃う前にチームを止めないため。）*
3. Child-session delegation が profile を逃れられない理由は？*（children は parent と同じ governing chain を継承するため。）*
4. OIDC が auditability に有効な理由は？*（cloud logs が shared static key ではなく session、organization、requesting-user claims に帰属するため。）*

## Sources

- [Security Profiles — 公式ドキュメント](https://docs.devin.ai/product-guides/security-profiles)
- [Cloud Authentication with OIDC — 公式ドキュメント](https://docs.devin.ai/product-guides/oidc)
- [Security Profiles API — 公式リファレンス](https://docs.devin.ai/api-reference/v3/security-profiles/list-organizations-security-profiles)
- [CognitionAI actions repository](https://github.com/CognitionAI/actions)
- [Devin Outposts overview](https://docs.devin.ai/cloud/outposts/overview)

## Changelog

- 2026-11-26 — 公式ドキュメントに基づく初版。Cloud-provider reproduction evidence は未整備。検証コマンドは示したが、ここでは独立実行していない。
