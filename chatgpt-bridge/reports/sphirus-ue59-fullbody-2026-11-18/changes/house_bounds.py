# house_bounds.py (read-only, editor world): bounds of the house look volume and of the house shell meshes -> probe/house_bounds.txt
import unreal as u
W = u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world(); o = []
for v in u.GameplayStatics.get_all_actors_of_class(W, u.PostProcessVolume):
    org, ext = v.get_actor_bounds(False); o.append('PPV %s %s org %s ext %s rot %s scale %s' % (v.get_name(), v.get_actor_label(), [round(x) for x in (org.x, org.y, org.z)], [round(x) for x in (ext.x, ext.y, ext.z)], v.get_actor_rotation(), v.get_actor_scale3d()))
for a in u.GameplayStatics.get_all_actors_of_class(W, u.Actor):
    l = a.get_actor_label().lower()
    if any(k in l for k in ('house', 'wall', 'window', 'roof', 'floor', 'glass')):
        org, ext = a.get_actor_bounds(False); o.append('ACT %s [%s] org %s ext %s' % (a.get_actor_label(), a.get_class().get_name(), [round(x) for x in (org.x, org.y, org.z)], [round(x) for x in (ext.x, ext.y, ext.z)]))
open(u.Paths.project_dir() + 'Saved/UE59Work/probe/house_bounds.txt', 'w').write('\n'.join(o)); print('HB', len(o))
