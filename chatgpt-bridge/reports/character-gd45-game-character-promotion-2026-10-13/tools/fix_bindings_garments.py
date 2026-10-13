"""GD45 follow-up mutation: (1) groom bindings came back NULL at PIE on the three inherited groom components (Hair / Eyebrows / Eyelashes) while the new
HairLoose kept its binding -> inspect the child Blueprints' inherited-component overrides (BP_GR_Player, BP_PBI_Player) and set the GD38 bindings there
too (child context templates), (2) the skinned garments cannot follow Manny through a template LeaderPoseComponent (not instanced; bones stayed at the
origin in PIE) -> give Henley / Shorts the body's runtime anim class (ABP_GR_MetaHuman retarget from CharacterMesh0) so they animate like the body.
Checkpointed copies of all three Blueprints exist in Saved/Codex/GD45_Promote_20261013/checkpoint."""
import unreal as u, json
OUT = 'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Saved/Codex/GD45_Promote_20261013/data/fix.json'
sds = u.get_engine_subsystem(u.SubobjectDataSubsystem); BFL = u.SubobjectDataBlueprintFunctionLibrary; EAL = u.EditorAssetLibrary; rep = {'api': [n for n in dir(BFL) if 'object' in n.lower()]}
GR = {'Hair': ('/Game/Sphirus/CharacterLab/GD11_HairQ_20261006/Hair/GR_LK_Hair_Main_h75c', '/Game/Sphirus/CharacterLab/GD38_IdentityMaster_20261011/Face/Bindings/GB_GD38_HairMain_t38h75c'),
      'HairLoose': ('/Game/Sphirus/CharacterLab/GD11_HairQ_20261006/Hair/GR_LK_Hair_Loose_h75c', '/Game/Sphirus/CharacterLab/GD38_IdentityMaster_20261011/Face/Bindings/GB_GD38_HairLoose_t38h75c'),
      'Eyebrows': ('/Game/Sphirus/CharacterLab/GD38_IdentityMaster_20261011/Grooms/GR_GD38_BrowCustom_ds8s', '/Game/Sphirus/CharacterLab/GD38_IdentityMaster_20261011/Face/Bindings/GB_GD38_EyebrowsCustom_ds8s_t38'),
      'Eyelashes': ('/Game/Sphirus/CharacterLab/GD31_IdentityMaster_20261011/Grooms/GR_GD31_Eyelashes_S_Thin', '/Game/Sphirus/CharacterLab/GD38_IdentityMaster_20261011/Face/Bindings/GB_GD38_EyelashesS_Thin31_t38')}
ABP_BODY = '/Game/GraceRanger/Animations/ABP_GR_MetaHuman'
BPS = ['/Game/ActionAdventureMovementS/Animations/Locomotion/CoreMotionAAMS/Integrated/BP_Player_MM', '/Game/GraceRanger/BP_GR_Player', '/Game/GraceRanger/Experimental/BodyInertia/BP_PBI_Player']
def pn(v): return v.get_path_name() if v is not None and hasattr(v, 'get_path_name') else v
for bpp in BPS:
    bp = u.load_asset(bpp); r = {}
    for h in sds.k2_gather_subobject_data_for_blueprint(bp):
        d = BFL.get_data(h); o = BFL.get_object(d)
        if o is None: continue
        nm = o.get_name().replace('_GEN_VARIABLE', '')
        if nm in GR or nm in ('Henley', 'Shorts', 'Manny', 'Face'):
            e = {'outer': o.get_outer().get_name() if o.get_outer() else None}
            if o.get_class().get_name() == 'GroomComponent': e['binding'] = pn(o.get_editor_property('binding_asset')); e['groom'] = pn(o.get_editor_property('groom_asset'))
            if isinstance(o, u.SkeletalMeshComponent): e['anim_class'] = pn(o.get_editor_property('anim_class')); e['mesh'] = pn(o.get_editor_property('skeletal_mesh_asset'))
            # child-context override template, when the API exists
            try:
                oc = BFL.get_object_for_blueprint(h, bp) if hasattr(BFL, 'get_object_for_blueprint') else None
                if oc is not None and oc is not o: e['child_override_outer'] = oc.get_outer().get_name(); e['child_override_binding'] = pn(oc.get_editor_property('binding_asset')) if oc.get_class().get_name() == 'GroomComponent' else None
            except Exception as ex: e['child_override_err'] = str(ex)[:80]
            r[nm] = e
    rep[bpp.rsplit('/', 1)[-1] + '_before'] = r
# apply: bindings on the owner templates again (idempotent) and on child override templates if any; garments anim class on the owner templates
owner = u.load_asset(BPS[0]); handles = {}; objs = {}
for h in sds.k2_gather_subobject_data_for_blueprint(owner):
    o = BFL.get_object(BFL.get_data(h))
    if o is None: continue
    nm = o.get_name().replace('_GEN_VARIABLE', ''); handles[nm] = h; objs[nm] = o
for nm, (g, b) in GR.items():
    c = objs[nm]; c.modify(); c.set_editor_property('groom_asset', u.load_asset(g)); c.set_binding_asset(u.load_asset(b)); c.set_editor_property('binding_asset', u.load_asset(b))
abp = u.load_class(None, ABP_BODY + '.ABP_GR_MetaHuman_C') or u.load_asset(ABP_BODY).generated_class()
for nm in ('Henley', 'Shorts'):
    c = objs[nm]; c.modify(); c.set_editor_property('anim_class', abp); c.set_editor_property('animation_mode', u.AnimationMode.ANIMATION_BLUEPRINT); c.set_editor_property('leader_pose_component', None)
u.BlueprintEditorLibrary.compile_blueprint(owner); rep['owner_saved'] = EAL.save_loaded_asset(owner, False)
# child blueprints: if they hold override templates for the grooms, align them; then compile + save so stale inherited overrides are refreshed
for bpp in BPS[1:]:
    bp = u.load_asset(bpp); changed = []
    for h in sds.k2_gather_subobject_data_for_blueprint(bp):
        d = BFL.get_data(h); o = BFL.get_object(d)
        if o is None or o.get_class().get_name() != 'GroomComponent': continue
        nm = o.get_name().replace('_GEN_VARIABLE', '')
        if nm not in GR: continue
        try: oc = BFL.get_object_for_blueprint(h, bp) if hasattr(BFL, 'get_object_for_blueprint') else None
        except Exception: oc = None
        if oc is not None and oc is not o:
            oc.modify(); oc.set_editor_property('groom_asset', u.load_asset(GR[nm][0])); oc.set_binding_asset(u.load_asset(GR[nm][1])); changed.append(nm)
    u.BlueprintEditorLibrary.compile_blueprint(bp); rep[bpp.rsplit('/', 1)[-1] + '_child_overrides_set'] = changed; rep[bpp.rsplit('/', 1)[-1] + '_saved'] = EAL.save_loaded_asset(bp, False)
rep['dirty_after'] = [str(p.get_path_name()) for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()][:20]
json.dump(rep, open(OUT, 'w'), indent=1); print('GD45_FIX', json.dumps({k: v for k, v in rep.items() if k != 'api' and not k.endswith('_before')}), flush=True)
