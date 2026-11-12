"""Build the visualization-first static site from the committed graph.json exports.

The site reads the same versioned JSON as generated/, so the website and the
repository outputs share one source of truth. Assets and data use relative paths,
so the output works at the GitHub Pages project URL (/roadmap/) and locally.

Local preview: make site && python3 -m http.server -d _site 8000
"""

import argparse
import json
import shutil
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[1]
SOURCE = REPOSITORY / 'site'
GENERATED = REPOSITORY / 'generated'
SHELL_FILES = ('index.html', 'app.js', 'style.css')
SCHEMA_VERSION = 1


def validate(graph, roadmap_id):
    """Reject data the viewer cannot render safely before anything is published."""
    if graph.get('schema_version') != SCHEMA_VERSION:
        raise ValueError(f'{roadmap_id}: unsupported schema_version {graph.get("schema_version")!r}')
    if graph['roadmap']['id'] != roadmap_id:
        raise ValueError(f'{roadmap_id}: graph declares roadmap id {graph["roadmap"]["id"]!r}')
    topics = set()
    for topic in graph['topics']:
        if topic['id'] in topics:
            raise ValueError(f'{roadmap_id}: duplicate topic {topic["id"]!r}')
        topics.add(topic['id'])
        for resource in topic['resources']:
            urls = [resource['url']]
            if resource['translation']:
                urls.append(resource['translation']['url'])
            for url in urls:
                if not url.startswith(('https://', 'http://')):
                    raise ValueError(f'{roadmap_id}: resource URL must be http(s): {url!r}')
    root = graph['roadmap']['root']
    if root not in topics:
        raise ValueError(f'{roadmap_id}: root {root!r} is not a topic')
    for edge in graph['edges']:
        for endpoint in (edge['source'], edge['target']):
            if endpoint not in topics:
                raise ValueError(f'{roadmap_id}: edge {edge["id"]!r} references unknown topic {endpoint!r}')
    return {'id': roadmap_id, 'label': graph['roadmap']['label'], 'root': root,
            'topics': len(topics), 'edges': len(graph['edges'])}


def build(output, generated=GENERATED, source=SOURCE):
    output = Path(output)
    if output.resolve() == REPOSITORY or REPOSITORY.is_relative_to(output.resolve()):
        raise ValueError(f'Refusing to replace {output}, which contains the repository')
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)
    for name in SHELL_FILES:
        shutil.copy2(source / name, output / name)
    shutil.copytree(source / 'vendor', output / 'vendor')
    # Keeps GitHub Pages from applying Jekyll processing to the static files.
    (output / '.nojekyll').touch()

    manifest = []
    for graph_path in sorted(generated.glob('*/*/graph.json')):
        roadmap_id = graph_path.parent.relative_to(generated).as_posix()
        graph = json.loads(graph_path.read_text(encoding='utf-8'))
        manifest.append(validate(graph, roadmap_id))
        destination = output / 'data' / f'{roadmap_id}.json'
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(json.dumps(graph, ensure_ascii=False, separators=(',', ':')) + '\n',
                               encoding='utf-8')
    if not manifest:
        raise ValueError(f'No graph.json files found under {generated}')
    (output / 'data' / 'index.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n',
                                                encoding='utf-8')
    return manifest


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=REPOSITORY / '_site')
    args = parser.parse_args()
    try:
        manifest = build(args.output)
    except ValueError as error:
        parser.exit(1, f'{error}\n')
    print(f'Built {len(manifest)} roadmaps into {args.output}')
