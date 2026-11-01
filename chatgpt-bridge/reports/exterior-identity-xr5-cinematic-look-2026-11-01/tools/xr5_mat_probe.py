"""xr5_mat_probe.py (measure job, read-only): owners for the XR5 §7 material pass - pond water MI (parent, params, which actor uses it),
Big_Rock_01/02 and Middle_Rock materials (vendor MI -> params), the broadleaf litter / dead-leaves meshes in the foliage list and their
materials, plus every project-owned MI under Exterior20260921/Materials with its parent. Output: design/xr5_mat_probe.json"""
import unreal as u, json, pathlib

PJ = pathlib.Path(u.Paths.project_dir()); D = PJ / 'Saved/Codex/ExteriorIdentity_XR3_20261031/design'
AR = u.AssetRegistryHelpers.get_asset_registry(); A = u.get_editor_subsystem(u.EditorActorSubsystem)
out = {'pond': {}, 'rocks': {}, 'litter': {}, 'project_mis': {}, 'errors': []}


def mi_info(mi):
    try:
        d = {'path': mi.get_path_name(), 'class': mi.get_class().get_name()}
        if isinstance(mi, u.MaterialInstance):
            p = mi.get_editor_property('parent'); d['parent'] = p.get_path_name() if p else None
            d['scalars'] = {str(x.parameter_info.name): round(x.parameter_value, 4) for x in mi.get_editor_property('scalar_parameter_values')}
            d['vectors'] = {str(x.parameter_info.name): [round(x.parameter_value.r, 3), round(x.parameter_value.g, 3), round(x.parameter_value.b, 3), round(x.parameter_value.a, 3)] for x in mi.get_editor_property('vector_parameter_values')}
            d['textures'] = {str(x.parameter_info.name): (x.parameter_value.get_path_name() if x.parameter_value else None) for x in mi.get_editor_property('texture_parameter_values')}
            try:
                base = mi.get_base_material(); d['base'] = base.get_path_name()
                d['all_scalar_names'] = [str(n) for n in u.MaterialEditingLibrary.get_scalar_parameter_names(mi)][:60]
                d['all_vector_names'] = [str(n) for n in u.MaterialEditingLibrary.get_vector_parameter_names(mi)][:60]
            except Exception as ex: d['names_err'] = str(ex)[:120]
        return d
    except Exception as ex:
        return {'err': str(ex)[:160]}


# pond: actors whose materials include 'Pond' or 'Water'
for a in A.get_all_level_actors():
    try:
        for c in a.get_components_by_class(u.MeshComponent):
            for i, m in enumerate(c.get_materials()):
                if m and any(k in m.get_name() for k in ('Pond', 'Water', 'Lake')):
                    out['pond'].setdefault(m.get_path_name(), {'info': mi_info(m), 'users': []})['users'].append([a.get_actor_label(), c.get_name(), i, str(c.get_class().get_name())])
    except Exception as ex:
        out['errors'].append('pond %s %s' % (a.get_actor_label(), str(ex)[:80]))

# rocks + litter meshes: from the recon foliage list + spawned static meshes named Big_Rock / Middle_Rock
names = {}
for a in A.get_all_level_actors():
    try:
        for c in a.get_components_by_class(u.StaticMeshComponent):
            sm = c.get_editor_property('static_mesh')
            if sm and any(k in sm.get_name() for k in ('Big_Rock', 'Middle_Rock', 'DeadLeaves', 'Leaves', 'Litter')):
                names.setdefault(sm.get_path_name(), {'mats': [m.get_path_name() if m else None for m in c.get_materials()], 'users': 0})['users'] += 1
    except Exception: pass
fol = json.loads((PJ / 'Saved/Codex/ExteriorRedesign_20261031/recon/foliage.json').read_text())
for r in fol:
    if any(k in r['mesh'] for k in ('DeadLeaves', 'Leaves', 'Litter', 'Rock')):
        sm = u.load_asset(r['mesh'])
        if sm: names.setdefault(r['mesh'], {'mats': [ (sm.get_material(i).get_path_name() if sm.get_material(i) else None) for i in range(sm.get_num_sections(0))], 'users': 0})['users'] += len(r['xf'])
for k, v in names.items():
    v['mat_info'] = [mi_info(u.load_asset(m)) if m else None for m in v['mats']]
    (out['rocks'] if 'Rock' in k else out['litter'])[k] = v

# project MIs
for ad in AR.get_assets_by_path('/Game/GraceRanger/Environment/Exterior20260921/Materials', False):
    try:
        mi = ad.get_asset()
        if isinstance(mi, u.MaterialInstance):
            p = mi.get_editor_property('parent'); out['project_mis'][str(ad.asset_name)] = p.get_path_name() if p else None
    except Exception as ex: out['errors'].append(str(ex)[:80])
(D / 'xr5_mat_probe.json').write_text(json.dumps(out, indent=1, default=str))
print('XR5_MAT_PROBE pond', len(out['pond']), 'rocks', len(out['rocks']), 'litter', len(out['litter']), 'project MIs', len(out['project_mis']), 'errors', len(out['errors']))
