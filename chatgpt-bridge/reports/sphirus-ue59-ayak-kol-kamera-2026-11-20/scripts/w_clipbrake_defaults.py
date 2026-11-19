# w_clipbrake_defaults.py (write, gated, 2026-11-19 evening): clip-bound stop brake ON. AC_Sph_Motion CDO + SphMotion template in
# BP_Sph_GASPCharacter: ClipBrakeOn True, ClipK 1.0, ClipMin 100, ClipMax 3000 (seqR CBA/CBAV runs, 30/60 Hz + variable step).
import unreal as u
L = u.BlueprintEditorLibrary; EA = u.EditorAssetLibrary
V = {'ClipBrakeOn': True, 'ClipK': 1.0, 'ClipMin': 100.0, 'ClipMax': 3000.0}
def save(a):
    try: assert EA.save_loaded_asset(a, False)
    except RuntimeError as e: print('SAVE_SCRIPT_WARNING', a.get_name(), str(e)[:100])
m = u.load_asset('/Game/Sphirus/Player/Motion/AC_Sph_Motion'); md = u.get_default_object(m.generated_class())
for k, v in V.items(): md.set_editor_property(k, v)
L.compile_blueprint(m); save(m)
c = u.load_asset('/Game/Sphirus/Player/GASP/BP_Sph_GASPCharacter'); t = u.find_object(None, '/Game/Sphirus/Player/GASP/BP_Sph_GASPCharacter.BP_Sph_GASPCharacter_C:SphMotion_GEN_VARIABLE')
for k, v in V.items(): t.set_editor_property(k, v)
save(c)
print('CLIPDEF', {k: md.get_editor_property(k) for k in V}, {k: t.get_editor_property(k) for k in V}, 'low/high', md.get_editor_property('BrakeDecelLow'), md.get_editor_property('BrakeDecelHigh'))
