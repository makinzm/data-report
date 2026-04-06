"""ページ3: 価格 vs 貿易量 — 国際価格と世界輸出総量の散布図"""

import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent))
from components.data_loader import load_baci, get_filtered, COMMODITY_MAP
from components.filters import render_sidebar

st.set_page_config(page_title="価格 vs 貿易量", page_icon="💹", layout="wide")
st.title("💹 価格 vs 貿易量")

# --- World Bank Pink Sheet の読み込み ---
PINK_SHEET_PATH = (
    Path(__file__).parent.parent.parent.parent
    / "20260402-ukraine-commodity-cpi"
    / "data"
    / "raw"
    / "CMO-Historical-Data-Monthly.xlsx"
)

# 価格データが利用可能な商品と列名のマッピング（Pink Sheet の列名）
PRICE_COL_MAP: dict[str, str] = {
    "1001": "Wheat, US HRW",       # 小麦
    "2709": "Crude oil, Brent",    # 原油
    "2701": "Coal, Australia",     # 石炭
}


@st.cache_data(show_spinner=False)
def load_pink_sheet_annual() -> pd.DataFrame:
    """Pink Sheet から年平均価格を返す"""
    if not PINK_SHEET_PATH.exists():
        return pd.DataFrame()
    xls = pd.read_excel(PINK_SHEET_PATH, sheet_name="Monthly Prices", header=4, index_col=0)
    xls.index = pd.to_datetime(xls.index, errors="coerce")
    xls = xls.dropna(how="all")
    xls["year"] = xls.index.year
    annual = xls.groupby("year").mean(numeric_only=True)
    return annual


# --- データ読み込み ---
with st.spinner("データを読み込み中..."):
    baci = load_baci()
    pink = load_pink_sheet_annual()

available_years = sorted(baci["year"].unique().tolist())
filters = render_sidebar(available_years)

hs4 = filters["hs4"]
commodity_label = filters["commodity_label"]

# 価格データが使えるか確認
if hs4 not in PRICE_COL_MAP:
    st.info(
        f"**{commodity_label}** の価格データ（World Bank Pink Sheet）が利用できません。\n\n"
        "価格データが利用可能な商品: " +
        ", ".join(COMMODITY_MAP[k] if k in COMMODITY_MAP else k
                  for k in PRICE_COL_MAP) +
        "\n\n※ 小麦・原油・石炭のいずれかを選択してください。"
    )
    st.stop()

price_col = PRICE_COL_MAP[hs4]
if pink.empty or price_col not in pink.columns:
    st.warning("Pink Sheet データが見つかりません。`20260402-ukraine-commodity-cpi/data/raw/` を確認してください。")
    st.stop()

# --- 集計 ---
df = get_filtered(baci, hs4, filters["year_range"])
world_export = (
    df.groupby("year")["value_kusd"].sum().reset_index()
    .rename(columns={"value_kusd": "world_export_kusd"})
)

price_series = pink[[price_col]].copy()
price_series.index.name = "year"
price_series = price_series.reset_index()
price_series.columns = ["year", "price"]

merged = world_export.merge(price_series, on="year", how="inner")
merged["world_export_busd"] = merged["world_export_kusd"] / 1e6  # → 十億 USD

# --- 散布図 ---
fig = px.scatter(
    merged,
    x="price",
    y="world_export_busd",
    text="year",
    trendline="ols",
    title=f"{commodity_label} — 年平均価格 vs 世界輸出総額",
    labels={
        "price": f"年平均価格 ({price_col})",
        "world_export_busd": "世界輸出総額（十億 USD）",
        "year": "年",
    },
)
fig.update_traces(textposition="top center")
fig.update_layout(height=500)
st.plotly_chart(fig, use_container_width=True)

# --- 時系列の並列表示 ---
col1, col2 = st.columns(2)
with col1:
    fig2 = px.line(
        merged, x="year", y="price", markers=True,
        title="年平均価格の推移",
        labels={"year": "年", "price": "価格"},
    )
    if 2022 in merged["year"].values:
        fig2.add_vline(x=2022, line_dash="dash", line_color="red",
                       annotation_text="2022侵攻")
    st.plotly_chart(fig2, use_container_width=True)

with col2:
    fig3 = px.line(
        merged, x="year", y="world_export_busd", markers=True,
        title="世界輸出総額の推移",
        labels={"year": "年", "world_export_busd": "十億 USD"},
    )
    if 2022 in merged["year"].values:
        fig3.add_vline(x=2022, line_dash="dash", line_color="red",
                       annotation_text="2022侵攻")
    st.plotly_chart(fig3, use_container_width=True)

st.caption(
    "価格: World Bank Commodity Price Data (The Pink Sheet). Source: The World Bank. "
    "貿易量: BACI International Trade Database, CEPII (Licence Etalab 2.0)."
)
