"""
BACI HS17 データを CEPII からダウンロードする。

Usage:
    uv run python scripts/download_baci.py

ダウンロード先: data/raw/BACI_HS17_V202601.zip
サイズ: 約 400-600 MB（時間がかかる場合がある）
"""

import sys
from pathlib import Path
import requests

RAW_DIR = Path(__file__).parent.parent / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

# CEPII BACI HS17 v202601 の直接ダウンロード URL
# 最新版は http://www.cepii.fr/CEPII/en/bdd_modele/bdd_modele_item.asp?id=37 で確認
BACI_URL = "http://www.cepii.fr/DATA_DOWNLOAD/baci/data/BACI_HS17_V202601.zip"
BACI_ZIP = RAW_DIR / "BACI_HS17_V202601.zip"


def download(url: str, dest: Path) -> None:
    if dest.exists():
        print(f"Already exists: {dest}")
        return

    print(f"Downloading {url} ...")
    with requests.get(url, stream=True, timeout=300) as r:
        r.raise_for_status()
        total = int(r.headers.get("content-length", 0))
        downloaded = 0
        with open(dest, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                f.write(chunk)
                downloaded += len(chunk)
                if total:
                    pct = downloaded / total * 100
                    print(f"\r  {pct:.1f}% ({downloaded // 1024 // 1024} MB)", end="", flush=True)
    print(f"\nSaved to {dest}")


if __name__ == "__main__":
    try:
        download(BACI_URL, BACI_ZIP)
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        print(
            "\nIf the download fails, manually download HS17 from:\n"
            "  http://www.cepii.fr/CEPII/en/bdd_modele/bdd_modele_item.asp?id=37\n"
            f"and save to: {BACI_ZIP}",
            file=sys.stderr,
        )
        sys.exit(1)
