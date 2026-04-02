# RUNBOOK: ウクライナ侵攻と世界資源価格・物価変動

このファイルの手順を上から順に実行すれば、誰でも同じ結果を再現できる。
コマンドは `analysis/economics/20260402-ukraine-commodity-cpi/` をカレントディレクトリとして実行する。

---

## Step 0 — 前提確認

```bash
# Python バージョン確認（3.10 以上推奨）
python3 --version

# リポジトリのルートに移動
cd /Users/hope/workspace/data-report

# ブランチ確認
git checkout analysis/economics/20260402-ukraine-commodity-cpi
```

---

## Step 1 — Python 環境セットアップ

```bash
# 仮想環境を作成（初回のみ）
python3 -m venv .venv
source .venv/bin/activate

# 依存パッケージをインストール
pip install -r analysis/economics/20260402-ukraine-commodity-cpi/requirements.txt
```

> `requirements.txt` がまだ存在しない場合は先にStep 2を読んでから作成する。

---

## Step 2 — UN Comtrade APIキー登録（初回のみ・手動作業）

UN Comtrade のデータは自動取得にAPIキーが必要。以下の手順で取得する。

1. ブラウザで https://comtradeplus.un.org/ を開く
2. 右上「Sign In」→「Register」でアカウントを作成
3. 登録後、https://comtradedeveloper.un.org/ を開く
4. 「Products」→「comtrade - v1」→「Subscribe」を選択
5. 発行された API キーをコピー
6. `.env` ファイルを作成して貼り付ける:

```bash
cd analysis/economics/20260402-ukraine-commodity-cpi
cp .env.example .env
# エディタで .env を開き COMTRADE_API_KEY=<取得したキー> を記入
```

**注意:** `.env` は `.gitignore` 済みのためコミットされない。

---

## Step 3 — データ取得（自動）

以下のスクリプトを順番に実行する。各スクリプトは `data/raw/` にデータを保存する。

### 3-1. World Bank Pink Sheet（原油・小麦・天然ガス）

```bash
python scripts/fetch_pinksheet.py
# 出力: data/raw/pinksheet_monthly.xlsx
# 取得元: World Bank（CC BY 4.0）
```

### 3-2. FAO Food Price Index

```bash
python scripts/fetch_fao_fpi.py
# 出力: data/raw/fao_food_price_index.csv
# 取得元: FAO（CC BY 4.0）
```

### 3-3. OECD CPI（11カ国・月次）

```bash
python scripts/fetch_oecd_cpi.py
# 出力: data/raw/oecd_cpi_monthly.csv
# 取得元: OECD SDMX-JSON API（CC BY 4.0）
# 対象国: DEU FRA ITA POL TUR USA GBR CAN AUS JPN KOR
```

### 3-4. IMF CPI（5カ国・年次・OECD非加盟国補完）

```bash
python scripts/fetch_imf_cpi.py
# 出力: data/raw/imf_cpi_annual.csv
# 取得元: IMF DataMapper API（研究利用可）
# 対象国: EGY NGA IND CHN SAU
```

### 3-5. UN Comtrade（ロシア・ウクライナ輸出データ・補助情報）

```bash
python scripts/fetch_comtrade.py
# 出力: data/raw/comtrade_ru_ua_exports.csv
# 取得元: UN Comtrade API（研究内部利用可）
# 注意: APIキーが .env に設定されている必要がある
# 注意: 1日500リクエスト上限。取得済みの場合はキャッシュが使われる
```

---

## Step 4 — データ確認チェック

```bash
python scripts/validate_data.py
# 各 data/raw/ ファイルの存在・行数・期間・欠損値を確認してレポートを出力
```

以下をすべて確認してから次のステップへ進む:
- [ ] `pinksheet_monthly.xlsx` が存在し、2020-01〜2023-12 の行を含む
- [ ] `fao_food_price_index.csv` が存在し、月次データが揃っている
- [ ] `oecd_cpi_monthly.csv` が存在し、11カ国 × 48ヶ月 = 528行以上ある
- [ ] `imf_cpi_annual.csv` が存在し、5カ国 × 4年 = 20行以上ある
- [ ] `comtrade_ru_ua_exports.csv` が存在する（補助情報）

---

## Step 5 — ノートブック実行

**重要:** ノートブックは必ずカーネルをリセットしてから先頭から順番に実行すること（再現性確保）。

```bash
jupyter lab
```

実行順序:

### 5-1. `notebooks/01_eda.ipynb`

```
Kernel → Restart Kernel and Run All Cells
```

出力されるもの:
- `outputs/figures/01_commodity_prices_timeseries.png` — 資源価格時系列
- `outputs/figures/02_fao_fpi_timeseries.png` — FAO食料価格指数時系列
- `outputs/figures/03_cpi_by_country.png` — 国別CPI推移
- `outputs/figures/04_cpi_peak_comparison.png` — ピーク時比較棒グラフ
- `outputs/figures/05_world_map_cpi.png` — 世界地図ヒートマップ
- `outputs/figures/06_world_map_exports.png` — 輸出依存度地図

### 5-2. `notebooks/02_analysis.ipynb`

```
Kernel → Restart Kernel and Run All Cells
```

出力されるもの:
- `outputs/figures/07_price_change_pct.png` — 侵攻前後の価格変化率
- `data/processed/summary_table.csv` — 集計サマリーテーブル

---

## Step 6 — レポート確認

`REPORT.md` を開いて以下を確認する:
- [ ] 先頭にRQへの直接回答がある
- [ ] EDA発見事項が「〜が観察された」「〜の傾向が見られた」という表現になっている
- [ ] 「〜が原因だ」「〜が証明された」という表現を使っていない
- [ ] 分析の限界と次のステップが記載されている

---

## Step 7 — 再現性の最終確認

別のターミナルで仮想環境をゼロから作り直し、Step 1〜5を再実行して同じ図が出ることを確認する。

```bash
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r analysis/economics/20260402-ukraine-commodity-cpi/requirements.txt
# Step 3〜5 を再実行
```

---

## データ取得日時の記録

データを取得したら以下を `data/raw/SOURCES.md` に記録すること（再現性のため）:

```markdown
| ファイル名 | 取得日時 | 取得者 | 備考 |
|-----------|---------|-------|------|
| pinksheet_monthly.xlsx | YYYY-MM-DD HH:MM | @username | |
| fao_food_price_index.csv | YYYY-MM-DD HH:MM | @username | |
| oecd_cpi_monthly.csv | YYYY-MM-DD HH:MM | @username | |
| imf_cpi_annual.csv | YYYY-MM-DD HH:MM | @username | |
| comtrade_ru_ua_exports.csv | YYYY-MM-DD HH:MM | @username | |
```

---

## トラブルシューティング

| 症状 | 対処 |
|------|------|
| `fetch_oecd_cpi.py` がタイムアウト | OECD API が混雑している。時間をおいて再試行 |
| `fetch_comtrade.py` が 403 エラー | `.env` の APIキーを確認。登録から反映まで数分かかる場合あり |
| `fetch_comtrade.py` が 429 エラー | 1日500リクエスト上限に達した。翌日再実行 |
| IMF API が空レスポンス | エンドポイント `PCPIPCH` は年次のみ。月次を期待しない |
| ノートブックの図が前回と違う | カーネルをリセットして最初から再実行する |
