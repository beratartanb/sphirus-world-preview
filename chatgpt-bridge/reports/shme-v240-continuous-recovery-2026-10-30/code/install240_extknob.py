"""install240_extknob.py (editor job) - V2.40: the external-effect yield can run WITHOUT the takeover (knob SHM240_ExtOn).
V2.39 measured (v239t/v239v j39_push_plan): with the V2.28 clip-speed contract a real shove during a planned cut is erased on the next tick
in PRODUCTION (no recovery at all); the residual |measured - commanded| (planned <= 9 cm/s, shove 282) lets the plan yield. It was gated
by SHM239_Own (the whole takeover). This patch makes the residual 'hit' read FMax(SHM239_Own, SHM240_ExtOn) - so the yield is a separate,
independently testable sub-fix (the yield setters themselves already AND NOT SHM239_Ext and are inert while Ext is false).
Idempotent (marker SHM240_ExtOn). builtins.V240_SAVE saves. Prints EXTK240 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj
import builtins, json
LS = u.EditorLoadingAndSavingUtils; M = '/Script/Engine.KismetMathLibrary:'
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
bp = u.load_asset(AP)
if 'SHM240_ExtOn' in [str(v) for v in B.list_variables(bp)]: out['patch'] = 'already'
else:
    ensure_vars(bp, [('SHM240_ExtOn', 'float', 'SHM240')]); compile_ok(bp)
    sg = pn(graph(bp, 'SHM_Snapshot')); gs = G(sg); sn = [pn(n) for n in B.find_nodes(obj(sg))]
    roots = [p for p in sn if tid(p).endswith('SetSHM239_Ext') or tid(p).endswith('SetSHM239_ExtT0')]; assert len(roots) == 2
    seen, stack, hits = set(), list(roots), []
    while stack:
        n_ = stack.pop()
        if n_ in seen: continue
        seen.add(n_)
        for q in info(n_).input_pins:
            if q.name in ('execute', 'then', 'self'): continue
            for s_ in src((n_, q.name)):
                if 'InRange' in tid(s_[0]) and any(tid(v[0]).endswith('GetSHM239_Own') for v in src((s_[0], 'Value'))): hits.append(s_[0])
                elif not tid(s_[0]).startswith('|Get'): stack.append(s_[0])
    hits = sorted(set(hits)); assert hits, 'no Own gate under Ext'
    for h in hits:
        disconnect((h, 'Value')); connect(gs.pure(M + 'FMax', {'A': gs.get('SHM239_Own'), 'B': gs.get('SHM240_ExtOn')}), (h, 'Value'))
    out['patch'] = {'own_gates_widened': len(hits)}
st, errs = compile_ok(bp); out['abp'] = [str(st), errs[:6]]; cpb = u.load_asset(CPA); out['abp_child'] = str(compile_ok(cpb)[0])
out['ok'] = 'UP_TO_DATE' in out['abp'][0] and not out['abp'][1] and 'UP_TO_DATE' in out['abp_child']
if out['ok'] and getattr(builtins, 'V240_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name() for q in LS.get_dirty_content_packages()]
print('EXTK240 ' + json.dumps(out, default=str))
