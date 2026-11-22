# an_contw.py <label> [k=6]: WORLD-ORIENTED variant (component pose rotated by the actor yaw, capsule translation removed).
# an_cont.py <label> [k=6]: pose continuity of the VISIBLE body from hk_pose data (component space, so capsule motion is excluded).
# For every bone: velocity v_i = (p_i - p_{i-1})/dt; a "pop" = velocity step |v_i - v_{i-1}| that exceeds k x the local median step
# (11-frame window) and an absolute floor (120 cm/s). Events are grouped per frame; reports count per segment, the clip pair at
# the event, bones involved and the size. Also counts clip switches and database switches per segment.
import json, sys, math
lab=sys.argv[1]; K=float(sys.argv[2]) if len(sys.argv)>2 else 6.0; FL=float(sys.argv[3]) if len(sys.argv)>3 else 120.0
D=json.load(open('Saved/Codex/Grip_20261106/rec/'+lab+'.json')); R=D['rows']; plan=D.get('plan') or []
BN=[b for b in R[5]['hook']['pv'].keys()]
def med(v): s=sorted(v); return s[len(s)//2]
ev={}  # frame -> [(bone,step)]
for src in ('pv',):
    for b in BN:
        P=[]
        for r in R:
            p=r['hook'][src][b]; a=math.radians(r['yaw']-90.0); c=math.cos(a); s_=math.sin(a); P.append((p[0]*c-p[1]*s_, p[0]*s_+p[1]*c, p[2]))
        T=[r['t'] for r in R]
        V=[(0,0,0)]+[tuple((P[i][j]-P[i-1][j])/max(1e-3,T[i]-T[i-1]) for j in range(3)) for i in range(1,len(P))]
        S=[0.0]+[math.dist(V[i],V[i-1]) for i in range(1,len(V))]
        for i in range(6,len(S)-6):
            m=med(S[i-5:i]+S[i+1:i+6])
            if S[i]>FL and S[i]>K*max(m,8.0): ev.setdefault(i,[]).append((b,S[i]))
seg={}; 
for i,l in ev.items(): seg.setdefault(R[i]['s'],[]).append(i)
sw={}; dbs={}
for i in range(1,len(R)):
    if R[i]['gasp'][0]!=R[i-1]['gasp'][0]: sw[R[i]['s']]=sw.get(R[i]['s'],0)+1
    if R[i]['gasp'][1]!=R[i-1]['gasp'][1]: dbs[R[i]['s']]=dbs.get(R[i]['s'],0)+1
print('%s: %d frames, %d pop frames (k %.0f, floor %.0f cm/s)'%(lab,len(R),len(ev),K,FL))
for s in sorted(set(r['s'] for r in R)):
    rr=[r for r in R if r['s']==s]; keys=plan[s][0] if s<len(plan) else '?'
    print(' s%-2d [%-22s] %.1fs clip sw %d db sw %d pops %d'%(s,keys,rr[-1]['t']-rr[0]['t'],sw.get(s,0),dbs.get(s,0),len(seg.get(s,[]))))
    for i in sorted(seg.get(s,[]))[:int(sys.argv[4]) if len(sys.argv)>4 else 6]:
        l=sorted(ev[i],key=lambda x:-x[1]); t0=[r['t'] for r in R if r['s']==s][0]
        print('     t %.3f (+%.2f) dt %.3f %s -> %s | %s'%(R[i]['t'],R[i]['t']-t0,R[i]['t']-R[i-1]['t'],str(R[i-1]['gasp'][0])[-26:],str(R[i]['gasp'][0])[-26:],' '.join('%s:%.0f'%(b.replace('upperarm','ua').replace('lowerarm','la'),v) for b,v in l[:6])))
