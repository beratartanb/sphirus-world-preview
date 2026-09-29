import unreal as u
m = u.load_asset('/Game/Sphirus/CharacterLab/CharacterFinal_20260929/Outfit/Materials/M_SPH_Textile'); u.MaterialEditingLibrary.recompile_material(m)
print('recompiled', u.EditorAssetLibrary.save_loaded_asset(m, False), 'stats', str(u.MaterialEditingLibrary.get_statistics(m))[:400])
