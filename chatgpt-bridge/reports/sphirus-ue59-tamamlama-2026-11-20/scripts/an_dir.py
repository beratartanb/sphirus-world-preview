# an_dir.py <label> <planfile> [win=1.6] [step=0.1]: input-change event log on simulated time.
# For every plan segment change: keys before -> after, then samples: t-rel, speed, v along OLD input dir (vo), v along NEW input
# dir (vn), body yaw minus camera yaw (by), pelvis yaw vs chest yaw twist (tw), Gait enum, GR_GaitSel, GR_Back, MaxWalkSpeed, clip, db.
# Summary per event: t_rev = time until v along new dir > 0 (reversal) ; t_80 = time to 80% of final speed along new dir;
# clips = ordered distinct clips in the window with entry times; max per-frame visible pelvis jump (pop) and chest yaw step.
import json, sys, math, ast
RD='Saved/Codex/Grip_20261106/rec/'
lab=sys.argv[1]; plan=ast.literal_eval(open(sys.argv[2]).read()); win=float(sys.argv[3]) if len(sys.argv)>3 else 1.6; stp=float(sys.argv[4]) if len(sys.argv)>4 else 0.1
R=json.load(open(RD+lab+'.json')); R=R['rows'] if isinstance(R,dict) else R
def dirv(keys, cy):
    f=0; r=0
    for k in keys.split():
        if k=='W': f+=1
        if k=='S': f-=1
        if k=='D': r+=1
        if k=='A': r-=1
    if f==0 and r==0: return None
    a=math.radians(cy); fx,fy=math.cos(a),math.sin(a); rx,ry=-fy,fx
    x=f*fx+r*rx; y=f*fy+r*ry; n=math.hypot(x,y); return (x/n,y/n)
def wrap(a): return (a+180)%360-180
ev=[i for i in range(1,len(R)) if R[i]['s']!=R[i-1]['s']]
for i in ev:
    a=R[i-1]; b=R[i]; k0=plan[a['s']][0]; k1=plan[b['s']][0] if b['s']<len(plan) else ''
    d0=dirv(k0,a['cy']); d1=dirv(k1,b['cy']); t0=b['t']
    print('\n== t %.2f  [%s] -> [%s]   v_in %.0f'%(t0,k0,k1,math.hypot(a['vx'],a['vy'])))
    nxt=t0; clips=[]; trev=None; pop=0; ystep=0; prev=None; vfin=None
    seg=[r for r in R[i-1:] if r['t']<=t0+win and r['s']==b['s'] or r is a]
    for r in seg:
        g=r.get('gasp') or (None,None,None,None); c=g[0]
        if not clips or clips[-1][1]!=c: clips.append((round(r['t']-t0,2),c))
        vn=(r['vx']*d1[0]+r['vy']*d1[1]) if d1 else None
        if d1 and d0 and trev is None and vn>0 and (d0[0]*d1[0]+d0[1]*d1[1])<0.3 and r['t']>t0: trev=r['t']-t0
        if prev is not None:
            dt=max(1e-3,r['t']-prev['t'])
            try:
                # pelvis pop: visible pelvis displacement minus capsule displacement per frame
                dp=math.hypot((r['ub']['pelvis'][0]-prev['ub']['pelvis'][0])-(r['x']-prev['x']),(r['ub']['pelvis'][1]-prev['ub']['pelvis'][1])-(r['y']-prev['y']))
                pop=max(pop,dp/dt); ystep=max(ystep,abs(wrap(r['ub']['spine_05'][3]-prev['ub']['spine_05'][3]))/dt)
            except Exception: pass
        prev=r
        if r['t']>=nxt-1e-6:
            nxt+=stp; vo=(r['vx']*d0[0]+r['vy']*d0[1]) if d0 else float('nan')
            try: tw=wrap(r['ub']['spine_05'][3]-r['ub']['pelvis'][3]); by=wrap(r['yaw']-r['cy'])
            except Exception: tw=by=float('nan')
            gt=r.get('gt') or [None]*6; g4=r.get('g4') or [None]*5
            print('  %+.2f sp %4.0f vo %5.0f vn %5s by %5.0f tw %4.0f | %-6s sel %s back %-5s max %4s | %-42s %s'%(r['t']-t0,math.hypot(r['vx'],r['vy']),vo,('%.0f'%vn) if vn is not None else '-',by,tw,str(g[2])[-6:],gt[2],g4[1],('%.0f'%gt[5]) if gt[5] is not None else '-',str(c)[:42],str(g[1]).replace('PSD_','')[:34]))
    print('  SUM t_rev %s  clips %d: %s'%(('%.2f'%trev) if trev else '-',len(clips),' > '.join('%s@%.2f'%(str(c).replace('M_Relaxed_','').replace('M_Neutral_','N_'),t) for t,c in clips)))
    print('  SUM max pelvis-vs-capsule speed %.0f cm/s, max chest yaw rate %.0f deg/s'%(pop,ystep))
