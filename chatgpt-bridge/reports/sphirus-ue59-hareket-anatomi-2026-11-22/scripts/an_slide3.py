# an_slide3.py <label> <planfile> [min_cm=8]: planted-foot slide, two readings per contact (contact = driver clip curve < 10 for >= 0.08 s):
#   curve  = largest horizontal distance of the VISIBLE ball from where the curve contact began (the round 2-4 metric, unchanged)
#   ground = the same, counted only while the ball is really on the ground (ball height <= ground + GZ, GZ = 6.5 cm; the standing ball
#            height of this body is 3.3-4.6 cm), measured from the first grounded frame.  air = part of the contact with the foot above GZ.
# A contact whose curve reading is large but whose ground reading is small is an EARLY CONTACT FLAG (the clip says planted while the foot
# is still landing after a blend); it is listed separately and is not removed from the curve totals.
import json, sys, math, ast
lab=sys.argv[1]; plan=ast.literal_eval(open(sys.argv[2]).read()); mn=float(sys.argv[3]) if len(sys.argv)>3 else 8.0; GZ=6.5
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
                p0=R[i]['ub'][b]; d=0; g0=None; dg=0; air=0; lift=0
                for q in range(i,j):
                    p=R[q]['ub'][b]; d=max(d,math.hypot(p[0]-p0[0],p[1]-p0[1]))
                    g=R[q]['gnd']['f'][k]; h=(p[2]-g[0]) if g else 0; lift=max(lift,h)
                    if h<=GZ:
                        if g0 is None: g0=p
                        dg=max(dg,math.hypot(p[0]-g0[0],p[1]-g0[1]))
                    else:
                        air+=1
                        if g0 is not None and h>GZ+3: g0=None
                C.append(dict(s=R[i]['s'],t=R[i]['t'],dur=R[j-1]['t']-R[i]['t'],foot='LR'[k],drift=d,ground=dg,air=air/float(j-i),lift=lift,sp=math.hypot(R[i]['vx'],R[i]['vy']),clip=str((R[i].get('gasp') or ['?'])[0]),ts=R[i]['t']-next(r['t'] for r in R if r['s']==R[i]['s'])))
            i=j
        else: i+=1
C.sort(key=lambda c:c['t'])
def keys(s): return plan[s][0] if 0<=s<len(plan) else '?'
def sh(x): return x.replace(' LeftShift','+Sh').replace(' LeftControl','+Ct') or '-'
print('%s: %d contacts'%(lab,len(C)))
for c in C:
    if c['drift']>=mn or c['ground']>=mn: print('  t %6.2f s%-2d [%s]->[%s] +%.2fs foot %s dur %.2f curve %5.1f ground %5.1f air %2.0f%% lift %4.1f v %3.0f %s%s'%(c['t'],c['s'],sh(keys(c['s']-1)),sh(keys(c['s'])),c['ts'],c['foot'],c['dur'],c['drift'],c['ground'],100*c['air'],c['lift'],c['sp'],c['clip'][-30:],'  EARLY-FLAG' if c['drift']>=10 and c['ground']<0.5*c['drift'] else ''))
D=sorted(c['drift'] for c in C); G=sorted(c['ground'] for c in C)
if D: print('  TOTAL n %d | curve: mean %.1f p90 %.1f worst %.1f, >=10: %d, >=20: %d | ground: mean %.1f p90 %.1f worst %.1f, >=10: %d, >=20: %d'%(len(D),sum(D)/len(D),D[int(0.9*(len(D)-1))],D[-1],sum(1 for d in D if d>=10),sum(1 for d in D if d>=20),sum(G)/len(G),G[int(0.9*(len(G)-1))],G[-1],sum(1 for d in G if d>=10),sum(1 for d in G if d>=20)))
