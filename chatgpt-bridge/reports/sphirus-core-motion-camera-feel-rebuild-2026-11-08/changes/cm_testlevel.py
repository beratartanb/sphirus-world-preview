# cm_testlevel.py: empty locomotion test corridor /Game/Sphirus/Test/L_Sph_MoveTest from the default template (lit sky),
# 200 m flat floor, a
# player start at the origin facing +x, a doorway (two cubes, 90 cm gap) at x=1500 and a 1.2 m wall at x=3000 for the
# narrow-passage camera case. Uses the project game mode through the world settings default.
import unreal as u
E=u.EditorAssetLibrary; LES=u.get_editor_subsystem(u.LevelEditorSubsystem); AS=u.get_editor_subsystem(u.EditorActorSubsystem)
P='/Game/Sphirus/Test/L_Sph_MoveTest'
assert LES.new_level_from_template(P,'/Engine/Maps/Templates/Template_Default'); print('TEMPLATE level')
for a in list(AS.get_all_level_actors()):
    if a.get_actor_label().startswith('MT_') or a.get_class().get_name() in ('PlayerStart','StaticMeshActor'): AS.destroy_actor(a)
def sm(label,mesh,loc,scale,rot=(0,0,0),mat=None):
    a=AS.spawn_actor_from_object(u.load_asset(mesh),u.Vector(*loc),u.Rotator(*rot)); a.set_actor_label(label); a.set_actor_scale3d(u.Vector(*scale)); a.root_component.set_mobility(u.ComponentMobility.STATIC)
    if mat: a.get_component_by_class(u.StaticMeshComponent).set_material(0,u.load_asset(mat))
    return a
sm('MT_Floor','/Engine/BasicShapes/Plane',(0,0,0),(200,200,1),mat='/Engine/EngineMaterials/DefaultMaterial')
for i,y in enumerate((-300,300)): sm('MT_Door%d'%i,'/Engine/BasicShapes/Cube',(1500,y+(-255 if y<0 else 255)*0,0+150),(0.6,5.1 if False else 5.1,3.0))
# doorway: two blocks leaving a 90 cm gap centred on y=0
for a in list(AS.get_all_level_actors()):
    if a.get_actor_label().startswith('MT_Door'): AS.destroy_actor(a)
sm('MT_DoorL','/Engine/BasicShapes/Cube',(1500,-45-150,150),(0.6,3.0,3.0)); sm('MT_DoorR','/Engine/BasicShapes/Cube',(1500,45+150,150),(0.6,3.0,3.0))
sm('MT_Wall','/Engine/BasicShapes/Cube',(3000,-400,60),(0.6,6.0,1.2))
ps=AS.spawn_actor_from_class(u.PlayerStart,u.Vector(-200,0,100),u.Rotator(0,0,0)); ps.set_actor_label('MT_Start')
print('SAVE',LES.save_current_level()); print('ACTORS',len([a for a in AS.get_all_level_actors() if a.get_actor_label().startswith('MT_')]))
