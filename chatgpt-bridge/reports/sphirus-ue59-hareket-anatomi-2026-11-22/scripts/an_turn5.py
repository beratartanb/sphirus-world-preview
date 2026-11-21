# an_turn5.py <label>: per plan segment that changes direction while moving: turn angle (new velocity direction at the end of the
# segment vs the direction before), speed before, minimum speed and when, time back to 95 % of the segment's final speed, peak
# deceleration over 0.1 s, trunk momentum lean (PS_LP / PS_LR peak), worst planted-foot drift is reported by an_slide2.
import json, sys, math
D=json.load(open('Saved/Codex/Grip_20261106/rec/'+sys.argv[1]+'.json')); R=D['rows']; plan=D['plan']; segs={}
for r in R: segs.setdefault(r['s'],[]).append(r)
sp=lambda r: math.hypot(r['vx'],r['vy'])
for s in sorted(segs):
    if s==0 or s-1 not in segs: continue
    P=segs[s-1][-1]; W=segs[s]; v0=sp(P)
    if v0<100 or not plan[s][0].replace('LeftShift','').replace('LeftControl','').strip(): 
        if v0>=100:
            # stop: time to standstill and distance
            t0=W[0]['t']; ts=next((r['t']-t0 for r in W if sp(r)<5),None); dist=math.hypot(W[-1]['x']-W[0]['x'],W[-1]['y']-W[0]['y'])
            ps=[r['hook'].get('ps') for r in W if r['hook'].get('ps') and len(r['hook']['ps'])>19]
            print('s%-2d STOP from %3.0f: stand after %s s, %3.0f cm'%(s,v0,('%.2f'%ts) if ts else '-',dist))
        continue
    E=W[-1]; ang=math.degrees(math.acos(max(-1,min(1,(P['vx']*E['vx']+P['vy']*E['vy'])/max(1,v0*sp(E))))))
    t0=W[0]['t']; vmin=min(W[:90],key=sp); vend=sp(E); t95=next((r['t']-t0 for r in W if r['t']>vmin['t'] and sp(r)>=0.95*vend),None)
    pk=0
    for i in range(6,min(len(W),90)): pk=max(pk,(sp(W[i-6])-sp(W[i]))/max(1e-3,W[i]['t']-W[i-6]['t']))
    print('s%-2d [%-24s] turn %3.0f deg v %3.0f -> min %3.0f (%.0f %%) at +%.2f s, back to 95 %% of %3.0f at +%s s, peak decel %4.0f'%(s,plan[s][0],ang,v0,sp(vmin),100*sp(vmin)/v0,vmin['t']-t0,vend,('%.2f'%t95) if t95 else '-',pk))
