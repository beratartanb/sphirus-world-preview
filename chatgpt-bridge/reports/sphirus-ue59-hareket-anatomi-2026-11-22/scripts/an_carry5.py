# an_carry5.py <label> [tmin=1.2]: carriage in the THORAX frame (u = spine_03->neck_01, r = hip line right, f = r x u) of the
# visible body per steady plan segment, compared with the MetaHuman bind:
#  shoulders: lift / forward of the shoulder joint over spine_05, L and R (cm); arm: upper-arm abduction L/R mean [min..max] (deg, frontal
#  plane of the thorax), elbow flexion, wrist lateral from the pelvis line when passing the hip, wrist min lateral, elbow lateral
#  neck/head: neck angle (neck_01->head against u, + = forward), head forward of the shoulder line (cm along f), head pitch (face
#  axis elevation, deg), trunk lean (u against vertical), head yaw swing p2p against the hip line (deg)
import json, sys, math
def sub(a,b): return [a[i]-b[i] for i in range(3)]
def dot(a,b): return sum(a[i]*b[i] for i in range(3))
def nrm(a): l=math.sqrt(dot(a,a)) or 1; return [x/l for x in a]
def cross(a,b): return [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]]
def st(v): return (sum(v)/len(v), min(v), max(v)) if v else (0,0,0)
def frame(B):
    # component space: +X left, +Y fwd, +Z up -> (fwd, right, up)
    c=lambda p:[p[1],-p[0],p[2]]; P={k:c(v) for k,v in B.items()}
    r=sub(P['thigh_r'],P['thigh_l']); r[2]=0; r=nrm(r); u=nrm(sub(P['neck_01'],P['spine_03'])); f=nrm(cross(r,u)); f=[-x for x in f] if dot(f,cross(r,[0,0,1]))<0 else f
    return P,r,u,f
def met(B,q=None):
    P,r,u,f=frame(B); o={}
    for sd,sg in (('l',-1.0),('r',1.0)):
        s5=P['spine_05']; U=P['upperarm_'+sd]; E=P['lowerarm_'+sd]; H=P['hand_'+sd]
        o['lift_'+sd]=dot(sub(U,s5),u); o['fwd_'+sd]=dot(sub(U,s5),f)
        ue=sub(E,U); o['abd_'+sd]=math.degrees(math.atan2(sg*dot(ue,r), -dot(ue,u)))
        a=nrm(sub(U,E)); b=nrm(sub(H,E)); o['flex_'+sd]=math.degrees(math.acos(max(-1,min(1,dot(a,b)))))
        o['wlat_'+sd]=sg*dot(sub(H,P['pelvis']),r); o['wfwd_'+sd]=dot(sub(H,P['pelvis']),cross(r,[0,0,1])); o['elat_'+sd]=sg*dot(sub(E,P['pelvis']),r); o['wz_'+sd]=H[2]-P['pelvis'][2]
    nh=sub(P['head'],P['neck_01']); o['neck']=math.degrees(math.atan2(dot(nh,f),dot(nh,u)))
    sm=[(P['upperarm_l'][i]+P['upperarm_r'][i])/2 for i in range(3)]; o['headfwd']=dot(sub(P['head'],sm),f); o['lean']=math.degrees(math.atan2(dot(u,cross(r,[0,0,1])),u[2]))
    if q:
        x,y,z,w=q; Y=[2*(x*y-w*z), 1-2*(x*x+z*z), 2*(y*z+w*x)]; Yc=[Y[1],-Y[0],Y[2]]
        o['hpitch']=math.degrees(math.asin(max(-1,min(1,Yc[2])))); fw=cross(r,[0,0,1]); o['hyaw']=math.degrees(math.atan2(dot(Yc,r),dot(Yc,fw)))
    return o
def line(M,tag):
    g=lambda k:st([m[k] for m in M if k in m])
    hip=[m['wlat_'+s] for m in M for s in 'lr' if abs(m['wfwd_'+s])<8 and -24<m['wz_'+s]<8]
    return '%s sh lift %4.1f/%4.1f fwd %4.1f/%4.1f | abd L %4.1f [%4.1f..%4.1f] R %4.1f [%4.1f..%4.1f] flex %3.0f/%3.0f | elbow lat %4.1f/%4.1f wrist@hip %4.1f min %4.1f/%4.1f | neck %4.1f headfwd %4.1f pitch %5.1f yaw p2p %4.1f | lean %4.1f'%(
        tag,g('lift_l')[0],g('lift_r')[0],g('fwd_l')[0],g('fwd_r')[0],g('abd_l')[0],g('abd_l')[1],g('abd_l')[2],g('abd_r')[0],g('abd_r')[1],g('abd_r')[2],g('flex_l')[0],g('flex_r')[0],
        g('elat_l')[0],g('elat_r')[0],st(hip)[0],g('wlat_l')[1],g('wlat_r')[1],g('neck')[0],g('headfwd')[0],g('hpitch')[0],g('hyaw')[2]-g('hyaw')[1],g('lean')[0])
if __name__=='__main__':
    D=json.load(open('Saved/UE59Work/r4/raw.json')); print(line([met(D['ref_tgt'])],'BIND(MH)   '))
    tmin=float(sys.argv[2]) if len(sys.argv)>2 else 1.2; src=sys.argv[3] if len(sys.argv)>3 else 'pv'
    R=json.load(open('Saved/Codex/Grip_20261106/rec/'+sys.argv[1]+'.json')); plan=R.get('plan') or []; R=R['rows']; segs={}
    for r in R: segs.setdefault(r['s'],[]).append(r)
    print('####',sys.argv[1],src)
    for s,rr in sorted(segs.items()):
        W=[r for r in rr if r['t']-rr[0]['t']>tmin and src in r['hook']]
        if len(W)<40: continue
        sp=st([math.hypot(r['vx'],r['vy']) for r in W])[0]
        M=[met(r['hook'][src],r['hook'].get('pq',{}).get('head') if src=='pv' else None) for r in W]
        print(line(M,'s%-2d %-9s v%3.0f'%(s,(plan[s][0] if s<len(plan) else '?')[:9],sp)))
