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
DOTFILE="stacks/${STACK}/data/roadmap.dot"
SVGFILE="stacks/${STACK}/data/roadmap.svg"
PNGFILE="stacks/${STACK}/data/roadmap.png"
MDFILE="stacks/${STACK}/data/roadmap.md"

python3 ./tools/xmlg2dot.py --xmlg="${ROADMAPFILE}" --dot="${DOTFILE}"
echo "Check ${DOTFILE}"
dot -Tsvg "${DOTFILE}" -o "${SVGFILE}"
echo "Check ${SVGFILE}"
dot -Tpng "${DOTFILE}" -o "${PNGFILE}"
echo "Check ${PNGFILE}"

python3 ./tools/xmlg2md.py --xmlg="${ROADMAPFILE}" --materials="${MATERIALS}" --root="backend" > "${MDFILE}"
echo "Check ${MDFILE}"
