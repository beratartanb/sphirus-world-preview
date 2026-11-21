# c_stopdb5.py (control, IN MEMORY - nothing saved here; saved later by the gated write job): Sphirus stop databases without the
# Reface stops. PSD_Relaxed_Stand_Walk_Stops / Run_Stops offer only 90 / 180 deg "reface" turns besides the plain stops. After a
# camera-steered curve the mesh root is 25-50 deg behind the capsule; Motion Matching then picked Walk_Reface_Stop_090/180: the body
# turned 90 deg on the spot (42 deg past the capsule) and was dragged back at the next start (19-30 cm foot travel).
# New: PSD_Sph_R_Walk_Stops / PSD_Sph_R_Run_Stops = the same Relaxed plain stops (F/B/LL/RL x L/R foot), populated through a BranchIn
# notify track per clip (the only script route), and an ABP_Sph_GASP remap  Relaxed stops -> Sphirus stops.
import unreal as u, re
EA=u.EditorAssetLibrary; AL=u.AnimationLibrary; AT=u.AssetToolsHelpers.get_asset_tools(); D='/Game/Sphirus/Player/GASP/DB'
R='/Game/Characters/UEFN_Mannequin/Animations/MotionMatchingData/Databases/Relaxed/PSD_Relaxed_Stand_'
f=u.DataAssetFactory(); f.set_editor_property('data_asset_class',u.PoseSearchDatabase); res={}; dbs={}
for g in ('Walk','Run'):
    name='PSD_Sph_R_%s_Stops'%g; s=u.load_asset(R+g+'_Stops'); assert s
    clips=[s.get_animation_asset(i) for i in range(s.get_num_animation_assets())]; clips=[c for c in clips if c and 'Reface' not in c.get_name()]; assert len(clips)==8,(g,len(clips))
    db=u.load_asset(D+'/'+name) if EA.does_asset_exist(D+'/'+name) else (u.find_object(None,D+'/'+name+'.'+name) or AT.create_asset(name,D,u.PoseSearchDatabase,f))
    for k in ('schema','continuing_pose_cost_bias','base_cost_bias','looping_cost_bias','tags','normalization_set','pose_search_mode'):
        try: db.set_editor_property(k,s.get_editor_property(k))
        except Exception as e: print('PROP',name,k,str(e)[:100])
    tr='SphR_%s_Stops'%g
    for a in clips:
        if tr in [str(t) for t in AL.get_animation_notify_track_names(a)]: continue
        AL.add_animation_notify_track(a,tr); st=AL.add_animation_notify_state_event(a,tr,0.0,float(a.get_play_length()),u.AnimNotifyState_PoseSearchBranchIn)
        st.set_editor_property('database',db)
    got=sorted(db.get_animation_asset(i).get_name() for i in range(db.get_num_animation_assets()) if db.get_animation_asset(i))
    print('STOPDB',name,len(clips),len(got),got[:3]); dbs[g]=(s,db)
a=u.load_asset('/Game/Sphirus/Player/GASP/ABP_Sph_GASP'); c=u.get_default_object(a.generated_class())
ks=list(c.get_editor_property('CM_Keys')); vs=list(c.get_editor_property('CM_Vals'))
for g,(s,db) in dbs.items():
    if s in ks: vs[ks.index(s)]=db
    else: ks.append(s); vs.append(db)
c.set_editor_property('CM_Keys',ks); c.set_editor_property('CM_Vals',vs)
c2=u.get_default_object(a.generated_class()); print('STOPDB remap',len(c2.get_editor_property('CM_Keys')),[ (k.get_name(),v.get_name()) for k,v in zip(c2.get_editor_property('CM_Keys'),c2.get_editor_property('CM_Vals')) if 'Stops' in k.get_name()])
