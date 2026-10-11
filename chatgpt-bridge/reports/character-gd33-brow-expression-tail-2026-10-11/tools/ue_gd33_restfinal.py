"""GD33: the chosen calm rest pose as its own 1-second sequence AS_GD33_Rest_lid60 (CTRL_expressions_eyeUpperLidUpL/R = 0.6 constant) on the G31
face skeleton, for the evaluation Blueprint's face (looping single node). GD33 folder, refuses to overwrite."""
import unreal as u
G = '/Game/Sphirus/CharacterLab/GD33_IdentityMaster_20261011'; EAL = u.EditorAssetLibrary; path = G+'/Face/AS_GD33_Rest_lid60'; assert not EAL.does_asset_exist(path)
mesh = u.load_asset('/Game/Sphirus/CharacterLab/GD31_IdentityMaster_20261011/Face/SKM_GD31_Face_g31'); sk = mesh.skeleton
names = {str(n).lower(): str(n) for n in sk.get_curve_meta_data_names()}; V = {names['ctrl_expressions_eyeupperlidupl']: 0.6, names['ctrl_expressions_eyeupperlidupr']: 0.6}
fac = u.AnimSequenceFactory(); fac.target_skeleton = sk; fac.preview_skeletal_mesh = mesh
seq = u.AssetToolsHelpers.get_asset_tools().create_asset('AS_GD33_Rest_lid60', G+'/Face', u.AnimSequence, fac)
ctrl = seq.get_editor_property('controller'); ctrl.set_frame_rate(u.FrameRate(30, 1)); ctrl.set_number_of_frames(u.FrameNumber(30))
for k, v in V.items(): u.AnimationLibrary.add_curve(seq, k); u.AnimationLibrary.add_float_curve_keys(seq, k, [0.0, 1.0], [v, v])
print('GD33_RESTFINAL', EAL.save_loaded_asset(seq, False), sorted(V))
