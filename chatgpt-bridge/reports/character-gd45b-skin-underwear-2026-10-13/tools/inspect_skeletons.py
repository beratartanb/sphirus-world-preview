"""GD45 audit (read-only): skeletons, post-process ABPs, LODs, morphs, physics of the production MetaHuman meshes vs the LK body / GD38 face; retarget ABP target skeleton; groom binding targets; garments."""
import unreal as u, json
out = {}
def mesh_info(path):
    m = u.load_asset(path)
    if not m: return {'missing': True}
    d = {'skeleton': m.skeleton.get_path_name() if m.skeleton else None, 'lods': m.get_lod_num() if hasattr(m, 'get_lod_num') else None}
    try: d['post_process_abp'] = m.get_editor_property('post_process_anim_blueprint').get_path_name() if m.get_editor_property('post_process_anim_blueprint') else None
    except Exception as e: d['post_process_abp'] = 'ERR '+str(e)[:80]
    try: d['physics_asset'] = m.get_editor_property('physics_asset').get_path_name() if m.get_editor_property('physics_asset') else None
    except Exception: pass
    try: d['morphs'] = [str(x) for x in m.get_all_morph_target_names()][:40]
    except Exception: pass
    try: d['materials'] = [str(sm.material_interface.get_path_name()) if sm.material_interface else None for sm in m.materials][:8]
    except Exception: pass
    try:
        sk = m.skeleton; d['compatible_skeletons'] = [s.get_path_name() for s in sk.get_editor_property('compatible_skeletons')] if sk else None
    except Exception as e: d['compatible_skeletons'] = 'ERR '+str(e)[:80]
    return d
for k, p in (('mh_body', '/Game/MetaHumans/MH_MainCharacter/Body/SKM_MH_MainCharacter_BodyMesh'), ('mh_face', '/Game/MetaHumans/MH_MainCharacter/Face/SKM_MH_MainCharacter_FaceMesh'), ('lk_body', '/Game/Sphirus/CharacterLab/CharacterLookdev_20260930/Body/SKM_LK_BodyMesh'), ('gd38_face', '/Game/Sphirus/CharacterLab/GD38_IdentityMaster_20261011/Face/SKM_GD38_Face_t38'), ('henley', '/Game/Sphirus/CharacterLab/CharacterGuardian_20261001/Outfit/SKM_LK_Henley_g17e'), ('shorts', '/Game/Sphirus/CharacterLab/CharacterCorrective_20261001/Outfit/SKM_LK_Shorts_g16c')):
    out[k] = mesh_info(p)
AR = u.AssetRegistryHelpers.get_asset_registry(); out['mh_face_folder'] = [str(a.package_name) for a in AR.get_assets_by_path('/Game/MetaHumans/MH_MainCharacter/Face', recursive=False)][:30]; out['mh_body_folder'] = [str(a.package_name) for a in AR.get_assets_by_path('/Game/MetaHumans/MH_MainCharacter/Body', recursive=False)][:30]; out['mh_root'] = [str(a.package_name) for a in AR.get_assets_by_path('/Game/MetaHumans/MH_MainCharacter', recursive=False)][:30]
for k, p in (('abp_gr_mh', '/Game/GraceRanger/Animations/ABP_GR_MetaHuman'), ('abp_lk_pp', '/Game/Sphirus/CharacterLab/CharacterLookdev_20260930/Body/ABP_LK_Body_PostProcess')):
    a = u.load_asset(p)
    if a:
        try: out[k] = {'target_skeleton': a.get_editor_property('target_skeleton').get_path_name() if a.get_editor_property('target_skeleton') else None, 'parent': a.generated_class().get_super_class().get_path_name() if hasattr(a.generated_class(), 'get_super_class') else None}
        except Exception as e: out[k] = 'ERR '+str(e)[:100]
    else: out[k] = 'missing'
for k, p in (('gb_hair', '/Game/Sphirus/CharacterLab/GD38_IdentityMaster_20261011/Face/Bindings/GB_GD38_HairMain_t38h75c'),):
    b = u.load_asset(p)
    if b:
        try: out[k] = {'target': b.get_editor_property('target_skeletal_mesh').get_path_name() if b.get_editor_property('target_skeletal_mesh') else None, 'source': b.get_editor_property('source_skeletal_mesh').get_path_name() if b.get_editor_property('source_skeletal_mesh') else None, 'valid': b.is_valid() if hasattr(b, 'is_valid') else None}
        except Exception as e: out[k] = 'ERR '+str(e)[:100]
json.dump(out, open('C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Saved/Codex/GD45_Promote_20261013/data/skeleton_inspect.json', 'w'), indent=1); print('GD45_SKEL', json.dumps({k: (v.get('skeleton') if isinstance(v, dict) else v) for k, v in out.items() if k in ('mh_body', 'mh_face', 'lk_body', 'gd38_face', 'abp_gr_mh')}), flush=True)
