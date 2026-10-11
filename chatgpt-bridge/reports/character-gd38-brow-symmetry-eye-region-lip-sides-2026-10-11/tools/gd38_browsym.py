"""GD38 symmetric brow stations (user: the left brow looks odd / too asymmetric vs the right; the gap between the brows should follow the reference).
The GD31..GD37 custom brow was built from stations traced separately on each side of the (slightly yawed) reference photo, so the subject's right
brow (imgL, -x, image left) differs from the left one: thinner head (4.8 vs 6.4 mm), head 2.3 mm more medial and 2.1 mm higher, longer tail.
1. imgL := the aligned mirror of imgR (the subject's LEFT brow, +x, GD36 good side): x -> 2 MX - x, then the rigid transform that best maps the
   mirrored skin onto the skin (Kabsch over the face with the gd13 mirror_map pairs) -> the same brow on the right side of this head.
2. Both heads extended medially: every station point shifted toward the midline by GS x (1 - smoothstep(u / 0.35)) cm (u = 0 medial head).
   Reason: the stations sit on the reference brow heads (projected 62 px apart in the 2x front frame, as traced), but the groom's sparse short head
   hairs make the VISIBLE dark head start 2-3 mm lateral of the station -> visible gap 74-81 px vs reference 65-72 px.
usage: blender -b --factory-startup --python gd38_browsym.py -- <head.npy> <brow3d_in.json> <brow3d_out.json> [GS=0.25 cm] [MIRROR=1]"""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Saved/Codex/GD13_Identity_20261009/tools')); from gd13_common import NS, MX, mirror_map
a = sys.argv[sys.argv.index('--')+1:]; S = np.load(a[0])[:NS].astype(float); B = json.load(open(a[1])); OUT = a[2]
GS = float(a[3]) if len(a) > 3 else 0.25; MIR = int(a[4]) if len(a) > 4 else 1
def ss(t): t = min(max(t, 0.0), 1.0); return t*t*(3-2*t)
MM = mirror_map()[:NS]; Mr = S[MM].copy(); Mr[:, 0] = 2*MX-Mr[:, 0]; x, y, z = S[:, 0]-MX, S[:, 1], S[:, 2]
face = (y > 3) & (z > 148.5) & (z < 168) & ~((np.abs(x) > 6.2) & (y < 4.6))
P, Q = Mr[face], S[face]; pc, qc = P.mean(0), Q.mean(0); U_, s_, Vt = np.linalg.svd((P-pc).T@(Q-qc)); dd = np.sign(np.linalg.det(Vt.T@U_.T)); R = Vt.T@np.diag([1, 1, dd])@U_.T
def amir(p): q = np.asarray(p, float).copy(); q[0] = 2*MX-q[0]; return ((q-pc)@R.T+qc).tolist()
O = json.loads(json.dumps(B)); rep = {'GS_cm': GS, 'mirror': MIR, 'yaw_deg': float(np.degrees(np.arctan2(R[1, 0], R[0, 0])))}
if MIR:
    O['imgL'] = []
    for s in B['imgR']:
        t = dict(s); t['top'], t['cen'], t['bot'] = amir(s['top']), amir(s['cen']), amir(s['bot']); t['col'] = None; O['imgL'].append(t)
for side in ('imgL', 'imgR'):
    for s in O[side]:
        f = GS*(1-ss(s['u']/0.35))
        for k in ('top', 'cen', 'bot'):
            p = list(s[k]); p[0] = p[0]-np.sign(p[0]-MX)*f; s[k] = p
O['gd38'] = {'note': 'imgL = aligned mirror of imgR (+x brow); heads extended medially by GS*(1-ss(u/0.35))', **rep}
json.dump(O, open(OUT, 'w'), indent=1)
for side in ('imgL', 'imgR'):
    h = O[side][0]['cen']; t = O[side][-1]['cen']; h0 = B[side][0]['cen']
    print('BROWSYM %s head cen x %+.3f (|x-MX| %.3f, was %.3f) z %.2f (was %.2f) | tail |x-MX| %.3f z %.2f' % (side, h[0], abs(h[0]-MX), abs(h0[0]-MX), h[2], h0[2], abs(t[0]-MX), t[2]))
print('BROWSYM station head gap %.2f mm (was %.2f mm) | mirror yaw %.2f deg' % ((abs(O['imgL'][0]['cen'][0]-MX)+abs(O['imgR'][0]['cen'][0]-MX))*10, (abs(B['imgL'][0]['cen'][0]-MX)+abs(B['imgR'][0]['cen'][0]-MX))*10, rep['yaw_deg']))
