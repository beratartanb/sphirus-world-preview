"""install239_tkon.py (editor job) - V2.39: the takeover switch is a short LATCHED state, not a one-frame pulse (after install239_own).
Measured (v239d_j39_rl_tk / v239e_j39_rl_tkx, 30 FPS): SHM239_TkGo was true on the touchdown frame in the snapshot telemetry, but the
Update_MotionMatching owner branch did not switch the database on the first pulse in 2 of 3 runs (the second pulse switched); a one-frame
pulse can be missed by the motion-matching update. Now:
  SHM239_TkN  := TkOn ? TkN + 1 : 0
  SHM239_TkOn := (TkGo OR TkOn) AND the takeover clip is not yet in the pose (curve SHM239_Tgt < 500) AND OwnOn AND TkN <= 6
  Update_MotionMatching: the takeover branch reads SHM239_TkOn (re-searches the takeover database, ForceInterrupt, until its clip plays).
Also re-applies the SHM239_DB_Back / _Opp defaults and reports them after compile (the Opp database was never selected at runtime).
Idempotent. builtins.V239_SAVE saves. Prints TKON239 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj
import builtins, json
LS = u.EditorLoadingAndSavingUtils
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CPA = AP.replace('Base', '')
V9 = '/Game/GraceRanger/SHME/Animations/V239'
DAS = {'/Game/GraceRanger/Profiles/DA_GR_LocomotionBehavior', '/Game/GraceRanger/SHME/DA_SHM_Response_Default', '/Game/GraceRanger/Experimental/BodyInertia/DA_PBI_Prototype'}
dirty = list(LS.get_dirty_content_packages()); names = [p.get_name() for p in dirty]
assert all(n in DAS or n in (AP, CPA) for n in names), ('unexpected dirty', names)
if dirty: LS.reload_packages(dirty, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
out = {'reloaded': names}
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
bp = u.load_asset(AP)
ensure_vars(bp, [('SHM239_TkOn', 'bool', 'SHM239'), ('SHM239_TkN', 'float', 'SHM239')]); compile_ok(bp)
set_defaults(bp, {'SHM239_DB_Back': u.load_asset(V9 + '/PSD_SHM239_Tk_Back'), 'SHM239_DB_Opp': u.load_asset(V9 + '/PSD_SHM239_Tk_Opp'), 'SHM239_Own': 0.0}); compile_ok(bp)
sg = pn(graph(bp, 'SHM_Snapshot')); gs = G(sg); sn = [pn(n) for n in B.find_nodes(obj(sg))]
if any(tid(p).endswith('SetSHM239_TkOn') for p in sn): out['snapshot'] = 'already'
else:
    last = [p for p in sn if tid(p).endswith('SetSHM239_PrevStep')]; assert len(last) == 1
    nxt = [p for p in sn if any(q.name == 'execute' for q in info(p).input_pins) and (last[0], 'then') in src((p, 'execute'))]
    for x in nxt: disconnect((x, 'execute'))
    t = gs.set('SHM239_TkN', gs.select(gs.get('SHM239_TkOn'), gs.math(gs.get('SHM239_TkN'), 1.0, 1), 0.0), (last[0], 'then'))
    on = gs.AND(gs.AND(gs.OR(gs.get('SHM239_TkGo'), gs.get('SHM239_TkOn')), gs.NOT(gs.within(gs.get('SHM239_TgtC'), 500.0, 1.0e9))),
                gs.AND(gs.get('SHM239_OwnOn'), gs.within(gs.get('SHM239_TkN'), -1.0, 6.0)))
    t = gs.set('SHM239_TkOn', on, t)
    for x in nxt: connect(t, (x, 'execute'))
    out['snapshot'] = 'added'
gp = pn(graph(bp, 'Update_MotionMatching')); nodes = [pn(n) for n in B.find_nodes(obj(gp))]; g = G(gp)
br = [p for p in nodes if any(q.name == 'Condition' for q in info(p).input_pins) and any(tid(s[0]).endswith('GetSHM239_TkGo') for s in src((p, 'Condition')))]   # branch type ids are localized ('Dal')
if not br: out['umm'] = 'already' if any(tid(p).endswith('GetSHM239_TkOn') for p in nodes) else 'MISSING'
else:
    assert len(br) == 1; disconnect((br[0], 'Condition')); connect(g.get('SHM239_TkOn'), (br[0], 'Condition')); out['umm'] = 'TkGo -> TkOn'
st, errs = compile_ok(bp); out['abp'] = [str(st), errs[:6]]
cpb = u.load_asset(CPA); out['abp_child'] = str(compile_ok(cpb)[0])
def rd(b, k):
    v = u.get_default_object(b.generated_class()).get_editor_property(k); return v.get_name() if hasattr(v, 'get_name') else (None if v is None else float(v))
out['defaults'] = {n: {k: rd(b, k) for k in ('SHM239_DB_Back', 'SHM239_DB_Opp', 'SHM239_Own')} for n, b in (('base', bp), ('child', cpb))}
ok = 'UP_TO_DATE' in out['abp'][0] and not out['abp'][1] and 'UP_TO_DATE' in out['abp_child'] and out['umm'] != 'MISSING' \
     and all(d['SHM239_DB_Opp'] == 'PSD_SHM239_Tk_Opp' and d['SHM239_DB_Back'] == 'PSD_SHM239_Tk_Back' and d['SHM239_Own'] == 0.0 for d in out['defaults'].values())
out['ok'] = ok
if ok and getattr(builtins, 'V239_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name() for q in LS.get_dirty_content_packages()]
print('TKON239 ' + json.dumps(out, default=str))
