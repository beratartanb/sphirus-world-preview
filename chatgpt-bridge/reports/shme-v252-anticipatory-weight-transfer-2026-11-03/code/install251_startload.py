"""install251_startload.py (editor job, write manifest = ABP base + child): V2.51 LOAD-AWARE START FOOT (knob SHM251_StartLoad, default 0 =
production unchanged).
Measured (v250c30 w42_id oi, weighted idle): the weighted idle stands on the LEFT leg (left ankle 4.9 cm, right heel lifted 7.6 cm), yet
the walk start stepped with the LEFT foot (SHM_StartTransfer_FR_Lfoot) and the unloaded right foot, now the 'support' of the clip,
skated 19.7 cm. Owner: the start side = component RecoverySide = SwingSide = 1 - SupportSide, and SupportSide comes from contact confidence
with a switch margin: in double support it keeps the side of the LAST STEP, not the weight. The component already computes the real weight
split SupportLoadL / SupportLoadR (COM projection between the foot centres). A person starting from a standstill steps with the foot that
is NOT carrying the weight.
Patch (SHM_Snapshot): the rawSide input of the V1.3.9 start latch (SetSHM_StartSideL value = Select(stNow AND StartPrev, StartSideL, rawSide))
becomes loadSide := (StartLoad > 0.5 AND component Speed < SHM249_RestSpeed AND DoubleSupport > 0.5) ?
   (LoadL > LoadR + SHM251_LoadMargin ? 1 (right swings) : (LoadR > LoadL + margin ? 0 (left swings) : rawSide)) : rawSide.
Only the start latch changes (recovery side, SupportSide and every other consumer untouched). Idempotent (variable SHM251_StartLoad).
builtins.V251_SAVE saves. Prints STARTLOAD251 {...}."""
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
if 'SHM251_StartLoad' in V: out['patch'] = 'already'
else:
    ensure_vars(bp, [('SHM251_StartLoad', 'float', 'SHM'), ('SHM251_LoadMargin', 'float', 'SHM')]); compile_ok(bp)
    set_defaults(bp, {'SHM251_StartLoad': 0.0, 'SHM251_LoadMargin': 0.1}); compile_ok(bp)
    sg = pn(graph(bp, 'SHM_Snapshot')); gs = G(sg); sn = [pn(n) for n in B.find_nodes(obj(sg))]
    comp = [p for p in sn if 'GetComponentByClass' in tid(p) or 'GetComponentbyClass' in tid(p)]; assert comp; ct = (comp[0], 'ReturnValue')
    ss = [p for p in sn if tid(p).endswith('|SetSHM_StartSideL')]; assert len(ss) == 1, ss
    sel = src((ss[0], 'SHM_StartSideL')); assert len(sel) == 1 and 'Select' in tid(sel[0][0]), (sel, tid(sel[0][0]) if sel else '')
    selp = sel[0][0]; raw = src((selp, 'B')); assert len(raw) == 1, raw
    out['raw_src'] = raw[0][0].rsplit('.', 1)[-1] + ' ' + tid(raw[0][0]).rsplit('|', 1)[-1]
    disconnect((selp, 'B'))
    lL = gs.get('SupportLoadL', COMP, ct); lR = gs.get('SupportLoadR', COMP, ct); m = gs.get('SHM251_LoadMargin')
    leftHeavy = gs.within(gs.math(lL, lR, -1), m, 1.0e9)
    rightHeavy = gs.within(gs.math(lR, lL, -1), m, 1.0e9)
    byLoad = gs.select(leftHeavy, 1.0, gs.select(rightHeavy, 0.0, raw[0]))
    gate = gs.AND(gs.AND(gs.within(gs.get('SHM251_StartLoad'), 0.5, 1.0e9), gs.within(gs.get('Speed', COMP, ct), -1.0, gs.get('SHM249_RestSpeed'))),
                  gs.within(gs.get('DoubleSupport', COMP, ct), 0.5, 1.0e9))
    connect(gs.select(gate, byLoad, raw[0]), (selp, 'B'))
    out['wired'] = {'set': ss[0].rsplit('.', 1)[-1], 'select': selp.rsplit('.', 1)[-1]}
st_, errs = compile_ok(bp); out['abp'] = [str(st_), errs[:6]]; cpb = u.load_asset(CPA); out['abp_child'] = str(compile_ok(cpb)[0])
cdo = u.get_default_object(bp.generated_class()); out['knobs'] = {k: str(cdo.get_editor_property(k)) for k in ('SHM251_StartLoad', 'SHM251_LoadMargin')}
out['ok'] = 'UP_TO_DATE' in out['abp'][0] and not out['abp'][1] and 'UP_TO_DATE' in out['abp_child'] and out['knobs']['SHM251_StartLoad'] == '0.0'
if out['ok'] and getattr(builtins, 'V251_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name().split('/')[-1] for q in LS.get_dirty_content_packages()]
print('STARTLOAD251 ' + json.dumps(out, default=str))
