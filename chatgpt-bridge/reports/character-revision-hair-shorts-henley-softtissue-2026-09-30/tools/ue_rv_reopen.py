"""Save/reopen verification (run in a FRESH editor session): loads every revision asset from disk and checks morph targets,
driver nodes, curve metadata, groom sim / material / bindings, LOD counts and body material. Read-only (nothing saved)."""
import unreal as u, pathlib, json
R = pathlib.Path(u.Paths.project_dir()).resolve(); O = R/'Saved/Codex/CharacterRevision_20260930/reopen_check.json'
F = '/Game/Sphirus/CharacterLab/CharacterRevision_20260930'; out = {'dirty_before': [p.get_path_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]}
sme = u.get_editor_subsystem(u.SkeletalMeshEditorSubsystem)
def mesh_info(path):
    m = u.load_asset(path); d = {'loaded': m is not None}
    if not m: return d
    names = [x.get_name() for x in m.get_editor_property('morph_targets')]
    d['morph_total'] = len(names); d['rv_morphs'] = sorted(n for n in names if n.startswith('RV_')); d['shc_morphs'] = len([n for n in names if n.startswith('SHC_')])
    n = sme.get_lod_count(m); d['lods'] = [[sme.get_num_verts(m, i), None] for i in range(n)]
    try: d['lod_tris'] = [sum(s.get_editor_property('num_triangles') for s in m.get_editor_property('lod_info')[i].get_editor_property('sections')) for i in range(n)]
    except Exception as e: d['lod_tris'] = 'n/a'
    d['materials'] = [x.get_editor_property('material_interface').get_path_name() if x.get_editor_property('material_interface') else None for x in m.get_editor_property('materials')]
    d['post_process_abp'] = m.post_process_anim_blueprint.get_path_name() if m.post_process_anim_blueprint else None
    d['skeleton'] = m.skeleton.get_path_name(); return d
out['body'] = mesh_info(F+'/Body/SKM_RV_BodyMesh'); out['face'] = mesh_info(F+'/Body/SKM_RV_FaceMesh')
out['henley'] = mesh_info(F+'/Outfit/SKM_RV_Henley'); out['shorts'] = mesh_info(F+'/Outfit/SKM_RV_Shorts')
bp = u.load_asset(F+'/Body/ABP_RV_Body_PostProcess')
nodes = u.AnimationLibrary.get_nodes_of_class(bp, u.AnimGraphNode_PoseDriver, True) if hasattr(u, 'AnimationLibrary') else []
out['abp'] = {'loaded': bp is not None, 'pose_drivers': [str(n.get_editor_property('tag')) for n in nodes]}
try: out['abp']['status'] = str(bp.get_editor_property('status'))
except Exception as e: out['abp']['status'] = 'n/a'
sk = u.load_asset(out['body']['skeleton'].split('.')[0]) if out['body'].get('skeleton') else None
curves = ['RV_Bend30', 'RV_Bend60', 'RV_Bend90', 'RV_Twist_l', 'RV_Twist_r'] + [f'RV_Arm{a}_{s}' for a in ('090', '120', '150', '180', 'Fwd') for s in 'lr'] + [f'RV_Hip{a}_{s}' for a in ('075', '110') for s in 'lr']
out['curve_meta'] = {c: bool(sk.get_curve_meta_data_morph_target(c)) for c in curves} if sk else None
G = {}
for tag in ('Main', 'Loose'):
    g = u.load_asset(f'{F}/Hair/GR_RV_Hair_{tag}_v12'); bd = u.load_asset(f'{F}/Hair/GR_RV_Hair_{tag}_v12_Binding')
    gi = {'loaded': g is not None, 'binding_loaded': bd is not None}
    if g:
        gi['sim'] = [p.get_editor_property('solver_settings').get_editor_property('enable_simulation') for p in g.get_editor_property('hair_groups_physics')]
        gi['groups'] = len(g.get_editor_property('hair_groups_rendering'))
        try: gi['materials'] = [s.get_editor_property('material').get_path_name() for s in g.get_editor_property('hair_groups_materials')]
        except Exception as e: gi['materials'] = str(e)[:120]
        try: gi['groom_info'] = [x.export_text()[:200] for x in g.get_editor_property('hair_groups_info')]
        except Exception as e: gi['groom_info'] = str(e)[:120]
    if bd:
        try: gi['binding_target'] = bd.get_editor_property('target_skeletal_mesh').get_path_name()
        except Exception as e: gi['binding_target'] = str(e)[:120]
    G[tag] = gi
for n in ('RV_Eyebrows_M_Slit_Binding', 'RV_Eyelashes_L_Curl_Binding'): G[n] = {'loaded': u.load_asset(f'{F}/Hair/{n}') is not None}
mi = u.load_asset(F+'/Hair/MI_RV_Hair_Auburn')
G['MI_RV_Hair_Auburn'] = {'loaded': mi is not None, 'parent': mi.get_editor_property('parent').get_path_name() if mi else None,
    'melanin': u.MaterialEditingLibrary.get_material_instance_scalar_parameter_value(mi, 'hairMelanin') if mi else None, 'redness': u.MaterialEditingLibrary.get_material_instance_scalar_parameter_value(mi, 'hairRedness') if mi else None}
out['grooms'] = G; out['poselib'] = u.load_asset(F+'/Anim/AN_RV_PoseLib2') is not None
out['dirty_after'] = [p.get_path_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
O.write_text(json.dumps(out, indent=1)); print('REOPEN_OK', json.dumps({k: (v.get('morph_total'), len(v.get('rv_morphs', [])), v.get('lods')) for k, v in out.items() if isinstance(v, dict) and 'morph_total' in v}))
