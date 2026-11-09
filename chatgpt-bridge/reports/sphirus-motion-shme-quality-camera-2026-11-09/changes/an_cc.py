# an_cc.py <rec.json> [seg ...]: TRUE played clip per frame from the SphClip/SphTime curves (cm_curves1). Per segment:
# clip run-lengths (name@start->end, duration), blend frames (non-integer id), switches, restarts (time jumps back inside
# one clip), play rate (clip-time slope vs game time), capsule speed trace. With no segs: a per-segment summary table.
import json,sys,math
ids=json.load(open('Saved/Codex/Day_20261107/clipids.json')); LEN={k.replace('af_Loco_','').replace('af_Stand_',''):v['len'] for k,v in json.load(open('Saved/Codex/Day_20261107/trim_plan.json')).items()}; byid={v:k.replace('af_Loco_','').replace('af_Stand_','') for k,v in ids.items()}
d=json.load(open(sys.argv[1])); R=d['rows']; segs=[int(x) for x in sys.argv[2:]]
def runs(rows):
    out=[]; t=0.0; cur=None
    for r in rows:
        cc=r.get('cc'); gdt=r.get('gdt',1/30)
        if not cc: t+=gdt; continue
        cid,ct=cc; blend=abs(cid-round(cid))>0.02; name=byid.get(int(round(cid)),'?%s'%cid)
        if blend: name='~'
        if cur and cur['n']==name and blend:
            cur['tend']=t; cur['ct']=ct; cur['ctend']=ct; cur['ids'].add(round(cid,1))
        elif cur and cur['n']==name and not blend:
            if ct<cur['ct']-0.2 and not (cur['ct']>LEN.get(name,99)-0.25 and ct<0.3): cur['restart']+=1
            cur['ct']=ct; cur['tend']=t; cur['ctend']=ct
        else:
            if cur: out.append(cur)
            cur=dict(n=name,t0=t,tend=t,ct0=ct,ct=ct,ctend=ct,restart=0,ids={round(cid,1)})
        t+=gdt
    if cur: out.append(cur)
    return out
for s in sorted(set(r['s'] for r in R)):
    rows=[r for r in R if r['s']==s]
    if len(rows)<4: continue
    rs=runs(rows); real=[x for x in rs if x['n']!='~']; blendt=sum(x['tend']-x['t0'] for x in rs if x['n']=='~')
    sw=max(0,len(real)-1); rst=sum(x['restart'] for x in real)
    rates=[(x['ctend']-x['ct0'])/(x['tend']-x['t0']) for x in real if x['tend']-x['t0']>0.3]
    plan=d['plan'][s][0] or 'release'; T=sum(r.get('gdt',1/30) for r in rows)
    print('== seg %d %-14s %.1fs clips %d switches %d restarts %d blend %.2fs rate %s'%(s,plan,T,len(real),sw,rst,blendt,[round(x,2) for x in rates][:6]))
    if s in segs or not segs:
        for x in rs:
            if x['n']=='~':
                lo,hi=min(x['ids']),max(x['ids']); print('   %5.2f-%5.2f  ~blend %s -> %s'%(x['t0'],x['tend'],byid.get(int(lo),'?'),byid.get(int(hi)+1 if hi>int(hi) else int(hi),'?'))); continue
            print('   %5.2f-%5.2f  %-28s %5.2f->%5.2f%s'%(x['t0'],x['tend'],x['n'],x['ct0'],x['ctend'],(' RESTART x%d'%x['restart']) if x['restart'] else ''))
