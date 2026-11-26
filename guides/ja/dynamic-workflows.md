# ガイド 20 — Dynamic Workflows

**目標：** 決定的な Python スクリプトで複数の Devin sessions をオーケストレーションする——独立した作業をファンアウトし、構造化結果を後段に渡し、中断した run を再開し、ACU コストを常に把握する。
**レベル：** 上級 · **時間：** 初回 run の設計に約 35 分。実コストは agent 数に依存
**ソース：** [Dynamic Workflows 公式ドキュメント](https://docs.devin.ai/work-with-devin/dynamic-workflows) · 2026-11-26 に公式ドキュメントを確認

> **エビデンス状態：** これは公式ソースに基づく運用ガイドであり、まだ独立した再現実験ではありません。実際の workflow は複数の Devin sessions を起動し、大きな ACU を消費する可能性があるため、以下の再現演習は意図的に小さく限定し、承認制にしています。

## いつ使うか

作業そのものに構造がある場合に dynamic workflow を使います。

- **広いファンアウト + 統合ステップ**——おおよそ 5 つ以上の独立したファイル、モジュール、エンドポイント、チケット、候補があり、それぞれ判断や検証が必要で、最後にマージ、重複排除、推奨を行う。
- **段階的パイプライン**——後段が前段の構造化出力を消費する。例：*audit → fix → verify*。
- **制御されたループ**——測定可能な停止条件を満たすまで run/fix/check を繰り返す。

次の場合は使わないでください。

- codemod、linter autofix、ジェネレーター、shell loop で機械的に実行できる。
- 独立した session が 1〜2 個だけで、データの受け渡しもない。
- 共有状態で強く結合している、または小さく順次的な作業である。

Workflow は「AI を増やす」ものではありません。オーケストレーションをコード化するものです。どの agent を、どの順序で、どの prompt で実行し、どの構造化データを次へ渡すかをスクリプトが決めます。

## メンタルモデル

```text
あなたが成果を記述する
        ↓
Devin が workflow.py を書く
        ↓
スクリプトが prompt + JSON Schema で agent(...) を呼ぶ
        ↓
各 agent が構造化出力を返す
        ↓
後段の prompt が前段の出力から組み立てられる
        ↓
run が記録され、再開できる
```

Workflow がバックグラウンドで実行されている間も、オーケストレーション側の session は対話可能です。workflow パネルには phase、agent、live status が表示され、個別 agent session を開いたり、進捗要約を求めたり、run を停止したりできます。

Enterprise アカウントでは、管理者が **Enterprise Settings → Devin** で **Dynamic workflows** を有効にするまで、企業内のどの organization でも使えない場合があります。

## オーサリング契約

スクリプトは Devin が書きますが、run を承認する前に本番コードと同じ基準でレビューしてください。

| Primitive | 用途 |
| --- | --- |
| `register_workflow(meta)` | agent 実行前に名前、説明、phase を宣言 |
| `agent(prompt, phase=..., schema=...)` | 1 つの agent を実行し、JSON Schema に沿った dict を返す |
| `pipeline(items, stage1, stage2, ...)` | 各 item を独立して各 stage に流す。stage 間にバリアはない |
| `parallel([...])` | async callables を並行実行し、すべて待つ。マージや dedup のように本当に全結果が必要な stage だけで使う |
| `log("message")` | 実行中に見える進捗行を書く |

Schema 設計ルール：

1. 小さく、平坦で、明示的にする。
2. 長文ではなく識別子と証拠を返す——branch 名、ファイルパス、件数、状態、1 行の finding。
3. 後段の作業が不要なら `None` または明示的な failure status を返す。
4. prompt や schema に secret を入れない。
5. agent output は次の prompt への信頼できない入力として扱い、実行前に検証する。

## 決定性が resume の代償

workflow を再開すると、スクリプトは先頭から再実行されます。完了済みの `agent()` 呼び出しは記録済み output を replay し、未完または失敗した呼び出しだけが再実行されます。これはスクリプトが毎回同じ呼び出しを行う場合にだけ成立します。

したがって、workflow ロジックと prompt は次に依存してはいけません。

- 現在時刻や日付
- 乱数や生成 ID
- 環境変数
- ファイルシステム状態
- ネットワーク応答

外部世界を観測する必要がある処理は `agent()` 呼び出しの中に入れます。スクリプトは記録済み output だけを消費します。

重要な結果が 2 つあります。

- prompt を編集すると、その agent と下游のすべてが再実行される。
- 中断またはタイムアウトした run は run ID で再開できる。既定および最大の run budget は 7 日間。

## Agent はどこで実行されるか

| モード | 使う場面 | 引き継ぎ | 主なリスク |
| --- | --- | --- | --- |
| Separate VM（既定） | agent に隔離された machine や通常の repo 環境が必要 | git branch を push/read する | agent ごとの setup とコストが増える |
| Shared VM | agent が現在の working tree を読み書きする必要がある | 共有ファイルシステム | CPU/メモリ競合と書き込み衝突 |

Shared-VM のファンアウトでは、並行して書く agent には厳密に重ならないファイルまたはディレクトリを割り当てます。Separate-VM pipeline では、branch 名を構造化 output に含めます。

分類のような大量・低判断の stage では、agent を低コストの Devin mode に固定することもできます。

## 最初の安全な workflow を作る

最初の workflow をリポジトリ全体に向けないでください。パターンを証明できるだけの広さがあり、かつ負担できる小ささの slice を選びます。

### 0. 絞った単位を選ぶ

良い最初の slice：

- 3 コンポーネントのアクセシビリティ audit
- 1 ディレクトリ内の SQL クエリの pagination 問題
- 5 件の open ticket の dedup と severity triage
- 3 つの migration unit（それぞれ独立 branch）

悪い最初の slice：

- 「monorepo 全体を audit」
- 「flaky test を全部直す」
- 「すべてのファイルを永久に review」

### 1. スクリプトではなく成果を書く

公式 migration パターンを改変した例：

```text
Use a workflow to audit the auth, billing, and search modules for missing
pagination and N+1 query patterns. Run one analysis agent per module.
For each confirmed issue, run a fix agent on its own branch and verify the
fix with an EXPLAIN plan before and after. Roll up the confirmed fixes,
skipped items, and anything needing human review.
```

この prompt には、scope、並列化単位、stage、検証方法、rollup 形状が含まれています。

### 2. 承認前に生成スクリプトをレビューする

次を正確に確認します。

- `register_workflow()` が agent より先に呼ばれている。
- 各 `agent()` に schema がある。
- agent 数が明示的な list で制限され、無制限 crawl ではない。
- failure behavior が明示されている：retry、status 付き skip、default 代入、run 失敗。
- スクリプトが決定的である。
- separate-VM agents が branch 経由でコードを受け渡し、shared-VM agents が互いを上書きしない。
- 最終 rollup が「done」だけでなく、証拠と未解決項目を含む。

Run は既定で自動承認されます。毎回 checkpoint が必要なら、**Settings → Preferences → Auto-approve workflows** をオフにします。

### 3. 実行、観察、正しい停止

実行中：

- workflow パネルで phase と agent status を見る。
- 1 つの agent session を開き、prompt と schema が意図に合うか確認する。
- 各 agent を手動で止めるのではなく、オーケストレーション session に進捗要約を求める。
- 設計が間違っていたら run を停止する。停止するとスクリプトが cancel され、残りの child sessions は sleep します。完了済みの結果は記録されたままです。

### 4. 決定性を保ってから再開する

中断された run は、同じスクリプトと run ID で再開します。prompt を編集した場合、その agent と下游の作業が新しい作業になることを理解してください。

### 5. 実証済み workflow を保存する

Workflow が成功したら、repo skill として保存するよう Devin に依頼します。`workflow.py` を、いつ使うかを説明する `SKILL.md` の隣に置きます。一度きりの orchestration が、再利用可能な組織の能力になります。

## コスト管理

各 workflow agent は 1 つの Devin session です。コストはファンアウト幅と session 深度の両方に比例します。

次の順序で進めます。

1. 3 item で prototype する。
2. workflow パネルで agent ごとの ACU usage を確認する。
3. 拡大前に full run を見積もる。
4. 分類・抽出 stage には低コスト mode を使う。
5. 高価な判断は、より少ない後段 agent に残す。
6. loop には hard stop condition を設定する。

Loop には「3 回連続で pass」「新しい修正がない round」など、書かれた終了条件が必要です。ない場合、workflow は予算を消費しながら、技術的には正しいが無用な進捗を生み続ける可能性があります。

## Verify it

初回再現は、次のすべてを満たす場合にだけ有効です。

- [ ] workflow が repo 全体ではなく 3–5 unit の限定 slice で実行された。
- [ ] workflow パネルに phase と個別 agent status が表示された。
- [ ] 少なくとも 1 つの後段 prompt が前段 agent の構造化 output を明示的に消費した。
- [ ] 1 つの agent session を開いて確認した。
- [ ] 最終 rollup が verified results、skipped items、failures、human-review items を分けた。
- [ ] agent ごとおよび run 全体の ACU usage を記録した。
- [ ] 中断または意図的停止後、run が正しく再開した。または再開できない理由を記録した。

## 落とし穴

- **機械的作業に agent を使う。** スクリプトが決定的に変換できるなら、スクリプトをツールとして使い、agent は判断に限定する。
- **Schema が essay を返す。** 長文は下游で使いにくい。 compact な structured facts を返す。
- **隠れた時間依存。** スクリプト内の「今日」、timestamp、random ID、live network check は replay semantics を壊す。
- **Shared-VM の書き込み衝突。** 2 つの agent が同じファイルを編集するのは並列化ではなく、merge conflict の製造です。
- **無制限ファンアウト。** workflow 内部で追加作業を発見する crawl はコストを爆発させる可能性があります。発見を制限するか、上流で人間が承認した input にします。
- **Failure contract がない。** 失敗した agent を skip、retry、item block、run failure のどれにするか、実行前に決めます。
- **早すぎる再利用。** 実際の slice で成功し、コストを理解するまで workflow を skill として保存しないでください。

## 演習

1. リポジトリ内の反復 review task を 1 つ選び、workflow prompt を書く。Devin に実行を求める前に、ファンアウト items を正確に列挙する。
2. *audit → fix* の 2 段階 schema を設計する。path や branch 名以外の各 field は 120 文字以内にする。
3. 失敗した agent を想定し、3 つの failure policy を書いて 1 つ選ぶ。rollup に何を表示すべきか説明する。
4. 3-item prototype から 50-item fan-out のコストを見積もる。その見積もりを有効にする証拠は何か。

## Capstone

書面化された standard に対して 5 つのファイルまたはモジュールを audit し、確認済み issue を独立 branch で修正し、利用可能な最も狭い実チェックで各修正を verify し、最終 evidence table を出す workflow を作ります。2 回目も成功した後にだけ、skill として保存します。

## Knowledge check

1. workflow prompt が「today」や random ID を避けるべき理由は？*（再開時にスクリプトが再実行され、入力変化が agent-call identity を変え、deterministic replay を壊すため。）*
2. `parallel()` が既定の composition primitive でない理由は？*（多くの pipeline は item ごとに流れるべきで、`parallel()` はバリアを作る。本当に全結果が必要な stage だけに使うため。）*
3. 最初に最も安全な fan-out サイズは？*（約 3–5 unit の限定 slice。orchestration を証明でき、コスト測定と挙動確認もできる大きさ。）*
4. workflow が skill になるに値するのはいつか？*（実作業で成功し、コストと failure behavior が分かり、再利用可能性が高いとき。）*

## Sources

- [Dynamic Workflows — 公式ドキュメント](https://docs.devin.ai/work-with-devin/dynamic-workflows)
- [Advanced capabilities — managed Devins](https://docs.devin.ai/work-with-devin/advanced-capabilities)
- [Skills — 公式ドキュメント](https://docs.devin.ai/product-guides/skills)
- [Devin MCP — 公式ドキュメント](https://docs.devin.ai/work-with-devin/devin-mcp)

## Changelog

- 2026-11-26 — 公式ドキュメントに基づく初版。独立した再現エビデンスは未整備。実際の run が記録されるまで、演習を検証済みとみなさないこと。
