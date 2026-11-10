# an_shoulder.py <label...>: shoulder girdle / arm / spine posture of driver (ud, UEFN GASP) vs visible MetaHuman (ub),
# per motion band (idle <5, walk 100-220, run 300-520, sprint >540 cm/s), capsule frame.
#  clavElev  = elevation of clavicle->upperarm above horizontal (deg, mean L/R) ; + = shoulder tip raised
#  dropRatio = (neck_01.z - mean upperarm.z) / shoulder width
#  handGap   = lateral distance hand - same-side thigh (cm, mean L/R) ; small = arms glued to hips (visible only)
#  twist     = p95-p5 of shoulder-line vs hip-line yaw (deg) ; chestLean = forward lean of neck over pelvis (deg)
import json,math,sys
def P(v,q): v=sorted(v); return v[int(q*(len(v)-1))] if v else float('nan')
def m(v): return sum(v)/len(v) if v else float('nan')
for L in sys.argv[1:]:
    d=json.load(open('Saved/Codex/Grip_20261106/rec/%s.json'%L)); R=d['rows']
    bands={'idle':(0,5),'walk':(100,220),'run':(300,520),'sprint':(540,900)}
    print('==',L)
    for bn,(lo,hi) in bands.items():
        rows=[r for r in R if lo<=math.hypot(r['vx'],r['vy'])<hi and isinstance(r.get('ub'),dict) and isinstance(r.get('ud'),dict)]
        if len(rows)<10: continue
        out=[]
        for key in ('ud','ub'):
            ce=[];dr=[];tw=[];ln=[];hg=[]
            for r in rows:
                b=r[key]; y=math.radians(r['yaw']); fx,fy=math.cos(y),math.sin(y); rx,ry=-fy,fx
                for s in 'lr':
                    c=b['clavicle_'+s]; a=b['upperarm_'+s]; dz=a[2]-c[2]; h=math.hypot(a[0]-c[0],a[1]-c[1]); ce.append(math.degrees(math.atan2(dz,h)))
                w=math.dist(b['upperarm_l'][:3],b['upperarm_r'][:3]); dr.append((b['neck_01'][2]-0.5*(b['upperarm_l'][2]+b['upperarm_r'][2]))/w)
                sl=math.atan2(b['upperarm_r'][1]-b['upperarm_l'][1],b['upperarm_r'][0]-b['upperarm_l'][0]); hl=math.atan2(b['thigh_r'][1]-b['thigh_l'][1],b['thigh_r'][0]-b['thigh_l'][0])
                tw.append((math.degrees(sl-hl)+180)%360-180)
                n=b['neck_01'];p=b['pelvis']; ln.append(math.degrees(math.atan2((n[0]-p[0])*fx+(n[1]-p[1])*fy,n[2]-p[2])))
                if key=='ub':
                    for s,hk in (('l','v_hand_l'),('r','v_hand_r')):
                        h_=r.get(hk); t_=b['thigh_'+s]
                        if h_: hg.append(abs((h_[0]-p[0])*rx+(h_[1]-p[1])*ry)-abs((t_[0]-p[0])*rx+(t_[1]-p[1])*ry))
            out.append('%s clavElev %5.1f° drop/w %.3f twist %4.1f° lean %4.1f°%s'%('DRV' if key=='ud' else 'VIS',m(ce),m(dr),P(tw,.95)-P(tw,.05),m(ln),(' handGap %4.1f cm'%m(hg)) if hg else ''))
        print('  %-6s n%4d | %s | %s'%(bn,len(rows),out[0],out[1]))
