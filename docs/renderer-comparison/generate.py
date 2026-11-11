"""Export the same roadmap nodes, edges, and resource links for three renderers."""

import argparse
from collections import defaultdict
import json
from pathlib import Path
import sys

REPOSITORY = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPOSITORY / 'tools'))

from pipeline import load_roadmap
from xmlg2dot import dot_string


def export(xml, output, grouped):
    roadmap = load_roadmap(xml, xml.with_name('materials.xml'))
    groups = defaultdict(list)
    ids = {}
    for number, node in enumerate(roadmap.nodes.values(), start=1):
        group = node.subjects[0] if grouped and node.subjects else ''
        identifier = f'n{number}'
        ids[node.id] = (group, identifier)
        url = node.resources[0].url if node.resources else ''
        groups[group].append((identifier, node.label, url))

    dot = ['digraph roadmap {', '  rankdir=LR;']
    mermaid = ['flowchart LR']
    d2 = ['direction: right']
    for group, nodes in groups.items():
        indent = '  ' if group else ''
        if group:
            group_id = group.replace('-', '_')
            dot.extend([f'  subgraph cluster_{group_id} {{', f'    label="{group}";'])
            mermaid.append(f'  subgraph subject_{group_id}["{group}"]')
            d2.append(f'{group}: {{')
        for identifier, label, url in nodes:
            attributes = f'label={dot_string(label)}'
            if url:
                attributes += f', URL={dot_string(url)}'
            dot.append(f'  {indent}{identifier} [{attributes}];')
            mermaid_label = label.replace('#', '#35;').replace('"', '#quot;')
            mermaid.append(f'  {indent}{identifier}["{mermaid_label}"]')
            d2_label = json.dumps(label, ensure_ascii=False)
            if url:
                d2.append(f'{indent}{identifier}: {d2_label} {{')
                d2.append(f'{indent}  link: {json.dumps(url)}')
                d2.append(f'{indent}}}')
            else:
                d2.append(f'{indent}{identifier}: {d2_label}')
        if group:
            dot.append('  }')
            mermaid.append('  end')
            d2.append('}')

    for edge in roadmap.edges.values():
        source_group, source = ids[edge.source]
        target_group, target = ids[edge.target]
        dot.append(f'  {source} -> {target};')
        mermaid.append(f'  {source} --> {target}')
        d2_source = f'{source_group}.{source}' if source_group else source
        d2_target = f'{target_group}.{target}' if target_group else target
        d2.append(f'{d2_source} -> {d2_target}')
    for nodes in groups.values():
        for identifier, _, url in nodes:
            if url:
                mermaid.append(f'  click {identifier} href {json.dumps(url)}')

    for extension, lines in (('dot', dot + ['}']), ('mmd', mermaid), ('d2', d2)):
        output.with_suffix(f'.{extension}').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'{output.name}: {len(ids)} nodes, {len(roadmap.edges)} edges, '
          f'{sum(bool(url) for nodes in groups.values() for _, _, url in nodes)} linked nodes')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output_directory', type=Path)
    output = parser.parse_args().output_directory
    output.mkdir(parents=True, exist_ok=True)
    export(REPOSITORY / 'subjects/data-structures-algorithms/roadmap.xml', output / 'dsa', grouped=False)
    export(REPOSITORY / 'roadmaps/roles/go-engineer/roadmap.xml', output / 'go', grouped=True)


if __name__ == '__main__':
    main()
