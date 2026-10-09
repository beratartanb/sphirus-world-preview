"""GD13 diagnostic: reference panels (2x) with the reference evidence (cyan: tracker curves, yellow: manual / auto contours + brow lines)
and the candidate's projected evidence (magenta: bound tracker curves + brow points + subnasale, green: model silhouette points chosen
for each contour sample). usage: -- <head.npy> <cams.json> <out.jpg> [views...]"""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(__file__)); from gd13_common import *; import gd13_img as gi
a = sys.argv[sys.argv.index('--')+1:]; X = np.load(a[0]); C = json.load(open(a[1])); OUT = a[2]; VV = a[3:] or VIEWS
os.environ['GD13_DIAG'] = '1'
MM = mirror_map(X); TR = ref_tracks(); PK = json.load(open(os.path.join(GD, 'data/picks_manual.json'))); AU = json.load(open(os.path.join(GD, 'data/contours_auto.json')))
S0 = np.load(os.path.join(GD, 'data/head_F1H.npy'))[:NS]; AX = np.abs(S0[:, 0]-MX)
BROW = {}
for side, sg in (('R', -1), ('L', 1)):
    idx = []
    for ax in np.arange(1.4, 5.01, 0.2):
        zc = 164.05+0.35*np.exp(-((ax-3.3)/1.5)**2)-0.35*np.clip((ax-4.5)/1.0, 0, 1)**1.5
        m = (np.abs(S0[:, 0]-(MX+sg*ax)) < 0.18) & (np.abs(S0[:, 2]-zc) < 0.25) & (S0[:, 1] > 6.0)
        if m.any(): i = np.nonzero(m)[0]; idx.append(int(i[np.argmax(S0[i, 1])]))
    BROW[side] = np.array(idx)
TRI = np.asarray(pkg()['head']['triangles']); TRI = TRI[(TRI < NS).all(1)]
def vnormals(P):
    n = np.cross(P[TRI[:, 1]]-P[TRI[:, 0]], P[TRI[:, 2]]-P[TRI[:, 0]]); N = np.zeros((NS, 3)); [np.add.at(N, TRI[:, k], n) for k in range(3)]; return -N/np.maximum(np.linalg.norm(N, axis=1), 1e-12)[:, None]
JAW = jaw_line(X)
def line(I, P, col, s=2):
    P = np.asarray(P, float)*s
    for i in range(len(P)-1):
        for t in np.linspace(0, 1, 16):
            x, y = (P[i]*(1-t)+P[i+1]*t).astype(int)
            if 0 <= y < I.shape[0] and 0 <= x < I.shape[1]: I[y, x, :3] = col
def dot(I, p, col, r=2, s=2):
    x, y = int(p[0]*s), int(p[1]*s); I[max(y-r, 0):y+r+1, max(x-r, 0):x+r+1, :3] = col
tiles = []
for v in VV:
    I = gi.load(f'{ROOT}/SourceAssets/Characters/GD13_IdentityMaster_20261009/references/GD13_REF_panel_{v}.png'); I = gi.resize(I, I.shape[1]*2, I.shape[0]*2); c = C[v]
    B = bindings(v, MM)
    for ck, rp in TR[v].items():
        line(I, rp, [0, 1, 1])
        if ck in B:
            P = bind_pts(B[ck], X); P = P[~np.isnan(P[:, 0])]
            if len(P): line(I, project(c, P), [1, 0.1, 0.9])
    for cc in PK.get(v, {}).get('contours', []): line(I, cc['pts'], [1, 1, 0]) if len(cc['pts']) > 1 else dot(I, cc['pts'][0], [1, 1, 0], 3)
    for nm, P in AU.get(v, {}).items():
        for p in P[::2]: dot(I, p, [1, 0.85, 0], 1)
    for cv in PK.get(v, {}).get('curves', []):
        line(I, cv['pts'], [1, 1, 0]);
        if 'brow' in cv:
            for p in project(c, X[BROW[cv['brow']]]): dot(I, p, [1, 0.1, 0.9], 2)
    for p in project(c, X[JAW]): dot(I, p, [0.2, 1, 0.2], 2)
    tiles.append(I[:1082, :964])
gi.save(OUT, np.concatenate(tiles, 1)); print('DIAG_OK', OUT)
