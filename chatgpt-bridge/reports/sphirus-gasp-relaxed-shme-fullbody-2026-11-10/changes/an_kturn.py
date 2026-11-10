# an_kturn.py <label...>: keyboard direction changes (camera fixed). Per input segment: entry speed and heading, min speed,
# time until the velocity heading is within 20 deg of the new input direction, exit speed, selected clips, chest-lead peak (SphMotion
# not recorded directly -> visible-minus-driver shoulder-line yaw), and stop data on release.
import json,math,sys
def wrap(a): return (a+180)%360-180
DIR={'W':0,'W D':45,'D':90,'S D':135,'S':180,'S A':-135,'A':-90,'W A':-45}
for L in sys.argv[1:]:
    d=json.load(open('Saved/Codex/Grip_20261106/rec/%s.json'%L)); R=d['rows']; plan=d['plan']; print('==',L)
    camyaw=None
    for s,(keys,dur,*_) in enumerate(plan):
        rows=[r for r in R if r['s']==s]
        if not rows: continue
        k=' '.join(x for x in keys.split() if x!='LeftShift'); sh='LeftShift' in keys
        sp=[math.hypot(r['vx'],r['vy']) for r in rows]
        hd=[math.degrees(math.atan2(r['vy'],r['vx'])) for r in rows]
        cy=rows[0].get('cy',0) or 0
        t0=rows[0]['t']; txt='  seg %2d %-12s %4.1fs in %3.0f min %3.0f out %3.0f'%(s,keys or 'release',dur,sp[0],min(sp),sp[-1])
        if k in DIR and sp[0]>40:
            want=wrap(cy+DIR[k]); tt=None
            for r,h,v in zip(rows,hd,sp):
                if v>40 and abs(wrap(h-want))<20: tt=r['t']-t0; break
            txt+=' | turn %4.0f° reach %s'%(abs(wrap(hd[0]-want)),'%.2fs'%tt if tt is not None else '>seg')
        if not k:
            st=None
            for r,v in zip(rows,sp):
                if v<5: st=r['t']-t0; break
            if sp[0]>30: txt+=' | stop %s'%('%.2fs'%st if st is not None else '>seg')
        sel=[]
        for r in rows:
            g=(r.get('gasp') or [None])[0]
            if g and (not sel or sel[-1]!=g): sel.append(g)
        print(txt); print('       ',' > '.join(x.replace('M_Relaxed_','R:').replace('M_Neutral_','N:') for x in sel[:6]))
