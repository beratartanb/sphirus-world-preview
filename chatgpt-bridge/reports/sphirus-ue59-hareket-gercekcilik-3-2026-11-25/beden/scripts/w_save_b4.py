# w_save_b4.py (write, gated): B4 body form wiring (c_b4_wire) + pass-3 defaults, then saves AC_Sph_Motion, AC_Sph_Camera, BP_HybridA_Player.
import unreal as u
exec(open(u.Paths.project_dir()+'Tools/UE59_20261124/c_b4_wire.py',encoding='utf8').read())
c=u.get_default_object(u.load_asset('/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player').generated_class())
assert 'B4' in c.get_editor_property('GR_OutfitTop')[1].get_name()
exec(open(u.Paths.project_dir()+'Tools/UE59_20261124/w_save_mr3.py',encoding='utf8').read())
