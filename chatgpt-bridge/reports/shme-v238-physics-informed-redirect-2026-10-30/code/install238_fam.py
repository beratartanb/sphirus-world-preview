"""install238_fam.py (editor job) - V2.38: an authored, physically planned redirect is not a shove.
Measured (v238c1_j38_c90r_cut1S / j38_c90l_cut1): on the request frame GR's redirect friction drops the capsule 300 -> 217 cm/s before the
cut clip is bound; the V2.28 clip-speed contract then restores the designed speed (217 -> 281 in one frame). SHME's push detector
(SHM_UpdatePlanner pushRaw: speed increase > 1.5 x max acceleration) reads that restore as an external push -> PerturbState 1 ->
RecoveryDemand 0.81-0.97 -> component FamilyRoute 6 -> Update_MotionMatching routes the standstill shove recoveries (PSD_SHM_Recovery_R)
over the planned brake / plant (the false Stable -> Recovery switch).
Fix (ABP only, behind the V2.38 knob): in SHM_Snapshot, right after SHM_Family := component FamilyRoute, while an authored redirect clip is
in the pose (curve SHM238_W > 0.3) and SHM238_Yaw > 0.5, recovery families 1 and 6 are ignored (SHM_Family := 0) - the clip already IS
the planned brake / recovery; a real shove after the clip (or with the knob off) still routes. Idempotent. builtins.V238_SAVE saves."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj
import builtins, json
LS = u.EditorLoadingAndSavingUtils
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CPA = AP.replace('Base', '')
DAS = {'/Game/GraceRanger/Profiles/DA_GR_LocomotionBehavior', '/Game/GraceRanger/SHME/DA_SHM_Response_Default', '/Game/GraceRanger/Experimental/BodyInertia/DA_PBI_Prototype'}
dirty = list(LS.get_dirty_content_packages()); names = [p.get_name() for p in dirty]
assert all(n in DAS or n in (AP, CPA) for n in names), ('unexpected dirty', names)   # harness abp_flags dirty the ABP CDOs: reload from disk
if dirty: LS.reload_packages(dirty, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
out = {'reloaded': names}
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
bp = u.load_asset(AP); ensure_vars(bp, [('SHM238_FamOff', 'bool', 'SHM238')]); compile_ok(bp)
sg = pn(graph(bp, 'SHM_Snapshot')); gs = G(sg); sn = [pn(n) for n in B.find_nodes(obj(sg))]
if any('SetSHM238_FamOff' in tid(p) for p in sn): out['snapshot'] = 'already'
else:
    fs = [p for p in sn if tid(p).endswith('SetSHM_Family')]; assert fs, 'SetSHM_Family'
    out['snapshot'] = []
    for f_ in fs:                                       # every path that sets the family gets the same guard right after it
        nxt = [p for p in sn if any(q.name == 'execute' for q in info(p).input_pins) and (f_, 'then') in src((p, 'execute'))]
        for x in nxt: disconnect((x, 'execute'))
        vW = gs.pure('/Script/Engine.AnimInstance:GetCurveValue', {'CurveName': 'SHM238_W'})
        fam = gs.get('SHM_Family')
        rec = gs.OR(gs.within(fam, 0.5, 1.5), gs.within(fam, 5.5, 6.5))
        off = gs.AND(gs.AND(gs.within(gs.get('SHM238_Yaw'), 0.5, 1.0e9), gs.within(vW, 0.3, 1.0e9)), rec)
        tail = gs.set('SHM238_FamOff', off, (f_, 'then'))
        tail = gs.set('SHM_Family', gs.select(gs.get('SHM238_FamOff'), 0.0, gs.get('SHM_Family')), tail)
        for x in nxt: connect(tail, (x, 'execute'))
        out['snapshot'].append({'after': f_.rsplit('.', 1)[-1], 'next': [x.rsplit('.', 1)[-1] for x in nxt]})
st, errs = compile_ok(bp); out['abp'] = [str(st), errs[:6]]
cpb = u.load_asset(CPA); out['abp_child'] = str(compile_ok(cpb)[0])
cdo = u.get_default_object(bp.generated_class()); out['knob'] = float(cdo.get_editor_property('SHM238_Yaw'))
ok = 'UP_TO_DATE' in out['abp'][0] and not out['abp'][1] and 'UP_TO_DATE' in out['abp_child'] and out['knob'] == 0.0
out['ok'] = ok
if ok and getattr(builtins, 'V238_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name() for q in LS.get_dirty_content_packages()]
print('FAM238 ' + json.dumps(out, default=str))
