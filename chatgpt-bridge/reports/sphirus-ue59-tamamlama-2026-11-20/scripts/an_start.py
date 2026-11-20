# an_start.py <label> <planfile>: every start from standstill: t50/t90 of the segment's top speed, distance at 0.3 s, worst clip-contact drift
# of contacts that are active during the first 1.0 s after the key press (contact from the driver clip curve, hk_gait hook).
import json,sys,math,ast
lab=sys.argv[1]; plan=ast.literal_eval(open(sys.argv[2]).read())
R=json.load(open('Saved/Codex/Grip_20261106/rec/'+lab+'.json')); R=R['rows'] if isinstance(R,dict) else R
out=[]
for i in range(1,len(R)):
    if R[i]['s']==R[i-1]['s'] or R[i]['s']>=len(plan): continue
    k1=plan[R[i]['s']][0]; 
    if not any(x in k1.split() for x in 'WASD') or math.hypot(R[i-1]['vx'],R[i-1]['vy'])>20: continue
    S=[r for r in R[i:] if r['s']==R[i]['s']]; t0=S[0]['t']; vm=max(math.hypot(r['vx'],r['vy']) for r in S)
    t5=next(r['t']-t0 for r in S if math.hypot(r['vx'],r['vy'])>=0.5*vm); t9=next(r['t']-t0 for r in S if math.hypot(r['vx'],r['vy'])>=0.9*vm)
    d3=next(math.hypot(r['x']-S[0]['x'],r['y']-S[0]['y']) for r in S if r['t']-t0>=0.3)
    W=[r for r in S if r['t']-t0<=1.0]; worst=[]
    for k,b in ((0,'ball_l'),(1,'ball_r')):
        p0=None; d=0
        for r in W:
            if r['hook']['cv'][k]<10:
                if p0 is None: p0=r['ub'][b]
                d=max(d,math.hypot(r['ub'][b][0]-p0[0],r['ub'][b][1]-p0[1]))
            else: p0=None
        worst.append(d)
    out.append(max(worst))
    print('  t %6.2f start [%s] vmax %3.0f t50 %.2f t90 %.2f d(0.3s) %3.0f cm | first-step drift L %4.1f R %4.1f | %s'%(t0,k1.replace(' LeftShift','+Sh').replace(' LeftControl','+Ct'),vm,t5,t9,d3,worst[0],worst[1],str((S[min(20,len(S)-1)].get('gasp') or ['?'])[0])[-32:]))
print('%s starts n %d worst %.1f mean %.1f'%(lab,len(out),max(out),sum(out)/len(out)))
