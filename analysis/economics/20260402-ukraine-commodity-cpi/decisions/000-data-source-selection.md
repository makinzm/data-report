# ADR-000: データソース選定とナビゲーション記録

## ステータス
In Progress — OECD・IMF は仕様書確認が不完全。要確認事項あり。

## コンテキスト

ウクライナ侵攻前後の資源価格・各国 CPI を探索的に分析するにあたり、
以下の基準でデータソースを選定した。

- オープンデータであること
- 月次データが得られること（CPI の一部は年次で代替）
- 分析結果を非商用で公開できること
- 2020年〜2023年の期間をカバーすること

---

## 1. World Bank Commodity Price Data (Pink Sheet)

### なぜこれを選んだか

原油・小麦・天然ガスの国際価格を一つのソースで月次取得できる。
他の選択肢（EIA、IMF PCPS）と比較したとき、World Bank は
Brent 原油・US HRW 小麦・欧州 TTF ガスの3つを同一ファイルで提供しており、
データ整合性の担保が容易。

### 公式ドキュメントの場所

- ランディングページ: https://www.worldbank.org/en/research/commodity-markets
- データの説明・方法論: **要確認** — Pink Sheet 自体に方法論ドキュメントのリンクがあるが未読。読んでおくべき。

### データへのたどり着き方

1. 上記ランディングページを開く
2. "Historical Data" セクションの "Monthly Prices" Excel リンクをクリック
3. 直接 URL: `https://thedocs.worldbank.org/en/doc/18675f1d1639c7a34d463f59263ba0a2-0050012025/related/CMO-Historical-Data-Monthly.xlsx`

### ダウンロードコマンドと保存先

```bash
# 保存先: data/raw/pinksheet_monthly.xlsx
curl -L -o data/raw/pinksheet_monthly.xlsx \
  "https://thedocs.worldbank.org/en/doc/18675f1d1639c7a34d463f59263ba0a2-0050012025/related/CMO-Historical-Data-Monthly.xlsx"
```

取得後、`data/raw/SOURCES.md` に取得日時を記録する。

### メタデータの確認先

- Excel ファイル内の "Notes" シートに指標の定義・出典が記載されている
- **要確認** — Notes シートの内容をまだ読んでいない。取得後に読んで記録する

### 未解決事項

- [ ] Excel の Notes シートを読み、各指標（Brent・HRW・TTF）の定義・単位・出典を確認する

---

## 2. FAO Food Price Index (FFPI)

### なぜこれを選んだか

食料価格（穀物・油脂・乳製品・肉・砂糖）をサブ指数込みで月次提供している
唯一の国際機関ソース。ウクライナはひまわり油・小麦の主要輸出国であり、
FAO 指数はこれらを含む食料価格全体の動向を把握するのに適している。

### 公式ドキュメントの場所

- ランディングページ: https://www.fao.org/worldfoodsituation/foodpricesindex/en/
- 方法論ドキュメント: **要確認** — ランディングページに方法論リンクがあるはずだが未読。
  「How is the FAO Food Price Index calculated?」の記述を確認すべき

### データへのたどり着き方

1. 上記ランディングページを開く
2. "Download data" リンクから CSV を取得
3. 安定 URL（月名なし）: `https://www.fao.org/media/docs/worldfoodsituationlibraries/default-document-library/food_price_indices_data.csv`

### ダウンロードコマンドと保存先

```bash
# 保存先: data/raw/fao_food_price_index.csv
curl -L -o data/raw/fao_food_price_index.csv \
  "https://www.fao.org/media/docs/worldfoodsituationlibraries/default-document-library/food_price_indices_data.csv"
```

取得後、`data/raw/SOURCES.md` に取得日時を記録する。

### メタデータの確認先

- CSV の列定義はランディングページの説明文に記載
- **要確認** — 基準年（2014-16=100）の意味と各サブ指数の計算方法を方法論文書で確認する

### 未解決事項

- [ ] 方法論ドキュメントを読み、各サブ指数の品目構成・ウェイトを確認する
- [ ] CSV の列名と実際の指標の対応を記録する

---

## 3. OECD Stats CPI

### なぜこれを選んだか

OECD 加盟国（G7・欧州主要国・日韓）の月次 CPI を一つの API で取得できる。
各国の国家統計局データを集約・標準化しており、国際比較に適している。

### 公式ドキュメントの場所

- SDMX REST v2 仕様（OECD 固有）: **要確認** — 以下を読む必要がある
  - https://data.oecd.org/api/sdmx-json-documentation/
  - https://www.oecd.org/en/data/insights/data-explainers/2024/09/api.html
- SDMX 標準仕様（一般）: https://github.com/sdmx-twg/sdmx-rest/blob/master/doc/data.md

### データへのたどり着き方

1. OECD Data Explorer ( https://data-explorer.oecd.org/ ) を開く
2. "Prices" → "Consumer Prices" を選択
3. 国・指標・期間を選択後、「Developer API」アイコンからクエリ URL を取得する
   （**これが本来の正しいたどり着き方。仕様書から推測ではなく UI からクエリを生成すべきだった**）

### メタデータの確認先

- データ構造定義 (DSD):
  `https://sdmx.oecd.org/public/rest/v2/structure/datastructure/OECD.SDD.TPS/DSD_PRICES?references=all`
- 次元・コードリストはこの DSD を読めば確認できる
- **現状** — DSD は調査済みで次元構造は把握した（REF_AREA.FREQ.METHODOLOGY.MEASURE.UNIT_MEASURE.EXPENDITURE.ADJUSTMENT.TRANSFORMATION）
  ただし OECD Data Explorer でクエリを生成して正とする

### ダウンロードコマンドと保存先

**クエリ URL は OECD Data Explorer で生成してから記入すること（以下は未確定）:**

```bash
# 保存先: data/raw/oecd_cpi_monthly.json
# ※ URL は Data Explorer で生成した正式なものに差し替える
curl -L -o data/raw/oecd_cpi_monthly.json \
  "<OECD Data Explorer で生成した URL>"
```

取得後、`data/raw/SOURCES.md` に取得日時と使用した URL を記録する。

### クエリの現状と問題

以下のクエリは**まだ動作未確認**（ユーザーに確認をお願いしている）:

```
https://sdmx.oecd.org/public/rest/data/OECD.SDD.TPS,DSD_PRICES@DF_PRICES_ALL/DEU+FRA+ITA+POL+TUR+USA+GBR+CAN+AUS+JPN+KOR.M.N.CPI.PA._T.N.GY/?startPeriod=2020-01&endPeriod=2023-12&format=jsondata
```

- `startPeriod`/`endPeriod` の使用可否が OECD 実装で未確定
- TUR のコードが `TUR` で正しいか未確認

### 未解決事項

- [ ] OECD Data Explorer で国・指標・期間を選択し、正式なクエリ URL を生成して記録する（上記コマンドの URL を差し替える）
- [ ] 上記クエリの動作を確認する（ユーザー確認待ち）
- [ ] TUR（トルコ）が CL_AREA に存在するか確認する

---

## 4. IMF DataMapper（OECD 非加盟国 CPI 補完）

### なぜこれを選んだか

エジプト・ナイジェリア・インド・中国・サウジアラビアは OECD 非加盟で
OECD Stats から取得できない。IMF は世界 190 カ国以上の CPI データを
提供しており、非加盟国の補完として使用する。ただし年次データのみ。

### 公式ドキュメントの場所

- API ドキュメント: https://www.imf.org/external/datamapper/api/help
- DataMapper UI: https://www.imf.org/external/datamapper/
- **要確認** — API ドキュメントをまだ通読していない。読んで記録する

### データへのたどり着き方

1. DataMapper UI ( https://www.imf.org/external/datamapper/ ) を開く
2. "Inflation rate, average consumer prices" (PCPIPCH) を選択
3. 対象国を選択して API URL を確認する
4. または直接: `https://www.imf.org/external/datamapper/api/v1/PCPIPCH/EGY/NGA/IND/CHN/SAU`

### ダウンロードコマンドと保存先

```bash
# 保存先: data/raw/imf_cpi_annual.json
curl -L -o data/raw/imf_cpi_annual.json \
  "https://www.imf.org/external/datamapper/api/v1/PCPIPCH/EGY/NGA/IND/CHN/SAU"
```

取得後、`data/raw/SOURCES.md` に取得日時を記録する。

### メタデータの確認先

- 指標定義: `https://www.imf.org/external/datamapper/api/v1/indicators/PCPIPCH`
- **要確認** — PCPIPCH の定義（年平均か期末か）・計算方法を上記で確認する
- OECD の "Percent per annum" と IMF の PCPIPCH が同じ定義か確認が必要

### 未解決事項

- [ ] API ドキュメント ( https://www.imf.org/external/datamapper/api/help ) を読む
- [ ] PCPIPCH の定義を確認し、OECD CPI との比較可能性を検証する
- [ ] 対象5カ国のデータが 2020〜2023 年分存在するか確認する

---

## 選定しなかったソースと理由

| ソース | 選定しなかった理由 |
|--------|-----------------|
| EIA（原油・ガス価格） | World Bank Pink Sheet が同じデータを含み、小麦も同一ファイルで取得できるため |
| UN Comtrade（貿易統計） | ライセンスがグレーゾーン。初版完成後に問い合わせ予定 (makinzm/data-report#3) |
| Our World in Data | 元データの出典が上記機関と重複するため、一次ソースを直接使う |
| 各国国家統計局 | 国ごとに API・フォーマットが異なり統一取得が困難 |
