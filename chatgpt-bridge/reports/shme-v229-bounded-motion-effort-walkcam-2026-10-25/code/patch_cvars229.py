"""patch_cvars229.py (offline, only when no chain runs): add the V2.29 effort contract to the harness telemetry cvars (v212_run.sh)."""
import pathlib
p = pathlib.Path(__file__).resolve().parents[2] / 'Tools/SHME_V212_20261017/v212_run.sh'; s = p.read_text(encoding='utf8')
if '"EffortE"' in s: print('CVARS229 already')
else:
    a = 'CV=\'"cvars":["ClipSpeed","ClipSpeedOn",'
    assert s.count(a) == 1; s = s.replace(a, a + '"EffortE","EffortLoad","EffortLoadDir","EffortAccScale","EffortTurnScale",'); p.write_text(s, encoding='utf8'); print('CVARS229 added')
