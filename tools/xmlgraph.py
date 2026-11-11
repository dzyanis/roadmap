#!/usr/bin/env python3

from graphlib import CycleError, TopologicalSorter

from xmlincludes import load_xml


class Edge:
    def __init__(self, edge_id, source, target, filepath):
        self.id = edge_id
        self.source = source
        self.target = target
        self.filepath = filepath
        self.type = 'contains'


class Node:
    def __init__(self, node_id, label, filepath):
        self.id = node_id
        self.label = label
        self.filepath = filepath
        self.childrenids = []


class Roadmap:
    def __init__(self, filepath, validator=None):
        self.edges = {}
        self.nodes = {}
        self.validator = validator
        self.add_from_file(filepath)

    def add_from_file(self, filepath):
        nodes = self.nodes.copy()
        edges = self.edges.copy()
        self._load_from_file(filepath, (), nodes, edges)

        # Connect edges only after all included files have been loaded.
        topology = TopologicalSorter()
        for edge in edges.values():
            for endpoint in ('source', 'target'):
                node_id = getattr(edge, endpoint)
                if node_id not in nodes:
                    raise ValueError(
                        f'{edge.filepath}: Edge {edge.id!r} references unknown '
                        f'{endpoint} node {node_id!r}')
            topology.add(edge.target, edge.source)
        try:
            topology.prepare()
        except CycleError as error:
            cycle = ' -> '.join(error.args[1])
            raise ValueError(f'{filepath}: roadmap cycle: {cycle}') from error

        for node in nodes.values():
            node.childrenids.clear()
        for edge in edges.values():
            nodes[edge.source].childrenids.append(edge.target)
        self.nodes = nodes
        self.edges = edges

    def _load_from_file(self, filepath, ancestors, nodes, edges):
        root, ancestors = load_xml(filepath, ancestors, self.validator)
        for child in root:
            if child.tag == 'include':
                include = ancestors[-1].parent / child.attrib['filepath']
                self._load_from_file(include, ancestors, nodes, edges)
                continue
            for element in child:
                element_id = element.get('id')
                if element.tag == 'edge':
                    if element_id in edges:
                        raise ValueError(f'{filepath}: duplicate edge ID {element_id!r} '
                                         f'(first defined in {edges[element_id].filepath})')
                    edges[element_id] = Edge(element_id, element.get('source'),
                                             element.get('target'), filepath)
                elif element.tag == 'node':
                    if element_id in nodes:
                        raise ValueError(f'{filepath}: duplicate node ID {element_id!r} '
                                         f'(first defined in {nodes[element_id].filepath})')
                    nodes[element_id] = Node(element_id, element.get('label'), filepath)
