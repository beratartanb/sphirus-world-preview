# probe_turncurves.py (read-only): movedata_speed profile of turn / pivot clips (value every 0.1 s, time and value of the minimum)
import unreal as u
AR=u.AssetRegistryHelpers.get_asset_registry(); L=u.AnimationLibrary; o=[]
want=['M_Neutral_Run_Start_F_Lfoot','M_Neutral_Run_Start_F_Rfoot','M_Neutral_Walk_Start_F_Rfoot','M_Neutral_Walk_Start_F_Lfoot','M_Relaxed_Sprint_Start_F_Lfoot','M_Neutral_Run_Diamond_F_BR_Rfoot','M_Neutral_Run_Reface_Start_F_R_090','CM_af_Loco_Jog_Fwd_Start','M_Relaxed_Run_Stop_F_Rfoot','M_Relaxed_Run_Stop_F_Lfoot']
f=u.ARFilter(class_paths=[u.TopLevelAssetPath('/Script/Engine','AnimSequence')],package_paths=['/Game'],recursive_paths=True)
for ad in AR.get_assets(f):
    n=str(ad.asset_name)
    if n in want:
        s=u.load_asset(str(ad.package_name)); d=s.get_play_length()
        try:
            ts,vs=L.get_float_keys(s,'movedata_speed')
            def val(t):
                i=min(range(len(ts)),key=lambda k:abs(ts[k]-t)); return vs[i]
            mi=min(range(len(vs)),key=lambda k:vs[k])
            o.append('%-36s len %.2f min %.0f @ %.2f | %s'%(n,d,vs[mi],ts[mi],' '.join('%.0f'%val(k*0.1) for k in range(0,int(min(d,1.6)*10)+1))))
        except Exception as e: o.append('%s ERR %s'%(n,str(e)[:80]))
print('TURNCURVES\n'+'\n'.join(sorted(set(o))))
