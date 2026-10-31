"""xr_apply.py (WRITE job under a manifest; NEVER saves): apply a designed variant of the Exterior World Redesign in memory, or restore.
builtins.XR_MODE in {'dryrun', 'apply', 'restore'}; builtins.XR_VARIANT (e.g. 'r2').
  heightmap: RG16 PNG -> RGBA8 render target (Canvas, nearest, no sRGB) -> verify samples -> landscape_import_heightmap_from_render_target
             (the RG-decode route of FrontRefugeE2/apply_height.py, proven on this 5.8.1 landscape) -> re-export -> verify samples.
             restore = the same route with recon/height_before (exported from this editor session before any change).
  foliage:   for every changed component (mesh + cull): its FoliageType is the unique owned type with the same mesh and cull distances
             (path of AIToolingEval pilot_apply.py); InstancedFoliageActor.remove_all_instances + add_instances with the designed list
             (apply) or with the recon snapshot list (restore). Per-component instance counts are checked unchanged.
  dryrun:    resolves every foliage type and checks the PNG decode samples; changes nothing.
Output: <D>/design/apply_<mode>_<variant>.json"""
import unreal as u, pathlib, json, time, builtins, array

P = pathlib.Path(u.Paths.project_dir()); D = P / 'Saved/Codex/ExteriorRedesign_20261031'
MODE, VAR = getattr(builtins, 'XR_MODE'), getattr(builtins, 'XR_VARIANT', 'r2')
assert MODE in ('dryrun', 'apply', 'restore')
E = u.get_editor_subsystem(u.UnrealEditorSubsystem); assert E.get_game_world() is None, 'PIE running'
w = E.get_editor_world(); assert w.get_path_name().startswith('/Game/GraceRanger/Maps/L_GR_SphirusHouse.')
actors = u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors()
land = next(a for a in actors if isinstance(a, u.Landscape))
ifas = [a for a in actors if a.get_class().get_name() == 'InstancedFoliageActor']
plan = json.loads((D / 'design' / ('plan_%s.json' % VAR)).read_text())
changed = json.loads((D / 'design' / ('foliage_%s.json' % VAR)).read_text())
recon = {(r['mesh'], tuple(r['cull'])): r for r in json.loads((D / 'recon' / 'foliage.json').read_text())}
if MODE == 'restore':
    png = D / 'design' / 'height_before.png'
else:
    png = D / 'design' / plan['file']
reg = u.AssetRegistryHelpers.get_asset_registry()
FT_DIR = '/Game/GraceRanger/Environment/Exterior20260921/Foliage'
fts = [t for t in (ad.get_asset() for ad in reg.get_assets_by_path(FT_DIR, True)) if isinstance(t, u.FoliageType_InstancedStaticMesh)]
S = u.EditorLoadingAndSavingUtils
res = {'mode': MODE, 'variant': VAR, 'png': png.name, 'problems': [], 'foliage': [],
       'dirty_before': sorted([p.get_name() for p in S.get_dirty_content_packages()] + [p.get_name() for p in S.get_dirty_map_packages()])}


def comp_for(mesh, cull):
    out = []
    for a in ifas:
        for c in a.get_components_by_class(u.FoliageInstancedStaticMeshComponent):
            if c.static_mesh and c.static_mesh.get_path_name().split('.')[0] == mesh and [c.get_editor_property('instance_start_cull_distance'), c.get_editor_property('instance_end_cull_distance')] == list(cull):
                out.append(c)
    return out


def ft_of(c):
    return [t for t in fts if t.get_editor_property('mesh') == c.static_mesh and t.get_editor_property('cull_distance').min == c.get_editor_property('instance_start_cull_distance')
            and t.get_editor_property('cull_distance').max == c.get_editor_property('instance_end_cull_distance')]


def tf(x):
    return u.Transform(location=u.Vector(x[0], x[1], x[2]), rotation=u.Rotator(pitch=x[3], yaw=x[4], roll=x[5]), scale=u.Vector(x[6], x[7], x[8]))


todo = []
for ch in changed:
    key = (ch['mesh'], tuple(ch['cull'])); cs = comp_for(*key)
    if len(cs) != 1:
        res['problems'].append('component not unique %s %s: %d' % (key[0], key[1], len(cs))); continue
    f = ft_of(cs[0])
    if len(f) != 1:
        res['problems'].append('foliage type not unique %s %s: %s' % (key[0], key[1], [t.get_path_name() for t in f])); continue
    n_now = cs[0].get_instance_count()
    if n_now != ch['n']:
        res['problems'].append('count changed since recon %s: %d vs %d' % (key[0], n_now, ch['n'])); continue
    todo.append((f[0], ch['xf_after'] if MODE != 'restore' else recon[key]['xf'], n_now, key))
if res['problems']:
    (D / 'design' / ('apply_%s_%s.json' % (MODE, VAR))).write_text(json.dumps(res, indent=1, default=str))
    raise RuntimeError('REFUSED before any change: %s' % res['problems'][:6])

tex = u.RenderingLibrary.import_file_as_texture2d(w, str(png))
tex.set_editor_property('srgb', False); tex.set_editor_property('filter', u.TextureFilter.TF_NEAREST)
tex.set_editor_property('compression_settings', u.TextureCompressionSettings.TC_VECTOR_DISPLACEMENTMAP)
rt = u.RenderingLibrary.create_render_target2d(w, 1017, 1017, u.TextureRenderTargetFormat.RTF_RGBA8, u.LinearColor(0, 0, 0, 1), False, False)
builtins.XR_KEEP = (tex, rt); st = {'t': time.monotonic(), 'stage': 0}
if MODE == 'restore':
    H = array.array('H'); H.frombytes((D / 'recon' / 'height_before.u16').read_bytes())
    import random
    rr = random.Random(7); samples = [{'x': x, 'y': y, 'height': H[y * 1017 + x]} for x, y in ((rr.randrange(300, 700), rr.randrange(300, 700)) for _ in range(60))]
else:
    samples = plan['samples']


def done(ok):
    u.unregister_slate_post_tick_callback(builtins.XR_AH)
    res['finished'] = time.strftime('%H:%M:%S'); res['ok'] = ok
    res['dirty_after'] = sorted([p.get_name() for p in S.get_dirty_content_packages()] + [p.get_name() for p in S.get_dirty_map_packages()])
    (D / 'design' / ('apply_%s_%s.json' % (MODE, VAR))).write_text(json.dumps(res, indent=1, default=str))


def rg(x, y):
    c = u.RenderingLibrary.read_render_target_raw_pixel(w, rt, x, y, False)
    return round(c.r) * 256 + round(c.g)


def tick(dt):
    try:
        now = time.monotonic()
        if now - st['t'] < 4:
            return
        if st['stage'] == 0:
            canvas, size, ctx = u.RenderingLibrary.begin_draw_canvas_to_render_target(w, rt)
            canvas.draw_texture(tex, u.Vector2D(0, 0), u.Vector2D(1017, 1017), u.Vector2D(0, 0), u.Vector2D(1, 1), u.LinearColor(1, 1, 1, 1), u.BlendMode.BLEND_OPAQUE)
            u.RenderingLibrary.end_draw_canvas_to_render_target(w, ctx); st.update(t=now, stage=1); return
        if st['stage'] == 1:
            bad = [(s, rg(s['x'], s['y'])) for s in samples if rg(s['x'], s['y']) != s['height']]
            res['decode_bad'] = bad[:10]
            if bad:
                res['problems'].append('decode mismatch %d' % len(bad)); return done(False)
            if MODE == 'dryrun':
                res['foliage'] = [{'mesh': k[0], 'cull': k[1], 'ft': f.get_path_name(), 'n': n} for f, xf, n, k in todo]; return done(True)
            with u.ScopedEditorTransaction('Exterior redesign %s %s (unsaved test)' % (MODE, VAR)):
                land.modify(); assert land.landscape_import_heightmap_from_render_target(rt, True, 0)
            st.update(t=now, stage=2); return
        if st['stage'] == 2:
            builtins.XR_RT2 = u.RenderingLibrary.create_render_target2d(w, 1017, 1017, u.TextureRenderTargetFormat.RTF_RGBA32F, u.LinearColor(0, 0, 0, 1), False, False)
            st.update(t=now, stage=3); return
        if st['stage'] == 3:
            assert land.landscape_export_heightmap_to_render_target(builtins.XR_RT2, False, True); st.update(t=now, stage=4); return
        if st['stage'] == 4:
            if now - st['t'] < 20:
                return
            got = [(s, round(u.RenderingLibrary.read_render_target_raw_pixel(w, builtins.XR_RT2, s['x'], s['y'], False).r)) for s in samples]
            mism = [g for g in got if abs(g[1] - g[0]['height']) > 1]
            res['readback_mismatch'] = mism[:10]; res['readback_n'] = len(got)
            if mism:
                res['problems'].append('height readback mismatch %d (foliage NOT changed)' % len(mism)); return done(False)
            with u.ScopedEditorTransaction('Exterior redesign foliage %s %s (unsaved test)' % (MODE, VAR)):
                for f, xf, n0, key in todo:
                    u.InstancedFoliageActor.remove_all_instances(w, f)
                    u.InstancedFoliageActor.add_instances(w, f, [tf(x) for x in xf])
            for f, xf, n0, key in todo:
                cs = comp_for(*key); n1 = cs[0].get_instance_count() if len(cs) == 1 else -1
                res['foliage'].append({'mesh': key[0], 'cull': key[1], 'n_before': n0, 'n_after': n1})
                if n1 != n0:
                    res['problems'].append('count %s %d -> %d' % (key[0], n0, n1))
            return done(not res['problems'])
    except Exception as ex:
        res['problems'].append(repr(ex)); done(False)


builtins.XR_AH = u.register_slate_post_tick_callback(tick)
print('XR_APPLY scheduled', MODE, VAR, 'components', len(todo), 'png', png.name)
