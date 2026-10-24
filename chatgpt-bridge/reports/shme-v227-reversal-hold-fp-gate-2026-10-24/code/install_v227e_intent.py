"""install_v227e_intent.py (editor job) - V2.27 candidate, fifth pass. Two defects measured in pass d (t4/u60):
 (1) 60 FPS ph0: the Motion Matching node re-selected the opposite-phase clip ONE frame after entry (P14 ct 0.10 -> P30 ct 0.03) although the
     search throttle (pass d) was installed: SHM227_Thr read LAST frame's SHM_RedirectActive, so the throttle started two frames after entry.
     The component's episode (RedirectActive) is already on at the entry frame -> Thr = RevHold & Rev>0 & (last ABP episode OR component
     episode on) & not Dead: active from the first frame after entry; the entry frame itself still searches (bridge database change).
 (2) j24_dbl (second request during the reversal): the component ended its episode with RedirectEnd 3 (new intent) and the capsule
     accelerated FORWARD while the held F_B clip ran backward to its end (1.1 s, planted-foot slip 100 cm). A hold is only valid while the
     intent that started the reversal persists: RedirectEnd 3 (new intent) or 4 (lost) -> SHM227_IntentEnd -> SHM227_Dead latched until the
     component restarts (hold off, throttle off, episode ends, MM searches the loop). RedirectEnd 1 (aligned) / 2 (max dwell) keep the hold.
Graph-level patch of SHM_Snapshot (no DSL rebuild): SetSHM227_IntentEnd inserted before SetSHM227_Dead; Dead = OR(old, IntentEnd);
Thr inner AND .A = OR(get SHM_RedirectActive, rdOn). Knobs unchanged (0 = production). Idempotent (SetSHM227_IntentEnd present).
builtins.V227_SAVE saves. Prints RH227E {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj, arg
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
ensure_vars(bp, [('SHM227_IntentEnd', 'bool', 'SHM227')]); compile_ok(bp)
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
sg = pn(graph(bp, 'SHM_Snapshot')); gs = G(sg); sn = [pn(n) for n in B.find_nodes(obj(sg))]
if any('SetSHM227_IntentEnd' in tid(p) for p in sn): out['snapshot'] = 'already'
else:
    dd = [p for p in sn if 'SetSHM227_Dead' in tid(p)]; assert len(dd) == 1, dd
    th = [p for p in sn if 'SetSHM227_Thr' in tid(p) and 'ThrottleT' not in tid(p)]; assert len(th) == 1, th
    comp = [p for p in sn if 'GetComponentByClass' in tid(p) or 'GetComponentbyClass' in tid(p)]; assert comp, 'component getter'
    hse = [p for p in sn if tid(p).endswith('|GetHumanStateEnabled')]; assert hse, 'HumanStateEnabled getter'
    ct = (comp[0], 'ReturnValue')
    # ---- (2) IntentEnd before Dead; Dead = OR(old, get IntentEnd)
    prev_exec = src((dd[0], 'execute')); assert len(prev_exec) == 1, prev_exec
    disconnect((dd[0], 'execute'))
    iend = gs.within(gs.get('RedirectEnd', COMP, ct), 2.5, 4.5)            # 3 = new intent, 4 = lost (1 aligned / 2 max dwell keep the hold)
    t1 = gs.set('SHM227_IntentEnd', iend, prev_exec[0]); connect(t1, (dd[0], 'execute'))
    do = src((dd[0], 'SHM227_Dead')); assert len(do) == 1 and 'ORBoolean' in tid(do[0][0]), do
    disconnect((dd[0], 'SHM227_Dead')); connect(gs.OR(do[0], gs.get('SHM227_IntentEnd')), (dd[0], 'SHM227_Dead'))
    # ---- (1) Thr inner AND: .A (get SHM_RedirectActive) -> OR(get SHM_RedirectActive, rdOn)
    to = src((th[0], 'SHM227_Thr')); assert len(to) == 1 and 'ANDBoolean' in tid(to[0][0]), to
    inner = None
    for k in ('A', 'B'):
        s = src((to[0][0], k))
        if len(s) == 1 and 'ANDBoolean' in tid(s[0][0]):
            for kk in ('A', 'B'):
                ss = src((s[0][0], kk))
                if len(ss) == 1 and 'SHM_RedirectActive' in tid(ss[0][0]) and 'Set' not in tid(ss[0][0]): inner = (s[0][0], kk, ss[0])
    assert inner, 'Thr inner AND / RedirectActive getter not found'
    out['thr_pin'] = inner[1]
    rdOn = gs.AND((hse[0], 'HumanStateEnabled'), gs.get('RedirectActive', COMP, ct))
    disconnect((inner[0], inner[1])); connect(gs.OR(inner[2], rdOn), (inner[0], inner[1]))
    out['snapshot'] = 'wired'
st, errs = compile_ok(bp); out['status'] = str(st); out['errs'] = errs[:6]
cpb = u.load_asset(CP); out['child'] = str(compile_ok(cpb)[0])
cdo = u.get_default_object(bp.generated_class()); out['knobs'] = {k: float(cdo.get_editor_property(k)) for k in ('SHM227_RevHold', 'SHM227_FPOff', 'SHM227_HoldExit', 'SHM227_FlatMax', 'SHM227_ThrottleT')}
ok = 'UP_TO_DATE' in str(st) and not errs and 'UP_TO_DATE' in out['child'] and out['knobs']['SHM227_RevHold'] == 0.0 and out['knobs']['SHM227_FPOff'] == 0.0
out['ok'] = ok
if ok and getattr(builtins, 'V227_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name() for q in LS.get_dirty_content_packages()]
print('RH227E ' + json.dumps(out, default=str))
