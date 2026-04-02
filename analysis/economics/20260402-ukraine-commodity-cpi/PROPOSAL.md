# PROPOSAL: ウクライナ侵攻と世界資源価格・物価変動

作成日: 2026-04-02
分析ディレクトリ: `analysis/economics/20260402-ukraine-commodity-cpi/`

---

## 1. リサーチクエスチョン

2022年のロシアによるウクライナ侵攻（2022年2月24日）の前後で、主要資源（原油・小麦・天然ガス）の国際価格はどのように変動したか。また同時期の消費者物価上昇率は世界各国でどのように異なるか。

具体的に答えたい問い：
- 侵攻前後（2021年1月〜2023年12月）の原油・小麦・天然ガス価格のピーク時期・規模・収束速度はどうだったか
- CPI 上昇率の大きさは国・地域によってどのように異なるか（欧州 vs アジア vs アフリカなど）

---

## 2. 動機・背景

### 誰が何を得るか

- 地政学リスクと実体経済の関係を学ぶ学習者・研究者が、データに基づいた事実整理を得られる
- 政策立案・報道・教育の場で「侵攻がどの程度・どの地域に影響したか」を定量的に参照できる素材となる

### 社会的意義

2022年のウクライナ侵攻は、ロシア・ウクライナが原油・天然ガス・小麦の主要供給国であることから、資源価格の急騰を引き起こした。この価格ショックは各国の CPI に波及したが、エネルギー自給率・輸入依存度・補助金政策の差により影響は国ごとに大きく異なると考えられる。侵攻から約4年が経過した現在、データを整理して事実を記録することは歴史的にも意義がある。

---

## 3. 分析タイプの明示

**本分析は探索的分析（EDA）および記述的分析のみである。**

- 因果推論・仮説検証（CDA）は対象外
- 「侵攻が CPI 上昇を引き起こした」という因果関係の証明は行わない
- 時系列の推移・規模・国際比較をデータで可視化・記述することが目的

---

## 4. 事前登録（分析軸の固定）

EDA・記述分析であるため、p-hacking 防止のため「見る指標・期間・対象」をここに事前固定する。
分析開始後に都合の良い指標・期間・国を後付けで追加しない。

### 4.1 見る指標（変数）

| カテゴリ | 指標 | 単位 | データソース |
|---------|------|------|------------|
| 資源価格 | 原油価格（Brent） | USD/バレル（月次） | World Bank Pink Sheet |
| 資源価格 | 小麦価格（US HRW） | USD/トン（月次） | World Bank Pink Sheet |
| 資源価格 | 天然ガス価格（TTF欧州） | USD/MMBtu（月次） | World Bank Pink Sheet |
| 食料価格 | FAO食料価格指数（総合・穀物・油脂・乳製品・肉・砂糖） | 指数（2014-16=100）（月次） | FAO |
| 消費者物価 | CPI 前年同月比（国別） | %（月次） | OECD Stats / IMF |

### 4.2 対象期間

**2020年1月〜2023年12月（48ヶ月）**

- 侵攻前の基準期間として2020-2021年、侵攻後として2022-2023年を含む
- COVID-19の影響（2020年）も含めることで、資源価格変動の文脈を把握する
- この期間設定はデータ取得前に固定する

### 4.3 対象国・地域

CPI 比較の対象国を以下に事前固定する（データ取得後に国を追加しない）：

**OECD加盟国グループ（OECD Stats から取得）:**
- 欧州: ドイツ・フランス・イタリア・ポーランド・トルコ
- 英語圏: アメリカ・イギリス・カナダ・オーストラリア
- アジア: 日本・韓国

**OECD非加盟国グループ（IMF CPI から取得）:**
- アフリカ: エジプト・ナイジェリア
- アジア: インド・中国
- 中東: サウジアラビア

計17カ国を固定。分析中にこのリストを変更する場合は変更理由を記録すること。

### 4.4 見る可視化・集計の軸（事前固定）

1. 各資源価格の月次推移（時系列折れ線グラフ）— 侵攻日に縦線マーカーを入れる
2. 侵攻前後の価格変化率（侵攻月を基準とした%変化）
3. 各国 CPI 前年同月比の時系列推移（国別・地域グループ別）
4. 侵攻ピーク月（2022年6月前後）における各国 CPI 水準の比較（棒グラフ）
5. FAO 食料価格指数の時系列推移（サブ指数含む）

---

## 5. スコープ

### 対象

- 期間: 2020年1月〜2023年12月
- 資源: 原油（Brent）・小麦（US HRW）・天然ガス（TTF欧州）
- 食料価格指数: FAO 総合・サブ指数
- CPI: 上記17カ国の月次前年同月比
- 分析タイプ: 記述統計・時系列可視化・国際比較

### 対象外（スコープ外の明示）

- 因果推論・反事実分析（「侵攻がなければ CPI は〜だった」は対象外）
- 個別国の金融政策・財政政策の効果分析
- 資源価格と CPI の計量経済的回帰分析・Granger 因果性検定（本分析では行わない）
- 株式市場・為替市場への影響
- 天然ガス以外のエネルギー（石炭・電力）
- 2024年以降のデータ（ロシア・ウクライナ停戦交渉期）

---

## 6. データ取得計画

### 6.1 World Bank Pink Sheet（原油・小麦・天然ガス月次価格）

| 項目 | 内容 |
|------|------|
| データ名 | Commodity Price Data (The Pink Sheet) |
| 提供機関 | World Bank |
| ランディングページ | https://thedocs.worldbank.org/en/doc/18675f1d1639c7a34d463f59263ba0a2-0050012025/world-bank-commodities-price-data-the-pink-sheet |
| 月次 Excel 直接 DL | https://thedocs.worldbank.org/en/doc/18675f1d1639c7a34d463f59263ba0a2-0050012025/related/CMO-Historical-Data-Monthly.xlsx |
| ライセンス | CC BY 4.0 |
| 取得方法 | Excel 直接ダウンロード（最も確実）。DataBank API は個別指標コードの公式ドキュメントが不明のため Excel を使用する |
| 認証方式 | 不要 |
| 登録の要否 | 不要 |
| レート制限 | なし |
| 対象指標 | Brent（原油）・US HRW（小麦）・Europe（天然ガス TTF）の月次価格列 |
| 粒度 | 月次（1960年〜） |
| 利用注意点 | 商用利用可。引用時は World Bank を出典として明記。ファイルは毎月更新されるため取得日時を `data/raw/` の README に記録すること |

### 6.2 FAO Food Price Index（食料価格指数）

| 項目 | 内容 |
|------|------|
| データ名 | FAO Food Price Index (FFPI) |
| 提供機関 | Food and Agriculture Organization of the United Nations (FAO) |
| ランディングページ | https://www.fao.org/worldfoodsituation/foodpricesindex/en/ |
| CSV 直接 DL | https://www.fao.org/media/docs/worldfoodsituationlibraries/default-document-library/food_price_indices_data_csv_mar.csv |
| ライセンス | CC BY 4.0 |
| 取得方法 | CSV 手動ダウンロード。FAOSTAT API v1 は JWT 認証が必要なため、CSV 直接取得を使用する |
| 認証方式 | 不要（CSV 直接 DL） |
| 登録の要否 | 不要 |
| レート制限 | なし |
| 対象指標 | FFPI 総合・穀物（Cereals）・油脂（Oils）・乳製品（Dairy）・肉（Meat）・砂糖（Sugar） |
| 粒度 | 月次（1990年〜） |
| 利用注意点 | 商用利用可。引用時は FAO を出典として明記。CSV のファイル名に月名が含まれるため取得日時を記録すること |

### 6.3 OECD Stats CPI（OECD加盟国消費者物価）

| 項目 | 内容 |
|------|------|
| データ名 | Consumer Prices — OECD.SDD.TPS |
| 提供機関 | OECD |
| API ドキュメント | https://data.oecd.org/api/sdmx-json-documentation/ |
| SDMX v2 エンドポイント | `https://sdmx.oecd.org/public/rest/v2` |
| データフロー | `OECD.SDD.TPS,DSD_PRICES@DF_PRICES_ALL` |
| クエリ例（DEU 月次 2020-2023） | `https://sdmx.oecd.org/public/rest/data/OECD.SDD.TPS,DSD_PRICES@DF_PRICES_ALL/DEU.M.GY.CPI.IX._T.N.?startPeriod=2020-01&endPeriod=2023-12&format=jsondata` |
| ライセンス | CC BY 4.0 |
| 取得方法 | SDMX-JSON API（`requests` + `pandas` で取得可能） |
| 認証方式 | APIキー不要 |
| 登録の要否 | 不要 |
| レート制限 | 記載なし（過度なリクエストは避ける） |
| 対象指標 | CPI 前年同月比（`GY` = growth rate year-on-year） |
| 対象国 | DEU・FRA・ITA・POL・TUR・USA・GBR・CAN・AUS・JPN・KOR |
| 粒度 | 月次 |
| 利用注意点 | 商用利用可。引用時は OECD を出典として明記。OECD Data Explorer でデータを選択後「Developer API」アイコンから正確なクエリを確認できる |

### 6.4 IMF CPI（OECD非加盟国補完）

| 項目 | 内容 |
|------|------|
| データ名 | International Financial Statistics (IFS) — Consumer Price Index |
| 提供機関 | International Monetary Fund (IMF) |
| URL | https://www.imf.org/en/Data |
| SDMX API ドキュメント | https://datahelp.imf.org/knowledgebase/articles/667681-using-json-restful-web-service |
| SDMX エンドポイント例 | `https://www.imf.org/external/datamapper/api/v1/PCPIPCH/EGY/NGA/IND/CHN/SAU` |
| ライセンス | IMF 著作権（研究・教育目的の非商用利用可、再配布には許可要） |
| 取得方法 | IMF DataMapper JSON API |
| 認証方式 | APIキー不要 |
| 登録の要否 | 不要 |
| レート制限 | 記載なし |
| 対象指標 | PCPIPCH（Inflation, end of period consumer prices, % change） |
| 対象国 | EGY（エジプト）・NGA（ナイジェリア）・IND（インド）・CHN（中国）・SAU（サウジアラビア） |
| 粒度 | 年次（月次データが入手困難な国の補完として使用） |
| 利用注意点 | **再配布は要許可**。本分析の成果物に IMF データの加工結果を公開する場合は IMF の利用規約を再確認すること。研究・学習目的の内部利用は可とみなされる。取得データは `data/raw/` に保管し、加工データのみ `data/processed/` に置く |

### 6.5 UN Comtrade（輸出品目・輸出先 — 補助情報）

| 項目 | 内容 |
|------|------|
| データ名 | UN Comtrade Database |
| 提供機関 | United Nations Statistics Division |
| URL | https://comtradeplus.un.org/ |
| 開発者ポータル | https://comtradedeveloper.un.org/ |
| ライセンス | UN 著作権（研究内部利用可、**再配布には許可要**） |
| 取得方法 | Python ライブラリ `comtradeapicall` を使用 |
| インストール | `pip install comtradeapicall` |
| 認証方式 | **無料 API キー登録必須**（`comtradeplus.un.org` でアカウント作成 → 開発者ポータルで `comtrade - v1` プロダクトを選択） |
| 登録先 | https://comtradeplus.un.org/ |
| レート制限 | **1日500リクエスト上限**（無料プラン）。`previewFinalData`（500件・キー不要）と `getFinalData`（フル取得・キー必要）の2種類あり |
| 対象データ | ロシア・ウクライナの原油・小麦・天然ガス輸出先構成（HS コード別・年次） |
| 粒度 | 年次 |
| 利用注意点 | **再配布要許可**。APIキーは `.env` ファイルで管理し `.gitignore` に追加すること。1日500リクエスト上限のため取得結果を `data/raw/` にキャッシュして再利用する。本分析では補助情報（背景地図の輸出依存度表示）として使用し、主要時系列分析には含めない |

---

## 7. DoD Sec 1 自己チェック

### 1.1 リサーチクエスチョン
- [x] 分析で答えたい問いを1〜2文で明示している
- [x] 問いは「どれくらい」「どのように異なるか」など、答えられる形になっている
- [x] 「手法を試したい」「なんとなく面白そう」が動機になっていない（地政学的事実の記録が動機）

### 1.2 動機・背景
- [x] この問いに答えることで誰が何を得るか書いている（学習者・研究者・政策立案者）
- [x] 社会的意義を書いている（ウクライナ侵攻の経済的影響の定量的記録）

### 1.3 事前登録（EDA・記述分析のため分析軸を登録）
- [x] 見る指標・変数を事前に列挙している（Sec 4.1）
- [x] 対象期間・地域・集団を固定している（2020-2023年、17カ国、Sec 4.2-4.3）
- [x] 「結果を見てから都合の良い軸を選ぶ」余地を排除している（Sec 4.4 で可視化軸も固定）

### 1.4 スコープ
- [x] 分析対象の期間・地域・集団などを明示している
- [x] 答えない問い・対象外事項も書いている（因果推論・回帰分析・2024年以降など）
