"""CORRECTIVE pass save/reopen verification (run in a FRESH editor session, before any QA scene): loads the final corrective
candidate from disk (face j + skin c12s, hair id17 + bindings, Henley g16c (+ m1 materials, soft-tissue correctives), Chaos shorts
CA_CR_Shorts_m1 + collider, m1 textile MIs) and checks morphs / LODs / slots / groom LOD mode / cloth asset. Read-only (nothing saved).
Writes Saved/Codex/CharacterCorrective_20261001/reopen_check.json"""
import unreal as u, pathlib, json
R = pathlib.Path(u.Paths.project_dir()).resolve(); O = R/'Saved/Codex/CharacterCorrective_20261001/reopen_check.json'
F = '/Game/Sphirus/CharacterLab/CharacterCorrective_20261001'; EAL = u.EditorAssetLibrary; ME = u.MaterialEditingLibrary
out = {'dirty_before': [p.get_path_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]}
sme = u.get_editor_subsystem(u.SkeletalMeshEditorSubsystem)
def mesh_info(path):
    m = u.load_asset(path); d = {'loaded': m is not None}
    if not m: return d
    names = [x.get_name() for x in m.get_editor_property('morph_targets')]
    d['morph_total'] = len(names); d['rv_morphs'] = sorted(n for n in names if n.startswith('RV_')); d['br_neutral'] = 'BR_Neutral' in names
    n = sme.get_lod_count(m); d['lod_verts'] = [sme.get_num_verts(m, i) for i in range(n)]
    d['materials'] = [(str(x.get_editor_property('material_slot_name')), x.get_editor_property('material_interface').get_name() if x.get_editor_property('material_interface') else None) for x in m.get_editor_property('materials')]
    d['skeleton'] = m.skeleton.get_path_name().split('.')[-1]; d['post_process_abp'] = m.post_process_anim_blueprint.get_path_name().split('/')[-1] if m.post_process_anim_blueprint else None; return d
out['face_j'] = mesh_info(F+'/Face/SKM_CR_FaceMesh_j')
out['henley_g16c'] = mesh_info(F+'/Outfit/SKM_LK_Henley_g16c'); out['shorts_g16c'] = mesh_info(F+'/Outfit/SKM_LK_Shorts_g16c')
G = {}
for part in ('Main', 'Loose'):
    g = u.load_asset(f'{F}/Hair/GR_LK_Hair_{part}_id17'); gi = {'loaded': g is not None}
    if g:
        gi['lods'] = len(g.get_editor_property('hair_groups_lod'))
        try: gi['lod_mode'] = str(g.get_editor_property('lod_mode'))
        except Exception as e: gi['lod_mode'] = 'n/a '+str(e)[:80]
        try: gi['sim'] = [x.export_text()[:160] for x in g.get_editor_property('hair_groups_physics')][:1]
        except Exception as e: gi['sim'] = 'n/a '+str(e)[:80]
    G[part] = gi
for b in ('HairMain', 'HairLoose', 'Eyebrows', 'Eyelashes'):
    bd = u.load_asset(f'{F}/Face/Bindings/GB_CR_{b}_j'); G['GB_CR_'+b+'_j'] = {'loaded': bd is not None}
    if bd:
        try: G['GB_CR_'+b+'_j'].update({'groom': bd.get_editor_property('groom').get_name(), 'target': bd.get_editor_property('target_skeletal_mesh').get_name()})
        except Exception as e: G['GB_CR_'+b+'_j']['err'] = str(e)[:120]
out['hair'] = G
C = {}
for n in ('CA_CR_Shorts_m1', 'PHYS_CR_ShortsCollider', 'SM_CR_Shorts_m1_Sim', 'DF_CR_Shorts_m1'):
    a = u.load_asset(F+'/Cloth/'+n); r = {'loaded': a is not None, 'class': a.get_class().get_name() if a else None}
    if a and n.startswith('CA_'):
        try: r['physics_asset'] = a.get_editor_property('physics_asset').get_name()
        except Exception as e: r['physics_asset'] = 'n/a '+str(e)[:80]
        try: r['materials'] = [m.get_editor_property('material_interface').get_name() for m in a.get_editor_property('materials')]
        except Exception as e: r['materials'] = 'n/a '+str(e)[:80]
    C[n] = r
out['cloth'] = C
MI = {}
for n in ('MI_LK_Henley_m1', 'MI_LK_Henley_Trim_m1', 'MI_LK_Buttons_m1', 'MI_LK_Shorts_m1_cloth', 'MI_LK_Shorts_Trim_m1_cloth', 'MI_LK_Drawstring_m1_cloth'):
    m = u.load_asset(F+'/Outfit/Materials/'+n); r = {'loaded': m is not None}
    if m: r['parent'] = m.get_editor_property('parent').get_name(); r['base'] = ME.get_material_instance_texture_parameter_value(m, 'BaseColorTex').get_name()
    MI[n] = r
for n in ('MI_LK_Face_LOD0_VT_c12s', 'MI_LK_Face_LOD1_VT_c12s'):
    m = u.load_asset(F+'/Skin/'+n); r = {'loaded': m is not None}
    if m: r['parent'] = m.get_editor_property('parent').get_name(); r['srmf'] = ME.get_material_instance_texture_parameter_value(m, 'SRMF Baked VT').get_name(); r['normal'] = ME.get_material_instance_texture_parameter_value(m, 'Normal Baked VT').get_name(); r['bc'] = ME.get_material_instance_texture_parameter_value(m, 'Basecolor Baked VT').get_name()
    MI[n] = r
out['materials'] = MI
out['dirty_after'] = [p.get_path_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
O.write_text(json.dumps(out, indent=1)); print('CR_REOPEN', json.dumps(out)[:3000])
