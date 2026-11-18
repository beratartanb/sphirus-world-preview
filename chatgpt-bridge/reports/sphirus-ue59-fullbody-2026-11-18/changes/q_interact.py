import unreal as u
W = u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world(); o = []
A = u.GameplayStatics.get_all_actors_of_class(W, u.Actor)
for a in A:
    n = a.get_class().get_name()
    if any(k in n for k in ('Mask', 'Tea', 'Bed', 'Door', 'Kettle', 'Cup', 'Hearth', 'Fire', 'Interact', 'Sleep')) and 'Light' not in n:
        l = a.get_actor_location(); o.append('%s [%s] %d %d %d' % (a.get_actor_label(), n, l.x, l.y, l.z))
o.append('WORLD %s n %d' % (W.get_path_name(), len(A)))
open(u.Paths.project_dir() + 'Saved/UE59Work/probe/interact.txt', 'w').write('\n'.join(sorted(o))); print('INTERACT', len(o))
