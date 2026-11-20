# an_carry.py <label> <planfile> : steady-state carriage per plan segment (last 55% of each moving segment >= 2 s, and idle >= 2 s).
# Visible body (MetaHuman) vs driver (UEFN retarget source), in the ACTOR frame (fwd = velocity direction when moving).
#  abd  = upper-arm abduction, deg: elbow lateral offset outward from the shoulder joint vs its vertical drop (mean L/R), mean over cycle
#  elb  = elbow lateral distance outside the shoulder joint (cm, mean L/R; negative = elbow inside the shoulder line)
#  hand = hand lateral distance from the spine_05 midline (cm, mean of L/R, min over cycle in brackets)
#  swing= fore-aft hand travel range (cm, mean L/R)
#  neck = forward inclination of neck_01->head from vertical (deg, + = head ahead); chest = spine_05->neck_01 forward incl.
#  hd   = head centre ahead of pelvis (cm)
import json, sys, math, ast, statistics as S
RD='Saved/Codex/Grip_20261106/rec/'
lab=sys.argv[1]; plan=ast.literal_eval(open(sys.argv[2]).read())
R=json.load(open(RD+lab+'.json')); R=R['rows'] if isinstance(R,dict) else R
def fr(r):
    sp=math.hypot(r['vx'],r['vy'])
    if sp>40: f=(r['vx']/sp,r['vy']/sp)
    else: a=math.radians(r['yaw']); f=(math.cos(a),math.sin(a))
    return f,(-f[1],f[0])
def met(P,f,rt,side):
    # P: dict name->xyz ; side 'l'/'r'
    sh=P['upperarm_'+side]; el=P['lowerarm_'+side]; ha=P['hand_'+side]; mid=P['spine_05']
    sg=-1 if side=='l' else 1
    lat=lambda a,b:((a[0]-b[0])*rt[0]+(a[1]-b[1])*rt[1])*sg
    fw=lambda a,b:((a[0]-b[0])*f[0]+(a[1]-b[1])*f[1])
    e=lat(el,sh); drop=max(1e-3,sh[2]-el[2])
    return math.degrees(math.atan2(e,drop)), e, lat(ha,mid), fw(ha,mid)
def incl(a,b,f): return math.degrees(math.atan2((b[0]-a[0])*f[0]+(b[1]-a[1])*f[1], b[2]-a[2]))
segs={}
for r in R: segs.setdefault(r['s'],[]).append(r)
print('%-3s %-26s %5s | %-44s | %-44s | %s'%('seg','keys','speed','VISIBLE abd  elb  hand(min) swing neck chest hd','DRIVER  abd  elb  hand(min) swing neck chest hd','MoveA RelA RunA  clip'))
for s in sorted(segs):
    if s>=len(plan): continue
    rows=segs[s]; dur=rows[-1]['t']-rows[0]['t']
    if dur<1.9: continue
    rows=[r for r in rows if r['t']>=rows[0]['t']+0.45*dur]
    acc={'v':[], 'd':[]}
    for r in rows:
        f,rt=fr(r)
        try:
            V={'upperarm_l':r['ub']['upperarm_l'],'upperarm_r':r['ub']['upperarm_r'],'lowerarm_l':r['ub2']['lowerarm_l'],'lowerarm_r':r['ub2']['lowerarm_r'],'hand_l':r['v_hand_l'],'hand_r':r['v_hand_r'],'spine_05':r['ub']['spine_05'],'neck_01':r['ub']['neck_01'],'head':r['ub']['head'],'pelvis':r['ub']['pelvis']}
            D=r['sh']['d']
        except Exception: continue
        for key,Pp in (('v',V),('d',D)):
            if 'head' not in Pp: continue
            l=met(Pp,f,rt,'l'); rr=met(Pp,f,rt,'r')
            acc[key].append(((l[0]+rr[0])/2,(l[1]+rr[1])/2,(l[2]+rr[2])/2,min(l[2],rr[2]),l[3],rr[3],incl(Pp['neck_01'],Pp['head'],f),incl(Pp['spine_05'],Pp['neck_01'],f),(Pp['head'][0]-Pp['pelvis'][0])*f[0]+(Pp['head'][1]-Pp['pelvis'][1])*f[1]))
    def fmt(A):
        if not A: return '-'*44
        m=lambda i:S.mean(a[i] for a in A)
        sw=((max(a[4] for a in A)-min(a[4] for a in A))+(max(a[5] for a in A)-min(a[5] for a in A)))/2
        return '%5.1f %5.1f %5.1f(%5.1f) %5.1f %5.1f %5.1f %5.1f'%(m(0),m(1),m(2),min(a[3] for a in A),sw,m(6),m(7),m(8))
    a=rows[len(rows)//2].get('sh',{}).get('a',{}) if isinstance(rows[len(rows)//2].get('sh'),dict) else {}
    sp=S.mean(math.hypot(r['vx'],r['vy']) for r in rows)
    print('%-3d %-26s %5.0f | %s | %s | %s %s %s  %s'%(s,plan[s][0][:26],sp,fmt(acc['v']),fmt(acc['d']),a.get('MoveA'),a.get('RelA'),a.get('RunA'),str((rows[len(rows)//2].get('gasp') or ['?'])[0])[-26:]))
