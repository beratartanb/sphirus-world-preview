"""GD38 face symmetry (user: the face looks good turned to the image left = q3_faceL, i.e. the subject's LEFT side, +x; turned to the right =
q3_faceR, the subject's RIGHT side, -x, it looks odd and further from the reference -> make the right side like the left).
1. Asymmetry analysis: the mirrored copy of the head (x -> 2 MX - x, vertex pairs from the symmetric DNA topology, gd13 mirror_map) is rigidly
   aligned to the head (Kabsch over the face skin), so a global yaw / offset is not counted as asymmetry. Per vertex d = X - aligned mirror;
   per region (gd13_checks regions): mean / p95 |d| on the -x side and the mean signed d along (lateral-out, forward, up).
2. Target: the -x side replaced by the aligned mirror of the +x side (the good side), with weight W(ax) ramping from 0 on the midline to
   AMT at ax >= RAMP cm (keeps the midline continuous); optional region exclusions; ears / cranium / neck keep their shape with the same ramp
   on a 3-D falloff. +x side untouched (exactly).
usage: python gd38_sym.py <head.npy> <out_target.npy> <out_report.json> [AMT=1.0] [RAMP=0.6] [EXCL=comma regions]"""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Saved/Codex/GD13_Identity_20261009/tools')); from gd13_common import NS, MX, mirror_map
a = sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else sys.argv[1:]; HEAD, OUT, REP = a[:3]; AMT = float(a[3]) if len(a) > 3 else 1.0; RAMP = float(a[4]) if len(a) > 4 else 0.6; EXCL = [e for e in (a[5] if len(a) > 5 else '').split(',') if e]
X = np.load(HEAD).astype(float); S = X[:NS]; MM = mirror_map()[:NS]
ax = np.abs(S[:, 0]-MX); y, z = S[:, 1], S[:, 2]; ear = (ax > 6.2) & (y < 4.6) & (z > 154) & (z < 168); f = ~ear & (y > 3)
REG = {'forehead': f & (z > 165.0), 'temple': ~ear & (ax > 4.8) & (z > 162) & (z < 167) & (y > 0) & (y < 9),
       'brow_supraorbital': f & (z > 163.3) & (z <= 165.0) & (ax > 0.9) & (ax < 5.2), 'glabella_radix': f & (z > 161.5) & (z <= 165.0) & (ax <= 0.9),
       'upper_lid': f & (z > 162.2) & (z <= 163.6) & (ax > 1.0) & (ax < 4.6) & (y > 9.5), 'lower_lid_infraorbital': f & (z > 160.6) & (z <= 162.2) & (ax > 1.2) & (ax < 4.8),
       'malar_zygoma': f & (z > 159.0) & (z <= 161.2) & (ax > 3.4) & (ax < 6.4), 'mid_cheek': f & (z > 156.5) & (z <= 159.0) & (ax > 2.6) & (ax < 6.2),
       'lower_cheek_jowl': f & (z > 152.5) & (z <= 156.5) & (ax > 3.4) & (ax < 6.4), 'nose_dorsum': f & (z > 159.6) & (z <= 162.2) & (ax < 1.2) & (y > 11),
       'nose_tip_alae': f & (z > 157.3) & (z <= 159.6) & (ax < 2.4) & (y > 12.3), 'upper_lip': f & (z > 155.9) & (z <= 157.3) & (ax < 2.8) & (y > 11),
       'lower_lip': f & (z > 154.6) & (z <= 155.9) & (ax < 2.8) & (y > 11), 'chin': f & (z > 151.3) & (z <= 154.6) & (ax < 2.6) & (y > 9),
       'jaw_body_angle': ~ear & (z > 150.5) & (z <= 156.5) & (ax >= 2.6) & (ax < 6.4) & (y > -1) & (y < 9), 'submental': ~ear & (z > 148.5) & (z <= 151.6) & (ax < 3.5) & (y > 4) & (y < 12),
       'cranium': (z > 168) | ((y < -1.5) & (z > 150)), 'neck': z < 148.5, 'ears': ear}
face = f & (z > 148.5) & (z < 168)
Mr = S[MM].copy(); Mr[:, 0] = 2*MX-Mr[:, 0]
MAF = os.environ.get('MAFILE', '')   # preferred: continuous UV mirror (gd38_uvmirror.py, already aligned) instead of the nearest-vertex pairs
P, Q = Mr[face], S[face]; pc, qc = P.mean(0), Q.mean(0); U_, s_, Vt = np.linalg.svd((P-pc).T@(Q-qc)); dd = np.sign(np.linalg.det(Vt.T@U_.T))
Rm = Vt.T@np.diag([1, 1, dd])@U_.T; Ma = (Mr-pc)@Rm.T+qc   # aligned mirror
if MAF: Ma = np.load(MAF)[:NS].astype(float)
SM = int(os.environ.get('DSMOOTH', '0'))   # optional smoothing of the mirror displacement field (graph Laplacian iterations)
if SM:
    T_ = np.asarray(__import__('gd13_common').pkg()['head']['triangles']); T_ = T_[(T_ < NS).all(1)]; E_ = np.unique(np.sort(np.r_[T_[:, [0, 1]], T_[:, [1, 2]], T_[:, [2, 0]]], 1), axis=0)
    J0 = np.r_[E_[:, 0], E_[:, 1]]; J1 = np.r_[E_[:, 1], E_[:, 0]]; DG = np.bincount(J0, minlength=NS).astype(float); Dd = Ma-S
    for _ in range(SM): acc = np.zeros_like(Dd); np.add.at(acc, J0, Dd[J1]); Dd = 0.5*Dd+0.5*acc/np.maximum(DG, 1)[:, None]
    Ma = S+Dd
yaw = np.degrees(np.arctan2(Rm[1, 0], Rm[0, 0])); D = S-Ma
neg = S[:, 0] < MX; rep = {'alignment': {'yaw_deg': round(float(yaw), 3), 'shift_cm': [round(float(v), 4) for v in (qc-pc)]}, 'regions': {}}
for k, m in REG.items():
    mm = m & neg
    if mm.sum() < 5: continue
    d = D[mm]; n = np.linalg.norm(d, axis=1)*10
    out_lat = -d[:, 0]   # -x side: lateral-out = -x direction
    rep['regions'][k] = {'n': int(mm.sum()), 'mean_mm': round(float(n.mean()), 2), 'p95_mm': round(float(np.percentile(n, 95)), 2),
                         'out_mm': round(float(out_lat.mean()*10), 2), 'fwd_mm': round(float(d[:, 1].mean()*10), 2), 'up_mm': round(float(d[:, 2].mean()*10), 2)}
# target
w = np.clip(ax/RAMP, 0, 1); w = w*w*(3-2*w)*AMT; w[~neg] = 0.0
for e in EXCL:
    if e in REG:   # soft exclusion: 0 inside the region, smooth 0.8 cm falloff around it
        C = S[REG[e] & neg]
        if len(C):
            dist = np.min(np.linalg.norm(S[:, None, :]-C[None, ::max(1, len(C)//400)], axis=2), axis=1); fall = dict(kv.split(':') for kv in os.environ.get('EXFALLS', '').split(',') if kv).get(e, os.environ.get('EXFALL', '0.8')); g = np.clip(dist/float(fall), 0, 1); w *= g*g*(3-2*g)
keep = REG['cranium'] | REG['neck'] | REG['ears']
if keep.any():
    Ck = S[keep]; dist = np.full(NS, 9.0)   # distance to ALL keep vertices (chunked), so the falloff is exactly 0 at the keep border
    for c0 in range(0, NS, 1500): dist[c0:c0+1500] = np.min(np.linalg.norm(S[c0:c0+1500, None, :]-Ck[None, ::2], axis=2), axis=1)
    g = np.clip(dist/float(os.environ.get('KEEPFALL', '1.0')), 0, 1); w *= g*g*(3-2*g)
w[keep] = 0.0   # 2026-10-11 fix: the keep regions (cranium / back of head, neck, ears) never move (the falloff to a subsampled set left them partly weighted)
Y = X.copy(); Y[:NS] = S+(Ma-S)*w[:, None]; np.save(OUT, Y)
mv = np.linalg.norm(Y[:NS]-S, axis=1)*10
rep['keep_moved_max_mm'] = round(float(np.linalg.norm((Y[:NS]-S)[keep], axis=1).max()*10), 4)
rep['target'] = {'AMT': AMT, 'RAMP_cm': RAMP, 'EXCL': EXCL, 'moved_gt_0p5mm': int((mv > 0.5).sum()), 'max_mm': round(float(mv.max()), 2), 'mean_moved_mm': round(float(mv[mv > 0.05].mean()), 2) if (mv > 0.05).any() else 0.0,
                 'plus_side_max_mm': round(float(mv[~neg].max()), 4)}
json.dump(rep, open(REP, 'w'), indent=1)
print('SYM yaw %.3f deg | ' % yaw + ' | '.join('%s %.1f(p95 %.1f) out%+.1f fwd%+.1f up%+.1f' % (k, v['mean_mm'], v['p95_mm'], v['out_mm'], v['fwd_mm'], v['up_mm']) for k, v in rep['regions'].items() if k not in ('cranium', 'neck', 'ears')))
print('SYM target', json.dumps(rep['target']))
