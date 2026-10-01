"""GUARDIAN-3: dump ref-pose component-space positions of all bones of face meshes (P baseline vs new auto-rigged face) for the joint comparison.
builtins.GD3_JD = {'meshes': {label: path}, 'out': json path}"""
import unreal as u, json, builtins
C = builtins.GD3_JD; actors = u.get_editor_subsystem(u.EditorActorSubsystem); out = {}
for lab, p in C['meshes'].items():
    m = u.load_asset(p); a = actors.spawn_actor_from_class(u.SkeletalMeshActor, u.Vector(0, 0, -5000)); c = a.get_component_by_class(u.SkeletalMeshComponent); c.set_skeletal_mesh_asset(m)
    r = {}
    for i in range(c.get_num_bones()):
        n = str(c.get_bone_name(i)); t = c.get_socket_transform(n, u.RelativeTransformSpace.RTS_COMPONENT).translation; r[n] = [round(t.x, 4), round(t.y, 4), round(t.z, 4)]
    out[lab] = r; a.destroy_actor()
open(C['out'], 'w').write(json.dumps(out)); print('GD3_JD', {k: len(v) for k, v in out.items()})
