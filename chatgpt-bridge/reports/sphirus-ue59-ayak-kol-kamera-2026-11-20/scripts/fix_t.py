# fix_t.py <label...>: copy a pre-patch-#8 recording to <label>_simt with t = simulated time (running sum of gdt) and
#   tf = the old frame label. Lets every analyser re-measure old runs on simulated time. Originals stay untouched.
import json, sys
RD = 'Saved/Codex/Grip_20261106/rec/'
for L in sys.argv[1:]:
    d = json.load(open(RD + L + '.json')); R = d['rows']
    if 'tw' in R[0]: print(L, 'already sim time'); continue
    T = 0.0
    for i, r in enumerate(R):
        if i: T += r['gdt']
        r['tf'] = r['t']; r['t'] = round(T, 4)
    d['label'] = L + '_simt'; d['note'] = 't rebuilt from sum(gdt) by fix_t.py; tf = old frame label'
    json.dump(d, open(RD + L + '_simt.json', 'w')); print(L, 'rows', len(R), 'old t', R[-1]['tf'], 'sim', R[-1]['t'])
