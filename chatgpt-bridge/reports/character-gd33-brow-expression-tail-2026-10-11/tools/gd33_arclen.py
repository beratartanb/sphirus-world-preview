import sys, json, numpy as np
for p in sys.argv[sys.argv.index('--')+1:]:
    B = json.load(open(p)); out = []
    for side in ('imgL', 'imgR'):
        C = np.array([0.5*(np.array(s['top'])+np.array(s['bot'])) for s in B[side]]); out.append('%s %.3f cm' % (side, np.linalg.norm(np.diff(C, axis=0), axis=1).sum()))
    print('ARCLEN', p.rsplit('/', 1)[-1], ' | '.join(out))
