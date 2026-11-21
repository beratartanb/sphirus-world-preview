# an_stopphase.py <label:planfile> ... : for every release-to-stop event: gait phase at the release frame (contact curves L/R, ball heights,
# which foot is ahead along the travel direction, cm) -> stop clip chosen 0.1 s later and the worst planted-foot drift in the next 0.6 s.
import json, sys, math, ast
for arg in sys.argv[1:]:
    lab,pf=arg.split(':'); plan=ast.literal_eval(open('Saved/UE59Work/'+pf+'.txt').read())
    R=json.load(open('Saved/Codex/Grip_20261106/rec/'+lab+'.json')); R=R['rows'] if isinstance(R,dict) else R
    R=[r for r in R if isinstance(r.get('hook'),dict) and r['hook'].get('cv')]
    for i in range(1,len(R)):
        r=R[i]; p=R[i-1]
        if r['s']!=p['s'] and 0<r['s']<len(plan) and plan[r['s']][0]=='' and plan[p['s']][0]!='':
            v=math.hypot(p['vx'],p['vy'])
            if v<100: continue
            d=(p['vx']/v,p['vy']/v); bl=p['ub']['ball_l']; br=p['ub']['ball_r']; ahead=(bl[0]-br[0])*d[0]+(bl[1]-br[1])*d[1]
            worst=0; wf=''
            for k,b in ((0,'ball_l'),(1,'ball_r')):
                j=i
                while j<len(R) and R[j]['t']<r['t']+0.6:
                    if R[j]['hook']['cv'][k]<10:
                        q=j; p0=R[j]['ub'][b]; dd=0
                        while q<len(R) and R[q]['hook']['cv'][k]<10 and R[q]['t']<r['t']+1.2:
                            a=R[q]['ub'][b]; dd=max(dd,math.hypot(a[0]-p0[0],a[1]-p0[1])); q+=1
                        if dd>worst: worst=dd; wf='LR'[k]
                        j=q
                    else: j+=1
            c=next((x for x in R[i:] if x['t']>=r['t']+0.1),r)
            print('%-9s s%-2d [%-12s] v %3.0f cL %3.0f cR %3.0f zL %4.1f zR %4.1f Lahead %+5.1f -> %-30s worst %5.1f %s %s'%(lab,r['s'],plan[p['s']][0][:12],v,p['hook']['cv'][0],p['hook']['cv'][1],bl[2],br[2],ahead,str(c['gasp'][0])[-30:],worst,wf,'BAD' if worst>=10 else ''))
