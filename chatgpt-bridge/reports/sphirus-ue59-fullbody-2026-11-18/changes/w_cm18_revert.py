# w_cm18_revert.py (write, gated): remove the Relaxed_Stand_Sprint_Stops -> Dense remap again (T_JSTOP: less crouch but 2x foot slide)
import unreal as u
L = u.BlueprintEditorLibrary; EAL = u.EditorAssetLibrary
a = u.load_asset('/Game/Sphirus/Player/GASP/ABP_Sph_GASP'); c = u.get_default_object(a.generated_class())
ks = list(c.get_editor_property('CM_Keys')); vs = list(c.get_editor_property('CM_Vals'))
keep = [(k, v) for k, v in zip(ks, vs) if not k.get_name() == 'PSD_Relaxed_Stand_Sprint_Stops']
c.set_editor_property('CM_Keys', [k for k, _ in keep]); c.set_editor_property('CM_Vals', [v for _, v in keep])
L.compile_blueprint(a); assert 'UP_TO_DATE' in str(a.get_editor_property('status'))
print('REVERTED', len(ks), '->', len(u.get_default_object(a.generated_class()).get_editor_property('CM_Keys'))); assert EAL.save_loaded_asset(a, False); print('DONE')
