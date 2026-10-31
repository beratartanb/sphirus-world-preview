"""recon.py (measure job, read-only): exterior snapshot for the Exterior World Redesign masterplan AND the restore source.
Writes <D>/recon/:
  landscape.json   actor transform, component layout, edit layers, material
  height_before.u16 1017x1017 little-endian heightmap (same export route as FrontRefugeE2 height_export.py, delayed read)
  foliage.json     every IFA component: mesh path, cull, collision, instance transforms [x,y,z,pitch,yaw,roll,sx,sy,sz]
  actors.json      every level actor: class, label, level, bounds origin/extent, mesh (static mesh actors)
Nothing is modified."""
import unreal as u, pathlib, json, time, array, builtins

D = pathlib.Path(u.Paths.project_dir()) / 'Saved/Codex/ExteriorRedesign_20261031' / getattr(builtins, 'XR_RECON_DIR', 'recon'); D.mkdir(parents=True, exist_ok=True)
assert getattr(builtins, 'XR_RECON_DIR', 'recon') != 'recon' or not (D / 'foliage.json').exists(), 'recon snapshot exists - never overwrite the restore source'
ed = u.get_editor_subsystem(u.UnrealEditorSubsystem); assert ed.get_game_world() is None, 'PIE running'
w = ed.get_editor_world()
actors = u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors()
land = next(a for a in actors if isinstance(a, u.Landscape))
T = land.get_actor_transform()
L = {'label': land.get_actor_label(), 'loc': [T.translation.x, T.translation.y, T.translation.z], 'scale': [T.scale3d.x, T.scale3d.y, T.scale3d.z],
     'rot': [land.get_actor_rotation().pitch, land.get_actor_rotation().yaw, land.get_actor_rotation().roll]}
for k in ('component_size_quads', 'subsection_size_quads', 'num_subsections', 'landscape_material'):
    try:
        L[k] = str(land.get_editor_property(k))
    except Exception as e:
        L[k] = 'n/a %s' % e
comps = land.get_components_by_class(u.LandscapeComponent); L['n_components'] = len(comps)
o, e = land.get_actor_bounds(False); L['bounds'] = [[o.x, o.y, o.z], [e.x, e.y, e.z]]
try:
    L['edit_layers'] = [str(l.get_editor_property('name')) for l in land.get_editor_property('landscape_layers')]
except Exception as ex:
    L['edit_layers'] = 'n/a %s' % ex
(D / 'landscape.json').write_text(json.dumps(L, indent=1, default=str))

ifa = [a for a in actors if isinstance(a, u.InstancedFoliageActor)]
F = []
for a in ifa:
    for c in a.get_components_by_class(u.InstancedStaticMeshComponent):
        n = c.get_instance_count()
        if not n or not c.static_mesh:
            continue
        b = c.static_mesh.get_bounds()
        rec = {'ifa': a.get_actor_label(), 'comp': c.get_name(), 'mesh': c.static_mesh.get_path_name().split('.')[0],
               'cull': [c.get_editor_property('instance_start_cull_distance'), c.get_editor_property('instance_end_cull_distance')],
               'collision': str(c.get_collision_enabled()).split('.')[-1].split(':')[0],
               'mesh_bounds': [[b.origin.x, b.origin.y, b.origin.z], [b.box_extent.x, b.box_extent.y, b.box_extent.z]], 'xf': []}
        for i in range(n):
            t = c.get_instance_transform(i, True); r = t.rotation.rotator()
            rec['xf'].append([round(t.translation.x, 1), round(t.translation.y, 1), round(t.translation.z, 1), round(r.pitch, 2), round(r.yaw, 2), round(r.roll, 2),
                              round(t.scale3d.x, 3), round(t.scale3d.y, 3), round(t.scale3d.z, 3)])
        F.append(rec)
(D / 'foliage.json').write_text(json.dumps(F))
A = []
for a in actors:
    try:
        o, e = a.get_actor_bounds(False)
    except Exception:
        continue
    r = {'label': a.get_actor_label(), 'class': a.get_class().get_name(), 'level': a.get_level().get_outer().get_name(),
         'loc': [round(a.get_actor_location().x), round(a.get_actor_location().y), round(a.get_actor_location().z)],
         'b': [[round(o.x), round(o.y), round(o.z)], [round(e.x), round(e.y), round(e.z)]], 'hidden': a.is_hidden_ed()}
    if isinstance(a, u.StaticMeshActor):
        m = a.static_mesh_component.static_mesh
        r['mesh'] = m.get_path_name().split('.')[0] if m else None
    A.append(r)
(D / 'actors.json').write_text(json.dumps(A))

builtins.XR_RT = u.RenderingLibrary.create_render_target2d(w, 1017, 1017, u.TextureRenderTargetFormat.RTF_RGBA32F, u.LinearColor(0, 0, 0, 1), False, False)
assert land.landscape_export_heightmap_to_render_target(builtins.XR_RT, False, True)
t0 = time.monotonic()


def _read(dt):
    if time.monotonic() - t0 < 20:
        return
    u.unregister_slate_post_tick_callback(builtins.XR_HT)
    vals = array.array('H', (round(c.r) for c in u.RenderingLibrary.read_render_target_raw(w, builtins.XR_RT, False)))
    assert len(vals) == 1017 ** 2
    (D / 'height_before.u16').write_bytes(vals.tobytes())
    (D / 'height_before.ok').write_text('%d %d' % (min(vals), max(vals)))


builtins.XR_HT = u.register_slate_post_tick_callback(_read)
print('RECON', json.dumps(L, default=str)[:600], 'foliage comps', len(F), 'instances', sum(len(r['xf']) for r in F), 'actors', len(A))
