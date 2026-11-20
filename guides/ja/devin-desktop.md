# ガイド 17 — Devin Desktop

**目標：** エージェントネイティブなエディタ——Devin の全サーフェスを1つのウィンドウに：クラウドセッション、ローカルセッション（Devin Local）、Bots、そして本物の IDE。
**レベル：** 入門
**ソース：** [Desktop changelog](https://docs.devin.ai/desktop/changelog) · [CLI changelog](https://docs.devin.ai/cli/changelog/stable)

## これは何か

Devin Desktop は Windsurf ベースのエディタで、Devin の各サーフェスが並んで存在する。まず3つを区別する：

| サーフェス | 実行場所 | 用途 |
| --- | --- | --- |
| クラウドセッション | Devin のマシン、あなたの組織内 | 無人タスク、並列作業、レビュー待ちの PR |
| Devin Local | あなたのマシンのバックグラウンドプロセス | チェックアウト済み repo を手作業で編集 |
| Bot | 永続エージェント（ガイド 1–5 参照） | 成果を丸ごと任せる——v3.14 から Desktop に搭載 |

## Agent Command Center

Command Center はセッションのハブであり、エディタではない：

- **タブ**（v3.13.4）：1つのウィンドウで複数セッションとページを開け、各タブに独自の戻る/進む履歴——フリートのブラウザと考える。
- **セッションヘッダーの "..." メニュー**：そのセッションの MCP servers——セッションごとに切替え・再認証。
- **Devin Review**：PR ウォークスルー（diff、バグ、テスト録画）が同じウィンドウのページとして開く。

## Devin Local —— daemon 化

v3.13.4（Desktop）/ v3000.13.4（CLI）以降、ローカルセッションは起動したウィンドウではなく**バックグラウンドプロセス**で動く：

- Devin Desktop や CLI を閉じて開き直しても、セッションは**止まらない**。
- 同一セッションは**全クライアントに見える**（`devin ls`、Desktop の一覧）が、アタッチは単一所有：2 番目のクライアントにはロックバナーが出、Force open で最初のクライアントを止めてセッションを引き継ぐ。
- `devin daemon` がプロセスの起動/停止/状態確認を行う。最後のセッションとクライアントが離れて約10分で自動終了する。
- `--process-model` が `daemon` と `in-process` を切替える。`config.json` の `process_model` または `/config` がデフォルト設定。
- `devin ls`、`devin -r`、`/resume` は**セッションモニター**を開く——最終更新順のセッション一覧にステータス・ディレクトリ・メッセージ数付き。

実務上の帰結：ローカル作業が永続化した。長いタスクを始めてノートPCを閉じ、別クライアントから再接続できる——セッションは動き続けている。

## IDE モード

- 埋め込み IDE は **Cmd/Ctrl+S** で手動保存（自動保存は廃止）。未保存タブにはドットが付く。
- Devin Local のブラウザプレビューで**ページ要素やコンソール出力を選ぶと composer に追加される**——バグを説明せず、指し示す。
- Files タブは PDF をプレビュー、CSV/TSV を表として描画、メディアを再生する。

## 真似る価値のあるワークフロー2つ

**1. ローカル → クラウド → ローカル。** Devin Local で作業し、限界に達したら（組織ツールが必要、さらに並列化、ノートPCの稼働時間超過）`/handoff` でクラウドへ。PR をレビューして手元に戻す。daemon で両側とも再開できる。

**2. 1つのウィンドウ、全サーフェス。** Command Center でフリート全体、Local で手元の repo、Bot で見守りたくない成果——3つが同じウィンドウを共有するのは Desktop だけ。

## 実録ウォークスルー — Devin Desktop v3.14.30825 で収録

モックではなく実演：macOS、Pro プラン。Devin Local セッションが使い捨ての `demo-repo` を SWE-2 High で編集し、アプリを閉じても生き残り、CLI と Desktop 間で受け渡しされる。

**動画（91 秒、無音）：** Command Center → タブ → Bots → Devin Local → daemon 実証 → IDE ビュー。

[![SWE-2 High で完了する Devin Local セッション — demo-repo の 2 ファイル変更](https://till3005.github.io/built-with-devin/assets/guides/devin-desktop/walkthrough-poster.webp)](https://till3005.github.io/built-with-devin/assets/guides/devin-desktop/walkthrough.mp4)

![1. Command Center ホーム — 最近のセッション、Your Bots、コンポーザーの Cloud/Local 切替](https://till3005.github.io/built-with-devin/assets/guides/devin-desktop/step1-command-center.webp)
*1. Command Center ホーム — 最近のセッション、Your Bots、コンポーザーの Cloud/Local 切替*

![2. コンポーザーのモデルピッカー — 能力ティアとモデルプレビュー](https://till3005.github.io/built-with-devin/assets/guides/devin-desktop/step2-model-picker.webp)
*2. コンポーザーのモデルピッカー：能力ティア（Fusion → Free）とプレビュー（SWE-2 Lightning/Flash を含む）*

![3. クラウドセッションがタブで開き、右レールに Computer、Files、Changes、Terminal](https://till3005.github.io/built-with-devin/assets/guides/devin-desktop/step3-session-tab.webp)
*3. クラウドセッションがタブで開く — 右レールに Computer、Files、Changes、Terminal*

![4. セッションヘッダーの「…」メニュー — 使用量、アーカイブ、ネットワーク設定、セッションから automation/skill を作成](https://till3005.github.io/built-with-devin/assets/guides/devin-desktop/step4-session-menu.webp)
*4. セッションヘッダーの「…」メニュー；MCP サーバーがあるセッションではここに出る（これには無い）*

![5. Desktop の Bots — Bots ページは開くが、メッセージ送信は Max または Teams が必要](https://till3005.github.io/built-with-devin/assets/guides/devin-desktop/step5-bots-gate.webp)
*5. Desktop の Bots：ページは開くがこのプランでは Bot に送れない —「Bots require Max or Teams」（正直なギャップ）*

![6. Devin Local はコマンド実行前に確認 — 逐条 Allow / Reject](https://till3005.github.io/built-with-devin/assets/guides/devin-desktop/step6-local-approval.webp)
*6. Devin Local はコマンド実行前に確認 — 逐条 Allow / Reject*

![7. SWE-2 High の Local セッション完了 — 2 ファイル変更、クイックレビュー diff 付き](https://till3005.github.io/built-with-devin/assets/guides/devin-desktop/step7-local-done.webp)
*7. SWE-2 High の Local セッション完了 — 2 ファイル変更、クイックレビュー diff 付き*

![8. daemon の実証：Desktop を閉じても `devin ls` に残り、resume で全文転写つき接続](https://till3005.github.io/built-with-devin/assets/guides/devin-desktop/step8-cli-attached.webp)
*8. daemon の実証：Desktop を閉じても `devin ls` に残る — resume で全文転写つき接続*

![9. 2 番目のクライアントにはロックバナー；Force open でセッションを引き継ぎ、先のクライアントは切断](https://till3005.github.io/built-with-devin/assets/guides/devin-desktop/step9-force-open.webp)
*9. 2 クライアントは同居できない：2 番目にはロック表示、Force open で引き継ぎ、先のクライアントは切断*

![10. IDE ビュー：Source Control にセッションの変更一覧；未保存タブはドット表示、Cmd+S で保存](https://till3005.github.io/built-with-devin/assets/guides/devin-desktop/step10-ide-view.webp)
*10. IDE ビュー：同じセッションを包む本物のエディタ — Source Control に変更一覧；未保存タブはドット表示、Cmd+S で保存*

## 検証

- [ ] Devin Local セッションが Desktop を閉じて開き直しても動き続ける
- [ ] `devin ls` に Desktop 発のセッションが見え、`devin -r` で全文転写つき再開できた
- [ ] `devin ls` でセッションモニターが開き、実行中のセッションに join できる
- [ ] Desktop のチャットで作った Bot が同じチャットで返答する

## 落とし穴

- **"Not authorized to use the CLI"** —— Desktop 権限はあるが CLI 権限のないアカウントが Devin Local のサインインで出るエラー（v3.14.30825 で修正済み。見かけたら更新）。
- **タブはウィンドウの状態。** セッションページ内の操作は自分のタブだけに作用——ただし*セッション*は共有なので、別クライアントが接続するとコピーではなく同じ生きたセッションが見える。
- **管理対象マシン：** エンタープライズ管理者はデバイスポリシーで Desktop 設定を制御する（例：言語サーバーの `DetectProxy`）。ネットワークを疑う前に IT に確認。
- **「Archive」対「Mark done」。** Desktop の "..." メニュー（フレーム 4）はまだ *Archive* だが、webapp では *Mark done* に改名（11/16）：セッションは Done フォルダに移るが実行は続き、他の購読者からも見える——サイドバーには購読中のセッションが並ぶので、他人が依存するセッションを「掃除」しないこと。関連：新しい **Phonebook** が各メンバーの Devin/Slack/Teams/git/Jira/Linear の ID を紐付ける。

## 理解度チェック

1. v3.13.4 でローカルセッションは何が変わったか？（バックグラウンドプロセスで動作するようになった——アプリを閉じても止まらず、どのクライアントからも確認・引き継ぎできる。）
2. いつクラウドセッションではなく Devin Local を選ぶか？（ローカルコンテキストでチェックアウト済み repo を直接編集したいとき。規模や組織統合が必要ならクラウドへ。）
3. セッションヘッダーの "..." メニューには何があるか？（そのセッションの MCP servers——セッションごとの切替え・再認証。）

## ソース

- [Devin Desktop changelog](https://docs.devin.ai/desktop/changelog) —— v3.13.4（タブ、バックグラウンドローカルセッション）、v3.14（Desktop 内 Bots、`DetectProxy` ポリシー）
- [Devin リリースノート](https://docs.devin.ai/release-notes/2026) —— 11/16：*Mark done* が Archive を置換、購読サイドバー、Phonebook
- [Devin CLI changelog](https://docs.devin.ai/cli/changelog/stable) —— v3000.13.4：`devin daemon`、`--process-model`、セッションモニター
- 関連：[ガイド 12 — Devin CLI と拡張性](devin-cli.md) · [ガイド 1 — 初めての Bot](bots-101-first-bot.md)
