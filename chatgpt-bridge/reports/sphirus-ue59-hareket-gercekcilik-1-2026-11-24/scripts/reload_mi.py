# reload_mi.py (control): reload the saved material instances FROM DISK inside the running editor and read the values (persistence check).
import unreal as u
ME=u.MaterialEditingLibrary
T={'/Game/Sphirus/CharacterLab/Sph_20261108/Skin/MI_Sph8_Head_LOD1_VT':('Micro Skin Normal Strength','Normal Flatten','Scatter Distance Global Multiply Post-Bake','Roughness Global Multiply Post-Bake','Micro Skin Cavity Specular Multiply'),
   '/Game/Sphirus/CharacterLab/Day_20261107/Skin/MI_Sph_Body_Home':('Micro Skin Normal Strength','Normal Flatten','Scatter Distance Global Multiply Post-Bake'),
   '/Game/Sphirus/CharacterLab/Sph_20261108/Built/MHC_Sph8/Face/Materials/MI_EyeL_Baked':('Iris Global Saturation','Iris Primary Color Value','Fake Reflection Intensity'),
   '/Game/Sphirus/CharacterLab/GD35_IdentityMaster_20261011/Looks/MI_GD35_BrowS_n4':('Desat','hairRedness','hairMelanin')}
ps=[u.find_package(p) for p in T]; print('RELOAD',u.EditorLoadingAndSavingUtils.reload_packages([p for p in ps if p]))
for p,ns in T.items():
    m=u.load_asset(p); print('DISKMI',p.split('/')[-1],{n:round(ME.get_material_instance_scalar_parameter_value(m,n),3) for n in ns})
