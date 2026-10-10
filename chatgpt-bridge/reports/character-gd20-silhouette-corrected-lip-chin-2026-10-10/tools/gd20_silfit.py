"""GD20 silhouette fit: turns the calibrated background-key profile residuals (per row, + = model in front) into control points of the smooth
perioral profile field (gd20_profield.py): for each row the model's silhouette vertex z comes from the gd13_fit iters-0 dump (prof_front entries),
f(z) = -residual * 0.071 cm (move back when in front), averaged over +-2 rows, limited to |f| <= FMAX and to z in [Z0, Z1]; endpoints 0.
usage: -- <bgbands json> <label> <dumpF json> <out ctrl json> <Z0> <Z1> [FMAX cm=0.6] [GAIN=1.0]"""
import sys, json, numpy as np
a = sys.argv[sys.argv.index('--')+1:]; BG = json.load(open(a[0])); LAB = a[1]; D = json.load(open(a[2])); OUT = a[3]; Z0, Z1 = float(a[4]), float(a[5]); FMAX = float(a[6]) if len(a) > 6 else 0.6; GAIN = float(a[7]) if len(a) > 7 else 1.0
res = {int(k): v for k, v in BG['residual_px_calibrated'][LAB].items()}
rows = sorted({round(e[1][1], 1): e[5][2] for e in D['prof_faceL'] if e[0] == 'prof_front'}.items())   # (row, model z)
zr = {int(r): z for r, z in rows}
pts = []
for r in sorted(zr):
    z = zr[r]
    if not (Z0 <= z <= Z1): continue
    v = [res[q] for q in range(r-2, r+3) if q in res]
    if not v: continue
    f = -np.mean(v)*0.071*GAIN; pts.append([z, float(np.clip(f, -FMAX, FMAX))*10])
pts = sorted(pts); zs = [p[0] for p in pts]
# thin to ~0.3 cm spacing, average inside each bin; endpoints 0
out = []; z = Z0
while z < Z1:
    sel = [p[1] for p in pts if z <= p[0] < z+0.3]
    if sel: out.append([round(z+0.15, 2), round(float(np.mean(sel)), 2)])
    z += 0.3
ctrl = [[Z0-0.3, 0.0]] + out + [[Z1+0.3, 0.0]]
json.dump(ctrl, open(OUT, 'w')); print('SILFIT ctrl (z, mm):', ctrl)
