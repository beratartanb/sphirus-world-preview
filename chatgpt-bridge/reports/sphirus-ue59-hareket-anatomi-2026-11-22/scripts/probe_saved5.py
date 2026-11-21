# probe_saved5.py (read-only): round-5 values as loaded from disk after a relaunch.
import unreal as u, re
o = []
p = u.get_default_object(u.load_asset('/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player').generated_class())
o.append('player ' + str({k: round(float(p.get_editor_property(k)), 3) for k in ('GR_SprintMinSp', 'CT_Look', 'CT_Dec', 'CT_VRef', 'CT_SBump', 'CT_SStag', 'CT_SDown', 'CT_GrazeLean', 'PS_K', 'PS_Keep', 'PS_AbdBase', 'PS_AbdRun', 'PS_HP0', 'PS_ShL', 'PS_LK')}) + ' CT_On %s' % p.get_editor_property('CT_On'))
g = u.load_asset('/Game/Sphirus/Player/GASP/BP_Sph_GASPCharacter'); sds = u.get_engine_subsystem(u.SubobjectDataSubsystem); m = None
for h in sds.k2_gather_subobject_data_for_blueprint(g):
    x = u.SubobjectDataBlueprintFunctionLibrary.get_object(u.SubobjectDataBlueprintFunctionLibrary.get_data(h))
    if x and 'SphMotion' in x.get_name(): m = x
o.append('motion ' + str({k: (round(float(m.get_editor_property(k)), 3) if not isinstance(m.get_editor_property(k), bool) else m.get_editor_property(k)) for k in ('TlOn', 'TlG45', 'TlG90', 'TlArm', 'StSoftT', 'StSoftK', 'StartCapOn', 'DmOn', 'DmMax', 'CtCap', 'CtBrake', 'RcOn')}))
a = u.load_asset('/Game/Sphirus/Player/GASP/ABP_Sph_GASP'); c = u.get_default_object(a.generated_class())
o.append('abp idle yaw rate %s' % c.get_editor_property('TrajectoryGenerationData_Idle').get_editor_property('max_controller_yaw_rate'))
o.append('abp remap stops ' + str([(k.get_name(), v.get_name()) for k, v in zip(c.get_editor_property('CM_Keys'), c.get_editor_property('CM_Vals')) if 'Stops' in k.get_name()]))
T = u.BlueprintToolset
for gr in T.list_graphs(a):
    for n in T.find_nodes(gr):
        cn = n.get_class().get_name()
        if cn == 'AnimGraphNode_FootPlacement': o.append('pelvis ' + re.search(r'LinearStiffness=([0-9.]+)', n.get_editor_property('node').export_text()).group(0))
        if cn == 'AnimGraphNode_Steering' and 'MotionMatching_0' in n.get_path_name():
            inf = T.get_node_infos([n])[0]; o.append('steer %s ' % n.get_name()[-10:] + str({str(q.get_editor_property('name')): str(q.get_editor_property('value')) for q in inf.get_editor_property('input_pins') if str(q.get_editor_property('name')) == 'ProceduralTargetTime'}))
for dbn in ('PSD_Sph_R_Walk_Stops', 'PSD_Sph_R_Run_Stops'):
    d = u.load_asset('/Game/Sphirus/Player/GASP/DB/' + dbn); o.append('%s %d clips' % (dbn, d.get_num_animation_assets()))
b = u.get_default_object(u.load_asset('/Game/GraceRanger/SF/MaskJob/BP_GR_MaskBench').generated_class())
o.append('mask ' + str({k: b.get_editor_property(k) for k in ('GR_InB', 'GR_InS', 'GR_InH', 'GR_InW', 'GR_GripF', 'GR_GripZ')}))
bd = u.get_default_object(u.load_asset('/Game/Sphirus/Player/GASP/ABP_Sph_Body_GASP').generated_class()); o.append('body ClavDeg %s FatBreath %s' % (bd.get_editor_property('ClavDeg'), bd.get_editor_property('FatBreath')))
print('SAVED5\n' + '\n'.join(o))
