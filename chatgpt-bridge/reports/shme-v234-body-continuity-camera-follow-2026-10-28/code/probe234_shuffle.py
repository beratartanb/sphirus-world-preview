"""probe234_shuffle.py (measure): which PoseSearch databases hold the stance-change shuffle clips (*Shuffle*) and the stop databases'
size; the ABP database variables that point at them. Prints SHUF234 {...}."""
import unreal as u, json
ar = u.AssetRegistryHelpers.get_asset_registry()
dbs = [a for a in ar.get_assets_by_class(u.TopLevelAssetPath('/Script/PoseSearch', 'PoseSearchDatabase'))]
out = {'dbs_with_shuffle': {}, 'shuffle_clips': set()}
for a in dbs:
    p = str(a.package_name)
    if not p.startswith(('/Game/GraceRanger', '/Game/ActionAdventureMovementS', '/Game/Sphirus')): continue
    d = a.get_asset(); n = d.get_num_animation_assets()
    names = [d.get_animation_asset(i).get_name() for i in range(n) if d.get_animation_asset(i)]
    sh = [x for x in names if 'Shuffle' in x]
    if sh: out['dbs_with_shuffle'][p] = {'n': n, 'shuffle': sh[:40]}; out['shuffle_clips'].update(sh)
out['shuffle_clips'] = sorted(out['shuffle_clips'])
abp = u.load_asset('/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'); cdo = u.get_default_object(abp.generated_class())
out['abp_hold_db'] = str(cdo.get_editor_property('SHM_HoldDB'))[:120]
print('SHUF234 ' + json.dumps(out, default=str))
