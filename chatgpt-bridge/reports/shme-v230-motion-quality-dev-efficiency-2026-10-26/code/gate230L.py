import json,sys
l=[x for x in open(sys.argv[1],encoding='utf8',errors='replace') if 'G230L {' in x][0]; d=json.loads(l[l.index('{'):]); c=d['clips']
err=[k for k,v in c.items() if v.get('err')]; fe=sum(1 for v in c.values() if (v.get('foot_err') or 0)>3); dr=sum(1 for v in c.values() if (v.get('planted_drift') or 0)>3); mx=max(v.get('planted_drift') or 0 for v in c.values())
print('GATE230L clips %d err %d foot>3 %d drift>3 %d maxdrift %.1f' % (len(c), len(err), fe, dr, mx)); sys.exit(0 if (not err and fe <= 14 and dr == 0) else 1)
