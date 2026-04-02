# /analysis — 分析自動化 Skill

データを渡すと DoD に沿った分析を実装し、DA レビューが収束したら PR を作成する。

## 起動方法

```
/analysis <data_path_or_theme> --domain <domain> [--title <slug>] [--rq "リサーチクエスチョン"] [--no-model]
```

**引数:**
- `<data_path_or_theme>` — データファイルのパス、URL、または分析テーマの文字列（必須）
- `--domain <domain>` — ドメイン（必須）。DoD Sec 7 のドメイン表を参照
  - 例: `demographics`, `economics`, `health`, `environment`, `education`, `transportation`, `finance`, `society`
  - 不明な場合は `/brainstorm` skill で相談してから決める
- `--title <slug>` — 分析タイトルのスラッグ（省略時は日付+テーマから自動生成）
- `--rq "..."` — リサーチクエスチョン（省略時は EDA 後に analysis-agent が提案）
- `--no-model` — モデリングフェーズをスキップする

**例:**
```
/analysis data/raw/population.csv --domain demographics --title population-aging --rq "少子高齢化の地域差はどれくらいか"
/analysis "東京都の気温と電力消費" --domain environment --no-model
```

## 依存ファイル

- `.claude/rules/analysis-dod.md` — DoD（読み取り専用・唯一の真実）
- `.claude/agents/analysis-agent.md` — 分析実装エージェント
- `.claude/agents/da-reviewer.md` — DA レビュワーエージェント
- `.github/PULL_REQUEST_TEMPLATE.md` — 手動 PR 用テンプレート（自動 PR では body を動的生成）

## メインフロー

```
Step 1: 引数パース
Step 2: ブランチ作成
Step 3: PROPOSAL 作成（analysis-agent Phase 1）
Step 4: PROPOSAL DA レビューループ  ← HARKing をここで封じる
Step 5: 分析実施（analysis-agent Phase 2〜5）
Step 6: 分析結果 DA レビューループ
Step 7: PR 作成
Step 8: 完了報告
```

---

### Step 1 — 引数パース

`$ARGUMENTS` を解析して以下を決定する:

```
data_path  = <最初の位置引数>
domain     = --domain の値（未指定の場合はユーザーに確認して停止）
title      = --title の値 OR "YYYYMMDD-" + data_path のファイル名（拡張子なし）
rq         = --rq の値 OR null
has_model  = --no-model が指定されていなければ true
```

今日の日付を YYYYMMDD 形式で取得し title の先頭に付与する。
`--domain` が未指定の場合は以下を伝えて停止する:
```
--domain が必要です。DoD Sec 7 のドメイン表を参照するか、/brainstorm で相談してください。
例: --domain demographics
```

---

### Step 2 — ブランチ作成

```bash
git checkout -b analysis/<domain>/<title>
```

ブランチが既に存在する場合はそのままチェックアウトする（再実行の場合）。

---

### Step 3 — PROPOSAL 作成（analysis-agent Phase 1 のみ）

`analysis-agent` を Agent ツールで呼び出す:

```
data_path      : <Step 1 で決定>
title          : <Step 1 で決定>
rq             : <Step 1 で決定>
has_model      : <Step 1 で決定>
phase          : "proposal"
review_feedback: null
```

`analysis-agent` から `PROPOSAL_COMPLETE` を受け取るまで待機する。

---

### Step 4 — PROPOSAL DA レビューループ

**目的: 仮説・RQ・スコープを EDA 開始前に確定させ、HARKing の余地をなくす。**
LGTM が出るまで分析（Step 5）には進まない。

制御変数:
```
proposal_review_count = 0
max_reviews           = 3
proposal_lgtm         = false
```

`proposal_lgtm == false` かつ `proposal_review_count < max_reviews` の間ループする:

1. `da-reviewer` を Agent ツールで呼び出す
   ```
   analysis_dir  : "analysis/<domain>/<title>/"
   review_mode   : "proposal"
   review_count  : proposal_review_count + 1
   ```

2. 出力を受け取る:
   - `LGTM` を含む → `proposal_lgtm = true`、ループ終了
   - `NEEDS_REVISION` を含む → `proposal_feedback` に指摘内容を格納

3. `proposal_lgtm == false` の場合:
   - `proposal_review_count += 1`
   - `analysis-agent` を再呼び出しする
     ```
     phase          : "proposal"
     review_feedback: <proposal_feedback>
     その他は Step 3 と同じ
     ```
   - `PROPOSAL_COMPLETE` を受け取るまで待機する

ループ終了後、`proposal_review_count >= max_reviews` かつ `proposal_lgtm == false` の場合:
- ユーザーに報告して確認を求める:
  ```
  PROPOSAL が 3 往復で収束しませんでした。
  RQ・仮説・スコープを手動で確認・修正してから続行してください。
  続行しますか？
  ```
- ユーザーが承認した場合のみ Step 5 へ進む

---

### Step 5 — 分析実施（analysis-agent Phase 2〜5）

PROPOSAL が確定した後に初めて EDA・分析・モデリングを開始する。

`analysis-agent` を Agent ツールで呼び出す:

```
data_path      : <Step 1 で決定>
title          : <Step 1 で決定>
rq             : <Step 1 で決定（PROPOSAL.md で確定済みの内容）>
has_model      : <Step 1 で決定>
phase          : "analysis"
review_feedback: null
```

`analysis-agent` から `ALL_PHASES_COMPLETE` を受け取るまで待機する。

---

### Step 6 — 分析結果 DA レビューループ

制御変数:
```
review_count = 0
max_reviews  = 3
lgtm         = false
```

`lgtm == false` かつ `review_count < max_reviews` の間ループする:

1. `da-reviewer` を Agent ツールで呼び出す
   ```
   analysis_dir  : "analysis/<domain>/<title>/"
   review_mode   : "full"
   review_count  : review_count + 1
   ```

2. 出力を受け取る:
   - `LGTM` を含む → `lgtm = true`、ループ終了
   - `NEEDS_REVISION` を含む → `feedback_text` に指摘内容を格納

3. `lgtm == false` の場合:
   - `review_count += 1`
   - `analysis-agent` を再呼び出しする
     ```
     phase          : "analysis"
     review_feedback: <feedback_text>
     その他は Step 5 と同じ
     ```
   - `REVISION_COMPLETE` を受け取るまで待機する

ループ終了後、`review_count >= max_reviews` かつ `lgtm == false` の場合:
- ユーザーに確認を求める:
  ```
  分析レビューが 3 往復で収束しませんでした。
  現在の状態で PR を作成しますか？（手動レビューを推奨します）
  ```
- ユーザーが承認した場合のみ Step 7 へ進む

---

### Step 7 — PR body の動的生成と PR 作成

**`.claude/rules/analysis-dod.md` を Read して PR body を動的に組み立てる。**
DoD のチェック項目はこのファイルに書かない。

1. `.claude/rules/analysis-dod.md` を Read する
2. セクション 1〜5 の `- [ ]` で始まる行をすべて抽出し、セクション見出しでグループ化する
3. `PROPOSAL.md` を Read して RQ・動機を抽出する
4. 以下の構造で PR body を組み立てる:

```markdown
## 分析概要

**リサーチクエスチョン:** {PROPOSAL.md から抽出}

**動機・背景:** {PROPOSAL.md から抽出}

---

## 成果物

{analysis/<title>/ 以下の実際のファイル一覧}

---

## DoD チェックリスト

> ソース: `.claude/rules/analysis-dod.md`（このリストはファイルから動的生成）

{Sec 1〜5 の全 - [ ] 行をセクション見出しつきで展開}

---

## DA レビュー履歴

- PROPOSAL レビュー: {proposal_review_count} 往復 → {LGTM / 手動承認}
- 分析結果レビュー: {review_count} 往復 → {LGTM / 手動承認}

---

## レビュワーへの補足

（特記事項があれば記載）

---

_Generated by `/analysis` skill. DoD: `.claude/rules/analysis-dod.md`_
```

5. PR を作成する:

```bash
git add analysis/<domain>/<title>/
git commit -m "analysis(<domain>/<title>): {RQ の先頭 50 文字}"
git push -u origin analysis/<domain>/<title>
gh pr create \
  --title "analysis(<domain>): {title} — {RQ の先頭 60 文字}" \
  --body "{組み立てた body}" \
  --base main
```

---

### Step 8 — 完了報告

```
分析が完了しました。

ブランチ: analysis/<domain>/<title>
PR: {PR URL}

PROPOSAL レビュー: {proposal_review_count} 往復で収束
分析結果レビュー: {review_count} 往復で収束
成果物: analysis/<domain>/<title>/REPORT.md
```

---

## エラーハンドリング

| 状況 | 対処 |
|------|------|
| `data_path` が存在しない | ユーザーにパスを確認して停止 |
| PROPOSAL が 3 往復で収束しない | ユーザーに手動確認を求め、承認後のみ続行 |
| `ALL_PHASES_COMPLETE` が返らない | エラー内容をユーザーに報告して停止 |
| `git push` が失敗する | エラーをユーザーに報告。force push は行わない |
| PR 作成が失敗する | `gh` のエラーをユーザーに報告。手動作成を案内する |
