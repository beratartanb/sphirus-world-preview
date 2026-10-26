"""ltp231.py - V2.31 LTP reader (per-frame telemetry side files, Saved/Codex/SHME_V1_20260925/LTP/<label>.ltp; .ltp.gz too).
load(label) -> list of dict rows (stage, t, numeric fields parsed; vectors -> (x,y,z) tuples). Used by the V2.31 analysis scripts."""
import gzip, os, re, sys
LTP = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'Saved', 'Codex', 'SHME_V1_20260925', 'LTP')
VEC = re.compile(r'^X=(-?[\d.eE+-]+) Y=(-?[\d.eE+-]+) Z=(-?[\d.eE+-]+)$')
def conv(v):
    m = VEC.match(v)
    if m: return tuple(float(x) for x in m.groups())
    try: return float(v)
    except ValueError: return v
def load(label, stage=None):
    p = os.path.join(LTP, label + '.ltp')
    op = open
    if not os.path.exists(p): p += '.gz'; op = gzip.open
    rows = []
    with op(p, 'rt', encoding='utf8', errors='replace') as fh:
        for ln in fh:
            i = ln.find('LTP|')
            if i < 0: continue
            parts = ln[i:].rstrip('\r\n').split('|')
            r = {}
            for kv in parts[2:]:
                k, _, v = kv.partition('=')
                if k not in r: r[k] = conv(v)
            if stage and r.get('stage') != stage: continue
            if rows and r.get('t') == rows[-1].get('t'): continue   # the LTP sometimes logs one frame twice (dt 0 -> fake acceleration spikes)
            rows.append(r)
    return rows
def short(o): return str(o).split('.')[-1].split("'")[0] if o else ''
if __name__ == '__main__':
    rows = load(sys.argv[1]); st = {}
    for r in rows: st.setdefault(r.get('stage'), []).append(r['t'])
    for k, v in st.items(): print(k, len(v), min(v), max(v))
