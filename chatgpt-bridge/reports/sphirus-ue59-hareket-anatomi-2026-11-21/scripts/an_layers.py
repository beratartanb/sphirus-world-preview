# an_layers.py <label> [label2 ...]: per plan segment (steady part, >1.2 s after segment start) cycle statistics of the
# VISIBLE body and of the DRIVER skeleton in the capsule frame (x fwd, y right, z up):
#  arm: abduction of upper arm (elbow outward of the shoulder joint, deg from vertical in the frontal plane) L/R mean [min..max],
#       hand lateral distance from the pelvis line (cm) min/mean, hand fore-aft swing range (cm)
#  spine: sagittal lean (deg fwd +) of pelvis->spine_03, spine_03->spine_05, spine_05->neck_01, neck_01->head; head fwd of pelvis (cm)
#  clips: number of clip switches in the steady window
import json, sys, math
def loc(r, p):
    c=math.cos(math.radians(r['yaw'])); s=math.sin(math.radians(r['yaw'])); dx=p[0]-r['x']; dy=p[1]-r['y']
    return (dx*c+dy*s, -dx*s+dy*c, p[2]-r['z'])
def st(v): 
    v=[x for x in v if x is not None]
    return (sum(v)/len(v), min(v), max(v)) if v else (0,0,0)
def lean(a,b): return math.degrees(math.atan2(b[0]-a[0], b[2]-a[2]))
for lab in sys.argv[1:]:
    D=json.load(open('Saved/Codex/Grip_20261106/rec/'+lab+'.json')); R=D['rows']; plan=D.get('plan')
    print('####',lab,len(R),'rows')
    segs={}
    for r in R: segs.setdefault(r['s'],[]).append(r)
    for s,rr in sorted(segs.items()):
        t0=rr[0]['t']; W=[r for r in rr if r['t']-t0>1.2]
        if len(W)<60: continue
        sp=st([math.hypot(r['vx'],r['vy']) for r in W])[0]
        if sp<50: continue
        out={}
        for tag in ('vis','drv'):
            ab={'l':[],'r':[]}; hl={'l':[],'r':[]}; hf={'l':[],'r':[]}; el={'l':[],'r':[]}; L=[[],[],[],[]]; hd=[]
            for r in W:
                try:
                    if tag=='vis':
                        B={k:loc(r,v) for k,v in r['ub'].items()}; B.update({k:loc(r,v) for k,v in r['ub2'].items()}); B['hand_l']=loc(r,r['v_hand_l']); B['hand_r']=loc(r,r['v_hand_r'])
                    else:
                        B={k:loc(r,v) for k,v in r['sh']['d'].items()}
                except Exception: continue
                for sd,sg in (('l',-1.0),('r',1.0)):
                    u_=B['upperarm_'+sd]; e_=B['lowerarm_'+sd]; h_=B['hand_'+sd]
                    ab[sd].append(math.degrees(math.atan2(sg*(e_[1]-u_[1]), u_[2]-e_[2])))
                    el[sd].append(sg*(e_[1]-B['pelvis'][1])); hl[sd].append(sg*(h_[1]-B['pelvis'][1])); hf[sd].append(h_[0]-B['pelvis'][0])
                ch=[B['pelvis'],B['spine_03'],B['spine_05'],B['neck_01'],B['head']]
                for i in range(4): L[i].append(lean(ch[i],ch[i+1]))
                hd.append(B['head'][0]-B['pelvis'][0])
            a_l=st(ab['l']); a_r=st(ab['r'])
            out[tag]='abd L %5.1f [%5.1f..%5.1f] R %5.1f [%5.1f..%5.1f] | elbow-lat L %4.1f R %4.1f | hand-lat min L %4.1f R %4.1f mean %4.1f/%4.1f | hand swing L %4.1f R %4.1f | lean P-S3 %5.1f S3-S5 %5.1f S5-N %5.1f N-H %5.1f | head fwd %5.1f'%(
                a_l[0],a_l[1],a_l[2],a_r[0],a_r[1],a_r[2], st(el['l'])[0],st(el['r'])[0], st(hl['l'])[1],st(hl['r'])[1],st(hl['l'])[0],st(hl['r'])[0],
                st(hf['l'])[2]-st(hf['l'])[1], st(hf['r'])[2]-st(hf['r'])[1], st(L[0])[0],st(L[1])[0],st(L[2])[0],st(L[3])[0], st(hd)[0])
        sw=sum(1 for i in range(1,len(W)) if W[i]['gasp'][0]!=W[i-1]['gasp'][0])
        keys=plan[s][0] if plan and s<len(plan) else '?'
        print('s%d [%s] v %.0f  %.1f s  clip switches %d  clips %s'%(s,keys,sp,W[-1]['t']-W[0]['t'],sw,sorted(set(str(r['gasp'][0])[-28:] for r in W))[:4]))
        for tag in ('vis','drv'): print('   %s %s'%(tag,out[tag]))
