# ガイド 12 — Devin CLI と拡張性

**目標：** ローカルターミナルの Devin——エージェントをあなたのマシンで実行し、作業を Devin Cloud に渡し、スキル・ルール・プラグイン・フック・サブエージェントで拡張する。
**レベル：** 中級
**出典：** [Devin CLI ドキュメント](https://docs.devin.ai/cli/index.md) — [紹介](https://docs.devin.ai/cli/introducing-devin-cli.md)、[基本コマンド](https://docs.devin.ai/cli/essential-commands.md)、[拡張性](https://docs.devin.ai/cli/extensibility/index.md)

## 概要

Devin CLI はターミナルに住み Devin Cloud に接続するコーディングエージェント。2 つの動作モードがあり、力はその往復にある：

- **ローカル** —— チェックアウト済みのリポジトリをあなたのマシン上で編集
- **クラウド** —— `devin --cloud` でクラウドセッションを作成・操作・再開する。ローカルセッションで `/handoff` を実行すると、タスクを Devin Cloud に引き継げる。CLI で開いたクラウドセッション内で `/handoff` を実行すると、その PR のブランチを取得して切り替え、そのブランチでローカルセッションを開始する（`/open` は Web アプリか Devin Desktop でセッションを開く）。この方法で始めたクラウドセッションは [Local Hands](https://docs.devin.ai/work-with-devin/local-hands) で承認済みコマンド/ファイル操作をあなたのマシン上で実行できる。CLI が接続を持つため、セッションが要求した時に自動で接続される。

```text
ローカルリポジトリ ──/handoff──► Devin Cloud セッション ──/handoff──► ローカルリポジトリ
     ▲                                │
     └──── devin ssh / forward（VM 内を検査）────┘
```

## 重要な部品

| 面 | 役割 |
| --- | --- |
| `devin ssh` / `devin forward` | クラウドセッションの VM へ SSH、ポート転送、`scp` でファイル転送 |
| サブエージェント | 独自プロファイル・権限を持つ独立エージェントへの委任（フォア/バックグラウンド） |
| モデル | 適応ルーティングがタスクごとにモデルを選択；Fusion はフロンティアリード + 安価なサイドキックのペア。SWE-2.1 は CLI/Desktop/Cloud で利用可能。Cognition によれば Desktop/CLI で 2026-12-08 まで無料、2027-01-30 まで割引 |
| ACP | Agent Client Protocol 経由で JetBrains、Zed、Xcode 内で動作 |
| Daemon | v3000.13.4 以降、ローカルセッションはバックグラウンドプロセスで実行——アプリを閉じても止まらず、任意のクライアントから再接続（`devin daemon`、`devin ls` セッションモニター） |

daemon はマルチクライアントの挙動も書き換えた：別のターミナルやエディタで開いているセッションはもはやロックされない——2 つ目のクライアントは*ジョイン*し、どのクライアントにも出力と質問が見える。`devin daemon start|stop|status` がプロセスを管理（最後のセッションとクライアントが離れて約 10 分で自動終了）。`--process-model daemon|in-process` が起動ごとの選択、`config.json` か `/config` の `process_model` が既定値。録画上の例外：Desktop v3.14.30825 では 2 台目の Desktop ウィンドウにロックバナー + *Force open* が出た——ジョインは CLI 側で成立（ガイド 17、フレーム 9）。

## 拡張性スタック

チームが CLI を*自分のもの*にする場所——ガイド 9 と同じ層構造のローカル版：

| 層 | ファイル/機構 | 用途 |
| --- | --- | --- |
| ルール | `AGENTS.md` / ルールファイル | 全セッションが読む常時有効な指示 |
| スキル | `SKILL.md` | 再利用可能な手順——スラッシュ呼出またはエージェントが選択、独自の権限/`allowed-tools` 付き |
| プラグイン | プラグインマニフェスト | スキル + ルール + フック + MCP サーバーのバンドル；**チームマーケットプレイス**で共有 |
| フック | ライフサイクルフック | `PreToolUse`、`PostToolUse`、`SessionStart`、`SessionEnd` などでのシェル/LLM ロジック——ツール呼出をブロック・書換、コンテキスト注入 |
| MCP | MCP 設定 | 外部ツールサーバー（stdio / HTTP / SSE） |

**インポート経路：** `read_config_from` で Cursor、Windsurf、Claude Code、Copilot、Codex、Kiro、OpenCode、Zed の設定を取り込める——移行は書き直しではなくフラグ一つ。

## 真似る価値のある 3 つのワークフロー

**1. ローカル → クラウドへの展開。** タスクはローカルで始め、クラウドが必要になったら `/handoff` で Devin のマシンに引き継ぐ。PR ができたら、CLI でそのクラウドセッションを開くか再開し、そこで `/handoff` を実行して PR のブランチで作業を続ける。

**2. メモリとしてのスキル。** 繰り返す手順（ガイド 11 の移行スキル、緊急修正ランブック、リリースカット）を `SKILL.md` にする——CLI ドキュメントは*成功したセッションの記録*をスキルに還流させて隙間を埋めることを推奨。プラグインがパッケージ化してチーム全体に共有する。

**3. フックによるガードレール。** `rm -rf` パターンをブロックしたりマイグレーションにレビューを強制したりする `PreToolUse` フック——強制は期待されるモデル挙動ではなくフックに住む。

## 実演 —— Devin CLI v3000.14 で録画

モックではなく実際の実行です：Linux 上の Devin CLI `3000.14.30821`、Pro プラン、`app.py` だけの使い捨て `demo-repo`。モデルは編集タスクに `swe-2-flash-high`、スキル実行に `swe-2-high`（`devin models` では SWE-2 の両ティアが **Free** 表示）。

**動画（67 秒・音声なし）：**ログインから handoff のエラーまで、下記のセッション全体。

[![2. プロンプト：subtract 関数とテストを追加。Devin が diff を示して許可を求める —— Allow / Accept edits mode / Bypass mode / Deny](https://till3005.github.io/built-with-devin/assets/guides/devin-cli/walkthrough-poster.webp)](https://till3005.github.io/built-with-devin/assets/guides/devin-cli/walkthrough.mp4)

![1. devin --model swe-2-flash-high —— ログイン確認の後、ディレクトリ信頼の確認](https://till3005.github.io/built-with-devin/assets/guides/devin-cli/step1-login-trust.webp)
*1. devin --model swe-2-flash-high —— ログイン確認の後、ディレクトリ信頼の確認*

![2. プロンプト：subtract 関数とテストを追加。Devin が diff を示して許可を求める —— Allow / Accept edits mode / Bypass mode / Deny](https://till3005.github.io/built-with-devin/assets/guides/devin-cli/step3-permission-prompt.webp)
*2. プロンプト：subtract 関数とテストを追加。Devin が diff を示して許可を求める —— Allow / Accept edits mode / Bypass mode / Deny*

![3. 結果：app.py を編集し test_app.py を作成。pytest が無いため python -c でテストを実行し、その旨を報告](https://till3005.github.io/built-with-devin/assets/guides/devin-cli/step4-task-done.webp)
*3. 結果：app.py を編集し test_app.py を作成。pytest が無いため python -c でテストを実行し、その旨を報告*

![4. /model —— Adaptive、Fusion（リード + サイドキック）、各モデルファミリー。SWE-2 Flash は FREE でクォータ消費なし](https://till3005.github.io/built-with-devin/assets/guides/devin-cli/step5-model-picker.webp)
*4. /model —— Adaptive、Fusion（リード + サイドキック）、各モデルファミリー。SWE-2 Flash は FREE でクォータ消費なし*

![5. /exit で devin -r <slug> の再開ヒントが出る。devin ls はローカルのセッションモニター](https://till3005.github.io/built-with-devin/assets/guides/devin-cli/step6-devin-ls.webp)
*5. /exit で devin -r <slug> の再開ヒントが出る。devin ls はローカルのセッションモニター*

![6. devin --cloud から /list-sessions —— アカウントのクラウドセッションを新しい順に表示](https://till3005.github.io/built-with-devin/assets/guides/devin-cli/step8-cloud-sessions.webp)
*6. devin --cloud から /list-sessions —— アカウントのクラウドセッションを新しい順に表示*

![7. .devin/skills/review/SKILL.md が /review として swe-2-high で動き、未コミットの変更をレビュー](https://till3005.github.io/built-with-devin/assets/guides/devin-cli/step10-skill-result.webp)
*7. .devin/skills/review/SKILL.md が /review として swe-2-high で動き、未コミットの変更をレビュー*

![8. 落とし穴：git remote の無いリポジトリでは /handoff が失敗 ——「Handoff only works from git repos with a remote configured」](https://till3005.github.io/built-with-devin/assets/guides/devin-cli/step11-handoff-no-remote.webp)
*8. 落とし穴：git remote の無いリポジトリでは /handoff が失敗 ——「Handoff only works from git repos with a remote configured」*

手順 7 で使ったスキル（原文）：

```markdown
---
name: review
description: Review recent changes in this repo and report issues
---

Review the working tree's uncommitted changes. List each changed file,
summarize what it does, and flag anything that looks wrong or risky.
Keep it under 10 lines.
```

## 検証チェックリスト

- [ ] `devin` でローカルセッションが動き、`devin --cloud` でクラウドセッションを一覧/作成できる
- [ ] `/handoff` でクラウドに送ったタスクから PR が作成され、そのクラウドセッション内で `/handoff` を実行すると、PR のブランチに切り替わってローカルセッションが始まった
- [ ] スラッシュコマンドで呼んだ `SKILL.md` があなたの手順を実行した
- [ ] （Enterprise）チームマーケットプレイスがあなたのプラグインを別メンバーに配れた

## 落とし穴

- **並列作業にローカルを使う。** CLI はターミナルの 1 エージェント——並列スライスにはクラウドセッションか Bot を使う；CLI は*手を動かす*面。
- **ルールの散乱。** `AGENTS.md` + プロジェクトルール + グローバルルールは優先順位で相互作用——各ルールはちょうど 1 層に置かないと衝突する。
- **`/handoff` には remote が必要。** git remote の無いリポジトリでは即失敗する —— 先に Devin Cloud が clone できる場所へ push しておく。

## 理解度チェック

1. ローカルで終わらせるのでなく `/handoff` で Devin Cloud に渡すのはいつか？*（作業にクラウドスケールの並列性、組織ツール、あるいはラップトップを開いていられる時間を超える長時間実行が要るとき）*
2. スキル・ルール・プラグインの違いは？*（スキルはタスク手順、ルールは恒常コンテキスト、プラグインは両方 + フックを出荷するパッケージ）*
3. なぜフック + サブエージェントがチーム導入で重要か？*（フックは全 CLI セッションで組織ポリシーを強制し、サブエージェントは一人のオペレーターが艦隊を運営できるようにする——逆向きにスケールする 2 つ）*

## 出典

- [Devin CLI ドキュメント](https://docs.devin.ai/cli/index.md) — クイックスタート、コマンド、クラウド連携、拡張性、ACP、モデル
- [Local Hands ドキュメント](https://docs.devin.ai/work-with-devin/local-hands) — CLI/Desktop 経由でクラウドセッションがマシンを使用
- [Introducing SWE-2.1](https://cognition.ai/blog/swe-2-1) — 提供形態とベンダー自報のモデル主張
- 関連：[ガイド 9 — プレイブックとナレッジ](playbooks-and-knowledge.md)（同じ規約層の組織版）
