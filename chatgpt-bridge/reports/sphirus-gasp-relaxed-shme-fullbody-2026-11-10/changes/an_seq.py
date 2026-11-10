# an_seq.py <label...>: speed profile + selected clip/database sequence from vid.py recordings.
import json,math,sys
for L in sys.argv[1:]:
    d=json.load(open('Saved/Codex/Grip_20261106/rec/%s.json'%L)); R=d['rows']; t0=R[0]['t']; S=[math.hypot(r['vx'],r['vy']) for r in R]
    print('==',L,'max',round(max(S)),'mo0',R[0].get('mo'))
    print('  v',' '.join('%d'%S[i] for i in range(0,len(R),6)))
    prev=None
    for i,r in enumerate(R):
        g=r.get('gasp') or [None,None]; c=(g[0],(g[1] or '').replace('PSD_',''),str(r.get('mont'))[:20])
        if c!=prev: print('  %5.2f v%4d  %s'%(r['t']-t0,S[i],c)); prev=c
