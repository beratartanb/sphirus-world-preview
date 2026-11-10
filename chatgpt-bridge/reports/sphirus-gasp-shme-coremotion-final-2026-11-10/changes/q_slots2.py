import unreal as u
AR=u.AssetRegistryHelpers.get_asset_registry()
for a in AR.get_assets_by_path('/Game/Sphirus/Player/Anim',True):
    if str(a.asset_class_path.asset_name)!='AnimMontage': continue
    m=u.load_asset(str(a.package_name))
    try: sl=[str(t.get_editor_property('slot_name')) for t in m.get_editor_property('slot_anim_tracks')]
    except Exception as e: sl=['ERR '+str(e)[:60]]
    print('SLOT',str(a.package_name).split('/')[-1],sl)
