# an_fat9.py <label> <planfile>: fatigue chain per segment (no pinned fatigue): effort E / fatigue Fat at start -> end, steady speed,
# step time, arm swing range, visible trunk lean, neck lean, shoulder height above spine_05, breathing chest pitch amplitude, camera z range.
import json, sys, math, ast
lab=sys.argv[1]; plan=ast.literal_eval(open(sys.argv[2]).read())
d=json.load(open('Saved/Codex/Grip_20261106/rec/%s.json'%lab))['rows']
def lean(p,a,b): x=p[a]; y=p[b]; return math.degrees(math.atan2(math.hypot(y[0]-x[0],y[1]-x[1]),y[2]-x[2]))
segs={}
for r in d: segs.setdefault(r['s'],[]).append(r)
print('#### %s (fatigue is NOT pinned; E = effort, Fat = fatigue 0..1)'%lab)
for s in sorted(segs):
    R=segs[s]; keys=plan[s][0] if s<len(plan) else '?'; T=R[-1]['t']-R[0]['t']
    e0=R[0]['hook'].get('eff') or [0,0,0,0]; e1=R[-1]['hook'].get('eff') or [0,0,0,0]
    St=[r for r in R if r['t']-R[0]['t']>min(2.0,0.5*T)]
    sp=[math.hypot(r['vx'],r['vy']) for r in St]; v=sum(sp)/len(sp) if sp else 0
    # step time from contact_l falling edges
    ed=[St[i]['t'] for i in range(1,len(St)) if St[i]['hook']['cv'][0]<10<=St[i-1]['hook']['cv'][0]]
    stp=(ed[-1]-ed[0])/(len(ed)-1) if len(ed)>2 else 0
    pv=[r['hook']['pv'] for r in St if 'pv' in r['hook']]
    if pv:
        hx=[p['hand_r'][1] for p in pv]; arm=max(hx)-min(hx)
        tl=sum(lean(p,'pelvis','spine_05') for p in pv)/len(pv); nl=sum(lean(p,'spine_05','head') for p in pv)/len(pv)
        sh=sum((p['clavicle_l'][2]+p['clavicle_r'][2])/2-p['spine_05'][2] for p in pv)/len(pv)
    else: arm=tl=nl=sh=0
    ps=[r['hook']['ps'] for r in St if r['hook'].get('ps')]; br=(max(p[1] for p in ps)-min(p[1] for p in ps)) if ps else 0
    cz=[r['cam'][2]-r['z'] for r in St]; czr=max(cz)-min(cz) if cz else 0
    print('s%-2d [%-22s] %5.1f s | E %.2f->%.2f Fat %.2f->%.2f | v %3.0f step %.2f s | arm swing %4.1f cm | trunk lean %4.1f neck %4.1f shoulder %4.1f cm | chest pitch range %4.1f | cam z range %4.1f'%(s,keys,T,e0[0],e1[0],e0[2],e1[2],v,stp,arm,tl,nl,sh,br,czr))
