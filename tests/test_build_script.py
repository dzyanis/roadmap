import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


BUILD_SCRIPT = Path(__file__).resolve().parents[1] / 'tools' / 'build.sh'


class BuildScriptTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.bin = self.root / 'bin'
        self.bin.mkdir()
        self.data = self.root / 'generated' / 'roles' / 'go-engineer'
        self.data.mkdir(parents=True)
        self.markdown = self.data / 'guide.md'
        self.outputs = ('roadmap.dot', 'roadmap.svg', 'roadmap.png', 'guide.md', 'graph.json')
        for filename in self.outputs:
            (self.data / filename).write_text(f'Existing {filename}\n')
        source = self.root / 'roadmaps' / 'roles' / 'go-engineer'
        source.mkdir(parents=True)
        for filename in ('roadmap.xml', 'materials.xml'):
            (source / filename).touch()
        self.log = self.root / 'calls.log'

    def tool(self, name, script):
        path = self.bin / name
        path.write_text('#!/bin/sh\n' + script)
        path.chmod(0o755)

    def install_tools(self):
        for name in ('mkdir', 'mktemp', 'mv', 'rm'):
            (self.bin / name).symlink_to(shutil.which(name))
        self.tool('python3', '''
printf 'python3 %s\n' "$*" >> "$BUILD_TEST_LOG"
if [ "$BUILD_TEST_FAIL" = exporter ]; then exit 7; fi
for arg in "$@"; do
  case "$arg" in --output=*) staging=${arg#--output=} ;; esac
done
printf 'New DOT\n' > "$staging/roadmap.dot"
printf 'New Markdown\n' > "$staging/guide.md"
printf 'New JSON\n' > "$staging/graph.json"
''')
        self.tool('xmllint', 'exit 0\n')
        self.tool('dot', '''
printf 'dot %s\n' "$*" >> "$BUILD_TEST_LOG"
if [ "$BUILD_TEST_FAIL" = "$1" ]; then exit 7; fi
printf 'New image\n' > "$4"
''')

    def build(self, fail=''):
        environment = dict(os.environ, PATH=str(self.bin),
                           BUILD_TEST_LOG=str(self.log), BUILD_TEST_FAIL=fail)
        return subprocess.run(['/bin/sh', str(BUILD_SCRIPT), 'roles/go-engineer'],
                              cwd=self.root, env=environment,
                              capture_output=True, text=True)

    def test_missing_dependencies_fail_before_changing_outputs(self):
        for missing in ('python3', 'dot', 'xmllint'):
            with self.subTest(tool=missing):
                for tool in self.bin.iterdir():
                    tool.unlink()
                for name in ('python3', 'dot', 'xmllint'):
                    if name != missing:
                        self.tool(name, 'exit 0\n')
                result = self.build()
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(f"required tool '{missing}'", result.stderr)
                self.assertIn('Install Python 3 and Graphviz', result.stderr)
                self.assertEqual(self.markdown.read_text(), 'Existing guide.md\n')
                self.assertFalse(self.log.exists())

    def test_each_failed_step_stops_the_build(self):
        self.install_tools()
        stages = ('exporter', '-Tsvg', '-Tpng')
        for expected_calls, stage in enumerate(stages, start=1):
            with self.subTest(stage=stage):
                self.log.write_text('')
                result = self.build(fail=stage)
                self.assertEqual(result.returncode, 7)
                self.assertEqual(len(self.log.read_text().splitlines()), expected_calls)
                self.assertNotIn('Check generated/roles/go-engineer/guide.md', result.stdout)
                for filename in self.outputs:
                    self.assertEqual((self.data / filename).read_text(), f'Existing {filename}\n')
                self.assertFalse(list(self.data.glob('.roadmap.*')))

    def test_success_runs_every_step_in_order(self):
        self.install_tools()
        result = self.build()
        self.assertEqual(result.returncode, 0, result.stderr)
        calls = self.log.read_text().splitlines()
        self.assertEqual(len(calls), 3)
        self.assertTrue(calls[0].startswith('python3 ./tools/export.py '))
        self.assertTrue(calls[1].startswith('dot -Tsvg '))
        self.assertTrue(calls[2].startswith('dot -Tpng '))
        self.assertIn('Check generated/roles/go-engineer/guide.md', result.stdout)
        self.assertEqual(self.markdown.read_text(), 'New Markdown\n')
        self.assertEqual((self.data / 'graph.json').read_text(), 'New JSON\n')


if __name__ == '__main__':
    unittest.main()
