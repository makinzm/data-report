## 分析概要

<!-- PROPOSAL.md の RQ を 1〜2 文で転記 -->

**リサーチクエスチョン:**

**動機・背景:**

---

## 成果物

<!-- 生成・更新したファイルの一覧 -->
- [ ] `analysis/<title>/PROPOSAL.md`
- [ ] `analysis/<title>/decisions/` に ADR が ___ 件
- [ ] `analysis/<title>/notebooks/01_eda.ipynb`
- [ ] `analysis/<title>/notebooks/02_analysis.ipynb`
- [ ] `analysis/<title>/notebooks/03_model.ipynb` （モデリングあり時）
- [ ] `analysis/<title>/REPORT.md`

---

## DoD セクション別確認

> 各セクションの詳細チェック項目は [`.claude/rules/analysis-dod.md`](.claude/rules/analysis-dod.md) を参照。
> 自動 PR（`/analysis` skill 経由）の場合、以下の代わりに DoD 全項目が動的展開される。

- [ ] **Sec 0 — HARKing 禁止**: 仮説・評価指標を分析前に文書化している
- [ ] **Sec 1 — 着手前チェック**: PROPOSAL.md（RQ・仮説・スコープ）が完成している
- [ ] **Sec 2 — データ**: 出典・品質・再現性（シード・環境情報）を記録している
- [ ] **Sec 3 — 手法選定 ADR**: 採用した手法ごとに ADR を作成し選択理由を書いている
- [ ] **Sec 4 — 分析実施**: EDA/CDA/可視化 および モデル診断（該当時）を実施している
- [ ] **Sec 5 — 結論・レポート**: 論理整合性・限界の記載・クリーン実行確認を完了している

---

## DA レビュー

<!-- /analysis skill 経由の場合は自動記入される -->

- レビュー往復回数:
- 最終判定: LGTM / 未収束（手動レビュー推奨）

---

## レビュワーへの補足

<!-- DA が見落とした可能性のある特記事項、データの特殊性、判断に迷った箇所など -->
