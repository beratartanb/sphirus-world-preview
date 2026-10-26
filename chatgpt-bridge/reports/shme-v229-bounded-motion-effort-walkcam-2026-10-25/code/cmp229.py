"""cmp229.py tag scen varA varB [...]: side-by-side agility events (agil229) of two variants of the same scenario."""
import sys, subprocess, pathlib
PY = sys.executable; T = pathlib.Path(__file__).resolve().parent
tag, scen, vs = sys.argv[1], sys.argv[2], sys.argv[3:]
for v in vs:
    lab = 'v229%s_%s_%s_r1' % (tag, scen, v)
    out = subprocess.run([PY, str(T / 'agil229.py'), lab], capture_output=True, text=True).stdout.strip().splitlines()
    print('--', lab); [print('  ' + l.strip()) for l in out if l.strip().startswith('{')]
