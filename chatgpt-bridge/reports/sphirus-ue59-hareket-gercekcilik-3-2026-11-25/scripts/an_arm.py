# an_arm.py <label> <plan>: arm anatomy and arm / leg clearance of the VISIBLE body.
#  anatomy (first idle frames): upper arm (shoulder joint -> elbow), forearm (elbow -> wrist), shoulder width, stature from eye height
#  (eye height = 0.936 stature), ratios vs adult female reference (upper arm 0.186, forearm 0.146 of stature; biacromial 0.215).
#  per plan segment: wrist and mid-forearm clearance to the same-side thigh (axis hip joint -> knee, radius 9.5 -> 6.5 cm) and to the
#  hip block (lateral distance of the wrist from the pelvis midline when it is at hip height); wrist-to-wrist and elbow-to-elbow
#  distance vs shoulder joint distance. clearance < 3 cm = the wrist (half thickness ~3 cm) is inside the thigh / shorts.
import json,sys,math
lab=sys.argv[1]; rows=json.load(open('Saved/Codex/Grip_20261106/rec/%s.json'%lab))['rows']; plan=eval(open(sys.argv[2]).read())
sub=lambda a,b:[a[i]-b[i] for i in range(3)]; dot=lambda a,b:sum(a[i]*b[i] for i in range(3)); ln=lambda a:math.sqrt(dot(a,a))
def seg(p,a,b,ra,rb):
    ab=sub(b,a); t=max(0.0,min(1.0,dot(sub(p,a),ab)/max(dot(ab,ab),1e-6))); q=[a[i]+ab[i]*t for i in range(3)]; return ln(sub(p,q))-(ra+(rb-ra)*t)
key=lambda x: x.replace(' LeftShift','+Sh').replace(' LeftControl','+Ct') or '-'
def A(r): return {'upperarm_l':r['ub']['upperarm_l'],'upperarm_r':r['ub']['upperarm_r'],'lowerarm_l':r['ub2']['lowerarm_l'],'lowerarm_r':r['ub2']['lowerarm_r'],'hand_l':r['v_hand_l'],'hand_r':r['v_hand_r']}
r0=rows[10]; a=A(r0)
ua=(ln(sub(a['upperarm_l'][:3],a['lowerarm_l'][:3]))+ln(sub(a['upperarm_r'][:3],a['lowerarm_r'][:3])))/2; fa=(ln(sub(a['lowerarm_l'][:3],a['hand_l'][:3]))+ln(sub(a['lowerarm_r'][:3],a['hand_r'][:3])))/2
sw=ln(sub(a['upperarm_l'][:3],a['upperarm_r'][:3])); gz=r0['z']-88.2+0.0; eye=(r0['eyes'][0][2]+r0['eyes'][1][2])/2-(r0['z']-88.2); st=eye/0.936
hipw=ln(sub(r0['ub']['thigh_l'][:3],r0['ub']['thigh_r'][:3]))
print('%s ANATOMY upper arm %.1f cm (%.3f of stature, ref 0.186) | forearm %.1f (%.3f, ref 0.146) | shoulder joints %.1f (%.3f, biacromial ref 0.215 incl. ~4 cm soft tissue) | hip joints %.1f | eye height %.1f -> stature %.1f | wrist height idle %.1f (%.3f of stature, ref 0.485)'%(lab[-20:],ua,ua/st,fa,fa/st,sw,sw/st,hipw,eye,st,(a['hand_l'][2]+a['hand_r'][2])/2-(r0['z']-88.2),((a['hand_l'][2]+a['hand_r'][2])/2-(r0['z']-88.2))/st))
segs={}
for i,r in enumerate(rows): segs.setdefault(r['s'],[]).append(i)
for s,ix in sorted(segs.items()):
    if s>=len(plan): continue
    ix=ix[len(ix)//3:]  # steady part
    cw=[];cf=[];lat=[];ww=[];ee=[]
    for i in ix:
        r=rows[i]; a=A(r); u=r['ub']; c=r['ub2']
        mid=[(u['thigh_l'][k]+u['thigh_r'][k])/2 for k in range(3)]; ax=sub(u['thigh_r'][:3],u['thigh_l'][:3]); n=ln(ax); ax=[x/n for x in ax]
        for sd in ('l','r'):
            h=a['hand_'+sd][:3]; e=a['lowerarm_'+sd][:3]; m=[(h[k]+e[k])/2 for k in range(3)]; th=u['thigh_'+sd][:3]; kn=c['calf_'+sd][:3]
            cw.append(seg(h,th,kn,9.5,6.5)); cf.append(seg(m,th,kn,9.5,6.5))
            if abs(h[2]-th[2])<12: lat.append(abs(dot(sub(h,mid),ax)))
        ww.append(ln(sub(a['hand_l'][:3],a['hand_r'][:3]))); ee.append(ln(sub(a['lowerarm_l'][:3],a['lowerarm_r'][:3])))
    v=math.hypot(rows[ix[-1]]['vx'],rows[ix[-1]]['vy'])
    print('s%-2d [%-9s] v %3.0f | wrist-thigh clearance min %5.1f p5 %5.1f, inside (<3 cm) %2.0f %% | forearm min %5.1f | wrist from midline at hip height min %s (hip half-width ~18.5) | wrists apart min %4.1f mean %4.1f | elbows apart min %4.1f (shoulders %.1f) | %s'%(s,key(plan[s][0]),v,min(cw),sorted(cw)[len(cw)//20],100.0*sum(1 for x in cw if x<3)/len(cw),min(cf),('%4.1f'%min(lat)) if lat else '  - ',min(ww),sum(ww)/len(ww),min(ee),sw,rows[ix[-1]]['gasp'][0][-22:]))
