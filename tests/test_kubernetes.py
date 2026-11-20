"""Integration checks for selective shared topics and Kubernetes learning resources."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from pipeline import load_roadmap
import build_site


class KubernetesTests(unittest.TestCase):
    def test_subject_is_reusable_and_every_branch_has_resources(self):
        path = ROOT / 'subjects/kubernetes'
        graph = load_roadmap(path / 'roadmap.xml', path / 'materials.xml', 'dev_orchestration_k8s')
        for topic in graph.nodes.values():
            with self.subTest(topic=topic.id):
                self.assertTrue(topic.resources, 'Topic has no learning resources')

    def test_selected_prerequisites_reuse_their_definitions(self):
        path = ROOT / 'roadmaps/technologies/kubernetes'
        graph = load_roadmap(path / 'roadmap.xml', path / 'materials.xml', 'backend')
        selected = {'operating-systems': ['os_processes_lifecycle', 'os_linux_processes', 'os_shell_bash'],
                    'networking': ['net_dns', 'net_protocols_ip', 'net_protocols_tcp'],
                    'devops': ['devops_containers_1'],
                    'software-development': ['dev_orchestration_k8s']}
        for subject, ids in selected.items():
            original = load_roadmap(ROOT / 'subjects' / subject / 'roadmap.xml')
            for topic_id in ids:
                with self.subTest(topic=topic_id):
                    self.assertEqual(graph.nodes[topic_id].label, original.nodes[topic_id].label)
                    self.assertEqual(graph.nodes[topic_id].subjects, (subject,))
                    self.assertTrue(graph.nodes[topic_id].resources)
        self.assertNotIn('db', graph.nodes)
        self.assertNotIn('dev', graph.nodes)
        self.assertNotIn('devops_cloud', graph.nodes)
        seen = set()
        def visit(key):
            if key in seen:
                return
            seen.add(key)
            for child in graph.nodes[key].childrenids:
                visit(child)
        visit('backend')
        self.assertEqual(seen, set(graph.nodes))
        self.assertEqual(len(graph.nodes['k8s_practice'].childrenids), 7)
        for topic_id in graph.nodes['k8s_practice'].childrenids:
            self.assertTrue(graph.nodes[topic_id].resources)

    def test_site_discovers_technology_roadmap_and_preserves_topic_links(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / 'site'
            manifest = build_site.build(output)
            self.assertIn('technologies/kubernetes', [entry['id'] for entry in manifest])
            data = json.loads((output / 'data/technologies/kubernetes.json').read_text())
            self.assertEqual(data['roadmap']['label'], 'Kubernetes')
            self.assertIn('dev_orchestration_k8s', {t['id'] for t in data['topics']})
