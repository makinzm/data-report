"""
世界貿易フロー可視化ダッシュボード
エントリポイント

Usage:
    uv run streamlit run app/app.py
"""

import streamlit as st

st.set_page_config(
    page_title="世界貿易フロー ダッシュボード",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🌍 世界貿易フロー可視化ダッシュボード")
st.markdown(
    """
    主要農産品・エネルギー商品・金属の**輸出/輸入フロー**をインタラクティブに探索します。

    **データソース**: BACI International Trade Database, CEPII (Licence Etalab 2.0)

    左のサイドバーからページを選択してください:

    | ページ | 内容 |
    |--------|------|
    | 📈 時系列 | 国別の輸出/輸入量・額の年次推移 |
    | 🔀 Sankey | 輸出国→輸入国のフロー図（選択年） |
    | 💹 価格 vs 貿易量 | 国際価格と世界輸出総量の関係 |
    | 🗺️ 地図 | 国別の輸出額/輸入額のコロプレス |
    """
)

st.divider()
st.caption(
    "Source: BACI International Trade Database, CEPII (Licence Etalab 2.0). "
    "Gaulier, G. and Zignago, S. (2010). BACI: International Trade Database at the Product-Level. "
    "CEPII Working Paper N°2010-23."
)
