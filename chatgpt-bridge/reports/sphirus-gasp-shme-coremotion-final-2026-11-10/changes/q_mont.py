# q_mont.py (read-only): skeleton of every montage the stations / player use, and of their animation tracks.
import unreal as u
AR=u.AssetRegistryHelpers.get_asset_registry()
ms=[str(a.package_name) for a in AR.get_assets_by_path('/Game/Sphirus/Player/Anim',True) if str(a.asset_class_path.asset_name)=='AnimMontage']
for p in sorted(ms):
    m=u.load_asset(p); sk=m.get_editor_property('skeleton')
    print('MONT',p.replace('/Game/Sphirus/Player/Anim/',''),'skel',sk.get_name() if sk else None,'len',round(m.get_play_length(),2))
for p in ('/Game/Characters/UEFN_Mannequin/Meshes/SK_UEFN_Mannequin','/Game/MC_Core_Motion/Demo/Characters/MCPaul/Meshes/SK_MCPaul_Skeleton'):
    s=u.load_asset(p)
    try: print('COMPAT',s.get_name(),[x.get_name() for x in s.get_editor_property('compatible_skeletons')])
    except Exception as e: print('COMPAT ERR',str(e)[:120])
