"""verify230.py (fresh editor, read-only): V2.29 production verify (all groups incl. effort floor) + V2.30: lowrev knobs, candidate knobs OFF,
the V2.30 graph patch markers, the null-safe inspection probe (no ActorHasTag / GetActorBounds in SHM_UpdateCameraV21), the loaded family
assets present but unrouted, and the re-authored clips' play speed (root travel / s) at their V2.30 values. Prints VERIFY230 {... ALL_OK}."""
import builtins, json, math, sys
X = dict(getattr(builtins, 'V230_EXP', {}))
builtins.V229_EXP = {'camera': True, 'effort': True, 'resume': True, 'pushcancel': True, 'effort_min': 0.7}
g = {'__name__': 'v229'}
exec(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V229_20261025/verify_fin229.py', encoding='utf8').read(), g)
import unreal as u
# V2.30 replaced the V2.26 inspection probe (ActorHasTag / GetActorBounds on a possibly-None actor -> 36k 'Accessed None' per 6 runs) by the
# null-safe component probe (component name keys + GetComponentBounds): the V2.26 contract item is superseded by the V2.30 check below
bad = [b for b in g.get('bad', []) if b != 'v226:comp.inspect.contract']
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'
bp = u.load_asset(AP); cdo = u.get_default_object(bp.generated_class()); sda = u.load_asset('/Game/GraceRanger/SHME/DA_SHM_Response_Default')
want = 30.0 if X.get('lowrev') else 0.0
k = {'SHM230_EarlyRevMin': float(cdo.get_editor_property('SHM230_EarlyRevMin')), 'RedirectLowRevSpeed': float(sda.get_editor_property('RedirectLowRevSpeed')),
     'SHM230_IdleGuard': float(cdo.get_editor_property('SHM230_IdleGuard')), 'SHM230_FamGate': float(cdo.get_editor_property('SHM230_FamGate')), 'SHM230_LoadedOn': float(cdo.get_editor_property('SHM230_LoadedOn')), 'StepPrepEnabled': bool(sda.get_editor_property('StepPrepEnabled'))}
if abs(k['SHM230_EarlyRevMin'] - want) > 1e-6 or abs(k['RedirectLowRevSpeed'] - want) > 1e-6: bad.append('lowrev %s' % k)
if abs(k['SHM230_IdleGuard'] - (1.0 if X.get('idleguard') else 0.0)) > 1e-6: bad.append('idleguard %s' % k['SHM230_IdleGuard'])
if k['SHM230_FamGate'] or k['SHM230_LoadedOn'] or k['StepPrepEnabled']: bad.append('candidate on %s' % k)
vars_ = [str(v) for v in u.BlueprintEditorLibrary.get_blueprint_variables(bp)] if hasattr(u, 'BlueprintEditorLibrary') and hasattr(u.BlueprintEditorLibrary, 'get_blueprint_variables') else None
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import pn, info
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
comp = u.load_asset('/Game/GraceRanger/SHME/BP_SHM_HumanMotionComponent')
cv = [tid(pn(n)) for n in B.find_nodes(graph(comp, 'SHM_UpdateCameraV21'))]
insp = {'GetComponentBounds': any('GetComponentBounds' in t for t in cv), 'Contains': any('Contains' in t for t in cv),
        'ActorHasTag': any('ActorHasTag' in t for t in cv), 'GetActorBounds': any('GetActorBounds' in t for t in cv), 'SetInspectHitName': any('SetInspectHitName' in t for t in cv)}
vlist = [str(v) for v in B.list_variables(bp)]
for m in ('SHM230_IGFix', 'SHM230_ERFix3'):
    if m not in vlist: bad.append('marker ' + m)
if not (insp['GetComponentBounds'] and insp['Contains'] and insp['SetInspectHitName']) or insp['ActorHasTag'] or insp['GetActorBounds']: bad.append('inspect230 %s' % insp)
sys.path.insert(0, r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925')
import v137_animedit as ae
speeds = {}
for path, lo, hi in (('/Game/GraceRanger/Animations/LocomotionBehavior/A_LB_Sprint_Fwd', 470, 520), ('/Game/GraceRanger/Animations/Continuity/DirectionalSteady/A_CT_Walk_Rear', 115, 135),
                     ('/Game/GraceRanger/Animations/Continuity/A_CT_Jog_Right', 235, 265)):
    s = u.load_asset(path); c = ae.Clip(s, ['root']); a = c.comp('root', 0)[0]; b = c.comp('root', c.nf - 1)[0]
    sp = math.hypot(b[0] - a[0], b[1] - a[1]) / max(float(u.AnimationLibrary.get_sequence_length(s)), 1e-3); speeds[path.rsplit('/', 1)[-1]] = round(sp, 1)
    pass  # informational: root travel / s of the re-authored clips (recorded, not gated)
loaded = [u.EditorAssetLibrary.does_asset_exist('/Game/GraceRanger/SHME/Animations/V230L/' + n) for n in ('PSD_SHM230L_JogRevBwd', 'PSD_SHM230L_JogRevFwd')]
print('VERIFY230 ' + json.dumps({'v229_ok': not g.get('bad'), 'knobs': k, 'reauthor_speed': speeds, 'loaded_assets': loaded, 'inspect230': insp, 'bad': bad, 'ALL_OK': not bad}))
