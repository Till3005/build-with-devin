# ガイド 6 — イベント駆動の自動化

**目標：** 外部イベント——Slack、Teams、GitHub、Linear、Jira、PagerDuty、cron、webhook——を、自分で起動する Devin セッションに配線する。
**レベル：** ここから始める（プラットフォームガイド）· **所要時間：** 約20分
**出典：** [Automations ドキュメント](https://docs.devin.ai/product-guides/automations) · [公式動画ウォークスルー](https://www.youtube.com/watch?v=6xxKtIpgOyE)

## 構造

すべての自動化は 4 部品：

| 部品 | 役割 |
| --- | --- |
| Trigger | 発火させるイベント——Slack メッセージ、失敗した CI 実行、cron の刻み、HTTP webhook |
| Conditions | 任意のフィルター——ラベル `bug` のみ、このリポジトリのみ、`/devin` を含むメッセージのみ |
| Preflight check | 任意の LLM フィルターまたはスクリプト。マッチ*後*・アクション前に走り、イベントをスキップしたり作業項目に分割したりできる |
| Action | 実行内容：セッション開始、既存セッションへのメッセージ、トリアージ監視、メール通知 |

## トリガーカタログ

| ソース | 発火条件 | 定番の用途 |
| --- | --- | --- |
| Slack | 新規メッセージ、リアクション追加、ユーザーグループメンション | `#incidents` のトリアージ；🚨 リアクション → 調査 |
| Microsoft Teams | メッセージ、リアクション | 投稿されたスレッド内でバグ報告に回答 |
| GitHub | issue、issue コメント、PR、PR レビュー、チェック実行、push | 失敗した CI の自動修正；`/devin` コメント → セッション |
| GitLab | MR、MR コメント、issue、push、パイプライン | 失敗したパイプラインの修正 |
| Linear | issue 作成/ラベル/ステータス/優先度/アサイン/移動 | Devin にアサインされたチケットを実装 |
| Jira | issue 作成/更新/ラベル/ステータス/アサイン/コメント | 同上、Jira 形 |
| Pylon | issue 作成/タグ/ステータス | 顧客バグのトリアージ |
| PagerDuty | インシデント発生/確認/解決 | 高緊急度インシデントを発生時に調査 |
| Schedule | cron または一回限り | 日次 Sentry スイープ、週次依存更新、夜間スモークテスト |
| Webhook | 任意の HTTP POST | それ以外全部——Datadog、Sentry、自社システム |

1 つの自動化に複数トリガーを付けると OR 動作——例：GitHub CI 失敗*または* Slack リアクションのどちらでも発火。

## レシピ 1 — 任意の issue で `/devin`

世の中で最も導入されているトリガー：

```text
Trigger:   GitHub → issue comment, repo = your/repo
Condition: comment body starts with "/devin"
Action:    Start session — prompt includes the event payload
```

結果：チームの誰かが issue に `/devin investigate this` とコメントすると、スレッド全文をコンテキストにしたセッションが拾う。

## レシピ 2 — CI 失敗の自己修復

```text
Trigger:   GitHub → check run, repo = your/repo
Condition: conclusion = failure
Action:    Start session: "CI check <name> failed on this commit.
            Diagnose the failure from the logs, fix it, and push to
            the same branch."
```

イベントペイロードが失敗したチェック + コミットをセッションに運ぶ——人間のコピペ不要。

## レシピ 3 — 定期スイープ

```text
Trigger:   Schedule → daily 09:00
Action:    Start session: "Sweep yesterday's Sentry issues in
            <project>. File the top 3 by impact as tickets and
            start the most actionable one."
```

日次の衛生ループ（Sentry スイープ、依存更新、スモークテスト）は最も ROI の高い自動化——「誰かが確認すべき」を「確認済み」に変える。

## アクション種別の選び方

| アクション | 使う場面 |
| --- | --- |
| Start session | デフォルト——各イベントに新しいマシンとコンテキスト |
| Message session | 長寿命セッションが状態を持つ場合——イベントをそこに流し込む（Bot の種） |
| Triage Devin | 常駐 Devin が Slack チャンネル全体を監視し、子調査を生成（インシデントには Devin Oncall 参照） |
| Email notification | 実行したことだけ伝える |

**自動化 vs Bot：** 自動化は無口な管——イベントが入り、セッションが出る。Bot は同じトリガーの周りにメモリ・判断・マルチセッション計画を足す。まず自動化から始め、作業に継続的な遂行が要るようになったら Bot に卒業する（ガイド 2–5）。

## 作り方

Automations ページの 3 つの作成経路：

1. **Create** —— 空のエディタ：トリガー → 条件 → アクションを選ぶ
2. **Template** —— よくあるワークフロー向けの事前設定済み自動化ギャラリー
3. **Generate with Devin** —— 英語で記述（*"when a CI check fails on my-org/my-repo, have Devin fix it and push to the same branch"*）、生成された設定をレビュー

人がハマる注意点：

- Slack トリガーには Devin のチャンネル招待**と** Settings → Connections での個人 Slack 接続の両方が必要
- Teams のプライベートチャンネルは @メンションでのみ発火
- GitHub トリガーは特定リポジトリを指名する必要がある
- 多数運用するなら **Terraform provider** で宣言的管理

## 検証チェックリスト

- [ ] トリガーを手動で一度発火（`/devin test` とコメント、または失敗コミットを push）し、イベントペイロード付きでセッションが始まるのを確認した
- [ ] マッチしないイベント（違うラベル、違うチャンネル）が何も起こさない
- [ ] アクションの出力が期待した場所に着地した（PR、Slack スレッド、チケット）

## 落とし穴

- **ループ。** 出力が自分を再トリガーしうる自動化（Devin が PR にコメント、トリガーが「新規コメント」を監視）はセッションを永久に燃やす。作者、ラベル、イベントサブタイプでゲートする。
- **トリガー嵐。** PR 単位ではなくコミット単位で発火する webhook は、忙しい日に 50 セッションを生む。絞る：生イベント単位ではなく*作業請求単位*に 1 自動化。
- **承認ゲートなし。** トリガーによる自動マージ・自動デプロイは人間の制御点をスキップする——計測された理由がない限り「セッションが PR を開き、人がマージする」形を維持する。

## 理解度チェック

1. 同僚が Devin に「GitHub 通知を全部監視してほしい」と言った——まず何を絞らせるか？*（どのイベントサブタイプが実際に実行可能な仕事を意味するか——ラベル付与、レビュー依頼など——すべての通知ではなく）*
2. なぜマッチしないイベントは「no-op を決めるセッション」ではなく*セッションゼロ*でなければならないか？*（セッションは ACU を消費する；上流でゲートするのは無料、セッション内でゲートするのは有料）*
3. 自動化が Bot を必要とするのはいつか？*（トリガーされた作業が時間をかけて蓄積される判断を要するとき——メモリ、優先度、恒常の成果）*

## 出典

- [Automations — ドキュメント](https://docs.devin.ai/product-guides/automations)
- [Devin Automations QuickStart（動画）](https://www.youtube.com/watch?v=6xxKtIpgOyE)
- 関連：[ガイド 3 — 定期監視 Bot](bots-202-scheduled-sentinel.md) cron の上に Bot の判断を載せる
