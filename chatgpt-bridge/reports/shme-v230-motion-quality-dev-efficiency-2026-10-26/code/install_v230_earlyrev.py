"""install_v230_earlyrev.py (editor job) - V2.30 low-speed reversal entry. Measured (v230t1 e29_load / s29_swl12, lr candidate): a back-run at
40-135 cm/s + W opens a reversal episode (class 2, RevIntent 2) but the frame-0 route that puts the authored SHM226 B_F/F_B family
(SHM224_EarlyRev, SHM213_MontTick) requires planar speed > 150; one frame later the hold latches whatever database Motion Matching
already searched (the vendor PSD_Dense_Stand_Sprint_Pivots tail -> WalkToSprint). At 144 cm/s (e29_chain) the same path works.
Change: the 150 lower bound becomes Select(SHM230_EarlyRevMin > 0 AND component SpeedPeak > SHM230_EarlyRevPeak, SHM230_EarlyRevMin,
150) - only a body that was running recently (SpeedPeak above any walk speed) gets the low-speed entry. Knob SHM230_EarlyRevMin
default 0 = V2.29 behaviour, SHM230_EarlyRevPeak default 145. Idempotent (SHM230_ERFix). builtins.V230_SAVE saves. Prints EARLYREV230 {...}."""
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
if 'SHM230_ERFix' in [str(v) for v in B.list_variables(bp)]:
    out['mt'] = 'already'
else:
    ensure_vars(bp, [('SHM230_EarlyRevMin', 'float', 'SHM230'), ('SHM230_EarlyRevPeak', 'float', 'SHM230')]); compile_ok(bp)
    set_defaults(bp, {'SHM230_EarlyRevPeak': 145.0}); compile_ok(bp)
    mg = pn(graph(bp, 'SHM213_MontTick')); gm = G(mg); mn = [pn(n) for n in B.find_nodes(obj(mg))]
    es = [p for p in mn if 'SetSHM224_EarlyRev' in tid(p)]; assert len(es) == 1, es
    # walk the EarlyRev condition tree for a 'float>float' whose A is VectorLengthXY(GetPlanarVelocity) and B a literal 150
    seen = set(); hits = []
    def walk(p, d=0):
        if p in seen or d > 12: return
        seen.add(p)
        for q in info(p).input_pins:
            for s_ in src((p, q.name)):
                n_ = s_[0]
                if 'float>float' in tid(n_) or 'Greater' in tid(n_):
                    a_ = src((n_, 'A')); b_ = src((n_, 'B'))
                    if a_ and b_ and 'VectorLengthXY' in tid(a_[0][0]) and any('PlanarVelocity' in tid(z[0]) for z in src((a_[0][0], 'A'))) and 'MakeLiteralFloat' in tid(b_[0][0]):
                        hits.append((n_, b_[0]))
                walk(n_, d + 1)
    walk(es[0])
    assert len(hits) == 1, ('lower-bound node', [h[0].rsplit('.', 1)[-1] for h in hits])
    gt, lit = hits[0]
    for p_ in mn:
        if 'GetComponentByClass' in tid(p_) or 'GetComponentbyClass' in tid(p_): comp = p_; break
    ct = (comp, 'ReturnValue')
    low = gm.AND(gm.within(gm.get('SHM230_EarlyRevMin'), 0.5, 1.0e9), gm.within(gm.get('SpeedPeak', COMP, ct), gm.get('SHM230_EarlyRevPeak'), 1.0e9))
    disconnect((gt, 'B')); connect(gm.select(low, gm.get('SHM230_EarlyRevMin'), lit), (gt, 'B'))
    ensure_vars(bp, [('SHM230_ERFix', 'bool', 'SHM230')])
    out['mt'] = {'node': gt.rsplit('.', 1)[-1]}
st, errs = compile_ok(bp); out['status'] = str(st); out['errs'] = errs[:6]
cpb = u.load_asset(CP); out['child'] = str(compile_ok(cpb)[0])
cdo = u.get_default_object(bp.generated_class()); out['knobs'] = {k: float(cdo.get_editor_property(k)) for k in ('SHM230_EarlyRevMin', 'SHM230_EarlyRevPeak', 'SHM230_FamGate')}
ok = 'UP_TO_DATE' in str(st) and not errs and 'UP_TO_DATE' in out['child'] and out['knobs']['SHM230_EarlyRevMin'] == 0.0
out['ok'] = ok
if ok and getattr(builtins, 'V230_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name() for q in LS.get_dirty_content_packages()]
print('EARLYREV230 ' + json.dumps(out, default=str))
