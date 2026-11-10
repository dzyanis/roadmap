#!/usr/bin/env python3

import xml.etree.ElementTree as Et


class Edge:
    def __init__(self, edge_id, source, target):
        self.id = edge_id
        self.source = source
        self.target = target


class Node:
    def __init__(self, node_id, label):
        self.id = node_id
        self.label = label
        self.childrenids = []


class Roadmap:
    def __init__(self, filepath):
        self.edges = {}
        self.nodes = {}
        self._edges_in_order = []
        self.add_from_file(filepath)

    def add_from_file(self, filepath):
        self._load_from_file(filepath)
        # Includes may define endpoints after the edges that reference them.
        # Keep declaration order, including repeated edges in existing data.
        for edge in self._edges_in_order:
            for endpoint in ('source', 'target'):
                node_id = getattr(edge, endpoint)
                if node_id not in self.nodes:
                    raise ValueError(
                        "Edge {!r} references unknown {} node {!r}".format(
                            edge.id, endpoint, node_id))
        for node in self.nodes.values():
            node.childrenids.clear()
        for edge in self._edges_in_order:
            self.nodes[edge.source].childrenids.append(edge.target)

    def _load_from_file(self, filepath):
        tree = Et.parse(filepath)
        root = tree.getroot()
        for child in root:
            if child.tag == 'include':
                self._load_from_file(child.get('filepath'))
            for dotElem in child:
                if dotElem.tag == 'edge':
                    edge_id = dotElem.get('id')
                    source = dotElem.get('source')
                    target = dotElem.get('target')
                    edge = Edge(edge_id, source, target)
                    self.edges[edge_id] = edge
                    self._edges_in_order.append(edge)
                elif dotElem.tag == 'node':
                    node_id = dotElem.get('id')
                    label = dotElem.get('label')
                    self.nodes[node_id] = (Node(node_id, label))
