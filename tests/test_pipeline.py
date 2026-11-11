import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

REPOSITORY = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY / 'tools'))

from export import export
from graphjson import write_json
from pipeline import load_roadmap
from xmlg2dot import write_dot
from xmlg2md import write_md


class PipelineTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.directory = Path(temporary.name)
        self.subject = self.write('subjects/example/fragments/topics.xml', '''<xmlgraph><graph id="g">
            <node id="a" label="A"/><node id="b" label="B"/>
            <node id="shared" label="Shared λ"/><node id="orphan" label="Orphan"/>
            <edge id="a-shared" source="a" target="shared"/>
            <edge id="b-shared" source="b" target="shared"/>
        </graph></xmlgraph>''')
        self.write('subjects/example/roadmap.xml', '''<xmlgraph>
            <include filepath="fragments/topics.xml"/>
        </xmlgraph>''')
        self.resources = self.write('subjects/example/fragments/resources.xml', '''<materials>
            <book lang="en"><title> Shared   resource </title>
                <url>https://example.org/
                guide</url><description> A   description </description>
                <translate lang="pl" url="https://example.org/pl"/>
                <tags><tag>shared</tag><tag>a</tag></tags>
            </book>
            <article lang="pl"><title>Second</title><url>https://example.org/second</url>
                <tags><tag>shared</tag></tags>
            </article>
        </materials>''')
        self.write('subjects/example/materials.xml', '''<materials>
            <include filepath="fragments/resources.xml"/>
        </materials>''')
        self.graph = self.write('roadmaps/roles/demo/roadmap.xml', '''<xmlgraph>
            <graph id="root">
                <edge id="root-b" source="backend" target="b"/>
                <edge id="root-a" source="backend" target="a"/>
                <node id="backend" label="Demo"/>
            </graph>
            <include filepath="../../../subjects/example/roadmap.xml"/>
        </xmlgraph>''')
        self.materials = self.write('roadmaps/roles/demo/materials.xml', '''<materials>
            <include filepath="../../../subjects/example/materials.xml"/>
        </materials>''')

    def write(self, filename, contents):
        path = self.directory / filename
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(contents, encoding='utf-8')
        return path

    def load(self):
        return load_roadmap(self.graph, self.materials, 'backend')

    def test_nested_includes_membership_and_resource_resolution(self):
        graph = self.load()
        self.assertEqual((graph.id, graph.root, graph.subjects), ('roles/demo', 'backend', ('example',)))
        self.assertEqual(graph.nodes['backend'].subjects, ())
        self.assertEqual(graph.nodes['backend'].childrenids, ('b', 'a'))
        topic = graph.nodes['shared']
        self.assertEqual(topic.subjects, ('example',))
        self.assertEqual([resource.title for resource in topic.resources], ['Shared resource', 'Second'])
        self.assertEqual(topic.resources[0].url, 'https://example.org/guide')
        self.assertEqual(topic.resources[0].description, 'A description')
        self.assertEqual(topic.resources[0].language, 'en')
        self.assertEqual(topic.resources[0].translate_lang, 'pl')
        self.assertIs(topic.resources[0], graph.nodes['a'].resources[0])

    def test_all_writers_use_the_same_model_and_preserve_shared_descendants(self):
        graph = self.load()
        dot, markdown, output = io.StringIO(), io.StringIO(), io.StringIO()
        with patch('xmlincludes.ET.parse', side_effect=AssertionError('Exporter read XML')):
            write_dot(graph, dot)
            write_md(graph, markdown)
            write_json(graph, output)
        data = json.loads(output.getvalue())
        self.assertEqual({topic['id'] for topic in data['topics']}, set(graph.nodes))
        self.assertEqual({edge['id'] for edge in data['edges']}, set(graph.edges))
        self.assertEqual(sum(edge['target'] == 'shared' for edge in data['edges']), 2)
        for edge in graph.edges.values():
            self.assertIn(f'{edge.source}->{edge.target};', dot.getvalue())
        self.assertIn('orphan [ label="Orphan" ];', dot.getvalue())
        self.assertEqual(markdown.getvalue().count('### Shared λ\n'), 2)
        self.assertLess(markdown.getvalue().index('## B'), markdown.getvalue().index('## A'))
        self.assertEqual(markdown.getvalue().count('[Shared resource]'), 3)
        shared = next(topic for topic in data['topics'] if topic['id'] == 'shared')
        self.assertEqual(shared['resources'][0]['translation'],
                         {'language': 'pl', 'url': 'https://example.org/pl'})
        self.assertIsNone(shared['resources'][1]['translation'])
        self.assertTrue(all(edge['type'] == 'contains' for edge in data['edges']))

    def test_json_is_deterministic_across_runs_and_checkout_locations(self):
        first, second, relocated = io.StringIO(), io.StringIO(), io.StringIO()
        write_json(self.load(), first)
        write_json(self.load(), second)
        with tempfile.TemporaryDirectory() as destination:
            copy = Path(destination) / 'checkout'
            shutil.copytree(self.directory, copy)
            graph = load_roadmap(copy / self.graph.relative_to(self.directory),
                                 copy / self.materials.relative_to(self.directory), 'backend')
            write_json(graph, relocated)
        self.assertEqual(first.getvalue(), second.getvalue())
        self.assertEqual(first.getvalue(), relocated.getvalue())
        self.assertNotIn(str(self.directory), first.getvalue())
        data = json.loads(first.getvalue())
        self.assertEqual([topic['id'] for topic in data['topics']], sorted(graph.nodes))
        self.assertEqual([edge['id'] for edge in data['edges']], sorted(graph.edges))

    def test_invalid_nested_inputs_fail_before_any_export(self):
        changes = [
            (self.subject, 'label="Shared λ"', '', 'label'),
            (self.subject, 'target="shared"', 'target="absent"', 'unknown target'),
            (self.subject, 'source="a" target="shared"', 'source="shared" target="b"', 'roadmap cycle'),
            (self.subject, 'id="orphan"', 'id="a"', 'duplicate node ID'),
            (self.subject, 'id="a-shared"', 'id="a-shared" type="related-to"', 'type'),
            (self.resources, '<tag>shared</tag>', '<tag>absent</tag>', 'material tag'),
            (self.resources, 'lang="en"', '', 'lang'),
            (self.graph, '<include filepath="../../../subjects/example/roadmap.xml"/>',
             '<include filepath="roadmap.xml"/>', 'XML include cycle'),
            (self.graph, 'id="backend"', 'id="wrong-root"', 'unknown source'),
        ]
        output = self.directory / 'output'
        output.mkdir()
        for path, before, after, error in changes:
            original = path.read_text()
            with self.subTest(error=error):
                path.write_text(original.replace(before, after))
                try:
                    with self.assertRaisesRegex(ValueError, error):
                        export(self.graph, self.materials, 'backend', output)
                    self.assertEqual(list(output.iterdir()), [])
                finally:
                    path.write_text(original)
        with self.assertRaisesRegex(ValueError, 'unknown root'):
            load_roadmap(self.graph, self.materials, 'absent')

    def test_build_does_not_publish_invalid_input(self):
        for name in ('tools', 'schemas'):
            shutil.copytree(REPOSITORY / name, self.directory / name)
        output = self.directory / 'generated/roles/demo'
        output.mkdir(parents=True)
        filenames = ('roadmap.dot', 'roadmap.svg', 'roadmap.png', 'guide.md', 'graph.json')
        for filename in filenames:
            (output / filename).write_text('previous build')
        self.resources.write_text(self.resources.read_text().replace('<tag>shared</tag>', '<tag>absent</tag>'))
        result = subprocess.run(['sh', 'tools/build.sh', 'roles/demo'], cwd=self.directory,
                                capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('material tag', result.stderr)
        for filename in filenames:
            self.assertEqual((output / filename).read_text(), 'previous build')
        self.assertFalse(list(output.glob('.roadmap.*')))
