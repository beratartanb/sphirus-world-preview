"""ARTIST SCULPT ROUND-TRIP - package builder (pure Python, UE engine interpreter; reads offline data only).
Collects, in UE bind space (cm, UE axes: +X = character left, +Y = character front, +Z = up):
  exact source-model LOD0 positions / triangles / per-corner UVs / material ids / skin weights / reference skeleton of
  the current BodyRealism candidate (SKM_BR_BodyMesh + SKM_BR_FaceMesh, extracted read-only by ue_as_extract.py),
  the accepted-B2 base (= those positions; BR is a morph) and the validated BR_Neutral v5 delta,
  protection/region vertex groups, seam pairs, measurement definitions and anatomical guide landmarks.
No geometry is authored here: the region groups are selections, the guides are reference curves only."""
import sys, json, gzip, math, hashlib
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'CharacterShoulderFix_20260928'))
from shc_combo import PARTS, WELD, NB, NH, CN, cid, nbr, cweights, C

OUT = C.parent/'BodyRealismArtist_20260929'; X = OUT/'extract'
EX = {p: json.load(gzip.open(X/f'{p}_topology_uv_skel.json.gz', 'rt')) for p in ('Body', 'Head')}
for p in EX:  # the extracted positions must equal the validated baseline source positions
    assert len(EX[p]['positions']) == len(PARTS[p]['pos'])
    assert max(abs(a[k]-b[k]) for a, b in zip(EX[p]['positions'], PARTS[p]['pos']) for k in range(3)) == 0.0
BR = json.load(open(C.parent/'BodyRealism_20260929'/'br_morph_v5.json'))
brd = {'Body': {int(k): v for k, v in BR['Body']['BR_Neutral'].items()}, 'Head': {int(k): v for k, v in BR['Head']['BR_Neutral'].items()}}
for j, b in WELD.items():  # seam pairs carry identical deltas (validated in the BR pass)
    assert brd['Head'].get(j, [0, 0, 0]) == brd['Body'].get(b, [0, 0, 0]), (j, b)

# combined (unwelded) vertex list used in Blender: body 0..NB-1, head NB..NB+NH-1
base = EX['Body']['positions'] + EX['Head']['positions']
brp = [list(p) for p in base]
for part, off in (('Body', 0), ('Head', NB)):
    for v, d in brd[part].items(): brp[off+v] = [brp[off+v][i]+d[i] for i in range(3)]
def cw(u): return PARTS['Body']['w'][u] if u < NB else PARTS['Head']['w'][u-NB]
# welded adjacency over the unwelded index space (head seam copies mapped onto their body partner)
def wid(u): return u if u < NB else cid('Head', u-NB)
seam_body = sorted(set(WELD.values())); seam_head = sorted(NB+j for j in WELD)
nb_u = [set() for _ in range(NB+NH)]
for part, off in (('Body', 0), ('Head', NB)):
    for t in EX[part]['triangles']:
        a, b, c = (off+t[0], off+t[1], off+t[2])
        nb_u[a] |= {b, c}; nb_u[b] |= {a, c}; nb_u[c] |= {a, b}
for j, b in WELD.items():  # couple the seam copies for region blurring / mask feathering
    nb_u[NB+j] |= nb_u[b]; nb_u[b] |= nb_u[NB+j]

def chain(u, pre): return sum(x for b, x in cw(u).items() if b.startswith(pre))
ARM = ('upperarm', 'lowerarm', 'hand', 'wrist', 'thumb', 'index', 'middle', 'ring', 'pinky')
LEG = ('thigh', 'calf', 'foot', 'ball', 'ankle', 'bigtoe', 'indextoe', 'middletoe', 'ringtoe', 'littletoe')
# mesh bind = the neutral-capture component-space bone transforms (neutral pose == bind; used by the validated LBS model).
# NOTE: the skeleton ASSET's reference pose (EX[...]['skeleton']) is the generic MetaHuman base and does NOT match this body.
from lbs import capture_affine
from shc_combo import E as _E
BIND = {p: capture_affine(_E, 'unpacked_gate_neutral', p)[1] for p in ('Body', 'Head')}
SK = {n: {'t': d['translation']} for n, d in BIND['Body'].items()}
def J(n, s='l'): t = SK[n.replace('#', s)]['t']; return t
nonskin_mats = {i for i, n in enumerate(EX['Head']['materials']) if not n.startswith('head_shader')}
head_nonskin = set()
for t, m in zip(EX['Head']['triangles'], EX['Head']['material_ids']):
    if m in nonskin_mats: head_nonskin |= {NB+t[0], NB+t[1], NB+t[2]}

# ---------------- protection groups ----------------
ZQA = 149.0     # face-identity QA line used in every previous pass (head verts above it: 0 mm)
ZLOCK = 147.0   # HEAD_IDENTITY_LOCK starts 2 cm below the QA line (buffer)
head_cy = sum(base[u][1] for u in range(NB, NB+NH) if base[u][2] > 160)/max(1, sum(1 for u in range(NB, NB+NH) if base[u][2] > 160))
FACE_LOCK = {u for u in range(NB, NB+NH) if (base[u][2] > ZQA and base[u][1] > head_cy-1.0) or u in head_nonskin}
HEAD_ID = {u for u in range(NB, NB+NH) if base[u][2] > ZLOCK} | FACE_LOCK
SEAM = set(seam_body) | set(seam_head)

# ---------------- region labels (primary) ----------------
REGIONS = ['NECK_COLLAR', 'SHOULDERS', 'CHEST_RIBCAGE', 'BREASTS', 'ABDOMEN', 'UPPER_BACK', 'LOWER_BACK', 'PELVIS_HIPS',
           'GLUTES', 'THIGHS', 'KNEES', 'CALVES_ANKLES', 'UPPER_ARMS', 'ELBOWS_FOREARMS', 'HANDS_FEET']
def spine_y(z):  # torso front/back split: interpolate the spine chain
    pts = sorted((J(n)[2], J(n)[1]) for n in ('pelvis', 'spine_01', 'spine_02', 'spine_03', 'spine_04', 'spine_05', 'neck_01'))
    if z <= pts[0][0]: return pts[0][1]
    for (z0, y0), (z1, y1) in zip(pts, pts[1:]):
        if z <= z1: return y0+(y1-y0)*(z-z0)/(z1-z0)
    return pts[-1][1]
def seg_t(p, a, b):
    ab = [b[i]-a[i] for i in range(3)]; L2 = sum(x*x for x in ab)
    return sum((p[i]-a[i])*ab[i] for i in range(3))/L2, math.sqrt(L2)
# breast apex per side: front-most torso vertex in the breast window
apex = {}
for s, sg in (('l', 1), ('r', -1)):
    # the neutral MetaHuman chest has no distinct apex (front depth peaks near the midline), so the breast centre is
    # estimated at the mid-clavicular line (|x| 8.5-10.5) at the height of maximum front depth there
    cand = [u for u in range(NB) if 8.5 < base[u][0]*sg < 10.5 and 115 < base[u][2] < 135 and chain(u, ARM) < 0.2]
    apex[s] = list(base[max(cand, key=lambda u: base[u][1])])
label = [None]*(NB+NH)
for u in range(NB+NH):
    p = base[u]; x, y, z = p; sg = 1 if x >= 0 else -1; s = 'l' if sg > 0 else 'r'
    if u in HEAD_ID: continue
    if u >= NB: label[u] = 'NECK_COLLAR'; continue
    a, lg = chain(u, ARM), chain(u, LEG)
    if a >= 0.5:
        sh, el, wr = J('upperarm_#', s), J('lowerarm_#', s), J('hand_#', s)
        t1, L1 = seg_t(p, sh, el); t2, L2 = seg_t(p, el, wr)
        if t2 > 1.0: label[u] = 'HANDS_FEET'
        elif t2 > 0 or math.dist(p, el) < 6.0: label[u] = 'ELBOWS_FOREARMS'
        elif t1 < 0.18: label[u] = 'SHOULDERS'
        else: label[u] = 'UPPER_ARMS'
        continue
    if lg >= 0.5:
        kn, an, hp = J('calf_#', s), J('foot_#', s), J('thigh_#', s)
        if z < an[2]-2.5 or (z < an[2]+1.5 and y > an[1]+4): label[u] = 'HANDS_FEET'
        elif abs(z-(kn[2]+1.5)) < 7.0: label[u] = 'KNEES'
        elif z < kn[2]: label[u] = 'CALVES_ANKLES'
        elif y < hp[1]-2.0 and z > 66: label[u] = 'GLUTES'
        elif abs(x) > abs(hp[0])+6.0 and z > 78: label[u] = 'PELVIS_HIPS'
        else: label[u] = 'THIGHS'
        continue
    front = y > spine_y(z)+1.0
    if z > 136 and abs(x) < 9 or chain(u, ('neck',)) > 0.3: label[u] = 'NECK_COLLAR'
    elif z > 122 and abs(x) > 11.5 or chain(u, ('clavicle_out', 'clavicle_scap', 'upperarm_')) > 0.35 and z > 122: label[u] = 'SHOULDERS'
    elif front:
        ax, ay, az = apex[s]
        if ((x-ax)/8.5)**2+((z-(az-1.0))/8.0)**2 < 1.0: label[u] = 'BREASTS'
        elif z >= 112: label[u] = 'CHEST_RIBCAGE'
        elif z >= 92: label[u] = 'ABDOMEN'
        else: label[u] = 'PELVIS_HIPS'
    else:
        if z >= 115: label[u] = 'UPPER_BACK'
        elif z >= 95: label[u] = 'LOWER_BACK'
        elif abs(x) < 18 and z > 68: label[u] = 'GLUTES'
        else: label[u] = 'PELVIS_HIPS'
for j, b in WELD.items(): label[NB+j] = label[b]
# soft region weights: indicator blurred 4x over the welded neighbourhood (overlapping, feathered boundaries)
def blur(w, it):
    for _ in range(it):
        w = [0.5*w[u]+0.5*sum(w[k] for k in nb_u[u])/len(nb_u[u]) if nb_u[u] else w[u] for u in range(NB+NH)]
    return w
groups = {}
for r in REGIONS:
    w = blur([1.0 if label[u] == r else 0.0 for u in range(NB+NH)], 4)
    groups[r] = {u: round(min(1.0, w[u]*1.0), 4) for u in range(NB+NH) if w[u] > 0.02 and u not in HEAD_ID}
groups['FACE_LOCK'] = {u: 1.0 for u in FACE_LOCK}
groups['HEAD_IDENTITY_LOCK'] = {u: 1.0 for u in HEAD_ID}
groups['SEAM_LOCK'] = {u: 1.0 for u in SEAM}

# ---------------- sculpt mask (1 = protected) ----------------
mask = [0.0]*(NB+NH)
for u in HEAD_ID | SEAM: mask[u] = 1.0
ring = set(SEAM); seen = set(SEAM)
for lvl, val in ((1, 0.75), (2, 0.5), (3, 0.25)):  # feather around the seam so no crease forms at the lock boundary
    ring = {k for u in ring for k in nb_u[u]} - seen; seen |= ring
    for u in ring: mask[u] = max(mask[u], val)
for u in range(NB, NB+NH):  # head collar: feather 145 -> 147 below the identity lock
    z = base[u][2]
    if 145.0 < z <= ZLOCK: mask[u] = max(mask[u], (z-145.0)/2.0)
for j, b in WELD.items(): mask[NB+j] = mask[b] = max(mask[NB+j], mask[b])

# ---------------- measurement definitions (vertex sets fixed on the base, plane = normal axis) ----------------
def torso(u): return chain(u, ARM) < 0.3 and u < NB
M = {}
def ring_ids(z, f, part_all=False):
    return [u for u in range(NB+NH) if abs(base[u][2]-z) < 0.4 and f(u, base[u]) and not (u >= NB and (u-NB) in WELD)]
M['neck_z146'] = {'ids': ring_ids(146, lambda u, p: abs(p[0]) < 8), 'axis': [0, 0, 1]}
for k, z, f in (('chest_z128', 128, lambda u, p: torso(u)), ('underbust_z119', 119, lambda u, p: torso(u)), ('waist_z109', 109, lambda u, p: torso(u)),
                ('high_hip_z97', 97, lambda u, p: torso(u) and abs(p[0]) < 20), ('hip_z86', 86, lambda u, p: torso(u) and abs(p[0]) < 22)):
    M[k] = {'ids': ring_ids(z, f), 'axis': [0, 0, 1]}
for s, sg in (('L', 1), ('R', -1)):
    M[f'thigh_{s}_z70'] = {'ids': ring_ids(70, lambda u, p, sg=sg: p[0]*sg > 0.5 and u < NB), 'axis': [0, 0, 1]}
    M[f'calf_{s}_z35'] = {'ids': ring_ids(35, lambda u, p, sg=sg: p[0]*sg > 0 and u < NB), 'axis': [0, 0, 1]}
    ls = s.lower()
    for k, a_, b_, tt in (('bicep', 'upperarm_#', 'lowerarm_#', 0.5), ('forearm', 'lowerarm_#', 'hand_#', 0.3)):
        A, B = J(a_, ls), J(b_, ls); ax = [B[i]-A[i] for i in range(3)]; L = math.sqrt(sum(q*q for q in ax)); ax = [q/L for q in ax]
        c = [A[i]+ax[i]*L*tt for i in range(3)]
        ids = [u for u in range(NB) if chain(u, ARM) > 0.5 and abs(sum((base[u][i]-c[i])*ax[i] for i in range(3))) < 0.4 and math.dist(base[u], c) < 8]
        M[f'{k}_{s}'] = {'ids': ids, 'axis': ax}
M['shoulder_width_z141'] = {'kind': 'xrange', 'zc': 141.0, 'dz': 3.0}
M['height'] = {'kind': 'zrange'}

# ---------------- anatomical guide landmarks (reference only) ----------------
# Stored as rays (UE cm) cast from INSIDE the body outward (spine axis / joint centres); the Blender build intersects them
# with the exact BR_Neutral surface, so guides lie smoothly on the skin and limbs can never occlude them.
def fr(x, z, face): return {'o': [x, spine_y(z), z], 'd': [0.0, 1.0 if face == 'front' else -1.0, 0.0]}
def azr(th, z): t = math.radians(th); return {'o': [0.0, spine_y(z), z], 'd': [math.sin(t), math.cos(t), 0.0]}
def interp(pts, n=12):
    out = []
    for k in range(len(pts)-1):
        for i in range(n+1 if k == len(pts)-2 else n):
            t = i/n; out.append(tuple(pts[k][j]+(pts[k+1][j]-pts[k][j])*t for j in range(len(pts[k]))))
    return out
guides = {'curves': {}, 'points': {}}
for s, sg in (('L', 1), ('R', -1)):
    FR = lambda pts, face: [fr(x*sg, z, face) for x, z in interp(pts)]
    AZ = lambda pts: [azr(th*sg, z) for th, z in interp(pts)]
    ls = s.lower(); ax_, ay_, az_ = apex[ls]; axa = abs(ax_)
    guides['curves'][f'CLAVICLE_{s}'] = FR([(2.2, 140.6), (7.0, 141.6), (12.5, 143.0), (15.5, 142.0)], 'front')
    guides['curves'][f'SCAPULA_SPINE_{s}'] = FR([(6.5, 138.5), (11.0, 140.0), (15.5, 141.0)], 'back')
    guides['curves'][f'SCAPULA_MEDIAL_BORDER_{s}'] = FR([(6.5, 138.5), (7.5, 128.0), (8.5, 119.0)], 'back')
    guides['curves'][f'SCAPULA_LATERAL_BORDER_{s}'] = FR([(8.5, 119.0), (12.5, 126.0), (14.5, 133.0)], 'back')
    guides['curves'][f'COSTAL_MARGIN_{s}'] = FR([(0.8, 117.5), (6.0, 112.0), (10.5, 107.5)], 'front')
    guides['curves'][f'RIBCAGE_LOWER_EDGE_{s}'] = AZ([(42.0, 106.5), (70.0, 105.0), (100.0, 104.0)])
    guides['curves'][f'ILIAC_CREST_{s}'] = AZ([(35.0, 94.5), (90.0, 98.0), (150.0, 95.0)])
    guides['curves'][f'INGUINAL_LINE_{s}'] = FR([(10.5, 94.5), (6.0, 90.0), (3.0, 86.5)], 'front')
    guides['curves'][f'INFRAMAMMARY_FOLD_{s}'] = FR([(axa-6.5, az_-6.5), (axa, az_-8.0), (axa+6.0, az_-5.5)], 'front')
    guides['curves'][f'GLUTEAL_FOLD_{s}'] = FR([(2.5, 76.5), (7.0, 75.5), (11.5, 77.5)], 'back')
    guides['points'][f'BREAST_CENTER_EST_{s}'] = fr(ax_, az_, 'front')
    guides['points'][f'ASIS_{s}'] = fr(10.5*sg, 94.5, 'front')
    guides['points'][f'PSIS_DIMPLE_{s}'] = fr(4.0*sg, 93.0, 'back')
    sh = J('upperarm_#', ls); n_ = math.hypot(0.45, 0.9)
    guides['points'][f'ACROMION_{s}'] = {'o': list(sh), 'd': [sg*0.45/n_, 0.0, 0.9/n_]}
    el = J('lowerarm_#', ls); n_ = math.hypot(0.3, 1.0)
    guides['points'][f'OLECRANON_{s}'] = {'o': list(el), 'd': [sg*0.3/n_, -1.0/n_, 0.0]}
    kn = J('calf_#', ls); an = J('foot_#', ls)
    guides['curves'][f'PATELLA_{s}'] = [{'o': [kn[0]+2.4*math.cos(a*math.pi/12), kn[1], kn[2]+1.5+2.9*math.sin(a*math.pi/12)], 'd': [0.0, 1.0, 0.0]} for a in range(25)]
    guides['curves'][f'ACHILLES_{s}'] = [{'o': [an[0], an[1], an[2]+1+k], 'd': [0.0, -1.0, 0.0]} for k in range(14)]
guides['curves']['STERNUM'] = [fr(0.0, z, 'front') for (z,) in interp([(141.0,), (118.0,)])]
guides['curves']['LINEA_ALBA'] = [fr(0.0, z, 'front') for (z,) in interp([(116.0,), (90.0,)], 20)]
guides['curves']['SPINE_ERECTOR_VALLEY'] = [fr(0.0, z, 'back') for (z,) in interp([(142.0,), (96.0,)], 30)]
guides['points']['STERNAL_NOTCH'] = fr(0.0, 141.2, 'front')
guides['points']['XIPHOID'] = fr(0.0, 117.5, 'front')
guides['points']['C7_VERTEBRA'] = fr(0.0, 143.0, 'back')
guides['points']['NAVEL_APPROX'] = fr(0.0, 102.0, 'front')

# ---------------- write ----------------
def uv_corners(part):
    s = EX[part]['uv_sets'][0]; el = s['elements']
    return [[el[str(e)] for e in t] for t in s['tri_elements']]
pkg = {
    'version': 'SPH_BR_ArtistSculpt_20260929_v1',
    'coords': 'UE bind space, cm; Blender = (x, -y, z) * 0.01 m; UV Blender v = 1 - UE v',
    'NB': NB, 'NH': NH,
    'body': {'triangles': EX['Body']['triangles'], 'uv': uv_corners('Body'), 'material_ids': EX['Body']['material_ids'], 'materials': EX['Body']['materials']},
    'head': {'triangles': EX['Head']['triangles'], 'uv': uv_corners('Head'), 'material_ids': EX['Head']['material_ids'], 'materials': EX['Head']['materials']},
    'accepted_b2': base, 'br_neutral': brp,
    'weights': [cw(u) for u in range(NB+NH)],
    'skeleton': {'bind_source': 'EquivalenceFix_20260929/unpacked_gate_neutral_front.json bone_transforms (component space, cm)',
                 'Body': {'path': EX['Body']['skeleton']['path'], 'parents': {b['name']: b['parent'] for b in EX['Body']['skeleton']['bones']},
                          'order': [b['name'] for b in EX['Body']['skeleton']['bones']], 'bind': BIND['Body'], 'asset_ref_pose_generic': EX['Body']['skeleton']['bones']},
                 'Head': {'path': EX['Head']['skeleton']['path'], 'parents': {b['name']: b['parent'] for b in EX['Head']['skeleton']['bones']},
                          'order': [b['name'] for b in EX['Head']['skeleton']['bones']], 'bind': BIND['Head']}},
    'weld_pairs': [[b, NB+j] for j, b in sorted(WELD.items())],
    'groups': {k: {str(u): w for u, w in v.items()} for k, v in groups.items()},
    'region_label': label, 'mask': mask,
    'measure': {k: v for k, v in M.items()}, 'guides': guides, 'breast_apex': apex,
    'thresholds': {'lock_disp_cm': 1e-4, 'seam_disp_cm': 1e-4, 'height_mm': 1.0, 'shoulder_width_mm': 5.0,
                   'circ_warn_mm': 5.0, 'circ_fail_mm': 10.0, 'vert_warn_mm': 8.0, 'vert_fail_mm': 20.0},
    'sources': {'body_mesh': '/Game/Sphirus/CharacterLab/BodyRealism_20260929/SKM_BR_BodyMesh', 'head_mesh': '/Game/Sphirus/CharacterLab/BodyRealism_20260929/SKM_BR_FaceMesh',
                'br_morph': 'Saved/Codex/BodyRealism_20260929/br_morph_v5.json', 'accepted_b2': '/Game/Sphirus/CharacterLab/NativeBody_20260928/MH_B2_PendingNativeWorkflow'},
}
B = OUT/'Blender'; B.mkdir(parents=True, exist_ok=True)
raw = json.dumps(pkg, separators=(',', ':')).encode()
with gzip.open(B/'sculpt_package.json.gz', 'wb') as f: f.write(raw)
summary = {'sha256_json': hashlib.sha256(raw).hexdigest(), 'verts': NB+NH, 'tris': len(pkg['body']['triangles'])+len(pkg['head']['triangles']),
           'groups': {k: len(v) for k, v in groups.items()}, 'labels': {r: label.count(r) for r in REGIONS},
           'masked_full': sum(1 for m in mask if m >= 1.0), 'masked_partial': sum(1 for m in mask if 0 < m < 1),
           'measure_verts': {k: len(v.get('ids', [])) for k, v in M.items()}, 'guides': {k: len(v) for k, v in guides['curves'].items()},
           'points': list(guides['points']), 'breast_apex': apex, 'head_center_y': head_cy}
(B/'package_summary.json').write_text(json.dumps(summary, indent=1)); print(json.dumps(summary, indent=1))
