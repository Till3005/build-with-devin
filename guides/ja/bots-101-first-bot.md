# ガイド 1 — 初めての Bot

**目標：** 成果（アウトカム）を所有する Devin Bot を作成し、以降のすべてのガイドの基礎となる 6 つの機構を学ぶ。
**レベル：** ここから始める · **所要時間：** 約15分
**出典：** [Bots 公式ドキュメント](https://docs.devin.ai/work-with-devin/bots)、[ローンチ記事](https://devin.ai/blog/introducing-devin-bots)

## Bot とは

セッションは一つのリクエストをこなす。Bot は*成果を所有する*：チャットで目標を一度伝えれば、Bot が作業を計画し、各部分ごとに子 Devin セッションを立ち上げ、監視し、あなたの判断が必要なものだけを持ち込む。永続する——メモリ、セッション、自動化は数週間をまたいで生き続ける。

登場順に並べた 6 つの機構：

| 機構 | 内容 | 操作する場所 |
| --- | --- | --- |
| Chat | Bot が所有するすべて（目標・レポート・質問）を集約する一つのスレッド | Bot のページ / Slack / iMessage |
| Sessions | 各作業が独立した Devin セッションとして専用マシンで実行される | Bot が生成・監視 |
| Needs you | 判断、PR レビュー、権限リクエスト、レポート——一つのリスト | Bot チャットの上部 |
| Memory | Bot が学んだこと。ファイルとして保存され、全セッション開始時に読まれる | Settings → Memory |
| Instructions | 人間が書く恒常ルール。全セッション開始時に読まれる | Settings → General |
| Access | Bot 自身の接続・シークレット、および Bot 間の付与 | Settings → Access |

## ステップ 1 — 作成する

サイドバー → **Bots** → *Create new Bot* → テンプレートを選ぶか *Start from scratch* → 名前を付ける。

新しい Bot は共有するまで自分専用。使用量は通常のセッションと同じくプランにカウントされる。

> ヒント：**Template library**（サイドバー → Bots）には Cognition 製テンプレート——QA Engineer、Migration Engineer、Data Analyst など——と組織内で共有されたものが並ぶ。同じセットは公開 [Bot marketplace](https://devin.ai/bots/templates) で未ログインでも見られる。このリポジトリのガイドでは引き続き *Start from scratch* が正解——成果プロンプトは自分で書く。

テンプレートから作った Bot が得るのはプロンプト**だけ**——非公開で、connections・secrets・memory はゼロ。チャットで管轄（リポジトリ、プロジェクト、チャンネル）を伝え、新規 Bot と同様に connections を配線する。トリガー前提のテンプレートなら、最初の会話で Bot 側が設定を提案してくる。プロンプトは独立コピー——後のテンプレート変更は届かない。（*Add to a current Bot* は新規作成ではなく、既存 Bot にプロンプトを送る。）

## ステップ 2 — 成果を割り当てる

最初のメッセージが Bot が受け取る最も重要な入力である。*タスク*ではなく*目標*を与える：

```text
You own the Android app now. Keep it at feature parity with iOS.
```

これは Cognition の Android Bot が実際に受けたプロンプトの原文。比較してみよう：

| 弱い（タスク） | 強い（成果） |
| --- | --- |
| 「チェックアウトボタンを直して」 | 「チェックアウトはあなたの担当。速く、正確で、テストでカバーされた状態を保て」 |
| 「ドキュメントを更新して」 | 「ドキュメントはあなたの担当。常に `main` と同期させよ」 |
| 「CI を見てて」 | 「`main` のビルド健全性はあなたの担当。チェックが退行したら原因を調べて直せ」 |

タスクは終われば完了するが、成果は Bot に永遠の再計画を促す。

### 限定された最初の任務

「所有権」は正しい*形*だが、最初の実行では*範範囲*を絞る：1つのフロー、1つの環境、1人のレビュアー——あなた。ANO フィールドガイドのパターンが最も確実な出発点：

```text
Own the newsletter signup check for [project] on staging.
Use [repository], [staging URL] and the test mailbox I provide.
Check the journey from submitting the form to receiving the
correct welcome email and opening its resource link.

Start with one run. Show me the result before proposing a schedule.
If you find a defect, reproduce it, make the smallest suitable fix,
and open a pull request with the evidence.

Do not merge, deploy, email real subscribers, change billing,
or connect another service without asking me.

Return: what passed/failed, screenshots or a short recording,
the PR if a fix was needed, anything you could not verify,
and any decision you need from me.
```

重要な行：ジャーニーの定義（フォーム→メール→リンク。「フォームが動く」だけではない）、*スケジュールの前に1回実行*、明示的な merge・deploy 禁止、期待する証拠の指定。Bot が信頼できる証拠を2回返してから、任務を広げる。

## ステップ 3 — 一緒に働く

成果が設定された後、あなたのメッセージの大半はチェックインになる：

```text
anything waiting on me?
```

Bot が何かを報告したら **Needs you**（チャット上部）を開く：

| 項目 | あなたの対応 |
| --- | --- |
| Decision | 選択肢を選ぶ——Bot が推奨案をマークする |
| Review PR / Merge PR | レビューまたはマージ |
| Permission request | 新しいアクセス、自動化、ネットワークホスト、使用量上限の引き上げを承認または拒否 |
| Report / FYI | 読むだけ |

どの項目にも、自分の言葉で返信するか、スヌーズするか、無視するかを選べる。

## ステップ 4 — マイクロ管理ではなくメモリで操る

- **Instructions**（Settings → General）：あなたの恒常ルール——Bot が起動する全セッションの開始時に読まれる。恒久的な方針はチャットではなくここに。
- **Memory**（Settings → Memory）：Bot が自分で書くファイル——好み、修正、プロジェクトの事実。記憶を変えたければチャットで伝えるだけ（「覚えておいて：デプロイは Cloud Run。ベア VM は絶対ダメ」）。Bot を使える全員がメモリを読める——共有 Bot のメモリは共有情報として扱う。

スケールするパターン：Bot を一度修正し、それをメモリに書かせる。以後の全セッションがそれを継承する。Cognition はこのループで週 2,000 件以上の PR をマージしている。

## 共有する前に——アクセスと使用量

ローンチ記事が省略してドキュメントが明記していることが2つある：

- **プライベート Bot はあなたのリソースを黙って引き継ぐ。** あなたが既に持つアクセスは、新しい確認プロンプトなしに grant として記録されうる——プライベート Bot はサンドボックスではない。共有前に Settings → Access を開き、任務に不要な grant を外す。会話や認証情報を見せずに方法だけ真似させたいなら、Bot ではなく*テンプレート*を共有する：Bot のサイドバーメニュー → *Share as template*。名前・一文の説明・秘匿情報を除いたプロンプトを下書きしてくれる——組織の Template library（Teams/Enterprise）か公開リンク（Pro+）で公開。リンクは署名済みテンプレート全体を URL に埋め込む——編集も取り消しもできず誰でもプロンプト全文を読めるので、コピー前に内部名は外すこと。
- **2026年11月20日——Access & Sharing が共有面を更新**（[release notes](https://docs.devin.ai/release-notes/2026)）：段階ロールアウト、エンタープライズは申請制。各セッションに独立した共有設定（自分のみ / ユーザーグループ / 組織）；Manage access がある全箇所——secrets、environments、sessions、automations、plugins、skills、MCP servers、knowledge——でユーザーグループを指定可能。管理者には SCM アクセス不一致レポートと repo sync（GitHub/GitLab のリポジトリをピッカーへ反映）も追加。
- **Bot の使用量 = チャット + 起動した全セッション。** Max：同梱クォータの後オンデマンド——Bot 専用の上限なし。Teams：自分のクォータの後チームクレジット。管理者が Bot 専用のオンデマンド上限を設定可能。Enterprise：別途割当がない限り作成者の上限に計上。チャット内の支出指示は設定済み上限ではない——Settings で設定し、文章で書かない。

## ステップ 5 — 働く場所に置く

- **Slack：** Bot 専用の Slack アプリを与えれば、チームが @メンションや DM を送れる（Settings → Slack）。報告されているすべてのチーム導入がこの形——Bot がチャンネル内の名前付きのチームメイトになる。
- **iMessage：** スマホから Bot にテキストを送る。
- **Web：** サイドバーの Bots セクションに、自分の Bot と共有された Bot が並ぶ。

## ステップ 6 — スケジュールとモード

- **Automations：** チャットで頼む——「開いている PR のサマリーを平日毎朝実行して」——Bot が自動化案を作成し、あなたの一度きりの承認を求める。Settings → Automations で管理（一時停止/再開/削除）。
- **Modes：** Bot には自身のモードに加え、生成するセッション向けの **Child Capability** デフォルトがある（チャットのモード選択で `Normal / Ultra` など）。個別のセッションで別モードを指定することも可能。

## ライフサイクル

| 操作 | 効果 |
| --- | --- |
| Recycle | 現在のセッションを終了；次回オープン時に新しいセッションが始まる。チャットメニューから |
| Archive | 応答を停止し、Bot 一覧から外し、Slack アプリと Bot 間付与を削除（アーカイブ解除してもそれらは復元されない——設定し直す必要がある） |
| Delete | 完全削除：設定、セッション、メモリ、自動化。元に戻せない |

Archive/Delete を見られるのは作成者と Manage Bots 権限を持つロールのみ。Enterprise プランでは `Use Bots` / `Manage Bots` / `Manage Bots across the enterprise` がカスタムロール内の独立した権限。

## 検証チェックリスト

- [ ] Bot を作成・命名し、チャットで成果プロンプトを送信した
- [ ] Bot が二度言われなくても少なくとも一つの子セッションを開始した
- [ ] **Needs you** に判断/PR/権限リクエストが現れ、解決した
- [ ] チャットで与えた修正が Settings → Memory にメモリファイルとして現れた
- [ ] （任意）Slack で @メンションにより Bot と連絡できた

## 落とし穴

- **タスク型プロンプト。** 「X を直せ」は Bot ではなくセッションを生む。Bot が終わって静かになったら、それはタスクだった——所有の形で言い直す。
- **チャットで方針を書く。** チャットに書いたルールは流れて消える；Instructions のルールは毎セッション読まれる。チャット = 指示と回答、Instructions = 法律。
- **Needs you の放置。** Bot は判断をまとめて持ってくる設計——常時監視ではなく、1 日 1〜2 回確認する。

## 理解度チェック

1. 単発セッションにないもので、Bot のセッション間で生き残るものは？*（メモリ——加えて恒常の成果、スケジュール、接続面）*
2. Bot がセッション途中で聞かず "needs-you" に回すのはなぜ？*（判断は一つのスレッドに非同期で集約される；人間はループ内のブロッキング呼び出しではない）*
3. 「賢いセッション」を「従業員」に変える機構は？*（成果の所有——個々のセッションが終わっても目標が残る）*

## 出典

- [AI Native Operators — Devin Bots: give an agent a job to own](https://ainativeoperators.ai/blog/devin-bots-guide) —— コミュニティフィールドガイド；上の限定任務パターンとアクセス/使用量の注意はここから
- 前：[ガイド 18 — Devin への伝え方](talking-to-devin.md)（outcome prompt の根底にある教義）

- [Devin Bots — ドキュメント](https://docs.devin.ai/work-with-devin/bots)
- [Introducing Devin Bots](https://devin.ai/blog/introducing-devin-bots)
- 次：[ガイド 2 — プロダクトオーナー Bot](bots-201-product-owner.md) · 関連：[ガイド 19 — セッションの全ループ](the-session-loop.md)（リサーチ → 委任 → レビュー → 学習）
