"""GD45b (user: 'classic MetaHuman underwear is still on the body - remove it'): the LK body mesh's default material carries the MetaHuman baked
maps with the underwear painted in. The approved lookdev composition (every 'ten' board since GD15/GD31) applied component material overrides:
Body slot 0 -> MI_GD15_Body_s1 (no underwear), Head slots -> GD31 n3 face skin LOD MIs + GD15 h6 eyes. Apply the same overrides on the in-game
pawn's Manny / Face templates (owner BP_Player_MM), compile, save owner + children; checkpoint2 copies taken before this job."""
import unreal as u, json
OUT = 'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Saved/Codex/GD45_Promote_20261013/data/skin.json'
sds = u.get_engine_subsystem(u.SubobjectDataSubsystem); BFL = u.SubobjectDataBlueprintFunctionLibrary; EAL = u.EditorAssetLibrary
BP = '/Game/ActionAdventureMovementS/Animations/Locomotion/CoreMotionAAMS/Integrated/BP_Player_MM'; bp = u.load_asset(BP)
OV = {'Manny': {0: '/Game/Sphirus/CharacterLab/GD15_IdentityMaster_20261009/Looks/MI_GD15_Body_s1'},
      'Face': {0: '/Game/Sphirus/CharacterLab/GD31_IdentityMaster_20261011/Looks/MI_GD31_Face_LOD0_s1t6n_n3', 9: '/Game/Sphirus/CharacterLab/GD31_IdentityMaster_20261011/Looks/MI_GD31_Face_LOD1_s1t6n_n3',
               10: '/Game/Sphirus/CharacterLab/GD31_IdentityMaster_20261011/Looks/MI_GD31_Face_LOD2_s1t6n_n3', 12: '/Game/Sphirus/CharacterLab/GD31_IdentityMaster_20261011/Looks/MI_GD31_Face_LOD3_s1t6n_n3',
               13: '/Game/Sphirus/CharacterLab/GD31_IdentityMaster_20261011/Looks/MI_GD31_Face_LOD4_s1t6n_n3', 14: '/Game/Sphirus/CharacterLab/GD31_IdentityMaster_20261011/Looks/MI_GD31_Face_LOD5to7_s1t6n_n3',
               3: '/Game/Sphirus/CharacterLab/GD15_IdentityMaster_20261009/Looks/MI_GD15_EyeL_h6', 4: '/Game/Sphirus/CharacterLab/GD15_IdentityMaster_20261009/Looks/MI_GD15_EyeR_h6'}}
for slots in OV.values():
    for p in slots.values(): assert EAL.does_asset_exist(p), 'missing ' + p
rep = {'before': {}, 'after': {}, 'slots': {}}
objs = {}
for h in sds.k2_gather_subobject_data_for_blueprint(bp):
    o = BFL.get_object(BFL.get_data(h))
    if o is not None and isinstance(o, u.SkeletalMeshComponent): objs[o.get_name().replace('_GEN_VARIABLE', '')] = o
for nm, slots in OV.items():
    c = objs[nm]; mesh = c.get_editor_property('skeletal_mesh_asset'); mats = mesh.get_editor_property('materials')
    rep['slots'][nm] = [str(m.material_slot_name) + ':' + (m.material_interface.get_name() if m.material_interface else 'None') for m in mats]
    cur = list(c.get_editor_property('override_materials')); rep['before'][nm] = [m.get_path_name() if m else None for m in cur]
    n = max(len(cur), len(mats), max(slots) + 1); arr = [cur[i] if i < len(cur) else None for i in range(n)]
    for i, p in slots.items(): arr[i] = u.load_asset(p)
    c.modify(); c.set_editor_property('override_materials', u.Array(u.MaterialInterface) if False else arr)
    rep['after'][nm] = [m.get_path_name() if m else None for m in c.get_editor_property('override_materials')]
u.BlueprintEditorLibrary.compile_blueprint(bp); rep['owner_saved'] = EAL.save_loaded_asset(bp, False)
for p in ('/Game/GraceRanger/BP_GR_Player', '/Game/GraceRanger/Experimental/BodyInertia/BP_PBI_Player'):
    b2 = u.load_asset(p); u.BlueprintEditorLibrary.compile_blueprint(b2); rep[p.rsplit('/', 1)[-1] + '_saved'] = EAL.save_loaded_asset(b2, False)
rep['dirty_after'] = [str(x.get_path_name()) for x in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()][:10]
json.dump(rep, open(OUT, 'w'), indent=1); print('GD45_SKIN', json.dumps({'slots': rep['slots'], 'after': rep['after'], 'saved': rep['owner_saved'], 'dirty': rep['dirty_after']})[:1500], flush=True)
