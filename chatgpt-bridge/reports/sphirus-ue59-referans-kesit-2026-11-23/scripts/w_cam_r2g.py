# w_cam_r2g.py (write, gated): AC_Sph_Camera class defaults for the R04 head-to-hip framing (2026-11-23 reference-to-game pass).
# old: OutD 124, OutDTight 108, HomeD 98, HomeDTight 86, HeadX 0.34, HeadY 0.33. FOV, lag, speed arm, context stations unchanged.
import unreal as u
V = {'OutD': 165.0, 'OutDTight': 135.0, 'HomeD': 118.0, 'HomeDTight': 98.0, 'HeadX': 0.30, 'HeadY': 0.24}
L = u.BlueprintEditorLibrary; EA = u.EditorAssetLibrary
a = u.load_asset('/Game/Sphirus/Player/Camera/AC_Sph_Camera'); d = u.get_default_object(a.generated_class())
for k, v in V.items(): d.set_editor_property(k, v)
L.compile_blueprint(a); d = u.get_default_object(a.generated_class())
for k, v in V.items(): d.set_editor_property(k, v)
try: r = EA.save_loaded_asset(a, False)
except Exception as e: r = 'SAVE_EXC ' + repr(e)[:160]
print('SAVE_CAM', r, {k: round(u.get_default_object(a.generated_class()).get_editor_property(k), 3) for k in V})
for p in ('/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player', '/Game/Sphirus/Player/GASP/BP_Sph_GASPCharacter'):
    bp = u.load_asset(p); sub = u.get_engine_subsystem(u.SubobjectDataSubsystem)
    for h in sub.k2_gather_subobject_data_for_blueprint(bp):
        o = u.SubobjectDataBlueprintFunctionLibrary.get_object(u.SubobjectDataBlueprintFunctionLibrary.get_data(h))
        if o and o.get_name().startswith('SphCamera'): print('TEMPLATE', p.split('/')[-1], {k: round(o.get_editor_property(k), 3) for k in V})
print('DIRTY', [x.get_name() for x in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()], [x.get_name() for x in u.EditorLoadingAndSavingUtils.get_dirty_map_packages()])
