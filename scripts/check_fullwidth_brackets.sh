#!/bin/bash
# URLやメールアドレスに隣接する全角括弧を検出する
# 検出パターン: URL/メール/コードブロックの前後に（または）がある

set -euo pipefail

files=("$@")
found=0

for file in "${files[@]}"; do
  # URL直前/直後の全角括弧
  if grep -Pn '（https?://|https?://[^\s）]*）|（[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}）' "$file" 2>/dev/null; then
    echo "ERROR: $file に URL/メールアドレスを囲む全角括弧（）があります。半角 () に変えてください。"
    found=1
  fi
done

if [ "$found" -eq 1 ]; then
  exit 1
fi
