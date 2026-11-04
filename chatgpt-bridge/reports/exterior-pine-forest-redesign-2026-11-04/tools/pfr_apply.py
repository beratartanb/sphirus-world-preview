"""pfr_apply.py (WRITE job under the pfr_world manifest; NEVER saves): apply a Pine Forest redesign variant to the open production map
IN MEMORY, idempotently (every step writes absolute state), or restore the recon state.
builtins.PFR_MODE in {'dryrun', 'apply', 'restore'}; builtins.PFR_VARIANT (e.g. 'p1'); builtins.PFR_STEPS subset of
['terrain', 'landscape', 'foliage', 'newfol', 'actors', 'mats', 'look'] (default all).
  terrain    x9 heightmap (design plan 'file') -> RG16 PNG -> RGBA8 RT -> verified samples -> landscape_import_heightmap_from_render_target
             -> re-export + sample read-back (the proven XR2 route); restore = recon/height_now.u16 of this pass (== XR recon)
  landscape  owned MI_EX_PF_Landscape (duplicate of the PFP instance, created once) + target layer infos + weight import per layer
             (land_trial.py logic); restore = original material / target layers
  foliage    existing owned components: remove_all + add (absolute lists, counts may change); restore = recon foliage.json
  newfol     new owned FoliageType assets (created once with FoliageType_InstancedStaticMeshFactory, properties from the design) and
             their instances (remove_all + add); restore = remove_all
  actors     every PFR_* actor destroyed, then the design's actors spawned (collision rules as XR2/XR3; owned cliff MI on big masses;
             hidden list applied); restore = destroy PFR_*
  mats       owned MI parameter overrides (backup on first apply -> design/<v>/mat_backup.json); new owned MIs created from vendor
             instances with parameter overrides; restore = backup
  look       light / fog / atmosphere / PP owner values (backup on first apply -> design/<v>/look_backup.json); restore = backup
Output: design/<v>/apply_<mode>.json"""
import unreal as u, pathlib, json, time, builtins, array, random, math

PJ = pathlib.Path(u.Paths.project_dir()); ROOTD = PJ / 'Saved/Codex/PineForestRedesign_20261104'
MODE = getattr(builtins, 'PFR_MODE', 'dryrun'); VAR = getattr(builtins, 'PFR_VARIANT', 'p1'); D = ROOTD / 'design' / VAR
STEPS = list(getattr(builtins, 'PFR_STEPS', ['terrain', 'foliage', 'newfol', 'actors', 'mats', 'look']))   # 'landscape' (PFP paint layers) is blocked: TargetLayers is read-only in 5.8 Python
assert MODE in ('dryrun', 'apply', 'restore')
E = u.get_editor_subsystem(u.UnrealEditorSubsystem); assert E.get_game_world() is None, 'PIE running'
A = u.get_editor_subsystem(u.EditorActorSubsystem); w = E.get_editor_world()
assert w.get_path_name().startswith('/Game/GraceRanger/Maps/L_GR_SphirusHouse.'), w.get_path_name()
S = u.EditorLoadingAndSavingUtils; ML = u.MaterialEditingLibrary
dirty = lambda: sorted([p.get_name() for p in S.get_dirty_content_packages()] + [p.get_name() for p in S.get_dirty_map_packages()])
actors = A.get_all_level_actors(); land = next(a for a in actors if isinstance(a, u.Landscape))
ifas = [a for a in actors if a.get_class().get_name() == 'InstancedFoliageActor']
reg = u.AssetRegistryHelpers.get_asset_registry(); FT_DIR = '/Game/GraceRanger/Environment/Exterior20260921/Foliage'
MAT_DIR = '/Game/GraceRanger/Environment/Exterior20260921/Materials'
res = {'mode': MODE, 'variant': VAR, 'steps': STEPS, 'started': time.strftime('%H:%M:%S'), 'problems': [], 'dirty_before': dirty(), 'log': []}
plan = json.loads((D / ('plan_%s.json' % VAR)).read_text()) if MODE != 'restore' else None
recon_fol = {(r['mesh'], tuple(r['cull'])): r for r in json.loads((ROOTD / 'recon/foliage.json').read_text())}


def log(*a):
    res['log'].append(' '.join(str(x) for x in a)); print('PFR', *a)


def done(ok):
    res['ok'] = ok; res['finished'] = time.strftime('%H:%M:%S'); res['dirty_after'] = dirty()
    (D / ('apply_%s.json' % MODE)).write_text(json.dumps(res, indent=1, default=str)); print('PFR_APPLY', MODE, VAR, 'ok', ok, 'problems', res['problems'][:5])


def fts_owned():
    return [t for t in (ad.get_asset() for ad in reg.get_assets_by_path(FT_DIR, True)) if isinstance(t, u.FoliageType_InstancedStaticMesh)]


def comp_for(mesh, cull):
    out = []
    for a in ifas:
        for c in a.get_components_by_class(u.FoliageInstancedStaticMeshComponent):
            if c.static_mesh and c.static_mesh.get_path_name().split('.')[0] == mesh and [c.get_editor_property('instance_start_cull_distance'), c.get_editor_property('instance_end_cull_distance')] == list(cull):
                out.append(c)
    return out


def ft_of(c, fts):
    return [t for t in fts if t.get_editor_property('mesh') == c.static_mesh and t.get_editor_property('cull_distance').min == c.get_editor_property('instance_start_cull_distance')
            and t.get_editor_property('cull_distance').max == c.get_editor_property('instance_end_cull_distance')]


def tf(x):
    return u.Transform(location=u.Vector(x[0], x[1], x[2]), rotation=u.Rotator(pitch=x[3], yaw=x[4], roll=x[5]), scale=u.Vector(x[6], x[7], x[8]))


# ------------------------------------------------------------------ foliage (existing components)
def step_foliage():
    fts = fts_owned(); design = json.loads((D / ('foliage_%s.json' % VAR)).read_text()) if MODE != 'restore' else None
    items = design if MODE != 'restore' else [{'mesh': k[0], 'cull': list(k[1]), 'xf_after': r['xf']} for k, r in recon_fol.items()]
    n_ok = 0
    for ch in items:
        key = (ch['mesh'], tuple(ch['cull'])); cs = comp_for(*key)
        if len(cs) > 1:
            res['problems'].append('component not unique %s %s: %d' % (key[0].split('/')[-1], key[1], len(cs))); continue
        if not cs:
            # an emptied component is removed by the IFA (e.g. the firs after a previous apply): resolve the owned type by mesh + cull
            if not ch['xf_after']: n_ok += 1; continue
            f = [t for t in fts if t.get_editor_property('mesh') and t.get_editor_property('mesh').get_path_name().split('.')[0] == key[0]
                 and t.get_editor_property('cull_distance').min == key[1][0] and t.get_editor_property('cull_distance').max == key[1][1]]
        else:
            f = ft_of(cs[0], fts)
        if len(f) != 1:
            res['problems'].append('foliage type not unique %s (%d)' % (key[0].split('/')[-1], len(f))); continue
        if MODE == 'dryrun': n_ok += 1; continue
        u.InstancedFoliageActor.remove_all_instances(w, f[0])
        if ch['xf_after']: u.InstancedFoliageActor.add_instances(w, f[0], [tf(x) for x in ch['xf_after']])
        cs2 = comp_for(*key); n1 = cs2[0].get_instance_count() if len(cs2) == 1 else (0 if not cs2 else -1)
        if n1 != len(ch['xf_after']): res['problems'].append('count %s wanted %d got %d' % (key[0].split('/')[-1], len(ch['xf_after']), n1))
        n_ok += 1
    log('foliage components written', n_ok)


# ------------------------------------------------------------------ new foliage types + instances
def ensure_ft(name, spec):
    path = FT_DIR + '/' + name; ft = u.load_asset(path)
    if ft: return ft, False
    tools = u.AssetToolsHelpers.get_asset_tools(); ft = tools.create_asset(name, FT_DIR, u.FoliageType_InstancedStaticMesh, u.FoliageType_InstancedStaticMeshFactory())
    if not ft: return None, False
    tpl = u.load_asset(FT_DIR + '/FT_EX_PineTree01')
    m = u.load_asset(spec['mesh']); ft.set_editor_property('mesh', m)
    cd = u.Int32Interval(); cd.set_editor_property('min', int(spec['cull'][0])); cd.set_editor_property('max', int(spec['cull'][1])); ft.set_editor_property('cull_distance', cd)
    for k in ('scale_x', 'scale_y', 'scale_z'):
        iv = u.FloatInterval(); iv.set_editor_property('min', 1.0); iv.set_editor_property('max', 1.0); ft.set_editor_property(k, iv)
    ft.set_editor_property('scaling', u.FoliageScaling.UNIFORM); ft.set_editor_property('align_to_normal', bool(spec.get('align_to_normal', False)))
    ft.set_editor_property('random_yaw', bool(spec.get('random_yaw', True))); ft.set_editor_property('cast_shadow', bool(spec.get('cast_shadow', True)))
    for k, v in (('collision_with_world', False), ('enable_density_scaling', False), ('enable_cull_distance_scaling', False), ('affect_distance_field_lighting', False), ('enable_static_lighting', False)):
        try: ft.set_editor_property(k, v)
        except Exception: pass
    try:
        bi = ft.get_editor_property('body_instance'); bi.set_editor_property('collision_profile_name', 'BlockAll' if spec.get('collision') else 'NoCollision'); ft.set_editor_property('body_instance', bi)
    except Exception as ex:
        res['problems'].append('collision profile %s: %s' % (name, repr(ex)[:80]))
    try:
        ft.set_editor_property('mobility', tpl.get_editor_property('mobility')) if tpl else None
    except Exception: pass
    return ft, True


def step_newfol():
    design = json.loads((D / ('newfol_%s.json' % VAR)).read_text()) if MODE != 'restore' else None
    names = list(design) if design else [a.get_name() for a in (ad.get_asset() for ad in reg.get_assets_by_path(FT_DIR, True)) if a.get_name().startswith('FT_EX_PF_')]
    created = 0; written = {}
    for name in names:
        if MODE == 'restore':
            ft = u.load_asset(FT_DIR + '/' + name)
            if ft: u.InstancedFoliageActor.remove_all_instances(w, ft); written[name] = 0
            continue
        spec = design[name]
        if MODE == 'dryrun':
            written[name] = len(spec['xf']); continue
        ft, new = ensure_ft(name, spec)
        if not ft: res['problems'].append('FT create failed ' + name); continue
        created += int(new)
        if spec.get('materials') is not None:   # owned material instances on the owned type (vendor mesh / materials untouched)
            want = [u.load_asset(p) for p in spec['materials']]
            if any(m is None for m in want): res['problems'].append('override material missing ' + name)
            elif [m.get_path_name() for m in ft.get_editor_property('override_materials')] != [m.get_path_name() for m in want]:
                ft.set_editor_property('override_materials', want); res.setdefault('ft_materials_set', []).append(name)
        u.InstancedFoliageActor.remove_all_instances(w, ft)
        if spec['xf']: u.InstancedFoliageActor.add_instances(w, ft, [tf(x) for x in spec['xf']])
        written[name] = len(spec['xf'])
    res['newfol'] = {'created': created, 'written': written}; log('new foliage types', len(names), 'created', created, 'instances', sum(written.values()))


# ------------------------------------------------------------------ actors
def step_actors():
    byl = {a.get_actor_label(): a for a in A.get_all_level_actors()}
    gone = [a for lab, a in byl.items() if lab.startswith('PFR_') and not lab.startswith('PFR_Board')]
    if MODE != 'dryrun':
        for a in gone: A.destroy_actor(a)
    res['actors_destroyed'] = len(gone)
    if MODE == 'restore': return
    sp = json.loads((D / ('spawn_%s.json' % VAR)).read_text()); meshes = {}; n = 0
    for s in sp['spawn']:
        if s['mesh'] not in meshes:
            meshes[s['mesh']] = u.load_asset(s['mesh'])
            if not meshes[s['mesh']]: res['problems'].append('mesh missing ' + s['mesh'])
    if MODE == 'dryrun' or res['problems']:
        res['actors_planned'] = len(sp['spawn']); return
    cliff = {}
    for s in sp['spawn']:
        a = A.spawn_actor_from_class(u.StaticMeshActor, u.Vector(s['x'], s['y'], s['z']), u.Rotator(pitch=s.get('pitch', 0.0), yaw=s['yaw'], roll=s.get('roll', 0.0)))
        a.set_actor_scale3d(u.Vector(*s['scale'])); c = a.static_mesh_component; c.set_static_mesh(meshes[s['mesh']]); c.set_editor_property('receives_decals', False)
        if s.get('invisible'):
            a.set_actor_hidden_in_game(True); c.set_editor_property('cast_shadow', False); c.set_editor_property('visible', False)
            c.set_collision_enabled(u.CollisionEnabled.QUERY_AND_PHYSICS); c.set_collision_response_to_all_channels(u.CollisionResponseType.ECR_IGNORE)
            c.set_collision_response_to_channel(u.CollisionChannel.ECC_PAWN, u.CollisionResponseType.ECR_BLOCK)
        elif s.get('soft'):
            c.set_collision_enabled(u.CollisionEnabled.NO_COLLISION)
        elif s.get('camera_ignore', True):
            c.set_collision_response_to_channel(u.CollisionChannel.ECC_CAMERA, u.CollisionResponseType.ECR_IGNORE)
        if s.get('material'):
            mi = cliff.get(s['material']) or u.load_asset(s['material']); cliff[s['material']] = mi
            if mi:
                for slot in range(len(c.get_materials())): c.set_material(slot, mi)
        a.set_actor_label(s['label']); a.set_folder_path('PFR_World/' + s['kind']); n += 1
    byl = {a.get_actor_label(): a for a in A.get_all_level_actors()}; h = 0
    for lab in sp.get('hide', []):
        a = byl.get(lab)
        if a: a.set_actor_hidden_in_game(True); a.set_is_temporarily_hidden_in_editor(True); h += 1
    res['actors_spawned'] = n; res['actors_hidden'] = h; log('actors spawned', n, 'hidden', h)


# ------------------------------------------------------------------ materials
def set_params(mi, ov):
    for k, v in ov.get('scalar', {}).items(): ML.set_material_instance_scalar_parameter_value(mi, k, float(v))
    for k, v in ov.get('vector', {}).items(): ML.set_material_instance_vector_parameter_value(mi, k, u.LinearColor(*v))
    for k, v in ov.get('texture', {}).items(): ML.set_material_instance_texture_parameter_value(mi, k, u.load_asset(v) if v else None)
    ML.update_material_instance(mi)


def step_mats():
    bk_path = D / 'mat_backup.json'
    if MODE == 'restore':
        if not bk_path.exists(): res['mats'] = 'no backup'; return
        bk = json.loads(bk_path.read_text())
        for mp, rec in bk.items():
            mi = u.load_asset(mp)
            if mi: set_params(mi, rec)
        res['mats'] = 'restored %d' % len(bk); return
    design = json.loads((D / ('mats_%s.json' % VAR)).read_text()); bk = json.loads(bk_path.read_text()) if bk_path.exists() else {}
    for mp, ov in design['mats'].items():
        mi = u.load_asset(mp)
        if not isinstance(mi, u.MaterialInstanceConstant) or not mp.startswith('/Game/GraceRanger/'):
            res['problems'].append('refusing material ' + mp); continue
        if mp not in bk:
            rec = {'scalar': {}, 'vector': {}, 'texture': {}}
            for k in ov.get('scalar', {}): rec['scalar'][k] = ML.get_material_instance_scalar_parameter_value(mi, k)
            for k in ov.get('vector', {}): c = ML.get_material_instance_vector_parameter_value(mi, k); rec['vector'][k] = [c.r, c.g, c.b, c.a]
            for k in ov.get('texture', {}): t = ML.get_material_instance_texture_parameter_value(mi, k); rec['texture'][k] = t.get_path_name().split('.')[0] if t else None
            bk[mp] = rec
        if MODE == 'apply': set_params(mi, ov)
    if MODE == 'apply': bk_path.write_text(json.dumps(bk, indent=1))
    made = []
    for mp, ov in design.get('newmats', {}).items():
        if MODE != 'apply': continue
        mi = u.load_asset(mp)
        if not mi:
            ok = u.EditorAssetLibrary.duplicate_asset(ov['parent_of'], mp); mi = u.load_asset(mp); made.append(mp.split('/')[-1])
        if not mi: res['problems'].append('new MI failed ' + mp); continue
        set_params(mi, ov)
    res['mats'] = {'edited': list(design['mats']), 'created': made}; log('materials', res['mats'])


# ------------------------------------------------------------------ look
LIGHT_OWNERS = {'sun': 'EX_PostRain_Sun', 'sky': 'EX_PostRain_Sky', 'fog': 'EX_PostRain_Humidity', 'atmos': 'EX_PostRain_Atmosphere', 'pp': 'EX_PostRain_NeutralExposure'}


def comp_of(a):
    if isinstance(a, u.DirectionalLight): return a.get_component_by_class(u.DirectionalLightComponent)
    if isinstance(a, u.SkyLight): return a.get_component_by_class(u.SkyLightComponent)
    if isinstance(a, u.ExponentialHeightFog): return a.get_component_by_class(u.ExponentialHeightFogComponent)
    if isinstance(a, u.SkyAtmosphere): return a.get_component_by_class(u.SkyAtmosphereComponent)
    return None


def look_get(a, k):
    if k == 'rot': r = a.get_actor_rotation(); return [r.pitch, r.yaw]
    if isinstance(a, u.PostProcessVolume):
        s = a.get_editor_property('settings'); v = s.get_editor_property(k)
        return [round(x, 4) for x in v.to_tuple()] if hasattr(v, 'to_tuple') else v
    v = comp_of(a).get_editor_property(k)
    return [round(x, 4) for x in v.to_tuple()] if hasattr(v, 'to_tuple') else v


def look_set(a, k, v):
    if k == 'rot': a.set_actor_rotation(u.Rotator(pitch=v[0], yaw=v[1], roll=0.0), False); return
    if isinstance(a, u.PostProcessVolume):
        s = a.get_editor_property('settings')
        if isinstance(v, list) and len(v) == 4: v = u.Vector4(*v)
        s.set_editor_property(k, v); s.set_editor_property('override_' + k, True); a.set_editor_property('settings', s); return
    c = comp_of(a)
    if isinstance(v, list) and k == 'volumetric_fog_albedo': v = u.Color(int(v[0]), int(v[1]), int(v[2]), 255)   # FColor (backup stores 4 ints)
    elif isinstance(v, list) and len(v) == 3: v = u.LinearColor(v[0], v[1], v[2], 1.0)
    elif isinstance(v, list) and len(v) == 4: v = u.LinearColor(*v)
    c.set_editor_property(k, v)


def step_look():
    bk_path = D / 'look_backup.json'; byl = {a.get_actor_label(): a for a in A.get_all_level_actors()}
    orig = ROOTD / 'design' / 'look_backup_original.json'   # the pre-pass (XR5 FINAL v2) values, written once by the first apply; restore always uses it
    if MODE == 'restore':
        src = orig if orig.exists() else bk_path
        if not src.exists(): res['look'] = 'no backup'; return
        bk = json.loads(src.read_text()); res['look_source'] = str(src.name)
        for own, vals in bk.items():
            a = byl.get(LIGHT_OWNERS[own])
            for k, v in vals.items():
                try: look_set(a, k, v)
                except Exception as ex: res['problems'].append('look restore %s.%s %s' % (own, k, repr(ex)[:60]))
        res['look'] = 'restored'; return
    design = json.loads((D / ('look_%s.json' % VAR)).read_text()); bk = json.loads(bk_path.read_text()) if bk_path.exists() else {}
    for own, vals in design.items():
        a = byl.get(LIGHT_OWNERS[own])
        if not a: res['problems'].append('light owner missing ' + own); continue
        bk.setdefault(own, {})
        for k, v in vals.items():
            if k not in bk[own]:
                try: bk[own][k] = look_get(a, k)
                except Exception as ex: res['problems'].append('look read %s.%s %s' % (own, k, repr(ex)[:60])); continue
            if MODE == 'apply':
                try: look_set(a, k, v)
                except Exception as ex: res['problems'].append('look set %s.%s %s' % (own, k, repr(ex)[:60]))
    if MODE == 'apply':
        bk_path.write_text(json.dumps(bk, indent=1, default=str))
        if not orig.exists(): orig.write_text(json.dumps(bk, indent=1, default=str))
    res['look'] = 'applied' if MODE == 'apply' else 'dryrun'; log('look', res['look'])


# ------------------------------------------------------------------ landscape material + weights (land_trial logic, inline)
MI_PATH = MAT_DIR + '/MI_EX_PF_Landscape'; SRC_MI = '/Game/PineForestPack/Materials/Landscape/Instances/MI_LandscapePineForest'
LI = '/Game/PineForestPack/Materials/Landscape/LandscapeLayers/LL_%s_LayerInfo'; LAYERS = ['Forest', 'Ground', 'GroundPath', 'ForestField', 'WetPuddle']
state_f = ROOTD / 'design/land_state.json'


def landscape_prepare():
    """material + target layers (sync part); returns the list of layers to paint"""
    if MODE == 'restore':
        if not state_f.exists(): res['landscape'] = 'nothing to restore'; return []
        st = json.loads(state_f.read_text())
        land.set_editor_property('landscape_material', u.load_asset(st['material'])); newtl = {}
        for nm, li in st['target_layers'].items():
            s = u.LandscapeTargetLayerSettings()
            if li: s.set_editor_property('layer_info_obj', u.load_asset(li))
            newtl[nm] = s
        land.set_editor_property('target_layers', newtl)
        try: land.delete_unused_layers()
        except Exception as ex: res['problems'].append('delete_unused_layers ' + repr(ex)[:80])
        state_f.unlink(); res['landscape'] = 'restored ' + st['material']; return []
    if not state_f.exists():
        tl0 = land.get_editor_property('target_layers'); orig = {}
        for k, v in tl0.items():
            li = v.get_editor_property('layer_info_obj'); orig[str(k)] = li.get_path_name().split('.')[0] if li else None
        state_f.write_text(json.dumps({'material': land.get_editor_property('landscape_material').get_path_name().split('.')[0], 'target_layers': orig}, indent=1))
    if MODE == 'dryrun': return []
    mi = u.load_asset(MI_PATH)
    if not mi:
        u.EditorAssetLibrary.duplicate_asset(SRC_MI, MI_PATH); mi = u.load_asset(MI_PATH)
    if not mi: res['problems'].append('landscape MI unavailable'); return []
    land.set_editor_property('landscape_material', mi)
    tl = land.get_editor_property('target_layers'); newtl = {}
    for k, v in tl.items():
        s = u.LandscapeTargetLayerSettings(); li = v.get_editor_property('layer_info_obj')
        if li: s.set_editor_property('layer_info_obj', li)
        newtl[str(k)] = s
    for nm in LAYERS + ['SandBeach']:
        s = u.LandscapeTargetLayerSettings(); lio = u.load_asset(LI % nm)
        if lio: s.set_editor_property('layer_info_obj', lio); newtl[nm] = s
    land.set_editor_property('target_layers', newtl)
    names = [str(x) for x in land.get_target_layer_names(False)]; res['landscape'] = {'targets': names}
    missing = [nm for nm in LAYERS if nm not in names]
    if missing: res['problems'].append('paint targets missing %s' % missing); return []
    return LAYERS


# ------------------------------------------------------------------ orchestration (tick-driven for render-target work)
Q = {'phase': 'start', 't': time.monotonic(), 'paint': [], 'pi': 0}
builtins.PFR_KEEP = Q


def rd(rt, x, y):
    return round(u.RenderingLibrary.read_render_target_raw_pixel(w, rt, x, y, False).r)


def rg(rt, x, y):
    c = u.RenderingLibrary.read_render_target_raw_pixel(w, rt, x, y, False); return round(c.r) * 256 + round(c.g)


def sync_steps():
    with u.ScopedEditorTransaction('PFR %s %s (unsaved)' % (MODE, VAR)):
        if 'foliage' in STEPS: step_foliage()
        if 'newfol' in STEPS: step_newfol()
        if 'mats' in STEPS: step_mats()        # before actors: the owned cliff MI must exist when the blocks are spawned
        if 'actors' in STEPS: step_actors()
        if 'look' in STEPS: step_look()


PREPARED = True   # never raise SystemExit inside a runner job: it wedges the gated runner (XR3 lesson, re-learned 2026-11-04)
try:
    # asset CREATION must happen in the synchronous job body: the runner's write guard (manifest) is active only there; the tick phase
    # runs as 'control' and refuses duplicate_asset (2026-11-04 22:31). FoliageType assets go through AssetTools (not guarded) but are
    # created here as well so that every new package is audited by G5 at job end.
    if MODE == 'apply':
        if 'mats' in STEPS:
            dm_ = json.loads((D / ('mats_%s.json' % VAR)).read_text())
            for mp, ov in dm_.get('newmats', {}).items():
                if not u.load_asset(mp):
                    ok = u.EditorAssetLibrary.duplicate_asset(ov['parent_of'], mp); res.setdefault('newmats_created', []).append([mp.split('/')[-1], bool(ok)])
            for tp, ov in dm_.get('newtex', {}).items():   # owned texture copies capped in size (streaming budget)
                t = u.load_asset(tp)
                if not t:
                    ok = u.EditorAssetLibrary.duplicate_asset(ov['source'], tp); t = u.load_asset(tp); res.setdefault('newtex_created', []).append([tp.split('/')[-1], bool(ok)])
                if t and ov.get('max_size') and t.get_editor_property('max_texture_size') != ov['max_size']:
                    t.set_editor_property('max_texture_size', int(ov['max_size']))
        if 'newfol' in STEPS:
            nf_ = json.loads((D / ('newfol_%s.json' % VAR)).read_text()); made = 0
            for name, spec in nf_.items():
                ft, new = ensure_ft(name, spec); made += int(new)
            res['newfol_assets_created_sync'] = made
    # terrain inputs
    if 'terrain' in STEPS and MODE != 'dryrun':
        if MODE == 'restore':
            Hbuf = array.array('H'); Hbuf.frombytes((ROOTD / 'recon/height_now.u16').read_bytes()); rr = random.Random(7)
            Q['hsamples'] = [{'x': x, 'y': y, 'height': Hbuf[y * 1017 + x]} for x, y in ((rr.randrange(300, 700), rr.randrange(300, 700)) for _ in range(60))]
            # restore source PNG: the ExteriorRedesign recon height_before.png (same data as recon/height_now.u16, verified sha1)
            Q['hpng'] = str(PJ / 'Saved/Codex/ExteriorRedesign_20261031/design/height_before.png')
        else:
            Q['hsamples'] = plan['samples']; Q['hpng'] = str(PJ / plan['file'])
        tex = u.RenderingLibrary.import_file_as_texture2d(w, Q['hpng']); tex.set_editor_property('srgb', False); tex.set_editor_property('filter', u.TextureFilter.TF_NEAREST); tex.set_editor_property('compression_settings', u.TextureCompressionSettings.TC_VECTOR_DISPLACEMENTMAP)
        Q['htex'] = tex; Q['hrt'] = u.RenderingLibrary.create_render_target2d(w, 1017, 1017, u.TextureRenderTargetFormat.RTF_RGBA8, u.LinearColor(0, 0, 0, 1), False, False)
    if 'landscape' in STEPS:
        Q['paint'] = landscape_prepare()
        weights = json.loads((ROOTD / 'design' / ('weights_%s.json' % VAR)).read_text()) if Q['paint'] else None
        Q['wsamples'] = weights['samples'] if weights else {}
        Q['wtex'] = {}; Q['wrt'] = {}
        for nm in Q['paint']:
            t = u.RenderingLibrary.import_file_as_texture2d(w, str(ROOTD / 'design' / ('weight_%s_%s.png' % (nm, VAR))))
            t.set_editor_property('srgb', False); t.set_editor_property('filter', u.TextureFilter.TF_NEAREST); t.set_editor_property('compression_settings', u.TextureCompressionSettings.TC_GRAYSCALE)
            Q['wtex'][nm] = t; Q['wrt'][nm] = u.RenderingLibrary.create_render_target2d(w, 1017, 1017, u.TextureRenderTargetFormat.RTF_RGBA8, u.LinearColor(0, 0, 0, 1), False, False)
    if MODE == 'dryrun':
        sync_steps(); done(not res['problems']); PREPARED = False
except Exception as ex:
    res['problems'].append('prepare ' + repr(ex)[:300]); done(False); PREPARED = False


def tick(dt):
    try:
        now = time.monotonic()
        if now - Q['t'] < 1.5: return
        ph = Q['phase']
        if ph == 'start':
            Q['phase'] = 'h_draw' if ('terrain' in STEPS) else ('w_draw' if Q['paint'] else 'sync'); Q['t'] = now; return
        if ph == 'h_draw':
            canvas, size, ctx = u.RenderingLibrary.begin_draw_canvas_to_render_target(w, Q['hrt'])
            canvas.draw_texture(Q['htex'], u.Vector2D(0, 0), u.Vector2D(1017, 1017), u.Vector2D(0, 0), u.Vector2D(1, 1), u.LinearColor(1, 1, 1, 1), u.BlendMode.BLEND_OPAQUE)
            u.RenderingLibrary.end_draw_canvas_to_render_target(w, ctx); Q.update(phase='h_verify', t=now); return
        if ph == 'h_verify':
            bad = [(s, rg(Q['hrt'], s['x'], s['y'])) for s in Q['hsamples'] if rg(Q['hrt'], s['x'], s['y']) != s['height']]
            if bad: res['problems'].append('height decode mismatch %d' % len(bad)); return finish_now(False)
            with u.ScopedEditorTransaction('PFR heightmap %s (unsaved)' % MODE):
                land.modify(); assert land.landscape_import_heightmap_from_render_target(Q['hrt'], True, 0)
            Q['hrt2'] = u.RenderingLibrary.create_render_target2d(w, 1017, 1017, u.TextureRenderTargetFormat.RTF_RGBA32F, u.LinearColor(0, 0, 0, 1), False, False); Q.update(phase='h_export', t=now); return
        if ph == 'h_export':
            assert land.landscape_export_heightmap_to_render_target(Q['hrt2'], False, True); Q.update(phase='h_read', t=now, tries=0); return
        if ph == 'h_read':
            if now - Q['t'] < 20: return
            got = [(s, round(u.RenderingLibrary.read_render_target_raw_pixel(w, Q['hrt2'], s['x'], s['y'], False).r)) for s in Q['hsamples']]
            if all(g[1] == 0 for g in got) and Q.get('tries', 0) < 4:
                Q['tries'] = Q.get('tries', 0) + 1; res['height_readback_retries'] = Q['tries']; Q.update(phase='h_export', t=now); return
            mism = [g for g in got if abs(g[1] - g[0]['height']) > 1]; res['height_readback_mismatch'] = len(mism)
            if mism: res['problems'].append('height readback mismatch %d' % len(mism)); return finish_now(False)
            log('terrain written and verified'); Q.update(phase='w_draw' if Q['paint'] else 'sync', t=now); return
        if ph == 'w_draw':
            if Q['pi'] >= len(Q['paint']): Q.update(phase='w_check', t=now); return
            nm = Q['paint'][Q['pi']]; canvas, size, ctx = u.RenderingLibrary.begin_draw_canvas_to_render_target(w, Q['wrt'][nm])
            canvas.draw_texture(Q['wtex'][nm], u.Vector2D(0, 0), u.Vector2D(1017, 1017), u.Vector2D(0, 0), u.Vector2D(1, 1), u.LinearColor(1, 1, 1, 1), u.BlendMode.BLEND_OPAQUE)
            u.RenderingLibrary.end_draw_canvas_to_render_target(w, ctx); Q.update(phase='w_import', t=now); return
        if ph == 'w_import':
            nm = Q['paint'][Q['pi']]; rt = Q['wrt'][nm]
            bad = [(x, y, v, rd(rt, x, y)) for x, y, v in Q['wsamples'][nm] if abs(rd(rt, x, y) - v) > 2]
            if bad: res['problems'].append('weight decode mismatch %s %d' % (nm, len(bad))); return finish_now(False)
            with u.ScopedEditorTransaction('PFR paint %s (unsaved)' % nm):
                ok = land.landscape_import_weightmap_from_render_target(rt, nm, 0)
            res.setdefault('weights_imported', {})[nm] = bool(ok)
            if not ok: res['problems'].append('weight import False ' + nm)
            Q.update(pi=Q['pi'] + 1, phase='w_draw', t=now); return
        if ph == 'w_check':
            chk = {}
            for nm in Q['paint']:
                rt2 = u.RenderingLibrary.create_render_target2d(w, 1017, 1017, u.TextureRenderTargetFormat.RTF_RGBA8, u.LinearColor(0, 0, 0, 1), False, False)
                ok = land.render_weightmap(land.get_actor_transform(), u.Box2D(u.Vector2D(0, 0), u.Vector2D(0, 0)), nm, rt2); chk[nm] = {'render_ok': bool(ok)}; Q['wrt']['chk_' + nm] = rt2
            res['weights_readback'] = chk; Q.update(phase='w_check2', t=now); return
        if ph == 'w_check2':
            if now - Q['t'] < 6: return
            for nm in Q['paint']:
                rt2 = Q['wrt']['chk_' + nm]; got = [(x, y, v, rd(rt2, x, y)) for x, y, v in Q['wsamples'][nm][:12]]
                res['weights_readback'][nm].update(samples=got, mismatch=sum(1 for g in got if abs(g[2] - g[3]) > 14))
            log('weights', json.dumps({k: (v['render_ok'], v.get('mismatch')) for k, v in res['weights_readback'].items()})); Q.update(phase='sync', t=now); return
        if ph == 'sync':
            sync_steps(); return finish_now(not res['problems'])
    except Exception as ex:
        res['problems'].append(repr(ex)[:300]); finish_now(False)


def finish_now(ok):
    try: u.unregister_slate_post_tick_callback(builtins.PFR_AH)
    except Exception: pass
    done(ok)


if PREPARED:
    builtins.PFR_AH = u.register_slate_post_tick_callback(tick)
    print('PFR_APPLY scheduled', MODE, VAR, STEPS, 'paint', Q['paint'])
else:
    print('PFR_APPLY finished synchronously', MODE, VAR, 'ok', res.get('ok'))
