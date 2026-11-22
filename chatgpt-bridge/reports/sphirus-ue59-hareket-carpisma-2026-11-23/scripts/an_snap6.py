# an_snap6.py <label...>: planted-foot lock-release snaps. Foot acceleration events of the visible ball in WORLD space: a frame where the
# ball's velocity changes by more than 900 cm/s within one frame while the ball is within 8 cm of the ground (a foot that is on the floor
# and is suddenly pulled). Lists the 6 largest (time, foot, one-frame jump in cm, clip) and the count; swing-phase frames are excluded.
import json,sys,math
for lab in sys.argv[1:]:
    R=json.load(open('Saved/Codex/Grip_20261106/rec/'+lab+'.json'))['rows']; R=[r for r in R if isinstance(r.get('hook'),dict) and r['t']>1.0]; E=[]
    for s in 'lr':
        for i in range(2,len(R)):
            a=R[i]['ub']['ball_'+s]; b=R[i-1]['ub']['ball_'+s]; c=R[i-2]['ub']['ball_'+s]; d1=R[i]['gdt'] or 1/60; d0=R[i-1]['gdt'] or 1/60
            v1=(math.hypot(a[0]-b[0],a[1]-b[1]))/d1; v0=(math.hypot(b[0]-c[0],b[1]-c[1]))/d0
            g=R[i]['gnd']['f'][0 if s=='l' else 1]; h=a[2]-g[0] if g else 99
            if h<8 and v1-v0>900 and R[i]['hook']['cv'][0 if s=='l' else 1]<50: E.append((v1*d1,R[i]['t'],s,str(R[i]['gasp'][0])[-28:],v1-v0))
    E.sort(reverse=True)
    print('%-12s snaps %2d | %s'%(lab,len(E),' ; '.join('t %.2f %s %.1fcm %s'%(e[1],e[2],e[0],e[3]) for e in E[:6])))
