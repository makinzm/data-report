# データ取得記録

データを取得したらこの表を埋めること（再現性確保）。

| ファイル名 | 取得日時 (JST) | 取得者 | 備考 |
|-----------|--------------|-------|------|
| pinksheet_monthly.xlsx | 2026-04-05 | makinzm | World Bank Pink Sheet 月次。ランディングページ (https://www.worldbank.org/en/research/commodity-markets) の "Monthly prices (XLS)" リンクから手動ダウンロード。URL は年次更新のためページから都度コピーすること |
| fao_food_price_index.csv | 2026-04-05 | Claude | FAO FFPI 月次。ベース URL は安定。439行 |
| oecd_cpi_monthly.csv | 2026-04-05 | Claude | OECD SDMX v1 API。DEU+FRA+ITA+POL+TUR+USA+GBR+CAN+AUS(除く)+JPN+KOR。2020-01〜2023-12。403行 |
| oecd_cpi_aus_quarterly.csv | 2026-04-05 | Claude | OECD SDMX v1 API。AUS のみ四半期（月次データなし）。2020-Q1〜2023-Q4。17行 |
| imf_cpi_annual.json | 2026-04-05 | Claude | IMF DataMapper API。OECD 非加盟国 (CHN/EGY/IND/NGA/SAU)。年次 1981〜2030 |
| (comtrade — 使用しない) | — | — | ライセンス確認中。makinzm/data-report#3 参照 |
