# an_apa.py <label> <planfile>: anticipatory weight transfer in starts from standstill (visible body).
# lateral axis = actor right at the key press. pelvis offset = pelvis lateral position minus the midpoint of the two ball bones.
# Reports: offset at the key press, the first foot to unplant (driver contact curve > 50) and when, the peak pelvis shift toward the
# STANCE foot before that toe-off (cm, relative to the offset at the key press), pelvis drop and forward lean of the chest at toe-off.
import json,sys,math,ast
lab=sys.argv[1]; plan=ast.literal_eval(open(sys.argv[2]).read())
R=json.load(open('Saved/Codex/Grip_20261106/rec/'+lab+'.json')); R=R['rows'] if isinstance(R,dict) else R
for i in range(1,len(R)):
    if R[i]['s']==R[i-1]['s'] or R[i]['s']>=len(plan): continue
    k=plan[R[i]['s']][0]
    if not any(x in k.split() for x in 'WASD') or math.hypot(R[i-1]['vx'],R[i-1]['vy'])>20: continue
    S=[r for r in R[i:] if r['s']==R[i]['s'] and r['t']-R[i]['t']<=1.2]; t0=S[0]['t']
    a=math.radians(S[0]['yaw']); rt=(-math.sin(a),math.cos(a))
    def off(r):
        u=r['ub']; mx=(u['ball_l'][0]+u['ball_r'][0])/2; my=(u['ball_l'][1]+u['ball_r'][1])/2
        return (u['pelvis'][0]-mx)*rt[0]+(u['pelvis'][1]-my)*rt[1]
    o0=off(S[0]); to=None
    for r in S:
        cv=r['hook']['cv']
        if cv[0]>50 or cv[1]>50: to=(r['t']-t0,'L' if cv[0]>50 else 'R'); break
    if not to: continue
    pre=[r for r in S if r['t']-t0<=to[0]]
    sgn=1 if to[1]=='L' else -1   # stance foot is the other one: left lifts -> stance right (+right axis)
    shift=max((off(r)-o0)*sgn for r in pre); drop=S[0]['ub']['pelvis'][2]-min(r['ub']['pelvis'][2] for r in pre)
    print('  t %6.2f start [%s] first toe-off %s at %.2f s | pelvis toward stance foot %4.1f cm before toe-off, pelvis drop %4.1f cm | %s'%(t0,k.replace(' LeftShift','+Sh').replace(' LeftControl','+Ct'),to[1],to[0],shift,drop,str((S[min(15,len(S)-1)].get('gasp') or ['?'])[0])[-30:]))
