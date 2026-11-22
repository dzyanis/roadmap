#!/usr/bin/env python3

import argparse
import re
from pipeline import load_roadmap
from xmlgraph import CONTAINS, PREREQUISITE, RELATED_TO


DOT_KEYWORDS = {'node', 'edge', 'graph', 'digraph', 'subgraph', 'strict'}


def dot_string(text):
    escaped = (text.replace('\\', '\\\\').replace('"', '\\"')
               .replace('\r\n', '\n').replace('\r', '\n').replace('\n', '\\n'))
    return f'"{escaped}"'


def dot_id(text):
    if re.fullmatch(r'[A-Za-z_][A-Za-z_0-9]*', text) and text.lower() not in DOT_KEYWORDS:
        return text
    return dot_string(text)


EDGE_ATTRIBUTES = {
    CONTAINS: '',
    PREREQUISITE: ' [style=dashed, label="learn first", constraint=false]',
    RELATED_TO: ' [style=dotted, dir=none, label="related", constraint=false]',
}


def write_dot(roadmap, output):
    output.write('digraph roadmap {\n\trankdir=LR;\n')
    for edge in roadmap.edges.values():
        attributes = EDGE_ATTRIBUTES[edge.type]
        output.write(f'\t{dot_id(edge.source)}->{dot_id(edge.target)}{attributes};\n')
    for node in roadmap.nodes.values():
        output.write(f'\t{dot_id(node.id)} [ label={dot_string(node.label)} ];\n')
    output.write('}\n')


def convert_dot(graphml, dot):
    roadmap = load_roadmap(graphml)
    with open(dot, 'w', encoding='utf-8') as output:
        write_dot(roadmap, output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Converting GraphML to DOT')
    parser.add_argument('--xmlg', help='XML Graph filename')
    parser.add_argument('--dot', help='DOT filename')
    args = parser.parse_args()

    try:
        convert_dot(args.xmlg, args.dot)
    except ValueError as error:
        parser.exit(1, f'{error}\n')
