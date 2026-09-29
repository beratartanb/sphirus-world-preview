import unreal as u, builtins
st = getattr(builtins, 'SPH_OF_CAPTURE', None)
if st: st['running'] = False
print('capture state reset', bool(st), [p.get_path_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()])
m = u.load_asset('/Game/Sphirus/CharacterLab/Outfit_Home_20260929/Materials/M_SPH_Textile'); print('two_sided', m.get_editor_property('two_sided'), 'shading', m.get_editor_property('shading_model'))
