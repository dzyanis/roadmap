"""Contract checks for the mermaid static viewer experiment."""
import importlib.util
import json
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / 'docs/prototypes/mermaid'
spec = importlib.util.spec_from_file_location('mermaid_prototype', HERE / 'build.py')
build = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build)


class PrototypeTests(unittest.TestCase):
    def test_committed_sources_match_validated_xml(self):
        for key, (directory, root) in build.INPUTS.items():
            with self.subTest(input=key):
                graph = build.load_roadmap(ROOT / directory / 'roadmap.xml', ROOT / directory / 'materials.xml', root, key)
                self.assertEqual(json.loads((HERE / f'demo/{key}.json').read_text()), build.graph_data(graph))
                self.assertEqual((HERE / f'demo/{key}.mmd').read_text(), build.candidate_source(graph, key))
                self.assertEqual((HERE / f'demo/{key}.dot').read_text(), build.baseline(graph, key))
                for engine in ('dagre', 'elk', 'graphviz'):
                    svg = ET.parse(HERE / f'demo/{key}-{engine}.svg').getroot()
                    ids = [a.get('data-topic') for a in svg.iter(f'{{{build.SVG}}}a') if a.get('data-topic')]
                    self.assertCountEqual(ids, graph.nodes)
                    self.assertFalse(list(svg.iter(f'{{{build.SVG}}}foreignObject')))

    def test_shared_descendant_keeps_both_incoming_edges(self):
        data = json.loads((HERE / 'demo/go.json').read_text())
        topic = next(t for t in data['topics'] if t['label'] == 'MySQL')
        self.assertEqual(len([e for e in data['edges'] if e['target'] == topic['id']]), 2)
        self.assertEqual(len([t for t in data['topics'] if t['id'] == topic['id']]), 1)

    def test_ids_are_aliased_and_links_round_trip(self):
        from types import SimpleNamespace
        from urllib.parse import parse_qs
        topic = SimpleNamespace(id='odd & # " id', label='A "quote" & <tag> #hash \n Unicode: 日本語', subjects=(), resources=())
        graph = SimpleNamespace(nodes={topic.id: topic}, edges={})
        ids, _ = build.source_data(graph)
        self.assertEqual(ids[topic.id], 'n0')
        self.assertEqual(parse_qs(build.topic_link('go', topic.id)[1:])['topic'], [topic.id])
        source = build.candidate_source(graph, 'go')
        self.assertNotIn('<tag>', source) if build.CANDIDATE == 'mermaid' else self.assertIn('\\"quote\\"', source)
        self.assertNotIn(topic.id, source)


if __name__ == '__main__':
    unittest.main()
