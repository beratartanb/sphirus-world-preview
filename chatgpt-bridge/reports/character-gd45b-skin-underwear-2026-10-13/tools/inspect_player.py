"""GD45 audit (read-only): component tree of the playable pawn chain (BP_PBI_Player -> parents), skeletal meshes / anim classes / grooms / bindings / leader pose, plus the MetaHuman MH_MainCharacter folder and referencers of the LK body / GD38 face."""
import unreal as u, json
EAL = u.EditorAssetLibrary; AR = u.AssetRegistryHelpers.get_asset_registry(); out = {}
BP = '/Game/GraceRanger/Experimental/BodyInertia/BP_PBI_Player'
bp = u.load_asset(BP); gen = bp.generated_class(); cdo = u.get_default_object(gen)
chain = []; c = gen
while c:
    chain.append(c.get_path_name()); c = c.get_super_class() if hasattr(c, 'get_super_class') else None
    if c and 'Script/' in c.get_path_name(): chain.append(c.get_path_name()); break
out['class_chain'] = chain
def comps_of(cls):
    try:
        bpa = u.BlueprintEditorLibrary.get_blueprint_asset(cls) if hasattr(u.BlueprintEditorLibrary, 'get_blueprint_asset') else None
    except Exception: bpa = None
    return bpa
# default object components via the CDO's subobjects: use a transient actor spawned in the editor world instead (SCS components are instanced on spawn)
w = u.EditorLevelLibrary.get_editor_world(); actor = u.EditorLevelLibrary.spawn_actor_from_class(gen, u.Vector(0, 0, -100000)); comps = []
for comp in actor.get_components_by_class(u.ActorComponent):
    d = {'name': comp.get_name(), 'class': comp.get_class().get_name()}
    par = comp.get_attach_parent() if isinstance(comp, u.SceneComponent) else None
    if par: d['parent'] = par.get_name()
    if isinstance(comp, u.SkeletalMeshComponent):
        sm = comp.get_skeletal_mesh_asset() if hasattr(comp, 'get_skeletal_mesh_asset') else comp.skeletal_mesh
        d['mesh'] = sm.get_path_name() if sm else None; d['anim_class'] = comp.get_anim_class().get_path_name() if comp.get_anim_class() else None
        d['anim_mode'] = str(comp.get_editor_property('animation_mode'))
        lp = comp.get_editor_property('leader_pose_component') if hasattr(comp, 'get_editor_property') else None
        try: lpc = comp.get_editor_property('leader_pose_component'); d['leader_pose'] = lpc.get_name() if lpc else None
        except Exception: pass
        d['materials'] = [m.get_path_name() if m else None for m in comp.get_materials()][:6]; d['visible'] = comp.is_visible()
    if comp.get_class().get_name() == 'GroomComponent':
        g = comp.get_editor_property('groom_asset'); b = comp.get_editor_property('binding_asset'); d['groom'] = g.get_path_name() if g else None; d['binding'] = b.get_path_name() if b else None; d['visible'] = comp.is_visible()
    if comp.get_class().get_name() == 'ChildActorComponent':
        cac = comp.get_editor_property('child_actor_class'); d['child_actor_class'] = cac.get_path_name() if cac else None
    comps.append(d)
out['components'] = comps; actor.destroy_actor()
out['mh_folder'] = [a.get_editor_property('package_name').__str__() for a in AR.get_assets_by_path('/Game/MetaHumans/MH_MainCharacter', recursive=True)][:60]
for key, path in (('lk_body', '/Game/Sphirus/CharacterLab/CharacterLookdev_20260930/Body/SKM_LK_BodyMesh'), ('gd38_face', '/Game/Sphirus/CharacterLab/GD38_IdentityMaster_20261011/Face/SKM_GD38_Face_t38')):
    refs = AR.get_referencers(u.Name(path.rsplit('/', 1)[0]+'/'+path.rsplit('/', 1)[1]), u.AssetRegistryDependencyOptions()) if False else []
    try:
        ids = u.AssetRegistryHelpers.get_asset_registry().get_referencers(path, u.AssetRegistryDependencyOptions())
        out[key+'_referencers'] = [str(x) for x in ids][:40]
    except Exception as e: out[key+'_referencers'] = 'ERR '+str(e)
json.dump(out, open('C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Saved/Codex/GD45_Promote_20261013/data/player_inspect.json', 'w'), indent=1); print('GD45_INSPECT', json.dumps({'chain': out['class_chain'], 'n_comps': len(comps)}), flush=True)
