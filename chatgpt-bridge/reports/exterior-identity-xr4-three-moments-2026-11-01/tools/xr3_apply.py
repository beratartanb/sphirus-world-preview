"""xr3_apply.py (WRITE job under the map manifest; NEVER saves): identity pass on top of the applied XR2 variant, in memory, or restore.
builtins.XR3_MODE in {'dryrun', 'apply', 'restore'}; builtins.XR3_VARIANT (e.g. 'i1'). Reads design/id_<var>.json:
  foliage  [{mesh, cull, xf_after}]  per component (instance COUNT MAY CHANGE: species are thinned/removed inside the slice);
           restore writes the recon snapshot list back (Saved/Codex/ExteriorRedesign_20261031/recon/foliage.json)
  spawn    XR2-format actor records (+ optional 'mid': {'parent_mi': path, 'scalar': {}, 'vector': {}} -> a dynamic material instance on
           the spawned component, so vendor materials never change) and 'soft' (no collision) / 'camera_ignore'
  mats     {mi_path: {'scalar': {}, 'vector': {}, 'texture': {}}} parameter overrides on PROJECT-OWNED material instances (in memory);
           the original values are recorded to design/mat_backup_<var>.json on apply and written back on restore
restore also destroys every actor labelled XR3_*. Output: design/id_<mode>_<var>.json"""
import unreal as u, pathlib, json, time, builtins, math

PJ = pathlib.Path(u.Paths.project_dir()); D = PJ / 'Saved/Codex/ExteriorIdentity_XR3_20261031'; RC = PJ / 'Saved/Codex/ExteriorRedesign_20261031/recon'
MODE, VAR = builtins.XR3_MODE, getattr(builtins, 'XR3_VARIANT', 'i1')
assert MODE in ('dryrun', 'apply', 'restore')
E = u.get_editor_subsystem(u.UnrealEditorSubsystem); assert E.get_game_world() is None, 'PIE running'
A = u.get_editor_subsystem(u.EditorActorSubsystem); w = E.get_editor_world()
assert w.get_path_name().startswith('/Game/GraceRanger/Maps/L_GR_SphirusHouse.')
actors = A.get_all_level_actors(); ifas = [a for a in actors if a.get_class().get_name() == 'InstancedFoliageActor']
design = json.loads((D / 'design' / ('id_%s.json' % VAR)).read_text())
recon = {(r['mesh'], tuple(r['cull'])): r for r in json.loads((RC / 'foliage.json').read_text())}
reg = u.AssetRegistryHelpers.get_asset_registry(); FT_DIR = '/Game/GraceRanger/Environment/Exterior20260921/Foliage'
fts = [t for t in (ad.get_asset() for ad in reg.get_assets_by_path(FT_DIR, True)) if isinstance(t, u.FoliageType_InstancedStaticMesh)]
S = u.EditorLoadingAndSavingUtils
dirty = lambda: sorted([p.get_name() for p in S.get_dirty_content_packages()] + [p.get_name() for p in S.get_dirty_map_packages()])
xr3_actors = lambda: [a for a in A.get_all_level_actors() if a.get_actor_label().startswith(('XR3_', 'XR4_'))]
res = {'mode': MODE, 'variant': VAR, 'problems': [], 'foliage': [], 'dirty_before': dirty(), 'xr3_actors_before': len(xr3_actors())}


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
for ch in design.get('foliage', []):
    key = (ch['mesh'], tuple(ch['cull'])); cs = comp_for(*key)
    if len(cs) != 1:
        res['problems'].append('component not unique %s: %d' % (key[0], len(cs))); continue
    f = ft_of(cs[0])
    if len(f) != 1:
        res['problems'].append('foliage type not unique %s' % key[0]); continue
    todo.append((f[0], ch['xf_after'] if MODE != 'restore' else recon[key]['xf'], cs[0].get_instance_count(), key))
meshes = {}
if MODE != 'restore':
    if res['xr3_actors_before']:
        res['problems'].append('XR3_ actors already present (%d): restore first' % res['xr3_actors_before'])
    for sp in design.get('spawn', []):
        for p in (sp['mesh'], (sp.get('mid') or {}).get('parent_mi')):
            if p and p not in meshes:
                meshes[p] = u.load_asset(p)
                if not meshes[p]:
                    res['problems'].append('asset missing ' + p)
mats = {}
for mp in design.get('mats', {}):
    mi = u.load_asset(mp)
    if not isinstance(mi, u.MaterialInstanceConstant):
        res['problems'].append('not a material instance: ' + mp)
    elif not mp.startswith('/Game/GraceRanger/'):
        res['problems'].append('refusing to edit a non project-owned material: ' + mp)
    else:
        mats[mp] = mi
if res['problems']:
    (D / 'design' / ('id_%s_%s.json' % (MODE, VAR))).write_text(json.dumps(res, indent=1, default=str))
    raise RuntimeError('REFUSED before any change: %s' % res['problems'][:6])
ML = u.MaterialEditingLibrary


def mat_apply():
    bk_path = D / 'design' / ('mat_backup_%s.json' % VAR)
    if MODE == 'restore':
        if not bk_path.exists():
            res['mats'] = 'no backup -> nothing to restore'; return
        bk = json.loads(bk_path.read_text())
        for mp, rec in bk.items():
            mi = u.load_asset(mp)
            for k, v in rec.get('scalar', {}).items():
                ML.set_material_instance_scalar_parameter_value(mi, k, v)
            for k, v in rec.get('vector', {}).items():
                ML.set_material_instance_vector_parameter_value(mi, k, u.LinearColor(*v))
            for k, v in rec.get('texture', {}).items():
                ML.set_material_instance_texture_parameter_value(mi, k, u.load_asset(v) if v else None)
            ML.update_material_instance(mi)
        res['mats'] = 'restored %d' % len(bk); return
    bk = {}
    for mp, ov in design['mats'].items():
        mi = mats[mp]; rec = {'scalar': {}, 'vector': {}, 'texture': {}}
        for k, v in ov.get('scalar', {}).items():
            rec['scalar'][k] = ML.get_material_instance_scalar_parameter_value(mi, k)
            if MODE == 'apply': ML.set_material_instance_scalar_parameter_value(mi, k, float(v))
        for k, v in ov.get('vector', {}).items():
            c = ML.get_material_instance_vector_parameter_value(mi, k); rec['vector'][k] = [c.r, c.g, c.b, c.a]
            if MODE == 'apply': ML.set_material_instance_vector_parameter_value(mi, k, u.LinearColor(*v))
        for k, v in ov.get('texture', {}).items():
            t = ML.get_material_instance_texture_parameter_value(mi, k); rec['texture'][k] = t.get_path_name().split('.')[0] if t else None
            if MODE == 'apply': ML.set_material_instance_texture_parameter_value(mi, k, u.load_asset(v))
        if MODE == 'apply': ML.update_material_instance(mi)
        bk[mp] = rec
    if MODE == 'apply':
        bk_path.write_text(json.dumps(bk, indent=1))
    res['mats'] = {'edited' if MODE == 'apply' else 'would_edit': list(bk)}


def retint():
    """dynamic material instances on EXISTING XR2 structural actors (label prefix match); originals recorded for restore"""
    bk_path = D / 'design' / ('retint_backup_%s.json' % VAR); rules = design.get('retint', [])
    if MODE == 'restore':
        if not bk_path.exists():
            res['retint'] = 'no backup'; return
        bk = json.loads(bk_path.read_text()); byl = {a.get_actor_label(): a for a in A.get_all_level_actors()}; n = 0
        for lab, mats_ in bk.items():
            a = byl.get(lab)
            if not a: continue
            c = a.static_mesh_component
            for slot, mp in enumerate(mats_):
                c.set_material(slot, u.load_asset(mp) if mp else None); n += 1
        res['retint'] = 'restored %d slots' % n; return
    bk = {}; n = 0
    for a in A.get_all_level_actors():
        lab = a.get_actor_label(); rule = next((r for r in rules if lab.startswith(r['prefix'])), None)
        if not rule or not isinstance(a, u.StaticMeshActor): continue
        c = a.static_mesh_component; mats_ = c.get_materials(); bk[lab] = [m.get_path_name().split('.')[0] if m else None for m in mats_]
        if MODE == 'apply':
            for slot, m in enumerate(mats_):
                if not m: continue
                mid = c.create_dynamic_material_instance(slot, m)
                for k, v in rule['mid'].get('scalar', {}).items(): mid.set_scalar_parameter_value(k, float(v))
                for k, v in rule['mid'].get('vector', {}).items(): mid.set_vector_parameter_value(k, u.LinearColor(*v))
                n += 1
    if MODE == 'apply':
        bk_path.write_text(json.dumps(bk, indent=1))
    res['retint'] = {'actors': len(bk), 'slots': n}


def hide_actors():
    byl = {a.get_actor_label(): a for a in A.get_all_level_actors()}; n = 0
    for lab in design.get('hide', []):
        a = byl.get(lab)
        if not a: continue
        a.set_actor_hidden_in_game(MODE != 'restore'); a.set_is_temporarily_hidden_in_editor(MODE != 'restore'); n += 1
    res['hidden' if MODE != 'restore' else 'unhidden'] = n


def do_actors():
    hide_actors()
    if MODE == 'restore':
        gone = xr3_actors()
        for a in gone:
            A.destroy_actor(a)
        res['actors_destroyed'] = len(gone); return
    n = 0
    for sp in design.get('spawn', []):
        a = A.spawn_actor_from_class(u.StaticMeshActor, u.Vector(sp['x'], sp['y'], sp['z']), u.Rotator(pitch=sp.get('pitch', 0), yaw=sp['yaw'], roll=sp.get('roll', 0)))
        a.set_actor_scale3d(u.Vector(*sp['scale']))
        c = a.static_mesh_component; c.set_static_mesh(meshes[sp['mesh']]); c.set_editor_property('receives_decals', False)
        if sp.get('mid'):
            md = sp['mid']
            for slot in range(len(c.get_materials()) if hasattr(c, 'get_materials') else 1):
                mid = c.create_dynamic_material_instance(slot, meshes[md['parent_mi']] if md.get('parent_mi') else None)
                if mid:
                    for k, v in md.get('scalar', {}).items(): mid.set_scalar_parameter_value(k, float(v))
                    for k, v in md.get('vector', {}).items(): mid.set_vector_parameter_value(k, u.LinearColor(*v))
        if sp.get('soft'):
            c.set_collision_enabled(u.CollisionEnabled.NO_COLLISION)
        elif sp.get('camera_ignore', True):
            c.set_collision_response_to_channel(u.CollisionChannel.ECC_CAMERA, u.CollisionResponseType.ECR_IGNORE)
        if sp.get('no_shadow'):
            c.set_editor_property('cast_shadow', False)
        a.set_actor_label(sp['label']); a.set_folder_path('XR3_Identity/' + sp['kind']); n += 1
    res['actors_spawned'] = n


def done(ok):
    res['finished'] = time.strftime('%H:%M:%S'); res['ok'] = ok; res['dirty_after'] = dirty(); res['xr3_actors_after'] = len(xr3_actors())
    (D / 'design' / ('id_%s_%s.json' % (MODE, VAR))).write_text(json.dumps(res, indent=1, default=str))


try:
    if MODE == 'dryrun':
        mat_apply(); retint(); res['foliage'] = [{'mesh': k[0], 'n_now': n, 'n_after': len(xf)} for f, xf, n, k in todo]; res['spawn_n'] = len(design.get('spawn', [])); done(True)
    else:
        with u.ScopedEditorTransaction('XR3 identity %s %s (unsaved test)' % (MODE, VAR)):
            for f, xf, n0, key in todo:
                u.InstancedFoliageActor.remove_all_instances(w, f)
                u.InstancedFoliageActor.add_instances(w, f, [tf(x) for x in xf])
            do_actors(); mat_apply(); retint()
        for f, xf, n0, key in todo:
            cs = comp_for(*key); n1 = cs[0].get_instance_count() if len(cs) == 1 else -1
            res['foliage'].append({'mesh': key[0], 'n_before': n0, 'n_after': n1, 'n_wanted': len(xf)})
            if n1 != len(xf):
                res['problems'].append('count %s wanted %d got %d' % (key[0], len(xf), n1))
        done(not res['problems'])
except Exception as ex:
    res['problems'].append(repr(ex)); done(False)
print('XR3_APPLY', MODE, VAR, 'ok', res.get('ok'), 'problems', res['problems'][:3])
