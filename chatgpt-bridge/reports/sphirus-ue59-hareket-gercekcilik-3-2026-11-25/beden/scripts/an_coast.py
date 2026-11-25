# an_coast.py <label> [obstacle face x rel. to start]: release speed / position, coast telemetry, stop distance, clips, closest approach
import json,sys,math
rows=json.load(open('Saved/Codex/Grip_20261106/rec/%s.json'%sys.argv[1]))['rows']; x0=rows[0]['x']; D=float(sys.argv[2]) if len(sys.argv)>2 else None
h=lambda r: r['hook'] if isinstance(r['hook'],dict) else {}
rel=[r for r in rows if r['s']==2]
if not rel: print(sys.argv[1],'no release'); sys.exit()
r0=rel[0]; ex=[h(r).get('ex') or [0,0,0,0,0] for r in rel]
st=next((r for r in rel if math.hypot(r['vx'],r['vy'])<10),rel[-1])
clips=[]
for r in rel:
    c=r['gasp'][0][-26:]
    if not clips or clips[-1]!=c: clips.append(c)
mx=max(r['x'] for r in rows)-x0
print('%s release x %+.0f v %.0f | avail %.0f floor %.0f budget %.0f coast %.2f s (dist %.0f) | rest after %.2f s at x %+.0f = %.0f cm | %s | max x %+.0f%s | z %.0f..%.0f | clips %s'%(sys.argv[1],r0['x']-x0,math.hypot(r0['vx'],r0['vy']),max(e[1] for e in ex),max(e[2] for e in ex),max(e[3] for e in ex),max(e[0] for e in ex),max(e[4] for e in ex),st['t']-r0['t'],st['x']-x0,st['x']-r0['x'],'obstacle face %+.0f -> gap %.0f'%(D,D-(mx+30)) if D is not None else '',mx,'',min(r['z'] for r in rel),max(r['z'] for r in rel),' > '.join(clips[:6])))
