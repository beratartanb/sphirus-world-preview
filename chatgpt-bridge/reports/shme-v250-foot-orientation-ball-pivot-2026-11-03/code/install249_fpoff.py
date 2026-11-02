"""install249_fpoff.py (editor job, write manifest = ABP base + child): FootPlacement yields to the authored feet while the V2.49 servo owns
the turning start. Measured frame by frame (v249n60 / i60 / a60 j45_sl2, TurnL135_crop, production V2.48 too): the repaired clip keeps both
balls at -0.9 cm (clipdump) while its heel rises (ankle 8.6 -> 12.8); in game the ankle stays at the idle plant height (4.6 -> 6) and the ball
goes to -9 cm (foot ~76 deg pitched, toe in the floor, ball 'slides' 16 cm and its yaw flips) for the first 0.15 s = FootPlacement
PlantSettings_Default LockRotation holds the ankle of the idle plant against the clip's heel lift. With the capsule locked to the clip root
path (servo, error <= 0.6 cm) the authored contact is already exact on flat ground, so FootPlacement is bypassed there.
Patch (SHM_Snapshot): SetSHM_FootPlaceOff value := old OR (SHM249_FPOff > 0.5 AND SHM249_Owned AND |TerrainSlope| <= SHM249_FlatMax 6)
(SHM_FootPlaceOff is OR'ed into every bDisableFootPlacement read since V1 install_tip_feet). Knob SHM249_FPOff default 0 = production
unchanged. Idempotent (variable SHM249_FPOff). builtins.V249_SAVE saves. Prints FPOFF249 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj, arg
import builtins, json
LS = u.EditorLoadingAndSavingUtils
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CPA = AP.replace('Base', '')
COMP = '/Game/GraceRanger/SHME/BP_SHM_HumanMotionComponent.BP_SHM_HumanMotionComponent_C'
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
out = {}
dirty = [p for p in LS.get_dirty_content_packages() if 'ABP_GR_MotionMatching' in p.get_name()]
if dirty:
    out['reloaded'] = [p.get_name().split('/')[-1] for p in dirty]; LS.reload_packages(dirty, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
bp = u.load_asset(AP); V = [str(v) for v in B.list_variables(bp)]
assert 'SHM249_Owned' in V and 'SHM_FootPlaceOff' in V, 'prerequisites'
if 'SHM249_FPOff' in V: out['patch'] = 'already'
else:
    ensure_vars(bp, [('SHM249_FPOff', 'float', 'SHM'), ('SHM249_FlatMax', 'float', 'SHM')]); compile_ok(bp); set_defaults(bp, {'SHM249_FPOff': 0.0, 'SHM249_FlatMax': 6.0}); compile_ok(bp)
    sg = pn(graph(bp, 'SHM_Snapshot')); gs = G(sg); sn = [pn(n) for n in B.find_nodes(obj(sg))]
    comp = [p for p in sn if 'GetComponentByClass' in tid(p) or 'GetComponentbyClass' in tid(p)]; assert comp, 'component getter'; ct = (comp[0], 'ReturnValue')
    fpo = [p for p in sn if tid(p).endswith('|SetSHM_FootPlaceOff') or 'SetSHM_FootPlaceOff' in tid(p)]; assert len(fpo) == 1, fpo
    old = src((fpo[0], 'SHM_FootPlaceOff')); out['old_src'] = [o[0].rsplit('.', 1)[-1] + '.' + o[1] for o in old]
    flat = gs.get('SHM249_FlatMax'); slope = gs.get('TerrainSlope', COMP, ct)
    term = gs.AND(gs.AND(gs.within(gs.get('SHM249_FPOff'), 0.5, 1.0e9), gs.get('SHM249_Owned')), gs.within(slope, gs.mul(flat, -1.0), flat))
    if old:
        disconnect((fpo[0], 'SHM_FootPlaceOff')); connect(gs.OR(old[0], term), (fpo[0], 'SHM_FootPlaceOff'))
    else:
        connect(term, (fpo[0], 'SHM_FootPlaceOff'))
    out['wired'] = fpo[0].rsplit('.', 1)[-1]
st_, errs = compile_ok(bp); out['abp'] = [str(st_), errs[:6]]; cpb = u.load_asset(CPA); out['abp_child'] = str(compile_ok(cpb)[0])
cdo = u.get_default_object(bp.generated_class()); out['knob'] = str(cdo.get_editor_property('SHM249_FPOff'))
out['ok'] = 'UP_TO_DATE' in out['abp'][0] and not out['abp'][1] and 'UP_TO_DATE' in out['abp_child'] and out['knob'] == '0.0'
if out['ok'] and getattr(builtins, 'V249_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name().split('/')[-1] for q in LS.get_dirty_content_packages()]
print('FPOFF249 ' + json.dumps(out, default=str))
