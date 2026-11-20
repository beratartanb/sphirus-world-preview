# an_rev.py <label> <seg,seg,...>: reversal profile per segment: speed along the old direction every 0.1 s, time of zero crossing,
# time to 90 % of the final opposite speed, peak deceleration (cm/s2 over 0.1 s), clip sequence, Rc values
import json, sys, math
D=json.load(open('Saved/Codex/Grip_20261106/rec/'+sys.argv[1]+'.json')); R=D['rows']; plan=D['plan']
for s in [int(x) for x in sys.argv[2].split(',')]:
    W=[r for r in R if r['s']==s]; P=[r for r in R if r['s']==s-1][-1]; n=math.hypot(P['vx'],P['vy']) or 1; d0=(P['vx']/n,P['vy']/n); t0=W[0]['t']
    al=lambda r:r['vx']*d0[0]+r['vy']*d0[1]; tz=None; tb=None; vend=min(al(x) for x in W)
    for r in W:
        if tz is None and al(r)<=0: tz=r['t']-t0
        if tb is None and al(r)<=0.9*vend: tb=r['t']-t0
    line=[]; pk=0
    for k in range(0,13):
        r=min(W,key=lambda x:abs(x['t']-t0-k*0.1)); line.append('%4.0f'%al(r))
        if k: pk=max(pk,(float(line[-2])-float(line[-1]))/0.1)
    clips=[]
    for r in W:
        c=str(r['gasp'][0])[-22:]
        if not clips or clips[-1][0]!=c: clips.append([c,r['t']-t0])
    m=[r['hook'].get('m') for r in W[:40]]; rk=[x[7] for x in m if x and len(x)>9 and x[6]>0]
    print('%s s%d [%s] v_in %3.0f t0 %.2f t90 %s peak %4.0f | %s | K %s'%(sys.argv[1],s,plan[s][0],n,tz or -1,('%.2f'%tb) if tb else '-',pk,' '.join(line),('%.2f'%rk[-1]) if rk else '-'))
    print('     clips: '+' > '.join('%s@%.2f'%(c,t) for c,t in clips[:6]))
