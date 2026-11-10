#!/bin/sh

set -e

for tool in python3 dot; do
  if ! command -v "$tool" >/dev/null 2>&1; then
    echo "Error: required tool '$tool' was not found in PATH. Install Python 3 and Graphviz before building." >&2
    exit 1
  fi
done

STACK=$1
ROADMAPFILE="stacks/${STACK}/roadmap.xml"
MATERIALS="stacks/${STACK}/materials.xml"
OUTDIR="stacks/${STACK}/data"
mkdir -p "$OUTDIR"
staging=$(mktemp -d "$OUTDIR/.roadmap.XXXXXX")
trap 'rm -rf "$staging"' 0
trap 'exit 1' HUP INT TERM

python3 ./tools/xmlg2dot.py --xmlg="$ROADMAPFILE" --dot="$staging/roadmap.dot"
dot -Tsvg "$staging/roadmap.dot" -o "$staging/roadmap.svg"
dot -Tpng "$staging/roadmap.dot" -o "$staging/roadmap.png"
python3 ./tools/xmlg2md.py --xmlg="$ROADMAPFILE" --materials="$MATERIALS" --root=backend > "$staging/roadmap.md"

for extension in dot svg png md; do
  mv "$staging/roadmap.$extension" "$OUTDIR/roadmap.$extension"
  echo "Check $OUTDIR/roadmap.$extension"
done
