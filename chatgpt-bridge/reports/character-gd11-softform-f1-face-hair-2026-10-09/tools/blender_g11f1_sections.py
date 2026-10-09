"""pass F1: HORIZONTAL CROSS-SECTION CONVEXITY of the cheek / jaw side (large-scale form, the 'flat plane / hollow / bony' read).
For each z level the outer shell of the skin is sampled by angle around a vertical axis (x = MX, y = AXY): theta = 0 forward, 90 lateral;
r(theta) = outermost skin point in a 2.5 deg bin (both sides, averaged after mirroring). Between theta A..B (default 22..84 deg: mouth side ->
cheek side in front of the ear) the signed distance of the section from its chord (+ = convex / outward) gives:
  sag_max (mm, the fullness of the section), sag_mean, and the most concave point (theta, mm) -> a flat or concave mid section reads hollow.
Also prints the section curvature profile per 10 deg (mm deviation from the chord) for A/B comparison.
usage: blender -b --python blender_g11f1_sections.py -- <head.npy> [label] [z levels comma] [A,B] [AXY=2.0]"""
import sys, os, math, json, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Tools/CharacterLookdev_20260930')); from id_common import SEG
a = sys.argv[sys.argv.index('--')+1:]; X = np.load(a[0])[:24049]; LAB = a[1] if len(a) > 1 else os.path.basename(a[0])
ZS = [float(v) for v in a[2].split(',')] if len(a) > 2 and a[2] else [159.0, 157.5, 156.0, 154.5, 153.0, 151.5, 150.5]
TA, TB = [float(v) for v in a[3].split(',')] if len(a) > 3 and a[3] else (22.0, 84.0); AXY = float(a[4]) if len(a) > 4 else 2.0; MX = -0.23
S = np.r_[np.arange(*SEG['skin'])]; S = S[S < 24049]; H = X[S]
out = {}
for z in ZS:
    m = np.abs(H[:, 2]-z) < 0.15; P = H[m]; dx = np.abs(P[:, 0]-MX); dy = P[:, 1]-AXY; th = np.degrees(np.arctan2(dx, dy)); r = np.hypot(dx, dy)
    bins = np.arange(TA, TB+0.01, 2.5); R = []
    for b in bins:
        s = np.abs(th-b) < 1.25
        R.append(r[s].max() if s.any() else np.nan)
    R = np.array(R); ok = ~np.isnan(R); b = bins[ok]; R = R[ok]
    xy = np.c_[R*np.sin(np.radians(b)), R*np.cos(np.radians(b))]; p0, p1 = xy[0], xy[-1]; t = (p1-p0)/np.linalg.norm(p1-p0); nrm = np.array([t[1], -t[0]])
    if (np.mean(xy, 0)-0.5*(p0+p1))@nrm < 0 and False: nrm = -nrm
    if nrm@(0.5*(p0+p1)) < 0: nrm = -nrm   # outward = away from the axis
    d = (xy-p0)@nrm*10; inner = d[1:-1]
    prof = {int(bb): round(float(dd), 1) for bb, dd in zip(b, d) if abs(bb % 10) < 0.1}
    i = int(np.argmin(inner)) if len(inner) else 0
    out[z] = dict(sag_max=round(float(inner.max()), 2), sag_mean=round(float(inner.mean()), 2), most_concave_deg=float(b[1:-1][i]), most_concave_mm=round(float(inner[i]), 2), chord_cm=round(float(np.linalg.norm(p1-p0)), 2), prof=prof)
    print('SEC %-8s z %.1f  sag max %+5.2f mean %+5.2f mm | min %+5.2f at %4.1f deg | chord %.2f cm | %s' % (LAB, z, out[z]['sag_max'], out[z]['sag_mean'], out[z]['most_concave_mm'], out[z]['most_concave_deg'], out[z]['chord_cm'], ' '.join('%d:%+.1f' % kv for kv in prof.items())))
json.dump(out, open(os.path.splitext(a[0])[0]+'_sections.json', 'w'), indent=1)
