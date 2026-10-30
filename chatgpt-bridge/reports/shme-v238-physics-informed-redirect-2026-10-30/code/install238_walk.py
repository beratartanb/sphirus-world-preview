"""install238_walk.py (editor job) - V2.38: the jog-cut route stays a JOG route.
Measured (v238reg_w38_c90r o / cut3): the V2.10 switch SHM210_JogCutMode stops skipping lateral episodes for every non-sprint gait
(RedirectGait < 0.5 includes walk) -> a walk 90 became a redirect episode with a database hold (search throttle) -> 10.5 cm walk-loop slide
(production 0). Patch: after every SetSHM_RdLatSkip in SHM_Snapshot, while SHM238_Yaw > 0.5 an episode whose START speed (component
RedirectSpeed0, latched at the episode start - the cut clips themselves dip to ~115-180 cm/s mid-turn) is below SHM238_JogMinSpeed (220)
stays skipped, exactly as before the switch. Idempotent. builtins.V238_SAVE saves. Prints WALK238 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj
import builtins, json
LS = u.EditorLoadingAndSavingUtils
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CPA = AP.replace('Base', '')
COMP = '/Game/GraceRanger/SHME/BP_SHM_HumanMotionComponent.BP_SHM_HumanMotionComponent_C'
DAS = {'/Game/GraceRanger/Profiles/DA_GR_LocomotionBehavior', '/Game/GraceRanger/SHME/DA_SHM_Response_Default', '/Game/GraceRanger/Experimental/BodyInertia/DA_PBI_Prototype'}
dirty = list(LS.get_dirty_content_packages()); names = [p.get_name() for p in dirty]
assert all(n in DAS or n in (AP, CPA) for n in names), ('unexpected dirty', names)
if dirty: LS.reload_packages(dirty, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
out = {'reloaded': names}
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
bp = u.load_asset(AP); ensure_vars(bp, [('SHM238_JogMinSpeed', 'float', 'SHM238'), ('SHM238_WalkSkip', 'bool', 'SHM238')]); compile_ok(bp)
cdo = u.get_default_object(bp.generated_class())
if abs(float(cdo.get_editor_property('SHM238_JogMinSpeed'))) < 1e-6: set_defaults(bp, {'SHM238_JogMinSpeed': 220.0}); compile_ok(bp)
sg = pn(graph(bp, 'SHM_Snapshot')); gs = G(sg); sn = [pn(n) for n in B.find_nodes(obj(sg))]
if any('SetSHM238_WalkSkip' in tid(p) for p in sn): out['snapshot'] = 'already'
else:
    comp = [p for p in sn if 'GetComponentByClass' in tid(p) or 'GetComponentbyClass' in tid(p)]; assert comp; ct = (comp[0], 'ReturnValue')
    ls = [p for p in sn if tid(p).endswith('SetSHM_RdLatSkip')]; assert ls, 'SetSHM_RdLatSkip'
    out['snapshot'] = []
    for s_ in ls:
        nxt = [p for p in sn if any(q.name == 'execute' for q in info(p).input_pins) and (s_, 'then') in src((p, 'execute'))]
        for x in nxt: disconnect((x, 'execute'))
        w = gs.AND(gs.within(gs.get('SHM238_Yaw'), 0.5, 1.0e9), gs.within(gs.get('RedirectSpeed0', COMP, ct), -1.0, gs.get('SHM238_JogMinSpeed')))
        t = gs.set('SHM238_WalkSkip', w, (s_, 'then'))
        t = gs.set('SHM_RdLatSkip', gs.OR(gs.get('SHM_RdLatSkip'), gs.get('SHM238_WalkSkip')), t)
        for x in nxt: connect(t, (x, 'execute'))
        out['snapshot'].append({'after': s_.rsplit('.', 1)[-1], 'next': [x.rsplit('.', 1)[-1] for x in nxt]})
st, errs = compile_ok(bp); out['abp'] = [str(st), errs[:6]]
cpb = u.load_asset(CPA); out['abp_child'] = str(compile_ok(cpb)[0])
cdo = u.get_default_object(bp.generated_class()); out['knobs'] = {k: float(cdo.get_editor_property(k)) for k in ('SHM238_Yaw', 'SHM238_JogMinSpeed')}
ok = 'UP_TO_DATE' in out['abp'][0] and not out['abp'][1] and 'UP_TO_DATE' in out['abp_child'] and out['knobs']['SHM238_Yaw'] == 0.0
out['ok'] = ok
if ok and getattr(builtins, 'V238_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name() for q in LS.get_dirty_content_packages()]
print('WALK238 ' + json.dumps(out, default=str))
