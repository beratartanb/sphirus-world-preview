import unreal as u, math
X=u.AnimPoseExtensions; o=[]
sk=u.load_asset('/Game/Characters/UEFN_Mannequin/Meshes/SK_UEFN_Mannequin')
try: o.append('COMPAT '+', '.join(str(x.get_name()) if hasattr(x,'get_name') else str(x) for x in sk.get_editor_property('compatible_skeletons')))
except Exception as e: o.append('compat err '+str(e)[:200])
opt=u.AnimPoseEvaluationOptions(); opt.set_editor_property('extract_root_motion',False)
for p in ('/Game/MC_Sample/Animations/Fight/am_Ready_Fight_01_Knockdown_A','/Game/MC_Sample/Animations/Fight/af_Ready_Fight_01_Knockdown_B','/Game/MC_Sample/Animations/Injured/am_InjuredBelly_DropToFloor','/Game/MC_Sample/Animations/Injured/am_InjuredBelly_DropToFloor_GetUp','/Game/MC_Sample/Animations/ProneCrawl/am_ProneCrawl_Trans_Stand','/Game/MC_Core_Motion/Animations/Kneel/am_KneelB_Trans_Stand','/Game/Characters/UEFN_Mannequin/Animations/Jump/M_Neutral_Jump_F_Land_Stumble_Lfoot','/Game/MC_Core_Motion/Animations/ReactBump/am_Stand_ReactBumpLight_Front'):
    s=u.load_asset(p); d=s.get_play_length(); st=0.25 if d>10 else 0.1; row=[]; k=0
    while k*st<=d+1e-6:
        t=min(k*st,d); ps=X.get_anim_pose_at_time(s,t,opt); pl=X.get_bone_pose(ps,'pelvis',u.AnimPoseSpaces.WORLD).translation; hd=X.get_bone_pose(ps,'head',u.AnimPoseSpaces.WORLD).translation; rt=X.get_bone_pose(ps,'root',u.AnimPoseSpaces.WORLD).translation
        row.append('%.0f/%.0f/%.0f'%(pl.z,hd.z,math.hypot(pl.x,pl.y))); k+=1
    o.append('%s len %.2f step %.2f pelvisZ/headZ/pelvisXYdist: %s'%(p.split('/')[-1],d,st,' '.join(row)))
open(u.Paths.project_dir()+'Saved/UE59Work/r5/fallclips.txt','w',encoding='utf8').write('\n'.join(o)); print('FALLCLIPS',len(o))
