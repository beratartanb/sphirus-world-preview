"""probe250_blendfk.py (measure job, read-only): does a LOCAL-space crossfade from the standing idle sample to a turning-start crop frame
drive the feet through the floor? Idle = af_Stand_Idle_NaturalBaseline_Phase275 @ 79.40 s (the in-game frozen idle sample before every
v249/v250 turn entry); target = each SHM248 turn crop @ 0.0 / 0.05 s. For w = 0..1 every bone of the leg chains is blended (slerp rotation,
lerp translation) and forward kinematics gives ball / ankle height and foot pitch. Also reports per-joint local angle differences.
Prints BLENDFK250 {...}."""
import unreal as u, json, math, sys, importlib
sys.path.insert(0, r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925')
import v137_animedit as ae; importlib.reload(ae)
ar = u.AssetRegistryHelpers.get_asset_registry()
allseq = {str(a.asset_name): str(a.package_name) for a in ar.get_assets_by_class(u.TopLevelAssetPath('/Script/Engine', 'AnimSequence'), True)}
idle = u.load_asset(allseq['af_Stand_Idle_NaturalBaseline_Phase275'])
BONES = ['ball_l', 'ball_r']
def local_at(seq, t):
    o = u.AnimPoseEvaluationOptions(); o.set_editor_property('evaluation_type', u.AnimDataEvalType.RAW)
    p = u.AnimPoseExtensions.get_anim_pose_at_time(seq, t, o)
    chain = {}
    for b in BONES:
        for x in ae.bone_path(seq, b): chain[x] = None
    for x in chain:
        tr = u.AnimPoseExtensions.get_bone_pose(p, x, u.AnimPoseSpaces.LOCAL)
        chain[x] = (ae.from_ue_v(tr.translation), ae.qnorm(ae.from_ue_q(tr.rotation)))
    return chain
par = {}
for b in BONES:
    pth = ae.bone_path(idle, b)
    for i, x in enumerate(pth): par[x] = pth[i + 1] if i + 1 < len(pth) else None
def fk(L, bone):
    ch = []; b = bone
    while b: ch.append(b); b = par[b]
    t = (0.0, 0.0, 0.0); q = (0.0, 0.0, 0.0, 1.0)
    for b in reversed(ch):
        lt, lq = L[b]; t = ae.vadd(t, ae.qrot(q, lt)); q = ae.qnorm(ae.qmul(q, lq))
    return t
def slerp(a, b, w):
    d = sum(x * y for x, y in zip(a, b))
    if d < 0: b = tuple(-x for x in b); d = -d
    if d > 0.9995: return ae.qnorm(tuple(x + w * (y - x) for x, y in zip(a, b)))
    th = math.acos(d); s = math.sin(th); return tuple((math.sin((1 - w) * th) * x + math.sin(w * th) * y) / s for x, y in zip(a, b))
def ang(a, b):
    d = abs(sum(x * y for x, y in zip(a, b))); return round(math.degrees(2 * math.acos(min(1.0, d))), 1)
def pitch(f, b): return round(math.degrees(math.atan2(f[2] - b[2], math.hypot(b[0] - f[0], b[1] - f[1]))), 1)
A = local_at(idle, 79.40); out = {'idle': {s: [round(fk(A, 'ball_' + s)[2], 1), round(fk(A, 'foot_' + s)[2], 1)] for s in 'lr'}, 'crops': {}}
for n in sorted(k for k in allseq if k.startswith('SHM248_Jog_Start_Turn') and k.endswith('_crop')):
    seq = u.load_asset(allseq[n]); rec = {}
    for t in (0.0, 0.05):
        Bp = local_at(seq, t); rows = []
        for w in (0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8, 1.0):
            L = {x: (tuple(a + w * (b - a) for a, b in zip(A[x][0], Bp[x][0])), slerp(A[x][1], Bp[x][1], w)) for x in A}
            r = [w]
            for s in 'lr':
                f = fk(L, 'foot_' + s); b = fk(L, 'ball_' + s); r += [round(b[2], 1), round(f[2], 1), pitch(f, b)]
            rows.append(r)
        rec['t%.2f' % t] = {'rows': rows, 'joint_deg': {x: ang(A[x][1], Bp[x][1]) for x in A}}
    out['crops'][n] = rec
print('BLENDFK250 ' + json.dumps(out))
