"""integrity230.py (editor job, read-only): after the 2026-10-26 disk cleanup, walk the hard + soft package dependencies of the live
locomotion owners (pawn chain, ABPs, SHME component/profiles/DAs, every PoseSearch DB they reach) and report any dependency package that
no longer exists, plus counts per class. Prints INTEGRITY230 {...}."""
import unreal as u, json
AR = u.AssetRegistryHelpers.get_asset_registry()
ROOTS = ['/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase',
         '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatching',
         '/Game/GraceRanger/SHME/BP_SHM_HumanMotionComponent', '/Game/GraceRanger/SHME/DA_SHM_Response_Default',
         '/Game/GraceRanger/Profiles/DA_GR_LocomotionBehavior', '/Game/GraceRanger/Maps/L_GR_SphirusHouse']
for p in ('BP_GR_Player', 'BP_PBI_Player', 'BP_Player_MM'):
    for a in AR.get_assets_by_class(u.TopLevelAssetPath('/Script/Engine', 'Blueprint'), True) if False else []: pass
r = [a for a in AR.get_all_assets(True) if str(a.asset_name) in ('BP_GR_Player', 'BP_PBI_Player', 'BP_Player_MM')]
ROOTS += [str(a.package_name) for a in r]
opt = u.AssetRegistryDependencyOptions(include_soft_package_references=True, include_hard_package_references=True, include_searchable_names=False, include_soft_management_references=False, include_hard_management_references=False)
seen = set(); missing = []; stack = list(ROOTS)
while stack:
    p = stack.pop()
    if p in seen: continue
    seen.add(p)
    deps = AR.get_dependencies(p, opt) or []
    for d in deps:
        d = str(d)
        if not d.startswith('/Game'): continue
        if not u.EditorAssetLibrary.does_asset_exist(d) and not AR.get_assets_by_package_name(d):
            missing.append((p, d)); continue
        stack.append(d)
cls = {}
for p in seen:
    for a in AR.get_assets_by_package_name(p) or []:
        c = str(a.asset_class_path.asset_name); cls[c] = cls.get(c, 0) + 1
print('INTEGRITY230 ' + json.dumps({'roots': len(ROOTS), 'packages': len(seen), 'missing': missing[:40], 'n_missing': len(missing), 'classes': dict(sorted(cls.items(), key=lambda x: -x[1])[:20])}))
