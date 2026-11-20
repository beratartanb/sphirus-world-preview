# w_round3_save.py (write, gated): strafe start databases without "reface" starts + round-3 defaults/maps + save of the in-memory
# Blueprint edits (m_stk_mcp, m_player3_mcp, m_tickpre_mcp, c_abp_int).
# Why the databases: backward / sideways (strafe) starts were mapped to PSD_Dense_Stand_<gait>_Starts, which also holds the
# Reface_Start_F_* clips (turn around and walk forward). A walk start with S selected Reface_Start_F_L_180 for 0.4 s (planted foot
# 26 cm). PSD_Sph_N_<gait>_S_Starts hold only M_Neutral_<gait>_Start_* (populated by a SphN_ BranchIn notify track per clip).
import unreal as u, re, builtins
EA=u.EditorAssetLibrary; AL=u.AnimationLibrary; AT=u.AssetToolsHelpers.get_asset_tools()
B='/Game/Characters/UEFN_Mannequin/Animations/MotionMatchingData/Databases/Dense/PSD_Dense_Stand_'; D='/Game/Sphirus/Player/GASP/DB'
f=u.DataAssetFactory(); f.set_editor_property('data_asset_class',u.PoseSearchDatabase)
for g in ('Walk','Run'):
    name='PSD_Sph_N_%s_S_Starts'%g; s=u.load_asset(B+g+'_Starts'); assert s
    clips=[s.get_animation_asset(i) for i in range(s.get_num_animation_assets())]; clips=[c for c in clips if c and re.search(r'^M_Neutral_%s_Start_'%g,c.get_name())]; assert clips
    db=u.load_asset(D+'/'+name) if EA.does_asset_exist(D+'/'+name) else AT.create_asset(name,D,u.PoseSearchDatabase,f)
    for k in ('schema','continuing_pose_cost_bias','base_cost_bias','looping_cost_bias','tags','normalization_set','pose_search_mode'):
        try: db.set_editor_property(k,s.get_editor_property(k))
        except Exception as e: print('PROP',name,k,str(e)[:80])
    assert EA.save_loaded_asset(db,False); tr='SphN_%s_S_Starts'%g
    for a in clips:
        if tr in [str(t) for t in AL.get_animation_notify_track_names(a)]: AL.remove_animation_notify_track(a,tr)
        AL.add_animation_notify_track(a,tr); st=AL.add_animation_notify_state_event(a,tr,0.0,float(a.get_play_length()),u.AnimNotifyState_PoseSearchBranchIn)
        st.set_editor_property('database',db); assert EA.save_loaded_asset(a,False)
    assert EA.save_loaded_asset(db,False)
    got=sorted(db.get_animation_asset(i).get_name() for i in range(db.get_num_animation_assets()) if db.get_animation_asset(i))
    print('DB',name,len(clips),len(got),got==sorted(c.get_name() for c in clips))
R_='PSD_Relaxed_Stand_'; WS=D+'/PSD_Sph_N_Walk_S_Starts'; RS=D+'/PSD_Sph_N_Run_S_Starts'
M={R_+'Run_Stops':(None,'/Game/Sphirus/Player/GASP/CM/DB/PSD_CM_Jog_Stops')}
for d_ in ('B','LL','RL'):
    M[R_+'Walk_%s_Starts'%d_]=(WS,WS); M[R_+'Run_%s_Starts'%d_]=(RS,None)
builtins.R3_MAP=M
exec(open(u.Paths.project_dir()+'Tools/UE59_20261120/c_round3.py',encoding='utf8').read())
for p in ('/Game/Sphirus/Player/Motion/AC_Sph_Motion','/Game/Sphirus/Player/GASP/BP_Sph_GASPCharacter','/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player','/Game/Sphirus/Player/GASP/ABP_Sph_GASP'):
    a=u.load_asset(p)
    try: print('SAVE',p.split('/')[-1],EA.save_loaded_asset(a,False))
    except Exception as e: print('SAVE_EXC',p.split('/')[-1],repr(e)[:90])
print('DIRTY',[x.get_name() for x in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()])
