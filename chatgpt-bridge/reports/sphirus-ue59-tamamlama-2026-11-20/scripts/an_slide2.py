# an_slide2.py <label> <planfile> [min_cm=8]: planted-foot slide over the WHOLE recording, contact taken from the driver clip.
# Needs the hk_gait hook (row.hook.cv = contact_l, contact_r, movedata_speed of the driver pose; contact curve 0 = planted, 100 = free).
# contact (per foot) = curve < 10 for >= 0.08 s of simulated time. Per contact:
#   drift = largest horizontal distance of the VISIBLE ball bone from where the contact began (world, cm)
#   path  = summed horizontal ball travel during the contact (cm); lift = max ball height above traced ground during the contact
# A contact is attributed to the plan segment in which it starts; "event" = keys of the previous segment -> keys of this one.
# Output: every contact with drift >= min_cm, then per-segment worst drift, then totals (count, mean, p90, worst).
import json, sys, math, ast
lab=sys.argv[1]; plan=ast.literal_eval(open(sys.argv[2]).read()); mn=float(sys.argv[3]) if len(sys.argv)>3 else 8.0
R=json.load(open('Saved/Codex/Grip_20261106/rec/'+lab+'.json')); R=R['rows'] if isinstance(R,dict) else R
R=[r for r in R if isinstance(r.get('hook'),dict) and r['hook'].get('cv')]
C=[]
for k,b in ((0,'ball_l'),(1,'ball_r')):
    i=0
    while i<len(R):
        if R[i]['hook']['cv'][k]<10:
            j=i
            while j<len(R) and R[j]['hook']['cv'][k]<10: j+=1
            if R[j-1]['t']-R[i]['t']>=0.08:
                p0=R[i]['ub'][b]; d=0; pa=0; lift=0
                for q in range(i+1,j):
                    p=R[q]['ub'][b]; pp=R[q-1]['ub'][b]; d=max(d,math.hypot(p[0]-p0[0],p[1]-p0[1])); pa+=math.hypot(p[0]-pp[0],p[1]-pp[1])
                    g=R[q]['gnd']['f'][k]; lift=max(lift,(p[2]-g[0]) if g else 0)
                sp=math.hypot(R[i]['vx'],R[i]['vy'])
                C.append(dict(s=R[i]['s'],t=R[i]['t'],dur=R[j-1]['t']-R[i]['t'],foot='LR'[k],drift=d,path=pa,lift=lift,sp=sp,clip=str((R[i].get('gasp') or ['?'])[0]),ts=R[i]['t']-next(r['t'] for r in R if r['s']==R[i]['s'])))
            i=j
        else: i+=1
C.sort(key=lambda c:c['t'])
def keys(s): return plan[s][0] if 0<=s<len(plan) else '?'
def sh(x): return x.replace(' LeftShift','+Sh').replace(' LeftControl','+Ct') or '-'
print('%s: %d contacts'%(lab,len(C)))
for c in C:
    if c['drift']>=mn: print('  t %6.2f s%-2d [%s]->[%s] +%.2fs foot %s dur %.2f drift %5.1f path %5.1f lift %4.1f speed %3.0f %s'%(c['t'],c['s'],sh(keys(c['s']-1)),sh(keys(c['s'])),c['ts'],c['foot'],c['dur'],c['drift'],c['path'],c['lift'],c['sp'],c['clip'][-30:]))
seg={}
for c in C: seg[c['s']]=max(seg.get(c['s'],0),c['drift'])
print('  per segment worst: '+'  '.join('s%d[%s]:%.0f'%(s,sh(keys(s)),v) for s,v in sorted(seg.items())))
D=sorted(c['drift'] for c in C)
if D: print('  TOTAL n %d mean %.1f p90 %.1f worst %.1f  | >=10 cm: %d  >=20 cm: %d'%(len(D),sum(D)/len(D),D[int(0.9*(len(D)-1))],D[-1],sum(1 for d in D if d>=10),sum(1 for d in D if d>=20)))
