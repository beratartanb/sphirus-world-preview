"""FACE-MATCH save/reopen verification (FRESH editor after restart, before any QA scene): every face-match candidate asset loaded
from disk and checked. Read-only (nothing saved). Writes Saved/Codex/CharacterIdentity_20260930/reopen_check.json."""
import unreal as u, pathlib, json
R = pathlib.Path(u.Paths.project_dir()).resolve(); O = R/'Saved/Codex/CharacterIdentity_20260930/reopen_check.json'
F = '/Game/Sphirus/CharacterLab/CharacterLookdev_20260930'; RVF = '/Game/Sphirus/CharacterLab/CharacterRevision_20260930'; EAL = u.EditorAssetLibrary; ME = u.MaterialEditingLibrary
HT, FS, SK, BM = 'id16d', 'c', 'c9', 'MI_LK_Body_Baked_G'
out = {'dirty_before': [p.get_path_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]}
sme = u.get_editor_subsystem(u.SkeletalMeshEditorSubsystem)
def mesh_info(path):
    m = u.load_asset(path); d = {'loaded': m is not None}
    if not m: return d
    names = [x.get_name() for x in m.get_editor_property('morph_targets')]
    d['morph_total'] = len(names); d['has_BR_Neutral'] = 'BR_Neutral' in names
    n = sme.get_lod_count(m); d['lod_verts'] = [sme.get_num_verts(m, i) for i in range(n)]
    d['skeleton'] = m.skeleton.get_path_name(); d['post_process_abp'] = m.post_process_anim_blueprint.get_path_name() if m.post_process_anim_blueprint else None
    d['materials'] = len(m.get_editor_property('materials')); return d
IDF = '/Game/Sphirus/CharacterLab/CharacterIdentity_20260930'; out['face_candidate'] = mesh_info(IDF+f'/Face/SKM_ID_FaceMesh_{FS}'); out['face_rv_source'] = mesh_info(RVF+'/Body/SKM_RV_FaceMesh')
fc, fr = out['face_candidate'], out['face_rv_source']
out['face_vs_source'] = {'same_lod_verts': fc.get('lod_verts') == fr.get('lod_verts'), 'same_morph_count': fc.get('morph_total') == fr.get('morph_total'),
                         'same_skeleton': fc.get('skeleton') == fr.get('skeleton'), 'same_pp_abp': fc.get('post_process_abp') == fr.get('post_process_abp')}
# BR_Neutral delta magnitude per LOD (the likeness bake) read back from disk: base mesh vs base+morph through GeometryScript
q = u.GeometryScript_MeshQueries
def lod_positions(m, L, morph=None):
    dm = u.DynamicMesh(); lod = u.GeometryScriptMeshReadLOD(); lod.lod_type = u.GeometryScriptLODType.SOURCE_MODEL; lod.lod_index = L
    r = u.GeometryScript_AssetUtils.copy_mesh_from_skeletal_mesh(m, dm, u.GeometryScriptCopyMeshFromAssetOptions(), lod)
    return dm if 'SUCCESS' in str(r[-1]) else None
def pick(r, typ):
    r = r if isinstance(r, tuple) else (r,); return [x for x in r if isinstance(x, typ)][0]
def verts(dm): return u.GeometryScript_List.convert_vector_list_to_array(pick(q.get_all_vertex_positions(dm, False), u.GeometryScriptVectorList))
mc = u.load_asset(IDF+f'/Face/SKM_ID_FaceMesh_{FS}'); mr = u.load_asset(RVF+'/Body/SKM_RV_FaceMesh'); base = {}
for L in range(sme.get_lod_count(mc)):
    a, b = lod_positions(mc, L), lod_positions(mr, L)
    if a and b:
        pa, pb = verts(a), verts(b)
        base[L] = max((abs(x.x-y.x)+abs(x.y-y.y)+abs(x.z-y.z)) for x, y in zip(pa, pb)) if len(pa) == len(pb) else 'count_mismatch'
out['base_geometry_diff_vs_source_cm'] = base   # must be 0: the likeness lives only in the BR_Neutral morph
G = {}
for part in ('Main', 'Loose'):
    g = u.load_asset(f'{F}/Hair/GR_LK_Hair_{part}_{HT}'); gi = {'loaded': g is not None}
    if g:
        gi['lod_mode'] = str(g.get_editor_property('lod_mode')); gi['lods'] = len(g.get_editor_property('hair_groups_lod')[0].get_editor_property('lods')) if g.get_editor_property('hair_groups_lod') else 0
        gi['sim'] = [p.get_editor_property('solver_settings').get_editor_property('enable_simulation') for p in g.get_editor_property('hair_groups_physics')]
        gi['materials'] = [s.get_editor_property('material').get_path_name().split('.')[-1] if s.get_editor_property('material') else None for s in g.get_editor_property('hair_groups_materials')]
        gi['meshes'] = len(g.get_editor_property('hair_groups_meshes'))
    G[part] = gi
G['helmet'] = {'mesh': u.load_asset(f'{F}/Hair/SM_LK_HairHelmet_{HT}') is not None}
out['grooms'] = G
BD = {}
for key in ('HairMain', 'HairLoose', 'Eyebrows', 'Eyelashes'):
    b = u.load_asset(f'{IDF}/Face/Bindings/GB_ID_{key}_{FS}'); d = {'loaded': b is not None}
    if b:
        tm = b.get_editor_property('target_skeletal_mesh'); gr = b.get_editor_property('groom')
        d['target'] = tm.get_path_name().split('.')[-1] if tm else None; d['groom'] = gr.get_path_name().split('.')[-1] if gr else None
    BD[key] = d
out['bindings'] = BD
SKN = {}
for n in [BM]+[f'MI_LK_Face_{x}_VT_{SK}' for x in ('LOD0', 'LOD1', 'LOD2', 'LOD3', 'LOD4', 'LOD5to7')]:
    m = u.load_asset(F+'/Skin/'+n); d = {'loaded': m is not None}
    if m:
        d['parent'] = m.get_editor_property('parent').get_name()
        d['basecolor'] = (lambda t: t.get_name() if t else None)(ME.get_material_instance_texture_parameter_value(m, 'Basecolor Baked VT'))
        d['normal'] = (lambda t: t.get_name() if t else None)(ME.get_material_instance_texture_parameter_value(m, 'Normal Baked VT'))
        if n == BM: d['scalars'] = {k: round(ME.get_material_instance_scalar_parameter_value(m, k), 3) for k in ('Micro Skin Tiling', 'Roughness Global Offset Post-Bake', 'Specular Global Multiply Post-Bake', 'Roughness Concavity Multiply', 'Specular Concavity Multiply')}
    SKN[n] = d
out['skin'] = SKN
GM = {}
for g in ('Henley', 'Shorts'):
    m = u.load_asset(F+f'/Outfit/SKM_LK_{g}_g15b'); d = {'loaded': m is not None}
    if m: d['lod_verts'] = [sme.get_num_verts(m, i) for i in range(sme.get_lod_count(m))]; d['morphs'] = len(m.get_editor_property('morph_targets')); d['materials'] = [sm.get_editor_property('material_interface').get_name() for sm in m.get_editor_property('materials')]
    GM[g] = d
out['garments_g15b'] = GM
out['mhc'] = {n: EAL.does_asset_exist(IDF+'/MHC/'+n) for n in ('MHC_ID_Base', 'MHC_ID_C')}
seq = u.load_asset(F+'/Face/Diagnostics/AS_FM_FacialRig'); out['rig_sequence'] = {'loaded': seq is not None, 'length_s': seq.get_play_length() if seq else None}
out['dirty_after'] = [p.get_path_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
O.write_text(json.dumps(out, indent=1, default=str)); print('ID_REOPEN_OK', json.dumps({'face': fc.get('morph_total'), 'lods': fc.get('lod_verts'), 'vs_source': out['face_vs_source'], 'base_diff': base, 'dirty': out['dirty_after']}, default=str))
