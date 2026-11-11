#!/bin/sh

set -e

for tool in python3 dot; do
  if ! command -v "$tool" >/dev/null 2>&1; then
    echo "Error: required tool '$tool' was not found in PATH. Install Python 3 and Graphviz before building." >&2
    exit 1
  fi
done

# Accept only discovered category/name paths, never arbitrary output paths.
ROADMAP=${1:-}
case "$ROADMAP" in
  roles/*|technologies/*|foundations/*) ;;
  *) echo "Usage: sh tools/build.sh <category/roadmap-name>" >&2; exit 1 ;;
esac
case "$ROADMAP" in
  *..*|*/*/*) echo "Invalid roadmap path: $ROADMAP" >&2; exit 1 ;;
esac
ROADMAPFILE="roadmaps/${ROADMAP}/roadmap.xml"
MATERIALS="roadmaps/${ROADMAP}/materials.xml"
OUTDIR="generated/${ROADMAP}"
if [ ! -f "$ROADMAPFILE" ] || [ ! -f "$MATERIALS" ]; then
  echo "Missing roadmap or materials: $ROADMAP" >&2
  exit 1
fi
mkdir -p "$OUTDIR"
staging=$(mktemp -d "$OUTDIR/.roadmap.XXXXXX")
trap 'rm -rf "$staging"' 0
trap 'exit 1' HUP INT TERM

python3 ./tools/xmlg2dot.py --xmlg="$ROADMAPFILE" --dot="$staging/roadmap.dot"
dot -Tsvg "$staging/roadmap.dot" -o "$staging/roadmap.svg"
dot -Tpng "$staging/roadmap.dot" -o "$staging/roadmap.png"
python3 ./tools/xmlg2md.py --xmlg="$ROADMAPFILE" --materials="$MATERIALS" --root=backend > "$staging/guide.md"

for filename in roadmap.dot roadmap.svg roadmap.png guide.md; do
  mv "$staging/$filename" "$OUTDIR/$filename"
  echo "Check $OUTDIR/$filename"
done
