# an_cs.py <rec.json>...: fixed-camera framing per segment: head/pelvis normalized X min/mean/max, time outside the
# 0.28-0.43 band (excluding the first 0.4 s of a segment = start transient), speed mean, arm length range.
import json,sys,math
for fn in sys.argv[1:]:
    d=json.load(open(fn)); R=d['rows']; print('==',fn.split('/')[-1])
    for s in sorted(set(r['s'] for r in R)):
        rows=[r for r in R if r['s']==s]; t=0; hx=[];px=[];sp=[];out=0.0;arm=[]
        for r in rows:
            h=r['scr']['head'][0]; hx.append(h); px.append(r['scr']['pelvis'][0]); sp.append(math.hypot(r['vx'],r['vy'])); arm.append(r['arm'][0])
            if t>0.4 and not (0.28<=h<=0.43): out+=r['gdt']
            t+=r['gdt']
        print('  seg %2d %-16s %4.1fs spd %3.0f | headX %.2f/%.2f/%.2f pelvisX %.2f | out-of-band %.2fs | arm %.0f-%.0f'%(s,d['plan'][s][0] or 'release',t,sum(sp)/len(sp),min(hx),sum(hx)/len(hx),max(hx),sum(px)/len(px),out,min(arm),max(arm)))
