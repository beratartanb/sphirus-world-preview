"""fps241.py <out.md> : V2.41 frame-rate table from the L chain LTPs (tags f120 f60 f20 freal; production o vs candidate tkhaB / wall wst / wsto /
push tkpB). Worst planted-foot SLIP/DRAG drift (contact231, drift > 4 cm) with its owner clip; duplicate candidate runs (_r1 overwritten) are the
last run only. Prints and writes a markdown table."""
import sys, os, glob
H = os.path.dirname(os.path.abspath(__file__)); sys.path[:0] = [H + '/../SHME_V231_20261026', H + '/../SHME_V238_20261030']
from ltp231 import load
from contact231 import classify
ROOT = os.path.join(H, '..', '..'); LTP = os.path.join(ROOT, 'Saved/Codex/SHME_V1_20260925/LTP')
TAGS = ['f120', 'f60', 'f20', 'freal']
def worst(lab):
    if not os.path.exists(os.path.join(LTP, lab + '.ltp')) and not os.path.exists(os.path.join(LTP, lab + '.ltp.gz')): return None
    R = load(lab); eps = [e for e in classify(R, 2.5, 1e9) if e['cls'] in ('SLIP', 'DRAG') and e['drift'] > 4]
    if not eps: return (0.0, '-', 0.0)
    e = max(eps, key=lambda e: e['drift']); return (e['drift'], e['clip'], e['t'])
sc = sorted({os.path.basename(f).split('.')[0].split('_', 1)[1].rsplit('_', 2)[0] for t in TAGS for f in glob.glob(os.path.join(LTP, 'v241%s_*.ltp*' % t))})
lines = ['| scenario | var | ' + ' | '.join(TAGS) + ' |', '|---|---|' + '---|' * len(TAGS)]
for s in sc:
    for v in ['o', 'tkhaB', 'tkpB', 'wst', 'wsto']:
        cells = []; any_ = False
        for t in TAGS:
            w = worst('v241%s_%s_%s_r1' % (t, s, v))
            if w is None: cells.append('-'); continue
            any_ = True; cells.append('%.1f (%s @%.2f)' % (w[0], str(w[1]).replace('A_', '')[:26], w[2]) if w[0] else '0')
        if any_: lines.append('| %s | %s | %s |' % (s, v, ' | '.join(cells)))
txt = '\n'.join(lines); print(txt); open(sys.argv[1], 'w', encoding='utf8').write(txt + '\n')
