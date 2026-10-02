"""GUARDIAN-8 hair architecture metrics (strands.npz vs head npy, UE cm; robust percentiles so single flyaways don't dominate):
  side_front_y[z]  : how far FORWARD the side hair reaches (98th pct of y of hair points lateral to |x|>5.0) at heights z
  side_low_z[y]    : lower boundary (3rd pct of z) of the MAIN side mass at |x|>5.0, depth band y (front of / above the ear)
  ear_cover        : hair points (main+loose) inside the ear box (|x|>6.6, -1.2<y<2.4, 157<z<163) per side
  bun              : centroid / z-range / y of the bun section (last 35% of main strand points), skull rear y at that z
usage: blender -b -P blender_gd8_hairmetrics.py -- <head.npy> <strands.npz> [...]"""
import sys, os, json, numpy as np
a = sys.argv[sys.argv.index('--')+1:]; X = np.load(a[0]); S = X[:24049]
for npz in a[1:]:
    D = np.load(npz); M = D['main']; L = D['loose']; Hm = M.reshape(-1, 3); Hall = np.concatenate([Hm, L.reshape(-1, 3)]); r = {}
    lat = Hall[np.abs(Hall[:, 0]) > 5.0]
    r['side_front_y'] = {z: round(float(np.percentile(lat[np.abs(lat[:, 2]-z) < 0.5, 1], 98)), 2) for z in (158.5, 160, 161.5, 163, 164.5, 166) if (np.abs(lat[:, 2]-z) < 0.5).sum() > 20}
    latm = Hm[np.abs(Hm[:, 0]) > 5.0]
    r['side_low_z'] = {y: round(float(np.percentile(latm[np.abs(latm[:, 1]-y) < 0.5, 2], 3)), 2) for y in (3.0, 1.5, 0.0, -1.5) if (np.abs(latm[:, 1]-y) < 0.5).sum() > 20}
    for sg, k in ((1, 'L'), (-1, 'R')):
        b = (sg*Hall[:, 0] > 6.6) & (Hall[:, 1] > -1.2) & (Hall[:, 1] < 2.4) & (Hall[:, 2] > 157) & (Hall[:, 2] < 163); r['ear_cover_'+k] = int(b.sum())
    n = M.shape[1]; Bp = M[:, int(n*0.65):, :].reshape(-1, 3); c = Bp.mean(0)
    sk = S[(np.abs(S[:, 0]+0.25) < 1.5) & (np.abs(S[:, 2]-c[2]) < 0.4) & (S[:, 1] < 0)]
    r['bun'] = {'centroid': np.round(c, 2).tolist(), 'z_p10_p90': [round(float(np.percentile(Bp[:, 2], 10)), 2), round(float(np.percentile(Bp[:, 2], 90)), 2)],
                'y_back_p95': round(float(np.percentile(Bp[:, 1], 5)), 2), 'skull_rear_y_at_centroid_z': round(float(sk[:, 1].min()), 2) if len(sk) else None}
    print('HM8', os.path.basename(os.path.dirname(npz)), json.dumps(r))
