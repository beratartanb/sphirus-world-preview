import unreal as u
w=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world(); o=['MAP '+w.get_outermost().get_name()]
for a in u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors():
    n=a.get_actor_label(); c=a.get_class().get_name()
    if c in ('StaticMeshActor','PlayerStart') or 'Start' in n:
        org,ext=a.get_actor_bounds(False); l=a.get_actor_location()
        o.append('%s [%s] loc (%.0f %.0f %.0f) ext (%.0f %.0f %.0f)'%(n,c,l.x,l.y,l.z,ext.x,ext.y,ext.z))
print('TESTMAP\n'+'\n'.join(o[:40]))
