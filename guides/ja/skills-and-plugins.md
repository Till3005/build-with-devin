# ガイド 17 — Skills と plugins：playbook の次のパッケージング層

**目標：** 組織の反復手順を `SKILL.md` としてエンコードし、すべてのセッションと Bot が同じ手順で実行するようにする — plugins でリポジトリをまたいで共有する。
**レベル：** 中級 · playbook に取って代わった層
**出典：** [docs.devin.ai/product-guides/skills](https://docs.devin.ai/product-guides/skills) · [release notes](https://docs.devin.ai/release-notes/overview) · [ガイド 9](playbooks-and-knowledge.md) の続編

## なぜ skills が今いちばん重要な層なのか

Playbook は Skills へ移行中です：アカウントは順次移行され、2026-10-24 以降の新規アカウントは Skills のみ — 各 playbook は同じ org/enterprise スコープの skill になります。Skills はオープンな **Agent Skills** 標準に従うため、同じファイルが他のコーディング agent でも動きます。playbook を書く知識はそのまま使えます。変わるのはファイル形式と発見の仕組みだけです。

| 成果物 | 置き場所 | 最適な用途 |
| --- | --- | --- |
| Knowledge | Customize ページ / リポジトリノート | 常駐コンテキスト — Devin が知り得ない事実 |
| Bot instructions | Bot 本体 | 一人の「従業員」への職務規定 |
| Skill | リポジトリの `SKILL.md`、または plugin | 名前付きの呼び出し可能な手順 |
| Rule | Plugin | 常時有効な制約（"never force-push"） |
| Hook | Plugin | ツール呼び出しを巡る決定的な強制 |

## ステップ 1 — skills の置き場所

自動発見されるソースは2つ：

1. **リポジトリ** — `SKILL.md` をコミット。Devin は接続済みの全リポジトリで 10 個のベンダーパスをスキャンします：`.agents/skills/`（推奨）、`.devin/skills/`、`.github/skills/`、`.claude/skills/`、`.cognition/skills/`、`.windsurf/skills/`、`.cursor/skills/`、`.codex/skills/`、`.codeium/skills/`、`.kiro/skills/`。リポジトリの skill はブランチ版管理 — セッション途中の clone も完了時にスキャンされます。
2. **Plugins** — plugin は skills + rules + MCP servers + hooks を束ね、personal・organization・enterprise スコープにインストールできます。同梱の skills はリポジトリの clone 前からコンテキストに入ります。

## ステップ 2 — SKILL.md の契約

```markdown
---
name: test-before-pr
description: Run the dev server and verify pages before any frontend PR.
argument-hint: <environment>
triggers: ["user"]
allowed-tools: read, grep, glob
permissions:
  allow: ["Exec(npm run *)"]
---

## Setup
1. `docker-compose up -d postgres` && `npm run dev`
## Verify
1. Open each page touched by the diff
2. Screenshot at 1280px and 375px
```

挙動を変える frontmatter フィールド：

- **`description`** — セッション開始時に Devin が唯一目にするテキスト。自動呼び出しを左右します。要約ではなくトリガーとして書く（"verify pages before any frontend PR"）。
- **`triggers: ["user"]`** — 自動呼び出しを無効化。破壊的なもの（deploy、migration）は必ずこれ。
- **`argument-hint`** + `$ARGUMENTS`/`$1` — パラメータ化：`@skills:deploy staging`。
- **`allowed-tools` / `permissions`** — skill 有効中のツールを事前承認またはゲート。

## ステップ 3 — 3 つの呼び出し経路

- **自動：** Devin がタスクを `description` と照合し、ヒットすれば skill 本文をコンテキストに読み込み、セッション終了まで保持します。
- **明示：** セッションや Bot メッセージで `@skills:<name> [args]` — チーム横断で手順を共有する確実な方法。
- **提案：** Devin が何かを学んだあと（スタックの起動方法など）、セッションタイムラインに `SKILL.md` の提案と **Create PR** ボタンが出ます — 受け入れましょう。skill ライブラリはこうして書き下ろしなしに育ちます。

## ステップ 4 — ライブラリを育てる

- 新しい skill には並行 2 セッションを当てる — ギャップは数分で出ます。
- セッション中に Devin を訂正したら、その訂正を skill に追記 — 次のセッションはより賢く始まります。
- 単一リポジトリで実証された skill は org plugin に昇格 — コピーなしで全リポジトリに届きます。

## 実録ウォークスルー — リポジトリスキルを実際に起動、Devin CLI v3000.14（swe-2-flash-medium）で収録

ステップ 3 の *明示的* な経路を端から端まで：デモリポジトリに `.devin/skills/coverage-check/SKILL.md` をコミットし、新しいセッションで起動。発見はドキュメント通り——`/` を打つとスキルが名前で列挙され、`description` が補完の説明文になる。

**動画（60 秒、無音）：** SKILL.md → スラッシュ補完 → `Invoked skill coverage-check` → 承認 → レポート。

[![スキルのレポート — app.py と orders.py の関数別カバレッジ表](https://till3005.github.io/built-with-devin/assets/guides/skills-and-plugins/walkthrough-poster.webp)](https://till3005.github.io/built-with-devin/assets/guides/skills-and-plugins/walkthrough.mp4)

![1. ディスク上のスキル — frontmatter の name/description と番号付き手順](https://till3005.github.io/built-with-devin/assets/guides/skills-and-plugins/step1-skill-file.webp)
*1. ディスク上のスキル — `.devin/skills/coverage-check/SKILL.md`：frontmatter `name`/`description` と番号付き手順*

![2. `/` でスキルが列挙される — 名前 + description が補完エントリ](https://till3005.github.io/built-with-devin/assets/guides/skills-and-plugins/step2-slash-autocomplete.webp)
*2. `/` でスキルが列挙される — 発見で読み込まれるのは名前 + `description` そのもの*

![3. `Invoked skill coverage-check` — 最初のコマンドも Allow 待ち](https://till3005.github.io/built-with-devin/assets/guides/skills-and-plugins/step3-invoked.webp)
*3. `Invoked skill coverage-check` — 最初のコマンドにも Allow が必要*

![4. 手順がそのまま実行される — unittest を走らせ、全ソース/テストファイルを読む](https://till3005.github.io/built-with-devin/assets/guides/skills-and-plugins/step4-coverage-report.webp)
*4. 手順がそのまま実行される — `python3 -m unittest -v`、続いて app.py・orders.py・両テストファイルを読む*

![5. 結果：フルカバレッジ — 全ブランチを挙げた関数別表；ファイル無変更、コミットなし](https://till3005.github.io/built-with-devin/assets/guides/skills-and-plugins/step5-full-coverage.webp)
*5. 結果：フルカバレッジ — SKILL.md が要求した通りのレポート*

## plugins と MCP アクセスを治理する

- **Offered と Required は管理者の選択。**組織および enterprise の管理者は marketplace plugin を **Required** ではなく **Offered** にできる。Required は管理基線の一部で、Offered はメンバー任意の追加である。便利パックを Required にしない——全メンバーが継承する管理基線が広がる。
- **MCP 承認は最も狭い範囲で。**MCP ツール承認カードに **Allow for this session** が追加された。同じタスク内では繰り返し必要だが権限はセッションと一緒に消えてほしい場合はこれを優先し、広い承認は監査済みツールだけに残す。
- **API key は secrets に置く。**API-key marketplace MCP server の空 header は secret にバインドされ、未使用 secret はフラグされる。生キーを plugin 設定、プロンプト、チャットに入れない。
- **Automatic は未認証という意味ではない。**新しい custom MCP server は最初から **Automatic** authentication が選択される。本番スコープへ接続する前に、サーバーが実際に何をネゴシエートするか確認する。

## 検証チェックリスト

- [ ] 新しいセッションが skill を名前つきで列挙する（起動時に name + description が読まれる）
- [ ] `@skills:<name>` が手順を逐語実行し、引数が置換される
- [ ] `triggers:["user"]` の skill が自動発火しない
- [ ] plugin 経由の skill がリポジトリ clone 完了前に利用可能

## 落とし穴

- **過剰な規定。** 具体的なコマンド/フラグ/文字列こそが価値。硬直した長文は違います。あらゆる判断を書き尽くした skill は Devin の途中適応力を奪います。
- **本文だけ書いて description を書かない。** 自動呼び出しは description で決まります。本文が良くても description が曖昧なら一度も発火しません。
- **破壊的 skill の自動発火。** deploy と migration は `triggers:["user"]` か明示的な `permissions.ask` の後ろに置きましょう。
- **skill に secret を書く。** skill はスコープ内の全セッションに読まれます — 認証情報は secrets store に入れ `$VAR` で参照。

## 理解度チェック

1. なぜ `description` が skill 本文より重要？*（セッション開始時に読まれる唯一のテキストであり、自動呼び出しを駆動するから。本文は skill が選ばれた後にのみ読まれる。）*
2. 手順をリポジトリ skill ではなく plugin skill にすべき場面は？*（スコープ内の全リポジトリ/セッションが必要とするとき — plugin は clone 前に読み込まれ、ブランチごとのドリフトも起きない。）*
3. 破壊的ステップを含む skill を安全にするには？*（`triggers:["user"]` で明示呼び出しのみにし、危険なツール matcher に `permissions.ask` を付ける。）*

## 出典

- [Devin Skills ドキュメント](https://docs.devin.ai/product-guides/skills) — ファイル形式、発見パス、frontmatter
- [Release notes](https://docs.devin.ai/release-notes/overview) — playbooks→Skills 移行、Customize ページ
- 関連：[ガイド 9 — Playbooks & knowledge](playbooks-and-knowledge.md)（skills の隣にあるコンテキスト層）
- [Release notes — 2026-11-23](https://docs.devin.ai/release-notes/overview) — Offered plugins、セッション単位の MCP 承認、secret にバインドされた API-key header、Automatic auth の既定
