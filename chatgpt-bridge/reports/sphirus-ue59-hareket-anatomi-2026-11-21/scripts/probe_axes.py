# probe_axes.py (read-only): for the posture nodes moved to PARENT-BONE space - linear map from a component-space rotation vector
# (roll about +X, pitch about +Y, yaw about +Z of the MetaHuman body component at the bind pose) to the parent bone's rotator
# components. Output Saved/UE59Work/r4/axes.json: {bone: {'parent':..., 'M': 3x3 rows = parent (roll,pitch,yaw) per unit comp (roll,pitch,yaw)}}
import unreal as u, json
X=u.AnimPoseExtensions
m=u.load_asset('/Game/Sphirus/CharacterLab/Sph_20261108/Built/MHC_Sph8/Body/SKM_MHC_Sph8_BodyMesh')
pose=X.get_reference_pose(m.get_editor_property('skeleton'))
PAR={'spine_03':'spine_02','spine_05':'spine_04','neck_01':'spine_05','neck_02':'neck_01','head':'neck_02','clavicle_l':'spine_05','clavicle_r':'spine_05','upperarm_l':'clavicle_l','upperarm_r':'clavicle_r'}
out={}
for b,p in PAR.items():
    qp=X.get_bone_pose(pose,p,u.AnimPoseSpaces.WORLD).rotation; qi=qp.inversed(); M=[]
    for k in range(3):
        r=u.Rotator(roll=8.0 if k==0 else 0.0, pitch=8.0 if k==1 else 0.0, yaw=8.0 if k==2 else 0.0); d=r.quaternion()
        rp=(qi*d*qp).rotator(); M.append([round(rp.roll/8.0,3),round(rp.pitch/8.0,3),round(rp.yaw/8.0,3)])
    # M[k] = parent rotator for unit comp component k -> transpose to rows by parent comp
    out[b]={'parent':p,'cols':M}
    # verify parent name
    try: out[b]['realparent']=str(X.get_bone_pose(pose,b,u.AnimPoseSpaces.WORLD) is not None)
    except Exception as e: out[b]['err']=str(e)[:60]
json.dump(out,open(u.Paths.project_dir()+'Saved/UE59Work/r4/axes.json','w'),indent=0)
print('AXES',json.dumps({k:v['cols'] for k,v in out.items()}))
