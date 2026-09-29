"""SPHIRUS artist-sculpt validator (Blender 5.2; read-only - never modifies the file).
Headless:  blender -b <file.blend> --python validate_sculpt.py -- <sculpt_package.json.gz> <report.json>
In-file:   SPHIRUS panel > Validate (runs this file; package path taken from the object property).
Compares ARTIST_SCULPT against the package (exact UE source-model LOD0 data) and SCULPT_BASE (= BR_Neutral)."""
import bpy, sys, gzip, json, math, hashlib
import numpy as np

OBJ = 'SPH_BR_ArtistSculpt'
def load_pkg(path): return json.loads(gzip.open(path, 'rb').read())
def to_ue(a): a = np.asarray(a, dtype=np.float64).reshape(-1, 3); return np.stack([a[:, 0]*100, -a[:, 1]*100, a[:, 2]*100], 1)
def hull_len(pts):
    pts = sorted(set((round(float(x), 4), round(float(y), 4)) for x, y in pts))
    if len(pts) < 3: return 0.0
    cr = lambda o, a, b: (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
    lo, up = [], []
    for p in pts:
        while len(lo) >= 2 and cr(lo[-2], lo[-1], p) <= 0: lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up) >= 2 and cr(up[-2], up[-1], p) <= 0: up.pop()
        up.append(p)
    h = lo[:-1]+up[:-1]; return sum(math.dist(h[i], h[(i+1) % len(h)]) for i in range(len(h)))
def measure(P, X):
    out = {}
    for k, m in P['measure'].items():
        if m.get('kind') == 'zrange': out[k] = float(X[:, 2].max()-X[:, 2].min()); continue
        if m.get('kind') == 'xrange':
            nb = P['NB']; body = X[:nb]; sel = np.abs(body[:, 2]-m['zc']) < m['dz']
            out[k] = float(body[sel, 0].max()-body[sel, 0].min()); continue
        ax = np.asarray(m['axis'], float); ax /= np.linalg.norm(ax)
        a1 = np.cross(ax, [1.0, 0, 0] if abs(ax[0]) < 0.9 else [0, 1.0, 0]); a1 /= np.linalg.norm(a1); a2 = np.cross(ax, a1)
        pts = X[m['ids']]; out[k] = hull_len(list(zip(pts @ a1, pts @ a2)))
    return out
def tri_normals(X, T):
    n = np.cross(X[T[:, 1]]-X[T[:, 0]], X[T[:, 2]]-X[T[:, 0]]); a = np.linalg.norm(n, axis=1); return n/np.maximum(a, 1e-12)[:, None], a/2

def validate(P, ob=None):
    R = {'checks': {}, 'metrics': {}, 'warnings': []}
    def chk(name, ok, detail=None, level='FAIL'):
        R['checks'][name] = {'result': 'PASS' if ok else level, 'detail': detail}
    ob = ob or bpy.data.objects.get(OBJ)
    chk('object_present', ob is not None and ob.type == 'MESH', OBJ)
    if ob is None: R['overall'] = 'FAIL'; return R
    me = ob.data; NB, NH = P['NB'], P['NH']; NV = NB+NH; th = P['thresholds']
    T = np.asarray([list(t) for t in P['body']['triangles']]+[[a+NB, b+NB, c+NB] for a, b, c in P['head']['triangles']], dtype=np.int64)
    # ---- topology / order ----
    chk('vertex_count', len(me.vertices) == NV, [len(me.vertices), NV])
    chk('triangle_count', len(me.polygons) == len(T), [len(me.polygons), len(T)])
    ok_topo = False
    if len(me.polygons) == len(T) and len(me.loops) == T.size:
        ls = np.zeros(len(me.polygons), np.int32); me.polygons.foreach_get('loop_start', ls)
        lt = np.zeros(len(me.polygons), np.int32); me.polygons.foreach_get('loop_total', lt)
        lv = np.zeros(len(me.loops), np.int32); me.loops.foreach_get('vertex_index', lv)
        ok_topo = (lt == 3).all() and (ls == np.arange(0, T.size, 3)).all() and (lv == T.ravel()).all()
    chk('topology_identical (polygon order + corner order + vertex ids)', bool(ok_topo))
    E = np.sort(np.concatenate([T[:, [0, 1]], T[:, [1, 2]], T[:, [2, 0]]]), 1); ne = len(np.unique(E, axis=0))
    chk('edge_count', len(me.edges) == ne, [len(me.edges), ne])
    chk('no_modifiers', len(ob.modifiers) == 0, [m.type for m in ob.modifiers])
    chk('object_transform_identity', tuple(ob.location) == (0, 0, 0) and tuple(ob.rotation_euler) == (0, 0, 0) and tuple(ob.scale) == (1, 1, 1),
        [tuple(ob.location), tuple(ob.rotation_euler), tuple(ob.scale)], level='WARN')
    # ---- UVs / materials ----
    uvok = False
    if ok_topo and me.uv_layers.get('UVMap') is not None and len(me.uv_layers) == 1:
        a = np.zeros(T.size*2, np.float32); me.uv_layers['UVMap'].data.foreach_get('uv', a); a = a.reshape(-1, 2)
        ref = np.asarray(P['body']['uv']+P['head']['uv'], np.float64).reshape(-1, 2); ref[:, 1] = 1-ref[:, 1]
        uverr = float(np.abs(a-ref).max()); uvok = uverr < 1e-6; R['metrics']['uv_max_err'] = uverr
    chk('uv_integrity (single UVMap, per-corner exact)', uvok)
    if ok_topo:
        mi = np.zeros(len(T), np.int32); me.polygons.foreach_get('material_index', mi)
        exp = np.asarray(list(P['body']['material_ids'])+[m+len(P['body']['materials']) for m in P['head']['material_ids']])
        chk('material_ids', (mi == exp).all())
    # ---- vertex groups (skin weights + protection/regions) ----
    names = {g.index: g.name for g in ob.vertex_groups}
    expw = {}
    for u, wd in enumerate(P['weights']):
        for b, w in wd.items(): expw[(u, b)] = w
    for g, d in P['groups'].items():
        for u, w in d.items(): expw[(int(u), g)] = w
    got = {}
    for v in me.vertices:
        for ge in v.groups:
            if ge.weight > 0: got[(v.index, names[ge.group])] = ge.weight
    werr = max([abs(got.get(k, 0)-w) for k, w in expw.items()]+[abs(w) for k, w in got.items() if k not in expw]+[0])
    R['metrics']['weight_max_err'] = werr
    chk('skin_weights_and_groups_unchanged', werr < 1e-5, werr)
    # ---- shape keys ----
    kb = me.shape_keys.key_blocks if me.shape_keys else {}
    need = ['ACCEPTED_B2', 'BR_NEUTRAL', 'SCULPT_BASE', 'ARTIST_SCULPT']
    chk('shape_keys_present', me.shape_keys is not None and [k.name for k in kb][:4] == need, [k.name for k in kb] if me.shape_keys else None)
    if not (me.shape_keys and all(n in kb for n in need)): R['overall'] = 'FAIL'; return R
    extra = [k.name for k in kb if k.name not in need]
    chk('no_extra_shape_keys', not extra, extra, level='WARN')
    def key(n):
        a = np.zeros(NV*3, np.float32); kb[n].data.foreach_get('co', a); return to_ue(a)
    B2 = np.asarray(P['accepted_b2']); BRN = np.asarray(P['br_neutral'])
    K = {n: key(n) for n in need}
    for n, ref in (('ACCEPTED_B2', B2), ('BR_NEUTRAL', BRN), ('SCULPT_BASE', BRN)):
        e = float(np.abs(K[n]-ref).max()); R['metrics'][f'{n}_max_err_cm'] = e
        chk(f'reference_key_unchanged:{n}', e < 1e-3, e)
    chk('reference_keys_locked', all(kb[n].lock_shape for n in need[:3]), [kb[n].lock_shape for n in need[:3]], level='WARN')
    chk('ARTIST_SCULPT_value_1_relative_to_B2', abs(kb['ARTIST_SCULPT'].value-1) < 1e-6 and kb['ARTIST_SCULPT'].relative_key.name == 'ACCEPTED_B2'
        and all(abs(kb[n].value) < 1e-6 for n in need[1:3]), [kb[n].value for n in need], level='WARN')
    A = K['ARTIST_SCULPT']
    chk('finite', bool(np.isfinite(A).all()))
    D = A-BRN; dn = np.linalg.norm(D, axis=1)*10  # mm
    # ---- locks ----
    def ids(g): return np.asarray([int(u) for u in P['groups'][g]], dtype=np.int64)
    for g in ('FACE_LOCK', 'HEAD_IDENTITY_LOCK'):
        m = float(dn[ids(g)].max()); R['metrics'][f'{g}_max_disp_mm'] = m
        chk(f'{g}_zero_displacement', m <= th['lock_disp_cm']*10, m)
    fq = np.asarray([u for u in range(NB, NV) if B2[u, 2] > 149.0])  # face-identity QA region used by every pass (head verts above z 149)
    hb = float(np.linalg.norm(A[fq]-B2[fq], axis=1).max()*10); R['metrics']['face_identity_vs_B2_max_mm'] = hb
    chk('face_identity_vs_accepted_B2_0mm (head verts z>149)', hb <= th['lock_disp_cm']*10, hb)
    sm = float(dn[ids('SEAM_LOCK')].max()); R['metrics']['SEAM_LOCK_max_disp_mm'] = sm
    chk('SEAM_LOCK_zero_displacement', sm <= th['seam_disp_cm']*10, sm)
    wp = np.asarray(P['weld_pairs']); pe = float(np.linalg.norm(A[wp[:, 0]]-A[wp[:, 1]], axis=1).max()*10)
    chk('seam_pairs_coincident', pe <= 1e-3, pe)
    # ---- displacement ----
    moved = dn > 0.01
    R['metrics']['moved_vertices'] = int(moved.sum())
    R['metrics']['disp_mm'] = {'mean_moved': float(dn[moved].mean()) if moved.any() else 0.0, 'p95_moved': float(np.percentile(dn[moved], 95)) if moved.any() else 0.0, 'max': float(dn.max())}
    lab = P['region_label']; reg = {}
    for r in sorted(set(x for x in lab if x)):
        sel = np.asarray([u for u, x in enumerate(lab) if x == r]); d = dn[sel]; mv = d > 0.01
        L = sel[B2[sel, 0] >= 0]; Rr = sel[B2[sel, 0] < 0]
        reg[r] = {'moved': int(mv.sum()), 'mean_moved_mm': round(float(d[mv].mean()), 3) if mv.any() else 0.0,
                  'p95_mm': round(float(np.percentile(d, 95)), 3), 'max_mm': round(float(d.max()), 3),
                  'mean_L_mm': round(float(dn[L].mean()), 3) if len(L) else 0, 'mean_R_mm': round(float(dn[Rr].mean()), 3) if len(Rr) else 0}
    R['metrics']['region_disp'] = reg
    mx = float(dn.max())
    chk('max_vertex_displacement', mx <= th['vert_warn_mm'], mx, level='WARN' if mx <= th['vert_fail_mm'] else 'FAIL')
    # ---- geometry sanity ----
    nA, aA = tri_normals(A, T); nB, aB = tri_normals(BRN, T)
    degen = int((aA < 1e-6).sum()); degen0 = int((aB < 1e-6).sum())
    chk('no_new_degenerate_triangles', degen <= degen0, [degen, degen0])
    flips = int(((nA*nB).sum(1) < 0).sum()); chk('no_flipped_triangles', flips == 0, flips)
    # new sharp creases: dihedral increase > 40 deg on interior edges
    Es = np.sort(np.concatenate([T[:, [0, 1]], T[:, [1, 2]], T[:, [2, 0]]]), 1); tid = np.tile(np.arange(len(T)), 3)
    o = np.lexsort((Es[:, 1], Es[:, 0])); Es, tid = Es[o], tid[o]
    same = (Es[1:] == Es[:-1]).all(1); t1, t2 = tid[:-1][same], tid[1:][same]
    angA = np.degrees(np.arccos(np.clip((nA[t1]*nA[t2]).sum(1), -1, 1))); angB = np.degrees(np.arccos(np.clip((nB[t1]*nB[t2]).sum(1), -1, 1)))
    inc = angA-angB; nc = int((inc > 40).sum()); R['metrics']['dihedral_increase_p999_deg'] = float(np.percentile(inc, 99.9))
    chk('no_new_sharp_creases (>40 deg dihedral increase)', nc == 0, nc, level='WARN')
    # ---- proportions ----
    mB2, mBR, mA = measure(P, B2), measure(P, BRN), measure(P, A)
    prop = {}
    for k in mA:
        d = (mA[k]-mBR[k])*10
        if k == 'height': ok = abs(d) <= th['height_mm']; lvl = 'FAIL'
        elif k.startswith('shoulder_width'): ok = abs(d) <= th['shoulder_width_mm']; lvl = 'FAIL'
        else: ok = abs(d) <= th['circ_warn_mm']; lvl = 'WARN' if abs(d) <= th['circ_fail_mm'] else 'FAIL'
        prop[k] = {'B2_cm': round(mB2[k], 3), 'BR_cm': round(mBR[k], 3), 'ARTIST_cm': round(mA[k], 3), 'drift_vs_BR_mm': round(d, 2), 'drift_vs_B2_mm': round((mA[k]-mB2[k])*10, 2)}
        chk(f'measure:{k}', ok, prop[k]['drift_vs_BR_mm'], level=lvl)
    R['metrics']['proportions'] = prop
    res = [c['result'] for c in R['checks'].values()]
    R['overall'] = 'FAIL' if 'FAIL' in res else ('PASS_WITH_WARNINGS' if 'WARN' in res else 'PASS')
    R['file'] = bpy.data.filepath; R['package'] = P['version']
    return R

def summary(R):
    lines = [f"OVERALL: {R['overall']}"]
    for k, c in R['checks'].items():
        if c['result'] != 'PASS': lines.append(f"  {c['result']}: {k}  {c['detail']}")
    m = R['metrics']
    if 'disp_mm' in m: lines.append('  displacement mm: moved %d, mean %.2f, p95 %.2f, max %.2f' % (m['moved_vertices'], m['disp_mm']['mean_moved'], m['disp_mm']['p95_moved'], m['disp_mm']['max']))
    for k, v in m.get('proportions', {}).items(): lines.append(f"  {k}: {v['ARTIST_cm']:.2f} cm (vs BR {v['drift_vs_BR_mm']:+.2f} mm)")
    return '\n'.join(lines)

if __name__ == '__main__' and '--' in sys.argv:
    a = sys.argv[sys.argv.index('--')+1:]
    R = validate(load_pkg(a[0]))
    open(a[1], 'w').write(json.dumps(R, indent=1)); print(summary(R))
