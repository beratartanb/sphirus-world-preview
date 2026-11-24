import json,sys
# vc.py <label> <t0> <t1> : compact t / vx / vy / clip / state / brake fields
lab,t0,t1=sys.argv[1],float(sys.argv[2]),float(sys.argv[3])
for r in json.load(open('Saved/Codex/Grip_20261106/rec/%s.json'%lab))['rows']:
    if t0<=r['t']<=t1:
        g=r['gasp']; print('%6.2f v(%5.0f,%5.0f) %-30s %-6s mo %s'%(r['t'],r['vx'],r['vy'],g[0][-30:],g[3][:6],r.get('mo',[''])[-1]))
