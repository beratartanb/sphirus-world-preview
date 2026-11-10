# an_rootslip.py <label...>: (1) visible pelvis vs capsule horizontal offset (cm; ~ GASP Offset Root Bone + clip pelvis sway),
# (2) planted-foot horizontal speed on the visible MetaHuman feet (min of the two feet per frame, cm/s) per speed band,
# (3) selection changes per second on steady segments.
import json,math,sys
def P(v,q): v=sorted(v); return v[int(q*(len(v)-1))] if v else float('nan')
for L in sys.argv[1:]:
    try: d=json.load(open('Saved/Codex/Grip_20261106/rec/%s.json'%L))
    except Exception as e: print('==',L,'missing'); continue
    R=d['rows']; off=[]; bands={'walk':(100,220,[]),'run':(300,450,[]),'sprint':(500,800,[])}
    for i in range(1,len(R)):
        r=R[i]; q=R[i-1]; b=r.get('ub')
        if isinstance(b,dict): off.append(math.hypot(b['pelvis'][0]-r['x'],b['pelvis'][1]-r['y']))
        sp=math.hypot(r['vx'],r['vy']); dt=max(r['t']-q['t'],1e-3)
        # stance foot: the lower foot, and only when it is within 2 cm of its own lowest height over +-0.4 s (planted)
        if not (r.get('v_foot_l') and r.get('v_foot_r') and q.get('v_foot_l')): continue
        k='v_foot_l' if r['v_foot_l'][2]<r['v_foot_r'][2] else 'v_foot_r'
        win=[x[k][2] for x in R[max(0,i-12):i+13] if x.get(k)]
        if r[k][2]-min(win)>2.0: continue
        f=math.hypot(r[k][0]-q[k][0],r[k][1]-q[k][1])/dt
        for bn,(lo,hi,acc) in bands.items():
            if lo<=sp<hi: acc.append(f)
    s='== %-18s pelvis-capsule p50 %.1f p95 %.1f max %.1f cm'%(L,P(off,.5),P(off,.95),max(off) if off else float('nan'))
    for bn,(lo,hi,acc) in bands.items():
        if len(acc)>15: s+=' | %s slip p50 %.1f p75 %.1f (n%d)'%(bn,P(acc,.5),P(acc,.75),len(acc))
    print(s)
