import json
from pathlib import Path
import sys
import tempfile
import unittest

REPOSITORY = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY / 'tools'))

import build_site


def graph(**overrides):
    data = {
        'schema_version': 1,
        'roadmap': {'id': 'roles/example', 'label': 'Example', 'root': 'backend'},
        'subjects': [],
        'topics': [
            {'id': 'backend', 'label': 'Example', 'subjects': [], 'resources': []},
            {'id': 'db', 'label': 'Databases', 'subjects': ['databases'], 'resources': [
                {'type': 'book', 'title': 'Guide', 'url': 'https://example.org/guide', 'language': 'en',
                 'description': '', 'translation': None},
            ]},
        ],
        'edges': [{'id': 'backend_db', 'source': 'backend', 'target': 'db', 'type': 'contains'}],
    }
    data.update(overrides)
    return data


class SiteTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix='roadmap-site-')
        self.addCleanup(temporary.cleanup)
        self.directory = Path(temporary.name)
        self.generated = self.directory / 'generated'

    def write_graph(self, roadmap_id, data):
        path = self.generated / roadmap_id / 'graph.json'
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data), encoding='utf-8')

    def test_builds_shell_and_data_for_every_roadmap(self):
        self.write_graph('roles/example', graph())
        output = self.directory / 'site'
        manifest = build_site.build(output, generated=self.generated)

        self.assertEqual([entry['id'] for entry in manifest], ['roles/example'])
        for name in ('index.html', 'app.js', 'style.css', '.nojekyll'):
            self.assertTrue((output / name).is_file(), name)
        for name in ('cytoscape.min.js', 'cytoscape-dagre.min.js', 'dagre.min.js'):
            self.assertTrue((output / 'vendor' / name).is_file(), name)
        self.assertEqual(json.loads((output / 'data' / 'roles' / 'example.json').read_text())['roadmap']['root'],
                         'backend')
        index = json.loads((output / 'data' / 'index.json').read_text())
        self.assertEqual(index[0]['topics'], 2)

    def test_shell_uses_relative_paths_for_github_pages_project_urls(self):
        for name in ('index.html', 'app.js'):
            text = (REPOSITORY / 'site' / name).read_text(encoding='utf-8')
            self.assertNotIn('src="/', text)
            self.assertNotIn('href="/', text)
            self.assertNotIn("fetch('/", text)
            self.assertNotIn('const DATA = \'/', text)

    def test_rejects_unsupported_schema(self):
        self.write_graph('roles/example', graph(schema_version=2))
        with self.assertRaisesRegex(ValueError, 'unsupported schema_version'):
            build_site.build(self.directory / 'site', generated=self.generated)

    def test_rejects_edges_to_unknown_topics(self):
        data = graph(edges=[{'id': 'x', 'source': 'backend', 'target': 'missing', 'type': 'contains'}])
        self.write_graph('roles/example', data)
        with self.assertRaisesRegex(ValueError, "unknown topic 'missing'"):
            build_site.build(self.directory / 'site', generated=self.generated)

    def test_rejects_non_http_resource_urls(self):
        data = graph()
        data['topics'][1]['resources'][0]['url'] = 'javascript:alert(1)'
        self.write_graph('roles/example', data)
        with self.assertRaisesRegex(ValueError, 'resource URL must be http'):
            build_site.build(self.directory / 'site', generated=self.generated)

    def test_rejects_missing_root_topic(self):
        self.write_graph('roles/example', graph(roadmap={'id': 'roles/example', 'label': 'x', 'root': 'nope'}))
        with self.assertRaisesRegex(ValueError, "root 'nope'"):
            build_site.build(self.directory / 'site', generated=self.generated)

    def test_refuses_to_replace_the_repository(self):
        with self.assertRaisesRegex(ValueError, 'Refusing to replace'):
            build_site.build(REPOSITORY, generated=self.generated)

    def test_committed_graphs_build_into_a_site(self):
        output = self.directory / 'committed-site'
        manifest = build_site.build(output)
        committed = sorted(path.parent.relative_to(REPOSITORY / 'generated').as_posix()
                           for path in (REPOSITORY / 'generated').glob('*/*/graph.json'))
        self.assertEqual(sorted(entry['id'] for entry in manifest), committed)
        self.assertTrue(committed, 'Expected committed graph.json files')


if __name__ == '__main__':
    unittest.main()
