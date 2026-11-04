"""probe_pfr.py (measure job, read-only): Pine Forest redesign - current production world facts + landscape layer API capability.
Writes Saved/Codex/PineForestRedesign_20261104/recon/probe.json, foliage.json, actors.json, height_now.u16 (+ .ok), weight_<layer>.u8
(old export API) and prints PROBE_PFR {...}. Nothing is modified (the weight export renders into transient render targets only)."""
import unreal as u, json, pathlib, time, array, builtins, hashlib

D = pathlib.Path(u.Paths.project_dir()) / 'Saved/Codex/PineForestRedesign_20261104/recon'; D.mkdir(parents=True, exist_ok=True)
E = u.get_editor_subsystem(u.UnrealEditorSubsystem); assert E.get_game_world() is None, 'PIE running'
w = E.get_editor_world(); A = u.get_editor_subsystem(u.EditorActorSubsystem); actors = A.get_all_level_actors()
S = u.EditorLoadingAndSavingUtils
out = {'world': w.get_path_name(), 'started': time.strftime('%Y-%m-%d %H:%M:%S'),
       'dirty': sorted([p.get_name() for p in S.get_dirty_content_packages()] + [p.get_name() for p in S.get_dirty_map_packages()])}
land = next(a for a in actors if isinstance(a, u.Landscape))
out['landscape'] = {'label': land.get_actor_label(), 'material': str(land.get_editor_property('landscape_material')),
                    'loc': [round(v) for v in land.get_actor_location().to_tuple()], 'scale': [round(v, 2) for v in land.get_actor_scale3d().to_tuple()]}
api = {}
for n in ('render_weightmap', 'render_weightmaps', 'landscape_import_weightmap_from_render_target', 'landscape_export_weightmap_to_render_target',
          'landscape_import_heightmap_from_render_target', 'landscape_export_heightmap_to_render_target', 'get_target_layer_names', 'get_edit_layers_bp',
          'get_edit_layer_by_name_bp', 'add_target_layer', 'has_target_layer', 'get_target_layers', 'remove_target_layer', 'create_layer',
          'get_layer_count', 'set_landscape_material', 'landscape_material', 'get_landscape_info', 'editor_apply_spline', 'has_layers_content',
          'can_have_layers_content', 'get_layers', 'target_layers', 'editor_layer_settings'):
    try:
        v = getattr(land, n)
        api[n] = (v.__doc__ or '')[:320].replace('\n', ' | ') if callable(v) else 'PROP ' + str(v)[:200]
    except Exception as ex:
        api[n] = 'NO: ' + repr(ex)[:120]
out['api'] = api
for flag in (False, True):
    try:
        out['target_layers_%s' % flag] = [str(x) for x in land.get_target_layer_names(flag)]
    except Exception as ex:
        out['target_layers_%s' % flag] = repr(ex)[:200]
try:
    L = land.get_edit_layers_bp(); out['edit_layers'] = []
    for l in L:
        d = {'cls': l.get_class().get_name()}
        for k in ('name', 'visible', 'locked'):
            try: d[k] = str(l.get_editor_property(k))
            except Exception as ex: d[k] = 'n/a'
        out['edit_layers'].append(d)
except Exception as ex:
    out['edit_layers'] = 'n/a ' + repr(ex)[:200]
# landscape material instance: parent chain + parameters + grass types of the master
try:
    mi = land.get_editor_property('landscape_material'); chain = []; m = mi
    while m is not None and isinstance(m, u.MaterialInstance):
        chain.append(m.get_path_name()); m = m.get_editor_property('parent')
    if m is not None: chain.append(m.get_path_name())
    out['landscape_mat_chain'] = chain
    ML = u.MaterialEditingLibrary
    if isinstance(mi, u.MaterialInstanceConstant):
        out['landscape_mi_scalars'] = {str(n): round(ML.get_material_instance_scalar_parameter_value(mi, n), 4) for n in ML.get_scalar_parameter_names(mi)}
        out['landscape_mi_textures'] = {str(n): (ML.get_material_instance_texture_parameter_value(mi, n).get_path_name() if ML.get_material_instance_texture_parameter_value(mi, n) else None) for n in ML.get_texture_parameter_names(mi)}
except Exception as ex:
    out['landscape_mat_err'] = repr(ex)[:300]
# Pine Forest Pack landscape master: layer names (LayerBlend) + grass types
try:
    pm = u.load_asset('/Game/PineForestPack/Materials/Landscape/Masters/M_Landscape_PineForest')
    pmi = u.load_asset('/Game/PineForestPack/Materials/Landscape/Instances/MI_LandscapePineForest')
    info = {'master': pm.get_path_name() if pm else None, 'mi': pmi.get_path_name() if pmi else None}
    if pmi:
        ML = u.MaterialEditingLibrary
        info['mi_scalars'] = {str(n): round(ML.get_material_instance_scalar_parameter_value(pmi, n), 4) for n in ML.get_scalar_parameter_names(pmi)}
        info['mi_textures'] = {str(n): (ML.get_material_instance_texture_parameter_value(pmi, n).get_path_name() if ML.get_material_instance_texture_parameter_value(pmi, n) else None) for n in ML.get_texture_parameter_names(pmi)}
        info['mi_vectors'] = {str(n): [round(c, 3) for c in ML.get_material_instance_vector_parameter_value(pmi, n).to_tuple()] for n in ML.get_vector_parameter_names(pmi)}
        info['mi_static_switches'] = {}
        try:
            for n in ML.get_static_switch_parameter_names(pmi):
                info['mi_static_switches'][str(n)] = ML.get_material_instance_static_switch_parameter_value(pmi, n)
        except Exception as ex:
            info['mi_static_switches'] = repr(ex)[:120]
    out['pfp_landscape'] = info
    reg = u.AssetRegistryHelpers.get_asset_registry()
    out['pfp_grass_types'] = [str(a.package_name) for a in reg.get_assets_by_path('/Game/PineForestPack/Procedurals', True) if str(a.asset_class_path.asset_name) == 'LandscapeGrassType']
    out['pfp_layer_infos'] = [str(a.package_name) for a in reg.get_assets_by_path('/Game/PineForestPack/Materials/Landscape/LandscapeLayers', True)]
    gts = {}
    for p in out['pfp_grass_types']:
        gt = u.load_asset(p)
        try:
            gts[p.split('/')[-1]] = [{'mesh': (v.get_editor_property('grass_mesh').get_path_name().split('.')[0] if v.get_editor_property('grass_mesh') else None),
                                      'density': v.get_editor_property('grass_density').get_editor_property('default') if hasattr(v.get_editor_property('grass_density'), 'get_editor_property') else str(v.get_editor_property('grass_density')),
                                      'start_cull': v.get_editor_property('start_cull_distance').get_editor_property('default') if hasattr(v.get_editor_property('start_cull_distance'), 'get_editor_property') else str(v.get_editor_property('start_cull_distance')),
                                      'end_cull': v.get_editor_property('end_cull_distance').get_editor_property('default') if hasattr(v.get_editor_property('end_cull_distance'), 'get_editor_property') else str(v.get_editor_property('end_cull_distance')),
                                      'scale': [str(v.get_editor_property('scale_x')), str(v.get_editor_property('scale_y')), str(v.get_editor_property('scale_z'))]} for v in gt.get_editor_property('grass_varieties')]
        except Exception as ex:
            gts[p.split('/')[-1]] = 'n/a ' + repr(ex)[:160]
    out['pfp_grass_detail'] = gts
except Exception as ex:
    out['pfp_err'] = repr(ex)[:300]
# RVT actors / volumes present?
out['rvt_volumes'] = [a.get_actor_label() for a in actors if a.get_class().get_name() in ('RuntimeVirtualTextureVolume',)]
# foliage census + actors (same format as ExteriorRedesign recon.py)
ifa = [a for a in actors if isinstance(a, u.InstancedFoliageActor)]; F = []
for a in ifa:
    for c in a.get_components_by_class(u.InstancedStaticMeshComponent):
        n = c.get_instance_count()
        if not n or not c.static_mesh: continue
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
(D / 'foliage.json').write_text(json.dumps(F)); out['foliage'] = {'comps': len(F), 'instances': sum(len(r['xf']) for r in F)}
AC = []
for a in actors:
    try: o, e = a.get_actor_bounds(False)
    except Exception: continue
    r = {'label': a.get_actor_label(), 'class': a.get_class().get_name(), 'level': a.get_level().get_outer().get_name(),
         'loc': [round(a.get_actor_location().x), round(a.get_actor_location().y), round(a.get_actor_location().z)],
         'b': [[round(o.x), round(o.y), round(o.z)], [round(e.x), round(e.y), round(e.z)]], 'hidden': a.is_hidden_ed()}
    if isinstance(a, u.StaticMeshActor):
        m = a.static_mesh_component.static_mesh; r['mesh'] = m.get_path_name().split('.')[0] if m else None
    AC.append(r)
(D / 'actors.json').write_text(json.dumps(AC)); out['actors'] = len(AC)
# light owners (current production values)
LO = {}
for a in actors:
    lab = a.get_actor_label()
    if lab.startswith(('EX_PostRain', 'EX_Look')):
        d = {'class': a.get_class().get_name()}
        try:
            if isinstance(a, u.DirectionalLight):
                c = a.get_component_by_class(u.DirectionalLightComponent); d.update(rot=[round(v, 1) for v in a.get_actor_rotation().to_tuple()], intensity=c.get_editor_property('intensity'), temp=c.get_editor_property('temperature'), angle=c.get_editor_property('light_source_angle'), vol=c.get_editor_property('volumetric_scattering_intensity'))
            elif isinstance(a, u.SkyLight):
                c = a.get_component_by_class(u.SkyLightComponent); d.update(intensity=c.get_editor_property('intensity'))
            elif isinstance(a, u.ExponentialHeightFog):
                c = a.get_component_by_class(u.ExponentialHeightFogComponent); d.update(density=c.get_editor_property('fog_density'), falloff=c.get_editor_property('fog_height_falloff'), start=c.get_editor_property('start_distance'), opacity=c.get_editor_property('fog_max_opacity'))
        except Exception as ex:
            d['err'] = repr(ex)[:100]
        LO[lab] = d
out['lights'] = LO
# heightmap export (old API, delayed read) + weightmap export per target layer (old API)
LAY = out.get('target_layers_False') if isinstance(out.get('target_layers_False'), list) else []
builtins.PFR_RT = u.RenderingLibrary.create_render_target2d(w, 1017, 1017, u.TextureRenderTargetFormat.RTF_RGBA32F, u.LinearColor(0, 0, 0, 1), False, False)
builtins.PFR_WRT = {l: u.RenderingLibrary.create_render_target2d(w, 1017, 1017, u.TextureRenderTargetFormat.RTF_RGBA8, u.LinearColor(0, 0, 0, 1), False, False) for l in LAY}
out['height_export_ok'] = bool(land.landscape_export_heightmap_to_render_target(builtins.PFR_RT, False, True))
out['weight_export_ok'] = {}
for l in LAY:
    try:
        out['weight_export_ok'][l] = bool(land.landscape_export_weightmap_to_render_target(builtins.PFR_WRT[l], l, False))
    except Exception as ex:
        out['weight_export_ok'][l] = 'ERR ' + repr(ex)[:160]
st = {'t': time.monotonic(), 'tries': 0}


def _read(dt):
    if time.monotonic() - st['t'] < 20: return
    try:
        vals = array.array('H', (round(c.r) for c in u.RenderingLibrary.read_render_target_raw(w, builtins.PFR_RT, False)))
        if max(vals) == 0 and st['tries'] < 3:
            st['tries'] += 1; st['t'] = time.monotonic(); land.landscape_export_heightmap_to_render_target(builtins.PFR_RT, False, True); return
        (D / 'height_now.u16').write_bytes(vals.tobytes()); out['height'] = {'min': min(vals), 'max': max(vals), 'sha1': hashlib.sha1(vals.tobytes()).hexdigest(), 'retries': st['tries']}
        ref = pathlib.Path(u.Paths.project_dir()) / 'Saved/Codex/ExteriorRedesign_20261031/recon/height_before.u16'
        if ref.exists(): out['height']['same_as_xr_recon'] = hashlib.sha1(ref.read_bytes()).hexdigest() == out['height']['sha1']
        ws = {}
        for l in LAY:
            px = u.RenderingLibrary.read_render_target_raw(w, builtins.PFR_WRT[l], False)
            v = array.array('B', (max(0, min(255, round(c.r * 255))) for c in px))
            (D / ('weight_%s.u8' % l)).write_bytes(v.tobytes()); ws[l] = {'max': max(v), 'mean': round(sum(v) / len(v), 2), 'nonzero': sum(1 for x in v if x)}
        out['weights'] = ws
    except Exception as ex:
        out['read_err'] = repr(ex)[:300]
    u.unregister_slate_post_tick_callback(builtins.PFR_HT); out['finished'] = time.strftime('%H:%M:%S')
    (D / 'probe.json').write_text(json.dumps(out, indent=1, default=str)); (D / 'probe.done').write_text('ok')


builtins.PFR_HT = u.register_slate_post_tick_callback(_read)
print('PROBE_PFR scheduled', json.dumps({k: out[k] for k in ('world', 'dirty', 'foliage', 'actors', 'target_layers_False', 'height_export_ok', 'weight_export_ok')}, default=str)[:900])
