# an_hip.py <label> [plan file] : pelvis / trunk / arm motion per steady segment, DRIVER (retargeted UEFN skeleton) vs VISIBLE body.
# Component space: x lateral, y forward, z up. p2p = mean peak-to-peak per gait cycle (cycle from left-foot contact curve), after removing a
# linear trend. obliq = hip-line roll (deg), rot = hip-line yaw (deg), sh = shoulder line, width = lateral foot spacing at mid stance.
import json, sys, math
lab=sys.argv[1]; rows=json.load(open('Saved/Codex/Grip_20261106/rec/%s.json'%lab))['rows']
plan=eval(open(sys.argv[2]).read()) if len(sys.argv)>2 else None
def line(p,a,b):
    dx=p[b][0]-p[a][0]; dy=p[b][1]-p[a][1]; dz=p[b][2]-p[a][2]; return math.degrees(math.atan2(dz,math.hypot(dx,dy))), math.degrees(math.atan2(dy,dx))
def cyc(seg):
    # cycle boundaries: rising edges of left contact
    e=[i for i in range(1,len(seg)) if seg[i]['hook']['cv'][0]>50 and seg[i-1]['hook']['cv'][0]<=50]; return [(e[i],e[i+1]) for i in range(len(e)-1)]
def p2p(v,cs):
    o=[]
    for a,b in cs:
        w=v[a:b]; n=len(w)
        if n<6: continue
        k=(w[-1]-w[0])/(n-1); d=[w[i]-w[0]-k*i for i in range(n)]; o.append(max(d)-min(d))
    return sum(o)/len(o) if o else float('nan')
def unwrap(v):
    o=[v[0]]
    for x in v[1:]:
        d=(x-o[-1]+180)%360-180; o.append(o[-1]+d)
    return o
print('####',lab); segs={}
for r in rows: segs.setdefault(r['s'],[]).append(r)
for s,seg in sorted(segs.items()):
    sp=[math.hypot(r['vx'],r['vy']) for r in seg]
    if len(seg)<90 or sum(sp)/len(sp)<60: continue
    t0=seg[0]['t']; st=[r for r in seg if r["t"]-t0>0.9 and 'pv' in r['hook']]
    if len(st)<60: continue
    v=sum(math.hypot(r['vx'],r['vy']) for r in st)/len(st); cs=cyc(st)
    if len(cs)<2: continue
    T=sum(st[b]['t']-st[a]['t'] for a,b in cs)/len(cs); name=(plan[s][0] if plan and s<len(plan) else '')
    print('s%-2d [%-22s] v %3.0f cm/s | %d cycles x %.2f s | clip %s'%(s,name,v,len(cs),T,st[len(st)//2]['gasp'][0][-26:]))
    for tag in ('pd','pv'):
        P=[r['hook'][tag] for r in st]
        lat=p2p([p['pelvis'][0] for p in P],cs); ver=p2p([p['pelvis'][2] for p in P],cs)
        ob=p2p([line(p,'thigh_l','thigh_r')[0] for p in P],cs); ro=p2p(unwrap([line(p,'thigh_l','thigh_r')[1] for p in P]),cs)
        so=p2p([line(p,'upperarm_l','upperarm_r')[0] for p in P],cs); sr=p2p(unwrap([line(p,'upperarm_l','upperarm_r')[1] for p in P]),cs)
        hl=p2p([p['head'][0] for p in P],cs); hv=p2p([p['head'][2] for p in P],cs)
        sw=p2p([p['hand_l'][1]-p['pelvis'][1] for p in P],cs); ab=sum(abs(p['hand_l'][0]-p['pelvis'][0])+abs(p['hand_r'][0]-p['pelvis'][0]) for p in P)/(2*len(P))
        wd=sum(abs(p['foot_l'][0]-p['foot_r'][0]) for p in P)/len(P); bl=p2p([p['ball_l'][0]-p['pelvis'][0] for p in P],cs)
        print('   %s pelvis lat %4.1f cm ver %4.1f cm obliq %4.1f deg rot %4.1f deg | shoulder obliq %4.1f rot %4.1f | head lat %4.1f ver %4.1f | hand swing %5.1f cm hand-to-midline %4.1f | foot spacing %4.1f cm'%({'pd':'DRIVER ','pv':'VISIBLE'}[tag],lat,ver,ob,ro,so,sr,hl,hv,sw,ab,wd))
