"""verify240.py (fresh editor, read-only, SHME_KIND=measure): verify239 (V2.37..V2.39 production) + the V2.40 state:
  - SHM239_Own default 0 (all V2.39/V2.40 takeover patches inert), SHM240_Det 1, SHM240_Retry 0.05, SHM240_YSpd 80, SHM240_BlkSpd 60,
    SHM240_AOFadeRate 4; SHM240_ExtOn / SHM240_HeadOn / SHM240_BlkDB reported (0 / stand DB unless promoted)
  - the 96 deterministic entry databases PSD_SHM240_E00..E95 exist, are non-empty and are the defaults of SHM240_E00..E95
  - the 48 V2.38 cut clips carry SHM240_Src (case-insensitive)
  - SHM_Snapshot exec integrity (V2.40 exec-splice trap): every impure node in the graph has an incoming exec link (no orphaned tail) and
    SetSHM240_WasTk has its 3 incoming links (exit branch then/else + EDB cast fail)
Prints VERIFY240 {...}."""
import builtins, json, io, contextlib
g9 = {'__name__': 'v239'}; buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    exec(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V239_20261030/verify239.py', encoding='utf8').read(), g9)
import unreal as u
v9 = json.loads(buf.getvalue().split('VERIFY239 ', 1)[1].strip().splitlines()[0])
from qa_graph import src, pn, info, obj
B = g9['B']; graph = g9['graph']
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
bad = list(v9['bad'])
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; bp = u.load_asset(AP)
cdo = u.get_default_object(bp.generated_class())
def dv(n):
    try: return cdo.get_editor_property(n)
    except Exception: return None
knobs = {k: dv(k) for k in ('SHM239_Own', 'SHM240_Det', 'SHM240_Retry', 'SHM240_ExtOn', 'SHM240_HeadOn', 'SHM240_YSpd', 'SHM240_BlkSpd', 'SHM240_AOFadeRate')}
EXP = {'SHM240_YSpd': 80.0, 'SHM240_BlkSpd': 60.0, 'SHM240_AOFadeRate': 4.0}
for k, v in EXP.items():
    if knobs[k] is None or abs(float(knobs[k]) - v) > 1e-6: bad.append('%s %s (expected %s)' % (k, knobs[k], v))
for k in ('SHM240_ExtOn', 'SHM240_HeadOn'):
    if knobs[k] is None: bad.append('%s missing' % k)
bdb = dv('SHM240_BlkDB'); knobs['SHM240_BlkDB'] = bdb.get_name() if bdb else None
if knobs['SHM240_Det'] is None or float(knobs['SHM240_Det']) != 1.0: bad.append('SHM240_Det %s' % knobs['SHM240_Det'])
if knobs['SHM240_Retry'] is None or abs(float(knobs['SHM240_Retry']) - 0.05) > 1e-6: bad.append('SHM240_Retry %s' % knobs['SHM240_Retry'])
V0 = '/Game/GraceRanger/SHME/Animations/V240/'; edb_bad = []
for i in range(96):
    d = u.load_asset(V0 + 'PSD_SHM240_E%02d' % i); dfl = dv('SHM240_E%02d' % i)
    if not d or d.get_num_animation_assets() < 1: edb_bad.append('E%02d empty' % i)
    elif dfl is None or dfl.get_name() != d.get_name(): edb_bad.append('E%02d default %s' % (i, dfl))
if edb_bad: bad.append('entry dbs %s' % edb_bad[:6])
AL = u.AnimationLibrary; d = u.load_asset('/Game/GraceRanger/SHME/Animations/V238/PSD_SHM238_JogCut'); nosrc = []
for i in range(d.get_num_animation_assets()):
    s = d.get_animation_asset(i)
    if 'shm240_src' not in set(str(c).lower() for c in AL.get_animation_curve_names(s, u.RawCurveTrackTypes.RCT_FLOAT)): nosrc.append(s.get_name())
if nosrc: bad.append('SHM240_Src missing %s' % nosrc[:6])
sg = pn(graph(bp, 'SHM_Snapshot')); sn = [pn(n) for n in B.find_nodes(obj(sg))]; orphan = []; wastk = None
for p in sn:
    ins = [q.name for q in info(p).input_pins]
    if 'execute' not in ins: continue
    if not src((p, 'execute')): orphan.append(tid(p)[-60:])
    if tid(p).endswith('SetSHM240_WasTk'): wastk = len(src((p, 'execute')))
if orphan: bad.append('snapshot orphan exec %s' % orphan[:6])
if wastk != 3: bad.append('SetSHM240_WasTk incoming exec %s (expected 3)' % wastk)
dirty = [p.get_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
out = {'v239_ALL_OK': v9['ALL_OK'], 'knobs': {k: (float(v) if isinstance(v, (int, float)) else str(v)) for k, v in knobs.items()},
       'entry_dbs_bad': len(edb_bad), 'src_missing': len(nosrc), 'snapshot_orphans': len(orphan), 'wastk_links': wastk, 'dirty': dirty,
       'bad': bad, 'ALL_OK': not bad}
print('VERIFY240 ' + json.dumps(out, default=str))
