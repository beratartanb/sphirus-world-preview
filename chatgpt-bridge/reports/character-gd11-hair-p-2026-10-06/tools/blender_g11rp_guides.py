"""GD11 hair pass P: AUTHORED main-lock centrelines ('curtain' topology read from the reference): hair leaves the centre part sideways,
drapes over the forehead corner / temple, runs back above the ear and gathers behind the ear into the low bun. Each primary lock gets a
route = scalp waypoints (azimuth deg from the front around the vertical axis at x=MX, y=2.5; height z; stand-off cm) chosen per FAMILY from
its ROOT position (stable identity: the root is stored and re-checked by the builder), with per-lock variation; families pass at different
heights / depths so they overlap and cross instead of sharing one sweep. Back / nape locks only get entry / bow variation.
usage: blender -b --factory-startup --python blender_g11rp_guides.py -- <base guides.json (built)> <out guides.json> <head.npy>
env GP_SCALE=1.0 (blend factor toward the authored route)  GP_SO=1.0 (stand-off scale)  GP_ROUTES=<json file overriding / adding per-lock routes>"""
import bpy, sys, os, json, math, numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
sys.path.insert(0, os.path.join(os.getcwd(), 'Tools/CharacterLookdev_20260930'))
from gd_common import head_topology
a = sys.argv[sys.argv.index('--')+1:]; IN, OUT, HEAD = a[0], a[1], a[2]; E = lambda k, d: float(os.environ.get(k, d)); MX = -0.23; CY = 2.5; PART_X = -0.25
G = json.load(open(IN)); X = np.load(HEAD)[:24049]; T, MI = head_topology(); TT = T[(MI == 0) & (T.max(1) < 24049)]
bvh = BVHTree.FromPolygons([tuple(map(float, p)) for p in X], [tuple(int(i) for i in t) for t in TT]); fn = np.cross(X[TT[:, 1]]-X[TT[:, 0]], X[TT[:, 2]]-X[TT[:, 0]]); fn = -fn/np.maximum(np.linalg.norm(fn, axis=1), 1e-9)[:, None]
OVR = json.load(open(os.environ['GP_ROUTES'])) if os.environ.get('GP_ROUTES') else {}
def nearest(p): loc, nrm, idx, d = bvh.find_nearest(Vector(p)); return np.asarray(loc), np.asarray(fn[idx])
def pinna(p): return abs(p[0]-MX) > 7.55 and p[2] < 163.7 and -6.0 < p[1] < 4.0
def S(az, z, sd):
    """scalp point at azimuth az (deg), height z, on side sd (skull, not the ear pinna)"""
    r = math.radians(az); d = np.array([sd*math.sin(r), math.cos(r), 0.0]); o = np.array([MX, CY, z])+d*30.0; h = None
    for _ in range(4):
        hit = bvh.ray_cast(Vector(o), Vector(-d))
        if hit[0] is None: return nearest(np.array([MX, CY, z])+d*8.0)[0]
        h = np.asarray(hit[0])
        if not pinna(h): return h
        o = h-d*0.4
    return h
def azof(p): return math.degrees(math.atan2(abs(p[0]-MX), p[1]-CY))
def sstep(t): t = min(max(t, 0.0), 1.0); return t*t*(3-2*t)
def catmull(P, n):
    P = [np.asarray(p, float) for p in P]; P = [P[0]*2-P[1]]+P+[P[-1]*2-P[-2]]; out = []; segs = len(P)-3
    for i in range(n):
        u = i/(n-1)*segs; k = min(int(u), segs-1); t = u-k; p0, p1, p2, p3 = P[k], P[k+1], P[k+2], P[k+3]
        out.append(0.5*((2*p1)+(-p0+p2)*t+(2*p0-5*p1+4*p2-p3)*t*t+(-p0+3*p1-3*p2+p3)*t**3))
    return np.asarray(out)
def resample(pts, n):
    arc = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(pts, axis=0), axis=1))]); s = np.linspace(0, arc[-1], n); return np.stack([np.interp(s, arc, pts[:, k]) for k in range(3)], 1)
def hsh(i, k): return ((math.sin(i*12.9898+k*78.233)*43758.5453) % 1.0)*2-1     # deterministic per-lock variation in [-1, 1]
def route(pid, r, grp):
    """-> (family, [(az, z, standoff)]) for the root r; None = keep"""
    a_ = azof(r); x, y, z = r; j1, j2, j3 = hsh(pid, 1), hsh(pid, 2), hsh(pid, 3)
    if str(pid) in OVR: o = OVR[str(pid)]; return (o['family'], [tuple(w) for w in o['wp']] if o.get('wp') else None) if o else None
    if grp in ('front_to_bun', 'top_to_bun', 'side_to_bun'):
        if y > 7.4 and z > 168.8:                       # A front edge: along the hairline over the forehead corner, low over the temple, level above the ear
            return 'A_front_edge', [(min(max(a_+20+4*j1, 36), 56), 167.3+0.6*j2-0.035*max(a_-20, 0), 0.40), (66+5*j1, 164.5+0.9*j2, 0.85), (93+3*j3, 164.5+0.95*j2, 1.05), (123+5*j1, 164.7+0.9*j3, 1.2)]
        if y > 3.4 and z > 170.2:                       # B front top (near the part): diagonal over the side, steeper behind the ear, outer layer (crosses A behind the ear)
            return 'B_front_top', [(a_+(92-a_)*0.5+5*j1, 169.4+0.5*j2, 0.7), (99+5*j1, 167.0+1.0*j2, 1.3), (127+5*j3, 163.3+0.8*j2, 1.6)]
        if grp == 'top_to_bun' and y > 1.5:             # F1 top mid: down the side toward the back of the ear
            return 'F_top_mid', [(116+5*j1, 169.6+0.5*j2, 0.75), (140+5*j3, 165.6+0.6*j2, 1.4)]
        # (P4: crown-side locks keep their original straight-back route so the crown stays covered)
        if grp == 'top_to_bun': return None
        if a_ < 84 and z < 169.2:                       # C temple edge: hugs the temple under the curtains (inner layer), slight down-back then level
            return 'C_temple_edge', [(a_+13+3*j1, z-0.8-0.3*j2, 0.32), (101+4*j1, max(164.0, z-1.3)+0.35*j2, 0.55), (126+4*j3, 163.4+0.5*j2, 0.85)]
        if a_ < 84:                                     # (front side, higher): like B but shorter
            return 'B_front_top', [(a_+(95-a_)*0.5+4*j1, z-1.3+0.4*j2, 0.65), (102+5*j1, 166.4+0.9*j2, 1.2), (128+5*j3, 163.5+0.8*j2, 1.5)]
        if z < 165.6 and a_ < 110:                      # D above / in front of the ear: rise over the ear top, then into the mass behind the ear
            return 'D_above_ear', [(101+3*j1, max(z, 163.9)+0.3*j2, 0.45), (125+4*j3, 162.6+0.6*j2, 1.0)]
        if a_ < 112:                                    # E upper side: diagonal down-back, feeds the volume behind the ear
            return 'E_upper_side', [(a_+17+3*j1, z-1.9+0.4*j2, 0.8), (134+4*j3, 164.2+0.6*j2, 1.3)]
        if z > 165.8: return 'E_upper_side', [(a_+14+3*j1, z-1.6+0.4*j2, 0.85), (146+4*j3, 164.6+0.5*j2, 1.25)]
        return 'G_behind_ear', None                     # G rooted behind the ear: keep the route, add real stand-off volume
    if grp == 'back_to_bun' and a_ < 146 and z < 168.5: return 'G_behind_ear', None
    if grp in ('back_to_bun', 'nape_to_bun'): return 'H_back', None
    return None
SC, SO = E('GP_SCALE', '1.0'), E('GP_SO', '1.0'); RISE, WAVE = E('GP_RISE', '0.3'), E('GP_WAVE', '0.3'); log = {}
for k, v in list(G.items()):
    if not (k.startswith('prim:') and isinstance(v, dict) and 'ctrl' in v): continue
    pid = int(k[5:]); c = np.asarray(v['ctrl'], float); r = np.asarray(v['root'], float); sd = 1.0 if r[0] > PART_X else -1.0; fam = route(pid, r, v['group'])
    if fam is None: continue
    name, wp = fam; n = len(c); end = c[-1]
    if wp is not None:
        W = [S(az, z, sd) for az, z, h in wp]; H = [0.07]+[h*SO*(1+0.18*hsh(pid, 7)) for az, z, h in wp]
        pre = (W[-1]+end)*0.5; lp, np_ = nearest(pre); pre = lp+np_*max(1.1, float(np.dot(pre-lp, np_)))      # mid point of the last leg kept off the scalp / bun
        ctrlp = [c[0]]+W+[pre, end]; dense = catmull(ctrlp, 90); arcw = [0.0]
        for i in range(1, len(ctrlp)): arcw.append(arcw[-1]+float(np.linalg.norm(ctrlp[i]-ctrlp[i-1])))
        arcd = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(dense, axis=0), axis=1))]); arcd *= arcw[-1]/arcd[-1]
        hh = np.interp(arcd, arcw[:len(H)], H); a0_ = arcw[len(H)-1]; rel = np.array([sstep((s_-a0_)/max(arcw[-1]-a0_, 1e-6)) for s_ in arcd])   # release toward the bun over the last leg
        new = []
        for i, q in enumerate(dense):
            loc, nrm = nearest(q); rise = RISE*(1+0.3*hsh(pid, 9))*math.exp(-((arcd[i]-1.7)/1.3)**2) if name[0] in 'ABF' else 0.0
            und = 0.14*math.sin(2*math.pi*arcd[i]/(5.5+1.5*hsh(pid, 11))+3.1*hsh(pid, 12))*sstep(arcd[i]/3.0)
            onp = loc+nrm*max(hh[i]*sstep(arcd[i]/2.2)+0.07*(1-sstep(arcd[i]/2.2))+rise+und, 0.07)
            tgq = dense[min(i+1, len(dense)-1)]-dense[max(i-1, 0)]; latq = np.cross(tgq, nrm); latq /= max(np.linalg.norm(latq), 1e-9)
            onp = onp+latq*WAVE*(1+0.4*hsh(pid, 13))*math.sin(2*math.pi*arcd[i]/(7.5+2.0*hsh(pid, 14))+3.1*hsh(pid, 15))*sstep((arcd[i]-1.5)/3.0)
            new.append(onp*(1-rel[i])+q*rel[i])
        new = np.asarray(new); new[0] = c[0]; new[-1] = end
        for _ in range(2): new[1:-1] = 0.25*new[:-2]+0.5*new[1:-1]+0.25*new[2:]
        new = resample(new, n); new = c+(new-c)*SC; new[0] = c[0]; new[-1] = end
    elif name == 'G_behind_ear':                        # volume: stand-off bulge over the first part (real mass behind the ear)
        new = c.copy(); amp = (0.55+0.2*hsh(pid, 4))*SO*SC
        for i in range(1, n-1):
            t = i/(n-1); w = math.sin(math.pi*min(t/0.62, 1.0))**1.2
            loc, nrm = nearest(c[i]); new[i] = c[i]+nrm*amp*w
    else:                                               # H back / nape: break the regular comb: alternating lateral bow + depth, different bun entries
        new = c.copy(); bow = (0.55*hsh(pid, 5))*SC; dep = (0.3*hsh(pid, 6))*SC; tg = np.gradient(c, axis=0); tg /= np.maximum(np.linalg.norm(tg, axis=1), 1e-9)[:, None]
        for i in range(1, n):
            t = i/(n-1); loc, nrm = nearest(c[i]); lat = np.cross(tg[i], nrm); lat /= max(np.linalg.norm(lat), 1e-9); w = math.sin(math.pi*t)
            new[i] = c[i]+lat*bow*w+nrm*max(dep, -0.12)*w+(lat*bow*0.9+np.array([0, 0, 0.45*hsh(pid, 8)]))*SC*sstep((t-0.7)/0.3)
    v['ctrl'] = [[round(float(x_), 4) for x_ in p] for p in new]; v['family_p'] = name; log.setdefault(name, []).append(pid)
json.dump(G, open(OUT, 'w')); print('GUIDES_P_OK', json.dumps({k: sorted(v) for k, v in log.items()}))
