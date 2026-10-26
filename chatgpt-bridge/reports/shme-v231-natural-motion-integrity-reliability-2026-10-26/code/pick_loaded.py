import json, sys
d = json.load(open(sys.argv[1])); good = []
for n, v in d['clips'].items():
    if v.get('err'): continue
    if v.get('planted_drift', 99) < 3.0 and v.get('foot_err', 99) < 7.5 and v.get('penetration', -9) > -1.5: good.append(n)
json.dump(good, open(sys.argv[2], 'w')); print('GOOD', len(good), sorted(int(x.rsplit('P', 1)[1]) for x in good))
