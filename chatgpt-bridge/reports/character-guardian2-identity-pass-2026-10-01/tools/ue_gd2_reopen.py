"""GUARDIAN-2 pass save/reopen verification (builtins.GD2_RO = {face, hair, skin}) (FRESH editor, before any QA scene): loads the final candidate from disk (face H + skin c14s,
brows / lashes, hair id18 + bindings, Henley g17e, Chaos shorts m1, body MI t1) and checks morphs / LODs / slots / groom LOD mode / cloth.
Read-only. Writes Saved/Codex/CharacterGuardian2_20261001/reopen_check.json"""
import unreal as u, pathlib, json, builtins
RO = getattr(builtins, 'GD2_RO', {'face': 'p', 'hair': 'id20', 'skin': 'c16'})
R = pathlib.Path(u.Paths.project_dir()).resolve(); O = R/'Saved/Codex/CharacterGuardian2_20261001/reopen_check.json'
GD = '/Game/Sphirus/CharacterLab/CharacterGuardian_20261001'; G = '/Game/Sphirus/CharacterLab/CharacterGuardian2_20261001'; CR = '/Game/Sphirus/CharacterLab/CharacterCorrective_20261001'; ME = u.MaterialEditingLibrary
out = {'dirty_before': [p.get_path_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]}
sme = u.get_editor_subsystem(u.SkeletalMeshEditorSubsystem)
def mesh_info(path):
    m = u.load_asset(path); d = {'loaded': m is not None}
    if not m: return d
    names = [x.get_name() for x in m.get_editor_property('morph_targets')]
    d['morph_total'] = len(names); d['rv_morphs'] = len([n for n in names if n.startswith('RV_')]); d['br_neutral'] = 'BR_Neutral' in names
    d['lod_verts'] = [sme.get_num_verts(m, i) for i in range(sme.get_lod_count(m))]
    d['materials'] = [x.get_editor_property('material_interface').get_name() if x.get_editor_property('material_interface') else None for x in m.get_editor_property('materials')]
    d['post_process_abp'] = m.post_process_anim_blueprint.get_path_name().split('/')[-1] if m.post_process_anim_blueprint else None; return d
out['face_'+RO['face']] = mesh_info(G+'/Face/SKM_GD_FaceMesh_'+RO['face']); out['henley_g17e'] = mesh_info(GD+'/Outfit/SKM_LK_Henley_g17e'); out['shorts_g16c'] = mesh_info(CR+'/Outfit/SKM_LK_Shorts_g16c')
H = {}
for part in ('Main', 'Loose'):
    g = u.load_asset(f"{G}/Hair/GR_LK_Hair_{part}_{RO['hair']}"); H[part] = {'loaded': g is not None}
    if g: H[part]['lod_mode'] = str(g.get_editor_property('lod_mode')); H[part]['lods'] = len(g.get_editor_property('hair_groups_lod')[0].get_editor_property('lods'))
for b in ('HairMain_'+RO['face'], 'HairLoose_'+RO['face'], 'EyebrowsM_SlightArch_'+RO['face'], 'EyelashesS_Thin_'+RO['face']):
    bd = u.load_asset(f'{G}/Face/Bindings/GB_GD_{b}'); H['GB_GD_'+b] = {'loaded': bd is not None}
    if bd: H['GB_GD_'+b].update({'groom': bd.get_editor_property('groom').get_name(), 'target': bd.get_editor_property('target_skeletal_mesh').get_name()})
out['grooms'] = H
ca = u.load_asset(CR+'/Cloth/CA_CR_Shorts_m1'); out['cloth'] = {'loaded': ca is not None, 'pa': ca.get_editor_property('physics_asset').get_name() if ca else None, 'materials': [m.get_editor_property('material_interface').get_name() for m in ca.get_editor_property('materials')] if ca else None}
MI = {}
for p in (G+'/Skin/MI_LK_Face_LOD0_VT_g2'+RO['skin'], G+'/Skin/MI_LK_Face_LOD1_VT_g2'+RO['skin'], GD+'/Skin/MI_GD_Body_t1', G+'/Face/Diagnostics/AS_GD2_RefExpression'):
    m = u.load_asset(p); r = {'loaded': m is not None}
    if m:
        if 'AS_' in p: MI[p.split('/')[-1]] = r; continue
        r['parent'] = m.get_editor_property('parent').get_name(); v = ME.get_material_instance_vector_parameter_value(m, 'Basecolor Global Multiply Post-Bake'); r['tint'] = [round(v.r, 3), round(v.g, 3), round(v.b, 3)]
        if 'Face' in p: r['bc'] = ME.get_material_instance_texture_parameter_value(m, 'Basecolor Baked VT').get_name()
    MI[p.split('/')[-1]] = r
out['materials'] = MI
out['dirty_after'] = [p.get_path_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
O.write_text(json.dumps(out, indent=1)); print('GD_REOPEN', json.dumps(out)[:2500])
