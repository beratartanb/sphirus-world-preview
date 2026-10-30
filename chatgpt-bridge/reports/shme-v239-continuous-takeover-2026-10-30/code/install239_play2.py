"""install239_play2.py (editor job) - V2.39: the play database follows the LATCHED target (after install239_play).
Measured (v239q_j39_rw_tk): the Back takeover entered correctly (P10_K1_Back), but the play-database choice read the clip curve
SHM239_Tgt, which BLENDS during the entry (0 -> 1000 passes 564 < 950 = 'Opp') -> PSD_SHM239_TkP_Opp -> P21_K1_Opp -> yaw 39 -> -80 deg
(773 deg/s). Patch: the Update_MotionMatching play branch reads SHM239_TkTgt (latched at the request: -90 Opp / 0 Back) instead.
Idempotent. builtins.V239_SAVE saves. Prints PLAY2_239 {...}."""
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
bp = u.load_asset(AP); gp = pn(graph(bp, 'Update_MotionMatching')); g = G(gp); nodes = [pn(n) for n in B.find_nodes(obj(gp))]
br = [p for p in nodes if any(q.name == 'Condition' for q in info(p).input_pins) and any('InRange' in tid(s[0]) and any(tid(v[0]).endswith('GetSHM239_TgtC') for v in src((s[0], 'Value'))) for s in src((p, 'Condition')))]
if not br: out['patch'] = 'already' if any(tid(p).endswith('GetSHM239_TkTgt') for p in nodes) else 'MISSING'
else:
    assert len(br) == 1, br; disconnect((br[0], 'Condition')); connect(g.within(g.get('SHM239_TkTgt'), -1.0e9, -45.0), (br[0], 'Condition')); out['patch'] = 'play DB by TkTgt'
st, errs = compile_ok(bp); out['abp'] = [str(st), errs[:6]]; cpb = u.load_asset(CPA); out['abp_child'] = str(compile_ok(cpb)[0])
out['ok'] = 'UP_TO_DATE' in out['abp'][0] and not out['abp'][1] and 'UP_TO_DATE' in out['abp_child'] and out['patch'] != 'MISSING'
if out['ok'] and getattr(builtins, 'V239_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name() for q in LS.get_dirty_content_packages()]
print('PLAY2_239 ' + json.dumps(out, default=str))
