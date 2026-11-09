# q_trim.py (measure): root-motion speed / yaw-rate profiles of the gait database clips and a proposed BranchIn range per
# clip, so that start clips only offer their acceleration, stop clips only their deceleration and idle turns only the turn
# itself (the steady tails made the search flip between start/stop clips instead of the loops). Writes trim_plan.json.
import unreal as u, json, math
C='/Game/Sphirus/Player/Anim/Core/'
TURNS=['af_Stand_Idle_Turn%s%03d'%(s,a) for s in 'LR' for a in (45,90,135,180)]
WALK=['af_Loco_Walk_Fwd','af_Loco_Walk_Fwd_Start','af_Loco_Walk_Fwd_Stop','af_Loco_Walk_Fwd_Pivot','af_Loco_Walk_FwdLeft','af_Loco_Walk_FwdRight']+['af_Loco_Walk_Start_Turn%s%03d_%sfoot'%(s,a,s) for s in 'LR' for a in (45,90,135,180)]
JOG=[x.replace('Walk','Jog') for x in WALK]
RUN=['af_Loco_Run_Fwd','af_Loco_Run_Fwd_Start','af_Loco_Run_Fwd_Stop']+['af_Loco_Run_Start_Turn%s%03d_%sfoot'%(s,a,s) for s in 'LR' for a in (90,180)]
STEP=0.1; plan={}; out=[]
opt=u.AnimPoseEvaluationOptions(); opt.set_editor_property('evaluation_type',u.AnimDataEvalType.RAW); opt.set_editor_property('extract_root_motion',False)
def rootat(a,t):
    pose=u.AnimPoseExtensions.get_anim_pose_at_time(a,t,opt); return u.AnimPoseExtensions.get_bone_pose(pose,'root',u.AnimPoseSpaces.WORLD)
def prof(a):
    # the root bone track carries the root motion (not extracted): speed and yaw rate from successive root poses
    L=float(a.get_play_length()); rows=[]; t=0.0; r0=rootat(a,0.0)
    while t+STEP<=L+1e-4:
        r1=rootat(a,t+STEP); d=r1.translation-r0.translation; sp=math.hypot(d.x,d.y)/STEP
        dy=(r1.rotation.rotator().yaw-r0.rotation.rotator().yaw+540)%360-180; yr=abs(dy)/STEP
        rows.append((round(t,2),round(sp),round(yr))); t+=STEP; r0=r1
    return L,rows
for n in TURNS+WALK+JOG+RUN:
    a=u.load_asset(C+n)
    if not a: out.append('MISSING '+n); continue
    L,rows=prof(a); sp=[r[1] for r in rows]; yr=[r[2] for r in rows]; mx=max(sp) if sp else 0
    rng=None
    if n.endswith('_Start') or '_Start_Turn' in n:
        idx=[i for i,s in enumerate(sp) if s>=0.9*mx]; t_pl=rows[idx[0]][0] if idx else L
        rng=(0.0,round(min(L,max(0.6,t_pl+0.25)),2))
    elif n.endswith('_Stop'):
        idx=[i for i,s in enumerate(sp) if s>=0.9*mx]; t_de=rows[idx[-1]][0] if idx else 0.0
        z=[r[0] for r in rows if r[0]>t_de and r[1]<3]; t_z=(z[0]+0.4) if z else L   # settled: keep 0.4 s of the standing end
        rng=(round(max(0.0,t_de-0.25),2),round(min(L,t_z),2))
    elif 'Idle_Turn' in n:
        idx=[i for i,y in enumerate(yr) if y>15]; t_ys=rows[idx[-1]][0]+STEP if idx else L
        rng=(0.0,round(min(L,max(0.5,t_ys+0.3)),2))
    plan[n]=dict(len=round(L,2),range=rng,maxspd=mx)
    out.append('%s L=%.2f max=%d range=%s | %s'%(n,L,mx,rng,' '.join('%.1f:%d/%d'%r for r in rows)))
json.dump(plan,open(u.Paths.project_dir()+'Saved/Codex/Day_20261107/trim_plan.json','w'),indent=0)
print('\n'.join(out)); print('PLAN',len(plan))
