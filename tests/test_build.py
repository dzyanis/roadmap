from pathlib import Path
import json
import shutil
import struct
import subprocess
import tempfile
import unittest
import xml.etree.ElementTree as ET


REPOSITORY = Path(__file__).resolve().parents[1]


class BuildTests(unittest.TestCase):
    def test_all_roadmaps_build_from_xml(self):
        for tool in ('python3', 'dot', 'make', 'xmllint'):
            self.assertIsNotNone(shutil.which(tool),
                                 f'Install {tool} before running the build tests')

        with tempfile.TemporaryDirectory(prefix='roadmap-build-') as directory:
            workspace = Path(directory)
            for name in ('tools', 'subjects', 'roadmaps', 'schemas'):
                shutil.copytree(REPOSITORY / name, workspace / name,
                                ignore=shutil.ignore_patterns('__pycache__'))
            shutil.copy2(REPOSITORY / 'Makefile', workspace / 'Makefile')
            roadmaps = sorted((workspace / 'roadmaps').glob('*/*/roadmap.xml'))
            self.assertTrue(roadmaps, 'No roadmaps found')

            technology = workspace / 'roadmaps' / 'technologies' / 'example'
            shutil.copytree(workspace / 'roadmaps' / 'foundations' / 'data-structures-algorithms', technology)
            roadmaps = sorted((workspace / 'roadmaps').glob('*/*/roadmap.xml'))
            result = subprocess.run(['make', 'all'], cwd=workspace,
                                    capture_output=True, text=True, timeout=120)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

            for roadmap in roadmaps:
                with self.subTest(roadmap=roadmap.parent.name):
                    data = workspace / 'generated' / roadmap.parent.relative_to(workspace / 'roadmaps')
                    for extension in ('dot', 'svg', 'png', 'md'):
                        output = data / ('guide.md' if extension == 'md' else f'roadmap.{extension}')
                        self.assertTrue(output.is_file(), f'Missing {output}')
                        self.assertGreater(output.stat().st_size, 0, str(output))
                    self.assertTrue((data / 'roadmap.dot').read_text().startswith('digraph roadmap {'))
                    self.assertTrue((data / 'guide.md').read_text().startswith('# '))
                    graph = json.loads((data / 'graph.json').read_text())
                    self.assertEqual(graph['schema_version'], 1)
                    self.assertEqual(graph['roadmap']['id'], roadmap.parent.relative_to(workspace / 'roadmaps').as_posix())
                    self.assertEqual(graph['roadmap']['root'], 'backend')
                    topics = {topic['id'] for topic in graph['topics']}
                    self.assertIn('backend', topics)
                    for edge in graph['edges']:
                        self.assertIn(edge['source'], topics)
                        self.assertIn(edge['target'], topics)
                    # Text exporters must agree with the committed generated artifacts.
                    committed = REPOSITORY / 'generated' / roadmap.parent.relative_to(workspace / 'roadmaps')
                    if committed.is_dir():
                        for filename in ('roadmap.dot', 'guide.md'):
                            self.assertEqual((data / filename).read_bytes(), (committed / filename).read_bytes())
                    svg = ET.parse(data / 'roadmap.svg').getroot()
                    self.assertEqual(svg.tag, '{http://www.w3.org/2000/svg}svg')
                    png = (data / 'roadmap.png').read_bytes()
                    self.assertEqual(png[:8], b'\x89PNG\r\n\x1a\n')
                    self.assertEqual(png[12:16], b'IHDR')
                    width, height = struct.unpack('>II', png[16:24])
                    self.assertGreater(width, 0)
                    self.assertGreater(height, 0)

            for alias in ('go', 'golang', 'java', 'php', 'python', 'ruby', 'devops', 'cs'):
                result = subprocess.run(['make', alias], cwd=workspace, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertNotIn('sh tools/build.sh', result.stdout)

            up_to_date = subprocess.check_output(['make', '-n', 'all'], cwd=workspace, text=True)
            self.assertNotIn('sh tools/build.sh', up_to_date)
            key = roadmaps[0].parent.relative_to(workspace / 'roadmaps')
            (workspace / 'generated' / key / 'graph.json').unlink()
            rebuild = subprocess.check_output(['make', '-n', 'all'], cwd=workspace, text=True)
            self.assertEqual([line for line in rebuild.splitlines() if 'sh tools/build.sh' in line],
                             [f'sh tools/build.sh {key}'])

            subprocess.run(['make', 'clean'], cwd=workspace, check=True, capture_output=True)
            for roadmap in roadmaps:
                self.assertEqual(list((workspace / 'generated' / roadmap.parent.relative_to(workspace / 'roadmaps')).iterdir()), [])


if __name__ == '__main__':
    unittest.main()
