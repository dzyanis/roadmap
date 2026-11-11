#!/usr/bin/env python3

import argparse
import re
from urllib.parse import quote
import sys
from pipeline import load_roadmap


def markdown_text(value):
    return re.sub(r'([\\\[\]`*_<>~&!])', r'\\\1', value)


def markdown_link(title, url):
    destination = quote(url, safe=":/?#[]@!$&'*+,;=%").replace('&', '&amp;')
    return f'[{markdown_text(title)}]({destination})'


def walk(roadmap, nodeid, level, output):
    node = roadmap.nodes[nodeid]

    if level > 6:
        level = 6
    label = markdown_text(node.label).replace('#', r'\#')
    print('#'*level + ' ' + label + '\n', file=output)

    node_mat = node.resources
    for m in node_mat:
        link = markdown_link(m.title, m.url)
        translation = f'[{markdown_link(m.translate_lang, m.translate_url)}]' if m.translate_url else ''
        print(f'- {m.type}: {link}{translation}', file=output)

    if len(node_mat) > 0:
        print('\n', file=output)

    for childid in node.childrenids:
        walk(roadmap, childid, level+1, output)


def write_md(roadmap, output):
    if roadmap.root not in roadmap.nodes:
        raise ValueError('Markdown export requires a valid root topic')
    walk(roadmap, roadmap.root, 1, output)


def convert_md(graphml, xmlmaterials, rootid):
    roadmap = load_roadmap(graphml, xmlmaterials, rootid)
    write_md(roadmap, sys.stdout)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Combining GraphML and materials into markdown')
    parser.add_argument('--xmlg', default='roadmap.xml', help='XML Graph filename')
    parser.add_argument('--materials', default='materials.xml', help='Materials XML filename')
    parser.add_argument('--root', default='backend', help='Root element id')
    args = parser.parse_args()

    try:
        convert_md(args.xmlg, args.materials, args.root)
    except ValueError as error:
        parser.exit(1, f'{error}\n')
