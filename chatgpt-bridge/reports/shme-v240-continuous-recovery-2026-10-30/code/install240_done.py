"""install240_done.py (editor job) - V2.40: the confirmed-entry test also recognises the per-source entry databases (after install240_edb).
Measured (v240b30 j39_rl_l / j39_rl): with the deterministic entry the selected database is PSD_SHM240_E<idx>, but SHM240_TkDone looked
for 'PSD_SHM239_Tk' in its name -> the entry was never confirmed, the 50 ms retry re-forced the search and the selection hopped
(P21_K3 -> P17_K1 -> P17_K2, 51 cm, 806 deg/s). Patch: the Contains() under SetSHM240_TkDone tests 'PSD_SHM240_E' OR 'PSD_SHM239_Tk'.
Idempotent. builtins.V240_SAVE saves. Prints DONE240 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj
import builtins, json
LS = u.EditorLoadingAndSavingUtils
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CPA = AP.replace('Base', '')
DAS = {'/Game/GraceRanger/Profiles/DA_GR_LocomotionBehavior', '/Game/GraceRanger/SHME/DA_SHM_Response_Default', '/Game/GraceRanger/Experimental/BodyInertia/DA_PBI_Prototype'}
dirty = list(LS.get_dirty_content_packages()); names = [p.get_name() for p in dirty]
assert all(n in DAS or n in (AP, CPA) for n in names), ('unexpected dirty', names)
if dirty: LS.reload_packages(dirty, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
out = {'reloaded': names}
bp = u.load_asset(AP); sg = pn(graph(bp, 'SHM_Snapshot')); gs = G(sg); sn = [pn(n) for n in B.find_nodes(obj(sg))]
cont = [p for p in sn if 'Contains' in tid(p) and any(q.name == 'Substring' and 'PSD_SHM239_Tk' in str(q.value) for q in info(p).input_pins)]
if not cont: out['patch'] = 'already' if any('Contains' in tid(p) and any(q.name == 'Substring' and 'PSD_SHM240_E' in str(q.value) for q in info(p).input_pins) for p in sn) else 'MISSING'
else:
    assert len(cont) == 1; c0 = cont[0]
    outs = [(p, q.name) for p in sn for q in info(p).input_pins if (c0, 'ReturnValue') in src((p, q.name))]; assert len(outs) == 1, outs
    nm = src((c0, 'SearchIn')); assert len(nm) == 1
    c1 = gs.pure('/Script/Engine.KismetStringLibrary:Contains', {'SearchIn': nm[0], 'Substring': 'PSD_SHM240_E', 'bUseCase': False, 'bSearchFromEnd': False})
    disconnect(outs[0]); connect(gs.OR((c0, 'ReturnValue'), c1), outs[0]); out['patch'] = 'TkDone recognises PSD_SHM240_E'
st, errs = compile_ok(bp); out['abp'] = [str(st), errs[:6]]; cpb = u.load_asset(CPA); out['abp_child'] = str(compile_ok(cpb)[0])
out['ok'] = 'UP_TO_DATE' in out['abp'][0] and not out['abp'][1] and 'UP_TO_DATE' in out['abp_child'] and out['patch'] != 'MISSING'
if out['ok'] and getattr(builtins, 'V240_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name() for q in LS.get_dirty_content_packages()]
print('DONE240 ' + json.dumps(out, default=str))
