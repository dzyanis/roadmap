from pathlib import Path
import shutil
import struct
import subprocess
import tempfile
import unittest
import xml.etree.ElementTree as ET


REPOSITORY = Path(__file__).resolve().parents[1]


class BuildTests(unittest.TestCase):
    def test_all_stacks_build_from_xml(self):
        for tool in ('python3', 'dot', 'make'):
            self.assertIsNotNone(shutil.which(tool),
                                 f'Install {tool} before running the build tests')

        with tempfile.TemporaryDirectory(prefix='roadmap-build-') as directory:
            workspace = Path(directory)
            for name in ('tools', 'subjects', 'stacks'):
                shutil.copytree(REPOSITORY / name, workspace / name,
                                ignore=shutil.ignore_patterns('data', '__pycache__'))
            shutil.copy2(REPOSITORY / 'Makefile', workspace / 'Makefile')
            stacks = sorted((workspace / 'stacks').glob('*/roadmap.xml'))
            self.assertTrue(stacks, 'No stack roadmaps found')
            for roadmap in stacks:
                (roadmap.parent / 'data').mkdir()

            result = subprocess.run(['make', 'all'], cwd=workspace,
                                    capture_output=True, text=True, timeout=120)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

            for roadmap in stacks:
                with self.subTest(stack=roadmap.parent.name):
                    data = roadmap.parent / 'data'
                    for extension in ('dot', 'svg', 'png', 'md'):
                        output = data / f'roadmap.{extension}'
                        self.assertTrue(output.is_file(), f'Missing {output}')
                        self.assertGreater(output.stat().st_size, 0, str(output))
                    self.assertTrue((data / 'roadmap.dot').read_text().startswith('digraph roadmap {'))
                    self.assertTrue((data / 'roadmap.md').read_text().startswith('# '))
                    svg = ET.parse(data / 'roadmap.svg').getroot()
                    self.assertEqual(svg.tag, '{http://www.w3.org/2000/svg}svg')
                    png = (data / 'roadmap.png').read_bytes()
                    self.assertEqual(png[:8], b'\x89PNG\r\n\x1a\n')
                    self.assertEqual(png[12:16], b'IHDR')
                    width, height = struct.unpack('>II', png[16:24])
                    self.assertGreater(width, 0)
                    self.assertGreater(height, 0)


if __name__ == '__main__':
    unittest.main()
