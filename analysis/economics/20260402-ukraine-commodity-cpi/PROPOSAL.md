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
| 月次 Excel 直接 DL | https://thedocs.worldbank.org/en/doc/74e8be41ceb20fa0da750cda2f6b9e4e-0050012026/related/CMO-Historical-Data-Monthly.xlsx |
| URL の注意 | URL はファイル更新のたびに変わる。取得時点のリンクをランディングページの "Monthly prices (XLS)" から取得して `SOURCES.md` に記録すること |
| ライセンス | CC BY 4.0 |
| ライセンス確認 URL | https://www.worldbank.org/en/about/legal/terms-of-use-for-datasets |
| 分析結果の公開 | **可**（帰属表示必須） |
| 判断根拠（原文引用） | "You are encouraged to use the Datasets to benefit yourself and others in creative ways. You may extract, download, and make copies of the data contained in the Datasets, and you may share that data with third parties." |
| 帰属表示フォーマット | `Source: The World Bank, Commodity Price Data (The Pink Sheet).` |
| 注意点 | World Bank が本分析を後援・承認していると示唆することは禁止。ファイルは毎月更新されるため取得日時を `data/raw/SOURCES.md` に記録すること |
| 取得方法 | Excel 直接ダウンロード |
| 認証・登録 | 不要 |
| 対象指標 | Brent（原油）・US HRW（小麦）・Europe（天然ガス TTF）の月次価格列 |
| 粒度 | 月次（1960年〜） |

### 6.2 FAO Food Price Index（食料価格指数）

| 項目 | 内容 |
|------|------|
| データ名 | FAO Food Price Index (FFPI) |
| 提供機関 | Food and Agriculture Organization of the United Nations (FAO) |
| ランディングページ | https://www.fao.org/worldfoodsituation/foodpricesindex/en/ |
| CSV 直接 DL | https://www.fao.org/media/docs/worldfoodsituationlibraries/default-document-library/food_price_indices_data.csv |
| ライセンス | CC BY 4.0 |
| ライセンス確認 URL | https://www.fao.org/contact-us/terms/db-terms-of-use/en/ |
| 分析結果の公開 | **可**（非商用目的・帰属表示必須） |
| 判断根拠（原文引用） | "All datasets disseminated through FAO corporate statistical databases...are licensed under the Creative Commons Attribution-4.0 International licence (CC BY 4.0)." |
| 帰属表示フォーマット | `FAO. [YYYY]. FAO Food Price Index. [Accessed on DD Month YYYY]. https://www.fao.org/worldfoodsituation/foodpricesindex/en/ Licence: CC-BY-4.0.` |
| 注意点 | **企業製品の販促目的での利用は不可**（"shall not be used for or in conjunction with the promotion of a commercial enterprise and/or its product(s)"）。ブログ・YouTube・GitHub での分析公開は問題なし |
| 取得方法 | CSV 直接ダウンロード（FAOSTAT API v1 は JWT 認証が必要なため不使用） |
| 認証・登録 | 不要 |
| 対象指標 | FFPI 総合・穀物・油脂・乳製品・肉・砂糖（月次） |
| 粒度 | 月次（1990年〜） |

### 6.3 OECD Stats CPI（OECD加盟国消費者物価）

| 項目 | 内容 |
|------|------|
| データ名 | Consumer Prices — OECD.SDD.TPS |
| 提供機関 | OECD |
| ライセンス | OECD 独自規約（CC BY ではない。Data セクション適用） |
| ライセンス確認 URL | https://www.oecd.org/en/about/terms-conditions.html (Sec 3. Data) |
| 分析結果の公開 | **可**（商用含む。ただしサードパーティ制限の確認が必要） |
| 判断根拠（原文引用） | "Except where additional restrictions apply as stated above, you can extract from, download, copy, adapt, print, distribute, share and embed Data for any purpose, even for commercial use." ただし同条件に: "Data may be subject to restrictions beyond the scope of these Terms and Conditions, either because specific terms apply to those Data or because third parties may have ownership interests. It is the user's responsibility to verify...whether the Data is fully or partially owned by third parties." |
| 帰属表示フォーマット | 規約上の明示義務はないが慣行として記載: `Source: OECD, Consumer Prices (MEI), https://stats.oecd.org/` |
| **要確認事項** | OECD Stats の CPI データが第三者所有データを含まないか、データのメタデータまたは「source」タブで確認すること（取得時に記録） |
| 取得方法 | SDMX-JSON API v2 |
| API エンドポイント | `https://sdmx.oecd.org/public/rest/v2` |
| データフロー | `OECD.SDD.TPS,DSD_PRICES@DF_PRICES_ALL` |
| クエリ（11カ国・月次） | `https://sdmx.oecd.org/public/rest/v2/data/dataflow/OECD.SDD.TPS/DSD_PRICES@DF_PRICES_ALL/1.0/DEU+FRA+ITA+POL+TUR+USA+GBR+CAN+AUS+JPN+KOR.M.N.CPI.IX._T.N.GY?startPeriod=2020-01&endPeriod=2023-12&format=jsondata` |
| クエリ補足 | 次元順: REF_AREA.FREQ.METHODOLOGY.MEASURE.UNIT_MEASURE.EXPENDITURE.ADJUSTMENT.TRANSFORMATION。**レート制限で動作未確認。スクリプト実装時に要検証** |
| 認証・登録 | 不要 |
| 対象国 | DEU・FRA・ITA・POL・TUR・USA・GBR・CAN・AUS・JPN・KOR |
| 粒度 | 月次 |

### 6.4 IMF CPI（OECD非加盟国補完）

| 項目 | 内容 |
|------|------|
| データ名 | IMF DataMapper — PCPIPCH（Consumer Price Index） |
| 提供機関 | International Monetary Fund (IMF) |
| ライセンス | IMF 独自著作権。統計データには General Terms とは別の特別条項（"The Use of IMF Data"）が適用される |
| ライセンス確認 URL | https://www.imf.org/en/about/copyright-and-terms ("The Use of IMF Data" セクション) |
| 分析結果の公開 | **可**（非商用。帰属表示・変換の明示が必須） |
| 判断根拠（原文引用） | Data 特別条項: "You may download, extract, copy, create derivative works, publish, distribute, and use Data obtained from IMF Sites, subject to the following conditions: Whether obtained directly from the IMF or another party, when Data is distributed or reproduced in any manner, it must appear accurately with attribution to the IMF as the source. ...If the Data is materially transformed by the User, this must be stated explicitly along with the required source citation." 商用利用: "For any potential commercial reuse of IMF Data, please email copyright@imf.org to request permission." |
| 帰属表示フォーマット | `Source: International Monetary Fund, International Financial Statistics, https://data.imf.org/` |
| 注意点 | **商用利用は要問い合わせ** (copyright@imf.org)。本分析はブログ・YouTube・GitHub での非商用の学習・研究目的であり、Data 特別条項の "publish, distribute, and use" に該当すると判断する。データを加工・集計している場合はその旨を成果物に明示すること |
| API エンドポイント | `https://www.imf.org/external/datamapper/api/v1/PCPIPCH/EGY/NGA/IND/CHN/SAU` |
| 認証・登録 | 不要 |
| 対象国 | EGY・NGA・IND・CHN・SAU |
| 粒度 | 年次 |

### 6.5 UN Comtrade（輸出品目・輸出先）— **本分析では不使用**

| 項目 | 内容 |
|------|------|
| データ名 | UN Comtrade Database |
| 提供機関 | United Nations Statistics Division |
| URL | https://comtradeplus.un.org/ |
| 開発者ポータル | https://comtradedeveloper.un.org/ |
| ライセンス | UN 著作権（CC BY ではない） |
| ライセンス確認 URL | https://comtrade.un.org/licenseagreement.html |
| 分析結果の公開 | **要確認**（データそのものの再配布は明示禁止。加工済み分析結果の公開は規約上グレーゾーン） |
| 判断根拠（原文引用） | "copying, automated browsing or downloading, redistribution, publication, or commercial exploitation of any material...is strictly prohibited." および "Re-dissemination means re-using UN Comtrade data as is (without any transformation) in other data platforms (printed or online), not for internal use." |
| 使用状況 | **本分析では使用しない。** 加工済みグラフの公開可否が規約上グレーゾーンのため除外。初版完成後に comtrade@un.org へ許可を問い合わせ、承認が得られた場合に補足として追加する (makinzm/data-report#3) |
| 取得方法 | `comtradeapicall` ライブラリ (`uv add comtradeapicall`) |
| 認証 | **無料 API キー必須** (comtradeplus.un.org でアカウント作成 → 開発者ポータルで `comtrade - v1` を Subscribe) |
| レート制限 | 1日500リクエスト上限（無料プラン） |
| APIキー管理 | `.env` ファイルで管理。`.gitignore` 済み |
| 対象データ | ロシア・ウクライナの原油・小麦・天然ガス輸出先構成（HS コード別・年次） |
| 粒度 | 年次 |

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

### 2.1 ライセンス確認
- [x] 各データソースのライセンス種別を記載している（Sec 6）
- [x] ライセンス原文を引用し、判断根拠 URL を記載している（Sec 6 各項）
- [x] 分析結果（グラフ・レポート・動画）の公開可否を判断している（Sec 6 各項）
- [x] 「データそのものの再配布」と「加工済み分析結果の公開」を区別して判断している
- [x] UN Comtrade はライセンスがグレーゾーンのため本分析から除外。初版完成後に問い合わせ予定（makinzm/data-report#3）
