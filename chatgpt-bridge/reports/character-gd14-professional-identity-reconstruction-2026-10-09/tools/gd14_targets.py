"""GD14: landmark target generator. ops json: {"moves": {"name": {"lm": [indices], "d": [dx, dy, dz] cm, "sym": true}}}; x of d is the OUTWARD
lateral component for landmarks off the midline (mirrored for the other side). Landmarks on the midline (|x - MX| < 0.3) get d with x=0.
writes target json {idx: [x, y, z]} from the base landmark positions. usage: -- <base landmarks.json> <ops.json> <out targets.json>"""
import sys, json, numpy as np
a = sys.argv[sys.argv.index('--')+1:]; L = np.array(json.load(open(a[0]))); OPS = json.load(open(a[1])); MX = -0.23
D = np.zeros_like(L); names = {}
for nm, op in OPS['moves'].items():
    for i in op['lm']:
        d = np.array(op['d'], float).copy(); side = np.sign(L[i, 0]-MX) if abs(L[i, 0]-MX) > 0.3 else 0.0; d[0] = d[0]*side
        D[i] += d; names.setdefault(i, []).append(nm)
T = {int(i): (L[i]+D[i]).tolist() for i in range(len(L)) if np.abs(D[i]).max() > 0}
json.dump(T, open(a[2], 'w'), indent=0); print('TARGETS', len(T), 'max mm %.2f' % (np.abs(D).max()*10)); [print('  ', i, names[i], (D[i]*10).round(2)) for i in sorted(T)]
