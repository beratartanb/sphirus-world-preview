"""CharacterFinal BR_Neutral v6: the accepted BR v5 feature set (imported from br_sculpt.py) + targeted secondary /
soft-tissue corrections from the 2026-09-29 body audit (breast root & lateral transition, inframammary softening,
sternal plane, flank pad, lower abdomen, glute-ham weight & lateral fold fade, inner thigh) and a foot / ankle pass
(medial arch lift, malleoli, Achilles hollows, heel pad) that is exempt from the low-pass subtraction (the arch is a
silhouette change by intent, ~8 mm, everything else stays a detail layer). PROCEDURAL — not an artist sculpt.
usage (cwd = Tools/CharacterShoulderFix_20260928): python ../CharacterFinal_20260929/cf_sculpt.py [gain]"""
import sys, json, math, os
sys.path.insert(0, '.')
import br_sculpt as B
from br_sculpt import F, FEAT, e2, seg2, fac, chainw, limb, azg, g1, BT, cpos, NR, CN, NB, WELD, nbr, ASYM, GM
from pathlib import Path
VER = 'v6'; GAIN = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0
OUT = B.C.parent/'CharacterFinal_20260929'; OUT.mkdir(exist_ok=True)
def e3(p, c, r): return math.exp(-sum(((p[i]-c[i])/r[i])**2 for i in range(3)))
# ---- breast / ribcage: attachment and transitions, not size
@F('lateral_root_soften', 'breast')
def _(v, p, n, sg, s): return -0.7*e2(p[0]*sg, p[2], 13.6, 126.0, 1.7, 4.5)*fac(n, 'front', sg)+0.45*e2(p[0]*sg, p[2], 16.5, 125.0, 2.2, 4.5)*fac(n, 'lat', sg)
@F('axillary_tail', 'breast')
def _(v, p, n, sg, s): return 0.35*seg2(p[0]*sg, p[2], (14.0, 129.0), (17.5, 134.0), 1.6)*max(fac(n, 'front', sg), fac(n, 'lat', sg))
@F('imf_soften', 'breast')
def _(v, p, n, sg, s): return 0.55*seg2(p[0]*sg, p[2], (4.5, 115.8), (12.5, 117.6), 1.2)*fac(n, 'front', sg)+0.4*e2(p[0]*sg, p[2], 7.5, 121.5, 3.5, 2.4)*fac(n, 'front', sg)-0.3*seg2(p[0]*sg, p[2], (4.0, 117.6), (13.0, 119.6), 0.7)*fac(n, 'front', sg)
@F('upper_pole_relax', 'breast')
def _(v, p, n, sg, s): return -0.3*e2(p[0]*sg, p[2], 8.0, 134.0, 4.0, 2.5)*fac(n, 'front', sg)
@F('sternal_plane', 'chest')
def _(v, p, n, sg, s): return -0.3*e2(p[0], p[2], 0.0, 127.0, 2.2, 5.0)*fac(n, 'front', sg)
# ---- abdomen / flank
@F('flank_pad', 'abdomen')
def _(v, p, n, sg, s): return 0.45*e2(p[0]*sg, p[2], 13.5, 99.0, 2.5, 3.5)*max(fac(n, 'lat', sg), 0.6*fac(n, 'front', sg), 0.6*fac(n, 'back', sg))
@F('lower_abdomen_soft', 'abdomen')
def _(v, p, n, sg, s): return 0.4*e2(p[0], p[2], 0.0, 91.0, 6.0, 3.0)*fac(n, 'front', sg)
# ---- glutes
@F('glute_ham_weight', 'glute')
def _(v, p, n, sg, s): return 0.5*e2(p[0]*sg, p[2], 7.5, 74.0, 4.0, 1.8)*fac(n, 'back', sg)
@F('fold_lateral_fade', 'glute')
def _(v, p, n, sg, s): return 0.45*seg2(p[0]*sg, p[2], (9.5, 77.3), (13.0, 78.2), 0.9)*fac(n, 'back', sg)
@F('lower_glute_medial', 'glute')
def _(v, p, n, sg, s): return 0.35*e2(p[0]*sg, p[2], 5.0, 79.5, 2.5, 3.0)*fac(n, 'back', sg)
@F('lateral_glute_soft', 'glute')
def _(v, p, n, sg, s): return -0.25*e2(p[0]*sg, p[2], 15.5, 84.0, 2.0, 3.0)*max(fac(n, 'lat', sg), fac(n, 'back', sg))
# ---- thighs (shorts)
@F('inner_thigh_soft', 'thigh')
def _(v, p, n, sg, s):
    if chainw(v, ('thigh',)) < 0.4: return 0.0
    t, az = limb(p, *B.TH(s), sg); return 0.25*g1(t, 0.18, 0.15)*azg(az, -90, 40)
# ---- feet / ankle (vector field, no low-pass)
FT = lambda s: (BT(f'foot_{s}'), BT(f'ball_{s}'))
FOOTV = {}
def foot_vec(v, p, n, sg, s):
    """returns (dx, dy, dz) in mm or None. Left foot: medial edge = small |x|, lateral = large |x|."""
    if chainw(v, ('foot', 'ball', 'bigtoe', 'indextoe', 'middletoe', 'ringtoe', 'littletoe', 'calf')) < 0.3 or p[2] > 18: return None
    xa = abs(p[0]); y = p[1]; z = p[2]
    d = [0.0, 0.0, 0.0]
    # medial longitudinal arch: lift the medial half of the sole between the heel pad and the ball (y 2..11)
    if z < 3.2:
        wm = max(0.0, min(1.0, (14.3-xa)/4.2)); a = g1(y, 6.5, 4.2)*wm*max(0.0, 1-z/4.5)
        d[2] += 8.5*a
        # lateral arch: much lower
        wl = max(0.0, min(1.0, (xa-15.5)/3.0)); d[2] += 1.5*g1(y, 7.0, 4.0)*wl*max(0.0, 1-z/2.0)
    # malleoli: medial (higher, more forward) and lateral bumps along the normal
    med = 1.3*e3([xa, y, z], [9.6, 1.6, 9.4], [1.8, 1.9, 1.7])*max(0.0, -n[0]*sg)
    lat = 1.0*e3([xa, y, z], [16.4, 0.6, 8.3], [1.8, 1.9, 1.6])*max(0.0, n[0]*sg)
    # hollows either side of the Achilles, Achilles ridge, heel pad rounding
    hol = -0.7*(e3([xa, y, z], [10.6, -3.4, 10.5], [1.4, 1.6, 2.4])+e3([xa, y, z], [14.6, -3.4, 10.0], [1.4, 1.6, 2.4]))*max(0.0, -n[1])
    ach = 0.5*e3([xa, y, z], [12.6, -4.0, 12.0], [1.0, 1.4, 4.0])*max(0.0, -n[1])
    heel = 0.5*e3([xa, y, z], [12.6, -3.0, 1.6], [2.4, 2.0, 1.4])*max(0.0, -n[1]*0.6+max(0.0, -n[2])*0.8)
    # metatarsal heads / ball: slight fullness on the sole under the ball, dorsal tendon hint to the big toe
    ball = 0.4*e3([xa, y, z], [14.0, 14.5, 0.6], [3.0, 2.0, 1.0])*max(0.0, -n[2])
    ext = 0.35*seg2(xa, y, (12.4, 6.0), (12.8, 15.0), 0.8)*max(0.0, n[2])*(1.0 if z < 6 else 0.0)
    amp = med+lat+hol+ach+heel+ball+ext
    for i in range(3): d[i] += n[i]*amp
    return d if any(abs(x) > 1e-4 for x in d) else None
# ---- hands (light: knuckle hierarchy and thenar fullness; scale untouched)
def hand_vec(v, p, n, sg, s):
    if chainw(v, ('hand', 'index', 'middle', 'ring', 'pinky', 'thumb')) < 0.5: return None
    amp = 0.0
    for f_ in ('index', 'middle', 'ring', 'pinky'):
        j = BT(f'{f_}_01_{s}'); amp += 0.45*e3(p, j, [1.1, 1.1, 1.1])
    j = BT(f'thumb_01_{s}'); amp += 0.35*e3(p, j, [1.6, 1.6, 1.6])
    if amp < 0.01: return None
    return [n[i]*amp for i in range(3)]

def main():
    disp = [0.0]*CN; per = {}; vec = {}
    for v in range(CN):
        if v >= NB and (v-NB) in WELD: continue
        p = cpos[v]; n = NR[v]; sg = 1 if p[0] >= 0 else -1; s = 'l' if sg > 0 else 'r'
        tot = 0.0
        for name, group, fn in FEAT:
            a = fn(v, p, n, sg, s)
            if a:
                a *= ASYM[s].get(group, ASYM[s].get('default', 1.0)) if s == 'r' else 1.0
                a *= GM.get(group, 1.0); tot += a; per[name] = max(per.get(name, 0.0), abs(a))
        if v >= NB: tot *= max(0.0, min(1.0, (149.0-p[2])/2.0))
        disp[v] = tot*GAIN
        if v < NB:
            fv = foot_vec(v, p, n, sg, s); hv = hand_vec(v, p, n, sg, s)
            if fv or hv:
                d = [0.0, 0.0, 0.0]
                for src in (fv, hv):
                    if src: d = [d[i]+src[i] for i in range(3)]
                vec[v] = [x*GAIN for x in d]
    for _ in range(2):
        nd = list(disp)
        for v in range(CN):
            if disp[v] == 0.0 and all(disp[u] == 0.0 for u in nbr[v]): continue
            nd[v] = 0.5*disp[v]+0.5*sum(disp[u] for u in nbr[v])/len(nbr[v])
        disp = nd
    LPI = int(os.environ.get('BR_LPI', '40'))
    if LPI:
        lp = list(disp)
        for _ in range(LPI): lp = [0.5*lp[v]+0.5*sum(lp[u] for u in nbr[v])/len(nbr[v]) if nbr[v] else lp[v] for v in range(CN)]
        disp = [disp[v]-lp[v] for v in range(CN)]
    # smooth the vector field (feet / hands) 3 iterations, then merge
    keys = set(vec)
    for _ in range(2):
        nv = {}
        for v in keys | {u for k in keys for u in nbr[k]}:
            acc = [0.0, 0.0, 0.0]; cnt = 0
            for u in nbr[v] | {v}:
                if u in vec: acc = [acc[i]+vec[u][i] for i in range(3)]
                cnt += 1
            nv[v] = [x/cnt*0.5+(vec.get(v, [0, 0, 0])[i]*0.5) for i, x in enumerate(acc)]
        vec = {v: d for v, d in nv.items() if any(abs(x) > 1e-4 for x in d)}; keys = set(vec)
    for v in range(CN):
        if v >= NB and cpos[v][2] > 149.0: disp[v] = 0.0
    morph = {'Body': {'BR_Neutral': {}}, 'Head': {'BR_Neutral': {}}}
    for v in range(CN):
        if v >= NB and (v-NB) in WELD: continue
        d = [NR[v][i]*disp[v]*0.1 for i in range(3)]
        if v in vec: d = [d[i]+vec[v][i]*0.1 for i in range(3)]
        if math.sqrt(sum(x*x for x in d)) < 0.0005: continue
        if v < NB: morph['Body']['BR_Neutral'][str(v)] = d
        else: morph['Head']['BR_Neutral'][str(v-NB)] = d
    for j, bi in WELD.items():
        if str(bi) in morph['Body']['BR_Neutral']: morph['Head']['BR_Neutral'][str(j)] = morph['Body']['BR_Neutral'][str(bi)]
    mags = sorted(math.sqrt(sum(x*x for x in d))*10 for d in morph['Body']['BR_Neutral'].values())
    fm = sorted(math.sqrt(sum(x*x for x in d)) for d in vec.values())
    stats = {'moved_verts': len(mags), 'mean_mm': sum(mags)/len(mags), 'p95_mm': mags[int(len(mags)*.95)], 'max_mm': mags[-1], 'feet_hands_verts': len(vec), 'feet_hands_max_mm': fm[-1] if fm else 0, 'feature_max_mm': {k: round(v, 2) for k, v in per.items()}}
    (OUT/f'br_morph_{VER}.json').write_text(json.dumps(morph)); (OUT/f'br_stats_{VER}.json').write_text(json.dumps(stats, indent=1))
    print(json.dumps({k: (round(v, 3) if isinstance(v, float) else v) for k, v in stats.items() if k != 'feature_max_mm'}), 'body', len(morph['Body']['BR_Neutral']), 'head', len(morph['Head']['BR_Neutral']))
    print({k: v for k, v in stats['feature_max_mm'].items() if k in ('lateral_root_soften', 'axillary_tail', 'imf_soften', 'flank_pad', 'glute_ham_weight', 'fold_lateral_fade')})
if __name__ == '__main__': main()
