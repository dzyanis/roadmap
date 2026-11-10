#!/usr/bin/env python3
from collections import defaultdict

from xmlincludes import load_xml


class Material:
    def __init__(self, filepath):
        self.filepath = filepath
        self.type = ''
        self.title = ''
        self.url = ''
        self.translate_lang = ''
        self.translate_url = ''


def parsexml(filepath, ancestors=()):
    root, ancestors = load_xml(filepath, ancestors)
    materials = defaultdict(lambda: [])
    for mat_desc in root:
        if mat_desc.tag == 'include':
            materials.update(parsexml(mat_desc.attrib['filepath'], ancestors))
            continue
        material = Material(filepath)
        material.type = mat_desc.tag
        for item in mat_desc:
            if item.tag == 'title':
                material.title = item.text
            if item.tag == 'url':
                material.url = item.text
            if item.tag == 'translate':
                material.translate_lang = item.attrib['lang']
                material.translate_url = item.attrib['url']
            if item.tag == 'tags':
                for tag in item:
                    materials[tag.text].append(material)
    return materials
