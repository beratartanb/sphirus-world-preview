# w_char18.py (write, gated, manifest ue59_m18_char): persist the 2026-11-18 character changes.
#  AC_Sph_Motion: slope defaults (graph edits were made in memory through Epic MCP / Graph DSL) -> compile, save
#  BP_HybridA_Player: CharacterMovement.bUseFlatBaseForFloorChecks = False (capsule rides on its rounded base on slopes) -> compile, save
import unreal as u
EAL = u.EditorAssetLibrary; L = u.BlueprintEditorLibrary
m = u.load_asset('/Game/Sphirus/Player/Motion/AC_Sph_Motion'); mc = u.get_default_object(m.generated_class())
for k, v in dict(SlopeKUp=0.55, SlopeKDown=0.15, SlopeMaxUp=12.0, SlopeMaxDown=3.0, SlopeSlowUp=0.25, SlopeSlowDown=0.12, SlopeOn=True).items(): mc.set_editor_property(k, v)
L.compile_blueprint(m); st = str(m.get_editor_property('status')); assert 'UP_TO_DATE' in st, st
mc = u.get_default_object(m.generated_class()); print('MOTION', {k: mc.get_editor_property(k) for k in ('SlopeKUp', 'SlopeMaxUp', 'SlopeSlowUp', 'SlopeOn', 'BodyOn')})
assert EAL.save_loaded_asset(m, False)
b = u.load_asset('/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'); bc = u.get_default_object(b.generated_class())
cm = bc.get_editor_property('character_movement'); print('FLAT before', cm.get_editor_property('use_flat_base_for_floor_checks'))
cm.set_editor_property('use_flat_base_for_floor_checks', False)
L.compile_blueprint(b); st = str(b.get_editor_property('status')); assert 'UP_TO_DATE' in st, st
cm2 = u.get_default_object(b.generated_class()).get_editor_property('character_movement'); print('FLAT after compile', cm2.get_editor_property('use_flat_base_for_floor_checks'))
assert cm2.get_editor_property('use_flat_base_for_floor_checks') == False
assert EAL.save_loaded_asset(b, False)
print('DONE')
