import unreal as u, json
out = {}
for a in u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors():
    l = a.get_actor_label()
    if l.startswith('VMP_') and ('ferngrp1' in l or 'toe_stone_b' in l or 'bank_rock1' in l):
        c = a.get_component_by_class(u.StaticMeshComponent)
        out[l] = {'enabled': str(c.get_collision_enabled()), 'profile': str(c.get_collision_profile_name()),
                  'cam': str(c.get_collision_response_to_channel(u.CollisionChannel.ECC_CAMERA)),
                  'vis': str(c.get_collision_response_to_channel(u.CollisionChannel.ECC_VISIBILITY)),
                  'body_setup': str(c.get_editor_property('static_mesh').get_editor_property('body_setup').get_editor_property('collision_trace_flag')) if c.get_editor_property('static_mesh').get_editor_property('body_setup') else None}
json.dump(out, open(r'C:/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/5f49a232-b001-47ad-8881-1eb04d9cb1c5/scratchpad/vmp/vmpcol.json', 'w'), indent=1)
print('VMPCOL', json.dumps(out)[:1500])
