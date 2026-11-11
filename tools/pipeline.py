"""Assemble validated XML into the rendering-independent exporter model."""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from materials import parsexml
from xmlgraph import Roadmap
from xmlvalidation import SchemaValidator


@dataclass
class Topic:
    id: str
    label: str
    childrenids: tuple
    subjects: tuple
    resources: tuple


@dataclass
class Graph:
    id: str
    root: Optional[str]
    nodes: dict
    edges: dict
    subjects: tuple


def subject_id(filepath):
    """Subject membership follows the declaring file, including nested fragments."""
    for directory in Path(filepath).resolve().parents:
        if directory.parent.name == 'subjects':
            return directory.name
    return None


def load_roadmap(graphml, xmlmaterials=None, rootid=None, roadmap_id=None):
    """Validate and assemble once; exporters receive this Graph and do no XML I/O.

    Materials/root are optional for graph-only legacy DOT and subject prototypes.
    JSON and Markdown require a root. IDs default to category/name for roadmaps.
    """
    path = Path(graphml).resolve()
    roadmap = Roadmap(path, validator=SchemaValidator('roadmap.xsd'))
    if rootid is not None and rootid not in roadmap.nodes:
        raise ValueError(f'{graphml}: unknown root node {rootid!r}')
    resources = (parsexml(xmlmaterials, validator=SchemaValidator('materials.xsd'))
                 if xmlmaterials is not None else {})
    unknown_tags = [f'{entries[0].filepath}: material tag {tag!r} has no node in {graphml}'
                    for tag, entries in resources.items() if tag not in roadmap.nodes]
    if unknown_tags:
        raise ValueError('\n'.join(unknown_tags))

    nodes = {}
    subjects = set()
    for node in roadmap.nodes.values():
        subject = subject_id(node.filepath)
        membership = (subject,) if subject else ()
        subjects.update(membership)
        nodes[node.id] = Topic(node.id, node.label, tuple(node.childrenids), membership,
                               tuple(resources.get(node.id, ())))
    if roadmap_id is None:
        roadmap_id = (f'{path.parent.parent.name}/{path.parent.name}'
                      if path.parent.parent.parent.name == 'roadmaps' else path.parent.name)
    return Graph(roadmap_id, rootid, nodes, roadmap.edges, tuple(sorted(subjects)))
