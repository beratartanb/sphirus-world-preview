# an_revslide.py <label> <planfile> [win=1.3]: planted-foot drift after every input change between two MOVING key sets (turn / reversal).
# contact per foot = visible ball < 5 cm above traced ground and |vertical ball speed| < 20 cm/s for >= 0.10 s (sim time);
# drift = largest horizontal ball distance from where that contact began. Reports t_rev (time until velocity along the new input > 0),
# speed minimum and its time, worst drift L/R, pelvis drop vs the 0.3 s before the change.
import json, sys, math, ast
lab=sys.argv[1]; plan=ast.literal_eval(open(sys.argv[2]).read()); win=float(sys.argv[3]) if len(sys.argv)>3 else 1.3
R=json.load(open('Saved/Codex/Grip_20261106/rec/'+lab+'.json')); R=R['rows'] if isinstance(R,dict) else R
def dirv(keys,cy):
    f=sum((k=='W')-(k=='S') for k in keys.split()); r=sum((k=='D')-(k=='A') for k in keys.split())
    if f==0 and r==0: return None
    a=math.radians(cy); x=f*math.cos(a)-r*math.sin(a); y=f*math.sin(a)+r*math.cos(a); n=math.hypot(x,y); return (x/n,y/n)
def drift(S,k,b):
    fl=[False]
    for j in range(1,len(S)):
        ga,gb=S[j-1]['gnd']['f'][k],S[j]['gnd']['f'][k]
        if not(ga and gb): fl.append(False); continue
        dt=max(1e-3,S[j]['t']-S[j-1]['t']); za=S[j-1]['ub'][b][2]-ga[0]; zb=S[j]['ub'][b][2]-gb[0]
        fl.append(za<5 and zb<5 and abs((S[j]['ub'][b][2]-S[j-1]['ub'][b][2])/dt)<20)
    w=0; j=0
    while j<len(fl):
        if fl[j]:
            i=j
            while j<len(fl) and fl[j]: j+=1
            if S[j-1]['t']-S[i]['t']>=0.10:
                p0=S[i]['ub'][b]; w=max(w,max(math.hypot(S[q]['ub'][b][0]-p0[0],S[q]['ub'][b][1]-p0[1]) for q in range(i,j)))
        else: j+=1
    return w
tot=[]
for i in range(1,len(R)):
    if R[i]['s']==R[i-1]['s'] or R[i]['s']>=len(plan): continue
    a,b=R[i-1],R[i]; d0=dirv(plan[a['s']][0],a['cy']); d1=dirv(plan[b['s']][0],b['cy'])
    if not d1 or (d0 and (d0[0]*d1[0]+d0[1]*d1[1])>0.95): continue
    if not d0: d0=(-d1[0],-d1[1]) if False else d1
    S=[r for r in R[i-1:] if r['t']<=b['t']+win and r['s']==b['s']]
    if len(S)<5: continue
    trev=next((r['t']-b['t'] for r in S if r['vx']*d1[0]+r['vy']*d1[1]>0),None); sp=[math.hypot(r['vx'],r['vy']) for r in S]; im=sp.index(min(sp))
    pre=[r['ub']['pelvis'][2]-r['z'] for r in R[max(0,i-20):i]]; pd=sum(pre)/len(pre)-min(r['ub']['pelvis'][2]-r['z'] for r in S)
    dl=drift(S,0,'ball_l'); dr=drift(S,1,'ball_r'); tot.append(max(dl,dr))
    ang=math.degrees(math.acos(max(-1,min(1,d0[0]*d1[0]+d0[1]*d1[1])))) if plan[a['s']][0] else -1
    print('t %6.2f [%s]->[%s] %3.0f deg v_in %3.0f | t_rev %s vmin %3.0f @%.2f | drift L %4.1f R %4.1f | pelvis drop %4.1f | dur %.2f'%(b['t'],plan[a['s']][0],plan[b['s']][0],ang,math.hypot(a['vx'],a['vy']),('%.2f'%trev) if trev is not None else '-',min(sp),S[im]['t']-b['t'],dl,dr,pd,S[-1]['t']-b['t']))
if tot: print('WORST %.1f  MEAN %.1f  n %d'%(max(tot),sum(tot)/len(tot),len(tot)))
