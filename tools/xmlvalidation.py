"""Schema validation shared by repository checks and assembled-model loading."""

from pathlib import Path
import shutil
import subprocess


SCHEMAS = Path(__file__).resolve().parents[1] / 'schemas'


def validate_schema(schema, files):
    if not shutil.which('xmllint'):
        raise ValueError('Install xmllint (libxml2-utils on Ubuntu) before validating or building')
    for filepath in files:
        result = subprocess.run(
            ['xmllint', '--nonet', '--noout', '--schema', str(schema), str(filepath)],
            capture_output=True, text=True)
        if result.returncode:
            raise ValueError(result.stderr.strip())


class SchemaValidator:
    """Validate each included source once per load, including arbitrary filenames."""

    def __init__(self, schema):
        self.schema = SCHEMAS / schema
        self.validated = set()

    def __call__(self, filepath):
        if filepath not in self.validated:
            validate_schema(self.schema, [filepath])
            self.validated.add(filepath)
