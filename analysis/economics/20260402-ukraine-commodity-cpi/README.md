# ウクライナ侵攻と世界資源価格・物価変動

**分析タイプ:** 探索的分析（EDA）・記述的分析  
**ドメイン:** economics  
**期間:** 2020年1月〜2023年12月  
**ブランチ:** `analysis/economics/20260402-ukraine-commodity-cpi`

## リサーチクエスチョン

2022年のロシアによるウクライナ侵攻（2022年2月24日）の前後で、主要資源（原油・小麦・天然ガス）の国際価格はどのように変動したか。また同時期の消費者物価上昇率は世界各国でどのように異なるか。

## ディレクトリ構成

```
.
├── PROPOSAL.md          # 着手前チェックリスト（RQ・分析軸・データ取得計画）
├── README.md            # このファイル
├── decisions/           # ADR（分析手法選定記録）
├── data/
│   ├── raw/             # 取得したままのデータ（変更しない）
│   └── processed/       # 加工済みデータ
├── notebooks/
│   ├── 01_eda.ipynb     # 探索的分析（時系列・国際比較・地図）
│   └── 02_analysis.ipynb # 記述的分析・集計
├── outputs/
│   └── figures/         # 出力グラフ
└── REPORT.md            # 最終レポート
```

## データソース

| データ | 機関 | ライセンス | 取得方法 |
|--------|------|-----------|---------|
| Pink Sheet（原油・小麦・ガス月次） | World Bank | CC BY 4.0 | Excel 直接 DL |
| FAO Food Price Index（月次） | FAO | CC BY 4.0 | CSV 直接 DL |
| CPI 各国月次（OECD加盟国） | OECD | CC BY 4.0 | SDMX-JSON API |
| CPI 各国年次（OECD非加盟国補完） | IMF | IMF著作権・研究利用可 | DataMapper API |
| 輸出品目・輸出先（補助情報） | UN Comtrade | UN著作権・研究内部利用可 | comtradeapicall |

詳細（API エンドポイント・登録手順・レート制限）は `PROPOSAL.md` Sec 6 を参照。

## 環境セットアップ

```bash
pip install -r requirements.txt
```

`.env.example` をコピーして `.env` を作成し、UN Comtrade の API キーを設定:

```bash
cp .env.example .env
# .env に COMTRADE_API_KEY=your_key_here を記入
```

## ノートブックの実行順序

```
notebooks/01_eda.ipynb → notebooks/02_analysis.ipynb
```

各ノートブックはトップから順に実行することで再現できる。

## 注意事項

- `data/raw/` のデータは取得後に変更しない
- UN Comtrade の API キーを Git にコミットしない（`.gitignore` 済み）
- IMF データの加工結果を外部に再配布する場合は IMF 利用規約を再確認すること
