# w_brake_v1.py (write, gated): BrakeDecelLow back to 380 (walk keeps its old brake; seqN V1: walk stop slide 35 -> 1-5 cm at 30/60 Hz),
# BrakeDecelHigh stays 1100 (jog ~808, sprint 1100). AC_Sph_Motion CDO + SphMotion template in BP_Sph_GASPCharacter.
import unreal as u
L = u.BlueprintEditorLibrary; EA = u.EditorAssetLibrary
def save(a):
    try: assert EA.save_loaded_asset(a, False)
    except RuntimeError as e: print('SAVE_SCRIPT_WARNING', a.get_name(), str(e)[:100])
m = u.load_asset('/Game/Sphirus/Player/Motion/AC_Sph_Motion'); md = u.get_default_object(m.generated_class()); md.set_editor_property('BrakeDecelLow', 380.0); L.compile_blueprint(m); save(m)
c = u.load_asset('/Game/Sphirus/Player/GASP/BP_Sph_GASPCharacter'); t = u.find_object(None, '/Game/Sphirus/Player/GASP/BP_Sph_GASPCharacter.BP_Sph_GASPCharacter_C:SphMotion_GEN_VARIABLE')
t.set_editor_property('BrakeDecelLow', 380.0); save(c)
print('BRAKE', md.get_editor_property('BrakeDecelLow'), md.get_editor_property('BrakeDecelHigh'), t.get_editor_property('BrakeDecelLow'), t.get_editor_property('BrakeDecelHigh'))
