#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
p = subprocess.run([sys.executable, str(HERE / 'diagnosticoamo.py'), '--demo', '--compact'], capture_output=True, text=True, check=True)
r = json.loads(p.stdout)
assert r['schema'] == 'desarrollamo.diagnostico.v1'
assert sorted(r['inputs']['received']) == ['device', 'network', 'system']
assert r['privacy']['external_requests_performed'] is False
assert r['score']['total'] >= 75
assert r['score']['method']
print('DiagnosticoAMO schema OK')
