# probe_fol.py (measure): foliage components by mesh/instance count/material and the parameters of the dominant ground-cover instances.
import unreal as u
O=[]
ML=u.MaterialEditingLibrary
seen={}
for a in u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors():
    if a.get_class().get_name()!='InstancedFoliageActor': continue
    for c in a.get_components_by_class(u.InstancedStaticMeshComponent):
        m=c.get_editor_property('static_mesh'); mats=c.get_materials()
        O.append('FOL %-34s n %5d  cull %s  mats %s'%(m.get_name() if m else None,c.get_instance_count(),(c.get_editor_property('instance_start_cull_distance'),c.get_editor_property('instance_end_cull_distance')),[x.get_name() if x else None for x in mats][:3]))
        for x in mats:
            if x and isinstance(x,u.MaterialInstanceConstant): seen[x.get_path_name()]=x
for p,mi in sorted(seen.items()):
    n=mi.get_name()
    if not any(k in n for k in ('Grass','GroundCover','Ground_Cover','Fern','Meadow','Clover','Plant','Sweet')): continue
    O.append('MI %s parent %s'%(p.split('.')[0],mi.get_editor_property('parent').get_name() if mi.get_editor_property('parent') else None))
    try:
        O.append('   scalars %s'%{str(k):round(ML.get_material_instance_scalar_parameter_value(mi,k),3) for k in ML.get_scalar_parameter_names(mi)})
        O.append('   vectors %s'%{str(k):tuple(round(v,3) for v in ML.get_material_instance_vector_parameter_value(mi,k).to_tuple()) for k in ML.get_vector_parameter_names(mi)})
    except Exception as e: O.append('   ERR '+repr(e)[:150])
open(u.Paths.project_dir()+'Saved/UE59Work/r2g2/probe_fol.txt','w',encoding='utf8').write('\n'.join(O)); print('PF',len(O))
