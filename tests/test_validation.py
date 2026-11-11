import contextlib
import io
from pathlib import Path
import sys
import tempfile
import unittest

TOOLS = Path(__file__).resolve().parents[1] / 'tools'
sys.path.insert(0, str(TOOLS))

from materials import parsexml
from validate import validate_schema
from xmlg2md import convert_md
from xmlgraph import Roadmap


class ValidationTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.directory = Path(directory.name)

    def write_xml(self, filename, content):
        path = self.directory / filename
        path.write_text(content)
        return path

    def test_schema_errors_name_file_and_missing_field(self):
        for schema, content, field in (
            ('roadmap.xsd', '<xmlgraph><graph id="g"><node id="a"/></graph></xmlgraph>', 'label'),
            ('materials.xsd', '<materials><book lang="en"><title>A</title>'
             '<tags><tag>a</tag></tags></book></materials>', 'url'),
        ):
            with self.subTest(schema=schema):
                path = self.write_xml('invalid.xml', content)
                with self.assertRaises(ValueError) as failure:
                    validate_schema(TOOLS.parent / 'schemas' / schema, [path])
                self.assertIn(str(path), str(failure.exception))
                self.assertIn(field, str(failure.exception))

    def test_duplicate_ids_across_includes_report_both_definitions(self):
        for kind, element in (
            ('node', '<node id="duplicate" label="Example"/>'),
            ('edge', '<edge id="duplicate" source="a" target="b"/>'),
        ):
            with self.subTest(kind=kind):
                contents = f'<xmlgraph><graph id="g">{element}</graph></xmlgraph>'
                first = self.write_xml('first.xml', contents)
                second = self.write_xml('second.xml', contents)
                roadmap = self.write_xml('roadmap.xml', f'<xmlgraph>'
                                         f'<include filepath="{first}"/>'
                                         f'<include filepath="{second}"/></xmlgraph>')
                with self.assertRaisesRegex(ValueError, f"duplicate {kind} ID 'duplicate'") as failure:
                    Roadmap(roadmap)
                self.assertIn(str(first), str(failure.exception))
                self.assertIn(str(second), str(failure.exception))

    def test_include_cycles_report_the_chain_for_both_parsers(self):
        for root, parse in (('xmlgraph', Roadmap), ('materials', parsexml)):
            with self.subTest(root=root):
                first = self.directory / 'first.xml'
                second = self.write_xml('second.xml', f'<{root}><include filepath="{first}"/></{root}>')
                self.write_xml('first.xml', f'<{root}><include filepath="{second}"/></{root}>')
                with self.assertRaises(ValueError) as failure:
                    parse(first)
                self.assertIn(f'XML include cycle: {first.resolve()} -> {second.resolve()} -> '
                              f'{first.resolve()}', str(failure.exception))

    def test_graph_cycle_is_rejected_before_markdown_output(self):
        roadmap = self.write_xml('roadmap.xml', '''<xmlgraph><graph id="g">
            <node id="backend" label="Root"/>
            <node id="a" label="A"/>
            <node id="b" label="B"/>
            <edge id="ab" source="a" target="b"/>
            <edge id="ba" source="b" target="a"/>
        </graph></xmlgraph>''')
        materials = self.write_xml('materials.xml', '<materials/>')
        with contextlib.redirect_stdout(io.StringIO()) as output:
            with self.assertRaisesRegex(ValueError, r'roadmap cycle: (a -> b -> a|b -> a -> b)'):
                convert_md(roadmap, materials, 'backend')
        self.assertEqual(output.getvalue(), '')

    def test_markdown_checks_root_and_material_tags(self):
        roadmap = self.write_xml('roadmap.xml', '<xmlgraph><graph id="g">'
                                 '<node id="backend" label="Root"/></graph></xmlgraph>')
        subject = self.write_xml('subject-materials.xml', '''<materials><book lang="en">
            <title>Book</title><url>https://example.org</url>
            <tags><tag>absent</tag></tags>
        </book></materials>''')
        materials = self.write_xml('materials.xml', f'<materials><include filepath="{subject}"/></materials>')
        with self.assertRaisesRegex(ValueError, "unknown root node 'absent'"):
            convert_md(roadmap, materials, 'absent')
        with self.assertRaisesRegex(ValueError, "material tag 'absent' has no node") as failure:
            convert_md(roadmap, materials, 'backend')
        self.assertIn(str(subject), str(failure.exception))
        self.assertIn(str(roadmap), str(failure.exception))
