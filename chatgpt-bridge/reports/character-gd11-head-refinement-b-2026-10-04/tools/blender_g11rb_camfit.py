"""GUARDIAN face pass: re-solve a reference camera (UE perspective, orbiting the eye midpoint at the capture distance, fov 15) + a 2D
similarity into the reference frame, from eyes + lips only (identity-neutral anchors; nose / cheeks excluded). Grid over yaw / pitch / roll.
Point correspondences: mesh lid / lip curves bound from the FRONT render (semantic json) vs the reference tracker curves of the view.
usage: blender -b --factory-startup --python blender_gd_camfit.py -- <semantic.json> <head.npy> <view> <out.json>"""
import sys, os, json, math, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Tools/CharacterLookdev_20260930'))
from gd_common import *
a = sys.argv[sys.argv.index('--')+1:]; SEM = json.load(open(a[0])); X = np.load(a[1]); VIEW = a[2]; OUT = a[3]
REF = ref_curves(VIEW); KEYS = [k for k in REF if 'eyelid' in k or 'lip_' in k and 'philtrum' not in k]
W8 = {k: (3.0 if 'eyelid' in k else 1.0) for k in KEYS}
P3, P2, WW = [], [], []
for k in KEYS:
    for e, r in zip(SEM['front'][k], REF[k]):
        if e is None: continue
        P3.append(np.asarray(e[1])@X[e[0]]); P2.append(r); WW.append(W8[k])
if VIEW == 'close' and os.environ.get('GD_EARS', '1') == '1':   # ear picks (strong yaw constraint): right ear tragus / lobe (mesh points located 2026-10-01)
    PKc = {p['name']: p['ref'] for p in json.load(open(I+'/ref_picks.json'))['close']['points']}
    for nm, p3 in (('ear_tragus', [-7.3, 3.4, 160.5]), ('ear_lobe', [-7.35, 2.65, 158.3])): P3.append(np.asarray(p3)); P2.append(PKc[nm]); WW.append(float(os.environ.get('GD_EARW', '40')))
P3 = np.asarray(P3); P2 = np.asarray(P2, float); WW = np.asarray(WW)
piv = 0.5*(X[28955:29725].mean(0)+X[29725:30495].mean(0)); v0 = VIEWS[VIEW]; o0, f0, _, _ = basis(v0['cam']); dist = np.linalg.norm(piv-o0)
def project(yaw, pit, roll):
    cy, sy, cp, sp = math.cos(math.radians(yaw)), math.sin(math.radians(yaw)), math.cos(math.radians(pit)), math.sin(math.radians(pit))
    f = np.array([cy*cp, sy*cp, sp]); r = np.array([-sy, cy, 0.0]); u = np.array([-cy*sp, -sy*sp, cp])
    cr, sr = math.cos(math.radians(roll)), math.sin(math.radians(roll)); r, u = cr*r+sr*u, -sr*r+cr*u
    o = piv-f*dist; d = P3-o; dd = d@f; t = math.tan(math.radians(7.5)); return np.stack([(d@r)/dd/t, -(d@u)/dd/t], -1), o
def simfit(A, B, w):   # B ~ s*A + t (no rotation; roll handled in the camera)
    wm = w/w.sum(); ma = (A*wm[:, None]).sum(0); mb = (B*wm[:, None]).sum(0); A0 = A-ma; B0 = B-mb
    s = (wm*(A0*B0).sum(1)).sum()/(wm*(A0*A0).sum(1)).sum(); return s, mb-s*ma
best = None
for yaw in np.arange(float(os.environ.get('GD_Y0', -75)), float(os.environ.get('GD_Y1', -24.9)), 1.0):
    for pit in np.arange(float(os.environ.get('GD_P0', -6)), float(os.environ.get('GD_P1', 18.1)), 1.0):
        for roll in ([0.0] if os.environ.get('GD_NOROLL') else np.arange(-6, 6.1, 1.0)):
            q, o = project(yaw, pit, roll); s, t = simfit(q, P2, WW); res = np.sqrt((WW*((s*q+t-P2)**2).sum(1)).sum()/WW.sum())
            if best is None or res < best[0]: best = (res, yaw, pit, roll, s, t.tolist(), o.tolist())
res, yaw, pit, roll, s, t, o = best
old = basis(v0['cam']); oy = math.degrees(math.atan2(old[1][1], old[1][0])); op = math.degrees(math.asin(old[1][2]))
q, _ = project(yaw, pit, roll); pe = s*q+np.asarray(t); print('EARRES', np.round(np.linalg.norm(pe[-2:]-P2[-2:], axis=1), 1).tolist(), 'eyes/lips rms', round(float(np.sqrt(((pe[:-2]-P2[:-2])**2).sum(1).mean())), 2))
print('CAMFIT', VIEW, 'rms px %.2f' % res, 'yaw %.1f pitch %.1f roll %.1f' % (yaw, pit, roll), '| old cam yaw %.1f pitch %.1f' % (oy, op), 'scale', round(s, 2), 'origin', np.round(o, 2).tolist())
json.dump({'view': VIEW, 'yaw': yaw, 'pitch': pit, 'roll': roll, 'origin': o, 'dist': float(dist), 'pivot': piv.tolist(), 's': s, 't': t, 'rms_px': res,
           'W': v0['W'], 'H': v0['H'], 'note': 'pixel = s * (tan-normalised camera coords) + t ; camera: forward from yaw/pitch, roll about forward'}, open(OUT, 'w'), indent=1)
