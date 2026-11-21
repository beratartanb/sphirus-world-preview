import unreal as u
a=u.load_asset('/Game/Sphirus/Player/GASP/ABP_Sph_GASP'); c=u.get_default_object(a.generated_class()); o=[]
for k in ('TrajectoryGenerationData_Idle','TrajectoryGenerationData_Moving','PlantSettings_Default','PlantSettings_Stops','InterpolationSettings_Default','InterpolationSettings_Stops','OffsetRootBoneEnabled','OffsetRootTranslationRadius','FootPlacementMode'):
    try:
        v=c.get_editor_property(k); o.append('%s = %s'%(k,v.export_text() if hasattr(v,'export_text') else v))
    except Exception as e: o.append('%s ERR %s'%(k,str(e)[:80]))
ks=[k.get_name() for k in c.get_editor_property('CM_Keys')]; vs=[v.get_name() for v in c.get_editor_property('CM_Vals')]
o.append('REMAP '+' | '.join('%s->%s'%(a_,b_) for a_,b_ in zip(ks,vs)))
g=u.load_asset('/Game/Sphirus/Player/GASP/BP_Sph_GASPCharacter'); cm=u.get_default_object(g.generated_class()).character_movement
o.append('CMC orient %s ctrlDesired %s rotRate %s'%(cm.orient_rotation_to_movement,cm.use_controller_desired_rotation,cm.rotation_rate))
open(u.Paths.project_dir()+'Saved/UE59Work/r5/traj.txt','w',encoding='utf8').write('\n'.join(o)); print('TRAJ',len(o))
