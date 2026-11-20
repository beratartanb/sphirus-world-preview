# an_body4.py <label> [tmin=1.2]: steady-window body carriage of the VISIBLE body (hk_pose 'pv', component space +X left, +Y fwd, +Z up)
# and the driver ('pd') per plan segment. lat = outward distance from the pelvis sagittal plane.
#  spine: lean over the MetaHuman bind (deg, fwd +) of pelvis->spine_03 (L1), spine_03->spine_05 (L2), spine_05->neck_01 (L3), neck_01->head (L4)
#  twist: shoulder-line yaw minus hip-line yaw, peak-to-peak (deg); shoulder lift: upperarm z above spine_05 (cm, mean L/R)
#  arms: elbow lat mean; wrist lat when passing the hip (|fwd|<8), at the front end and at the back end of the swing; wrist lat min;
#        elbow flexion mean [min..max]; frames with the wrist inside the hip zone (lat < 20 while |fwd| < 10 and z within pelvis-22..+10)
import json, sys, math
BIND={'pv':(7.1,-8.9,-11.2,11.9),'pd':(-3.3,-5.4,-3.8,15.4)}
def st(v): return (sum(v)/len(v), min(v), max(v)) if v else (0,0,0)
def lean(a,b): return math.degrees(math.atan2(b[1]-a[1], b[2]-a[2]))
def ang(a,b,c):
    u=[a[i]-b[i] for i in range(3)]; v=[c[i]-b[i] for i in range(3)]; d=sum(u[i]*v[i] for i in range(3))/max(1e-6,math.dist(a,b)*math.dist(c,b)); return math.degrees(math.acos(max(-1,min(1,d))))
def yawline(l,r): return math.degrees(math.atan2(r[1]-l[1], r[0]-l[0]))
tmin=float(sys.argv[2]) if len(sys.argv)>2 else 1.2
D=json.load(open('Saved/Codex/Grip_20261106/rec/'+sys.argv[1]+'.json')); R=D['rows']; plan=D.get('plan') or []
segs={}
for r in R: segs.setdefault(r['s'],[]).append(r)
print('####',sys.argv[1])
for s,rr in sorted(segs.items()):
    W=[r for r in rr if r['t']-rr[0]['t']>tmin and 'pv' in r['hook']]
    if len(W)<50: continue
    sp=st([math.hypot(r['vx'],r['vy']) for r in W])[0]
    print('s%d [%s] v %.0f n %d %s'%(s,plan[s][0] if s<len(plan) else '?',sp,len(W),sorted(set(str(r['gasp'][0])[-24:] for r in W))[:3]))
    for tag in ('pv','pd'):
        L=[[],[],[],[]]; tw=[]; sh=[]; el=[]; fx=[]; wl_mid=[]; wl_f=[]; wl_b=[]; wl=[]; clip=0; hf=[]
        for r in W:
            B=r['hook'][tag]; pz=B['pelvis']
            ch=[B['pelvis'],B['spine_03'],B['spine_05'],B['neck_01'],B['head']]
            for i in range(4): L[i].append(lean(ch[i],ch[i+1])-BIND[tag][i])
            tw.append(((yawline(B['upperarm_l'],B['upperarm_r'])-yawline(B['thigh_l'],B['thigh_r']))+180)%360-180)
            sh.append((B['upperarm_l'][2]+B['upperarm_r'][2])/2-B['spine_05'][2])
            for sd,sg in (('l',1.0),('r',-1.0)):
                e=B['lowerarm_'+sd]; h=B['hand_'+sd]; lat=sg*(h[0]-pz[0]); f=h[1]-pz[1]; z=h[2]-pz[2]
                el.append(sg*(e[0]-pz[0])); wl.append(lat); hf.append(f); fx.append(ang(B['upperarm_'+sd],e,h))
                if abs(f)<8: wl_mid.append(lat)
                if abs(f)<10 and -22<z<10 and lat<20: clip+=1
            
        fmax=max(hf); fmin=min(hf)
        for r in W:
            B=r['hook'][tag]; pz=B['pelvis']
            for sd,sg in (('l',1.0),('r',-1.0)):
                h=B['hand_'+sd]; f=h[1]-pz[1]; lat=sg*(h[0]-pz[0])
                if f>fmax-6: wl_f.append(lat)
                if f<fmin+6: wl_b.append(lat)
        print('  %s lean L1 %5.1f L2 %5.1f L3 %5.1f L4 %5.1f | twist p2p %4.1f | sh lift %4.1f | elbow lat %4.1f flex %5.1f [%3.0f..%3.0f] | wrist lat hip %4.1f front %4.1f back %4.1f min %5.1f | swing %+.0f..%+.0f | hip-zone frames %d/%d'%(
            'vis' if tag=='pv' else 'drv', st(L[0])[0],st(L[1])[0],st(L[2])[0],st(L[3])[0], st(tw)[2]-st(tw)[1], st(sh)[0], st(el)[0], st(fx)[0],st(fx)[1],st(fx)[2],
            st(wl_mid)[0],st(wl_f)[0],st(wl_b)[0],min(wl), fmin,fmax, clip, 2*len(W)))
