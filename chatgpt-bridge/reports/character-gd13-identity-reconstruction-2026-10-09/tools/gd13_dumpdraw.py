"""draw fit contour selections (dump json: {view: [[name, p_ref, q_model, r], ...]}) on the 2x panels: yellow ref sample, green model point, red link"""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(__file__)); import gd13_img as gi; from gd13_common import ROOT
a = sys.argv[sys.argv.index('--')+1:]; D = json.load(open(a[0])); OUT = a[1]; tiles = []
for v in ['front', 'q3_faceR', 'q3_faceL', 'prof_faceL']:
    I = gi.load(f'{ROOT}/SourceAssets/Characters/GD13_IdentityMaster_20261009/references/GD13_REF_panel_{v}.png'); I = gi.resize(I, I.shape[1]*2, I.shape[0]*2)
    for nm, p, q, r in D.get(v, []):
        p = np.array(p)*2; q = np.array(q)*2
        for t in np.linspace(0, 1, 30):
            x, y = (p*(1-t)+q*t).astype(int)
            if 0 <= y < I.shape[0] and 0 <= x < I.shape[1]: I[y, x, :3] = [1, 0, 0]
        for pt, col in ((p, [1, 1, 0]), (q, [0, 1, 0])):
            x, y = pt.astype(int); I[max(y-1, 0):y+2, max(x-1, 0):x+2, :3] = col
    tiles.append(I[:1082, :964])
gi.save(OUT, np.concatenate(tiles, 1))
for v, t in zip(['front', 'q3_faceR', 'q3_faceL', 'prof_faceL'], tiles): gi.save(OUT.replace('.jpg', '_'+v+'.jpg'), t[150:900, 100:900])
print('DD_OK')
