"""install_v228_lookaxis.py (editor job) - V2.28 deliverable 2c: the inspection look-at tilted the head DOWN. Measured (gaze228.py on
v227fin_ins_ws, head forward derived from the neutral frame): while InspectOn > 0.5 the head yaw followed the target but the head pitch was
-2..-17 deg with the target 0..+18 deg above eye level (gaze error mean 11 deg, mostly pitch). Cause: the three LookAt skeletal controls
(spine_03 / neck_01 / head, alphas 0.18 / 0.35 / 0.55, clamps 25 / 30 / 35 deg) point the bones' default X axis at the target, and on this
skeleton X is the bone UP axis (forward is +Y for head, neck_01, spine_03, pelvis: cos 0.975-0.997 to the facing at the neutral frame) -> the
top of the head turns toward the target = a forward tilt of up to 35 x 0.55 = 19 deg. Fix: LookAtAxis = +Y with LookUpAxis = +X kept upright.
Node properties (no knob possible); A/B = before (production evidence) vs after in the same scenarios, revert = the pre_v228 checkpoint.
builtins.V228_SAVE saves ABP_GR_MotionMatchingBase (+ child). Prints LOOKAXIS228 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import pn, info, obj
import builtins, json
LS = u.EditorLoadingAndSavingUtils
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CP = AP.replace('Base', '')
DAS = {'/Game/GraceRanger/Profiles/DA_GR_LocomotionBehavior', '/Game/GraceRanger/SHME/DA_SHM_Response_Default', '/Game/GraceRanger/Experimental/BodyInertia/DA_PBI_Prototype'}
dirty = list(LS.get_dirty_content_packages()); names = [p.get_name() for p in dirty]
assert all(n in DAS or n in (AP, CP) for n in names), ('unexpected dirty', names)
rl = [p for p in dirty if p.get_name() in DAS or p.get_name() in (AP, CP)]
if rl: LS.reload_packages(rl, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
out = {'reloaded': [p.get_name() for p in rl], 'nodes': {}}
bp = u.load_asset(AP); gp = graph(bp, 'AnimGraph')
for n in B.find_nodes(obj(pn(gp))):
    if n.get_class().get_name() != 'AnimGraphNode_LookAt': continue
    node = n.get_editor_property('node'); bone = str(node.get_editor_property('bone_to_modify').get_editor_property('bone_name'))
    la = node.get_editor_property('look_at_axis'); lu = node.get_editor_property('look_up_axis')
    before = {'look_at_axis': str(la.get_editor_property('axis')), 'look_up_axis': str(lu.get_editor_property('axis')), 'use_look_up_axis': node.get_editor_property('use_look_up_axis'), 'clamp': node.get_editor_property('look_at_clamp')}
    E = type(la.get_editor_property('axis'))            # the EAxis enum class as exposed to Python (FAxis is unreal.Axis)
    out.setdefault('enum', str(E)); AY = getattr(E, 'Y', None) or getattr(E, 'Y_AXIS', None); AX = getattr(E, 'X', None) or getattr(E, 'X_AXIS', None)
    assert AY is not None and AX is not None, ('enum members', [x for x in dir(E) if not x.startswith('_')][:12])
    la.set_editor_property('axis', AY); la.set_editor_property('in_bone_space', True)
    lu.set_editor_property('axis', AX); lu.set_editor_property('in_bone_space', True)
    node.set_editor_property('look_at_axis', la); node.set_editor_property('look_up_axis', lu); node.set_editor_property('use_look_up_axis', True)
    n.set_editor_property('node', node)
    la2 = n.get_editor_property('node').get_editor_property('look_at_axis')
    out['nodes'][bone] = {'before': before, 'after': {'look_at_axis': str(la2.get_editor_property('axis')), 'use_look_up_axis': n.get_editor_property('node').get_editor_property('use_look_up_axis')}}
st, errs = compile_ok(bp); out['status'] = str(st); out['errs'] = errs[:6]
cpb = u.load_asset(CP); out['child'] = str(compile_ok(cpb)[0])
ok = 'UP_TO_DATE' in str(st) and not errs and 'UP_TO_DATE' in out['child'] and len(out['nodes']) == 3 and all(v['after']['look_at_axis'].endswith('Y') or 'Y' in v['after']['look_at_axis'] for v in out['nodes'].values())
out['ok'] = ok
if ok and getattr(builtins, 'V228_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name() for q in LS.get_dirty_content_packages()]
print('LOOKAXIS228 ' + json.dumps(out, default=str))
