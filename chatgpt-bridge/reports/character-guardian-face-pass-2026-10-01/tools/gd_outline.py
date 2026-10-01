"""GUARDIAN face pass: face-outline widths (ears excluded) of a candidate head (DNA-order npy, UE cm) projected with the reffront camera
into the reference frame, vs the reference contour picks; all in IPD units relative to the eye line.
usage: blender -b --factory-startup --python gd_outline.py -- <head.npy> <ref_front tracker json> [out png overlay base img]"""
import sys, json, math, numpy as np
a = sys.argv[sys.argv.index('--')+1:]; X = np.load(a[0]); TRK = json.load(open(a[1]))
I = 'Saved/Codex/CharacterIdentity_20260930'; PK = json.load(open(I+'/ref_picks.json'))['front']
cam = [0.95, 129.7, 170.3, -90.4, -3.8]; fov = 15.0; W, H = 800, 960
rc = json.load(open(I+'/recon_c/recon.json'))['cams']['front']; R, s, t = rc['R'], rc['s'], rc['t']
dot = lambda p, q: sum(i*j for i, j in zip(p, q)); depth = dot(R[2], [0, 10, 160])
def world(px, py): u, v = (px-t[0])/s, (py-t[1])/s; return [R[0][k]*u+R[1][k]*v+R[2][k]*depth for k in range(3)]
x0, y0, z0, yaw, pit = cam; cy, sy, cp, sp = math.cos(math.radians(yaw)), math.sin(math.radians(yaw)), math.cos(math.radians(pit)), math.sin(math.radians(pit))
f = np.array((cy*cp, sy*cp, sp)); r = np.array((-sy, cy, 0.0)); up = np.array((-cy*sp, -sy*sp, cp)); tt = math.tan(math.radians(fov)/2)
def proj(P):
    v = np.asarray(P, float)-np.array([x0, y0, z0]); d = v@f; return np.stack([0.5+0.5*(v@r)/d/tt, 0.5-0.5*(v@up)/d/tt], -1)
(fx0, fy0), (fx1, fy1) = proj([world(0, 0)])[0], proj([world(W, H)])[0]
def topix(P): q = proj(P); return np.stack([(q[:, 0]-fx0)/(fx1-fx0)*W, (q[:, 1]-fy0)/(fy1-fy0)*H], -1)
SK = X[:24049]; pe = topix(np.stack([X[28955:29725].mean(0), X[29725:30495].mean(0)]))
ipd_c = np.linalg.norm(pe[0]-pe[1]); eyey_c = pe[:, 1].mean(); midx_c = pe[:, 0].mean()
front = SK[:, 1] > float(sys.argv[sys.argv.index('--')+3]) if len(a) > 2 and a[2].replace('.', '').replace('-', '').isdigit() else SK[:, 1] > -1.5
pp = topix(SK[front])
def cen(c): return np.mean(np.asarray(c), 0)
el = cen(TRK['crv_eyelid_upper_l']+TRK['crv_eyelid_lower_l']); er = cen(TRK['crv_eyelid_upper_r']+TRK['crv_eyelid_lower_r']); ipd_r = np.linalg.norm(el-er); eyey_r = (el[1]+er[1])/2; midx_r = (el[0]+er[0])/2
print('IPD px cand %.1f ref %.1f' % (ipd_c, ipd_r))
C = {c['name']: c['ref'] for c in PK['contours']}
for nm, (kl, kr) in {'cheek_hi': ('cheek_R_hi', 'cheek_L_hi'), 'cheek_mid': ('cheek_R_mid', 'cheek_L_mid'), 'cheek_lo': ('cheek_R_lo', 'cheek_L_lo'), 'jaw': ('jaw_R', 'jaw_L'), 'chin': ('chin_R', 'chin_L')}.items():
    L, Rr = C[kl], C[kr]; h = ((L[1]+Rr[1])/2-eyey_r)/ipd_r; wr = abs(Rr[0]-L[0])/ipd_r
    yc = eyey_c+h*ipd_c; band = np.abs(pp[:, 1]-yc) < 2.5
    wc = (pp[band, 0].max()-pp[band, 0].min())/ipd_c if band.any() else float('nan')
    print('%-10s h=%.2f  width ref %.3f  cand %.3f  ratio %.3f' % (nm, h, wr, wc, wc/wr))
mh = (C['menton'][1]-eyey_r)/ipd_r; ch = (pp[:, 1].max()-eyey_c)/ipd_c; print('menton below eyes: ref %.3f cand %.3f ratio %.3f' % (mh, ch, ch/mh))
np.save(a[0].replace('.npy', '_proj_front.npy'), pp)
# ---- mid-sagittal landmarks (candidate)
mid = np.abs(SK[:, 0]) < 0.35; Mv = SK[mid]; low = Mv[Mv[:, 2] < pe_z if False else Mv[:, 2] < 158]
pog = low[np.argmax(low[:, 1]-0.0*low[:, 2])] if False else None
chinreg = Mv[(Mv[:, 2] < 156) & (Mv[:, 2] > 140)]; pog = chinreg[np.argmax(chinreg[:, 1])]
cand_m = Mv[(Mv[:, 1] > pog[1]-3.0) & (Mv[:, 2] < pog[2])]; men = cand_m[np.argmin(cand_m[:, 2])]
pm = topix(np.stack([pog, men])); print('pogonion', np.round(pog, 2), 'menton', np.round(men, 2))
mh_c = (pm[1, 1]-eyey_c)/ipd_c; print('menton below eyes (IPD): ref %.3f cand %.3f ratio %.3f' % (mh, mh_c, mh_c/mh))
# widths at heights scaled by the eye->menton distance (proportional face)
for nm, (kl, kr) in {'cheek_hi': ('cheek_R_hi', 'cheek_L_hi'), 'cheek_mid': ('cheek_R_mid', 'cheek_L_mid'), 'cheek_lo': ('cheek_R_lo', 'cheek_L_lo'), 'jaw': ('jaw_R', 'jaw_L'), 'chin': ('chin_R', 'chin_L')}.items():
    L, Rr = C[kl], C[kr]; fr = ((L[1]+Rr[1])/2-eyey_r)/(C['menton'][1]-eyey_r); wr = abs(Rr[0]-L[0])/ipd_r
    yc = eyey_c+fr*(pm[1, 1]-eyey_c); band = (np.abs(pp[:, 1]-yc) < 2.5)
    wc = (pp[band, 0].max()-pp[band, 0].min())/ipd_c
    print('PROP %-10s frac %.2f  width ref %.3f cand %.3f ratio %.3f' % (nm, fr, wr, wc, wc/wr))
