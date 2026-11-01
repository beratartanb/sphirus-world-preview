import builtins
builtins.V242_IDB = {'dry': False, 'clips': ['/Game/GraceRanger/SHME/Animations/V242/SHM243_Idle_Weighted2'], 'name': 'PSD_SHM242_IdleB'}
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V242_20261101/build242_idledb.py', encoding='utf-8').read(), 'build242_idledb.py', 'exec'), {'__name__': '__job__'})
# the misnamed first build (PSD_SHM243_Idle: the V2.42 hook keeps its override only while the selected DB name contains 'SHM242_Idle';
# a non-conforming name flip-flops the search every frame) is removed so it cannot be referenced again; its backup is in manifest v243_idle2.
import unreal as u, json
OLD = '/Game/GraceRanger/SHME/Animations/V242/PSD_SHM243_Idle'
refs = u.EditorAssetLibrary.find_package_referencers_for_asset(OLD, False) if u.EditorAssetLibrary.does_asset_exist(OLD) else []
ok = (u.EditorAssetLibrary.delete_asset(OLD) if (u.EditorAssetLibrary.does_asset_exist(OLD) and not refs) else None)
print('DEL243 ' + json.dumps({'old': OLD, 'referencers': [str(r) for r in refs], 'deleted': ok, 'exists_after': u.EditorAssetLibrary.does_asset_exist(OLD)}))
