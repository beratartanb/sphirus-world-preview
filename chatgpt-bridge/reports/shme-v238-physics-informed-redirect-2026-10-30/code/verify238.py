"""verify238.py (fresh editor, read-only, SHME_KIND=measure): verify237 (every V2.37 group promoted) plus V2.38: ABP knobs per promoted group,
the cut database (48 SHM238_Cut_ entries, bias -25), the contract curves on every cut clip (SHM226_V/W, SHM238_Turn/W, SHM237_FPPelvisOff),
component contract variables ClipYaw / ClipYawOn, and the installed graph patches (SHM_Snapshot setters, GR SetActorRotation on ClipYawOn).
builtins.V238_EXP = {'cut': True, 'gaze': True}. A build / configuration check only - never a motion acceptance. Prints VERIFY238."""
import builtins, json, io, contextlib
E = dict(getattr(builtins, 'V238_EXP', {}))
builtins.V237_EXP = {'stop': True, 'start': True, 'resume': True}
g7 = {'__name__': 'v237'}; buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    exec(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V237_20261029/verify237.py', encoding='utf8').read(), g7)
import unreal as u
v7 = json.loads(buf.getvalue().split('VERIFY237 ', 1)[1].strip().splitlines()[0])
bad = list(v7['bad'])
B = g7['B']; graph = g7['graph']
from qa_graph import pn as _pn, obj as _obj, info as _info
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'
abp = u.load_asset(AP); cdo = u.get_default_object(abp.generated_class())
def rd(k):
    v = cdo.get_editor_property(k); return v.get_name() if hasattr(v, 'get_name') else round(float(v), 3)
want = {'cut': {'SHM210_JogCutMode': (1.0, 0.0), 'SHM_RedirectDB_JL': ('PSD_SHM238_JogCut', 'PSD_SHM_Redirect_JogLateral'), 'SHM238_Yaw': (1.0, 0.0), 'SHM238_GuardS': (1.6, 0.8)},
        'gaze': {'SHM238_Gaze': (1.0, 0.0)}}
knobs = {}
for g, kv in want.items():
    for k, (on, off) in kv.items():
        v = rd(k); knobs[k] = v
        if v != (on if E.get(g) else off): bad.append('%s %s = %s' % (g, k, v))
d = u.load_asset('/Game/GraceRanger/SHME/Animations/V238/PSD_SHM238_JogCut'); names = [d.get_animation_asset(i).get_name() for i in range(d.get_num_animation_assets())]
dbi = [len(names), sum(x.startswith('SHM238_Cut_') for x in names), round(d.get_editor_property('continuing_pose_cost_bias'), 3)]
if dbi[1] != 48 or abs(dbi[2] + 25.0) > 1e-3: bad.append('db PSD_SHM238_JogCut %s' % dbi)
AL = u.AnimationLibrary; miss = []
for x in names:
    s = d.get_animation_asset(names.index(x)); cn = set(str(c) for c in AL.get_animation_curve_names(s, u.RawCurveTrackTypes.RCT_FLOAT))
    for need in ('SHM226_V', 'SHM226_W', 'SHM238_Turn', 'SHM238_W', 'SHM237_FPPelvisOff'):
        if need not in cn: miss.append('%s:%s' % (x, need))
if miss: bad.append('curves missing %s' % miss[:6])
comp = u.load_asset('/Game/GraceRanger/SHME/BP_SHM_HumanMotionComponent'); cv = set(str(x) for x in B.list_variables(comp))
for k in ('ClipYaw', 'ClipYawOn', 'ClipSpeed', 'ClipSpeedOn'):
    if k not in cv: bad.append('component var %s' % k)
def tids(bp, gname):
    g = graph(bp, gname); out = []
    for n in B.find_nodes(_obj(_pn(g))):
        try: out.append(str(_info(_pn(n)).type_id))
        except Exception: pass
    return out
sn = tids(abp, 'SHM_Snapshot')
patch = {k: sum(t.endswith(k) for t in sn) for k in ('SetSHM238_Cmd', 'SetSHM238_FamOff', 'SetSHM238_HoldOn', 'SetSHM238_LastWT', 'SetSHM238_GazeOn', 'SetSHM238_GazeA', 'SetSHM238_WalkSkip')}
for k, n in patch.items():
    if n < 1: bad.append('snapshot patch %s missing' % k)
gr = u.load_asset('/Game/GraceRanger/BP_GR_Player'); gt = tids(gr, 'GR_Impl_CP_PhysicalRedirect')
grp = sum('ClipYawOn' in t for t in gt)
if grp < 1: bad.append('GR ClipYawOn branch missing')
dirty = [p.get_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
out = {'v237_bad': v7['bad'], 'knobs': knobs, 'db': dbi, 'curve_missing': len(miss), 'snapshot_patches': patch, 'gr_clipyaw_nodes': grp, 'dirty': dirty, 'bad': bad, 'ALL_OK': not bad}
print('VERIFY238 ' + json.dumps(out, default=str))
