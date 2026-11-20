# an_pop.py <label> [thr_deg_per_frame=14] [thr_cm=6]: discontinuities of the VISIBLE body per frame (sim time).
#  shoulder-line yaw (clavicle_l -> clavicle_r), hip-line yaw (thigh_l -> thigh_r): step per frame and rate
#  pelvis / head position relative to the capsule: step per frame (cm) beyond thr_cm
# Lists frames above the thresholds with the clip before/after, and the maxima per plan segment.
import json, sys, math
R=json.load(open('Saved/Codex/Grip_20261106/rec/'+sys.argv[1]+'.json')); R=R['rows'] if isinstance(R,dict) else R
thr=float(sys.argv[2]) if len(sys.argv)>2 else 14.0; thc=float(sys.argv[3]) if len(sys.argv)>3 else 6.0
def wrap(a): return (a+180)%360-180
def yaw(r,a,b): return math.degrees(math.atan2(r['ub'][b][1]-r['ub'][a][1], r['ub'][b][0]-r['ub'][a][0]))
ev=[]; seg={}
for i in range(1,len(R)):
    a,b=R[i-1],R[i]; dt=max(1e-3,b['t']-a['t'])
    ds=abs(wrap(yaw(b,'upperarm_l','upperarm_r')-yaw(a,'upperarm_l','upperarm_r'))); dh=abs(wrap(yaw(b,'thigh_l','thigh_r')-yaw(a,'thigh_l','thigh_r')))
    dp=math.hypot((b['ub']['pelvis'][0]-b['x'])-(a['ub']['pelvis'][0]-a['x']),(b['ub']['pelvis'][1]-b['y'])-(a['ub']['pelvis'][1]-a['y']))
    dz=abs((b['ub']['pelvis'][2]-b['z'])-(a['ub']['pelvis'][2]-a['z']))
    m=seg.setdefault(b['s'],[0,0,0,0]); m[0]=max(m[0],ds/dt); m[1]=max(m[1],dh/dt); m[2]=max(m[2],dp/dt); m[3]=max(m[3],dz/dt)
    if ds>thr*dt*60 or dh>thr*dt*60 or dp>thc*dt*60 or dz>thc*dt*60:
        ev.append('t %.3f s%d dt %.3f shoulder %5.1f deg hip %5.1f deg pelvisXY %4.1f cm Z %4.1f cm | %s -> %s'%(b['t'],b['s'],dt,ds,dh,dp,dz,str(a['gasp'][0])[-24:],str(b['gasp'][0])[-24:]))
print('%s: %d frames, %d above threshold (%.0f deg or %.0f cm per 1/60 s)'%(sys.argv[1],len(R),len(ev),thr,thc))
for e in ev[:25]: print(' ',e)
print('  per-segment max rates: shoulder deg/s | hip deg/s | pelvisXY cm/s | pelvisZ cm/s')
print('  '+'  '.join('s%d:%.0f/%.0f/%.0f/%.0f'%(s,*m) for s,m in sorted(seg.items())))
