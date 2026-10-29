"""verify237.py (fresh editor, read-only, SHME_KIND=measure): verify236 (-> 235 -> 234 contracts) with the V2.37 switches accepted as
deliberate, plus V2.37: ABP variables per promoted group, FootPlacement DisablePelvisCurveName, V2.37 database entry lists / biases, and the
curves SHM237_FPPelvisOff (every V2.37 stop / start / re-push clip) + SHM_StopSettle (every V2.37 stop). builtins.V237_EXP = {group: True}.
A build / configuration check only - never a motion acceptance. Prints VERIFY237."""
import builtins, json, io, contextlib
E = dict(getattr(builtins, 'V237_EXP', {}))
builtins.V236_EXP = {'stop': True, 'start': True, 'rev': True, 'load': True, 'resume': False}
g6 = {'__name__': 'v236'}; buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    exec(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V236_20261028/verify236.py', encoding='utf8').read(), g6)
import unreal as u
v6 = json.loads(buf.getvalue().split('VERIFY236 ', 1)[1].strip().splitlines()[0])
def _deliberate(b):
    b = str(b)
    if E.get('stop') and 'SHM236_DB_JogStop' in b and 'PSD_SHM237_JogStop' in b: return True
    if E.get('start') and 'SHM_JogStartDB_' in b and 'PSD_SHM237_JogStartS_' in b: return True
    if E.get('resume') and 'SHM236_DB_JogResume' in b and 'PSD_SHM237_JogResume' in b: return True
    return False
bad = [b for b in v6['bad'] if not _deliberate(b)]
B = g6['B']; graph = g6['graph']
from qa_graph import pn as _pn, obj as _obj
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'
abp = u.load_asset(AP); cdo = u.get_default_object(abp.generated_class())
want = {'stop': {'SHM236_DB_JogStop': ('PSD_SHM237_JogStop', 'PSD_SHM236_JogStop2')},
        'start': {'SHM_JogStartDB_L': ('PSD_SHM237_JogStartS_L', 'PSD_SHM236_JogStartS_L'), 'SHM_JogStartDB_R': ('PSD_SHM237_JogStartS_R', 'PSD_SHM236_JogStartS_R')},
        'resume': {'SHM236_DB_JogResume': ('PSD_SHM237_JogResume', 'PSD_CP2_JogStart')}}
vars_ = {}
for g, kv in want.items():
    for k, (on, off) in kv.items():
        v = cdo.get_editor_property(k).get_name(); vars_[k] = v
        if v != (on if E.get(g) else off): bad.append('%s %s = %s' % (g, k, v))
gfi = graph(abp, 'FeetIK_Layer'); fpn = [_pn(n) for n in B.find_nodes(_obj(_pn(gfi))) if n.get_class().get_name() == 'AnimGraphNode_FootPlacement']
fpc = str(_obj(fpn[0]).get_editor_property('node').get_editor_property('pelvis_settings').get_editor_property('disable_pelvis_curve_name')) if fpn else 'NO NODE'
if fpc != 'SHM237_FPPelvisOff': bad.append('FootPlacement DisablePelvisCurveName = %s' % fpc)
V = '/Game/GraceRanger/SHME/Animations/V237/'; AL = u.AnimationLibrary; ents = {}; miss = []
for n, pre, need, bias in (('PSD_SHM237_JogStop', 'SHM237_JogStop_', 24, -25.0), ('PSD_SHM237_JogStartS_L', 'SHM237_JogStart_F_L', 1, None), ('PSD_SHM237_JogStartS_R', 'SHM237_JogStart_F_R', 1, None),
                           ('PSD_SHM237_JogResume', 'SHM237_', 99, None)):
    d = u.load_asset(V + n); names = [d.get_animation_asset(i).get_name() for i in range(d.get_num_animation_assets())]
    c = sum(x.startswith(pre) for x in names); b = round(d.get_editor_property('continuing_pose_cost_bias'), 3); ents[n] = [len(names), c, b]
    if c != need or (bias is not None and abs(b - bias) > 1e-3): bad.append('db %s %s' % (n, ents[n]))
    for i in range(d.get_num_animation_assets()):
        a = d.get_animation_asset(i)
        if not a.get_name().startswith('SHM237_'): continue
        cn = [str(x) for x in AL.get_animation_curve_names(a, u.RawCurveTrackTypes.RCT_FLOAT)]
        if 'SHM237_FPPelvisOff' not in cn or (a.get_name().startswith('SHM237_JogStop_') and 'SHM_StopSettle' not in cn): miss.append(a.get_name())
if miss: bad.append('curves missing %s' % miss[:4])
print('VERIFY237 ' + json.dumps({'v236_bad': v6['bad'], 'vars': vars_, 'fp_curve': fpc, 'dbs': ents, 'bad': bad, 'ALL_OK': not bad}, default=str))
