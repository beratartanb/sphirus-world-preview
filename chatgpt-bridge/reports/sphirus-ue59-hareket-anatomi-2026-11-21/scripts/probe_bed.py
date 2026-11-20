# probe_bed.py (read-only, house map loaded): actors around the bed + bed station values + bed montage facts
import unreal as u
o=[u.UnrealEditorSubsystem().get_editor_world().get_path_name()]
C=u.Vector(1215,767,560)
for a in u.EditorLevelLibrary.get_all_level_actors():
    try:
        l=a.get_actor_location()
        if abs(l.x-C.x)<260 and abs(l.y-C.y)<260 and abs(l.z-C.z)<200:
            org,ext=a.get_actor_bounds(False); o.append('%-34s %-26s loc (%.0f,%.0f,%.0f) yaw %.0f bounds x %.0f..%.0f y %.0f..%.0f z %.0f..%.0f'%(a.get_actor_label()[:34],a.get_class().get_name()[:26],l.x,l.y,l.z,a.get_actor_rotation().yaw,org.x-ext.x,org.x+ext.x,org.y-ext.y,org.y+ext.y,org.z-ext.z,org.z+ext.z))
            if a.get_actor_label()=='GR_Day_Bed':
                for k in ('GR_Kind','GR_UseStand','GR_Stand','GR_StandYaw','GR_Clip','GR_Clip2','GR_ContactT','GR_AwaitAt','GR_CamFov','GR_Prompt','GR_Title'):
                    try: o.append('   %s = %s'%(k,str(a.get_editor_property(k))[:120]))
                    except Exception as e: o.append('   %s ? %s'%(k,str(e)[:40]))
    except Exception: pass
m=u.load_asset('/Game/Sphirus/Player/Anim/Bed/AM_Sph_Bed'); s=u.load_asset('/Game/Sphirus/Player/Anim/Bed/A_Sph_Bed')
o.append('montage len %.2f seq len %.2f rootmotion %s lock %s'%(m.get_play_length(),s.get_play_length(),s.get_editor_property('enable_root_motion'),s.get_editor_property('root_motion_root_lock')))
X=u.AnimPoseExtensions; opt=u.AnimPoseEvaluationOptions()
for t in (0.0,1.0,2.0,3.0,4.0,5.0,6.0,8.0,s.get_play_length()-0.05):
    try:
        p=X.get_anim_pose_at_time(s,t,opt); r=X.get_bone_pose(p,'root',u.AnimPoseSpaces.WORLD).translation; pe=X.get_bone_pose(p,'pelvis',u.AnimPoseSpaces.WORLD).translation; hd=X.get_bone_pose(p,'head',u.AnimPoseSpaces.WORLD).translation
        o.append('  t %.1f root (%.0f,%.0f,%.0f) pelvis (%.0f,%.0f,%.0f) head (%.0f,%.0f,%.0f)'%(t,r.x,r.y,r.z,pe.x,pe.y,pe.z,hd.x,hd.y,hd.z))
    except Exception as e: o.append('  t %.1f err %s'%(t,str(e)[:60]))
open(u.Paths.project_dir()+'Saved/UE59Work/r4/bed_probe.txt','w',encoding='utf8').write('\n'.join(o)); print('BED',len(o))
