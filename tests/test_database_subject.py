"""Check database classification and resource boundaries independently of consumers."""
from pathlib import Path
import sys
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from pipeline import load_roadmap


class DatabaseSubjectTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subject = ROOT / 'subjects/databases'
        cls.graph = load_roadmap(subject / 'roadmap.xml', subject / 'materials.xml', 'db')

    def test_products_are_separate_from_concurrency_mechanisms(self):
        nodes = self.graph.nodes
        self.assertIn('db_nosql_redis', nodes['db_nosql_keyvalue'].childrenids)
        self.assertIn('db_nosql_clickhouse', nodes['db_nosql_colbase'].childrenids)
        self.assertIn('db_nosql_colbase', nodes['db_analytics'].childrenids)
        for mechanism in ('db_relational_mvcc', 'db_relational_blocking', 'db_relational_acid'):
            self.assertIn(mechanism, nodes['db_transactions'].childrenids)
            self.assertFalse(nodes[mechanism].childrenids)
        self.assertEqual(nodes['db_search_elasticseaerch'].label, 'Elasticsearch')

    def test_major_branches_have_free_resources_and_all_topics_are_reachable(self):
        nodes = self.graph.nodes
        seen = set()
        def visit(key):
            if key in seen:
                return
            seen.add(key)
            for child in nodes[key].childrenids:
                visit(child)
        visit('db')
        self.assertEqual(seen, set(nodes))
        for key in list(nodes['db'].childrenids) + ['db_relational', 'db_nosql', 'db_analytics', 'db_search', 'db_message_broker']:
            with self.subTest(branch=key):
                self.assertTrue(any(r.type == 'article' and r.url.startswith('https://')
                                    for r in nodes[key].resources))

    def test_kubernetes_book_belongs_to_development_only(self):
        matches = []
        for path in (ROOT / 'subjects').glob('*/materials.xml'):
            for material in ET.parse(path).getroot():
                if material.findtext('title') == 'Kubernetes in Action':
                    matches.append((path.parent.name, material.findtext('tags/tag')))
        self.assertEqual(matches, [('software-development', 'dev_orchestration_k8s')])
