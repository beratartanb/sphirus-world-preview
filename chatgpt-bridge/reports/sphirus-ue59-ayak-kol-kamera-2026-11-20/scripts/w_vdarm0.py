# w_vdarm0.py (write, gated, 2026-11-19 late): slow-down upper-arm term VD_ArmL/R -> 0 (seqW vd0: abduction 6.7-7.8 deg vs walk 9 in the first second; the shortened transition no longer needs it).
# With the run->walk transition window cut to 0.6 s the walk loop arms arrive ~0.5 s after the release and the old term then
# closed the arms past the walk carriage (abduction 3 deg vs walk 9 in the 0.5-1.0 s window, A_jw10_w06); seqW vda: 8.5 deg.
import unreal as u
L = u.BlueprintEditorLibrary; EA = u.EditorAssetLibrary
a = u.load_asset('/Game/Sphirus/Player/GASP/ABP_Sph_Body_GASP'); d = u.get_default_object(a.generated_class())
d.set_editor_property('VD_ArmL', u.Vector(0, 0, 0)); d.set_editor_property('VD_ArmR', u.Vector(0, 0, 0))
L.compile_blueprint(a)
try: EA.save_loaded_asset(a, False)
except RuntimeError as e: print('SAVE_SCRIPT_WARNING', str(e)[:100])
print('VDARM', d.get_editor_property('VD_ArmL'), d.get_editor_property('VD_ArmR'), d.get_editor_property('VD_ForeL'), d.get_editor_property('VD_ForeR'))
