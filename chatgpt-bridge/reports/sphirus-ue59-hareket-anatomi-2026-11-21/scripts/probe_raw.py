# probe_raw.py (read-only): raw source clips sampled directly (no GASP graph) + reference poses of source/target skeletons.
# Output Saved/UE59Work/r4/raw.json: {clip: {dur, frames:[{bone:[x,y,z]}]}, ref_src:{...}, ref_tgt:{...}, rtg:{...}}; positions in component space.
import unreal as u, json
AR=u.AssetRegistryHelpers.get_asset_registry(); X=u.AnimPoseExtensions
BN=['pelvis','spine_01','spine_03','spine_05','neck_01','neck_02','head','clavicle_l','clavicle_r','upperarm_l','upperarm_r','lowerarm_l','lowerarm_r','hand_l','hand_r','thigh_l','thigh_r','calf_l','calf_r','foot_l','foot_r','ball_l','ball_r','root']
want=['M_Neutral_Walk_Loop_F','CM_af_Loco_Jog_Fwd','M_Neutral_Run_Loop_F','M_Relaxed_Sprint_Loop_F','M_Neutral_Walk_Loop_B','M_Relaxed_Walk_Loop_F','M_Relaxed_Run_Loop_F','M_Neutral_Stand_Idle_Loop','M_Relaxed_Stand_Idle_Loop']
out={'clips':{}}
f=u.ARFilter(class_paths=[u.TopLevelAssetPath('/Script/Engine','AnimSequence')],package_paths=['/Game'],recursive_paths=True)
found={}
for ad in AR.get_assets(f):
    n=str(ad.asset_name)
    if n in want: found.setdefault(n,[]).append(str(ad.package_name))
out['paths']=found
def P(pose,names):
    r={}
    for b in names:
        try: t=X.get_bone_pose(pose,b,u.AnimPoseSpaces.WORLD); r[b]=[round(t.translation.x,2),round(t.translation.y,2),round(t.translation.z,2)]
        except Exception: pass
    return r
opt=u.AnimPoseEvaluationOptions()
for n,ps in found.items():
    for p in ps[:1]:
        s=u.load_asset(p); d=s.get_play_length(); fr=[]; N=max(2,int(d*30))
        for i in range(N):
            pose=X.get_anim_pose_at_time(s,d*i/N,opt); fr.append(P(pose,BN))
        out['clips'][n]={'path':p,'dur':round(d,3),'skel':s.get_skeleton().get_path_name(),'frames':fr}
rtg=u.load_asset('/Game/Sphirus/Player/GASP/Rig/RTG_Sph_UEFN_to_MH'); c=u.IKRetargeterController.get_controller(rtg)
info={}
for tag,sd in (('src',u.RetargetSourceOrTarget.SOURCE),('tgt',u.RetargetSourceOrTarget.TARGET)):
    try:
        m=c.get_preview_mesh(sd); info[tag+'_mesh']=m.get_path_name() if m else None
        sk=m.get_editor_property('skeleton') if m else None
        if m:
            pose=X.get_reference_pose_from_skeletal_mesh(m) if hasattr(X,'get_reference_pose_from_skeletal_mesh') else X.get_reference_pose(sk)
            out['ref_'+tag]=P(pose,BN)
        info[tag+'_pose']=str(c.get_current_retarget_pose_name(sd))
        try:
            ik=c.get_ik_rig(sd); info[tag+'_rig']=ik.get_path_name()
        except Exception as e: info[tag+'_rig']=str(e)[:60]
        try:
            offs={}
            for b in ('pelvis','spine_01','spine_02','spine_03','spine_04','spine_05','neck_01','neck_02','head','clavicle_l','clavicle_r','upperarm_l','upperarm_r','lowerarm_l','lowerarm_r','hand_l','hand_r','thigh_l','thigh_r'):
                q=c.get_rotation_offset_for_retarget_pose_bone(b,sd); r=q.rotator()
                if abs(r.roll)+abs(r.pitch)+abs(r.yaw)>0.01: offs[b]=[round(r.roll,2),round(r.pitch,2),round(r.yaw,2)]
            info[tag+'_pose_offsets']=offs
            t=c.get_root_offset_in_retarget_pose(sd); info[tag+'_root_off']=[round(t.x,2),round(t.y,2),round(t.z,2)]
        except Exception as e: info[tag+'_offs_err']=str(e)[:120]
    except Exception as e: info[tag+'_err']=str(e)[:160]
try:
    ops=[]
    n=c.get_num_retarget_ops()
    for i in range(n): ops.append(str(c.get_op_name(i)))
    info['ops']=ops
except Exception as e: info['ops_err']=str(e)[:100]
out['rtg']=info
json.dump(out,open(u.Paths.project_dir()+'Saved/UE59Work/r4/raw.json','w'))
print('RAW',list(out['clips'].keys()),json.dumps(info)[:1500])
