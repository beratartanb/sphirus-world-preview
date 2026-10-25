"""fix_v228_abp_w.py (editor job): the blend-weight witness threshold for the clip-bound speed (SHM226_W > 0.3) delayed the contract by
three frames after the clip entry (v228t1 ph3: ClipSpeedOn 0.10 s after the selection). Lower it to 0.1 (the V / W ratio is exact at any
weight; 0.1 only rejects the first blend-in frame). Patches the InRange node fed by GetCurveValue(SHM226_W) in SHM_Snapshot. builtins.V228_SAVE saves."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, src, pn, info, obj, value
import builtins, json
LS = u.EditorLoadingAndSavingUtils
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CP = AP.replace('Base', '')
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
out = {}
dirty = list(LS.get_dirty_content_packages()); names = [q.get_name() for q in dirty]
DAS = {'/Game/GraceRanger/Profiles/DA_GR_LocomotionBehavior', '/Game/GraceRanger/SHME/DA_SHM_Response_Default', '/Game/GraceRanger/Experimental/BodyInertia/DA_PBI_Prototype'}
rl = [q for q in dirty if q.get_name() in DAS or q.get_name() in (AP, CP)]
if rl: LS.reload_packages(rl, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
bp = u.load_asset(AP); sg = pn(graph(bp, 'SHM_Snapshot')); sn = [pn(n) for n in B.find_nodes(obj(sg))]
out['reloaded'] = [q.get_name() for q in rl]
def pin_default(p, name):
    for q in info(p).input_pins:
        if q.name == name:
            for a in ('default_value', 'default', 'value', 'default_text'):
                if hasattr(q, a): return str(getattr(q, a))
            return 'ATTRS:' + ','.join(x for x in dir(q) if not x.startswith('_'))[:200]
    return None
cands = []
for p in sn:
    if 'InRange' not in tid(p): continue
    vs = src((p, 'Value'))
    if vs and 'GetCurveValue' in tid(vs[0][0]) and not src((p, 'Min')):
        cands.append((p, pin_default(p, 'Min'), pin_default(vs[0][0], 'CurveName')))
out['inrange_curve_nodes'] = [(c[0].rsplit('.', 1)[-1], c[1], c[2]) for c in cands]
cands = [c[0] for c in cands if c[2] and 'SHM226_W' in str(c[2])] or [c[0] for c in cands if c[1] and str(c[1]).startswith('0.3')]
out['cands'] = [c.rsplit('.', 1)[-1] for c in cands]
print('ABPW228 scan ' + json.dumps(out, default=str)); assert len(cands) == 1, cands
value((cands[0], 'Min'), 0.1); out['min_set'] = 0.1
st, errs = compile_ok(bp); out['status'] = str(st); out['errs'] = errs[:4]; cpb = u.load_asset(CP); out['child'] = str(compile_ok(cpb)[0])
ok = 'UP_TO_DATE' in str(st) and not errs; out['ok'] = ok
if ok and getattr(builtins, 'V228_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name() for q in LS.get_dirty_content_packages()]
print('ABPW228 ' + json.dumps(out, default=str))
