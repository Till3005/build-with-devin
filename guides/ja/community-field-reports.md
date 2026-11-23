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

**退屈だが必要なクリーンアップ。** 1 か月の実践レポート：放置リポジトリの整理と、「modernize this」の一言で gulp/webpack 時代のビルド環境を現代構成に刷新（約 1 時間）——地味なキューこそオフロードの価値が最大（[レポート](https://zenn.dev/mei999/articles/7d6132f1ca36b6)）。

**オブザーバビリティへの配線。** [Dynatrace MCP + Devin](https://medium.com/lets-code-future/how-i-turned-devin-into-a-performance-analysis-agent-with-dynatrace-mcp-753d3f4790a2)は Devin をパフォーマンス分析エージェントに変える：ライブ指標とトレースを問い合わせて診断——MCP サーバーがリポジトリにない本番コンテキストを運ぶ（Medium）。素直なチケット→PR ループの全行程は [Devin: バグレポートから PR へ](https://medium.com/@winter.inc/devin-from-bug-report-to-pull-request-25-days-of-ai-day-18-b158daa20f23)も参照。

## 失敗した、記録された事例

- **曖昧または広すぎるプロンプト。** Scott Logic の最初のプロンプトは使えないスキャフォールドを産んだ；スタックと依頼を絞る（「モデルだけ」）ことで修正。Devin は作りすぎる——何を作る*な*かを伝える。
- **規約適合タスク。** 「このエンドポイントにページネーションを追加」がコードベースの規約と不整合で返ってきた事例が独立した 2 レポートにある（[amillionmonkeys](https://www.amillionmonkeys.co.uk/blog/ai-coding-tools-small-studios)、[mohitkhare](https://web.archive.org/web/20260718112612/https://mohitkhare.me/blog/devin-vs-claude-code/)）——規約を運ばない限り Devin は孤立して作る（→ ガイド 9）。
- **グレースフルデグラデーションのエッジ。** [3 エージェント対決](https://dev.to/dextralabs/devin-ai-vs-claude-code-vs-cursor-agent-which-one-actually-ships-production-code-benchmarks-3mi2)の同じレート制限タスクで、Devin の実装はコードベースの規約に合致し Redis スライディングウィンドウも正しかった——しかし Redis 障害パスがフォールスルーではなく未処理 rejection を投げた。人間がエラーパスを読まなければ出荷できなかった。
- **カテゴリごと合わないケース。** [vesslabs](https://zenn.dev/vesslabs/articles/da9593d77369ee) は Pro で 1 週間・10 セッション・3 リポジトリの厳密な評価を行い、意図的に*不採用*を選んだ——Devin が失敗したのではなく、クラウドエージェントの強みが自社と合わなかった：依頼者が全員エンジニア（Slack/Jira の入口がセッション追跡の負担化）、6 人ではセッション共有が不要、iOS シミュレータが Linux サンドボックスで動かない、部位ごとのコスト内訳が取れない。正しい不採用は採用と同じくらい学びがある。
- **検査不能な仕事。** [expectedwrong](https://expectedwrong.com/devin-appraised)と [alanwest の 10 タスク検査](https://dev.to/alanwest/i-gave-devin-10-real-tasks-it-completed-3-3063)が失敗モードを記録：壊れているか存在しない自信満々の出力、ループで燃えるクレジット。彼らのタスクは明確な検証のない仕事に偏っていた——公式プレイブックが必須とするのと同じゲート（ガイド 11）。
- **フリート規模の不透明さ。** 初のフリート規模レポート（[raijuna、Day 1–2](https://www.raijuna.com/blog/devin-100-day-challenge-day-2)）は、シングルセッションユーザーが決して見ない失敗類にぶつかった：約 15 の Bot が動くと*どのセッションがどの PR を出したか*が追えなくなり、Devin 以外のモデルでは数分でコンテキストが失われ、週間クォータの 3 分の 1 がセットアップに消えた——オーケストレーションには独自の税がある。

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
| hubble | 2 つの常設ループ：すべての Dependabot PR を人間が読む前に Devin が調査——GREEN/YELLOW/RED リスクラベル**と根拠をコメントに残す**；週次 Datadog CCM ループがコスト候補を選び、深掘りし、判断可能なレポートを渡す | 人間が PR を開いた時点でレビュー材料が揃っている；届け物はラベルではなく根拠（[Dependabot ループ](https://zenn.dev/hubble/articles/88429bd24db476)、[コストループ](https://zenn.dev/hubble/articles/091e29a0c86ec3)、日本語） |
| SMARTCAMP | 常設セキュリティパイプライン：スケジュール GitHub Actions が ECS イメージを pull → Trivy スキャン（HIGH/CRITICAL）→ issue 起票 → Devin が修復；AWS 認証情報とスキャナージョブを分離し成果物だけが越境；ハッシュ固定 + リリース後 7 日の猶予でスキャナー遅延をガード | 脆弱性対応をセッションではなくパイプラインとして運用（[レポート](https://zenn.dev/smartcamp/articles/97ac804043530e)、日本語） |
| canly | コーダーではなくアナリストとしての Devin：過去約 700 件の問い合わせを分類し、「原因未特定」の正体を解明 | 半数以上はバグではなかった；AI に何を見せるか（DB？ドキュメント？）の選択がモデルより重要だった（[レポート](https://zenn.dev/canly/articles/9c19bb123e208c)、日本語） |
| Ryan Carson（Untangle） | ソロファウンダーが ~15 台の Devin エージェントを同時稼働——ダッシュボードではなくフォルダシステム + 紙の P0 リストで統制；「Watchdog」playbook が全法律事務所アカウントを監視；「LAN PR」スキルがループを閉じる——レビュー、ビデオウォークスルー、自動マージ | 月 ~$20k；QA レビュアーなしで ~40 PR/日をマージ；ローカルエージェントはほぼ卒業（[Lenny's ポッドキャスト](https://www.lennysnewsletter.com/p/i-spent-20000-on-devin-in-a-month)） |

中にある再利用可能なアイデア：**ポリシーテーブルゲーティング**（arufian：低リスク作業だけ自動 PR、複雑なものは計画優先）、**固定出力プロンプト**（Skillnote：固定 CSV 形式 + 変換用インライン Python が出力ばらつきを殺す）、**レビュアー事前消化**（rakko：人間が読む前に Devin が要約 + フラグ）、**根拠ファーストのトリアージ**（hubble：ラベルはポインタ、証拠を載せたコメントが届け物）、**パイプライン型修復**（SMARTCAMP：スキャン → issue → 修復を 1 本の CI 型ループに、認証あり/なしのステージを分離）、**正直な会計**（levtech の ACU 対賃金 ROI 式）。

**組織運営の細目**（Leverages の約 30 人の展開から、同じレポート）：

- 1 つの Slack ワークスペースは**1 つの** Devin 組織にしかバインドできない——Slack 駆動のセッションを計画する前に、他部署が既に紐づけていないか確認する。
- チームごとの ACU クォータ機能はない；API でセッション一覧を取り、Web UI から各セッションの ACU をスクレイピングして集計——強制ではなく可視化で予算管理。
- 静かな ACU 燃焼：デフォルトでは Devin 作成 PR へのコメントごとにセッションが起動。**「Only respond to PR comments that mention Devin」**をオンにし、人間は自由に議論できるようにした。
- リポジトリのオンボーディングは直列——セットアップ中の 1 リポジトリが次をブロックする。スケジュールすること。
- ROI 内訳：高かったのは PR 一次レビュー（`devin-review` ラベル → Actions → API Playbook で 1 回あたり約 1–2 ACU）、定期的なライブラリ更新のリスク評価、*類似の既存 PR* を与えたレガシー作業；低かったのは広範囲リファクタリングと小さすぎるタスク。

## Bots 時代——最初の領収書（2026 年 11 月）

ローンチ後のレポートはまだ薄いが、追う価値がある——3 つとも自己申告で、独立ベンチマークなし：

- **swyx の 1 週間**——Devin Bots の組織に AEO、QA、クロスプラットフォーム移植、個人管理、動画編集を任せ、ローカル worktree から離れた。結論：*「欲しいのは 'AI 従業員' ではなく、アウトカムを所有するエージェントマネージャーだ」*。本人が明記する留保：Cognition 関連、品質指標なし——実践者レポートでありベンチマークではない（[投稿](https://x.com/swyx/status/2122746401482592549)）。
- **raijuna の 100 Days**——自前のエージェントファクトリーの運営者が Bots へ移植。Day 1：約 15 Bot 稼働、セットアップだけで週間クォータの 18%、率直な UX 不満（セッション追跡がフリートにスケールしない）。Day 2：GPT モデルで Bot が数分でコンテキストを喪失（本人の留保：モデルのせいかも）、週の 33% が消えた——現時点で*「オープンソースの自前構築には敵わない」*（[Day 1](https://www.raijuna.com/blog/devin-100-day-challenge-day-1)、[Day 2](https://www.raijuna.com/blog/devin-100-day-challenge-day-2)）。
- **SupaSEO**——これまでで最もクリーンな出荷物：8 Bot の Chief-of-Staff→リード→スペシャリスト チェーンが約 48 時間で有料 SaaS（ローカル SEO + AI 引用追跡、$99）を構築、約 951 commits。人間が書いたのはランディングページのみ。再現可能なコツ：スペシャリスト Bot はプロジェクト横断で共有、プロンプトは細粒度（[ローンチスレッド](https://x.com/noah_z_zhang/status/2124146220159377769)）。

## 抽出された教訓

1. **プロジェクトではなくスライスをスコープする。** 成功はすべて境界のある単位；失敗は「広くこれを作って/直して」。（公式ドクトリン：ガイド 13。）コミュニティ報告のスイートスポット：変更約 ±150–250 行、3–5 ファイル、エージェント作業 ~30 分（[FAL-coffee](https://qiita.com/FAL-coffee/items/be4d59093dd2bb06fb69)）。
2. **検証するか委任しないか。** 機械が「完了」をチェックできる仕事を Devin に——テスト、ビルド、動く `curl`、レンダリングされたページ。
3. **仮定ではなくコンテキストを運ぶ。** 規約、（MCP 経由の）最新ドキュメント、スタックの形——失敗は能力の失敗ではなくコンテキストの失敗。
4. **委任する；見守らない。** すべての好意的レポートの ROI は*非同期性*——あなたが別のことをしている間にタスクが走る。タイピングを見つめるのが「遅い」と判断する方法。
5. **ツールではなくプロンプトを反復する。** Scott Logic の修正は別のエージェントではなく、より狭いプロンプトだった。最初の失敗実行はプロンプトのバグとして扱う。
6. **評決ではなく証拠を届ける。** hubble は Dependabot スキルの最終ステップを「マージ可否を決める」から「リスクを評価する」に書き換えた——エージェントは案件を組み立て、人間が決断を握る。

この 6 つの教訓の背後にある制約は、今や俗説ではなく計測された事実だ：[ハーバードの研究](https://news.ycombinator.com/item?id=50538303)（11/16、HN 459 コメント）は、AI コーディングエージェントが工学のボトルネックを*コードレビュー*へ移したことを示した——このガイドの持続するパターンがすべて、サイレントマージではなくレビューゲート（人間またはスクリプト）で終わる理由である。

## Scott Wu の社内トップ 5（Lenny's インタビューより）

Cognition 自身が最も委任するタスク：**フロントエンド修正、バージョンアップグレード、ドキュメント、インシデント対応、テスト**——加えて「第一防御線」パターン（人間が関わる前に Devin がクラッシュを分析）と、*より良いプロンプトを書く*ための DeepWiki リサーチ。

## 深読み — 何を真似るか、何に気をつけるか

**hubble の Dependabot ループ。** すべての Dependabot PR が Skill ファイルに駆動される Devin セッションを起動：diff、lockfile の差分、リリースノート、CI 状態を読み、GREEN/YELLOW/RED リスクラベル*と証拠一式*をコメント——更新ライブラリと更新タイプ、根拠つきリスク分類、互換性の確認結果、CI 状態、人間が手で確認すべき項目。効く理由：Skill が「ここでリスクとは何か」をファイル化している（どの gem がクリティカルか、CI が緑でも何を確認するか）——レビュアーの頭にだけあった暗黙知が、チーム全員が読んで育てられるファイルになった。最終ステップを「マージ可否を決める」から「リスクを評価する」に意図的に書き換えている。真似る点：まず自分のレビュー手順を Skill として書く——手順が書けないなら自動化も回せない。注意点：ラベルだけでは劣化する；根拠コメントがなければ何も教えてくれない。

**hubble の週次コストループ。** 週 1 回の Datadog CCM パス：Devin がコスト削減候補を 1 つ選び、設定と利用状況を深掘りし、判断可能なレポートを渡す。このループの産物は請求額ではなく*推奨つきの候補*。真似る点：「1 つ選び、掘り、渡す」は常設の衛生キューすべてに一般化できる。注意点：純正ツール（AWS のコスト系）と役割が重なる——コストデータが Datadog にあり、修正にリポジトリの文脈が要るときにだけ勝る。

**SMARTCAMP のスキャン→修復パイプライン。** スケジュール GitHub Actions が ECS イメージを pull → Trivy スキャン（HIGH/CRITICAL、OS パッケージ）→ issue 起票 → Devin が修復。真似る価値があるのは矢印ではなく堅牢化：AWS 認証情報を持つ pull ジョブと無権限のスキャナージョブを分離し成果物だけが越境；リリース後約 7 日待ってから結果を信頼（スキャナーの DB は新パッケージに遅れる）；イメージダイジェストをハッシュ固定し、古いハッシュを検知する PR チェック。注意点：これはスキャナー自体をサプライチェーン攻撃面とみなす多層防御——「スキャン → Devin」だけを真似ると要点を取りこぼす。

**canly のアナリスト導入。** Devin に「原因未特定」で滞留した約 700 件の問い合わせ履歴を分類させた。半数以上はバグではなかった——そしてこの取り組みの真の産物はラベルではなく、AI にまだ足りないコンテキストの地図（ドキュメント、DB 可視性、チケットのメタデータ）だった。真似る点：アナリストとしての Devin は第一級の使い道——ツールを買う前に「誰も分類したことがない山」に向けてみる。注意点：ボトルネックはモデルの質ではなくコンテキストの選び方。

**Tavrn の HIPAA テナント艦隊。** 8 人のエンジニアが HIPAA テナント内（SSO・スコープ権限・監査ログ）で Slack から eng/ops/CS/sales 横断の Devin に指示：6 週間で 1,600 セッション → 1,800+ PR、決定済み PR のマージ率 ~80%、先月のマージコードの 93% が Devin 発。本質は中央値：アラート→調査 35 秒、~90% のアラートがスレッド内で完全調査、ops/CS/sales から eng への質問は ~80% 減——5 件中 4 件は Devin の回答で吸収。真似る点：価値は PR 数ではなく「調査が無料になる」こと——日次 automation が品質判定落ちの案件を再調査し、システム自身の評価が次の仕事を供給する。注意点：「全社の質問を投げる」が成立するのはテナント権限が最初から完璧だから——SSO/スコープ/監査ログを先に固めてから蛇口を開ける。

**Hamming の「Devinable」フレームワーク。** Hamming は「Devin にできるか」ではなく、タスクを Devinable / 非 Devinable に振り分ける：有界・仕様が明確・客観的評価（テスト・チェック・数値）があるものだけが合格。その上でコードベース自体をエージェント向けに最適化：OOP より関数型、無アサーションテストより eval 駆動。結果：Devin が全コード量の 25% を生成し、人間エンジニア 2 人と並ぶトップ貢献者。真似る点：明日から使えるフィルター——派遣前に「有界+仕様+客観評価」を確認。どれか欠けたら、失敗はモデルではなくタスクの形の問題。注意点：エージェント向けコードベース最適化は本物の投資——艦隊規模が見合って初めて回収できる。

**Cognition 自身の通信簿。** 18 ヶ月のパフォーマンスレビューはベンダーとして異例に正直：PR マージ率 34%→67%、脆弱性修正は人間の 20 倍速（30 分→1.5 分/件）、ETL 移行 10 倍、カバレッジは概ね 50–60%→80–90%、自社 webapp コミットの約 1/3 が Devin 作——弱点も名指ししている：曖昧な要件、途中でのスコープ変更、ソフトスキル（悪い計画に異議を唱えない）。真似る点：組織内の期待値設定に使う——Devin の強みは機械的で測定可能、失敗モードは良い brief が防げるものだけ。注意点：強みの数字はすべてベンダー公表——このレビュー自体が、どの数字も引用する前に自艦隊を監査する方法の見本。

**Ryan Carson のワンマン艦隊。** Untangle のソロファウンダーは月 ~$20k で ~15 台の Devin エージェントを同時稼働——統制はダッシュボードではなくフォルダシステム + 紙の P0 リスト。その規模で本当のボトルネックはエージェントのスループットではなく*彼の*注意力だから。運用を支える 2 つの playbook：「Watchdog」が全法律事務所アカウントを監視し一人でカスタマーサクセスを担い、「LAN PR」が ~40 PR/日を締める——レビューループ + ビデオウォークスルー + 自動マージ、QA レビュアーなし。真似る点：スケールの単位は「面ごとの命名済み playbook」であってエージェント数ではない。注意点：ローカルエージェントはほぼ卒業——長いループはクラウド担当。残した例外は Codex での厳密スコープの設計書ビルドだけ。

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
- [hubble — Dependabot の PR を人より先に Devin が調査](https://zenn.dev/hubble/articles/88429bd24db476) · [hubble — Datadog CCM × Devin の週次コスト運用](https://zenn.dev/hubble/articles/091e29a0c86ec3)（日本語）
- [SMARTCAMP — Trivy スキャン → Devin 修復パイプライン](https://zenn.dev/smartcamp/articles/97ac804043530e)（日本語）
- [canly — 約 700 件の問い合わせを Devin で分類](https://zenn.dev/canly/articles/9c19bb123e208c)（日本語）
- [smasato — Devin を最大化する：成功のための Tips](https://zenn.dev/smasato/articles/6aebb0da2f56eb)（日本語）
- [vesslabs — Devin の採用を見送った理由](https://zenn.dev/vesslabs/articles/da9593d77369ee)
- [Dextra — Devin vs Claude Code vs Cursor Agent 対決](https://dev.to/dextralabs/devin-ai-vs-claude-code-vs-cursor-agent-which-one-actually-ships-production-code-benchmarks-3mi2)
- [FAL-coffee — Devin を導入したチームが最初に読む記事](https://qiita.com/FAL-coffee/items/be4d59093dd2bb06fb69)
- [mei999 — Devin を使い倒した：整理・モダナイズ・自動化](https://zenn.dev/mei999/articles/7d6132f1ca36b6)
- [Lenny's Newsletter — Ryan Carson：月 $20,000 を Devin に](https://www.lennysnewsletter.com/p/i-spent-20000-on-devin-in-a-month)
- [HN — ハーバード研究：エージェントはボトルネックをコードレビューへ移した](https://news.ycombinator.com/item?id=50538303)
- [知乎 — AI software engineer 如何接管工作区：Devin、SWE-agent 与 OpenHands](https://zhuanlan.zhihu.com/p/2025994849590026406)（中国語）—— 最も明晰な中国語のアーキテクチャ分析：ACI 設計、サンドボックス vs 開発者同域の 2 路線、3 つの真のボトルネック
- [掘金 — AI 编码 Agent 90 天落地清单](https://juejin.cn/post/7671231304077361203)（中国語）—— 正しい CI ゲート：AI 生成コードに独立したセキュリティスキャン、検出とスキャンを 2 段階に分離、混成スタック運用
- [Cognition — Devin's 2025 Performance Review](https://cognition.com/blog/devin-annual-performance-review-2025) — strengths and named weaknesses, 18 months of internal numbers
- [Tavrn customer story](https://devin.ai/customers/tavrn) · [Hamming customer story](https://devin.ai/customers/hamming) · [Crosby customer story](https://devin.ai/customers/crosby) — fleet telemetry, the "Devinable" task filter, lawyer-in-the-loop triage
- [AI Engineer — Walden Yan: 40× merged PRs on 2.7× engineers](https://aietalks.com/talks/40x-more-merged-prs-with-2-7x-the-engineers) — Cognition's internal software-factory talk
