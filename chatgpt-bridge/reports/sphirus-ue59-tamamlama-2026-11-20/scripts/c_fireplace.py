# c_fireplace.py: hearth flame placement (editor world; in memory as control job, saved by w_fireplace.py).
# N_CampFire draws its flame ~40 cm below the actor origin: the five actors sat 25-30 cm in front of the logs with the flames on the
# hearth floor behind/under them. FIRE_POS = {label: (x,y,z,scale)}.
import unreal as u, builtins
POS=getattr(builtins,'FIRE_POS',None) or {'GR_Day_FireFX':(1462,905,226,1.0),'GR_Day_FireFX2':(1462,880,222,1.0),'GR_Day_FireFX3':(1460,893,224,1.0),'GR_Day_FireFX4':(1460,917,224,1.0),'GR_Day_FireFX5':(1462,930,222,1.0)}
LI=getattr(builtins,'FIRE_LI',None) or {}
for a in u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors():
    l=a.get_actor_label()
    if l in POS:
        p=POS[l]; a.modify(); a.root_component.modify(); a.set_actor_location(u.Vector(p[0],p[1],p[2]),False,False); a.set_actor_scale3d(u.Vector(p[3],p[3],p[3])); print('POS',l,p)
    if l in LI:
        for c in a.get_components_by_class(u.PointLightComponent):
            a.modify(); c.modify()
            for k,v in LI[l].items():
                if k=='loc': a.set_actor_location(u.Vector(*v),False,False)
                else: c.set_editor_property(k,v)
            print('LIGHT',l,LI[l])
