# an_contact5.py <label> <t0> <t1> [step=1]: frame dump around a contact. Per frame: time, segment, capsule speed + travel direction (deg, world),
# actor yaw, driver clip, contact curves L/R (0 = planted), VISIBLE ball L/R horizontal speed (cm/s, world) and height, motion vars
# m = [StK,StT,BrakeDecel,BrakeLatchSpeed,StartT,TurnCap,RcW,RcK,RcA,RcExit,RevFricMul,TlG,TlPeak].
import json, sys, math
lab=sys.argv[1]; t0=float(sys.argv[2]); t1=float(sys.argv[3]); st=int(sys.argv[4]) if len(sys.argv)>4 else 1
R=json.load(open('Saved/Codex/Grip_20261106/rec/'+lab+'.json')); R=R['rows'] if isinstance(R,dict) else R
prev=None; n=0
for r in R:
    if r['t']<t0-0.05 or r['t']>t1: prev=r; continue
    if prev is not None and r['t']>=t0:
        n+=1
        if n%st==0:
            dt=max(r['t']-prev['t'],1e-4); h=r.get('hook') or {}; cv=h.get('cv') or [0,0,0]; m=h.get('m') or []
            def sp(b): a=r['ub'][b]; p=prev['ub'][b]; return math.hypot(a[0]-p[0],a[1]-p[1])/dt
            v=math.hypot(r['vx'],r['vy']); d=math.degrees(math.atan2(r['vy'],r['vx'])) if v>5 else 0
            g=(r.get('gasp') or ['?','?'])
            print('%6.2f s%-2d v%4.0f dir%5.0f yaw%5.0f %-34s c %3.0f %3.0f | ballL %4.0f z%4.1f ballR %4.0f z%4.1f | StK %.2f St %.2f RcW %.2f RcK %.2f Tcap %5.0f TlG %.2f mont %s'%(
                r['t'],r['s'],v,d,r['yaw'],str(g[0])[-34:],cv[0],cv[1],sp('ball_l'),r['ub']['ball_l'][2],sp('ball_r'),r['ub']['ball_r'][2],
                m[0] if m else 0,m[4] if m else 0,m[6] if m else 0,m[7] if m else 0,min(m[5],99999) if m else 0,m[11] if len(m)>11 else 0,r.get('mont')))
    prev=r
