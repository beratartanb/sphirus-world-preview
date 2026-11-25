# scene_place.py (control, in memory, test map only, never saved): removes MR3_*/B4_* test actors, places boxes from b4/scene.json
# [[x, y, zc, size_x, size_y, size_z, yaw, pitch], ...] world cm (engine cube = 100 cm)
import unreal as u, json
S=json.loads(open(u.Paths.project_dir()+'Saved/UE59Work/b4/scene.json').read())
es=u.get_editor_subsystem(u.EditorActorSubsystem); w=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world(); assert 'L_Sph_MoveTest' in w.get_path_name(), w.get_path_name()
n=0
for a in es.get_all_level_actors():
    if a.get_actor_label().startswith(('MR3_','B4_')): es.destroy_actor(a); n+=1
for i,b in enumerate(S):
    a=es.spawn_actor_from_class(u.StaticMeshActor,u.Vector(b[0],b[1],b[2]),u.Rotator(roll=0.0,pitch=float(b[7]) if len(b)>7 else 0.0,yaw=float(b[6]) if len(b)>6 else 0.0)); a.set_actor_label('B4_BOX%d'%i)
    a.static_mesh_component.set_static_mesh(u.load_asset('/Engine/BasicShapes/Cube')); a.set_actor_scale3d(u.Vector(b[3]/100.0,b[4]/100.0,b[5]/100.0))
print('SCENE removed',n,'placed',len(S))
