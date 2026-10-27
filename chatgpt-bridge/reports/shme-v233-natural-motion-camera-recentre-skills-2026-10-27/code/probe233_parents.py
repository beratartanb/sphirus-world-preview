"""probe233_parents.py (measure): ParentClass chain of the pawn BPs from asset registry tags. Prints PARENTS233 {...}."""
import unreal as u, json
AR = u.AssetRegistryHelpers.get_asset_registry()
def parent(pkg):
    for a in AR.get_assets_by_package_name(pkg):
        for k in ('ParentClass', 'NativeParentClass'):
            v = a.get_tag_value(k)
            if v: return str(v)
    return None
chain = {}
cands = [str(a.package_name) for a in AR.get_assets(u.ARFilter(class_paths=[u.TopLevelAssetPath('/Script/Engine', 'Blueprint')], package_paths=['/Game/GraceRanger', '/Game/ActionAdventureMovementS'], recursive_paths=True)) if str(a.asset_name) in ('BP_PBI_Player', 'BP_GR_Player', 'BP_Player_MM')]
chain['cands'] = cands
pkg = [c for c in cands if c.endswith('BP_PBI_Player')][0]
for i in range(8):
    p = parent(pkg); chain[pkg] = p
    if not p: break
    if p.split("'")[1 if "'" in p else 0].startswith('/Script/'): break
    pkg = p.split("'")[1].split('.')[0] if "'" in p else p.split('.')[0]
print('PARENTS233 ' + json.dumps(chain))
