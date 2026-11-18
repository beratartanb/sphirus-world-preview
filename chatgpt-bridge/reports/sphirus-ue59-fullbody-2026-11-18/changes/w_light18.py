# w_light18.py (write, gated, manifest ue59_m18_light): interior sun attenuation. M_Sph_SunInterior_LF rebuilt with InsideK = 0.02 and
# assigned as the light function of DirectionalLight_0 (EX_PostRain_Sun) in L_GR_SphirusHouse. Outside the house box the multiplier is 1.
import unreal as u, builtins
builtins.LF_K = 0.02
exec(open(u.Paths.project_dir() + 'Tools/UE59_20261118/m_lf_create.py', encoding='utf8').read())
mat = u.load_asset('/Game/Sphirus/Lighting/Day_20261118/M_Sph_SunInterior_LF')
W = u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world()
sun = [a for a in u.GameplayStatics.get_all_actors_of_class(W, u.DirectionalLight) if a.get_name() == 'DirectionalLight_0'][0]
c = sun.get_components_by_class(u.DirectionalLightComponent)[0]
c.set_editor_property('light_function_material', mat)
print('SUN lf', c.get_editor_property('light_function_material').get_name(), 'intensity', c.get_editor_property('intensity'))
print('MAPSAVE', u.EditorLoadingAndSavingUtils.save_packages([W.get_package()], False))
print('DONE')
