# an_weight.py <label> <plan>: starts and stops as the capsule performs them.
#  START (segment begins from < 15 cm/s): target speed, time to 50 % / 90 % of it, peak acceleration (cm/s2, 0.1 s window), distance at 0.3 s
#  STOP  (keys released at > 100 cm/s): speed at release, time to < 10 cm/s, stop distance, peak deceleration
#  GAIT CHANGE (speed change > 80 cm/s between moving segments): from -> to, time to cover 90 % of the change
import json,sys,math
lab=sys.argv[1]; rows=json.load(open('Saved/Codex/Grip_20261106/rec/%s.json'%lab))['rows']; plan=eval(open(sys.argv[2]).read())
sp=lambda r: math.hypot(r['vx'],r['vy'])
segs={}
for i,r in enumerate(rows): segs.setdefault(r['s'],[]).append(i)
def pk(i0,i1,sign):
    b=0
    for i in range(i0,i1):
        j=i
        while j<i1 and rows[j]['t']-rows[i]['t']<0.1: j+=1
        if j<i1: b=max(b,sign*(sp(rows[j])-sp(rows[i]))/(rows[j]['t']-rows[i]['t']))
    return b
for s,ix in sorted(segs.items()):
    if s==0 or s>=len(plan): continue
    i0,i1=ix[0],ix[-1]; k=plan[s][0]; kp=plan[s-1][0]; v0=sp(rows[i0-1]); t0=rows[i0]['t']
    key=lambda x: x.replace(' LeftShift','+Sh').replace(' LeftControl','+Ct') or '-'
    if k and v0<15:
        vt=max(sp(rows[i]) for i in ix)
        if vt<80: continue
        t5=next((rows[i]['t']-t0 for i in ix if sp(rows[i])>=0.5*vt),-1); t9=next((rows[i]['t']-t0 for i in ix if sp(rows[i])>=0.9*vt),-1)
        j=next((i for i in ix if rows[i]['t']-t0>=0.3),i1); d=math.hypot(rows[j]['x']-rows[i0]['x'],rows[j]['y']-rows[i0]['y'])
        print('%s s%-2d START [%-9s] v %3.0f | 50%% %.2f s  90%% %.2f s | peak accel %4.0f | dist@0.3s %3.0f cm | %s'%(lab[-20:],s,key(k),vt,t5,t9,pk(i0,min(i1,i0+60),1),d,rows[min(i1,i0+12)]['gasp'][0][-28:]))
    elif not k and v0>100:
        j=next((i for i in ix if sp(rows[i])<10),i1); d=math.hypot(rows[j]['x']-rows[i0]['x'],rows[j]['y']-rows[i0]['y'])
        print('%s s%-2d STOP  [%-9s] v %3.0f | to rest %.2f s | dist %3.0f cm | peak decel %4.0f | %s'%(lab[-20:],s,key(kp),v0,rows[j]['t']-t0,d,pk(i0,j,-1),rows[min(i1,i0+12)]['gasp'][0][-28:]))
    elif k and v0>=15:
        ve=sp(rows[i1])
        if abs(ve-v0)>80 and ('A' in k.split())==('A' in kp.split()) and ('D' in k.split())==('D' in kp.split()) and ('S' in k.split())==('S' in kp.split()):
            t9=next((rows[i]['t']-t0 for i in ix if abs(sp(rows[i])-v0)>=0.9*abs(ve-v0)),-1)
            print('%s s%-2d GAIT  [%-9s>%-9s] %3.0f -> %3.0f | 90%% %.2f s | %s'%(lab[-20:],s,key(kp),key(k),v0,ve,t9,rows[min(i1,i0+20)]['gasp'][0][-28:]))
