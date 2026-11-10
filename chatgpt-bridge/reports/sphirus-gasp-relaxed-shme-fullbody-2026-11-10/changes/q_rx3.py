# q_rx3.py (measure): root speed profile of Neutral vs Relaxed locomotion clips (loops, starts, stops, turns).
import unreal as u, json, re
L=u.AnimationLibrary; AR=u.AssetRegistryHelpers.get_asset_registry()
names=[]
for g in ('Walk','Run','Sprint'):
    for st in ('Neutral','Relaxed'):
        names+=['M_%s_%s_Loop_F'%(st,g),'M_%s_%s_Start_F_Lfoot'%(st,g),'M_%s_%s_Stop_F_Lfoot'%(st,g)]
names+=['M_Neutral_Run_Turn_R_180_Lfoot','M_Relaxed_Run_Turn_R_180_Lfoot','M_Neutral_Sprint_Turn_180_R_Lfoot','M_Relaxed_Sprint_Turn_180_R_Lfoot','M_Neutral_Walk_Turn_180_R_Lfoot','M_Relaxed_Walk_Turn_180_R_Lfoot','M_Relaxed_Stand_Idle_Loop','M_Neutral_Stand_Idle_Loop','M_Relaxed_Run_Pivot_F_B_Lfoot','M_Neutral_Run_Pivot_F_B_Lfoot']
idx={}
for a in AR.get_assets_by_path('/Game/Characters/UEFN_Mannequin/Animations',True):
    idx[str(a.asset_name)]=str(a.package_name)
out={}
for n in names:
    p=idx.get(n)
    if not p: out[n]='MISSING'; continue
    a=u.load_asset(p); ln=float(a.get_play_length()); N=24; seg=[]
    R=lambda t: L.get_bone_pose_for_time(a,'root',min(t,ln),False)
    P=[R(ln*i/N) for i in range(N+1)]
    for i in range(N):
        d=P[i+1].translation-P[i].translation; seg.append(round((d.x**2+d.y**2)**0.5/(ln/N)))
    d=P[-1].translation-P[0].translation
    out[n]={'len':round(ln,2),'dist':round((d.x**2+d.y**2)**0.5,1),'avg':round((d.x**2+d.y**2)**0.5/ln),'yaw':round(P[-1].rotation.rotator().yaw-P[0].rotation.rotator().yaw,1),'prof':seg}
json.dump(out,open(u.Paths.project_dir()+'Tools/GASP_20261109/rx_speeds.json','w'),indent=0); print('RXSPD',len(out))
