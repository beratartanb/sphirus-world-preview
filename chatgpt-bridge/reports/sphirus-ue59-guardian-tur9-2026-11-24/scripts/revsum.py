# revsum.py <label>...: per reversal segment: flip-frame prediction, chosen clip, contact state at flip, time to zero speed, overshoot distance, time to 90% speed in new direction
import json,sys,math
for lab in sys.argv[1:]:
    d=json.load(open('Saved/Codex/Grip_20261106/rec/%s.json'%lab))['rows']; segs={}
    for i,r in enumerate(d): segs.setdefault(r['s'],i)
    for s,i0 in sorted(segs.items()):
        if i0<3: continue
        p=d[i0-1]; v0=(p['vx'],p['vy']); sp0=math.hypot(*v0)
        if sp0<150: continue
        ux,uy=v0[0]/sp0,v0[1]/sp0
        # flip frame = first row where the selected clip changes or speed drops
        j=i0
        while j<len(d)-1 and abs(math.hypot(d[j]['vx'],d[j]['vy'])-sp0)<8 and j<i0+12: j+=1
        r=d[j]; tj=r['hook'].get('tj') or []; fut=[(a,x*ux+y*uy) for a,x,y in tj if a>0.01]
        mx=max([q for a,q in fut] or [0]); tmx=[a for a,q in fut if q==mx][:1]
        k=j; x0=(d[j-1]['x'],d[j-1]['y'])
        while k<len(d)-1 and (d[k]['vx']*ux+d[k]['vy']*uy)>0: k+=1
        ov=(d[k]['x']-x0[0])*ux+(d[k]['y']-x0[1])*uy
        n=k
        while n<len(d)-1 and (d[n]['vx']*ux+d[n]['vy']*uy)>-0.9*sp0 and d[n]['s']==r['s']: n+=1
        h=r['hook']
        print('%s s%-2d t %.2f v0 %3.0f | cv L%3.0f R%3.0f | %-26s | predicted overshoot %3.0f cm at %.2f s | real: zero after %.2f s, overshoot %3.0f cm, -90%% after %.2f s'%(lab,r['s'],r['t'],sp0,h['cv'][0],h['cv'][1],r['gasp'][0][-26:],mx,(tmx or [0])[0],d[k]['t']-d[j-1]['t'],ov,d[n]['t']-d[j-1]['t']))
