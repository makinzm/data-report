"""
BACI ZIP を展開し、対象商品（HS4）でフィルタして Parquet に変換する。

Usage:
    uv run python scripts/process_baci.py

出力先: data/processed/baci_filtered.parquet
列:
    year        (int)   : 年
    exporter    (int)   : 輸出国コード (BACI/UN numeric)
    importer    (int)   : 輸入国コード
    hs6         (str)   : HS6 コード（6桁ゼロ埋め文字列）
    hs4         (str)   : HS4 コード（先頭4桁）
    value_kusd  (float) : 貿易額（千 USD）
    qty_kton    (float) : 貿易量（千トン）

国コードマッピング: data/processed/country_codes.parquet
列:
    country_code (int)  : BACI 国コード
    iso3         (str)  : ISO 3166-1 alpha-3
    country_name (str)  : 国名（英語）
"""

import zipfile
from io import StringIO
from pathlib import Path

import pandas as pd

RAW_DIR = Path(__file__).parent.parent / "data" / "raw"
PROC_DIR = Path(__file__).parent.parent / "data" / "processed"
PROC_DIR.mkdir(parents=True, exist_ok=True)

BACI_ZIP = RAW_DIR / "BACI_HS17_V202601.zip"
COUNTRY_CSV = RAW_DIR / "country_codes_V202601.csv"  # ZIP に同梱

# PROPOSAL.md Sec 3.2 で事前登録した対象商品（HS4）
TARGET_HS4 = {"1001", "1005", "1201", "1511", "2709", "2711", "2701", "2601", "7403"}


def load_country_codes(zf: zipfile.ZipFile) -> pd.DataFrame:
    """BACI ZIP 内の国コードファイルを読み込む"""
    candidates = [n for n in zf.namelist() if "country_codes" in n.lower() and n.endswith(".csv")]
    if not candidates:
        # フォールバック: 空のマッピングを返す
        print("  Warning: country_codes CSV not found in ZIP. Country names will be unavailable.")
        return pd.DataFrame(columns=["country_code", "iso3", "country_name"])

    with zf.open(candidates[0]) as f:
        raw = f.read().decode("utf-8", errors="replace")
        df = pd.read_csv(StringIO(raw))

    # 列名の正規化（BACI バージョンにより異なる場合がある）
    col_map = {}
    for c in df.columns:
        cl = c.lower().strip()
        if cl in ("country_code", "code"):
            col_map[c] = "country_code"
        elif cl in ("country_iso3", "iso_3digit_alpha", "iso3", "iso_3"):
            col_map[c] = "iso3"
        elif cl in ("country_name_abbreviation", "country_name", "name"):
            col_map[c] = "country_name"
    df = df.rename(columns=col_map)

    for col in ["country_code", "iso3", "country_name"]:
        if col not in df.columns:
            df[col] = ""

    return df[["country_code", "iso3", "country_name"]].copy()


def process_year_csv(zf: zipfile.ZipFile, filename: str) -> pd.DataFrame:
    """1年分の BACI CSV を読み込み、対象 HS4 でフィルタして返す"""
    with zf.open(filename) as f:
        raw = f.read().decode("utf-8", errors="replace")
        df = pd.read_csv(StringIO(raw), dtype={"k": str})

    # BACI 列: t, i, j, k, v, q
    df = df.rename(columns={"t": "year", "i": "exporter", "j": "importer",
                             "k": "hs6", "v": "value_kusd", "q": "qty_kton"})

    # HS6 を6桁ゼロ埋め文字列に統一
    df["hs6"] = df["hs6"].str.zfill(6)
    df["hs4"] = df["hs6"].str[:4]

    # 対象商品のみ残す
    df = df[df["hs4"].isin(TARGET_HS4)].copy()
    return df


def main() -> None:
    if not BACI_ZIP.exists():
        raise FileNotFoundError(
            f"{BACI_ZIP} が見つかりません。\n"
            "先に scripts/download_baci.py を実行してください。"
        )

    print(f"Opening {BACI_ZIP.name} ...")
    with zipfile.ZipFile(BACI_ZIP) as zf:
        print("  Loading country codes ...")
        country_df = load_country_codes(zf)
        country_df.to_parquet(PROC_DIR / "country_codes.parquet", index=False)
        print(f"  Saved country_codes.parquet ({len(country_df)} rows)")

        # 年次 CSV ファイルを列挙
        year_files = sorted(
            [n for n in zf.namelist() if n.endswith(".csv") and "_Y" in n]
        )
        print(f"  Found {len(year_files)} year files")

        frames = []
        for fname in year_files:
            year = fname.split("_Y")[1][:4]
            print(f"  Processing {year} ...", end=" ", flush=True)
            df = process_year_csv(zf, fname)
            frames.append(df)
            print(f"{len(df):,} rows (filtered)")

    combined = pd.concat(frames, ignore_index=True)
    print(f"\nTotal filtered rows: {len(combined):,}")

    out = PROC_DIR / "baci_filtered.parquet"
    combined.to_parquet(out, index=False)
    print(f"Saved to {out}")

    # サマリー表示
    print("\nHS4 breakdown:")
    print(combined.groupby("hs4")["value_kusd"].sum().sort_values(ascending=False).to_string())


if __name__ == "__main__":
    main()
