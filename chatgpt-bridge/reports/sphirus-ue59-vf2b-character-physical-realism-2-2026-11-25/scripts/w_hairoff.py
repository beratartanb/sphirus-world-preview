# w_hairoff.py (write, gated): hair simulation back OFF on the player's HairMain2 (the H6 candidate made the fringe hang over the face
# and stay there after a jolt). Simulation text is restored from the copy taken before the VF2B wire job. Garment wiring is untouched.
import unreal as u, re
assert not u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world(), 'PIE running'
P = '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'; bp = u.load_asset(P)
t0 = open(u.Paths.project_dir() + 'Saved/UE59Work/vf2b/hair_sim_before_vf2.txt').read(); assert 'bEnableSimulation=False' in t0
sds = u.get_engine_subsystem(u.SubobjectDataSubsystem); B = u.SubobjectDataBlueprintFunctionLibrary; k = 0
for h in sds.k2_gather_subobject_data_for_blueprint(bp):
    d = B.get_data(h); o = B.get_object(d)
    if o and o.get_name().replace('_GEN_VARIABLE', '') == 'HairMain2':
        c = B.get_object_for_blueprint(d, bp); ss = c.get_editor_property('simulation_settings'); ss.import_text(t0); c.set_editor_property('simulation_settings', ss); c.set_editor_property('physics_asset', None)
        t1 = c.get_editor_property('simulation_settings').export_text(); print('WHO hair', re.search(r'bEnableSimulation=\w+', t1).group(0), 'text restored', t1 == t0, 'groom', c.get_editor_property('groom_asset').get_name()); k += 1
assert k == 1
cdo = u.get_default_object(bp.generated_class()); print('WHO outfits kept', [x.get_name() if x else None for x in cdo.get_editor_property('GR_OutfitTop')][1], [x.get_name() if x else None for x in cdo.get_editor_property('GR_OutfitLow')][1])
u.BlueprintEditorLibrary.compile_blueprint(bp); print('WHO saved', u.EditorAssetLibrary.save_asset(P, only_if_is_dirty=False))
print('WHO dirty', [p.get_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()])
