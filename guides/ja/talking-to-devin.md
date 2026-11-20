# ガイド 18 — Devin への伝え方：プロンプトの教義

**ゴール:** Devin が読み違えようのない指示を書く——仕上がるセッションと迷走するセッションの分かれ目。
**レベル:** ここから始める
**ソース:** [Coding Agents 101](https://devin.ai/agents101)（Cognition、2025年6月）· [Instructing Devin Effectively](https://docs.devin.ai/essential-guidelines/instructing-devin-effectively)——どちらも公式。以下は要点＋現場注釈

## このガイドが最初にある理由

このリポジトリのすべてのガイドが前提にするスキルがひとつある：欲しいものを Devin が誤解しようのない形で伝えられること。Cognition 自身の2つのガイダンス——*Coding Agents 101* と docs の *Instructing Devin Effectively*——は異なる角度から同じことを言っている：**エージェントを最も活用しているエンジニアは、願い事を書くのではなく、ジュニアな同僚にブリーフするように書く。** このガイドはその教義の凝縮版であり、カリキュラムの残りに繋がっている。

## 他のすべてを支える4つのルール

**1. 「何を」だけでなく「どう」を言う。** 「search モジュールの C++ バインディングを直して新しいユニットテストを通して——注意、変更のたびにバインディングを再コンパイルしてからテストして」。自分のコードベースの罠は自分が一番知っている。書き出せ。オープンエンドな指示（「アプリを良くして」「DB のパフォーマンスを改善して」）はオープンエンドな結果を返す。

**2. どこから始めるかを教える。** リポジトリ、ディレクトリ、ファイル、参照実装、ドキュメント URL——そのタスクが*あなたの*机に来たら欲しいものすべて。「`authTemplate.rs` を参考にエラーハンドリングの一貫性を保って」は、スタイルの長文に毎回勝つ。

**3. 成功をチェック可能な形で定義する。** 「ちゃんと動くこと」ではなく——Devin が実行できるチェック：*エンドポイントが X/Y/Z フィールド付きで 200 を返す*、*1440px と 375px で console エラーなしにレンダリングされる*、`npm test` がグリーン。Devin は完全なマシンを持っている——ブラウザ、シェル、IDE。自分で検証させよ（「`npm run dev` を実行して `/settings` が描画されることを確認」）。PR を見る前に QA が終わっている。

**4. フィードバックの雰囲気ではなくループを与える。** 型チェッカー、リンター、テスト、CI——エージェントの超能力はエラーメッセージに対して反復すること。リポジトリが間違いを教えられないなら、あなたがフィードバックループになる。それは一番高い構成だ。

## 公式の見本ブリーフの解剖

Cognition 自身のモデルプロンプトに注釈：

> In the Devin repo, build a tool that monitors RAM and CPU usage of the remote machines Devin runs on.——*スコープと目的を1行で*
>
> - Create a background task that launches when devin.rs starts——*かたまりではなく段階的に*
> - It opens a connection to all forked remote machines and monitors usage——*仕組みを名指し*
> - If usage exceeds 80%, emit a new type of Devin event (check how we use Kafka)——*成功基準 + 既存パターンへのポインタ*
> - Architect so it doesn't block other operations——*作者だけが知る制約*

ないものに注目：美的意見、留保、「たぶん」「良いと思えば」。すべての行がシステムを知る人間の下した決定だ。

## 防衛線の向こう：自分に残すもの

101 ガイドは限界について率直だ：**大きなチケットでは ~80% の時間削減を期待し、完全自動化ではない。** 数ファイルを超えるものは複数回のフィードバックを見込め。勝つ姿勢は*ジュニアのドラフト PR をレビューするアーキテクト*——正しさはあなた、キーストロークは Devin。

実際の帰結：

- **スコープを固く。** 「merge、deploy、billing に触れるのは私に聞いてから」——フェンスは明示し、暗示的な良識に頼らない。
- **大きな仕事は検証可能なサブタスクに分割**——サブタスクごとに1セッション、それぞれ成功チェック付き（ガイド 11 の移行パターンが効く理由でもある：小さな PR を何百も、すべて検証可能）。
- **繰り返すものは Skill に。** `SKILL.md` を一度書けば、Devin が自動で呼ぶ（ガイド 16）。

## 「指示」から「所有」へ

セッション指示は*「このタスクをうまくやれ」*に答える。Bot の outcome prompt は*「この領域を持て」*に答える。教義は同じ——具体性、境界、チェック可能な成功——だが対象がタスクから責任に変わる。ここが流暢になったら、[outcome-prompts リファレンス](bot-outcome-prompts.md)が同じ筋肉で Android Bot の 1,134 PR を生む様子を見せてくれる。

## 実録ウォークスルー — Devin CLI v3000.14（swe-2-flash-medium）で収録

使い捨ての `demo-repo` でドクトリンを実演：4 行のブリーフ——方法＋機構、ファイル名指名、検証可能な成功条件、明示の境界。1 セッション、途中確認ゼロ、自己検証済み。

**動画（90 秒、無音）：** ブリーフ → 編集 → 権限プロンプト → セルフチェック → 境界遵守。

[![SWE-2 Flash Medium がタスク完了 — 5 件の unittest 全パス、コミットなし](https://till3005.github.io/built-with-devin/assets/guides/talking-to-devin/walkthrough-poster.webp)](https://till3005.github.io/built-with-devin/assets/guides/talking-to-devin/walkthrough.mp4)

![1. demo-repo の CLI REPL、SWE-2 Flash Medium — composer 準備完了](https://till3005.github.io/built-with-devin/assets/guides/talking-to-devin/step1-repl-flash.webp)
*1. demo-repo の CLI REPL、SWE-2 Flash Medium — composer 準備完了*

![2. そのブリーフ — 4 行に 4 つのルール：方法、起点、成功条件、境界](https://till3005.github.io/built-with-devin/assets/guides/talking-to-devin/step2-the-brief.webp)
*2. そのブリーフ — 4 行に 4 つのルール：方法、起点、成功条件、境界*

![3. 途中：test_app.py を記述中 — 権限プロンプトは Allow / accept-edits / bypass / deny](https://till3005.github.io/built-with-devin/assets/guides/talking-to-devin/step3-edits-approval.webp)
*3. 途中：test_app.py を記述中 — 権限プロンプトは Allow / accept-edits / bypass / deny*

![4. 自己検証：エージェントが指名どおりのチェック `python3 -m unittest -v` を要求](https://till3005.github.io/built-with-devin/assets/guides/talking-to-devin/step4-self-check-prompt.webp)
*4. 自己検証：エージェントが指名どおりのチェック `python3 -m unittest -v` を要求*

![5. 完了 — 5 テスト全パス；報告自体が境界を確認「No commit made.」](https://till3005.github.io/built-with-devin/assets/guides/talking-to-devin/step5-tests-green.webp)
*5. 完了 — 5 テスト全パス；報告自体が境界を確認：「No commit made.」*

![6. /exit 後 — `devin -r` 再開ヒントと、境界が守られた `git status`：2 ファイル変更、新規コミットなし](https://till3005.github.io/built-with-devin/assets/guides/talking-to-devin/step6-no-commit.webp)
*6. /exit 後 — `devin -r` の再開ヒント、境界が守られた `git status`：2 ファイル変更、新規コミットなし*

## 確認

- [ ] バックログの実タスクに対し、10 分以内に「名前付きリポ/ファイル、参照パターン、明示的な成功チェック、宣言された境界」を含むブリーフが書ける。
- [ ] セッションが「当然でしょ」と思う確認を途中でしてこない。
- [ ] Devin が PR の前に自分で検証した——ブリーフで要求したから。

## 落とし穴

- **自分の混乱をそのまま書く。** 成功チェックが言えないならタスクはまだ早い。直感に頼るより、先に Devin と PRD を共同作成せよ（101 ガイドも推奨）。
- **権限に見合わない野心。** CI を見られないアカウントに「CI を直せ」は自信満々の間違いを生む。指示は実際に与えたアクセスに合わせる。
- **出力ではなく正しさをレビュー。** グリーンなテストと妥当な diff は進捗の証拠であって、正しさの証明ではない。最終検証は常にあなた。

## 理解度チェック

1. *「ユニットテストを追加」が「`poller.ts` のリトライパスにユニットテストを追加、`fetch` をモック、タイムアウトと 5xx をカバー」に負ける理由は？* 後者はエージェントが判断を下す必要をなくす：何をテストし、どのエッジが重要で、何をモックするか。明記されない決定はすべて、あなたが制御しないコイントス。
2. *Devin がきれいな diff とグリーン CI の PR を出した。完了？* まだ——CI グリーンはチェックが通ったという意味で、意図が満たされた証拠ではない。最終検証レイヤーはあなた。その非対称が取引の本質（~80% 削減、正しさは人間）。
3. *指示はいつ Skill に昇格する？* 同じものをまた打っていると気づいた時。3 度目は SKILL.md——フォーマットと発見パスはガイド 16。

## ソース

- [Coding Agents 101](https://devin.ai/agents101) — Cognition のプロンプト教義：say-how、起点指示、防御的プロンプト、フィードバックループ、80% ルール
- [Instructing Devin Effectively](https://docs.devin.ai/essential-guidelines/instructing-devin-effectively) — 公式 do/don't と上で解剖した見本ブリーフ
- [Devin チュートリアルライブラリ](https://docs.devin.ai/tutorial-library) + [Devin University](https://learndevin.com) — 動画・コース形式の教材
- 現場メモ：[コミュニティ実践レポート](community-field-reports.md)のすべてが同じ結論に収束する——願いではなくブリーフを
- 次：[ガイド 1 — 初めての Bot](bots-101-first-bot.md)（同じ教義、より大きな対象）· [outcome prompts リファレンス](bot-outcome-prompts.md)
