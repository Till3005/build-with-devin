# ガイド 11 — スケールする移行

**目標：** 大規模移行（言語、フレームワーク、データベース、依存関係、アーキテクチャ）を 1 回の英雄的リライトではなく、数百の小さな検証済み PR として実行する。
**レベル：** 中級 → 上級
**出典：** [ベストプラクティス](https://docs.devin.ai/use-cases/best-practices.md) · [移行とモダナイゼーション](https://docs.devin.ai/use-cases/migration-modernization.md) · 移行例：[Java アップグレード](https://docs.devin.ai/use-cases/examples/java-upgrades.md)、[COBOL](https://docs.devin.ai/use-cases/examples/cobol-modernization.md)、[SAS→PySpark](https://docs.devin.ai/use-cases/examples/sas-to-pyspark.md)、[JS→TS](https://docs.devin.ai/use-cases/examples/javascript-to-typescript.md)、[NoSQL→SQL](https://docs.devin.ai/use-cases/examples/nosql-to-sql.md) · Nubank ケーススタディ

## 公式プレイブック

Devin 自身のドキュメントはスケールするものを率直に述べている：**広く浅く**が**高く深く**に勝る。移行は典型的な広く浅い仕事——同じ小さな変換を数百の独立単位に適用する。

```text
移行 ──► 孤立した単位にスライス（各 90 分以内）
                 │
        ┌────────┴────────┐
        ▼                 ▼
   変換のスキル      並列セッション、
                    各 1 スライス
        │                 │
        └────► スライスごとに検証（テスト/ビルド/CI）
                        │
              人間レビュー → マージ → 繰り返し
```

## ステップ 1 — 移行が適格か確認する

公式基準から——ほとんどが成立すべき：

- 反復的なサブタスクの大量性
- スライスごとの複雑度がジュニアエンジニア級
- 孤立し、増分的で、後方互換な変更
- **スライスごとの客観的検証**（必須要件：テスト、ビルド、CI、またはカスタムスクリプト）
- 最小限のスライス間依存

不適格：すべてが一度に着地しなければならない全リポジトリのリライト。

## ステップ 2 — スライスする

スライスは最小の原子単位——ファイル、ノートブック、モジュール：

| ルール | 理由 |
| --- | --- |
| スライスあたり手作業 90 分未満 | Devin の信頼性はスライス単位 |
| 独立 + 後方互換 | スライスは並列で走り任意の順でマージできる |
| 各スライスが自身の検証を持つ | 検証なし、自動化なし——これが失敗ゲート |

公式の例：50 ファイルの REST→GraphQL 移行 → スコープを定め、競合しない作業パッケージに分割し、並列で実行。

## ステップ 3 — 変換をスキルとして書く

1 スキル = 全セッションが実行する再現可能なレシピ。公式例（Java 7→8、抜粋）：

```text
## Procedure
1. Verify the project is on Java 7
2. Install the Java 8 JDK
3. Update build configuration
4. Identify and replace deprecated Java 7 APIs
5. Analyze for Java 8 enhancement opportunities
6. Update unit tests
7. Test thoroughly
8. Update documentation
9. Build and verify
```

あなた版に含めるもの：明示的な手順、エンドツーエンドの参照（ガイドまたは動画）、**複数の前後コード例**——入出力ペアは与えられる最高品質のシグナル。

## ステップ 4 — 並列セッションを回す

スキルが固まったら、スライスをセッション群に展開——[API](https://docs.devin.ai) または Bot の子セッション（ガイド 4）。スライスごとに → 1 セッション → 1 PR。`main` へのマージは人間レビューがゲート。

スケールでは数値が複利になる：Nubank の数百万行 ETL 移行はこのループで効率 8–12 倍——ファインチューンされた Devin がタスクあたり時間を約40分→約10分に削った。

## ステップ 5 — 進捗バーではなくエラー率を見る

小さなエラー率は数千スライスで複利になる。雰囲気ではなくダッシュボードで運用する：

- 初回試行のスライス合格率を追跡——修正点はセッションではなくスキル
- 失敗したスライスはスキルにフィードバック（ドキュメント自身のループ：*「セッションリンクを Devin に投入してギャップをパッチ」*）
- スライスが孤立しているためマージ順は自由——それを活用する

## 移行 diff に stack が必要なとき

複数の移行スライスが一貫した依存チェーンを成すとき、それらをレビュー不能な巨大 diff に押し込まない。schema、変換機構、最初の移行スライス、クリーンアップのように、一貫した変更に自然な層があるときは、Devin に **stacked PR series** を頼む。各層は下の PR の上に乗る小さな PR で、マージは bottom-up かつアトミック。base が入ると GitHub が残りの層を自動で retarget する。

制約も重要である。stacked PRs は **GitHub.com のみ**、2–100 件の PR で構成され、GitHub の通常 merge フローは使えない。独立した通常の移行スライスは普通の並列 PR のままにし、順序どおりに一緒に入れる必要がある依存層だけを stack にする。

## 検証チェックリスト

- [ ] すべてのスライスが約 90 分以内に終わり独立してマージできる
- [ ] 検証に失敗したスライスが修正またはフラグ付きチケットを生む——静かなマージはない
- [ ] 最初の 20 スライスでスキルが測定可能に改善した（スライスあたりの人間修正が減少）
- [ ] 進捗が数えられる：N/M スライス移行済み、合格率が可視

## 落とし穴

- **スライスされていない移行。** 「リポジトリ全体を移行せよ」は公式アンチパターン——孤立なし、並列性なし、単位ごとの検証なし。
- **前後例なし。** 例のないスキルはセッションごとに異なるスタイルを産む。
- **人間レビューの省略。** 並列 ≠ 無人——各スライスは `main` 前にレビューされる。

## 理解度チェック

1. なぜ「深く完全な」スライスでなく「広く浅い」スライスか？*（各スライスがグリーンで着地しなければならない——90 分の検証済み PR は複利になる；3 日のメガブランチは main に対して腐る）*
2. なぜすべてのスライスが独自の検証を要るのか？*（スライスごとの証明がなければ、500 PR の移行は 500 の未検証 diff——失敗面は分割されるのでなく増殖する）*
3. Nubank が 8–12 倍の効率を報告——それをマーケティングでなく信頼できる数値にしたものは？*（公開された方法論：実際の ETL パイプラインで前後の段階時間を計測、予測ではなく）*

## 実録 —— 移行ループを逐次実行、Devin CLI v3000.14（swe-2-flash-medium）

数百の並列セッションはクラウドのクォータが必要——だが*ループ自体*には不要。無料枠で逐次実行した。`migrate-demo`：optparse CLI 4 本（greeter/calc/backup/report）、ツールごとに振る舞いテスト、変換レシピは `.devin/skills/optparse-to-argparse/SKILL.md`。プロンプト：「独立したスライスとして移行……各ツールを移行したらテストを実行し、緑になってから次へ。」

**動画（41 秒・無音）：** ベースライン → skill 呼び出し → 4 スライスそれぞれで緑 → `optparse` 残存ゼロ。

[![スライスループ全体——各ツール移行後にテスト緑、レシピどおりのまとめ](https://till3005.github.io/built-with-devin/assets/guides/migrations-at-scale/walkthrough-poster.webp)](https://till3005.github.io/built-with-devin/assets/guides/migrations-at-scale/walkthrough.mp4)

![1. ベースライン——optparse ツール 4 本、振る舞いテスト 7 件全緑](https://till3005.github.io/built-with-devin/assets/guides/migrations-at-scale/step1-baseline.webp)
*1. ベースライン：OptionParser 4 本・テスト 7 件・skill レシピをコミット済み*

![2. .devin/skills から skill が自動呼び出し——まず全ツールとテストを読む](https://till3005.github.io/built-with-devin/assets/guides/migrations-at-scale/step2-skill-invoked.webp)
*2. `Invoked skill optparse-to-argparse`——レシピが実行を駆動*

![3. スライスループ——「Green. Now calc.py——rest で位置引数を読むので parse_known_args で形を保つ」](https://till3005.github.io/built-with-devin/assets/guides/migrations-at-scale/step3-slice-loop.webp)
*3. スライスごとに検証。calc.py に `parse_known_args` が必要な点も自力で検出*

![4. /exit 後に検証——4 ファイル移行、+18/−18、optparse 参照ゼロ、コミットなし](https://till3005.github.io/built-with-devin/assets/guides/migrations-at-scale/step4-verify-diff.webp)
*4. 検証済みの小さな diff ×4——スライス規律そのもの（並列フリートは除く）*

## 出典

- [ベストプラクティス — docs.devin.ai](https://docs.devin.ai/use-cases/best-practices.md)
- [移行とモダナイゼーション + 5 つのプレイブック例](https://docs.devin.ai/use-cases/migration-modernization.md)
- [ユースケースギャラリー — 移行](https://docs.devin.ai/use-cases/gallery/index.md)
- [Cognition の .NET 移行プレイブック](https://cognition.com/blog/dotnet-migration-with-devin) —— Ask Devin がコンテキストでコントローラーをランク付け、連携セッションが並列移植：月 → 週（ベンダー公開）
- 関連：[ガイド 7 — エンタープライズ導入](enterprise-playbook.md)（形 1 はこのガイドの組織スケール版）
- [Stacked PRs docs](https://docs.devin.ai/work-with-devin/stacked-prs) — bottom-up atomic stack と GitHub.com 限定の制約
