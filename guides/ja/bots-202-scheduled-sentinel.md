# ガイド 3 — 定期監視 Bot

**目標：** 定期的な品質チェックを所有する Bot——スケジュールで実行し、失敗をトリアージし、原因まで追跡し、修正を出荷する。
**レベル：** 中級
**出典となる導入事例：** Cognition の **Layout Bot**——Devin web アプリのレイアウトシフト退行を監視。3 時間ごとに本番 `main` をビルドし、初回/再訪/遅延リクエストの訪問をシミュレートして修正を出荷する。**3 週間で 159 PR；ラグ −70%。** 野生では同じ形が最大規模で動いている：Grant Sanderson の **Manim メンテナー Bot** が 3Blue1Brown を支えるオープンソースエンジンの issue 事前トリアージを担当——**96.6k stars、月 25 万ダウンロード**分の保守が、メンテナの目に届く前に処理される。
**出典：** [ローンチ記事](https://devin.ai/blog/introducing-devin-bots) · [Automations ドキュメント](https://docs.devin.ai/product-guides/automations)

## パターン

「終わることのない」仕事がある——時計の上で再発する：パフォーマンス予算、視覚退行、依存関係の鮮度、シークレットスキャン、稼働率。監視 Bot は修正だけでなく*チェック自体*を所有する：コードベースの変化に合わせてチェックを維持し、ノイズを除去し、退行が本物のときだけ修正を開く。

```text
cron ──► Bot 起床 ──► 現実に近い条件でチェック実行
                              │
                  pass ───────┴──────── fail
                   │                      │
                  静寂              フレーク除外のため再実行
                                          │
                                導入した PR まで追跡
                                          │
                            修正 PR + 前後の証拠
```

## 前提条件

- Bot のマシン上で実行できるチェック（ビルド、テストスイート、Lighthouse、自作スクリプト）
- Devin Bot（ガイド 1）または Automation（ガイド 6）——どちらでも動く；Bot は実行と実行の間に判断を挟める

## ステップ 1 — 成果プロンプト

Layout Bot の文書化された挙動から再構成：

```text
Your job is to keep <surface> from <regressing>.

Watch <check/channel>, where <the check> posts every <interval>. Take over
that check and keep it working as the code changes. When something
regresses: rerun to rule out flakiness, trace the regression to the PR
that introduced it, and open a fix PR with before/after evidence.
```

`<check>` に入る実例（すべて実際の導入で観測）：

- 初回/再訪/個別遅延リクエストにまたがるレイアウトシフト計測（Layout Bot）
- 最も遅い 5 エンドポイントの p95 レイテンシ（Latency Optimizer テンプレート）
- `npm audit`/CVE スイープ（Code Health Engineer テンプレート）
- デッドコード検出（Code Reaper テンプレート）

## ステップ 2 — スケジュール設定

チャットで Bot に頼む：

```text
Run this check every 3 hours on a schedule.
```

Bot が自動化案を作成し、あなたは一度承認する（cron を自分で配線したい場合はガイド 6 の手動自動化を参照）。以後は Bot の Settings → Automations で管理。

## ステップ 3 — 現実に近い条件が重要

Layout Bot のチェックは一発の実行ではない——**初回訪問、再訪問、個別遅延リクエスト**をシミュレートする。狩っている退行が特定の負荷形状でしか現れないからだ。あなた版の等価物を定義する：

- どの環境か——Bot は dev サーバーではなく自分の VM で本番 `main` をビルドする
- どの入力か——コールド vs ウォームキャッシュ、シードデータ、現実的なリクエスト順序
- どの閾値か——「なんか遅い」ではなく数値

## ステップ 4 — ノイズ規律

監視 Bot が狼少年にならないための 2 ルール：

1. **行動前に再実行**——Layout Bot はフレークらしき結果を本物として扱う前に再実行する。プロンプトに書き込む：*"rerun any failed check once before acting on it."*
2. **修正前に追跡**——各退行は導入した PR まで追跡される。原因のない修正は推測である。

## ステップ 5 — すべての修正に証拠を

159 の PR それぞれが**前後の動画**を持つ。あなたのチェックでの等価物：

| チェック | 修正 PR に入れる証拠 |
| --- | --- |
| レイアウト/視覚 | 画面録画またはスクリーンショット、前後比較 |
| レイテンシ | タイミング数値、同じ計測方法で |
| デッドコード | そのコードに到達しない理由 |
| 依存関係/CVE | アドバイザリ + それを解決する diff |

## 検証チェックリスト

- [ ] 自動化が存在し、設定した cron で発火する（Settings → Automations に実行履歴）
- [ ] 仕込んだ退行が前後証拠付きの修正 PR を生成した
- [ ] フレークな実行が修正ではなく再実行を生成した
- [ ] チェック自体がメンテされる——アプリが変わったとき Bot がチェックを更新した

## 落とし穴

- **修正は所有するがチェックは所有しない。** チェックが壊れて 1 週間誰も気づかないなら、Bot は間違ったものを所有していた——プロンプトはチェック自体を割り当てる必要がある。
- **判断なしの cron。** 素のスケジュール自動化はチェックを実行できるが、失敗が本物かの判断は Bot がする。トリアージ不要のチェックにだけ素の自動化を使う（ガイド 6）。
- **アラートだけの出力。** チャンネルに「退行を検出」と報告するだけの監視は人間に仕事を作る。この導入の価値は*修正する*こと——それを基準に据える。

## 理解度チェック

1. なぜ監視 Bot は失敗報告を待たず cron で本番 `main` をビルドするのか？*（成果は「報告されたバグを直す」ではなく「退行がない」——所有とは人間より先に問題を見つけること）*
2. Layout Bot が前後動画付きで修正を出す——レビュアーにどんな判断を可能にするか？*（ローカル再現なしのマージ確信；証拠が PR と共に移動する）*
3. 症状を直すのでなく導入 PR まで退行を追跡する理由は？*（チェックの所有は履歴の所有を含む——修正が原因に着地し、知識が残る）*

## 出典

- [Introducing Devin Bots](https://devin.ai/blog/introducing-devin-bots) — Layout Bot の機構と数値
- [Automations — ドキュメント](https://docs.devin.ai/product-guides/automations) — スケジュール、トリガー、条件
- 関連：[ガイド 6 — イベント駆動の自動化](automations-101-event-driven.md) Bot なし版のこのループ
