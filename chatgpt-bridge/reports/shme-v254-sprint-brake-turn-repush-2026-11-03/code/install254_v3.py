"""install254_v3.py (editor job, write manifest = ABP base + child): V2.54 intent cancel also releases the V2.28 clip-speed contract.
Measured (v254e60 s54_tap rvc): SHM254_Cancel switched the yaw contract off (SHM238_On False, the body stayed facing forward) but
SHM228_On stayed True (the clip still owned the capsule speed) and the route kept the held database (SHM_HoldDB = PSD_SHM254_SprintRev):
the brake played on to 0 cm/s and re-pushed forward from rest. Production at the same frame: SHM228_On False -> PSD_SHM233_SprintCalm.
Patch: SHM_Snapshot SetSHM228_On := old value AND NOT SHM254_Cancel. Idempotent (variable SHM254_V3). builtins.V254_SAVE saves. Prints V3254 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj, arg
import builtins, json
LS = u.EditorLoadingAndSavingUtils
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CPA = AP.replace('Base', '')
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
out = {}
dirty = [p for p in LS.get_dirty_content_packages() if 'ABP_GR_MotionMatching' in p.get_name()]
if dirty:
    out['reloaded'] = [p.get_name().split('/')[-1] for p in dirty]; LS.reload_packages(dirty, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
bp = u.load_asset(AP); V = [str(v) for v in B.list_variables(bp)]
assert 'SHM254_Cancel' in V, 'install254_v2 first'
if 'SHM254_V3' in V: out['patch'] = 'already'
else:
    ensure_vars(bp, [('SHM254_V3', 'bool', 'SHM')]); compile_ok(bp)
    out['sets'] = []
    for gname in ('SHM_Snapshot',):
        sg = pn(graph(bp, gname)); gs = G(sg)
        so = [pn(n) for n in B.find_nodes(obj(sg)) if tid(pn(n)).endswith('|SetSHM228_On')]
        for s in so:
            s0 = src((s, 'SHM228_On')); assert len(s0) == 1, s0
            disconnect((s, 'SHM228_On')); connect(gs.AND(s0[0], gs.NOT(gs.get('SHM254_Cancel'))), (s, 'SHM228_On')); out['sets'].append(s.rsplit('.', 1)[-1])
    assert out['sets'], 'SetSHM228_On not found in SHM_Snapshot'
st_, errs = compile_ok(bp); out['abp'] = [str(st_), errs[:6]]; cpb = u.load_asset(CPA); out['abp_child'] = str(compile_ok(cpb)[0])
cdo = u.get_default_object(bp.generated_class()); out['knob'] = str(cdo.get_editor_property('SHM254_Turn'))
out['ok'] = 'UP_TO_DATE' in out['abp'][0] and not out['abp'][1] and 'UP_TO_DATE' in out['abp_child'] and out['knob'] == '0.0'
if out['ok'] and getattr(builtins, 'V254_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name().split('/')[-1] for q in LS.get_dirty_content_packages()]
print('V3254 ' + json.dumps(out, default=str))
