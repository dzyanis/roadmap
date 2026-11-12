"""Probe D2's native PNG path, including its link appendix, at two scales."""
import json
import os
from pathlib import Path
import struct
import subprocess
import tempfile
import time

HERE = Path(__file__).resolve().parent
rows = []
with tempfile.TemporaryDirectory(prefix='roadmap-d2-png-') as temporary:
    for key in ('dsa', 'go', 'devops'):
        for engine in ('dagre', 'elk'):
            for scale in (1, 0.2):
                output = Path(temporary) / f'{key}-{engine}-{scale}.png'
                command = [os.environ.get('D2', 'd2'), f'--layout={engine}', '--pad=24',
                           '--salt=roadmap-prototype', f'--scale={scale}',
                           str(HERE / f'demo/{key}.d2'), str(output)]
                start = time.perf_counter()
                try:
                    result = subprocess.run(command, capture_output=True, text=True, timeout=90)
                    row = {'input': key, 'layout': engine, 'scale': scale,
                           'seconds': round(time.perf_counter()-start, 3), 'exit_code': result.returncode,
                           'log': result.stderr.replace(temporary, '<temporary>')}
                    if result.returncode == 0:
                        data = output.read_bytes()
                        row['width'], row['height'] = struct.unpack('>II', data[16:24])
                        row['bytes'] = len(data)
                except subprocess.TimeoutExpired:
                    row = {'input': key, 'layout': engine, 'scale': scale, 'error': '90-second timeout'}
                rows.append(row)
                print(json.dumps(row), flush=True)
(HERE / 'png-results.json').write_text(json.dumps(rows, indent=2) + '\n')
