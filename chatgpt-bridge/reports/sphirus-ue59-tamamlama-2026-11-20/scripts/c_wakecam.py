# c_wakecam.py: bedroom wake camera on the hub instance (editor world). The stored GR_CamLoc/Aim (985,680,625)->(1120,785,580) looked
# past the bed at the wrong height; the character lies along +y at x 1230, chest z ~645 (Bed_real2 rec). New: east side, above.
import unreal as u, builtins
L=getattr(builtins,'WCAM',((1390.0,835.0,760.0),(1228.0,742.0,648.0),52.0))
for a in u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors():
    if a.get_actor_label()=='GR_DayHub':
        a.modify(); a.set_editor_property('GR_CamLoc',u.Vector(*L[0])); a.set_editor_property('GR_CamAim',u.Vector(*L[1])); a.set_editor_property('GR_CamFov',L[2])
        print('WCAM',a.get_editor_property('GR_CamLoc'),a.get_editor_property('GR_CamAim'))
