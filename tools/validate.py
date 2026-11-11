from pathlib import Path
import sys

from pipeline import load_roadmap
from xmlvalidation import validate_schema


def check_repository():
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
