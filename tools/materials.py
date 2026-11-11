#!/usr/bin/env python3
from collections import defaultdict

from xmlincludes import load_xml


class Material:
    def __init__(self, filepath):
        self.filepath = filepath
        self.type = ''
        self.title = ''
        self.url = ''
        self.language = ''
        self.description = ''
        self.translate_lang = ''
        self.translate_url = ''


def normalize_url(url):
    return ''.join(line.strip() for line in url.splitlines())


def parsexml(filepath, ancestors=(), validator=None):
    root, ancestors = load_xml(filepath, ancestors, validator)
    materials = defaultdict(list)
    for mat_desc in root:
        if mat_desc.tag == 'include':
            include = ancestors[-1].parent / mat_desc.attrib['filepath']
            for tag, entries in parsexml(include, ancestors, validator).items():
                materials[tag].extend(entries)
            continue
        material = Material(filepath)
        material.type = mat_desc.tag
        material.language = mat_desc.get('lang', '').strip()
        material.description = ' '.join(mat_desc.findtext('description', '').split())
        material.title = ' '.join(mat_desc.findtext('title', '').split())
        material.url = normalize_url(mat_desc.findtext('url', ''))
        if not material.title or not material.url:
            continue
        translation = mat_desc.find('translate')
        if translation is not None:
            material.translate_lang = translation.attrib['lang'].strip()
            material.translate_url = normalize_url(translation.attrib['url'])
        for element in mat_desc.findall('tags/tag'):
            tag = (element.text or '').strip()
            if tag:
                materials[tag].append(material)
    return materials
