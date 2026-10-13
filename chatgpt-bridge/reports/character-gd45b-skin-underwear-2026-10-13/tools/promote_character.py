"""GD45 PRODUCTION CHANGE (user request 2026-10-13: head + clothes onto the in-game character, body = the production LK body, GD39-44 candidates abandoned).
Mutating owner: /Game/ActionAdventureMovementS/Animations/Locomotion/CoreMotionAAMS/Integrated/BP_Player_MM (owns Manny / Face / grooms; parent of BP_GR_Player -> BP_PBI_Player).
Checkpoint: Saved/Codex/GD45_Promote_20261013/checkpoint (hash-verified copies of BP_Player_MM, BP_GR_Player, BP_PBI_Player) + owner.json / pawn2.json originals.
Changes: Manny mesh -> SKM_LK_BodyMesh (accepted B2 + BR_Neutral + LK_Neutral; post-process ABP re-enabled: it carries the always-on shape curves and the SHCB
correctives), Face mesh -> SKM_GD38_Face_t38, grooms -> GD38 bindings (+ new HairLoose), new skinned garments Henley / Shorts following Manny (leader pose).
Anim classes untouched (ABP_MH_Ranger_Retarget_V2 body, ABP_Face face). Component material overrides pointing at MH_MainCharacter materials are cleared."""
import unreal as u, json
OUT = 'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Saved/Codex/GD45_Promote_20261013/data/promote.json'
sds = u.get_engine_subsystem(u.SubobjectDataSubsystem); BFL = u.SubobjectDataBlueprintFunctionLibrary; EAL = u.EditorAssetLibrary
BP = '/Game/ActionAdventureMovementS/Animations/Locomotion/CoreMotionAAMS/Integrated/BP_Player_MM'; bp = u.load_asset(BP); assert bp
LKB = '/Game/Sphirus/CharacterLab/CharacterLookdev_20260930/Body/SKM_LK_BodyMesh'; FACE = '/Game/Sphirus/CharacterLab/GD38_IdentityMaster_20261011/Face/SKM_GD38_Face_t38'
GR = {'Hair': ('/Game/Sphirus/CharacterLab/GD11_HairQ_20261006/Hair/GR_LK_Hair_Main_h75c', '/Game/Sphirus/CharacterLab/GD38_IdentityMaster_20261011/Face/Bindings/GB_GD38_HairMain_t38h75c'),
      'HairLoose': ('/Game/Sphirus/CharacterLab/GD11_HairQ_20261006/Hair/GR_LK_Hair_Loose_h75c', '/Game/Sphirus/CharacterLab/GD38_IdentityMaster_20261011/Face/Bindings/GB_GD38_HairLoose_t38h75c'),
      'Eyebrows': ('/Game/Sphirus/CharacterLab/GD38_IdentityMaster_20261011/Grooms/GR_GD38_BrowCustom_ds8s', '/Game/Sphirus/CharacterLab/GD38_IdentityMaster_20261011/Face/Bindings/GB_GD38_EyebrowsCustom_ds8s_t38'),
      'Eyelashes': ('/Game/Sphirus/CharacterLab/GD31_IdentityMaster_20261011/Grooms/GR_GD31_Eyelashes_S_Thin', '/Game/Sphirus/CharacterLab/GD38_IdentityMaster_20261011/Face/Bindings/GB_GD38_EyelashesS_Thin31_t38')}
GARM = {'Henley': '/Game/Sphirus/CharacterLab/CharacterGuardian_20261001/Outfit/SKM_LK_Henley_g17e', 'Shorts': '/Game/Sphirus/CharacterLab/CharacterCorrective_20261001/Outfit/SKM_LK_Shorts_g16c'}
for p in [LKB, FACE] + [x for v in GR.values() for x in v] + list(GARM.values()):
    assert EAL.does_asset_exist(p), 'missing ' + p
handles = {}; objs = {}
for h in sds.k2_gather_subobject_data_for_blueprint(bp):
    o = BFL.get_object(BFL.get_data(h))
    if o is None: continue
    nm = o.get_name().replace('_GEN_VARIABLE', ''); handles[nm] = h; objs[nm] = o
assert 'Manny' in objs and 'Face' in objs, list(objs)
rep = {'before': {}, 'after': {}}
def snap(o):
    d = {}
    for p_ in ('skeletal_mesh_asset', 'anim_class', 'disable_post_process_blueprint', 'override_materials', 'groom_asset', 'binding_asset', 'leader_pose_component'):
        try:
            v = o.get_editor_property(p_)
            if isinstance(v, u.Array): d[p_] = [x.get_path_name() if x else None for x in v]
            else: d[p_] = v.get_path_name() if hasattr(v, 'get_path_name') else v
        except Exception: pass
    return d
for nm in ('Manny', 'Face', 'Hair', 'Eyebrows', 'Eyelashes'): rep['before'][nm] = snap(objs[nm])
def setp(o, k, v):
    o.modify(); o.set_editor_property(k, v)
# 1 body
manny = objs['Manny']; setp(manny, 'skeletal_mesh_asset', u.load_asset(LKB)); setp(manny, 'disable_post_process_blueprint', False)
om = list(manny.get_editor_property('override_materials'))
if any(m is not None and 'MH_MainCharacter' in m.get_path_name() for m in om):
    setp(manny, 'override_materials', u.Array(u.MaterialInterface)); rep['manny_overrides_cleared'] = [m.get_path_name() if m else None for m in om]
# 2 face
face = objs['Face']; setp(face, 'skeletal_mesh_asset', u.load_asset(FACE))
of = list(face.get_editor_property('override_materials'))
if any(m is not None and 'MH_MainCharacter' in m.get_path_name() for m in of):
    setp(face, 'override_materials', u.Array(u.MaterialInterface)); rep['face_overrides_cleared'] = [m.get_path_name() if m else None for m in of]
# 3 grooms (existing components) + HairLoose (new, under Face)
for nm in ('Hair', 'Eyebrows', 'Eyelashes'):
    g, b = GR[nm]; c = objs[nm]; setp(c, 'groom_asset', u.load_asset(g)); c.modify(); c.set_binding_asset(u.load_asset(b))
if 'HairLoose' not in objs:
    h, fail = sds.add_new_subobject(u.AddNewSubobjectParams(parent_handle=handles['Face'], new_class=u.GroomComponent, blueprint_context=bp)); assert not str(fail), str(fail)
    sds.rename_subobject(h, u.Text('HairLoose')); objs['HairLoose'] = BFL.get_object(BFL.get_data(h)); handles['HairLoose'] = h
g, b = GR['HairLoose']; c = objs['HairLoose']; setp(c, 'groom_asset', u.load_asset(g)); c.modify(); c.set_binding_asset(u.load_asset(b))
# 4 garments (skinned, following Manny)
for nm, mesh in GARM.items():
    if nm not in objs:
        h, fail = sds.add_new_subobject(u.AddNewSubobjectParams(parent_handle=handles['Manny'], new_class=u.SkeletalMeshComponent, blueprint_context=bp)); assert not str(fail), str(fail)
        sds.rename_subobject(h, u.Text(nm)); objs[nm] = BFL.get_object(BFL.get_data(h)); handles[nm] = h
    c = objs[nm]; setp(c, 'skeletal_mesh_asset', u.load_asset(mesh)); setp(c, 'use_attach_parent_bound', True)
    try:
        setp(c, 'leader_pose_component', manny); rep[nm + '_leader_set'] = True
    except Exception as e:
        rep[nm + '_leader_set'] = 'ERR ' + str(e)[:120]
for nm in ('Manny', 'Face', 'Hair', 'HairLoose', 'Eyebrows', 'Eyelashes', 'Henley', 'Shorts'): rep['after'][nm] = snap(objs[nm])
# compile + save
try:
    u.BlueprintEditorLibrary.compile_blueprint(bp); rep['compiled'] = True
except Exception as e:
    rep['compiled'] = 'ERR ' + str(e)[:120]
rep['saved'] = EAL.save_loaded_asset(bp, False)
# readback on a transient pawn instance (spawn the playable class, read, destroy)
gen = u.load_asset('/Game/GraceRanger/Experimental/BodyInertia/BP_PBI_Player').generated_class(); a = u.EditorLevelLibrary.spawn_actor_from_class(gen, u.Vector(0, 0, -100000)); rb = {}
for comp in a.get_components_by_class(u.ActorComponent):
    nm = comp.get_name()
    if isinstance(comp, u.SkeletalMeshComponent):
        m = comp.get_editor_property('skeletal_mesh_asset'); lp = comp.get_editor_property('leader_pose_component'); ac = comp.get_editor_property('anim_class'); par = comp.get_attach_parent()
        rb[nm] = {'mesh': m.get_path_name() if m else None, 'anim': ac.get_path_name() if ac else None, 'leader': lp.get_name() if lp else None, 'pp_disabled': comp.get_editor_property('disable_post_process_blueprint'), 'parent': par.get_name() if par else None}
    elif comp.get_class().get_name() == 'GroomComponent':
        g = comp.get_editor_property('groom_asset'); b = comp.get_editor_property('binding_asset'); par = comp.get_attach_parent()
        rb[nm] = {'groom': g.get_path_name() if g else None, 'binding': b.get_path_name() if b else None, 'parent': par.get_name() if par else None}
a.destroy_actor(); rep['readback_pawn'] = rb
rep['dirty_after'] = [str(p.get_path_name()) for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()][:20]
json.dump(rep, open(OUT, 'w'), indent=1)
print('GD45_PROMOTE', json.dumps({'compiled': rep['compiled'], 'saved': rep['saved'], 'leader': {k: v for k, v in rep.items() if k.endswith('_leader_set')}, 'dirty_after': rep['dirty_after'], 'rb_keys': list(rb)}), flush=True)
