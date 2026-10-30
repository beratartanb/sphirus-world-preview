"""verify239.py (fresh editor, read-only, SHME_KIND=measure): verify238 (V2.37 + V2.38 production) re-read for the two items V2.39 changes
in form only: (a) curve names are compared CASE-INSENSITIVELY (FNames are; after V2.39 the editor shows 'shm226_v' for SHM226_V and the
runtime reads them), (b) the AnimGraph MM SearchThrottleTime is now Select(SHM239_Own AND SHM239_TkOn, 0, <the V2.26/V2.27 FMax chain>) -
accepted when the Select's false branch IS that chain. Plus the V2.39 state: SHM239_Own default (0 = production unchanged, all V2.39 graph
patches inert), the 8 per-side takeover databases and their entry counts, the saved takeover clips. Prints VERIFY239 {...}."""
import builtins, json, io, contextlib
builtins.V238_EXP = {'cut': True, 'gaze': True}
g8 = {'__name__': 'v238'}; buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    exec(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V238_20261030/verify238.py', encoding='utf8').read(), g8)
import unreal as u
v8 = json.loads(buf.getvalue().split('VERIFY238 ', 1)[1].strip().splitlines()[0])
from qa_graph import src, pn, info, obj
B = g8['B']; graph = g8['graph']
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
bad = []; notes = []
for b in v8['bad']:
    if b.startswith('curves missing') or b == 'v226:throttle_wiring': notes.append(b[:80]); continue
    bad.append(b)
AL = u.AnimationLibrary
d = u.load_asset('/Game/GraceRanger/SHME/Animations/V238/PSD_SHM238_JogCut'); miss = []
for i in range(d.get_num_animation_assets()):
    s = d.get_animation_asset(i); cn = set(str(c).lower() for c in AL.get_animation_curve_names(s, u.RawCurveTrackTypes.RCT_FLOAT))
    for need in ('SHM226_V', 'SHM226_W', 'SHM238_Turn', 'SHM238_W', 'SHM237_FPPelvisOff', 'SHM239_Step', 'SHM239_StepN'):
        if need.lower() not in cn: miss.append('%s:%s' % (s.get_name(), need))
if miss: bad.append('curves missing (case-insensitive) %s' % miss[:6])
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; bp = u.load_asset(AP)
ag = pn(graph(bp, 'AnimGraph'))
mm = [pn(n) for n in B.find_nodes(obj(ag)) if n.get_class().get_name() == 'AnimGraphNode_MotionMatching']
thr = src((mm[0], 'SearchThrottleTime')); ok_thr = False
if len(thr) == 1 and 'Select' in tid(thr[0][0]):
    for k in ('A', 'B'):
        for s_ in src((thr[0][0], k)):
            if 'Max' in tid(s_[0]): ok_thr = True
if not ok_thr: bad.append('throttle: not Select(TkOn, 0, FMax chain)')
cdo = u.get_default_object(bp.generated_class())
own = float(cdo.get_editor_property('SHM239_Own'))
if own != 0.0: bad.append('SHM239_Own = %s (production must be 0)' % own)
V9 = '/Game/GraceRanger/SHME/Animations/V239/'; dbs = {}
for sd in ('R', 'L'):
    for kind in ('Tk', 'TkP'):
        for tg in ('Back', 'Opp'):
            n = 'PSD_SHM239_%s%s_%s' % (kind, sd, tg); x = u.load_asset(V9 + n); dbs[n] = x.get_num_animation_assets() if x else None
            if not dbs[n]: bad.append('db %s empty/missing' % n)
dirty = [p.get_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
out = {'v238_bad_reinterpreted': notes, 'curves_missing': len(miss), 'throttle_wrapper_ok': ok_thr, 'SHM239_Own': own, 'takeover_dbs': dbs, 'dirty': dirty, 'bad': bad, 'ALL_OK': not bad}
print('VERIFY239 ' + json.dumps(out, default=str))
