from pathlib import Path
import re
import unittest
import xml.etree.ElementTree as ET


REPOSITORY = Path(__file__).resolve().parents[1]


class LayoutTests(unittest.TestCase):
    def test_xml_schema_locations_resolve_after_directory_moves(self):
        attribute = '{http://www.w3.org/2001/XMLSchema-instance}noNamespaceSchemaLocation'
        for directory in ('subjects', 'roadmaps'):
            for xml in (REPOSITORY / directory).rglob('*.xml'):
                with self.subTest(xml=xml.relative_to(REPOSITORY)):
                    location = ET.parse(xml).getroot().get(attribute)
                    self.assertIsNotNone(location)
                    schema = (xml.parent / location).resolve()
                    self.assertEqual(schema.parent, REPOSITORY / 'schemas')
                    self.assertTrue(schema.is_file(), str(schema))

    def test_navigation_links_resolve_to_migrated_content(self):
        pages = [REPOSITORY / 'README.md', *(REPOSITORY / 'stacks').glob('*/README.md')]
        for page in pages:
            for destination in re.findall(r'\]\(([^)]+)\)', page.read_text()):
                if '://' in destination or destination.startswith('#'):
                    continue
                with self.subTest(page=page.name, destination=destination):
                    self.assertTrue((page.parent / destination).exists(), destination)
