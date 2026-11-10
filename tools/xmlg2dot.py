#!/usr/bin/env python3

import argparse
from xmlgraph import Roadmap


def convert_dot(graphml, dot):
    roadmap = Roadmap(graphml)

    file = open(dot, "w")
    file.write('digraph roadmap {\n\trankdir=LR;\n')
    for _, edge in roadmap.edges.items():
        file.write('\t' + edge.source + '->' + edge.target + ';\t\n')
    for _, node in roadmap.nodes.items():
        file.write('\t' + node.id + ' [ label="' + node.label + '" ];\n')
    file.write('}\n')
    file.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Converting GraphML to DOT')
    parser.add_argument('--xmlg', help='XML Graph filename')
    parser.add_argument('--dot', help='DOT filename')
    args = parser.parse_args()

    try:
        convert_dot(args.xmlg, args.dot)
    except ValueError as error:
        parser.exit(1, f'{error}\n')
