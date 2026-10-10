"""GD18 contour-band residuals (GD13 _bands.py logic) for heads measured with gd13_fit.py iters 0 + dump on FIXED cameras (cam_iters 0).
Residual sign = gd13_fit convention (d[3], px of the panel-original sheet along the outward image normal; + = model OUTSIDE the reference).
usage: blender -b --python gd18_bands.py -- <meas dir> <out.json> <tag1> [tag2 ...]"""
import json, os, sys, numpy as np
a = sys.argv[sys.argv.index('--')+1:]; D = a[0]; OUT = a[1]; TAGS = a[2:]
BANDS = {'prof_faceL': ('prof_front', [('alin', 140, 170), ('kok_burun_sirti_ust', 184, 216), ('burun_alt_sirt_uc', 220, 280), ('subnazal_ust_dudak', 284, 298), ('dudaklar_stomion', 300, 322), ('cene_yastigi', 324, 356)]),
         'front': ('cheek_two', [('alt_yanak_agiz_seviyesi', 296, 320), ('cene_govdesi', 320, 341)]),
         'q3_faceR': ('far_R', [('uzak_elmacik_yanak', 240, 300), ('uzak_cene', 320, 385)]), 'q3_faceL': ('far_L', [('uzak_elmacik_yanak', 240, 312), ('uzak_cene', 350, 385)])}
out = {}
for h in TAGS:
    Dm = json.load(open(os.path.join(D, h+'_dumpF.json'))); out[h] = {}
    for v, (nm, bands) in BANDS.items():
        rows = [d for d in Dm.get(v, []) if d[0].startswith('cheek_img') and '_two' in d[0]] if nm == 'cheek_two' else [d for d in Dm.get(v, []) if d[0] == nm]
        for lab, y0, y1 in bands:
            r = [d[3] for d in rows if y0 <= d[1][1] <= y1 and abs(d[3]) < 20]
            out[h][v+'.'+lab] = (round(float(np.mean(r)), 2), round(float(np.sqrt(np.mean(np.square(r)))), 2), len(r)) if r else None
    # front cheek per side
    for side in ('cheek_imgL_two', 'cheek_imgR_two'):
        for lab, y0, y1 in (('agiz', 296, 320), ('cene', 320, 341)):
            r = [d[3] for d in Dm.get('front', []) if d[0] == side and y0 <= d[1][1] <= y1 and abs(d[3]) < 20]
            out[h]['front.%s.%s' % (side, lab)] = (round(float(np.mean(r)), 2), round(float(np.sqrt(np.mean(np.square(r)))), 2), len(r)) if r else None
json.dump(out, open(OUT, 'w'), indent=1)
for k in out[TAGS[0]]: print('BAND %-40s' % k, '  '.join('%s %+5.1f rms %4.1f n%d' % (h, *out[h][k]) if out[h].get(k) else h+' -' for h in TAGS))
print('names', sorted(set(d[0] for d in Dm['front'])))
