"""Version 1 JSON contract. No renderer-specific fields or local file paths."""

import json


def resource_data(resource):
    return {
        'type': resource.type,
        'title': resource.title,
        'url': resource.url,
        'language': resource.language,
        'description': resource.description,
        'translation': ({'language': resource.translate_lang, 'url': resource.translate_url}
                        if resource.translate_url else None),
    }


def graph_data(roadmap):
    if roadmap.root not in roadmap.nodes:
        raise ValueError('JSON export requires a valid root topic')
    return {
        'schema_version': 1,
        'roadmap': {'id': roadmap.id, 'label': roadmap.nodes[roadmap.root].label,
                    'root': roadmap.root},
        'subjects': list(roadmap.subjects),
        'topics': [
            {'id': node.id, 'label': node.label, 'subjects': list(node.subjects),
             'resources': [resource_data(resource) for resource in node.resources]}
            for node in sorted(roadmap.nodes.values(), key=lambda node: node.id)
        ],
        'edges': [
            {'id': edge.id, 'source': edge.source, 'target': edge.target, 'type': edge.type}
            for edge in sorted(roadmap.edges.values(), key=lambda edge: edge.id)
        ],
    }


def write_json(roadmap, output):
    json.dump(graph_data(roadmap), output, ensure_ascii=False, indent=2)
    output.write('\n')
