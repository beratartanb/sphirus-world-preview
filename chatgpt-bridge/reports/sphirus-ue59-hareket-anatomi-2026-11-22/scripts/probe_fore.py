# probe_fore.py (read-only): lowerarm posture node in PARENT (upperarm) space - comp->parent column map at bind (as probe_axes) and the
# parent-space rotators for +1 deg forearm VALGUS (wrist outward, about the axis perpendicular to bone axis and elbow hinge) and +1 deg
# humeral EXTERNAL rotation (about the upper-arm axis; a flexed forearm swings outward). Output Saved/UE59Work/r5/fore_axes.json
import unreal as u, json, math
X=u.AnimPoseExtensions; M=u.MathLibrary
m=u.load_asset('/Game/Sphirus/CharacterLab/Sph_20261108/Built/MHC_Sph8/Body/SKM_MHC_Sph8_BodyMesh'); pose=X.get_reference_pose(m.get_editor_property('skeleton'))
out={}
for sd,sg in (('l',1.0),('r',-1.0)):   # comp +X = left
    T=lambda b:X.get_bone_pose(pose,b,u.AnimPoseSpaces.WORLD)
    qp=T('upperarm_'+sd).rotation; qi=qp.inversed(); U=T('upperarm_'+sd).translation; E=T('lowerarm_'+sd).translation; H=T('hand_'+sd).translation
    cols=[]
    for k in range(3):
        r=u.Rotator(roll=8.0 if k==0 else 0.0, pitch=8.0 if k==1 else 0.0, yaw=8.0 if k==2 else 0.0); rp=(qi*r.quaternion()*qp).rotator(); cols.append([round(rp.roll/8.0,3),round(rp.pitch/8.0,3),round(rp.yaw/8.0,3)])
    ua=(E-U); ua.normalize(); fa=(H-E); fa.normalize(); hinge=ua.cross(fa); hinge.normalize(); val=hinge.cross(ua); val.normalize()
    loc=lambda v:qi.rotate_vector(v)
    res={'cols':cols,'ua_local':[round(x,3) for x in (loc(ua).x,loc(ua).y,loc(ua).z)],'hinge_local':[round(x,3) for x in (loc(hinge).x,loc(hinge).y,loc(hinge).z)],'val_local':[round(x,3) for x in (loc(val).x,loc(val).y,loc(val).z)]}
    for name,axis in (('valgus',val),('ext',ua)):
        best=None
        for s in (1.0,-1.0):
            q=u.Quat(axis*s, math.radians(5.0)) if False else M.quat_from_axis_and_angle(axis*s, math.radians(5.0)) if hasattr(M,'quat_from_axis_and_angle') else M.rotator_from_axis_and_angle(axis*s,5.0).quaternion()
            h2=E+q.rotate_vector(H-E); dx=(h2.x-H.x)*sg
            if best is None or dx>best[0]: best=(dx,s,q)
        ql=qi*best[2]*qp; rl=ql.rotator(); res[name]=[round(rl.roll/5.0,3),round(rl.pitch/5.0,3),round(rl.yaw/5.0,3)]; res[name+'_dx_per_deg']=round(best[0]/5.0,3)
    out[sd]=res
json.dump(out,open(u.Paths.project_dir()+'Saved/UE59Work/r5/fore_axes.json','w'),indent=0); print('FORE',json.dumps(out)[:1400])
