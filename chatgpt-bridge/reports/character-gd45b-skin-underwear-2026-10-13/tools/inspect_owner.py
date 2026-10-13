"""GD45 audit (read-only): which Blueprint owns the Manny / Face / groom subobjects (SCS owner class), Manny flags, the GD38 eval BP garment component settings, and the bone-name difference between the game body skeleton and the ShoulderFix skeleton."""
import unreal as u, json
out = {}; sds = u.get_engine_subsystem(u.SubobjectDataSubsystem); BFL = u.SubobjectDataBlueprintFunctionLibrary
def gp(o, n):
    try: v = o.get_editor_property(n); return v.get_path_name() if hasattr(v, 'get_path_name') else (str(v) if not isinstance(v, (int, float, bool, str)) else v)
    except Exception as e: return 'ERR '+str(e)[:50]
def tree(bp_path, names):
    bp = u.load_asset(bp_path); res = {}
    for h in sds.k2_gather_subobject_data_for_blueprint(bp):
        d = BFL.get_data(h); o = BFL.get_object(d)
        if o is None: continue
        nm = o.get_name()
        try: inh = d.is_inherited_component() if hasattr(d, 'is_inherited_component') else None
        except Exception: inh = None
        if any(k in nm for k in names) or isinstance(o, u.SkeletalMeshComponent) or o.get_class().get_name() == 'GroomComponent':
            e = {'class': o.get_class().get_name(), 'outer': o.get_outer().get_name() if o.get_outer() else None, 'inherited': inh}
            if isinstance(o, u.SkeletalMeshComponent):
                for p_ in ('skeletal_mesh_asset', 'anim_class', 'animation_mode', 'leader_pose_component', 'disable_post_process_blueprint', 'forced_lod_model', 'use_attach_parent_bound', 'visible', 'collision_enabled'):
                    e[p_] = gp(o, p_)
                try: e['cloth'] = {'simulate': gp(o, 'disable_cloth_simulation'), 'collide_env': gp(o, 'collide_with_environment'), 'attached_collision': gp(o, 'collide_with_attached_children')}
                except Exception: pass
            if o.get_class().get_name() == 'GroomComponent':
                for p_ in ('groom_asset', 'binding_asset', 'visible'): e[p_] = gp(o, p_)
            res[nm] = e
    return res
out['pawn_tree'] = tree('/Game/GraceRanger/Experimental/BodyInertia/BP_PBI_Player', ['Manny', 'Face', 'Hair', 'Eyebrows', 'Eyelashes', 'Fuzz', 'Beard', 'Mustache'])
for bp in ('/Game/GraceRanger/BP_GR_Player', '/Game/ActionAdventureMovementS/Animations/Locomotion/CoreMotionAAMS/Integrated/BP_Player_MM'):
    try: out[bp.rsplit('/', 1)[-1]+'_tree'] = {k: v.get('outer') for k, v in tree(bp, ['Manny', 'Face', 'Hair']).items()}
    except Exception as e: out[bp] = 'ERR '+str(e)[:100]
evalbp = '/Game/Sphirus/CharacterLab/GD38_IdentityMaster_20261011/Assembly/BP_GD38_Character_T38'
if not u.EditorAssetLibrary.does_asset_exist(evalbp):
    ar = u.AssetRegistryHelpers.get_asset_registry(); cands = [str(a.package_name) for a in ar.get_assets_by_path('/Game/Sphirus/CharacterLab/GD38_IdentityMaster_20261011', recursive=True) if 'BP_GD38' in str(a.package_name)]; out['eval_bp_candidates'] = cands; evalbp = cands[0] if cands else None
out['eval_bp'] = evalbp
if evalbp: out['eval_tree'] = tree(evalbp, ['Henley', 'Shorts', 'Body', 'Face', 'Hair'])
# bone-name diff between the game body skeleton and the ShoulderFix skeleton (via the meshes' reference skeletons)
def bones(mesh_path):
    m = u.load_asset(mesh_path); sk = m.skeleton
    try: return [str(sk.get_editor_property('bone_tree')[i].name) if hasattr(sk.get_editor_property('bone_tree')[i], 'name') else None for i in range(len(sk.get_editor_property('bone_tree')))]
    except Exception as e: return 'ERR '+str(e)[:80]
try:
    rsk = u.load_asset('/Game/MetaHumans/MH_MainCharacter/Body/SKM_MH_MainCharacter_BodyMesh'); lsk = u.load_asset('/Game/Sphirus/CharacterLab/CharacterLookdev_20260930/Body/SKM_LK_BodyMesh')
    gb = set(str(n) for n in rsk.skeleton.get_reference_pose_bone_names()) if hasattr(rsk.skeleton, 'get_reference_pose_bone_names') else None
    if gb is None:
        gb = set(str(rsk.get_bone_name(i)) for i in range(rsk.get_num_bones())) if hasattr(rsk, 'get_num_bones') else set()
        lb = set(str(lsk.get_bone_name(i)) for i in range(lsk.get_num_bones()))
    else: lb = set(str(n) for n in lsk.skeleton.get_reference_pose_bone_names())
    out['bones_game_not_lk'] = sorted(gb-lb)[:40]; out['bones_lk_not_game'] = sorted(lb-gb)[:40]; out['n_bones'] = [len(gb), len(lb)]
except Exception as e: out['bones_err'] = str(e)[:200]
json.dump(out, open('C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Saved/Codex/GD45_Promote_20261013/data/owner.json', 'w'), indent=1); print('GD45_OWNER', json.dumps({'pawn': {k: (v.get('outer'), v.get('inherited')) for k, v in out['pawn_tree'].items()}, 'eval_bp': evalbp, 'nbones': out.get('n_bones'), 'bones_err': out.get('bones_err')}), flush=True)
