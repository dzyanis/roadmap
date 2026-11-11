from pathlib import Path
import xml.etree.ElementTree as ET


def load_xml(filepath, ancestors, validator=None):
    path = Path(filepath).resolve()
    if path in ancestors:
        cycle = (*ancestors[ancestors.index(path):], path)
        raise ValueError('XML include cycle: ' + ' -> '.join(map(str, cycle)))
    if validator is not None:
        validator(path)
    try:
        root = ET.parse(path).getroot()
    except (OSError, ET.ParseError) as error:
        raise ValueError(f'{filepath}: {error}') from error
    return root, (*ancestors, path)
