"""xr5_mat_trial.py (write job, in-memory only, nothing saved): XR5 §7 material pass, items 1 (pond water) and 3 (broadleaf litter).
builtins.XR5_MAT = 'apply' | 'restore'.
 - water: project-owned MI_EX_Pond (parent M_PR_CalystoPhysicalInland) parameter overrides, backed up to design/xr5_mat_backup.json
   on first apply: roughness up (sheet -> skin), calm normal amplitude up (after-rain micro ripple), murkier and darker absorption
   (dark tea-coloured depth instead of a mirror), lower specular.
 - litter: every foliage component whose mesh is SM_DeadLeaves02 gets a MaterialInstanceDynamic of its vendor MI_DeadLeaves01 with a
   needle-brown tint and lower albedo (component material override only; the vendor MI and the foliage type are untouched).
 - rocks (item 2) are NOT here: the Big_Rock ledge belongs to the unsaved XR4 world layer.
Output: design/xr5_mat_<mode>.json"""
import unreal as u, json, builtins, pathlib, time

PJ = pathlib.Path(u.Paths.project_dir()); D = PJ / 'Saved/Codex/ExteriorIdentity_XR3_20261031/design'
MODE = builtins.XR5_MAT; assert MODE in ('apply', 'restore')
E = u.get_editor_subsystem(u.UnrealEditorSubsystem); assert E.get_game_world() is None, 'PIE running'
A = u.get_editor_subsystem(u.EditorActorSubsystem); ML = u.MaterialEditingLibrary
res = {'mode': MODE, 'problems': [], 'started': time.strftime('%H:%M:%S')}
POND = '/Game/GraceRanger/Environment/Exterior20260921/Materials/MI_EX_Pond'
WATER = {'scalars': {'Roughness': 0.45, 'Specular': 0.16, 'Murkiness': 5.5, 'Calm Normal Amplitude': 0.06}, 'vectors': {'Absorption': [0.20, 0.165, 0.12, 1.0]}}
LITTER_MESH = 'SM_DeadLeaves02'; LITTER = {'Color_Tint': [0.38, 0.30, 0.19, 1.0], 'Albedo_Brightness': 0.45}
bk_path = D / 'xr5_mat_backup.json'
mi = u.load_asset(POND); assert mi, POND

if MODE == 'apply':
    if not bk_path.exists():
        bk = {'scalars': {k: ML.get_material_instance_scalar_parameter_value(mi, k) for k in WATER['scalars']},
              'vectors': {k: [getattr(ML.get_material_instance_vector_parameter_value(mi, k), c) for c in 'rgba'] for k in WATER['vectors']}}
        bk_path.write_text(json.dumps(bk, indent=1))
    for k, v in WATER['scalars'].items(): ML.set_material_instance_scalar_parameter_value(mi, k, v)
    for k, v in WATER['vectors'].items(): ML.set_material_instance_vector_parameter_value(mi, k, u.LinearColor(*v))
    ML.update_material_instance(mi)
    res['water'] = WATER
    n = 0
    for a in A.get_all_level_actors():
        if a.get_class().get_name() != 'InstancedFoliageActor': continue
        for c in a.get_components_by_class(u.HierarchicalInstancedStaticMeshComponent):
            sm = c.get_editor_property('static_mesh')
            if not sm or sm.get_name() != LITTER_MESH: continue
            base = c.get_material(0)
            if base is None or isinstance(base, u.MaterialInstanceDynamic): continue
            mid = c.create_dynamic_material_instance(0, base)
            mid.set_vector_parameter_value('Color_Tint', u.LinearColor(*LITTER['Color_Tint'])); mid.set_scalar_parameter_value('Albedo_Brightness', LITTER['Albedo_Brightness'])
            n += c.get_instance_count()
    res['litter'] = {'mesh': LITTER_MESH, 'instances': n, 'params': LITTER}
else:
    bk = json.loads(bk_path.read_text())
    for k, v in bk['scalars'].items(): ML.set_material_instance_scalar_parameter_value(mi, k, v)
    for k, v in bk['vectors'].items(): ML.set_material_instance_vector_parameter_value(mi, k, u.LinearColor(*v))
    ML.update_material_instance(mi); res['water_restored'] = bk
    n = 0
    for a in A.get_all_level_actors():
        if a.get_class().get_name() != 'InstancedFoliageActor': continue
        for c in a.get_components_by_class(u.HierarchicalInstancedStaticMeshComponent):
            sm = c.get_editor_property('static_mesh')
            if not sm or sm.get_name() != LITTER_MESH: continue
            cur = c.get_material(0)
            if isinstance(cur, u.MaterialInstanceDynamic):
                c.set_material(0, cur.get_editor_property('parent')); n += c.get_instance_count()
    res['litter_restored_instances'] = n
S = u.EditorLoadingAndSavingUtils
res['dirty'] = sorted([p.get_name() for p in S.get_dirty_content_packages()] + [p.get_name() for p in S.get_dirty_map_packages()])
res['finished'] = time.strftime('%H:%M:%S')
(D / ('xr5_mat_%s.json' % MODE)).write_text(json.dumps(res, indent=1, default=str))
print('XR5_MAT', MODE, 'problems', res['problems'], 'litter', res.get('litter', res.get('litter_restored_instances')))
