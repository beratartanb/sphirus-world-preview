# VF2B write job: wire the refitted top, the re-materialed shorts and hair simulation H6 into the player Blueprint.
# builtins.VF2B_WIRE = 'vf2' (default) | 'revert' (exact previous pointers, simulation off). Motion layers, ABPs, AC_Sph_Motion untouched.
import unreal as u, re, builtins
E = u.EditorAssetLibrary
assert not u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world(), 'PIE running'
which = getattr(builtins, 'VF2B_WIRE', 'vf2')
G0 = '/Game/Sphirus/CharacterLab/Day_20261107/Garments/'; G1 = '/Game/Sphirus/CharacterLab/VF2_20261124/Garments/'
top0 = u.load_asset(G0 + 'SKM_Sph_RetroTop'); top1 = u.load_asset(G1 + 'SKM_Sph_RetroTop_VF2'); sh0 = u.load_asset(G0 + 'SKM_Sph_CuffedShorts')
SP = G1 + 'SKM_Sph_CuffedShorts_VF2'
if which == 'vf2' and not E.does_asset_exist(SP):
    assert E.duplicate_asset(G0 + 'SKM_Sph_CuffedShorts', SP)
sh1 = u.load_asset(SP) if E.does_asset_exist(SP) else None
if which == 'vf2':
    ms = list(sh1.materials); mi = u.load_asset(G1 + 'MI_Sph_CuffedShorts_VF2')
    for x in ms: x.material_interface = mi
    sh1.materials = ms; print('WC shorts copy saved', E.save_loaded_asset(sh1, False), [x.material_interface.get_name() for x in sh1.materials])
P = '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'
bp = u.load_asset(P); cdo = u.get_default_object(bp.generated_class())
a, b = (top0, top1) if which == 'vf2' else (top1, top0); c_, d_ = (sh0, sh1) if which == 'vf2' else (sh1, sh0)
tp = list(cdo.get_editor_property('GR_OutfitTop')); lw = list(cdo.get_editor_property('GR_OutfitLow'))
print('WC before top', [x.get_name() if x else None for x in tp], 'low', [x.get_name() if x else None for x in lw])
tp = [b if x == a else x for x in tp]; lw = [d_ if x == c_ else x for x in lw]
cdo.set_editor_property('GR_OutfitTop', tp); cdo.set_editor_property('GR_OutfitLow', lw)
print('WC after  top', [x.get_name() if x else None for x in tp], 'low', [x.get_name() if x else None for x in lw])
SIM = {'bEnableSimulation=False': 'bEnableSimulation=True', 'LinearVelocityScale=[0-9.]+': 'LinearVelocityScale=0.450000', 'AngularVelocityScale=[0-9.]+': 'AngularVelocityScale=0.750000',
       'AirDrag=[0-9.]+': 'AirDrag=0.020000', 'BendDamping=[0-9.]+': 'BendDamping=0.150000', 'BendStiffness=[0-9.]+': 'BendStiffness=0.400000',
       'StretchDamping=[0-9.]+': 'StretchDamping=0.050000', 'CollisionRadius=[0-9.]+': 'CollisionRadius=0.300000'}
sds = u.get_engine_subsystem(u.SubobjectDataSubsystem); B = u.SubobjectDataBlueprintFunctionLibrary; k = 0
for h in sds.k2_gather_subobject_data_for_blueprint(bp):
    d = B.get_data(h); o = B.get_object(d)
    if not o: continue
    n = o.get_name().replace('_GEN_VARIABLE', '')
    if n == 'Henley':
        c = B.get_object_for_blueprint(d, bp)
        if c.get_skeletal_mesh_asset() == a: c.set_skeletal_mesh_asset(b)
        print('WC Henley default', c.get_skeletal_mesh_asset().get_name()); k += 1
    if n == 'HairMain2':
        c = B.get_object_for_blueprint(d, bp); ss = c.get_editor_property('simulation_settings'); t0 = ss.export_text()
        open(u.Paths.project_dir() + 'Saved/UE59Work/vf2b/hair_sim_before_%s.txt' % which, 'w').write(t0)
        if which == 'vf2':
            t = t0
            for x, y in SIM.items():
                t2 = re.sub(x, y, t); print('WC sim', y, 'ok' if (t2 != t or y in t) else 'NOCHANGE'); t = t2
            ss.import_text(t); c.set_editor_property('simulation_settings', ss)
            c.set_editor_property('physics_asset', u.load_asset('/Game/Sphirus/CharacterLab/Hazel_20261106/Common/Face/PHYS_Face'))
        else:
            ss.import_text(re.sub('bEnableSimulation=True', 'bEnableSimulation=False', t0)); c.set_editor_property('simulation_settings', ss)
        t1 = c.get_editor_property('simulation_settings').export_text()
        print('WC hair', re.search(r'bEnableSimulation=\w+', t1).group(0), re.search(r'BendStiffness=[0-9.]+', t1).group(0), 'phys', c.get_editor_property('physics_asset').get_name() if c.get_editor_property('physics_asset') else None,
              'groom', c.get_editor_property('groom_asset').get_name()); k += 1
assert k == 2, k
u.BlueprintEditorLibrary.compile_blueprint(bp)
print('WC saved', E.save_asset(P, only_if_is_dirty=False))
print('WC dirty', [p.get_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()], [p.get_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_map_packages()])
