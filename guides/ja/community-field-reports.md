# ガイド 14 — コミュニティ実践レポート

**目標：** 実際の業務で Devin を運用したエンジニアたちが学んだこと——失敗も含めて。称賛的・批判的双方の公開体験記から抽出。
**レベル：** 判断力を得るならここから
**出典：** 各レポートごとにリンク

このガイドは意図的にバランスを取っている：Devin が確実に勝つ領域、金を燃やす領域、そして二つの結果を分ける働き方。

## すべてのレポートに繰り返されるパターン

成果を出すユーザーは Devin をコード生成器ではなく**非同期のジュニアエンジニア**として扱う。Scott Wu（Cognition CEO）は [Lenny's Newsletter](https://www.lennysnewsletter.com/p/how-devin-replaces-your-junior-engineers) で内部ワークフローを説明している：範囲を絞ったタスクを委任し、会議中に走らせ、PR をレビューする。[Every の記事](https://every.to/chain-of-thought/coding-with-devin-my-new-ai-programming-agent)も同じ枠組みに落ちる——これは*スキルセット*を要する：何が得意かを学び、理解できるタスクを書き、介入すべきときを知り、自分とは違うやり方でされた仕事を信頼することを学ぶ。

## Devin が勝った、記録された事例

**エンドツーエンドのプロトタイピング。** 空のリポジトリから、Devin が FastAPI + React の「City Explorer」（画像/天気/ニュース連携）をスキャフォールドし、ローカルで実行し、PR を開き、公開 URL にデプロイ——約 90 分、人間の介入約 2 回（[Medium 体験記](https://medium.com/@sambhavgaur_70582/copilot-cursor-or-devin-my-hands-on-weekend-with-ai-that-codes-and-deploys-acc708e802b3)）。[Scott Logic](https://blog.scottlogic.com/2025/10/20/rapid-development-with-devin.html) は実際のクライアントプロトタイプで同じ弧を報告——下記に重要な反復の教訓。

**ランタイムが要る仕事。** [Claude Code との直接対決](https://web.archive.org/web/20260718112612/https://mohitkhare.me/blog/devin-vs-claude-code/)で、Devin は規約に合わせるタスクでは負けたが、マシンが活きる領域では明確に勝った：メモリリーク狩りでプロファイリング、負荷下でのヒープスナップショット、レポート生成——エージェント自身の VM が機能。

**ライブトラブルシューティング。** [Faros](https://www.faros.ai/blog/how-to-use-devin-ai-troubleshooting) は*顧客電話中に* Devin を使用：イントロスペクション API のコードを読み、動作する `curl` を数秒で生成——1〜2 日のフォローアップループを通話内に圧縮。

**最新ドキュメントを伴う実際の移行。** 厄介な Vue→React コードベースでの Tailwind 3→4 + DaisyUI 4→5 アップグレードは、チームが Context7 MCP 経由で最新ドキュメントを供給したとき機能した——プロンプトはタスクだけでなく*コンテキスト*を運んだ（[Bootcamp 記事](https://medium.com/design-bootcamp/day-7-of-30-getting-to-know-devon-ai-and-working-with-him-743c351cd0c4)）。

**自己検証。** [1 年間の実践者比較](https://architecttocto.substack.com/p/the-only-coding-agent-worth-paying)は Devin のブラウザ駆動 e2e テストを閾値の瞬間と評する：作ったものに自分で遷移して確認する——生成ではなくエンジニアリングに似たフィードバックループ。

**コードを超えて。** Cognition の研究者は、9 年前に学期の大半を費やした Lean 形式化を Devin が再構築し——完成させたと報告。**15 分以内**で（[投稿](https://x.com/penlume/status/2115806616796921885)）。数学の形式化は移行と同じ特性を報酬とする：機械チェック可能な完了定義。

**オブザーバビリティへの配線。** [Dynatrace MCP + Devin](https://medium.com/lets-code-future/how-i-turned-devin-into-a-performance-analysis-agent-with-dynatrace-mcp-753d3f4790a2)は Devin をパフォーマンス分析エージェントに変える：ライブ指標とトレースを問い合わせて診断——MCP サーバーがリポジトリにない本番コンテキストを運ぶ（Medium）。素直なチケット→PR ループの全行程は [Devin: バグレポートから PR へ](https://medium.com/@winter.inc/devin-from-bug-report-to-pull-request-25-days-of-ai-day-18-b158daa20f23)も参照。

## 失敗した、記録された事例

- **曖昧または広すぎるプロンプト。** Scott Logic の最初のプロンプトは使えないスキャフォールドを産んだ；スタックと依頼を絞る（「モデルだけ」）ことで修正。Devin は作りすぎる——何を作る*な*かを伝える。
- **規約適合タスク。** 「このエンドポイントにページネーションを追加」がコードベースの規約と不整合で返ってきた事例が独立した 2 レポートにある（[amillionmonkeys](https://www.amillionmonkeys.co.uk/blog/ai-coding-tools-small-studios)、[mohitkhare](https://web.archive.org/web/20260718112612/https://mohitkhare.me/blog/devin-vs-claude-code/)）——規約を運ばない限り Devin は孤立して作る（→ ガイド 9）。
- **検査不能な仕事。** [expectedwrong](https://expectedwrong.com/devin-appraised)と [alanwest の 10 タスク検査](https://dev.to/alanwest/i-gave-devin-10-real-tasks-it-completed-3-3063)が失敗モードを記録：壊れているか存在しない自信満々の出力、ループで燃えるクレジット。彼らのタスクは明確な検証のない仕事に偏っていた——公式プレイブックが必須とするのと同じゲート（ガイド 11）。

## 名付けられたチーム導入（コミュニティ、数値つき）

Devin の運用データを公開している実組織——異常に記録の良い日本のエンジニアリングコミュニティからが多い：

| チーム | 導入 | 報告された結果 |
| --- | --- | --- |
| rakko_inc | Playbooks + GitHub Actions + Devin API による Devin 自動コードレビュー——人間のレビュー前に全 PR を事前消化 | **月間レビュー PR 65 → 184 件（2.8 倍）**；人間は Devin の要約から開始（[レポート](https://zenn.dev/rakko_inc/articles/00cc5a5a679971)、日本語） |
| Skillnote（QA） | PR → Actions → Devin がテスト設計ドラフト（CSV/Excel、「なぜこのケースか」含む）を生成し PR に投稿 | **10 テストケースあたり約 35 分節約**；Devin 設計ケースが人間が見逃したバグを捕捉（[レポート](https://zenn.dev/skillnote/articles/5ba429ca249801)、日本語） |
| arufian | サーバーレスの GitHub イベント自動化（常駐サーバーなし）：`devin:fix`/`devin:plan` ラベルが Devin セッションを駆動、**優先度 × 複雑度ポリシーテーブル**と計画優先承認フロー | 安全スキャンがリスキーな PR をゲート；高複雑度の仕事は計画 → 人間承認 → `run that plan`（[レポート](https://zenn.dev/arufian/articles/f80a62f5217cee)、日本語） |
| Leverages（levtech） | 組織展開：14 チーム / 約30人 | 約2.5か月で**177 マージ PR**；ROI を `ACU コスト − 節約時間 × 賃金` で計測しタスク種別の構成も追跡（[レポート](https://zenn.dev/levtech/articles/9c869303820844)、日本語） |
| Decagon | Devin Cloud 上の AutoResearch：1 体のオーケストレーター Devin + 仮説を競わせる並列サブエージェント；すべてのアイデアを Modal GPU 上で再生した本番トラフィックに対して検証 | サポートトラフィックで**GPU あたり最大 2.5 倍のスループット**（[記事](https://x.com/DecagonAI/article/2115511110120120437)） |
| Nader Dabit | 個人 5 Bot 組織——**CTO**（全セッション/リポジトリ、iMessage VIP）、**Auto(mation)Bot**（自動化の運行、性能レポート）、**DevCommunityBot**（アンバサダープログラムのデータ → ミニアプリ）、**DevRelBot**（ドキュメント + *自分専用のコンピュータ、専用 Devin/GitHub/Linear アカウント、ElevenLabs 音声クローン*で作るチュートリアル動画） | 加えて **Windfable**：Unity iOS RPG のための約 10 の SuperJennyStack Bot、それぞれ専用 macOS+Xcode+Unity 持ち、iPhone Duo の折り畳み/展開両モードをスクリーンショット/動画差分でテスト（[入門](https://x.com/dabit3/status/2122755275182469515)） |
| Mark Fenner | 調整役 Chief Agent Bot（"Frankie"）の下で職務別 4 Bot を運営する一人オペレーター | 1 つの決裁面に集約された更新——チームなしでもマルチ Bot 組織形が機能（[ウォークスルー](https://x.com/markfenner/status/2122740244328145211)） |

中にある再利用可能なアイデア：**ポリシーテーブルゲーティング**（arufian：低リスク作業だけ自動 PR、複雑なものは計画優先）、**固定出力プロンプト**（Skillnote：固定 CSV 形式 + 変換用インライン Python が出力ばらつきを殺す）、**レビュアー事前消化**（rakko：人間が読む前に Devin が要約 + フラグ）、**正直な会計**（levtech の ACU 対賃金 ROI 式）。

## 抽出された教訓

1. **プロジェクトではなくスライスをスコープする。** 成功はすべて境界のある単位；失敗は「広くこれを作って/直して」。（公式ドクトリン：ガイド 13。）
2. **検証するか委任しないか。** 機械が「完了」をチェックできる仕事を Devin に——テスト、ビルド、動く `curl`、レンダリングされたページ。
3. **仮定ではなくコンテキストを運ぶ。** 規約、（MCP 経由の）最新ドキュメント、スタックの形——失敗は能力の失敗ではなくコンテキストの失敗。
4. **委任する；見守らない。** すべての好意的レポートの ROI は*非同期性*——あなたが別のことをしている間にタスクが走る。タイピングを見つめるのが「遅い」と判断する方法。
5. **ツールではなくプロンプトを反復する。** Scott Logic の修正は別のエージェントではなく、より狭いプロンプトだった。最初の失敗実行はプロンプトのバグとして扱う。

## Scott Wu の社内トップ 5（Lenny's インタビューより）

Cognition 自身が最も委任するタスク：**フロントエンド修正、バージョンアップグレード、ドキュメント、インシデント対応、テスト**——加えて「第一防御線」パターン（人間が関わる前に Devin がクラッシュを分析）と、*より良いプロンプトを書く*ための DeepWiki リサーチ。

## 検証チェックリスト

- [ ] 自スタックに最も近いレポートを 1 つ選び、蒸留版ではなく原文を読み直した——数値は文脈の中でも成立するか？
- [ ] 自組織で再現できると金を賭けられる教訓を 1 つ書き下した；名付けられなければ別のレポートを選ぶ

## 落とし穴

- **生存者バイアス。** 称賛レポートは数値を公開し；静かな失敗は何も公開しない。このコレクションの失敗を中央値の体験、勝利を天井として読む。
- **カーゴカルト。** Scott Logic のプロンプト反復が機能したのは*反復したから*——ループなしで最終プロンプトを真似ても、彼らの結果ではなく開始点が手に入る。

## 理解度チェック

1. 失敗レポートに共通し成功レポートに欠けているものは？*（検証不能な委任——失敗は「完了」を誰もチェックできない仕事を Devin に与えた；すべての成功がチェックを定義していた）*
2. Faros の「顧客電話中のデバッグ」が逸話でなく導入の教訓なのはなぜ？*（ライブトリアージの動作を示す：人間が顧客関係を保つ間にエージェントが第一応答者になる）*
3. なぜこのガイドは敵対的レポートを同等の出典として数えるのか？*（敵対的レポートは境界条件を明らかにする——地図の端は、その外に歩み出た人から学ぶ）*

## 出典

- [Scott Logic — Rapid development with Devin](https://blog.scottlogic.com/2025/10/20/rapid-development-with-devin.html)
- [Lenny's Newsletter — Scott Wu on Cognition's internal Devin usage](https://www.lennysnewsletter.com/p/how-devin-replaces-your-junior-engineers)
- [Every — Coding with Devin](https://every.to/chain-of-thought/coding-with-devin-my-new-ai-programming-agent)
- [dev>notes — Devin vs Claude Code](https://web.archive.org/web/20260718112612/https://mohitkhare.me/blog/devin-vs-claude-code/)
- [Faros — Devin for live troubleshooting](https://www.faros.ai/blog/how-to-use-devin-ai-troubleshooting)
- [Medium — Copilot, Cursor or Devin weekend](https://medium.com/@sambhavgaur_70582/copilot-cursor-or-devin-my-hands-on-weekend-with-ai-that-codes-and-deploys-acc708e802b3)
- [Bootcamp — Day 7 with Devin（Tailwind/DaisyUI 移行）](https://medium.com/design-bootcamp/day-7-of-30-getting-to-know-devon-ai-and-working-with-him-743c351cd0c4)
- [architect to CTO — The only coding agent worth paying for](https://architecttocto.substack.com/p/the-only-coding-agent-worth-paying)
- [expectedwrong — Devin, appraised](https://expectedwrong.com/devin-appraised) · [dev.to — 10 real tasks, 3 completed](https://dev.to/alanwest/i-gave-devin-10-real-tasks-it-completed-3-3063) · [amillionmonkeys](https://www.amillionmonkeys.co.uk/blog/ai-coding-tools-small-studios)
- [Signadot — Testing Devin's changes end to end](https://dev.to/signadot/test-devins-changes-end-to-end-with-signadot-a0)
