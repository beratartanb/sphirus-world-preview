"""install239_side.py (editor job) - V2.39: takeover databases per plan SIDE (after install239_play2).
Measured (v239s_j39_rl_e_tk): with one Opp database for both sides, a RIGHT cut entered SHM239_Tk_L_P07_K4_Opp (a LEFT cut's takeover:
its 'opposite' is the other world side) -> 68 cm slide later. The SHM_Snapshot now loads the active takeover databases from the plan's own
turn sign every frame: SHM238_Delta > 0 (right plan) -> PSD_SHM239_TkR_* / TkPR_*, else TkL_* / TkPL_* into SHM239_DB_Back / _Opp /
SHM239_DBP_Back / _Opp (the variables Update_MotionMatching already reads). Idempotent (marker SHM239_DBR_Back). Prints SIDE239 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj
import builtins, json
LS = u.EditorLoadingAndSavingUtils
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CPA = AP.replace('Base', '')
V9 = '/Game/GraceRanger/SHME/Animations/V239/'
DAS = {'/Game/GraceRanger/Profiles/DA_GR_LocomotionBehavior', '/Game/GraceRanger/SHME/DA_SHM_Response_Default', '/Game/GraceRanger/Experimental/BodyInertia/DA_PBI_Prototype'}
dirty = list(LS.get_dirty_content_packages()); names = [p.get_name() for p in dirty]
assert all(n in DAS or n in (AP, CPA) for n in names), ('unexpected dirty', names)
if dirty: LS.reload_packages(dirty, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
out = {'reloaded': names}
bp = u.load_asset(AP); DBC = u.PoseSearchDatabase.static_class()
SV = {('R', 'DB', 'Back'): 'TkR_Back', ('R', 'DB', 'Opp'): 'TkR_Opp', ('R', 'DBP', 'Back'): 'TkPR_Back', ('R', 'DBP', 'Opp'): 'TkPR_Opp',
      ('L', 'DB', 'Back'): 'TkL_Back', ('L', 'DB', 'Opp'): 'TkL_Opp', ('L', 'DBP', 'Back'): 'TkPL_Back', ('L', 'DBP', 'Opp'): 'TkPL_Opp'}
if 'SHM239_DBR_Back' in [str(v) for v in B.list_variables(bp)]: out['patch'] = 'already'
else:
    vn = lambda sd, kind, tg: 'SHM239_%s%s_%s' % (kind, sd, tg)
    ensure_vars(bp, [(vn(sd, kind, tg), DBC, 'SHM239') for (sd, kind, tg) in SV]); compile_ok(bp)
    set_defaults(bp, {vn(sd, kind, tg): u.load_asset(V9 + 'PSD_SHM239_' + a) for (sd, kind, tg), a in SV.items()}); compile_ok(bp)
    sg = pn(graph(bp, 'SHM_Snapshot')); gs = G(sg); sn = [pn(n) for n in B.find_nodes(obj(sg))]
    first = [p for p in sn if tid(p).endswith('SetSHM239_W')]; assert len(first) == 1
    prev = src((first[0], 'execute')); assert len(prev) == 1; disconnect((first[0], 'execute'))
    bt, be = gs.branch(gs.within(gs.get('SHM238_Delta'), 0.0, 1.0e9), prev[0])
    for sd, ex in (('R', bt), ('L', be)):
        t = ex
        for kind in ('DB', 'DBP'):
            for tg in ('Back', 'Opp'): t = gs.set('SHM239_%s_%s' % (kind, tg), gs.get(vn(sd, kind, tg)), t)
        connect(t, (first[0], 'execute'))
    out['patch'] = 'per-side takeover databases'
st, errs = compile_ok(bp); out['abp'] = [str(st), errs[:6]]; cpb = u.load_asset(CPA); out['abp_child'] = str(compile_ok(cpb)[0])
out['ok'] = 'UP_TO_DATE' in out['abp'][0] and not out['abp'][1] and 'UP_TO_DATE' in out['abp_child']
if out['ok'] and getattr(builtins, 'V239_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name() for q in LS.get_dirty_content_packages()]
print('SIDE239 ' + json.dumps(out, default=str))
