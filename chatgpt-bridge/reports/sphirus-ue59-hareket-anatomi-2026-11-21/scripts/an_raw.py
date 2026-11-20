# an_raw.py: same metrics as an_layers.py for the raw clips (component space: fwd = +y, right = -x) and the reference poses.
import json, math
D=json.load(open('Saved/UE59Work/r4/raw.json'))
def L(p): return (p[1], -p[0], p[2])
def st(v): return (sum(v)/len(v), min(v), max(v))
def lean(a,b): return math.degrees(math.atan2(b[0]-a[0], b[2]-a[2]))
def met(frames):
    ab={'l':[],'r':[]}; hl={'l':[],'r':[]}; hf={'l':[],'r':[]}; el={'l':[],'r':[]}; Ls=[[],[],[],[]]; hd=[]
    for f in frames:
        B={k:L(v) for k,v in f.items()}
        for sd,sg in (('l',-1.0),('r',1.0)):
            u_=B['upperarm_'+sd]; e_=B['lowerarm_'+sd]; h_=B['hand_'+sd]
            ab[sd].append(math.degrees(math.atan2(sg*(e_[1]-u_[1]), u_[2]-e_[2]))); el[sd].append(sg*(e_[1]-B['pelvis'][1])); hl[sd].append(sg*(h_[1]-B['pelvis'][1])); hf[sd].append(h_[0]-B['pelvis'][0])
        ch=[B['pelvis'],B['spine_03'],B['spine_05'],B['neck_01'],B['head']]
        for i in range(4): Ls[i].append(lean(ch[i],ch[i+1]))
        hd.append(B['head'][0]-B['pelvis'][0])
    a_l=st(ab['l']); a_r=st(ab['r'])
    return 'abd L %5.1f [%5.1f..%5.1f] R %5.1f [%5.1f..%5.1f] | elbow-lat L %4.1f R %4.1f | hand-lat min L %4.1f R %4.1f mean %4.1f/%4.1f | hand swing L %4.1f R %4.1f | lean P-S3 %5.1f S3-S5 %5.1f S5-N %5.1f N-H %5.1f | head fwd %5.1f'%(
        a_l[0],a_l[1],a_l[2],a_r[0],a_r[1],a_r[2], st(el['l'])[0],st(el['r'])[0], st(hl['l'])[1],st(hl['r'])[1],st(hl['l'])[0],st(hl['r'])[0],
        st(hf['l'])[2]-st(hf['l'])[1], st(hf['r'])[2]-st(hf['r'])[1], st(Ls[0])[0],st(Ls[1])[0],st(Ls[2])[0],st(Ls[3])[0], st(hd)[0])
for k in ('ref_src','ref_tgt'):
    if k in D:
        print(k, met([D[k]])); B=D[k]; print('    shoulder half-width %.1f hip joint half-width %.1f arm len %.1f+%.1f pelvis z %.1f head z %.1f'%(abs(B['upperarm_l'][0]-B['upperarm_r'][0])/2, abs(B['thigh_l'][0]-B['thigh_r'][0])/2, math.dist(B['upperarm_l'],B['lowerarm_l']), math.dist(B['lowerarm_l'],B['hand_l']), B['pelvis'][2], B['head'][2]))
for n,c in D['clips'].items(): print('%-28s %s'%(n, met(c['frames'])))
print(json.dumps(D['rtg'])[:1800])
