import json, sys
R = json.load(open('Saved/Codex/Grip_20261106/rec/%s.json' % sys.argv[1]))['rows']; P = json.loads(sys.argv[2])
for k, (t0, bone) in enumerate(P):
    S = [r['hook'] for r in R if 'pv' in r.get('hook', {}) and t0 - 0.05 <= r['hook'].get('tt', -1) <= t0 + 0.9]
    b0 = S[0]['pv']; mx = {}
    for h in S:
        for bn in ('spine_03', 'spine_05', 'head', 'clavicle_l', 'clavicle_r', 'hand_l', 'hand_r', 'pelvis'):
            d = [h['pv'][bn][i] - b0[bn][i] for i in range(3)]; m = sum(x * x for x in d) ** 0.5
            if m > mx.get(bn, (0,))[0]: mx[bn] = (round(m, 1), round(h['tt'] - t0, 2), [round(x, 1) for x in d])
    print('hit', k + 1, bone, ' '.join('%s %s@%s %s' % (b, v[0], v[1], v[2]) for b, v in mx.items()))
