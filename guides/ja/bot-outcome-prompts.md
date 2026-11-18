# Bot 成果プロンプト、解剖

**目標：** 文書化された導入が実際にやったように成果プロンプトを書く——タスクリストではなく領域の所有。
**レベル：** 中級 · **所要時間：** 草案 20 分、調整に 1 週間

大きな数値を出した公開 Bot 導入はすべて、*成果*を割り当てる短いプロンプトから始まった。このガイドは実物を集め、なぜ機能するのかを逆工学する。

## 模範例

> *"your job is to product manage the android app"*

Android Bot の割り当てのすべて。一文が 44 日間の自走的作業を生んだ：Bot は成果を自分で書いたチケットに分解し、チケットごとに Devin セッションを回し、1,134 のマージ PR を出荷した（[ローンチ記事](https://devin.ai/blog/introducing-devin-bots)）。プロンプトに**含まれない**ものに注目：チケットリストなし、受入基準なし、スケジュールなし。成果そのものがそれらすべてを含意する。

## 機能する成果プロンプトの構造

| 要素 | 役割 | 例 |
| --- | --- | --- |
| **役割** | 何を作るかだけでなく、どう*振る舞う*かを伝える | "product manage"、"own the QA of onboarding flows" |
| **境界のある領域** | Bot が全体を見通せるスコープ——アプリ、チェック、データソース | "the android app"、"layout regressions"、"30+ onboarding flows" |
| **暗黙の完了定義** | Bot が自己検証できる状態 | "feature parity with iOS"、"no layout-shift regressions"、"every flow green" |
| **恒常の権限** | Bot が*いつ*と*次に何を*を決める——それがスクリプトではなく Bot たる所以 | "your job is to…"、"keep…"、"watch for…" |

## 公式テンプレートマーケットプレイスのパターン

16 の[マーケットプレイステンプレート](https://devin.ai/bots/templates)はすべて同じ文法に従う。汎化した再利用可能な定式：

**領域の所有** —— "Find bugs, improvements, performance and refactoring work in a named product area; open one small PR at a time with proof it works."（Software Factory）

**チェックの所有** —— "Every 3 hours, build production main, simulate first/repeat/deferred visits, and file fixes with before/after videos for any regression you introduce—or find."（Layout Bot パターン）

**ライフサイクル段階の所有** —— "Take a ticket or an ask to a tested PR and through review."（Product Engineer）

**ケイデンスの所有** —— "Weekly: remove dead code, one safe PR per round."（Code Reaper）——定期成果はトリガーではなくリズムとして述べる。

**チーム代謝の所有** —— "Watch the channels, post updates, hand work to the right teammate, follow up until done."（Chief of Staff）

**衛生の所有** —— "Old flags, stale deps, CVEs — turned into small safe PRs."（Code Health Engineer）

## マルチ Bot 組織：権限を与えるプロンプト

艦隊（SuperJennyStack、Frankie、tigsbot）では、チーフ Bot のプロンプトに*ルーティング契約*が含まれる：どの Bot がどの領域を所有するか、横ではなく上にエスカレートするのはいつか。人間の真のプロンプトは集約仕様：「すべての未決事項を 1 スレッドに持ってこい」。完全な組織図は[ガイド 4](bots-203-multi-bot-org.md)を参照。

## アンチパターン

- **タスク型プロンプト。** 「この 12 issue を直せ」——Bot は終わってアイドルになる；Bot ではなくセッションを得る。
- **検証不能な成果。** 「アプリを良くして」——自己チェックがないと、Bot の唯一の出口は Needs-you スパム。
- **隠れたスコープ。** 成果が Bot に見えないシステム（届かないステージング環境、読めないダッシュボード）を必要とするなら、停滞するか進捗を幻覚する。領域を与えるか成果を縮める。
- **マージ権限の物語なし。** 88% の自己マージ率が存在するのは CI とレビューゲートが自律マージ用に事前設定されていたから。明記する："merge when CI is green and diff < N lines" または "always open as draft for human review"。

## あなたのものを起草——3 行テスト

良い成果プロンプトは順に答える：

1. **あなたのものは何か？** —— 領域
2. **良い状態とは？** —— 検証可能な状態
3. **それに対し何をするか？** —— 恒常の振る舞い

部外者が 2 行目の真偽を外部から判定できないなら、絞り直す。

## 検証チェックリスト

- [ ] リポジトリの実バックログ項目を取り、成果プロンプトに書き直した——領域、検証可能な状態、恒常の振る舞い
- [ ] コードベースを知らない人に見せた：Bot が「勝っている」か外部から判定できるか？
- [ ] Bot の最初の返信が計画かスコープの確認質問であるべき——「最初に何をすればいい？」と聞いたら、プロンプトは所有を割り当てていない

## 落とし穴

- **成果の衣を着たタスクリスト。** 「X、Y、Z を順にやれ」はチェックリストのまま——世界が変わっても Bot は優先順位を付け直せない。
- **「良い」の定義なき「アプリを良く保て」。** 検証可能な状態がなければ Bot が勝手に定義を選ぶ——あなたのものではない。
- **1 領域を超えるスコープ。** 「エンジニアリングを所有せよ」は失敗する；「iOS アプリを所有せよ」は出荷する。外部の一人が完全に観測できる単位で分割する。

## 理解度チェック

1. なぜ "fix Android bugs" より "own the Android app" が良いか？*（所有は恒常の判断を含意する——Bot は直すかどうかだけでなく、どのバグが重要かを決める）*
2. "make the CI fast" の何が悪いか？*（外部から検証不能——閾値がない。"CI under 8 minutes" は検証可能）*
3. "text me if tests fail" は 3 問のどれに答えているか？*（恒常の振る舞い——状態に対し Bot が何をするかは言うが、領域も目標も言わない）*

## 出典

- [Introducing Devin Bots](https://devin.ai/blog/introducing-devin-bots) · [Bots ドキュメント](https://docs.devin.ai/work-with-devin/bots) · [テンプレートマーケットプレイス](https://devin.ai/bots/templates)
- [built-with-devin](https://github.com/Till3005/built-with-devin#documented-deployments) にリンクされた導入レポート
