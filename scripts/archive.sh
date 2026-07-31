#!/usr/bin/env bash
# 归档脚本：把一个路径移入 archive/ 并在 archive/README.md 末尾的索引表登记一行
# 用法（在仓库根目录运行）:
#   scripts/archive.sh <相对路径> "<归档原因>"
# 示例:
#   scripts/archive.sh projects/old-tool "已被 new-tool 替代"
set -euo pipefail

if [ $# -lt 2 ]; then
  echo "用法: $0 <相对路径> \"<归档原因>\"" >&2
  exit 1
fi

REPO_ROOT="$(git rev-parse --show-toplevel)"
cd "$REPO_ROOT"

SRC="${1%/}"
REASON="$2"
NAME="$(basename "$SRC")"
DEST="archive/$NAME"
INDEX="archive/README.md"

if [ ! -e "$SRC" ]; then
  echo "错误: $SRC 不存在（路径需相对仓库根目录）" >&2
  exit 1
fi
case "$SRC" in
  archive|archive/*)
    echo "错误: $SRC 已在归档区内" >&2
    exit 1
    ;;
esac
if [ -e "$DEST" ]; then
  echo "错误: $DEST 已存在，请先给待归档内容改名（建议加来源后缀）" >&2
  exit 1
fi
if [ ! -f "$INDEX" ]; then
  echo "错误: 找不到索引 $INDEX" >&2
  exit 1
fi

git mv "$SRC" "$DEST"

TODAY="$(date +%F)"
printf '| %s | %s | /%s/ | %s | 已归档 |\n' "$TODAY" "$NAME" "$SRC" "$REASON" >> "$INDEX"
git add "$INDEX"

echo "✔ 已归档: /$SRC/ -> $DEST/"
echo "✔ 已登记索引: $INDEX（改动已暂存，请检查后自行 commit）"
