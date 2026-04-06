# ADR-000: データソースの選定（BACI）

## ステータス
Accepted

## コンテキスト
- 世界の貿易フロー（輸出/輸入の相手国・量・額）を国別・商品別に可視化したい
- 分析結果（グラフ）を YouTube・GitHub で公開する予定がある
- 当初 UN Comtrade を直接利用する案があったが、利用規約が "redistribution, publication...is strictly prohibited" と明記しており、公開可否がグレーゾーンになる

## 選択肢

| ソース | ライセンス | 公開可否 | API/DL | 備考 |
|--------|---------|---------|--------|------|
| UN Comtrade | 独自規約（再配布禁止） | グレーゾーン | API キー必要 | 最も生に近いデータ |
| **BACI (CEPII)** | **Etalab 2.0** | **明確に可** | 直接 DL | Comtrade を CEPII が調和処理済み |
| ITC Trade Map | 独自規約 | 要確認 | 要ログイン | Comtrade ベース |
| World Bank WITS | CC BY 4.0 | 可 | API | Comtrade ベース。品目の柔軟性がやや低い |

## 決定
BACI (CEPII) を使用する。

## 理由
- Etalab 2.0 ライセンスにより、グラフ・分析結果の公開が帰属表示のもとで明確に許可される
- BACI は Comtrade 生データをそのまま使うのではなく、CIF/FOB 調整と報告信頼性の重み付けを施した調和済みデータであり、品質が高い
- API キー不要。ZIP ファイルを直接ダウンロードできる
- comtradeapicall ライブラリが不要になり、依存が減る

## トレードオフ・リスク
- BACI は年次データのみ。月次の分解能は得られない
- ダウンロードファイルが大きい（HS17 ZIP は数百 MB）。`data/raw/` を .gitignore に追加し、git 管理外とする
- 最新データが UN Comtrade より数ヶ月遅れる場合がある（v202601 時点で 2024 年分まで収録）

## 参照
- BACI ページ: http://www.cepii.fr/CEPII/en/bdd_modele/bdd_modele_item.asp?id=37
- Etalab 2.0 ライセンス: https://www.etalab.gouv.fr/wp-content/uploads/2018/11/open-licence.pdf
- 引用: Gaulier, G. and Zignago, S. (2010). BACI: International Trade Database at the Product-Level. CEPII Working Paper N°2010-23.

## 結果（実施後に記入）
- 想定通りだった点：
- 想定外だった点：
