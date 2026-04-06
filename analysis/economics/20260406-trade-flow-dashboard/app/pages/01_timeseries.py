"""ページ1: 時系列 — 国別の輸出/輸入量・額の年次推移"""

import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent))
from components.data_loader import load_baci, load_country_codes, get_filtered
from components.filters import render_sidebar

st.set_page_config(page_title="時系列", page_icon="📈", layout="wide")
st.title("📈 時系列: 国別 輸出/輸入の推移")

# --- データ読み込み ---
with st.spinner("データを読み込み中..."):
    baci = load_baci()
    cc = load_country_codes()

available_years = sorted(baci["year"].unique().tolist())
filters = render_sidebar(available_years)

df = get_filtered(baci, filters["hs4"], filters["year_range"])

country_col = "exporter" if filters["flow"] == "export" else "importer"
metric = filters["metric"]

# --- 国選択 ---
# 合計値で上位 20 カ国を事前選択
top20 = (
    df.groupby(country_col)[metric]
    .sum()
    .nlargest(20)
    .index.tolist()
)

# 国コード → 国名マッピング
code_to_name = dict(zip(cc["country_code"].astype(int), cc["country_name"]))
top20_names = [code_to_name.get(c, str(c)) for c in top20]
all_codes = sorted(df[country_col].unique().tolist())
all_names = [code_to_name.get(c, str(c)) for c in all_codes]

selected_names = st.multiselect(
    "表示する国（複数選択可）",
    options=all_names,
    default=top20_names[:10],
)

# 名前 → コードの逆引き
name_to_code = {v: k for k, v in code_to_name.items()}
selected_codes = [name_to_code.get(n, n) for n in selected_names]

if not selected_codes:
    st.info("国を1カ国以上選択してください。")
    st.stop()

# --- 集計 ---
ts = (
    df[df[country_col].isin(selected_codes)]
    .groupby(["year", country_col])[metric]
    .sum()
    .reset_index()
)
ts["country_name"] = ts[country_col].map(code_to_name).fillna(ts[country_col].astype(str))

# --- グラフ ---
metric_label = filters["metric_label"]
flow_label = filters["flow_label"]
commodity_label = filters["commodity_label"]

fig = px.line(
    ts,
    x="year",
    y=metric,
    color="country_name",
    markers=True,
    title=f"{commodity_label} — {flow_label}量の推移",
    labels={"year": "年", metric: metric_label, "country_name": "国"},
)
fig.update_layout(
    legend_title_text="国",
    hovermode="x unified",
    height=500,
)
st.plotly_chart(fig, use_container_width=True)

# --- 侵攻ラインの注釈 ---
if 2022 in range(filters["year_range"][0], filters["year_range"][1] + 1):
    fig.add_vline(
        x=2022,
        line_dash="dash",
        line_color="red",
        annotation_text="2022: ウクライナ侵攻",
        annotation_position="top right",
    )
    st.plotly_chart(fig, use_container_width=True, key="with_annotation")

# --- データテーブル ---
with st.expander("データを表示"):
    pivot = ts.pivot(index="year", columns="country_name", values=metric).fillna(0)
    st.dataframe(pivot.style.format("{:,.0f}"))

st.caption(
    "Source: BACI International Trade Database, CEPII (Licence Etalab 2.0)."
)
