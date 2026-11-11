from pathlib import Path
import shutil
import subprocess
import sys

from xmlg2md import load_roadmap


def validate_schema(schema, files):
    for filepath in files:
        result = subprocess.run(
            ['xmllint', '--nonet', '--noout', '--schema', str(schema), str(filepath)],
            capture_output=True, text=True)
        if result.returncode:
            raise ValueError(result.stderr.strip())


def check_repository():
    if not shutil.which('xmllint'):
        raise ValueError('Install xmllint (libxml2-utils on Ubuntu) before running make check')
    for filename, schema in (('roadmap.xml', 'roadmap.xsd'),
                             ('materials.xml', 'materials.xsd')):
        files = sorted(Path('subjects').rglob(filename)) + sorted(Path('roadmaps').rglob(filename))
        validate_schema(Path('schemas') / schema, files)

    for roadmap in sorted(Path('roadmaps').glob('*/*/roadmap.xml')):
        load_roadmap(roadmap, roadmap.with_name('materials.xml'), 'backend')
    print('Roadmap and materials validation passed')


if __name__ == '__main__':
    try:
        check_repository()
    except ValueError as error:
        sys.exit(str(error))
