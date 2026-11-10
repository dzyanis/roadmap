import contextlib
import io
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))

from xmlgraph import Roadmap
from xmlg2dot import convert_dot
from xmlg2md import convert_md


class RoadmapTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)

    def write_graph(self, name, contents):
        path = self.root / name
        path.write_text('<xmlgraph>' + contents + '</xmlgraph>')
        return str(path)

    def test_edges_before_nodes_work_in_both_converters(self):
        path = self.write_graph('roadmap.xml', '''
            <graph id="roadmap">
                <edge id="first" source="backend" target="child"/>
                <node id="child" label="Child"/>
                <node id="backend" label="Root"/>
            </graph>
        ''')
        roadmap = Roadmap(path)
        self.assertEqual(roadmap.nodes['backend'].childrenids, ['child'])
        dot = self.root / 'roadmap.dot'
        convert_dot(path, str(dot))
        self.assertIn('backend->child;', dot.read_text())
        materials = self.root / 'materials.xml'
        materials.write_text('<materials/>')
        with contextlib.redirect_stdout(io.StringIO()) as captured:
            convert_md(path, str(materials), 'backend')
        self.assertEqual(captured.getvalue(), '# Root\n\n## Child\n\n')

    def test_edges_can_reference_nodes_in_later_nested_includes(self):
        nodes = self.write_graph('nodes.xml', '''
            <graph id="nodes">
                <node id="backend" label="Root"/>
                <node id="child" label="Child"/>
            </graph>
        ''')
        nested = self.write_graph('nested.xml', f'<include filepath="{nodes}"/>')
        edges = self.write_graph('edges.xml', '''
            <graph id="edges">
                <edge id="first" source="backend" target="child"/>
            </graph>
        ''')
        path = self.write_graph('roadmap.xml', f'''
            <include filepath="{edges}"/>
            <include filepath="{nested}"/>
        ''')
        self.assertEqual(Roadmap(path).nodes['backend'].childrenids, ['child'])

    def test_child_order_and_shared_descendants_are_preserved(self):
        path = self.write_graph('roadmap.xml', '''
            <graph id="roadmap">
                <edge id="second" source="backend" target="b"/>
                <edge id="first" source="backend" target="a"/>
                <edge id="shared" source="b" target="a"/>
                <node id="backend" label="Root"/>
                <node id="a" label="A"/>
                <node id="b" label="B"/>
            </graph>
        ''')
        roadmap = Roadmap(path)
        self.assertEqual(roadmap.nodes['backend'].childrenids, ['b', 'a'])
        self.assertEqual(roadmap.nodes['b'].childrenids, ['a'])

    def test_adding_a_file_does_not_duplicate_existing_children(self):
        first = self.write_graph('first.xml', '''
            <graph id="first">
                <node id="backend" label="Root"/>
                <node id="a" label="A"/>
                <edge id="first" source="backend" target="a"/>
            </graph>
        ''')
        second = self.write_graph('second.xml', '''
            <graph id="second">
                <edge id="second" source="backend" target="b"/>
                <node id="b" label="B"/>
            </graph>
        ''')
        roadmap = Roadmap(first)
        roadmap.add_from_file(second)
        self.assertEqual(roadmap.nodes['backend'].childrenids, ['a', 'b'])

    def test_unknown_endpoints_report_edge_and_node(self):
        for endpoint in ('source', 'target'):
            with self.subTest(endpoint=endpoint):
                source = 'missing' if endpoint == 'source' else 'backend'
                target = 'missing' if endpoint == 'target' else 'backend'
                path = self.write_graph('invalid.xml', f'''
                    <graph id="invalid">
                        <edge id="broken" source="{source}" target="{target}"/>
                        <node id="backend" label="Root"/>
                    </graph>
                ''')
                with self.assertRaisesRegex(
                        ValueError, f"Edge 'broken' references unknown {endpoint} node 'missing'"):
                    Roadmap(path)


if __name__ == '__main__':
    unittest.main()
