import json,sys
for l in sys.argv[1:]:
    R=json.load(open('Saved/Codex/Grip_20261106/rec/%s.json'%l)); R=R['rows'] if isinstance(R,dict) else R
    prev=None; out=[]
    for r in R:
        h=r.get('hook') or {}; k=(r.get('tgt'), str({a:b for a,b in (h.get('doors') or {}).items() if 'Lower' in a}))
        if k!=prev: out.append('t %.1f s%d tgt %s doors %s'%(r['t'],r['s'],k[0],k[1])); prev=k
    print(l); [print('  '+x[:170]) for x in out[:10]]
    if R and R[0].get('hook'): print('  hook keys',list(R[0]['hook'].keys())[:10])
