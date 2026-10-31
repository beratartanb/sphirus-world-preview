import unreal as u, json
A = u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors()
S = u.EditorLoadingAndSavingUtils
r = {'vmp_actors': sum(1 for a in A if a.get_actor_label().startswith('VMP_')), 'n_actors': len(A),
     'dirty_content': sorted(p.get_name() for p in S.get_dirty_content_packages()), 'dirty_maps': sorted(p.get_name() for p in S.get_dirty_map_packages()),
     'pie': u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is not None}
print('FINAL_STATE', json.dumps(r))
