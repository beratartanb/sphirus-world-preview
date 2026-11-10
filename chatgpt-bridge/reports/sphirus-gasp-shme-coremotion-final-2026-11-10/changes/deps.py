# deps.py (read-only, commandlet on the GASP project): dependency closure of the GASP CMC sandbox player.
import unreal as u, json, os
AR=u.AssetRegistryHelpers.get_asset_registry(); AR.search_all_assets(True)
roots=['/Game/Blueprints/SandboxCharacter_CMC','/Game/Blueprints/SandboxCharacter_CMC_ABP','/Game/Blueprints/GM_Sandbox','/Game/Blueprints/PC_Sandbox','/Game/Blueprints/Cameras/BP_Camera_MainGameplay' ]
opt_h=u.AssetRegistryDependencyOptions(include_soft_package_references=False,include_hard_package_references=True,include_searchable_names=False,include_soft_management_references=False,include_hard_management_references=False)
opt_s=u.AssetRegistryDependencyOptions(include_soft_package_references=True,include_hard_package_references=False,include_searchable_names=False,include_soft_management_references=False,include_hard_management_references=False)
res={}
for mode,opt in (('hard',opt_h),('all',None)):
    seen=set(); st=[r for r in roots]
    while st:
        p=st.pop()
        if p in seen: continue
        seen.add(p)
        ds=list(AR.get_dependencies(p,opt_h) or [])
        if mode=='all': ds+=list(AR.get_dependencies(p,opt_s) or [])
        for d in ds:
            d=str(d)
            if d.startswith('/Game/') and d not in seen: st.append(d)
    res[mode]=sorted(seen)
blp=[str(a.package_name) for a in AR.get_assets_by_path('/Game/Blueprints',True)]
res['roots_exist']={r:bool(AR.get_assets_by_package_name(r)) for r in roots}
out=os.environ.get('DEPS_OUT','C:/temp/deps.json'); json.dump(res,open(out,'w'),indent=0)
print('DEPS hard',len(res['hard']),'all',len(res['all']),res['roots_exist'])
