"""land_trial.py (WRITE job under the pfr_world manifest; NEVER saves): switch the production landscape to a project-owned instance of
the Pine Forest Pack landscape material and paint its layers from the design masks, in memory.
builtins.PFR_LAND_MODE 'apply' | 'restore'; builtins.PFR_LAND_VARIANT (mask set, default 'p1'); builtins.PFR_LAND_LAYERS (default the five
used by the showcase). apply: 1. MI_EX_PF_Landscape = duplicate of MI_LandscapePineForest (created once, reused), 2. landscape_material
= MI, 3. target_layers += {layer: LL_<layer>_LayerInfo}, 4. per layer: PNG -> texture -> RGBA8 RT (canvas) -> verified samples ->
landscape_import_weightmap_from_render_target -> render_weightmap read-back of a few samples. restore: original material + original
target layers back (weights of the PFP layers are left in the components; delete_unused_layers() removes the unused allocations).
Output: Saved/Codex/PineForestRedesign_20261104/design/land_<mode>_<variant>.json"""
import unreal as u, json, pathlib, time, builtins, array

PJ = pathlib.Path(u.Paths.project_dir()); D = PJ / 'Saved/Codex/PineForestRedesign_20261104/design'
MODE = getattr(builtins, 'PFR_LAND_MODE', 'apply'); VAR = getattr(builtins, 'PFR_LAND_VARIANT', 'p1')
LAYERS = list(getattr(builtins, 'PFR_LAND_LAYERS', ['Forest', 'Ground', 'GroundPath', 'ForestField', 'WetPuddle']))
MI_PATH = '/Game/GraceRanger/Environment/Exterior20260921/Materials/MI_EX_PF_Landscape'; SRC_MI = '/Game/PineForestPack/Materials/Landscape/Instances/MI_LandscapePineForest'
LI = '/Game/PineForestPack/Materials/Landscape/LandscapeLayers/LL_%s_LayerInfo'
E = u.get_editor_subsystem(u.UnrealEditorSubsystem); assert E.get_game_world() is None, 'PIE running'
w = E.get_editor_world(); A = u.get_editor_subsystem(u.EditorActorSubsystem)
land = next(a for a in A.get_all_level_actors() if isinstance(a, u.Landscape))
S = u.EditorLoadingAndSavingUtils
dirty = lambda: sorted([p.get_name() for p in S.get_dirty_content_packages()] + [p.get_name() for p in S.get_dirty_map_packages()])
res = {'mode': MODE, 'variant': VAR, 'started': time.strftime('%H:%M:%S'), 'problems': [], 'dirty_before': dirty()}
state_f = D / 'land_state.json'
weights = json.loads((D / ('weights_%s.json' % VAR)).read_text())


def finish(ok):
    res['ok'] = ok; res['finished'] = time.strftime('%H:%M:%S'); res['dirty_after'] = dirty()
    try: res['target_layers_after'] = [str(x) for x in land.get_target_layer_names(False)]
    except Exception as ex: res['target_layers_after'] = repr(ex)[:100]
    (D / ('land_%s_%s.json' % (MODE, VAR))).write_text(json.dumps(res, indent=1, default=str)); print('LAND_TRIAL', MODE, VAR, 'ok', ok, 'problems', res['problems'][:4])


if MODE == 'restore':
    st = json.loads(state_f.read_text()) if state_f.exists() else None
    if not st:
        res['problems'].append('no land_state.json (nothing applied?)'); finish(False)
    else:
        with u.ScopedEditorTransaction('PFR landscape restore (unsaved)'):
            land.set_editor_property('landscape_material', u.load_asset(st['material']))
            tl = land.get_editor_property('target_layers'); newtl = {}
            for nm, li in st['target_layers'].items():
                s = u.LandscapeTargetLayerSettings()
                if li: s.set_editor_property('layer_info_obj', u.load_asset(li))
                newtl[nm] = s
            land.set_editor_property('target_layers', newtl)
            try: land.delete_unused_layers()
            except Exception as ex: res['problems'].append('delete_unused_layers ' + repr(ex)[:100])
        res['restored_material'] = st['material']; state_f.unlink(); finish(not res['problems'])
else:
    # 0. record the original state once
    if not state_f.exists():
        tl0 = land.get_editor_property('target_layers'); orig = {}
        for k, v in tl0.items():
            li = v.get_editor_property('layer_info_obj'); orig[str(k)] = li.get_path_name().split('.')[0] if li else None
        state_f.write_text(json.dumps({'material': land.get_editor_property('landscape_material').get_path_name().split('.')[0], 'target_layers': orig}, indent=1))
    # 1. owned MI
    mi = u.load_asset(MI_PATH)
    if not mi:
        ok = u.EditorAssetLibrary.duplicate_asset(SRC_MI, MI_PATH); res['mi_created'] = bool(ok); mi = u.load_asset(MI_PATH)
    if not mi:
        res['problems'].append('MI not available'); finish(False); LAYERS = []
    # 2. material + 3. target layers
    with u.ScopedEditorTransaction('PFR landscape material + layers (unsaved)'):
        land.set_editor_property('landscape_material', mi)
        tl = land.get_editor_property('target_layers'); newtl = {}
        for k, v in tl.items():
            s = u.LandscapeTargetLayerSettings(); li = v.get_editor_property('layer_info_obj')
            if li: s.set_editor_property('layer_info_obj', li)
            newtl[str(k)] = s
        for nm in LAYERS + ['SandBeach']:
            s = u.LandscapeTargetLayerSettings(); lio = u.load_asset(LI % nm)
            if not lio: res['problems'].append('layer info missing ' + nm); continue
            s.set_editor_property('layer_info_obj', lio); newtl[nm] = s
        land.set_editor_property('target_layers', newtl)
    res['target_layers_set'] = [str(x) for x in land.get_target_layer_names(False)]
    missing = [nm for nm in LAYERS if nm not in res['target_layers_set']]
    if missing:
        res['problems'].append('layers not accepted as paint targets: %s' % missing); finish(False); LAYERS = []
    # 4. paint, one layer per tick sequence: draw PNG texture into an RGBA8 RT, verify, import
    q = {'i': 0, 'phase': 'draw', 't': time.monotonic(), 'imported': {}, 'tex': {}, 'rt': {}}
    for nm in LAYERS:
        tex = u.RenderingLibrary.import_file_as_texture2d(w, str(D / ('weight_%s_%s.png' % (nm, VAR))))
        if not tex: res['problems'].append('png import failed ' + nm); continue
        tex.set_editor_property('srgb', False); tex.set_editor_property('filter', u.TextureFilter.TF_NEAREST); tex.set_editor_property('compression_settings', u.TextureCompressionSettings.TC_GRAYSCALE)
        q['tex'][nm] = tex; q['rt'][nm] = u.RenderingLibrary.create_render_target2d(w, 1017, 1017, u.TextureRenderTargetFormat.RTF_RGBA8, u.LinearColor(0, 0, 0, 1), False, False)
    builtins.PFR_LAND_KEEP = q
    todo = [nm for nm in LAYERS if nm in q['tex']]

    def rd(rt, x, y):
        c = u.RenderingLibrary.read_render_target_raw_pixel(w, rt, x, y, False); return round(c.r)

    def tick(dt):
        try:
            now = time.monotonic()
            if q['i'] >= len(todo):
                # read-back check through the new API (final weight of each layer at the sample points)
                chk = {}
                for nm in todo:
                    rt2 = u.RenderingLibrary.create_render_target2d(w, 1017, 1017, u.TextureRenderTargetFormat.RTF_RGBA8, u.LinearColor(0, 0, 0, 1), False, False)
                    ok = land.render_weightmap(land.get_actor_transform(), u.Box2D(u.Vector2D(0, 0), u.Vector2D(0, 0)), nm, rt2)
                    chk[nm] = {'render_ok': bool(ok)}
                    q['rt']['chk_' + nm] = rt2
                res['readback'] = chk; q['chk'] = True; q['t'] = now; q['i'] += 1; return
            if q['i'] > len(todo):
                if now - q['t'] < 6: return
                for nm in todo:
                    rt2 = q['rt']['chk_' + nm]; sm = weights['samples'][nm][:12]
                    got = [(x, y, v, rd(rt2, x, y)) for x, y, v in sm]
                    res['readback'][nm]['samples'] = got; res['readback'][nm]['mismatch'] = sum(1 for g in got if abs(g[2] - g[3]) > 12)
                u.unregister_slate_post_tick_callback(builtins.PFR_LAND_H); finish(not res['problems']); return
            nm = todo[q['i']]; tex, rt = q['tex'][nm], q['rt'][nm]
            if q['phase'] == 'draw':
                canvas, size, ctx = u.RenderingLibrary.begin_draw_canvas_to_render_target(w, rt)
                canvas.draw_texture(tex, u.Vector2D(0, 0), u.Vector2D(1017, 1017), u.Vector2D(0, 0), u.Vector2D(1, 1), u.LinearColor(1, 1, 1, 1), u.BlendMode.BLEND_OPAQUE)
                u.RenderingLibrary.end_draw_canvas_to_render_target(w, ctx); q.update(phase='verify', t=now); return
            if q['phase'] == 'verify' and now - q['t'] > 0.5:
                bad = [(x, y, v, rd(rt, x, y)) for x, y, v in weights['samples'][nm] if abs(rd(rt, x, y) - v) > 2]
                if bad:
                    res['problems'].append('decode mismatch %s %d e.g. %s' % (nm, len(bad), bad[:3])); u.unregister_slate_post_tick_callback(builtins.PFR_LAND_H); finish(False); return
                with u.ScopedEditorTransaction('PFR paint %s (unsaved)' % nm):
                    ok = land.landscape_import_weightmap_from_render_target(rt, nm, 0)
                q['imported'][nm] = bool(ok); res['imported'] = dict(q['imported'])
                if not ok: res['problems'].append('import returned False for ' + nm)
                q.update(i=q['i'] + 1, phase='draw', t=now); return
        except Exception as ex:
            res['problems'].append(repr(ex)[:300]); u.unregister_slate_post_tick_callback(builtins.PFR_LAND_H); finish(False)

    builtins.PFR_LAND_H = u.register_slate_post_tick_callback(tick)
    print('LAND_TRIAL scheduled', MODE, VAR, 'layers', todo, 'targets', res['target_layers_set'])
