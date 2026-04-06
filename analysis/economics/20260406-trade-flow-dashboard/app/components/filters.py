"""サイドバーフィルター（全ページ共通）"""

import streamlit as st
from .data_loader import COMMODITY_MAP


def render_sidebar(available_years: list[int]) -> dict:
    """
    サイドバーにフィルターを描画し、選択値を dict で返す。

    Returns:
        {
            "commodity_label": str,  # 表示名
            "hs4": str,              # HS4コード
            "year_range": (int, int),
            "metric": str,           # "value_kusd" or "qty_kton"
            "flow": str,             # "export" or "import"
        }
    """
    st.sidebar.header("フィルター")

    commodity_label = st.sidebar.selectbox(
        "商品",
        list(COMMODITY_MAP.keys()),
        index=0,
    )
    hs4 = COMMODITY_MAP[commodity_label]

    min_y, max_y = min(available_years), max(available_years)
    year_range = st.sidebar.slider(
        "対象期間",
        min_value=min_y,
        max_value=max_y,
        value=(min_y, max_y),
        step=1,
    )

    metric = st.sidebar.radio(
        "指標",
        ["貿易額（千 USD）", "貿易量（千トン）"],
        index=0,
    )
    metric_col = "value_kusd" if metric == "貿易額（千 USD）" else "qty_kton"

    flow = st.sidebar.radio(
        "フロー",
        ["輸出", "輸入"],
        index=0,
    )
    flow_key = "export" if flow == "輸出" else "import"

    return {
        "commodity_label": commodity_label,
        "hs4": hs4,
        "year_range": year_range,
        "metric": metric_col,
        "metric_label": metric,
        "flow": flow_key,
        "flow_label": flow,
    }
