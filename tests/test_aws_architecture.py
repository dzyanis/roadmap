"""Keep AWS knowledge, neutral architecture and role composition independently usable."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from pipeline import load_roadmap
import build_site


def load(path, root):
    return load_roadmap(path / 'roadmap.xml', path / 'materials.xml', root)


class AWSArchitectureTests(unittest.TestCase):
    def test_subjects_stand_alone_with_resources_and_no_role_dependency(self):
        for name, root in [('architecture', 'arch'), ('aws', 'aws')]:
            graph = load(ROOT / 'subjects' / name, root)
            with self.subTest(subject=name):
                self.assertNotIn('backend', graph.nodes)
                self.assertNotIn('aws' if name == 'architecture' else 'arch', graph.nodes)
                for topic in graph.nodes.values():
                    self.assertTrue(topic.resources, topic.id)
                if name == 'architecture':
                    self.assertNotIn('aws', graph.subjects)
                    self.assertFalse(any(key.startswith('aws_') for key in graph.nodes))

    def test_role_reuses_shared_topics_without_unrelated_branches(self):
        graph = load(ROOT / 'roadmaps/roles/aws-solutions-architect', 'backend')
        selected = {'databases': ['db_distributed_replication', 'db_distributed_sharding',
                                  'db_distributed_consistency', 'db_message_broker_awssqs'],
                    'devops': ['devops_reliability_1', 'devops_reliability_3', 'devops_containers_1'],
                    'operating-systems': ['os_processes_lifecycle', 'os_linux_processes', 'os_shell_bash'],
                    'networking': ['net_dns', 'net_protocols_ip', 'net_protocols_tcp']}
        for subject, ids in selected.items():
            original = load_roadmap(ROOT / 'subjects' / subject / 'roadmap.xml')
            for key in ids:
                with self.subTest(topic=key):
                    self.assertEqual(graph.nodes[key].label, original.nodes[key].label)
                    self.assertEqual(graph.nodes[key].subjects, (subject,))
                    self.assertTrue(graph.nodes[key].resources)
        for unrelated in ['db', 'os', 'devops', 'dev', 'dev_orchestration_k8s']:
            self.assertNotIn(unrelated, graph.nodes)
        seen = set()
        def visit(key):
            if key in seen:
                return
            seen.add(key)
            for child in graph.nodes[key].childrenids:
                visit(child)
        visit('backend')
        self.assertEqual(seen, set(graph.nodes))
        self.assertEqual(len(graph.nodes['sa_practice'].childrenids), 3)
        for key in graph.nodes['sa_practice'].childrenids:
            self.assertTrue(graph.nodes[key].resources)

    def test_site_discovers_architect_role(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / 'site'
            manifest = build_site.build(output)
            self.assertIn('roles/aws-solutions-architect', [entry['id'] for entry in manifest])
            data = json.loads((output / 'data/roles/aws-solutions-architect.json').read_text())
            self.assertEqual(data['roadmap']['label'], 'AWS Solutions Architect')
            ids = {t['id'] for t in data['topics']}
            self.assertTrue({'arch', 'aws', 'db_message_broker_awssqs'} <= ids)
