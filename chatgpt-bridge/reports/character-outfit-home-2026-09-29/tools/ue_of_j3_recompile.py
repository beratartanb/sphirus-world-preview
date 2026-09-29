import unreal as u
m = u.load_asset('/Game/Sphirus/CharacterLab/Outfit_Home_20260929/Materials/M_SPH_Textile'); u.MaterialEditingLibrary.recompile_material(m)
print('recompiled', u.EditorAssetLibrary.save_loaded_asset(m, False), 'stats', str(u.MaterialEditingLibrary.get_statistics(m))[:400])
