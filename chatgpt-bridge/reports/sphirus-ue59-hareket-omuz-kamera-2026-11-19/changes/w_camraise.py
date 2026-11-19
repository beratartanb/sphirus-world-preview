# w_camraise.py (write, gated): AC_Sph_Camera TightRaise default 45 cm (seqJ: tr45 keeps the room readable above the head when blocked)
import unreal as u
L = u.BlueprintEditorLibrary; EA = u.EditorAssetLibrary
a = u.load_asset('/Game/Sphirus/Player/Camera/AC_Sph_Camera'); d = u.get_default_object(a.generated_class()); d.set_editor_property('TightRaise', 45.0)
L.compile_blueprint(a)
try: EA.save_loaded_asset(a, False)
except RuntimeError as e: print('SAVE_SCRIPT_WARNING', str(e)[:120])
print('TIGHTRAISE', u.get_default_object(a.generated_class()).get_editor_property('TightRaise'))
for p in ('/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player', '/Game/Sphirus/Player/GASP/BP_Sph_GASPCharacter'):
    bp = u.load_asset(p); sub = u.get_engine_subsystem(u.SubobjectDataSubsystem)
    for h in sub.k2_gather_subobject_data_for_blueprint(bp):
        o = u.SubobjectDataBlueprintFunctionLibrary.get_object(u.SubobjectDataBlueprintFunctionLibrary.get_data(h))
        if o and o.get_name().startswith('SphCamera'): print('TEMPLATE', p.split('/')[-1], o.get_path_name(), o.get_editor_property('TightRaise'))
print('DIRTY', [p.get_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()])
