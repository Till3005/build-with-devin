# ガイド 2 — プロダクトオーナー Bot

**目標：** アプリの一つの領域（サーフェス）全体をプロダクト管理する Bot——自分でチケットを起票し、実装し、マージし、毎日レポートする。
**レベル：** 中級 · **導入後の人間の負荷：** マージ 6 PR あたり約 1 メッセージ
**出典となる導入事例：** Cognition の **Android Bot**——Devin Android アプリを Google Play オープンベータまで **44 日**で出荷：マージ PR 1,134 件、Kotlin 344,651 行、スクリーンショットテスト 2,841 件、チケット 1,217 件。担当者の送信メッセージは**合計 183 件**（22 日間の無発言期間あり）、**PR の 88% が自己マージ**。現在は Android/iOS の機能パリティを所有している。
**出典：** [ローンチ記事](https://devin.ai/blog/introducing-devin-bots) · [Fortune](https://fortune.com/2026/11/17/exclusive-cognition-bets-on-devin-bots-coding-agents-in-challenge-to-anthropics-duet-and-openais-dots/) · Russell Kaplan のドッグフーディング記録

## パターン

一つの Bot が一つの*サーフェス*（アプリ、サイト、サービス）を、PM が所有するように所有する：何を作るか決め、チケットに落とし、チケットごとにセッションを回し、サーフェスを無期限に維持し続ける。人間は報告を受ける役職者として振る舞う。

```text
Bot ──► チケット起票 ──► チケットごとのセッション ──► PR ──► CI + Devin Review ──► マージ
 │                                                                                  │
 └──────────── 日次レポート + Needs-you の判断事項 ◄─────────────────────────────────┘
```

## 前提条件

- Bot が完全に所有できるリポジトリ（CI、レビュー、マージ経路のあるアプリリポジトリ）
- リポジトリで Devin Review が有効、CI チェックが配線済み
- Bot 用の Slack アプリ（推奨——文書化されたすべての導入が Slack に報告している）

## ステップ 1 — 成果プロンプト

Cognition の実際の原文：

```text
your job is to product manage the android app. Basically, you're going to
autonomously create the entire thing, but we need to figure out what the
blockers are for you doing that first.
```

あなたのサーフェス向けに再構成したテンプレート：

```text
Your job is to product manage <surface>. You're going to autonomously
<build / keep parity with <reference>>, but first enumerate the blockers
to you doing that — where the code lives, how to build and test it, and
how changes merge — then start working through them.
```

形に注目：**所有 + 自律性 + ブロッカー優先**。バックログを渡すな；委任状を渡し、必要なものを Bot 自身に洗い出させる。

## ステップ 2 — フェーズ 1：実装ではなく、障害除去

Android Bot は最初にコードを書かなかった——ブロッカーの列挙から始めた：リポジトリアクセス、ビルドコマンド、実機/エミュレータでのテスト方法、マージ経路。あなた版のリスト：

- 自分のマシンでプロジェクトをビルドできるか？（Blueprint/スナップショットの依存関係）
- インストール可能な成果物を作れるか（APK/TestFlight/プレビューデプロイ）？
- マージポリシーを知っているか——どのチェックが必須か、誰がレビューするか？
- 必要なクレデンシャル（ストアキー、署名）を持っているか——あるいは申請手順が文書化されているか？

この監査を終えてから、プロダクトチケットを起票させる。ここで解決したブロッカー一つ一つが、後で見ずに済む停滞セッションになる。

## ステップ 3 — 稼働ループ

障害が取れた後の定常状態：

1. Bot が次に取り組むべき作業単位のチケットを起票
2. 子セッションが実装して PR を開く——小さく、動作の証拠付き
3. CI + Devin Review がマージをゲート
4. Bot がマージ（判断が必要なときは Needs you に届く）
5. 日次レポートが Slack に届く——Android Bot のレポートには変更内容の**画面録画**が含まれる

レポート設定はチャットではなく Bot の Instructions に書く：

```text
Every day, post a report in #<channel>: what shipped, what's in flight,
what needs a human. Include a screen recording of visible changes.
```

## ステップ 4 — 役職者としてのあなたの仕事

44 日間の 183 メッセージは 2 種類に分かれた：

- **判断**——セキュリティレビューの承認、デザインのトレードオフ、承認カード
- **方向付け**——実際にあった例は「もっと野心的に」

それ以外——チケット、実装、修正、自己マージ——はすべて Bot の仕事。実装の質問に答えているなら、あなたは低すぎるレイヤーを管理している。一度修正 → メモリに着地 → 次のセッションが継承。

## 定常状態

初期構築の後、同じ Bot はサーフェスの*所有*フェーズに移る：

- 参照プロジェクトとのパリティ維持（Android Bot は現在 iOS の機能を追跡）
- 届いた報告のトリアージ（Google Play ベータのフィードバックを受け付けている）
- サーフェス横断の退行の捕捉——Android Bot は他者の変更による iOS/web 側の破損を自律的に発見・修正した

## 検証チェックリスト

- [ ] Bot の最初の行動が PR ではなくブロッカー監査だった
- [ ] 言われなくても自分のチケットキューを起票し消化している
- [ ] PR が小さく、証拠（テスト、スクリーンショット、録画）を伴う
- [ ] 日次レポートが可視の証拠付きで Slack に投稿される
- [ ] 1 日中メッセージを送らなくても PR がマージされた日があった

## 落とし穴

- **ブロッカーフェーズの省略。** ビルド/テスト/マージができる前にコーディングを始めたプロダクトオーナー Bot は、孤立した PR を量産する。
- **巨大 PR。** この導入の安全性は小さく検証可能な単位から来ている。PR が膨らんだら指示する：*「1 チケット、1 関心事、1 PR」*
- **方向ではなくコードをレビューする。** 週 30+ PR では全 diff をレビューできない——CI + Devin Review + Bot の証拠でゲートし、メッセージは方向付けに使う。

## 理解度チェック

1. Android Bot は自分の PR の 88% を自己マージした——自己マージを許せるほど安全にしたものは何か？*（検証が存在した：2,841 件のスクリーンショットテストとレビューゲート；「完了」が機械判定可能だから所有が機能した）*
2. セッションを直接プロンプトせず、なぜチケットを起票するのか？*（チケットは Bot が優先度でトリアージする監査可能なキューを作る——人間は 50 のセッションではなく 1 つのキューをレビューする）*
3. 「22 日間の無発言」は制御モデルについて何を示すか？*（例外時のみ報告が機能するのは Bot の「完了」定義が検証可能な場合だけ；沈黙は怠慢ではなく機能そのもの）*

## 出典

- [Introducing Devin Bots](https://devin.ai/blog/introducing-devin-bots) — Android Bot の数値とプロンプト
- [Fortune 独占記事](https://fortune.com/2026/11/17/exclusive-cognition-bets-on-devin-bots-coding-agents-in-challenge-to-anthropics-duet-and-openais-dots/) — 183 メッセージ、88% 自己マージ、ドッグフーディング記録
- 関連：[ガイド 4 — マルチ Bot 組織](bots-203-multi-bot-org.md) 一つのサーフェスが事業になったとき
