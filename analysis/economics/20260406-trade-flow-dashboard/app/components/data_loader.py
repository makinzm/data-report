"""Parquet キャッシュの読み込みモジュール"""

from pathlib import Path

import pandas as pd
import streamlit as st

PROC_DIR = Path(__file__).parent.parent.parent / "data" / "processed"

# PROPOSAL.md Sec 3.2 で事前登録した商品マッピング
COMMODITY_MAP: dict[str, str] = {
    "小麦 (1001)": "1001",
    "トウモロコシ (1005)": "1005",
    "大豆 (1201)": "1201",
    "パーム油 (1511)": "1511",
    "原油 (2709)": "2709",
    "天然ガス/LNG (2711)": "2711",
    "石炭 (2701)": "2701",
    "鉄鉱石 (2601)": "2601",
    "銅・精製銅 (7403)": "7403",
}


@st.cache_data(show_spinner=False)
def load_baci() -> pd.DataFrame:
    """フィルタ済み BACI データを読み込む"""
    path = PROC_DIR / "baci_filtered.parquet"
    if not path.exists():
        st.error(
            f"`{path}` が見つかりません。\n\n"
            "先に以下を実行してください:\n"
            "```\nuv run python scripts/download_baci.py\n"
            "uv run python scripts/process_baci.py\n```"
        )
        st.stop()
    return pd.read_parquet(path)


@st.cache_data(show_spinner=False)
def load_country_codes() -> pd.DataFrame:
    """国コードマッピングを読み込む"""
    path = PROC_DIR / "country_codes.parquet"
    if not path.exists():
        return pd.DataFrame(columns=["country_code", "iso3", "country_name"])
    return pd.read_parquet(path)


@st.cache_data(show_spinner=False)
def get_filtered(
    df: pd.DataFrame,
    hs4: str,
    years: tuple[int, int],
) -> pd.DataFrame:
    """商品・年範囲でフィルタ（キャッシュ付き）"""
    y0, y1 = years
    mask = (df["hs4"] == hs4) & (df["year"] >= y0) & (df["year"] <= y1)
    return df[mask].copy()


def get_top_countries(
    df: pd.DataFrame,
    flow: str,
    metric: str,
    top_n: int = 15,
) -> list[str]:
    """貿易額/量でソートした上位 N 国コードを返す（flow='export'|'import'）"""
    col = "exporter" if flow == "export" else "importer"
    top = df.groupby(col)[metric].sum().nlargest(top_n).index.tolist()
    return [str(c) for c in top]
