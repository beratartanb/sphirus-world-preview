# an_dump6.py <label> <t0> <t1> [foot l|r] [every]: per-frame capsule / clip-curve / motion-component / foot trace of one event
import json,math,sys
lab=sys.argv[1]; t0=float(sys.argv[2]); t1=float(sys.argv[3]); ft=sys.argv[4] if len(sys.argv)>4 else 'l'; ev=int(sys.argv[5]) if len(sys.argv)>5 else 1
MK=('StK','StT','BrakeDecel','BrakeLatchSpeed','StartT','TurnCap','RcW','RcK','RcA','RcExit','RevFricMul','TlG','TlPeak','DmT','DmK','DmDecel')
R=json.load(open('Saved/Codex/Grip_20261106/rec/%s.json'%lab))['rows']; p0=None; pv=None; k=0
for r in R:
    if t0<=r['t']<=t1:
        k+=1
        h=r['hook']; m=dict(zip(MK,h['m'])); b=r['ub']['ball_'+ft]; sp=math.hypot(r['vx'],r['vy'])
        if p0 is None: p0=b; pv=sp
        if k%ev==0:
            print('t %.2f v %4.0f (a %6.0f) yaw %4.0f cL %3.0f cR %3.0f md %4.0f | StK %.2f Bd %5.0f | RcW %.1f K %.2f A %5.0f | Dm %.2f %5.0f | cap %6.0f | ball d %5.1f z %4.1f | %s'%(r['t'],sp,(sp-pv)/max(r['gdt'],1e-3),r.get('yaw',0),h['cv'][0],h['cv'][1],h['cv'][2],m['StK'],m['BrakeDecel'],m['RcW'],m['RcK'],m['RcA'],m['DmT'],m['DmDecel'],min(m['TurnCap'],99999),math.hypot(b[0]-p0[0],b[1]-p0[1]),b[2],str(r['gasp'][0])[-30:]))
        pv=sp
