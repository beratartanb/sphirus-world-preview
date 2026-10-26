"""install_v231_slowroute_b.py (editor job) - fix of install_v231_slowroute.py (A1: the slow route never fired). The JR database is used on the
reversal's FIRST frame by the V2.24 EarlyRev branch of Update_MotionMatching, BEFORE the component episode starts; there RedirectSpeed0 still
holds the PREVIOUS episode's latched speed (s29_swl12: 424 cm/s from the sprint pivot), so the slow test failed and the hold latched the jog
database on that frame. Speed test := select(component RedirectActive, RedirectSpeed0, component Speed): the current speed until the episode
exists, its latched start speed afterwards (no database change inside an episode). Rewires the 'Value' pin of every InRange node fed by the
RedirectSpeed0 getter that install_v231_slowroute.py created. Idempotent (SHM231_SRFixB). builtins.V231_SAVE saves. Prints SLOWROUTE231B {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj
import builtins, json
LS = u.EditorLoadingAndSavingUtils
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CP = AP.replace('Base', '')
COMP = '/Game/GraceRanger/SHME/BP_SHM_HumanMotionComponent.BP_SHM_HumanMotionComponent_C'
DAS = {'/Game/GraceRanger/Profiles/DA_GR_LocomotionBehavior', '/Game/GraceRanger/SHME/DA_SHM_Response_Default', '/Game/GraceRanger/Experimental/BodyInertia/DA_PBI_Prototype'}
dirty = list(LS.get_dirty_content_packages()); names = [p.get_name() for p in dirty]
assert all(n in DAS or n in (AP, CP) for n in names), ('unexpected dirty', names)
rl = [p for p in dirty if p.get_name() in DAS or p.get_name() in (AP, CP)]
if rl: LS.reload_packages(rl, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
out = {'reloaded': [p.get_name() for p in rl]}
bp = u.load_asset(AP)
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
if 'SHM231_SRFixB' in [str(v) for v in B.list_variables(bp)]:
    out['eg'] = 'already'
else:
    assert 'SHM231_SRFix' in [str(v) for v in B.list_variables(bp)], 'slow route A not installed'
    eg = pn(graph(bp, 'EventGraph')); ge = G(eg); en = [pn(n) for n in B.find_nodes(obj(eg))]
    rs0 = [p for p in en if 'RedirectSpeed0' in tid(p) and 'Get' in tid(p).split('|')[-1] or tid(p).endswith('RedirectSpeed0')]
    users = []
    for p in en:
        if 'InRange' not in tid(p): continue
        s_ = src((p, 'Value'))
        if s_ and 'RedirectSpeed0' in tid(s_[0][0]): users.append((p, s_[0]))
    assert len(users) == 1, ('RedirectSpeed0 InRange users', [(tid(a)[-40:], tid(b[0])[-40:]) for a, b in users])
    rng, (g0, gpin) = users[0]
    comp_t = src((g0, 'self')); assert comp_t, 'component target of the RedirectSpeed0 getter'
    ct = comp_t[0]
    ra = ge.get('RedirectActive', COMP, ct); sp = ge.get('Speed', COMP, ct)
    sel = ge.select(ra, (g0, gpin), sp)
    disconnect((rng, 'Value')); connect(sel, (rng, 'Value'))
    ensure_vars(bp, [('SHM231_SRFixB', 'bool', 'SHM231')])
    out['eg'] = {'inrange': rng.rsplit('.', 1)[-1], 'getter': g0.rsplit('.', 1)[-1]}
st, errs = compile_ok(bp); out['status'] = str(st); out['errs'] = errs[:6]
cpb = u.load_asset(CP); out['child'] = str(compile_ok(cpb)[0])
cdo = u.get_default_object(bp.generated_class())
ok = 'UP_TO_DATE' in str(st) and not errs and 'UP_TO_DATE' in out['child'] and float(cdo.get_editor_property('SHM231_SlowOn')) == 0.0
out['ok'] = ok
if ok and getattr(builtins, 'V231_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name() for q in LS.get_dirty_content_packages()]
print('SLOWROUTE231B ' + json.dumps(out, default=str))
