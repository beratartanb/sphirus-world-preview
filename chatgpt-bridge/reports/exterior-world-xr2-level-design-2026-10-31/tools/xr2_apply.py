"""xr2_apply.py (WRITE job under the map manifest; NEVER saves): apply an XR2 design variant to the open main map IN MEMORY, or restore.
builtins.XR2_MODE in {'dryrun', 'apply', 'restore'}; builtins.XR2_VARIANT (e.g. 'x3').
  heightmap: RG16 PNG -> RGBA8 render target -> verified samples -> landscape_import_heightmap_from_render_target -> re-export ->
             verified samples (the proven R1 route of ExteriorRedesign_20261031/xr_apply.py). restore = recon/height_before.
  foliage:   per changed component (mesh + cull) the unique owned FoliageType: remove_all_instances + add_instances with the designed list
             (apply) or the recon snapshot list (restore); per-component counts must stay unchanged.
  actors:    apply spawns the variant's structural actors (label prefix XR2_, outliner folder XR2_Trial); invisible wade-limit cubes are
             hidden in game, cast no shadow and use the InvisibleWall profile (pawn only). restore destroys every actor labelled XR2_*.
  dryrun:    resolves foliage types / meshes and decodes the PNG; changes nothing.
Apply requires a clean start (no XR2_ actors); restore leaves heightmap, foliage and actors as the recon snapshot.
Output: Saved/Codex/ExteriorWorld_XR2_20261031/design/apply_<mode>_<variant>.json"""
import unreal as u, pathlib, json, time, builtins, array, random, math

PJ = pathlib.Path(u.Paths.project_dir()); D = PJ / 'Saved/Codex/ExteriorWorld_XR2_20261031'; RC = PJ / 'Saved/Codex/ExteriorRedesign_20261031'
MODE, VAR = builtins.XR2_MODE, getattr(builtins, 'XR2_VARIANT', 'x3')
STAGE = getattr(builtins, 'XR2_STAGE', 'build')       # 'build' (terrain + foliage + structural actors) | 'dress' (path decals only)
assert MODE in ('dryrun', 'apply', 'restore')
E = u.get_editor_subsystem(u.UnrealEditorSubsystem); assert E.get_game_world() is None, 'PIE running'
A = u.get_editor_subsystem(u.EditorActorSubsystem)
w = E.get_editor_world(); assert w.get_path_name().startswith('/Game/GraceRanger/Maps/L_GR_SphirusHouse.')
actors = A.get_all_level_actors()
land = next(a for a in actors if isinstance(a, u.Landscape))
ifas = [a for a in actors if a.get_class().get_name() == 'InstancedFoliageActor']
plan = json.loads((D / 'design' / ('plan_%s.json' % VAR)).read_text())
changed = json.loads((D / 'design' / ('foliage_%s.json' % VAR)).read_text())
spawns = json.loads((D / 'design' / ('spawn_%s.json' % VAR)).read_text())
recon = {(r['mesh'], tuple(r['cull'])): r for r in json.loads((RC / 'recon' / 'foliage.json').read_text())}
png = (RC / 'design' / 'height_before.png') if MODE == 'restore' else (D / 'design' / plan['file'])
reg = u.AssetRegistryHelpers.get_asset_registry()
FT_DIR = '/Game/GraceRanger/Environment/Exterior20260921/Foliage'
fts = [t for t in (ad.get_asset() for ad in reg.get_assets_by_path(FT_DIR, True)) if isinstance(t, u.FoliageType_InstancedStaticMesh)]
S = u.EditorLoadingAndSavingUtils
dirty = lambda: sorted([p.get_name() for p in S.get_dirty_content_packages()] + [p.get_name() for p in S.get_dirty_map_packages()])
xr2_actors = lambda: [a for a in A.get_all_level_actors() if a.get_actor_label().startswith('XR2_')]
res = {'mode': MODE, 'variant': VAR, 'png': png.name, 'problems': [], 'foliage': [], 'dirty_before': dirty(), 'xr2_actors_before': len(xr2_actors())}


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
meshes = {}
if MODE != 'restore':
    if STAGE == 'build' and res['xr2_actors_before']:
        res['problems'].append('XR2_ actors already present (%d): restore first' % res['xr2_actors_before'])
    if STAGE == 'dress' and (not res['xr2_actors_before'] or any(a.get_actor_label().startswith('XR2_Decal') for a in xr2_actors())):
        res['problems'].append('dress needs a built variant without decals')
    for sp in spawns:
        if sp['mesh'] not in meshes:
            meshes[sp['mesh']] = u.load_asset(sp['mesh'])
            if not meshes[sp['mesh']]:
                res['problems'].append('mesh missing ' + sp['mesh'])
if res['problems']:
    (D / 'design' / ('apply_%s_%s.json' % (MODE, VAR))).write_text(json.dumps(res, indent=1, default=str))
    raise RuntimeError('REFUSED before any change: %s' % res['problems'][:6])

tex = u.RenderingLibrary.import_file_as_texture2d(w, str(png))
tex.set_editor_property('srgb', False); tex.set_editor_property('filter', u.TextureFilter.TF_NEAREST)
tex.set_editor_property('compression_settings', u.TextureCompressionSettings.TC_VECTOR_DISPLACEMENTMAP)
rt = u.RenderingLibrary.create_render_target2d(w, 1017, 1017, u.TextureRenderTargetFormat.RTF_RGBA8, u.LinearColor(0, 0, 0, 1), False, False)
builtins.XR2_KEEP = (tex, rt); st = {'t': time.monotonic(), 'stage': 0}
if MODE == 'restore':
    H = array.array('H'); H.frombytes((RC / 'recon' / 'height_before.u16').read_bytes())
    rr = random.Random(7); samples = [{'x': x, 'y': y, 'height': H[y * 1017 + x]} for x, y in ((rr.randrange(300, 700), rr.randrange(300, 700)) for _ in range(60))]
else:
    samples = plan['samples']


def ground(x, y):
    h = u.SystemLibrary.line_trace_multi(w, u.Vector(x, y, 6000), u.Vector(x, y, -3000), u.TraceTypeQuery.TRACE_TYPE_QUERY1, True, [], u.DrawDebugTrace.NONE, True)
    for r_ in (h or []):
        t = r_.to_tuple()
        if t[0] and isinstance(t[9], u.Landscape):
            return t[4].z
    return None


def normal(x, y, d=60.0):
    zx0, zx1, zy0, zy1 = ground(x - d, y), ground(x + d, y), ground(x, y - d), ground(x, y + d)
    if None in (zx0, zx1, zy0, zy1):
        return u.Vector(0, 0, 1)
    return u.Vector(-(zx1 - zx0) / (2 * d), -(zy1 - zy0) / (2 * d), 1.0).normal()


def done(ok):
    u.unregister_slate_post_tick_callback(builtins.XR2_AH)
    res['finished'] = time.strftime('%H:%M:%S'); res['ok'] = ok; res['dirty_after'] = dirty(); res['xr2_actors_after'] = len(xr2_actors())
    (D / 'design' / ('apply_%s_%s.json' % (MODE, VAR))).write_text(json.dumps(res, indent=1, default=str))


def rg(x, y):
    c = u.RenderingLibrary.read_render_target_raw_pixel(w, rt, x, y, False)
    return round(c.r) * 256 + round(c.g)


def do_actors():
    if MODE == 'restore':
        gone = xr2_actors(); n = len(gone)
        for a in gone:
            A.destroy_actor(a)
        res['actors_destroyed'] = n; return
    n = 0
    for sp in spawns:
        if (sp.get('stage') == 'dress') != (STAGE == 'dress'):
            continue
        if sp['kind'] == 'decal':
            x, y = sp['x'], sp['y']; nrm = u.Vector(*sp['nrm']).normal(); fwd = u.Vector(math.cos(math.radians(sp['yaw'])), math.sin(math.radians(sp['yaw'])), 0.0)
            gz = sp['z']
            a = A.spawn_actor_from_class(u.DecalActor, u.Vector(x, y, gz + 5), u.MathLibrary.make_rot_from_xz(nrm * -1.0, fwd))
            dc = a.get_component_by_class(u.DecalComponent); dc.set_decal_material(meshes[sp['mesh']])
            dc.set_editor_property('decal_size', u.Vector(30.0, sp['size'][1], sp['size'][0])); dc.set_editor_property('sort_order', 0)
        else:
            a = A.spawn_actor_from_class(u.StaticMeshActor, u.Vector(sp['x'], sp['y'], sp['z']), u.Rotator(pitch=sp['pitch'], yaw=sp['yaw'], roll=sp['roll']))
            a.set_actor_scale3d(u.Vector(*sp['scale']))
            c = a.static_mesh_component; c.set_static_mesh(meshes[sp['mesh']]); c.set_editor_property('receives_decals', False)
            if sp.get('invisible'):
                a.set_actor_hidden_in_game(True); c.set_editor_property('cast_shadow', False); c.set_editor_property('visible', False)
                c.set_collision_enabled(u.CollisionEnabled.QUERY_AND_PHYSICS); c.set_collision_response_to_all_channels(u.CollisionResponseType.ECR_IGNORE)
                c.set_collision_response_to_channel(u.CollisionChannel.ECC_PAWN, u.CollisionResponseType.ECR_BLOCK)
            elif sp['kind'] == 'dress_soft':
                c.set_collision_enabled(u.CollisionEnabled.NO_COLLISION)
            elif sp['kind'] not in ('ring_rock', 'inner_rock', 'r6_outcrop', 'inner_bank', 'dress_tree'):
                # logs / deadfall / landmarks: pawn + Visibility collision, the GR spring arm ignores them (VMP v7 lesson)
                c.set_collision_response_to_channel(u.CollisionChannel.ECC_CAMERA, u.CollisionResponseType.ECR_IGNORE)
        a.set_actor_label(sp['label']); a.set_folder_path('XR2_Trial/' + sp['kind'])
        n += 1
    res['actors_spawned'] = n


def tick(dt):
    try:
        now = time.monotonic()
        if now - st['t'] < 4:
            return
        if STAGE == 'dress':
            if MODE == 'apply':
                with u.ScopedEditorTransaction('XR2 dress %s (unsaved test)' % VAR):
                    do_actors()
            return done(True)
        if st['stage'] == 0 and getattr(builtins, 'XR2_SKIP_HEIGHT', False):
            # resume: the heightmap was already imported and verified by a separate export (height_export.py); foliage + actors only
            res['height'] = 'skipped (verified separately)'; st.update(t=now - 30, stage=4, skip=True); return
        if st['stage'] == 4 and st.get('skip'):
            with u.ScopedEditorTransaction('XR2 %s %s foliage+actors (unsaved test)' % (MODE, VAR)):
                for f, xf, n0, key in todo:
                    u.InstancedFoliageActor.remove_all_instances(w, f)
                    u.InstancedFoliageActor.add_instances(w, f, [tf(x) for x in xf])
                do_actors()
            for f, xf, n0, key in todo:
                cs = comp_for(*key); n1 = cs[0].get_instance_count() if len(cs) == 1 else -1
                res['foliage'].append({'mesh': key[0], 'cull': key[1], 'n_before': n0, 'n_after': n1})
                if n1 != n0:
                    res['problems'].append('count %s %d -> %d' % (key[0], n0, n1))
            return done(not res['problems'])
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
                res['foliage'] = [{'mesh': k[0], 'cull': k[1], 'ft': f.get_path_name(), 'n': n} for f, xf, n, k in todo]; res['meshes'] = list(meshes); return done(True)
            with u.ScopedEditorTransaction('XR2 %s %s heightmap (unsaved test)' % (MODE, VAR)):
                land.modify(); assert land.landscape_import_heightmap_from_render_target(rt, True, 0)
            st.update(t=now, stage=2); return
        if st['stage'] == 2:
            builtins.XR2_RT2 = u.RenderingLibrary.create_render_target2d(w, 1017, 1017, u.TextureRenderTargetFormat.RTF_RGBA32F, u.LinearColor(0, 0, 0, 1), False, False)
            st.update(t=now, stage=3); return
        if st['stage'] == 3:
            assert land.landscape_export_heightmap_to_render_target(builtins.XR2_RT2, False, True); st.update(t=now, stage=4); return
        if st['stage'] == 4:
            if now - st['t'] < 20:
                return
            got = [(s, round(u.RenderingLibrary.read_render_target_raw_pixel(w, builtins.XR2_RT2, s['x'], s['y'], False).r)) for s in samples]
            if all(g[1] == 0 for g in got) and st.get('tries', 0) < 4:      # export not rendered yet (editor RT trap): export again
                st.update(t=now, stage=3, tries=st.get('tries', 0) + 1); res['readback_retries'] = st['tries']; return
            mism = [g for g in got if abs(g[1] - g[0]['height']) > 1]
            res['readback_mismatch'] = mism[:10]; res['readback_n'] = len(got)
            if mism:
                res['problems'].append('height readback mismatch %d (foliage/actors NOT changed)' % len(mism)); return done(False)
            with u.ScopedEditorTransaction('XR2 %s %s foliage+actors (unsaved test)' % (MODE, VAR)):
                for f, xf, n0, key in todo:
                    u.InstancedFoliageActor.remove_all_instances(w, f)
                    u.InstancedFoliageActor.add_instances(w, f, [tf(x) for x in xf])
                do_actors()
            for f, xf, n0, key in todo:
                cs = comp_for(*key); n1 = cs[0].get_instance_count() if len(cs) == 1 else -1
                res['foliage'].append({'mesh': key[0], 'cull': key[1], 'n_before': n0, 'n_after': n1})
                if n1 != n0:
                    res['problems'].append('count %s %d -> %d' % (key[0], n0, n1))
            return done(not res['problems'])
    except Exception as ex:
        res['problems'].append(repr(ex)); done(False)


builtins.XR2_AH = u.register_slate_post_tick_callback(tick)
print('XR2_APPLY scheduled', MODE, VAR, 'components', len(todo), 'spawns', len(spawns) if MODE != 'restore' else 0, 'png', png.name)
