# an_popsum.py <label...>: world-oriented pose pops (an_contw rule) split into UPPER-BODY frames (any of pelvis/spine/neck/head/
# clavicle/arm/hand bones above the threshold) and LEG-ONLY frames; largest upper-body step in cm per frame; 1-frame clip visits.
import json, sys, math
def med(v): s=sorted(v); return s[len(s)//2]
for lab in sys.argv[1:]:
    try: D=json.load(open('Saved/Codex/Grip_20261106/rec/'+lab+'.json'))
    except Exception as e: print(lab,'missing'); continue
    R=D['rows']; BN=list(R[5]['hook']['pv'].keys()); ev={}; big=0
    for b in BN:
        P=[]
        for r in R:
            p=r['hook']['pv'][b]; a=math.radians(r['yaw']-90.0); c=math.cos(a); s_=math.sin(a); P.append((p[0]*c-p[1]*s_, p[0]*s_+p[1]*c, p[2]))
        T=[r['t'] for r in R]; V=[(0,0,0)]+[tuple((P[i][j]-P[i-1][j])/max(1e-3,T[i]-T[i-1]) for j in range(3)) for i in range(1,len(P))]
        S=[0.0]+[math.dist(V[i],V[i-1]) for i in range(1,len(V))]
        for i in range(6,len(S)-6):
            m=med(S[i-5:i]+S[i+1:i+6])
            if S[i]>120.0 and S[i]>6.0*max(m,8.0):
                ev.setdefault(i,[]).append(b)
                if not any(k in b for k in ('foot','ball','calf','thigh')): big=max(big,S[i]*(T[i]-T[i-1]))
    up=[i for i,l in ev.items() if any(not any(k in b for k in ('foot','ball','calf','thigh')) for b in l)]
    one=sum(1 for i in range(1,len(R)-1) if R[i]['gasp'][0]!=R[i-1]['gasp'][0] and R[i]['gasp'][0]!=R[i+1]['gasp'][0])
    print('%-12s frames %5d | pop frames %3d: upper body %3d, legs only %3d | largest upper-body step %4.1f cm | one-frame clip visits %d'%(lab,len(R),len(ev),len(up),len(ev)-len(up),big,one))
