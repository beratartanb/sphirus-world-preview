"""GD11 head refinement B: nose DORSUM fill (script-based, not freehand). Package topology, UE cm (face looks +y).
The midline profile between the radix (deepest point below the glabella) and the supratip (tip z + SUPRA) is compared with a straight
radix->supratip line plus a small natural convexity (BUMP mm at 40 % of the span). Only the DEFICIT (concave scoop) is filled:
  fill(z) = ALPHA * max(0, target(z) - profile(z)),  smoothed in z
and applied as +y to dorsum vertices with a lateral Gaussian (SIGMA cm) and a hard guard away from the lids / tip lobule / base.
Tip lobule, nostrils, alar base, columella, radix depth, forehead and orbits are untouched by construction.
usage: blender -b --factory-startup --python gd11rb_dorsum.py -- <in.npy> <out.npy>   env: ALPHA=1.0 BUMP=0.3 SIGMA=0.75 SUPRA=0.9"""
import sys, os, json, numpy as np
a = sys.argv[sys.argv.index('--')+1:]; IN, OUT = a[0], a[1]; E = lambda k, d: float(os.environ.get(k, d))
X = np.load(IN); NH = 24049; S = X[:NH]; MX = -0.23
ez = 0.5*(X[28955:29725, 2].mean()+X[29725:30495, 2].mean())
def sstep(t): t = np.clip(t, 0, 1); return t*t*(3-2*t)
mid = (np.abs(S[:, 0]-MX) < 0.22) & (S[:, 1] > 8.0)
zs = np.arange(157.5, 166.0, 0.1); prof = np.array([S[mid & (np.abs(S[:, 2]-z) < 0.12), 1].max() if (mid & (np.abs(S[:, 2]-z) < 0.12)).any() else np.nan for z in zs])
ok = ~np.isnan(prof); prof = np.interp(zs, zs[ok], prof[ok])
tipz = zs[np.argmax(np.where((zs > 157.8) & (zs < 160.5), prof, -1e9))]
rad = (zs > ez) & (zs < ez+2.0); rz = zs[rad][np.argmin(prof[rad])]; ry = prof[rad].min()
sz = tipz+E('SUPRA', '0.9'); sy = float(np.interp(sz, zs, prof))
span = (zs >= sz) & (zs <= rz); t = (rz-zs)/(rz-sz)                                     # 0 at radix, 1 at supratip
target = ry+(sy-ry)*t+E('BUMP', '0.3')*0.1*np.sin(np.pi*np.clip(t/0.8, 0, 1))**1.5        # straight + slight convexity peaking ~40 %
deficit = np.where(span, np.maximum(0.0, target-prof), 0.0)
k = np.exp(-0.5*(np.arange(-8, 9)/3.0)**2); k /= k.sum(); fill = np.convolve(deficit, k, 'same')*E('ALPHA', '1.0')
fill *= sstep((zs-sz)/0.35)                                                               # fade to 0 into the supratip / lobule
ax = np.abs(S[:, 0]-MX); f_v = np.interp(S[:, 2], zs, fill, left=0, right=0)
w = np.exp(-0.5*(ax/E('SIGMA', '0.75'))**2)*(1-sstep((ax-float(os.environ.get('GUARD0', 1.15)))/float(os.environ.get('GUARDW', 0.55))))*sstep((S[:, 1]-10.8)/0.8)
X2 = X.copy(); X2[:NH, 1] += f_v*w
d = np.abs(X2[:NH, 1]-S[:, 1])*10
rep = {'eye_z': round(float(ez), 2), 'tip_z': round(float(tipz), 2), 'radix': [round(float(rz), 2), round(float(ry), 2)], 'supratip': [round(float(sz), 2), round(float(sy), 2)],
       'max_deficit_mm': round(float(deficit.max())*10, 2), 'max_fill_mm': round(float(d.max()), 2), 'moved_gt_0.1mm': int((d > 0.1).sum()),
       'tip_lobule_moved_max_mm': round(float(d[S[:, 2] < sz-0.1].max()), 3), 'lids_moved_max_mm': round(float(d[(ax > 1.3) & (S[:, 2] > ez-1)].max()), 3)}
np.save(OUT, X2); print('DORSUM_OK', json.dumps(rep))
