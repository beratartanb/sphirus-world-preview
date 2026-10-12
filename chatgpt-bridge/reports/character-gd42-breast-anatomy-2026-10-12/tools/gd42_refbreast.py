"""GD42: reference breast sagittal profile from the private sheet's side-view silhouette (front edge per row), in our cm, aligned at the apex row.
usage: python gd42_refbreast.py <refsil.json> <our_apex_z> <out.json>"""
import sys, json, numpy as np
if "--" in sys.argv: sys.argv = [sys.argv[0]]+sys.argv[sys.argv.index("--")+1:]
d = json.load(open(sys.argv[1]))['side']; our_apex_z = float(sys.argv[2]); rows = d['rows']; top, hp, ax = d['top'], d['height_px'], d['axis_x']
print('row sample', rows[300:303], 'top', top, 'height_px', hp, 'axis', ax)
cmpp = 173.16/hp   # reference figure height -> our standing height (head top 173.16)
prof = []
for i, r in enumerate(rows):
    if r is None or (isinstance(r, (list, tuple)) and len(r) < 2): continue
    x0, x1 = (r[0], r[1]) if isinstance(r, (list, tuple)) else (r.get('x0'), r.get('x1'))
    if x0 is None: continue
    f = i/float(hp); prof.append((f, (ax-x0)*cmpp, (x1-ax)*cmpp))   # front = image-left edge (the figure faces left)
prof = np.asarray(prof); f, yf, yb = prof.T
band = (f > 0.17) & (f < 0.40); k = np.argmax(np.where(band, yf, -99)); f_apex, y_apex = f[k], yf[k]
z = our_apex_z-(f-f_apex)*173.16   # proportional rows, anchored at the apex
below = (z < our_apex_z-1.5) & (z > our_apex_z-14); kf = np.argmin(np.where(below, yf, 99)); imf_z, imf_y = z[kf], yf[kf]
wall = yf[(z < imf_z-2) & (z > imf_z-5)].mean()
def yat(zz): return float(np.interp(-zz, -z, yf))
out = {'f_apex': round(float(f_apex), 4), 'apex_y_rel_axis': round(float(y_apex), 2), 'imf_z': round(float(imf_z), 2), 'imf_y_rel_axis': round(float(imf_y), 2), 'wall_y_rel_axis': round(float(wall), 2),
       'projection_cm': round(float(y_apex-wall), 2), 'apex_to_imf_cm': round(float(our_apex_z-imf_z), 2), 'upper_pole_drop_at+3': round(float(y_apex-yat(our_apex_z+3)), 2), 'upper_pole_drop_at+6': round(float(y_apex-yat(our_apex_z+6)), 2),
       'upper_pole_drop_at+9': round(float(y_apex-yat(our_apex_z+9)), 2), 'lower_pole_drop_at-3': round(float(y_apex-yat(our_apex_z-3)), 2), 'lower_pole_drop_at-5': round(float(y_apex-yat(our_apex_z-5)), 2),
       'profile_z_y': [[round(float(zz), 1), round(float(yy), 2)] for zz, yy in zip(z, yf) if our_apex_z-16 < zz < our_apex_z+14][::3]}
json.dump(out, open(sys.argv[3], 'w'), indent=1); print('REFBREAST', json.dumps({k: v for k, v in out.items() if k != 'profile_z_y'})); print('REFPROFILE', out['profile_z_y'])
