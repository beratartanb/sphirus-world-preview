# r5_rtg_clav.py (write) on RTG_Sph_UEFN_to_MH (Sphirus copy): raise the MetaHuman clavicles in the TARGET retarget pose.
# Root cause (an_shoulder.py): the UEFN->MH retarget lowers the clavicle elevation by ~4.3 deg against the GASP driver at
# every speed (old Core Motion retarget: +1 deg). Clavicle chains run OneToOne, so the target retarget-pose clavicle
# orientation carries straight into the output. Params from clav_param.json: {"deg": d, "axis": [x,y,z], "mirror": [sl, sr]}
# (rotation about the bone-local axis, sign per side). The offset is composed onto the current offset (idempotent via "set").
import unreal as u, json, math
p=json.load(open(u.Paths.project_dir()+'Tools/GASP_20261109/clav_param.json'))
r=u.load_asset('/Game/Sphirus/Player/GASP/Rig/RTG_Sph_UEFN_to_MH'); c=u.IKRetargeterController.get_controller(r)
T=u.RetargetSourceOrTarget.TARGET
pose=c.get_current_retarget_pose_name(T); print('POSE',pose)
for side,sg in (('l',p['mirror'][0]),('r',p['mirror'][1])):
    b='clavicle_'+side; cur=c.get_rotation_offset_for_retarget_pose_bone(b,T)
    base=p.get('base',{}).get(b)
    q0=u.Quat(*base) if base else cur
    import math; h=math.radians(p['deg']*sg)/2; ax=p['axis']; nn=math.sqrt(sum(x*x for x in ax)); d=u.Quat(ax[0]/nn*math.sin(h),ax[1]/nn*math.sin(h),ax[2]/nn*math.sin(h),math.cos(h))
    q=q0*d
    c.set_rotation_offset_for_retarget_pose_bone(b,q,T)
    print('CLAV',b,'before',cur.rotator(),'after',c.get_rotation_offset_for_retarget_pose_bone(b,T).rotator(),'base',[round(x,6) for x in (q0.x,q0.y,q0.z,q0.w)])
assert u.EditorAssetLibrary.save_loaded_asset(r,False); print('DONE')
