# RUNBOOK

## 前提

- Python >= 3.13、uv がインストール済みであること
- このディレクトリで全コマンドを実行する

```bash
cd analysis/economics/20260406-trade-flow-dashboard
uv sync
```

## Step 1: BACI データのダウンロード

```bash
uv run python scripts/download_baci.py
```

- ダウンロード先: `data/raw/BACI_HS17_V202601.zip`（約 400–600 MB）
- 自動ダウンロードが失敗した場合は、以下から手動ダウンロードして `data/raw/` に配置:
  http://www.cepii.fr/CEPII/en/bdd_modele/bdd_modele_item.asp?id=37
  → HS17 (2017-2024) を選択

## Step 2: データ処理（Parquet 変換）

```bash
uv run python scripts/process_baci.py
```

- 出力: `data/processed/baci_filtered.parquet`（対象 9 商品のみ）
- 出力: `data/processed/country_codes.parquet`（国コードマッピング）

## Step 3: ダッシュボード起動

```bash
uv run streamlit run app/app.py
```

ブラウザで http://localhost:8501 が開く。

## データ更新（BACI 新バージョンが出た場合）

1. CEPII のページで最新バージョンを確認
2. `scripts/download_baci.py` の `BACI_URL` を更新
3. Step 1–2 を再実行

## 注意事項

- `data/raw/` と `data/processed/` は `.gitignore` で除外済み。各自で処理を実行すること
- BACI ライセンス: Etalab 2.0。グラフ・分析結果の公開は帰属表示のもとで可
- 帰属表示: "Source: BACI International Trade Database, CEPII (Licence Etalab 2.0)."
