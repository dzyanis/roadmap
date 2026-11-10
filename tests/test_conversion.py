import contextlib
import io
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))

from materials import parsexml
from xmlg2dot import convert_dot
from xmlg2md import convert_md


class ConversionTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.directory = Path(directory.name)

    def write(self, name, contents):
        path = self.directory / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(contents, encoding='utf-8')
        return path

    def test_materials_merge_in_order_and_skip_incomplete_entries(self):
        self.write('resources/first.xml', '''<materials>
            <article><title> First  guide </title>
                <url>
                    https://example.org/
                    first
                </url><tags><tag/><tag> backend </tag></tags>
            </article>
            <book><title/><url>https://example.org/empty</url>
                <tags><tag>backend</tag></tags>
            </book>
            <book><title>Missing URL</title><tags><tag>backend</tag></tags></book>
        </materials>''')
        self.write('resources/nested/second.xml', '''<materials>
            <article><title>Second guide</title><url>https://example.org/second</url>
                <tags><tag>backend</tag><tag>  </tag></tags>
            </article>
        </materials>''')
        self.write('resources/nested.xml', '<materials><include filepath="nested/second.xml"/></materials>')
        materials = self.write('stack/materials.xml', '''<materials>
            <include filepath="../resources/first.xml"/>
            <include filepath="../resources/nested.xml"/>
        </materials>''')
        tags = parsexml(materials)
        self.assertEqual(list(tags), ['backend'])
        self.assertEqual([(item.title, item.url) for item in tags['backend']], [
            ('First guide', 'https://example.org/first'),
            ('Second guide', 'https://example.org/second'),
        ])

    def test_dot_handles_quoted_labels_and_ids_in_included_graphs(self):
        self.write('subject/nodes.xml', r'''<xmlgraph><graph id="g">
            <node id="node" label="Literal \N and &quot;quotes&quot;"/>
            <node id="with spaces" label="Child"/>
        </graph></xmlgraph>''')
        graph = self.write('stack/roadmap.xml', '''<xmlgraph>
            <include filepath="../subject/nodes.xml"/>
            <graph id="g"><edge id="example" source="node" target="with spaces"/></graph>
        </xmlgraph>''')
        dot = self.directory / 'roadmap.dot'
        convert_dot(graph, dot)
        svg = ET.fromstring(subprocess.check_output(['dot', '-Tsvg', str(dot)]))
        text = [element.text for element in svg.iter('{http://www.w3.org/2000/svg}text')]
        self.assertIn(r'Literal \N and "quotes"', text)
        self.assertIn('Child', text)

    def test_markdown_escapes_labels_titles_and_destinations(self):
        roadmap = self.write('roadmap.xml', '''<xmlgraph><graph id="g">
            <node id="backend" label="&lt;Root&gt; #"/>
        </graph></xmlgraph>''')
        materials = self.write('materials.xml', '''<materials>
            <article><title>Guide [v2] (updated) &amp; *details*</title>
                <url>https://example.org/a(b) c?x=1&amp;y=2</url>
                <translate lang="en[US]" url="https://example.org/(translation)"/>
                <tags><tag>backend</tag></tags>
            </article>
        </materials>''')
        with contextlib.redirect_stdout(io.StringIO()) as output:
            convert_md(roadmap, materials, 'backend')
        self.assertIn(r'# \<Root\> \#', output.getvalue())
        self.assertIn(r'[Guide \[v2\] (updated) \& \*details\*]'
                      '(https://example.org/a%28b%29%20c?x=1&amp;y=2)'
                      r'[[en\[US\]](https://example.org/%28translation%29)]',
                      output.getvalue())
