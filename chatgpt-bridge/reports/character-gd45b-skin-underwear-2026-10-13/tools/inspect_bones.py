"""GD45 audit (read-only, transient actors): bone-name differences game body vs LK body; Manny / Face template flags (post-process, LOD, bounds); garment SKM clothing assets."""
import unreal as u, json
out = {}
def bones_of(mesh_path):
    a = u.EditorLevelLibrary.spawn_actor_from_class(u.SkeletalMeshActor, u.Vector(0, 0, -100000)); c = a.skeletal_mesh_component; c.set_skeletal_mesh_asset(u.load_asset(mesh_path)); n = c.get_num_bones(); names = [str(c.get_bone_name(i)) for i in range(n)]; a.destroy_actor(); return names
g = bones_of('/Game/MetaHumans/MH_MainCharacter/Body/SKM_MH_MainCharacter_BodyMesh'); l = bones_of('/Game/Sphirus/CharacterLab/CharacterLookdev_20260930/Body/SKM_LK_BodyMesh')
out['n_bones'] = [len(g), len(l)]; out['game_not_lk'] = sorted(set(g)-set(l)); out['lk_not_game'] = sorted(set(l)-set(g)); out['order_same_prefix'] = g[:len(l)] == l if len(l) <= len(g) else None
gf = bones_of('/Game/MetaHumans/MH_MainCharacter/Face/SKM_MH_MainCharacter_FaceMesh'); lf = bones_of('/Game/Sphirus/CharacterLab/GD38_IdentityMaster_20261011/Face/SKM_GD38_Face_t38'); out['face_bones'] = [len(gf), len(lf), sorted(set(gf)-set(lf))[:10], sorted(set(lf)-set(gf))[:10]]
sds = u.get_engine_subsystem(u.SubobjectDataSubsystem); BFL = u.SubobjectDataBlueprintFunctionLibrary; bp = u.load_asset('/Game/ActionAdventureMovementS/Animations/Locomotion/CoreMotionAAMS/Integrated/BP_Player_MM'); fl = {}
for h in sds.k2_gather_subobject_data_for_blueprint(bp):
    o = BFL.get_object(BFL.get_data(h))
    if o is None or not isinstance(o, u.SkeletalMeshComponent): continue
    nm = o.get_name().replace('_GEN_VARIABLE', ''); e = {}
    for p_ in ('disable_post_process_blueprint', 'forced_lod_model', 'use_attach_parent_bound', 'leader_pose_component', 'visibility_based_anim_tick_option', 'cast_shadow', 'min_lod_model', 'skin_cache_usage'):
        try: v = o.get_editor_property(p_); e[p_] = v.get_name() if hasattr(v, 'get_name') else str(v)
        except Exception as ex: e[p_] = 'ERR '+str(ex)[:40]
    fl[nm] = e
out['template_flags'] = fl
for k, p in (('henley', '/Game/Sphirus/CharacterLab/CharacterGuardian_20261001/Outfit/SKM_LK_Henley_g17e'), ('shorts', '/Game/Sphirus/CharacterLab/CharacterCorrective_20261001/Outfit/SKM_LK_Shorts_g16c')):
    m = u.load_asset(p)
    try: ca = m.get_editor_property('mesh_clothing_assets'); out[k+'_cloth'] = [c.get_path_name() for c in ca]
    except Exception as ex: out[k+'_cloth'] = 'ERR '+str(ex)[:80]
    try: out[k+'_lods'] = m.get_editor_property('lod_info').__len__()
    except Exception: pass
json.dump(out, open('C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Saved/Codex/GD45_Promote_20261013/data/bones.json', 'w'), indent=1); print('GD45_BONES', json.dumps(out)[:1500], flush=True)
