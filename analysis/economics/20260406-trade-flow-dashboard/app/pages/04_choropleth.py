"""ページ4: Choropleth — 国別の輸出額/輸入額の地図"""

import sys
from pathlib import Path

import plotly.express as px
import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent))
from components.data_loader import load_baci, load_country_codes, get_filtered
from components.filters import render_sidebar

st.set_page_config(page_title="地図", page_icon="🗺️", layout="wide")
st.title("🗺️ Choropleth: 国別 輸出/輸入マップ")

# --- データ読み込み ---
with st.spinner("データを読み込み中..."):
    baci = load_baci()
    cc = load_country_codes()

available_years = sorted(baci["year"].unique().tolist())
filters = render_sidebar(available_years)

df = get_filtered(baci, filters["hs4"], filters["year_range"])
metric = filters["metric"]
metric_label = filters["metric_label"]
flow = filters["flow"]
country_col = "exporter" if flow == "export" else "importer"

# --- 国コード → ISO3 マッピング ---
code_to_iso3 = dict(zip(cc["country_code"].astype(int), cc["iso3"]))
code_to_name = dict(zip(cc["country_code"].astype(int), cc["country_name"]))

# --- 集計 ---
agg = (
    df.groupby(country_col)[metric]
    .sum()
    .reset_index()
    .rename(columns={country_col: "country_code", metric: "value"})
)
agg["iso3"] = agg["country_code"].map(code_to_iso3)
agg["country_name"] = agg["country_code"].map(code_to_name).fillna(agg["country_code"].astype(str))

# ISO3 がないレコードは除外（地図表示不可）
agg = agg.dropna(subset=["iso3"])
agg = agg[agg["iso3"].str.len() == 3]

year_label = (
    str(filters["year_range"][0])
    if filters["year_range"][0] == filters["year_range"][1]
    else f"{filters['year_range'][0]}–{filters['year_range'][1]}"
)

# --- コロプレス地図 ---
log_scale = st.checkbox("対数スケール", value=True, help="貿易額の偏りが大きい場合に推奨")

import numpy as np
if log_scale:
    agg["value_plot"] = np.log10(agg["value"].clip(lower=1))
    color_label = f"log10({metric_label})"
else:
    agg["value_plot"] = agg["value"]
    color_label = metric_label

fig = px.choropleth(
    agg,
    locations="iso3",
    color="value_plot",
    hover_name="country_name",
    hover_data={"value": ":,.0f", "value_plot": False, "iso3": False},
    color_continuous_scale="YlOrRd",
    title=(
        f"{filters['commodity_label']} — "
        f"{filters['flow_label']}額の国別分布 ({year_label})"
    ),
    labels={"value_plot": color_label, "value": metric_label},
)
fig.update_layout(
    geo=dict(showframe=False, showcoastlines=True),
    height=550,
    coloraxis_colorbar_title=color_label,
)
st.plotly_chart(fig, use_container_width=True)

# --- 上位 20 国のバーチャート ---
top20 = agg.nlargest(20, "value")
fig2 = px.bar(
    top20,
    x="value",
    y="country_name",
    orientation="h",
    title=f"上位 20 カ国 ({year_label})",
    labels={"value": metric_label, "country_name": "国"},
)
fig2.update_layout(yaxis={"categoryorder": "total ascending"}, height=500)
st.plotly_chart(fig2, use_container_width=True)

st.caption(
    "Source: BACI International Trade Database, CEPII (Licence Etalab 2.0)."
)
