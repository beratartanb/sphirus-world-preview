# an_hipstab.py <label>...: stability of the hip-line correction through transitions. Hip-line yaw / tilt (driver thigh sockets, component
# space) frame to frame: largest single-frame jump (deg) and count of sign-alternating jumps > 1.5 deg over 3 consecutive frames
# (= oscillation signature of a feedback loop), whole recording, yaw unwrapped.
import json,sys,math
for lab in sys.argv[1:]:
    rows=[r for r in json.load(open('Saved/Codex/Grip_20261106/rec/%s.json'%lab))['rows'] if r['hook'].get('pd')]
    out=[]
    for nm,fn in (('yaw',lambda p: math.degrees(math.atan2(p['thigh_r'][1]-p['thigh_l'][1],p['thigh_r'][0]-p['thigh_l'][0]))),('tilt',lambda p: math.degrees(math.atan2(p['thigh_r'][2]-p['thigh_l'][2],math.hypot(p['thigh_r'][0]-p['thigh_l'][0],p['thigh_r'][1]-p['thigh_l'][1]))))):
        v=[fn(r['hook']['pd']) for r in rows]; u=[v[0]]
        for x in v[1:]: u.append(u[-1]+((x-u[-1]+180)%360-180))
        d=[u[i]-u[i-1] for i in range(1,len(u))]; osc=sum(1 for i in range(2,len(d)) if abs(d[i])>1.5 and abs(d[i-1])>1.5 and abs(d[i-2])>1.5 and d[i]*d[i-1]<0 and d[i-1]*d[i-2]<0)
        j=max(range(len(d)),key=lambda i:abs(d[i])); out.append('%s max jump %5.1f deg at t %.2f (%s), p99 %.1f, oscillation triples %d'%(nm,abs(d[j]),rows[j+1]['t'],rows[j+1]['gasp'][0][-22:],sorted(abs(x) for x in d)[int(len(d)*0.99)],osc))
    print('%-26s frames %d | %s'%(lab,len(rows),' | '.join(out)))
