import unreal as u, json, os
AR=u.AssetRegistryHelpers.get_asset_registry(); AR.search_all_assets(True)
opt=u.AssetRegistryDependencyOptions(include_soft_package_references=False,include_hard_package_references=True,include_searchable_names=False,include_soft_management_references=False,include_hard_management_references=False)
roots=['/Game/MetaHumans/Common/Common/Rigs/RTG_UEFN_to_Metahuman_nrw','/Game/MetaHumans/Common/Common/RTG_metahuman']
seen=set(); st=list(roots)
while st:
    p=st.pop()
    if p in seen: continue
    seen.add(p)
    for d in AR.get_dependencies(p,opt) or []:
        d=str(d)
        if d.startswith('/Game/'): st.append(d)
json.dump(sorted(seen),open('C:/Users/berat/SphirusStaging/rtg_deps.json','w'),indent=0); print('RTGDEPS',len(seen))
for r in roots:
    a=u.load_asset(r); 
    try: print('RTG',r,'src',a.get_editor_property('source_ik_rig_asset').get_path_name(),'tgt',a.get_editor_property('target_ik_rig_asset').get_path_name())
    except Exception as e: print('RTG',r,str(e)[:120])
