import unreal as u
o=[]; W=o.append; ME=u.MaterialEditingLibrary
def dump(p, deep=True):
    m=u.load_asset(p)
    if not m: W('MISSING '+p); return
    chain=[]; x=m
    while isinstance(x,u.MaterialInstance): chain.append(x.get_name()); x=x.get_editor_property('parent')
    W('== %s | chain %s -> %s'%(p.split('/')[-1],' > '.join(chain), x.get_path_name() if x else None))
    if isinstance(x,u.Material):
        try: W('   base: shading %s | blend %s | sss profile %s'%(x.get_editor_property('shading_model'), x.get_editor_property('blend_mode'), x.get_editor_property('subsurface_profile')))
        except Exception as e: W('   base err '+repr(e)[:80])
    if isinstance(m,u.MaterialInstanceConstant):
        try: W('   sss override %s %s'%(m.get_editor_property('override_subsurface_profile'), m.get_editor_property('subsurface_profile')))
        except Exception as e: pass
        for n in ME.get_scalar_parameter_names(m): W('   S %s = %s'%(n, round(ME.get_material_instance_scalar_parameter_value(m,n),4)))
        for n in ME.get_vector_parameter_names(m):
            v=ME.get_material_instance_vector_parameter_value(m,n); W('   V %s = (%.3f,%.3f,%.3f,%.3f)'%(n,v.r,v.g,v.b,v.a))
        for n in ME.get_texture_parameter_names(m):
            t=ME.get_material_instance_texture_parameter_value(m,n); 
            try: W('   T %s = %s [%sx%s lodbias %s]'%(n, t.get_name() if t else None, t.blueprint_get_size_x() if t else '', t.blueprint_get_size_y() if t else '', t.get_editor_property('lod_bias') if t else ''))
            except Exception as e: W('   T %s = %s'%(n, t.get_name() if t else None))
        try:
            for n in ME.get_static_switch_parameter_names(m): W('   B %s = %s'%(n, ME.get_material_instance_static_switch_parameter_value(m,n)))
        except Exception as e: pass
for p in ('/Game/Sphirus/CharacterLab/Sph_20261108/Skin/MI_Sph8_Head_LOD1_VT','/Game/Sphirus/CharacterLab/Day_20261107/Skin/MI_Sph_Body_Home','/Game/Grooms/001_Messy_Bob/001_Messy_Bob/MI_001_Messy_Bob','/Game/Sphirus/CharacterLab/Sph_20261108/Built/MHC_Sph8/Face/Materials/MI_EyeL_Baked','/Game/Sphirus/CharacterLab/Sph_20261108/Built/MHC_Sph8/Face/Materials/MI_Face_EyeShell','/Game/Sphirus/CharacterLab/Sph_20261108/Built/MHC_Sph8/Face/Materials/MI_Face_LacrimalFluid'):
    dump(p)
open(u.Paths.project_dir()+'Saved/UE59Work/cr1/audit2.txt','w',encoding='utf8').write('\n'.join(o)); print('AUDIT2',len(o))
