import unreal as u
ar=u.AssetRegistryHelpers.get_asset_registry()
out=[]
for n in ('PSD_Relaxed_Stand_Run_F_Turns','PSD_Dense_Stand_Run_Pivots','PSD_Sph_N_Run_S_Starts'):
    for a in ar.get_assets_by_class(u.TopLevelAssetPath('/Script/PoseSearch','PoseSearchDatabase')):
        if str(a.asset_name)==n:
            d=a.get_asset(); s=d.get_editor_property('schema'); out.append('%s | %s | schema %s'%(n,a.package_name,s.get_path_name()))
            for p in ('continuing_pose_cost_bias','base_cost_bias','looping_cost_bias','pose_search_mode'):
                try: out.append('   %s %s'%(p,d.get_editor_property(p)))
                except Exception as e: out.append('   %s ERR'%p)
            try:
                for c in s.get_editor_property('channels'):
                    out.append('   ch %s w %s'%(c.get_class().get_name(), c.get_editor_property('weight') if hasattr(c,'get_editor_property') else '?'))
                    for q in ('bone','sample_time_offset','sampled_bones','samples','origin_bone','component_stripping','permutation_time_type'):
                        try: out.append('       %s %s'%(q,str(c.get_editor_property(q))[:300]))
                        except Exception: pass
            except Exception as e: out.append('   channels ERR %s'%e)
            try:
                aa=d.get_editor_property('animation_assets') if False else None
            except Exception: pass
open(u.Paths.project_dir()+'Saved/UE59Work/r8/psd_probe.txt','w',encoding='utf8').write('\n'.join(out)); print('PSDPROBE',len(out))
