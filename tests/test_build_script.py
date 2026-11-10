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
        self.data = self.root / 'stacks' / 'go' / 'data'
        self.data.mkdir(parents=True)
        self.markdown = self.data / 'roadmap.md'
        for extension in ('dot', 'svg', 'png', 'md'):
            (self.data / f'roadmap.{extension}').write_text(f'Existing {extension}\n')
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
case "$1" in
  ./tools/xmlg2dot.py) stage=dot-converter ;;
  ./tools/xmlg2md.py) stage=markdown-converter ;;
esac
if [ "$BUILD_TEST_FAIL" = "$stage" ]; then exit 7; fi
case "$stage" in
  dot-converter) printf 'New DOT\n' > "${3#--dot=}" ;;
  markdown-converter) printf 'New Markdown\n' ;;
esac
''')
        self.tool('dot', '''
printf 'dot %s\n' "$*" >> "$BUILD_TEST_LOG"
if [ "$BUILD_TEST_FAIL" = "$1" ]; then exit 7; fi
printf 'New image\n' > "$4"
''')

    def build(self, fail=''):
        environment = dict(os.environ, PATH=str(self.bin),
                           BUILD_TEST_LOG=str(self.log), BUILD_TEST_FAIL=fail)
        return subprocess.run(['/bin/sh', str(BUILD_SCRIPT), 'go'],
                              cwd=self.root, env=environment,
                              capture_output=True, text=True)

    def test_missing_dependencies_fail_before_changing_outputs(self):
        for missing in ('python3', 'dot'):
            with self.subTest(tool=missing):
                for tool in self.bin.iterdir():
                    tool.unlink()
                if missing == 'dot':
                    self.tool('python3', 'exit 0\n')
                result = self.build()
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(f"required tool '{missing}'", result.stderr)
                self.assertIn('Install Python 3 and Graphviz', result.stderr)
                self.assertEqual(self.markdown.read_text(), 'Existing md\n')
                self.assertFalse(self.log.exists())

    def test_each_failed_step_stops_the_build(self):
        self.install_tools()
        stages = ('dot-converter', '-Tsvg', '-Tpng', 'markdown-converter')
        for expected_calls, stage in enumerate(stages, start=1):
            with self.subTest(stage=stage):
                self.log.write_text('')
                result = self.build(fail=stage)
                self.assertEqual(result.returncode, 7)
                self.assertEqual(len(self.log.read_text().splitlines()), expected_calls)
                self.assertNotIn('Check stacks/go/data/roadmap.md', result.stdout)
                for extension in ('dot', 'svg', 'png', 'md'):
                    self.assertEqual((self.data / f'roadmap.{extension}').read_text(),
                                     f'Existing {extension}\n')
                self.assertFalse(list(self.data.glob('.roadmap.*')))

    def test_success_runs_every_step_in_order(self):
        self.install_tools()
        result = self.build()
        self.assertEqual(result.returncode, 0, result.stderr)
        calls = self.log.read_text().splitlines()
        self.assertEqual(len(calls), 4)
        self.assertTrue(calls[0].startswith('python3 ./tools/xmlg2dot.py '))
        self.assertTrue(calls[1].startswith('dot -Tsvg '))
        self.assertTrue(calls[2].startswith('dot -Tpng '))
        self.assertTrue(calls[3].startswith('python3 ./tools/xmlg2md.py '))
        self.assertIn('Check stacks/go/data/roadmap.md', result.stdout)
        self.assertEqual(self.markdown.read_text(), 'New Markdown\n')


if __name__ == '__main__':
    unittest.main()
