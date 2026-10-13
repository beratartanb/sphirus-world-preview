"""GD45 audit (read-only, transient actors only): pawn component tree with anim classes; compatible-skeleton lists; empirical anim-class compatibility of the LK body / GD38 face with the game's anim classes."""
import unreal as u, json
out = {}; EAL = u.EditorAssetLibrary
def gp(o, n):
    try: return o.get_editor_property(n)
    except Exception as e: return 'ERR '+str(e)[:60]
def pn(o): return o.get_path_name() if o is not None and not isinstance(o, str) else o
BP = '/Game/GraceRanger/Experimental/BodyInertia/BP_PBI_Player'; gen = u.load_asset(BP).generated_class(); chain = []; c = gen
for _ in range(8):
    chain.append(c.get_path_name()); 
    try: c = c.get_super_class()
    except Exception: break
    if c is None or 'Script/' in c.get_path_name(): chain.append(c.get_path_name() if c else None); break
out['class_chain'] = chain
actor = u.EditorLevelLibrary.spawn_actor_from_class(gen, u.Vector(0, 0, -100000)); comps = []
for comp in actor.get_components_by_class(u.ActorComponent):
    d = {'name': comp.get_name(), 'class': comp.get_class().get_name()}
    if isinstance(comp, u.SceneComponent):
        par = comp.get_attach_parent(); d['parent'] = par.get_name() if par else None; d['socket'] = str(comp.get_attach_socket_name())
    if isinstance(comp, u.SkeletalMeshComponent):
        d['mesh'] = pn(gp(comp, 'skeletal_mesh_asset')); d['anim_class'] = pn(gp(comp, 'anim_class')); d['anim_mode'] = str(gp(comp, 'animation_mode')); d['leader_pose'] = pn(gp(comp, 'leader_pose_component'))
        d['visible'] = comp.is_visible(); d['materials'] = [pn(m) for m in comp.get_materials()][:5]
    if comp.get_class().get_name() == 'GroomComponent': d['groom'] = pn(gp(comp, 'groom_asset')); d['binding'] = pn(gp(comp, 'binding_asset')); d['visible'] = comp.is_visible()
    if comp.get_class().get_name() == 'ChildActorComponent': d['child_actor_class'] = pn(gp(comp, 'child_actor_class'))
    comps.append(d)
out['components'] = comps; actor.destroy_actor()
SK = {'game_body': '/Game/MetaHumans/Common/Female/Medium/NormalWeight/Body/metahuman_base_skel', 'sf_body': '/Game/Sphirus/CharacterLab/ShoulderFix_20260928/Common/Female/Medium/NormalWeight/Body/metahuman_base_skel', 'plugin_body': '/MetaHumanCharacter/Female/Medium/NormalWeight/Body/metahuman_base_skel', 'game_face': '/Game/MetaHumans/Common/Face/Face_Archetype_Skeleton', 'plugin_face': '/MetaHumanCharacter/Face/Face_Archetype_Skeleton', 'sf_face': '/Game/Sphirus/CharacterLab/ShoulderFix_20260928/Common/Face/Face_Archetype_Skeleton'}
out['compat'] = {}
for k, p in SK.items():
    s = u.load_asset(p)
    if not s: out['compat'][k] = 'missing'; continue
    try: out['compat'][k] = {'bones': s.get_editor_property('bone_tree').__len__() if hasattr(s.get_editor_property('bone_tree'), '__len__') else None, 'compatible': [x.get_path_name() if hasattr(x, 'get_path_name') else str(x) for x in gp(s, 'compatible_skeletons')]}
    except Exception as e: out['compat'][k] = 'ERR '+str(e)[:120]
# empirical: transient actor with the LK body + the game's visible-body anim class, and the GD38 face + the game's face anim class (taken from the pawn audit)
body_anim = next((c.get('anim_class') for c in comps if c.get('mesh') and 'BodyMesh' in (c.get('mesh') or '')), None); face_anim = next((c.get('anim_class') for c in comps if c.get('mesh') and 'FaceMesh' in (c.get('mesh') or '')), None)
out['game_body_anim'] = body_anim; out['game_face_anim'] = face_anim; tests = {}
for key, mesh, anim in (('lk_body_with_game_abp', '/Game/Sphirus/CharacterLab/CharacterLookdev_20260930/Body/SKM_LK_BodyMesh', body_anim), ('gd38_face_with_game_face_abp', '/Game/Sphirus/CharacterLab/GD38_IdentityMaster_20261011/Face/SKM_GD38_Face_t38', face_anim), ('mh_body_with_game_abp_control', '/Game/MetaHumans/MH_MainCharacter/Body/SKM_MH_MainCharacter_BodyMesh', body_anim)):
    if not anim: tests[key] = 'no anim class found'; continue
    a = u.EditorLevelLibrary.spawn_actor_from_class(u.SkeletalMeshActor, u.Vector(0, 0, -100000)); sc = a.skeletal_mesh_component; sc.set_skeletal_mesh_asset(u.load_asset(mesh))
    cls = u.load_class(None, anim if anim.endswith('_C') else anim+'_C')
    try:
        sc.set_anim_instance_class(cls); inst = sc.get_anim_instance(); tests[key] = {'anim_instance': inst.get_class().get_name() if inst else None, 'set_ok': inst is not None and cls is not None and inst.get_class().get_path_name() == cls.get_path_name()}
    except Exception as e: tests[key] = 'ERR '+str(e)[:160]
    a.destroy_actor()
out['tests'] = tests
json.dump(out, open('C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Saved/Codex/GD45_Promote_20261013/data/pawn2.json', 'w'), indent=1); print('GD45_PAWN2', json.dumps({'body_anim': body_anim, 'face_anim': face_anim, 'tests': tests}), flush=True)
