"""Build an isolated, static renderer experiment from the validated XML model."""
import argparse
from collections import defaultdict
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import textwrap
import time
from urllib.parse import urlencode, parse_qs
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(REPO / 'tools'))
from pipeline import load_roadmap
from graphjson import graph_data
from xmlg2dot import dot_string

CANDIDATE = 'd2'
INPUTS = {
    'dsa': ('subjects/data-structures-algorithms', 'dsa'),
    'os': ('subjects/operating-systems', 'os'),
    'go': ('roadmaps/roles/go-engineer', 'backend'),
    'devops': ('roadmaps/roles/devops-engineer', 'backend'),
}
SVG = 'http://www.w3.org/2000/svg'
XLINK = 'http://www.w3.org/1999/xlink'
ET.register_namespace('', SVG)
ET.register_namespace('xlink', XLINK)


def topic_link(key, topic):
    return '#' + urlencode({'roadmap': key, 'topic': topic})


def source_data(graph):
    """Renderer-safe aliases are independent of XML IDs and label syntax."""
    ids = {key: f'n{i}' for i, key in enumerate(sorted(graph.nodes))}
    groups = defaultdict(list)
    for key in sorted(graph.nodes):
        node = graph.nodes[key]
        group = node.subjects[0] if node.subjects else 'roadmap'
        groups[group].append(node)
    return ids, groups


def wrapped(label):
    return '\n'.join(textwrap.wrap(label, width=28, break_long_words=False,
                                   break_on_hyphens=False))


def baseline(graph, key):
    ids, groups = source_data(graph)
    lines = ['digraph roadmap {', 'rankdir=LR;',
             'node [shape=box, fontname="Arial", fontsize=16];']
    for i, (group, nodes) in enumerate(groups.items()):
        lines += [f'subgraph cluster_{i} {{', f'label={dot_string(group)};']
        for node in nodes:
            lines.append(f'{ids[node.id]} [label={dot_string(wrapped(node.label))}, '
                         f'URL={dot_string(topic_link(key, node.id))}];')
        lines.append('}')
    for edge in graph.edges.values():
        lines.append(f'{ids[edge.source]} -> {ids[edge.target]};')
    return '\n'.join(lines + ['}']) + '\n'


def candidate_source(graph, key):
    ids, groups = source_data(graph)
    paths = {}
    lines = ['direction: right', '*.style.font-size: 16']
    for i, (group, nodes) in enumerate(groups.items()):
        lines += [f's{i}: {json.dumps(group)} {{', 'style.fill: "#eef4ff"']
        for node in nodes:
            paths[node.id] = f's{i}.{ids[node.id]}'
            lines += [f'{ids[node.id]}: {json.dumps(wrapped(node.label), ensure_ascii=False)} {{',
                      'style.fill: "#ffffff"', f'link: {json.dumps(topic_link(key, node.id))}', '}']
        lines.append('}')
    for edge in graph.edges.values():
        lines.append(f'{paths[edge.source]} -> {paths[edge.target]}')
    return '\n'.join(lines) + '\n'



def normalize_svg(path, graph):
    """Expose topic identity via public SVG links, not renderer DOM class names."""
    root = ET.parse(path).getroot()
    seen = []
    for anchor in root.iter(f'{{{SVG}}}a'):
        href = anchor.get('href', anchor.get(f'{{{XLINK}}}href', ''))
        topic = parse_qs(href.lstrip('#')).get('topic', [None])[0]
        if topic in graph.nodes:
            anchor.set('data-topic', topic)
            anchor.set('tabindex', '-1')
            anchor.set('aria-label', graph.nodes[topic].label)
            seen.append(topic)
    if sorted(seen) != sorted(graph.nodes):
        raise ValueError(f'{path}: rendered topic links differ from the model')
    viewbox = [float(value) for value in root.attrib['viewBox'].replace(',', ' ').split()]
    root.set('width', '100%')
    root.set('height', '100%')
    root.attrib.pop('style', None)
    ET.ElementTree(root).write(path, encoding='utf-8', xml_declaration=True)
    return viewbox[2:]


def run(command):
    start = time.perf_counter()
    result = subprocess.run([str(x) for x in command], capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(f'{command}\n{result.stdout}\n{result.stderr}')
    return round(time.perf_counter() - start, 3)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=HERE / 'demo')
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    for name in ('index.html', 'viewer.js', 'style.css'):
        shutil.copyfile(HERE / name, output / name)
    renderer = os.environ.get('D2', 'd2')
    version = subprocess.check_output([renderer, '--version'], text=True).strip()
    expected = '0.9.0'
    if version.lstrip('v') != expected:
        raise ValueError(f'Expected {CANDIDATE} {expected}, got {version}')
    report = {'candidate': CANDIDATE, 'renderer_version': version,
              'platform': platform.platform(), 'python': platform.python_version(),
              'graphviz': subprocess.run(['dot', '-V'], capture_output=True, text=True).stderr.strip(),
              'method': 'One serial warm-machine run per graph/layout; process startup included. SVG postprocessing excluded. No statistical confidence claimed.',
              'results': []}
    manifest = []
    for key, (directory, root) in INPUTS.items():
        start = time.perf_counter()
        graph = load_roadmap(REPO / directory / 'roadmap.xml', REPO / directory / 'materials.xml', root, key)
        data = graph_data(graph)
        (output / f'{key}.json').write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
        (output / f'{key}.dot').write_text(baseline(graph, key))
        extension = 'd2'
        source = output / f'{key}.{extension}'
        source.write_text(candidate_source(graph, key), encoding='utf-8')
        export_seconds = round(time.perf_counter() - start, 3)
        for engine in ('graphviz', 'dagre', 'elk'):
            svg = output / f'{key}-{engine}.svg'
            if engine == 'graphviz':
                command = ['dot', '-Tsvg', output / f'{key}.dot', '-o', svg]
            else:
                command = [renderer, f'--layout={engine}', '--pad=24', '--salt=roadmap-prototype', source, svg]
            seconds = run(command)
            width, height = normalize_svg(svg, graph)
            row = {'input': key, 'layout': engine, 'nodes': len(graph.nodes), 'edges': len(graph.edges),
                   'resources': sum(len(n.resources) for n in graph.nodes.values()),
                   'export_seconds': export_seconds, 'render_seconds': seconds,
                   'svg_bytes': svg.stat().st_size, 'width': width, 'height': height}
            report['results'].append(row)
            print(json.dumps(row), flush=True)
        manifest.append({'id': key, 'label': data['roadmap']['label']})
    (output / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    report['viewer_bytes'] = sum((output / f).stat().st_size for f in ('index.html', 'viewer.js', 'style.css'))
    report['total_demo_bytes'] = sum(p.stat().st_size for p in output.iterdir() if p.is_file() and p.name != 'metrics.json')
    (output / 'metrics.json').write_text(json.dumps(report, indent=2) + '\n')


if __name__ == '__main__':
    main()
