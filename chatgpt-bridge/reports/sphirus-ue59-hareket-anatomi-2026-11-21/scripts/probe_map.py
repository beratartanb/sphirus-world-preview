import unreal as u
w=u.UnrealEditorSubsystem().get_editor_world(); o=[w.get_path_name()]
for a in u.EditorLevelLibrary.get_all_level_actors():
    try:
        org,ext=a.get_actor_bounds(False); 
        if ext.x>200: o.append('%s org (%.0f,%.0f,%.0f) ext (%.0f,%.0f,%.0f)'%(a.get_actor_label(),org.x,org.y,org.z,ext.x,ext.y,ext.z))
    except Exception: pass
print('MAP','\n'.join(o))
