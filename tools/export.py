"""Load once and export all data formats into the build's staging directory."""

import argparse
from pathlib import Path

from graphjson import write_json
from pipeline import load_roadmap
from xmlg2dot import write_dot
from xmlg2md import write_md


def export(graphml, materials, root, output, roadmap_id=None):
    roadmap = load_roadmap(graphml, materials, root, roadmap_id)
    # Validation finishes before any exporter opens an output file.
    for filename, writer in (('roadmap.dot', write_dot), ('guide.md', write_md),
                             ('graph.json', write_json)):
        with (Path(output) / filename).open('w', encoding='utf-8', newline='\n') as stream:
            writer(roadmap, stream)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--xmlg', required=True)
    parser.add_argument('--materials', required=True)
    parser.add_argument('--root', default='backend')
    parser.add_argument('--id', dest='roadmap_id')
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    try:
        export(args.xmlg, args.materials, args.root, args.output, args.roadmap_id)
    except ValueError as error:
        parser.exit(1, f'{error}\n')
