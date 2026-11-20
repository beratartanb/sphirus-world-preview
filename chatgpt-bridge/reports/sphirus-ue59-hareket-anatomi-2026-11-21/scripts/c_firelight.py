# c_firelight.py (control job, house map loaded, in-memory): hearth light. 60 cd point light with source radius 0, 60 cm in front
# of the logs: blew the stone face out and left a hard specular speck on the stand to the right. Now a soft source (radius 10 /
# soft 28), 24 cd (builtins.FLV overrides), closer to the flames.
import unreal as u, builtins
V=getattr(builtins,'FLV',None) or {'I':24.0,'R':10.0,'S':28.0,'loc':(1422.0,905.0,198.0),'spec':0.5}
a=[x for x in u.EditorLevelLibrary.get_all_level_actors() if x.get_actor_label()=='GR_Day_FireLight'][0]; c=a.get_components_by_class(u.LightComponent)[0]
print('WAS',c.get_editor_property('intensity'),c.get_editor_property('source_radius'),a.get_actor_location())
c.set_editor_property('intensity',V['I']); c.set_editor_property('source_radius',V['R']); c.set_editor_property('soft_source_radius',V['S']); c.set_editor_property('specular_scale',V['spec'])
a.set_actor_location(u.Vector(*V['loc']),False,True); a.modify()
print('FIRELIGHT',c.get_editor_property('intensity'),c.get_editor_property('source_radius'),c.get_editor_property('soft_source_radius'),a.get_actor_location())
