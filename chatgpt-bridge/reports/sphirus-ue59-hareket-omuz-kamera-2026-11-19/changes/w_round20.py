# w_round20.py (write, gated, manifest ue59_m20_round): persist the 2026-11-19 screened values.
# 1 ABP_Sph_Body_GASP relax terms (R2): VW_ (MoveA) + VD_ (RelA) on clavicles, upper arms, spine_05
# 2 brake: BrakeDecelLow 380->500, BrakeDecelHigh 780->1100 (AC_Sph_Motion CDO + the SphMotion template in BP_Sph_GASPCharacter)
#   jog 415 brakes ~860 cm/s2 like the Relaxed run stop clip; sprint 1100 (stop clips brake 900-1650)
# 3 ABP_Sph_GASP remap: Relaxed_Stand_Sprint_Stops -> Dense_Stand_Run_Stops (sprint release uses the Neutral run stop: pelvis
#   drop 31 -> 12 cm, slide 62-73 -> 18-20 cm in seqF F4)
import unreal as u
exec(open(u.Paths.project_dir()+'Tools/UE59_20261119/b59.py',encoding='utf8').read())
L = u.BlueprintEditorLibrary; EA = u.EditorAssetLibrary
def save(a):
    try: assert EA.save_loaded_asset(a, False)
    except RuntimeError as e: print('SAVE_SCRIPT_WARNING', a.get_name(), str(e)[:120])
a = u.load_asset('/Game/Sphirus/Player/GASP/ABP_Sph_Body_GASP'); d = u.get_default_object(a.generated_class())
V = {'VW_ClavL': (0, -3, 3), 'VW_ClavR': (0, 3, -3), 'VW_ArmL': (0, -3, 0), 'VW_ArmR': (0, 3, 0), 'VW_Spine5': (4, 0, 0),
     'VD_ClavL': (0, -3, 2), 'VD_ClavR': (0, 3, -2), 'VD_ArmL': (0, -5, 0), 'VD_ArmR': (0, 5, 0), 'VD_Spine5': (0, 0, 0)}
for k, v in V.items(): d.set_editor_property(k, u.Vector(*v))
L.compile_blueprint(a); save(a); d = u.get_default_object(a.generated_class()); print('BODY', {k: str(d.get_editor_property(k)) for k in V})
m = u.load_asset('/Game/Sphirus/Player/Motion/AC_Sph_Motion'); md = u.get_default_object(m.generated_class())
md.set_editor_property('BrakeDecelLow', 500.0); md.set_editor_property('BrakeDecelHigh', 1100.0); L.compile_blueprint(m); save(m)
c = u.load_asset('/Game/Sphirus/Player/GASP/BP_Sph_GASPCharacter'); t = u.find_object(None, '/Game/Sphirus/Player/GASP/BP_Sph_GASPCharacter.BP_Sph_GASPCharacter_C:SphMotion_GEN_VARIABLE')
t.set_editor_property('BrakeDecelLow', 500.0); t.set_editor_property('BrakeDecelHigh', 1100.0); save(c)
print('BRAKE', md.get_editor_property('BrakeDecelLow'), md.get_editor_property('BrakeDecelHigh'), t.get_editor_property('BrakeDecelLow'), t.get_editor_property('BrakeDecelHigh'))
R = '/Game/Characters/UEFN_Mannequin/Animations/MotionMatchingData/Databases/'
k = u.load_asset(R + 'Relaxed/PSD_Relaxed_Stand_Sprint_Stops'); v = u.load_asset(R + 'Dense/PSD_Dense_Stand_Run_Stops'); assert k and v
g = u.load_asset('/Game/Sphirus/Player/GASP/ABP_Sph_GASP'); gd = u.get_default_object(g.generated_class())
ks = list(gd.get_editor_property('CM_Keys')); vs = list(gd.get_editor_property('CM_Vals')); names = [x.get_path_name() for x in ks]
if k.get_path_name() in names: vs[names.index(k.get_path_name())] = v
else: ks.append(k); vs.append(v)
gd.set_editor_property('CM_Keys', ks); gd.set_editor_property('CM_Vals', vs); L.compile_blueprint(g); save(g)
gd = u.get_default_object(g.generated_class()); print('REMAP', len(gd.get_editor_property('CM_Keys')), gd.get_editor_property('CM_Keys')[-1].get_name(), '->', gd.get_editor_property('CM_Vals')[-1].get_name())
print('DIRTY', [p.get_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]); print('DONE')
