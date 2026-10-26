"""add_scen229b.py (offline, only when no chain runs): V2.29 capture scenario c29_combo (idle -> first step -> W -> W+D -> D -> A -> stop + look)."""
import pathlib
p = pathlib.Path(__file__).resolve().parents[2] / 'Tools/SHME_V212_20261017/v212_run.sh'; s = p.read_text(encoding='utf8')
if 'c29_combo)' in s: print('SCEN229B already')
else:
    L = r'''  c29_combo) REQ=$(mvy '{"start":2.0,"gait":"walk","segments":[[2.5,0],[2.0,45],[2.0,90],[2.0,-90],[3.5,null]],"stop":1.0}' '{"start":10.9,"hold":0.8,"steps":[40,0,-40,0],"ramp":120}');;   # V2.29 calm walk chain: idle, first step, W, W+D, D, A, stop, look left / right
'''
    m = '  *) echo "unknown scenario $SCN"; exit 2;;'
    s = s.replace(m, L + m); p.write_text(s, encoding='utf8'); print('SCEN229B added')
