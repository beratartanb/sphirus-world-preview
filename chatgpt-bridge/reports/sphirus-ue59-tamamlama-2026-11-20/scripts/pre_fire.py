# pre_fire.py (PIE prelude, runtime candidate): move/scale the hearth fire FX. builtins.FIRE_SET = {label: (x,y,z,scale)}; FIRE_LIGHT = {label: intensity}
import unreal as u, builtins
W_=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world()
for a in u.GameplayStatics.get_all_actors_of_class(W_,u.Actor):
    l=a.get_actor_label(); s=(getattr(builtins,'FIRE_SET',None) or {}).get(l)
    if s: a.set_actor_location(u.Vector(s[0],s[1],s[2]),False,False); a.set_actor_scale3d(u.Vector(s[3],s[3],s[3]))
    i=(getattr(builtins,'FIRE_LIGHT',None) or {}).get(l)
    if i is not None:
        for c in a.get_components_by_class(u.PointLightComponent): c.set_intensity(i)
print('PREFIRE')
