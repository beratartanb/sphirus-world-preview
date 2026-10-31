"""verify241.py (read-only, SHME_KIND=measure): verify240 (V2.37..V2.40 production) + the V2.41 state:
  - ABP knobs SHM241_KOn 0 / SHM241_PushYawK 1 / SHM241_StartOn 0 (inert unless promoted), SHM241_StartHold 0.8
  - pawn BP_GR_Player defaults GR241_YawRateK 1, GR241_StartOn False
  - the 362 per-contact entry databases PSD_SHM240_E<eidx>_K<k> hold exactly their one clip and are the defaults of SHM241_K000..K383
    (missing slots = the V2.40 E database)
  - the 8 turning start copies carry SHM241_SYaw / SHM241_SW; the LookAtAimOffset node still plays the vendor BS_Neutral_AO_Stand
    (the regional copy BS_SHM241_AO_Head exists, 15 samples)
  - SHM_Snapshot exec integrity: no orphaned impure node (V2.40 exec-splice trap)
Prints VERIFY241 {...}."""
import builtins, json, io, contextlib, re
g0 = {'__name__': 'v240'}; buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    exec(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V240_20261030/verify240.py', encoding='utf8').read(), g0)
import unreal as u
v0 = json.loads(buf.getvalue().split('VERIFY240 ', 1)[1].strip().splitlines()[0])
B = g0['B']; graph = g0['graph']
from qa_graph import src, pn, info, obj
bad = list(v0['bad'])
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; bp = u.load_asset(AP)
cdo = u.get_default_object(bp.generated_class())
def dv(o, n):
    try: return o.get_editor_property(n)
    except Exception: return None
EXP = {'SHM241_KOn': 0.0, 'SHM241_PushYawK': 1.0, 'SHM241_StartOn': 0.0, 'SHM241_StartHold': 0.8}
knobs = {k: dv(cdo, k) for k in EXP}
for k, v in EXP.items():
    if knobs[k] is None or abs(float(knobs[k]) - v) > 1e-6: bad.append('%s %s (expected %s)' % (k, knobs[k], v))
pc = u.get_default_object(u.load_asset('/Game/GraceRanger/BP_GR_Player').generated_class())
pk = {'GR241_YawRateK': dv(pc, 'GR241_YawRateK'), 'GR241_StartOn': dv(pc, 'GR241_StartOn')}
if pk['GR241_YawRateK'] is None or abs(float(pk['GR241_YawRateK']) - 1.0) > 1e-6: bad.append('GR241_YawRateK %s' % pk['GR241_YawRateK'])
if pk['GR241_StartOn'] is not False: bad.append('GR241_StartOn %s' % pk['GR241_StartOn'])
V41 = '/Game/GraceRanger/SHME/Animations/V241/'; kbad = []; nk = 0
for i in range(384):
    e, k = i // 4, i % 4 + 1; p = V41 + 'PSD_SHM240_E%02d_K%d' % (e, k); dfl = dv(cdo, 'SHM241_K%03d' % i)
    if u.EditorAssetLibrary.does_asset_exist(p):
        d = u.load_asset(p); nk += 1
        if d.get_num_animation_assets() != 1: kbad.append('%s entries %d' % (p.split('/')[-1], d.get_num_animation_assets()))
        if dfl is None or dfl.get_name() != d.get_name(): kbad.append('K%03d default %s' % (i, dfl))
    elif dfl is None or dfl.get_name() != 'PSD_SHM240_E%02d' % e: kbad.append('K%03d fallback %s' % (i, dfl))
if kbad: bad.append('per-K dbs %s' % kbad[:6])
AL = u.AnimationLibrary; nocurve = []
for s in ('L045_Lfoot', 'L090_Lfoot', 'L135_Lfoot', 'L180_Lfoot', 'R045_Rfoot', 'R090_Rfoot', 'R135_Rfoot', 'R180_Rfoot'):
    a = u.load_asset('/Game/GraceRanger/SHME/Animations/Starts/Jog/SHM_JogQ_af_Loco_Jog_Start_Turn%s_AAMS' % s)
    cs = set(str(c) for c in AL.get_animation_curve_names(a, u.RawCurveTrackTypes.RCT_FLOAT))
    if not {'SHM241_SYaw', 'SHM241_SW'} <= cs: nocurve.append(s)
if nocurve: bad.append('start yaw curves missing %s' % nocurve)
ao = []
for g in B.list_graphs(bp):
    if g.get_name() == 'LookAtAimOffset':
        for n in B.find_nodes(g):
            if n.get_class().get_name() == 'AnimGraphNode_BlendSpacePlayer':
                b = n.get_editor_property('node').get_editor_property('blend_space'); ao.append(b.get_name() if b else None)
if 'BS_Neutral_AO_Stand' not in ao: bad.append('AO node %s' % ao)
hb = u.load_asset(V41 + 'AO/BS_SHM241_AO_Head'); nhs = len(hb.get_editor_property('sample_data')) if hb else 0
if nhs != 15: bad.append('BS_SHM241_AO_Head samples %d' % nhs)
sg = pn(graph(bp, 'SHM_Snapshot')); sn = [pn(n) for n in B.find_nodes(obj(sg))]; orphan = []
for p in sn:
    if 'execute' in [q.name for q in info(p).input_pins] and not src((p, 'execute')): orphan.append(str(info(p).type_id)[-50:])
if orphan: bad.append('snapshot orphan exec %s' % orphan[:6])
dirty = [p.get_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
out = {'v240_ALL_OK': v0['ALL_OK'], 'knobs': {k: float(v) if v is not None else None for k, v in knobs.items()}, 'pawn': {k: str(v) for k, v in pk.items()},
       'k_dbs': nk, 'k_bad': len(kbad), 'ao_node': ao, 'ao_head_samples': nhs, 'snapshot_orphans': len(orphan), 'dirty': dirty, 'bad': bad, 'ALL_OK': not bad}
print('VERIFY241 ' + json.dumps(out, default=str))
