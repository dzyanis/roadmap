#!/usr/bin/env python3

import argparse
import re
from urllib.parse import quote
import materials as mt
from xmlgraph import Roadmap


def markdown_text(value):
    return re.sub(r'([\\\[\]`*_<>~&!])', r'\\\1', value)


def markdown_link(title, url):
    destination = quote(url, safe=":/?#[]@!$&'*+,;=%").replace('&', '&amp;')
    return f'[{markdown_text(title)}]({destination})'


def walk(roadmap, nodeid, level, materials):
    node = roadmap.nodes[nodeid]

    if level > 6:
        level = 6
    label = markdown_text(node.label).replace('#', r'\#')
    print('#'*level + ' ' + label + '\n')

    node_mat = materials[nodeid]
    for m in node_mat:
        link = markdown_link(m.title, m.url)
        translation = f'[{markdown_link(m.translate_lang, m.translate_url)}]' if m.translate_url else ''
        print(f'- {m.type}: {link}{translation}')

    if len(node_mat) > 0:
        print('\n')

    for childid in node.childrenids:
        walk(roadmap, childid, level+1, materials)


def load_stack(graphml, xmlmaterials, rootid):
    roadmap = Roadmap(graphml)
    if rootid not in roadmap.nodes:
        raise ValueError(f'{graphml}: unknown root node {rootid!r}')
    materials = mt.parsexml(xmlmaterials)
    unknown_tags = [f'{entries[0].filepath}: material tag {tag!r} has no node in {graphml}'
                    for tag, entries in materials.items() if tag not in roadmap.nodes]
    if unknown_tags:
        raise ValueError('\n'.join(unknown_tags))
    return roadmap, materials


def convert_md(graphml, xmlmaterials, rootid):
    roadmap, materials = load_stack(graphml, xmlmaterials, rootid)
    walk(roadmap, rootid, 1, materials)


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
