# c_doorsphere.py: lower store / WC doors - interaction sphere moved from the hinge line to the middle of each door's own opening
# (instance override of the Sphere component: world y = hinge y - 42, radius 46). In memory as control job; saved by w_doorsphere.py.
import unreal as u, builtins
DY=float(getattr(builtins,'DOOR_DY',-42.0)); RAD=float(getattr(builtins,'DOOR_RAD',46.0)); pk=set()
for a in u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors():
    if a.get_actor_label() in ('SPH_Door_LowerStoreDoor','SPH_Door_LowerWCDoor'):
        s=[c for c in a.get_components_by_class(u.SphereComponent) if c.get_name()=='Sphere'][0]
        a.modify(); s.modify(); w0=s.get_world_location(); al=a.get_actor_location()
        s.set_world_location(u.Vector(al.x+float(getattr(builtins,'DOOR_DX',13.0)), al.y+DY, w0.z), False, False); s.set_sphere_radius(RAD, True)
        w1=s.get_world_location(); pk.add(a.get_outermost().get_name())
        print('DOOR',a.get_actor_label(),'sphere (%.0f,%.0f,%.0f) -> (%.0f,%.0f,%.0f) r %.0f rel %s'%(w0.x,w0.y,w0.z,w1.x,w1.y,w1.z,s.get_unscaled_sphere_radius(),[round(v,1) for v in s.get_editor_property('relative_location').to_tuple()]))
print('PKG',sorted(pk))
