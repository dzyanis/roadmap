from pathlib import Path
import subprocess
import sys
import unittest
import xml.etree.ElementTree as ET


REPOSITORY = Path(__file__).resolve().parents[1]
STACKS = sorted((REPOSITORY / 'stacks').glob('*/roadmap.xml'))


class MaterialsCoverageTests(unittest.TestCase):
    def test_stack_subjects_include_available_materials(self):
        self.assertTrue(STACKS, 'No stack roadmaps found')
        for roadmap in STACKS:
            materials_file = roadmap.with_name('materials.xml')
            included_materials = {
                (REPOSITORY / include.get('filepath')).resolve()
                for include in ET.parse(materials_file).getroot().findall('include')
            }
            for include in ET.parse(roadmap).getroot().findall('include'):
                subject = REPOSITORY / include.get('filepath')
                available_materials = subject.with_name('materials.xml')
                with self.subTest(stack=roadmap.parent.name, subject=subject.parent.name):
                    if available_materials.is_file():
                        self.assertIn(available_materials.resolve(), included_materials,
                                      f'{materials_file} omits {available_materials}')

    def test_os_resources_appear_under_their_matching_headings(self):
        subject = REPOSITORY / 'subjects' / 'os'
        labels = {
            node.get('id'): node.get('label')
            for node in ET.parse(subject / 'roadmap.xml').iter('node')
        }
        resources = []
        for material in ET.parse(subject / 'materials.xml').getroot():
            for tag in material.findall('tags/tag'):
                resources.append((labels[tag.text], material.findtext('title'),
                                  material.findtext('url')))
        self.assertTrue(resources, 'No OS materials found')

        for roadmap in STACKS:
            result = subprocess.run(
                [sys.executable, str(REPOSITORY / 'tools' / 'xmlg2md.py'),
                 '--xmlg', str(roadmap),
                 '--materials', str(roadmap.with_name('materials.xml')),
                 '--root', 'backend'], cwd=REPOSITORY,
                capture_output=True, text=True, timeout=30)
            self.assertEqual(result.returncode, 0, result.stderr)
            sections = {}
            heading = None
            for line in result.stdout.splitlines():
                if line.startswith('#'):
                    heading = line.lstrip('#').strip()
                    sections.setdefault(heading, [])
                elif heading is not None:
                    sections[heading].append(line)
            for heading, title, url in resources:
                with self.subTest(stack=roadmap.parent.name, resource=title):
                    self.assertIn(f'[{title}]({url})', '\n'.join(sections.get(heading, [])))


if __name__ == '__main__':
    unittest.main()
