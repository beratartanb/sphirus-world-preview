import unreal as u, collections
c=collections.Counter(); ex=[]
for a in u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors():
    if a.get_class().get_name()!='StaticMeshActor': continue
    lv=a.get_outer().get_outermost().get_name().split('/')[-1]
    m=a.static_mesh_component.get_editor_property('static_mesh')
    c[(lv,'ok' if m else 'NONE')]+=1
    if not m and len(ex)<6: ex.append(a.get_actor_label())
print('VH3',dict(c),ex)
m=u.load_asset('/Game/SphirusHouse/LivedIn_R05/Meshes/Revised/SM_HP_EastGableAligned'); print('VH3 asset load',m)
