"""ページ2: Sankey — 輸出国→輸入国のフロー図（ノードフォーカス機能付き）"""

import sys
from pathlib import Path

import plotly.graph_objects as go
import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent))
from components.data_loader import load_baci, load_country_codes, get_filtered
from components.filters import render_sidebar

st.set_page_config(page_title="Sankey", page_icon="🔀", layout="wide")
st.title("🔀 Sankey: 輸出国 → 輸入国 フロー")

# --- データ読み込み ---
with st.spinner("データを読み込み中..."):
    baci = load_baci()
    cc = load_country_codes()

available_years = sorted(baci["year"].unique().tolist())
filters = render_sidebar(available_years)

year_range = filters["year_range"]
hs4 = filters["hs4"]
metric = filters["metric"]

df = get_filtered(baci, hs4, year_range)

year_label = (
    str(year_range[0]) if year_range[0] == year_range[1]
    else f"{year_range[0]}–{year_range[1]} 合計"
)

# --- 国コードマッピング ---
code_to_name = dict(zip(cc["country_code"].astype(int), cc["country_name"]))

# --- 上位 N 国 ---
col_n, col_focus = st.columns([1, 2])
with col_n:
    top_n = st.slider("表示する国数（輸出・輸入それぞれ上位）", 5, 30, 15)

top_exporters = df.groupby("exporter")[metric].sum().nlargest(top_n).index.tolist()
top_importers = df.groupby("importer")[metric].sum().nlargest(top_n).index.tolist()

df_top = (
    df[df["exporter"].isin(top_exporters) & df["importer"].isin(top_importers)]
    .groupby(["exporter", "importer"])[metric]
    .sum()
    .reset_index()
)

if df_top.empty:
    st.info("データがありません。商品・期間・指標を変更してください。")
    st.stop()

# --- フォーカス国選択（クリック相当） ---
exp_names = [code_to_name.get(c, str(c)) for c in top_exporters]
imp_names = [code_to_name.get(c, str(c)) for c in top_importers]
all_node_names = sorted(set(exp_names + imp_names))

with col_focus:
    focus_label = st.selectbox(
        "フォーカス国（選択で絞り込み、同じ国を選び直すと全表示）",
        ["（全表示）"] + all_node_names,
        key="sankey_focus",
    )

# フォーカス国が選択された場合、その国に繋がるリンクだけ残す
name_to_code = {v: k for k, v in code_to_name.items()}

if focus_label != "（全表示）":
    focus_code = name_to_code.get(focus_label)
    if focus_code is not None:
        df_top = df_top[
            (df_top["exporter"] == focus_code) | (df_top["importer"] == focus_code)
        ]
        # フォーカス時は関連する輸出・輸入国のみ残す
        focused_exp = df_top["exporter"].unique().tolist()
        focused_imp = df_top["importer"].unique().tolist()
        top_exporters = [c for c in top_exporters if c in focused_exp]
        top_importers = [c for c in top_importers if c in focused_imp]

# --- ノードリスト構築 ---
exp_nodes = [f"{code_to_name.get(c, str(c))} (輸出)" for c in top_exporters]
imp_nodes = [f"{code_to_name.get(c, str(c))} (輸入)" for c in top_importers]
nodes = exp_nodes + imp_nodes

exp_idx = {c: i for i, c in enumerate(top_exporters)}
imp_idx = {c: i + len(top_exporters) for i, c in enumerate(top_importers)}

sources, targets, values, link_labels = [], [], [], []
for _, row in df_top.iterrows():
    exp = int(row["exporter"])
    imp = int(row["importer"])
    if exp in exp_idx and imp in imp_idx:
        sources.append(exp_idx[exp])
        targets.append(imp_idx[imp])
        values.append(row[metric])
        link_labels.append(
            f"{code_to_name.get(exp, str(exp))} → {code_to_name.get(imp, str(imp))}"
        )

# フォーカス国に応じてノード色を変える
focus_code_for_color = name_to_code.get(focus_label) if focus_label != "（全表示）" else None
node_colors = []
for i, c in enumerate(top_exporters):
    node_colors.append("#E55934" if c == focus_code_for_color else "#4C72B0")
for c in top_importers:
    node_colors.append("#E55934" if c == focus_code_for_color else "#DD8452")

# --- Sankey 図 ---
fig = go.Figure(
    go.Sankey(
        arrangement="snap",
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=nodes,
            color=node_colors,
        ),
        link=dict(
            source=sources,
            target=targets,
            value=values,
            label=link_labels,
            color="rgba(100, 150, 200, 0.3)",
        ),
    )
)
focus_suffix = f" — フォーカス: {focus_label}" if focus_label != "（全表示）" else ""
fig.update_layout(
    title=f"{filters['commodity_label']} — 貿易フロー ({year_label}){focus_suffix}",
    font_size=11,
    height=700,
)
st.plotly_chart(fig, use_container_width=True)

st.caption(
    f"上位 {top_n} 輸出国 × 上位 {top_n} 輸入国のフローを表示。"
    "Source: BACI International Trade Database, CEPII (Licence Etalab 2.0)."
)
