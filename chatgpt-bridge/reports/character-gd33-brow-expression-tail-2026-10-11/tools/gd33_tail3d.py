"""GD33 brow tail from the user-marked reference region (no hand-invented hook): the reference brow band measured inside the user's outline in
the solved q3_faceR camera (data/usermask/usermask_q3_faceR.npz: per column top / centre / bottom, 2x panel px) is lifted onto the head skin
through that camera (front-most surface layer under each pixel, like gd16_browproj.py). The near brow in q3_faceR is 'imgL' (subject's right,
-x). Stations 0..ANCHOR of the GD16 reference stations are kept; everything lateral of ANCHOR is replaced by the reference path from the column
of station ANCHOR to the reference tip, sampled every STEP px, blended into the anchor over the first BLEND samples (no kink), thickness taken
from the measured band, clamped to [TMIN, anchor thickness] and non-increasing toward the tip. 'imgR' (+x, far side in q3_faceR) gets the
mirrored tail displacement relative to its own anchor station (projected to its skin). Reports every station in q3_faceR / front px.
usage: blender -b --factory-startup --python gd33_tail3d.py -- <head.npy> <cams.json> <usermask npz> <brow3d in> <brow3d out> [ANCHOR=5] [STEP=8] [BLEND=2] [TMIN=0.12]"""
import sys, os, json, numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
sys.path.insert(0, os.path.join(os.getcwd(), 'Saved/Codex/GD13_Identity_20261009/tools')); from gd13_common import project, depth
sys.path.insert(0, os.path.join(os.getcwd(), 'Tools/CharacterLookdev_20260930')); from gd_common import head_topology
a = sys.argv[sys.argv.index('--')+1:]; HEAD, CAMS, NPZ, IN, OUT = a[:5]
ANCHOR = int(a[5]) if len(a) > 5 else 5; STEP = float(a[6]) if len(a) > 6 else 8.0; BLEND = int(a[7]) if len(a) > 7 else 2; TMIN = float(a[8]) if len(a) > 8 else 0.12
X = np.load(HEAD)[:24049]; T, MI = head_topology(); TT = T[(MI == 0) & (T.max(1) < 24049)]
bvh = BVHTree.FromPolygons([tuple(map(float, p)) for p in X], [tuple(int(i) for i in t) for t in TT])
def surf(p): loc, nrm, idx, d = bvh.find_nearest(Vector(tuple(float(v) for v in p))); return np.asarray(loc)
C = json.load(open(CAMS)); CQ = C['q3_faceR']; CF = C['front']; MX = -0.23
reg = np.nonzero((X[:, 2] > 160.5) & (X[:, 2] < 168.5) & (X[:, 1] > 3.0) & (X[:, 0]-MX < -1.0))[0]   # -x brow / temple skin
P2 = project(CQ, X[reg])*2.0; Z = depth(CQ, X[reg])   # 2x panel px
def pick(col, row):
    d = np.linalg.norm(P2-np.array([col, row]), axis=1); near = np.argsort(d)[:14]; zmin = Z[near].min(); near = near[Z[near] < zmin+0.6]
    w = 1.0/np.maximum(d[near], 0.3)**2; return surf((X[reg[near]]*w[:, None]).sum(0)/w.sum()), float(d[near].min())
U = np.load(NPZ); Pth = U['path']   # [col, top, cen, bot, dark, r0, r1]
B = json.load(open(IN)); st = B['imgL']; anc = st[ANCHOR]
ac = np.array(anc['cen']); acol, arow = project(CQ, ac[None])[0]*2.0; ath = np.linalg.norm(np.array(anc['top'])-np.array(anc['bot']))
tipcol = Pth[:, 0].min(); cols = np.arange(acol-STEP, tipcol-0.1, -STEP)
if cols[-1] > tipcol+2: cols = np.r_[cols, tipcol]
new = []; prev_th = ath; rep = []
for i, c in enumerate(cols):
    k = np.argmin(np.abs(Pth[:, 0]-c)); _, t, m, b = Pth[k, :4]
    cen, e = pick(c, m); top, _ = pick(c, t); bot, _ = pick(c, b)
    w = min(1.0, (i+1)/(BLEND+1))   # blend from the anchor's own height into the reference path
    if w < 1.0:   # old brow centre at this q3R column (old stations lateral of the anchor, interpolated by projected column)
        oc = np.array([s_['cen'] for s_ in st[ANCHOR:]]); ocol = project(CQ, oc)[:, 0]*2.0; o = np.argsort(ocol)
        old_c = np.array([np.interp(c, ocol[o], oc[o, j]) for j in range(3)]); cen = surf(w*cen+(1-w)*old_c)
    th = float(np.clip(np.linalg.norm(top-bot), TMIN, prev_th)); prev_th = th
    nrm_up = top-bot; nrm_up = nrm_up/max(np.linalg.norm(nrm_up), 1e-6)
    new.append({'col': None, 'q3R_px': [round(float(c), 1), round(float(m), 1)], 'top': surf(cen+nrm_up*th/2).round(4).tolist(), 'cen': cen.round(4).tolist(), 'bot': surf(cen-nrm_up*th/2).round(4).tolist(),
                'thick_mm': round(th*10, 2), 'pick_err_px': round(e, 2)})
B2 = dict(B); B2['imgL'] = st[:ANCHOR+1]+new
# imgR: mirrored tail displacement relative to its own anchor
sr = B['imgR']; arR = np.array(sr[ANCHOR]['cen']); newR = []
for n in new:
    for_k = {}
    for key in ('top', 'cen', 'bot'):
        d = np.array(n[key])-ac; d[0] = -d[0]; for_k[key] = surf(arR+d).round(4).tolist()
    for_k.update({'col': None, 'mirrored_from_imgL': True, 'thick_mm': n['thick_mm']}); newR.append(for_k)
B2['imgR'] = sr[:ANCHOR+1]+newR
B2['tail_from_user_mask'] = {'view': 'q3_faceR', 'anchor': ANCHOR, 'step_px': STEP, 'blend': BLEND, 'anchor_q3R_px': [round(float(acol), 1), round(float(arow), 1)], 'ref_tip_col': float(tipcol)}
json.dump(B2, open(OUT, 'w'), indent=1)
old = np.array([s['cen'] for s in st]); oq = project(CQ, old)*2.0; of = project(CF, old)*2.0
nq = project(CQ, np.array([n['cen'] for n in new]))*2.0; nf = project(CF, np.array([n['cen'] for n in new]))*2.0
print('TAIL3D old imgL stations q3R px:', ' '.join('(%.0f,%.0f)' % tuple(p) for p in oq), '| front px:', ' '.join('(%.0f,%.0f)' % tuple(p) for p in of))
print('TAIL3D new imgL tail q3R px:', ' '.join('(%.0f,%.0f)' % tuple(p) for p in nq), '| front px:', ' '.join('(%.0f,%.0f)' % tuple(p) for p in nf), '| thick mm', [n['thick_mm'] for n in new])
print('TAIL3D tip move vs old tip: %.2f mm, drop %.2f mm' % (np.linalg.norm(np.array(new[-1]['cen'])-old[-1])*10, (old[-1][2]-new[-1]['cen'][2])*10))
