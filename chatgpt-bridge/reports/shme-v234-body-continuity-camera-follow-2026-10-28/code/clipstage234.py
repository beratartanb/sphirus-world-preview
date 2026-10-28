"""clipstage234.py (measure job) - the SOURCE point of the sprint upper-body stage chain: the same metrics as stage234.py (component space,
travel frame = the clip's heading axes) for every clip of the production sprint DB and its V2.33 calm copy. arm = hand fore-aft relative
to the upper arm (p2p cm), uarm_deg = upper-arm sagittal swing (p2p deg), nlat = neck_01 lateral relative to the pelvis (p2p cm),
hlat = head lateral (p2p cm), trunk = pelvis->neck forward lean (deg). Prints CLIPSTAGE234 {...}."""
import unreal as u, json, math, pathlib, sys, importlib
P = pathlib.Path(u.Paths.project_dir()).resolve(); sys.path.insert(0, str(P / 'Tools/SHME_V1_20260925'))
import v137_animedit as ae; importlib.reload(ae)
DB = '/Game/GraceRanger/Animations/LocomotionBehavior/PSD_LB_SprintLoops'; CALM = '/Game/GraceRanger/SHME/Animations/V233/SprintCalm/SHM233_Calm_'
BONES = ['root', 'pelvis', 'spine_01', 'spine_03', 'spine_05', 'neck_01', 'head', 'clavicle_l', 'clavicle_r', 'upperarm_l', 'upperarm_r', 'lowerarm_l', 'lowerarm_r', 'hand_l', 'hand_r']
def m(clip):
    A = {'l': [], 'r': []}; AG = {'l': [], 'r': []}; NL = []; HL = []; TR = []
    for f in range(clip.nf):
        fwd, left = ae.heading_axes(clip, f, None)
        c = lambda b: clip.comp(b, f, None)[0]
        pel = c('pelvis')
        for s in 'lr':
            ua = ae.vsub(c('lowerarm_' + s), c('upperarm_' + s)); AG[s].append(math.degrees(math.atan2(ae.vdot(ua, fwd), -ua[2])))
            A[s].append(ae.vdot(ae.vsub(c('hand_' + s), c('upperarm_' + s)), fwd))
        NL.append(ae.vdot(ae.vsub(c('neck_01'), pel), left)); HL.append(ae.vdot(ae.vsub(c('head'), pel), left))
        d = ae.vsub(c('neck_01'), pel); TR.append(math.degrees(math.atan2(ae.vdot(d, fwd), d[2])))
    p2p = lambda x: max(x) - min(x)
    return {'arm': round((p2p(A['l']) + p2p(A['r'])) / 2, 1), 'uarm_deg': round((p2p(AG['l']) + p2p(AG['r'])) / 2, 1), 'nlat': round(p2p(NL), 1),
            'hlat': round(p2p(HL), 1), 'trunk': round(sum(TR) / len(TR), 1)}
db = u.load_asset(DB); out = {}
for i in range(db.get_num_animation_assets()):
    a = db.get_animation_asset(i)
    if not a or a.get_class().get_name() != 'AnimSequence': continue
    nm = a.get_name(); row = {'src': m(ae.Clip(a, BONES))}
    cp = u.load_asset(CALM + nm)
    if cp: row['calm'] = m(ae.Clip(cp, BONES))
    out[nm] = row
print('CLIPSTAGE234 ' + json.dumps(out))
