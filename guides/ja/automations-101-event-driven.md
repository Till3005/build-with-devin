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

Automations ページ右上の **Create automation** ドロップダウンに 4 つの作成経路：

1. **Create manually** —— 空のエディタ：トリガー → 条件 → アクションを選ぶ
2. **Create from template** —— よくあるワークフロー向けの事前設定済み自動化ギャラリー
3. **Create with Devin** —— 平易な言葉で記述（*"when a CI check fails on my-org/my-repo, have Devin fix it and push to the same branch"*）；セッションが設定を質問し、組み立てた自動化を承認に出す
4. **Ask Devin for suggestions** —— Devin がリポジトリを走査し、作る価値のある自動化を提案

人がハマる注意点：

- Slack トリガーには Devin のチャンネル招待**と** Settings → Connections での個人 Slack 接続の両方が必要
- Teams のプライベートチャンネルは @メンションでのみ発火
- GitHub トリガーは特定リポジトリを指名する必要がある
- 多数運用するなら **Terraform provider** で宣言的管理
- v3 のセッション作成 API は `memory_enabled: false` を受け付ける——起動されたセッション（とその子セッション）はメモリ無効で動く。実行間に学習コンテキストを持ち越したくない automation 向け

## 実録ウォークスルー — automation を実際に作成・発火・検証、Devin Desktop v3.14（Pro プラン）で収録

*Create with Devin* 経路を端から端まで：毎週 changelog スイープを平易に記述 → 設定質問に回答 → 生成された automation を承認 → 手動発火 → 本物のレポートが届くまで。

**動画（5 分、無音、4 倍速）：** Automations ページ → 生成セッション → 承認カード → 手動発火 → レポート。

[![生成セッションのオプションカード — アカウントの既存 automation を既に把握している](https://till3005.github.io/built-with-devin/assets/guides/automations-101-event-driven/walkthrough-poster.webp)](https://till3005.github.io/built-with-devin/assets/guides/automations-101-event-driven/walkthrough.mp4)

![1. Automations ページ — 既存の automation と Create automation ドロップダウン](https://till3005.github.io/built-with-devin/assets/guides/automations-101-event-driven/step1-automations-page.webp)
*1. Automations ページ — 既存の automation と Create automation ドロップダウン*

![2. 4 つの作成経路 — Create manually / from template / with Devin / ask for suggestions](https://till3005.github.io/built-with-devin/assets/guides/automations-101-event-driven/step2-create-options.webp)
*2. 4 つの作成経路 — Create manually / from template / with Devin / ask for suggestions*

![3. 生成セッションは的を絞った質問をする — 既存の automation を既に列挙](https://till3005.github.io/built-with-devin/assets/guides/automations-101-event-driven/step3-generate-options.webp)
*3. 生成セッションは的を絞った質問をする — 既存の automation を把握済み*

![4. すべての作成が承認カードにゲートされる — トリガー・範囲・run-as・ネットワークポリシーを表示](https://till3005.github.io/built-with-devin/assets/guides/automations-101-event-driven/step4-approve-card.webp)
*4. すべての作成が承認カードにゲートされる — トリガー・範囲・run-as・ネットワークポリシーを表示*

![5. Automation 作成完了 — 毎週金曜 10:00（北京時間）、読み取り専用レポート、メール通知](https://till3005.github.io/built-with-devin/assets/guides/automations-101-event-driven/step5-created.webp)
*5. Automation 作成完了 — 毎週金曜 10:00（北京時間）、読み取り専用レポート、メール通知*

![6. 手動発火 — 同じ承認カードのゲート；起動したセッションがサイドバーに現れる](https://till3005.github.io/built-with-devin/assets/guides/automations-101-event-driven/step6-manual-run.webp)
*6. 手動発火 — 同じ承認カードのゲート；起動したセッションがサイドバーに現れる*

![7. 正直なつまずき — 起動セッションの git プロキシ経由 clone が 403 を返した（2 回）；github.com をネットワークポリシーに追加 + 匿名 clone フォールバックで解決](https://till3005.github.io/built-with-devin/assets/guides/automations-101-event-driven/step7-403-fix.webp)
*7. 正直なつまずき — 起動セッションの git プロキシ経由 clone が 2 回 403；修復は github.com をネットワークポリシーに追加 + 匿名 clone フォールバック——automation が起動するセッションはローカル shell の git アクセスを自動では引き継がない*

![8. 検証された出力 — 今週の 103 コミットを分類した本物の changelog、artifact として配信](https://till3005.github.io/built-with-devin/assets/guides/automations-101-event-driven/step8-report.webp)
*8. 検証された出力 — 今週の 103 コミットを分類した本物の changelog、artifact として配信*

## 安全に運用する

- **スケジュールを信用する前に手動実行する。**Automations 一覧で行を右クリックすると、**Run now**、**Open in new tab**、**Copy link** が出る。cron や webhook を放置する前に、無害な payload で **Run now** を一度実行する。次の tick を待たずに同じ action 経路を確かめられる。
- **secret は automation の依存になりうる。**org secret を削除する前、Secrets ページにはその secret を使っている Preflight check を持つ automation が一覧される。先にローテーションまたは再バインドする。先に消すと、設定掃除が障害になる。
- **Preflight はコストゲートであり、正しさの証明ではない。**無関係なイベントを安く弾くには有効だが、preflight が通っても、破壊的な action は明示的レビューの後ろに置く。

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
- [Release notes — 2026-11-23](https://docs.devin.ai/release-notes/overview) — 右クリックの `Run now`；secret 削除時に Preflight 依存を警告
