# an_ev8.py <label>: per contact event (first frame of a non-normal contact state): the REAL foot phase at that frame (driver contact curves,
# 0 = planted / 100 = free -> left support / right support / double support / airborne), the support the system used (CT_Sup), the chosen
# reaction clip id (CT_RClip: 0-2 front, 3/4 stumble R/L foot, 5-7 back) and the horizontal speed 0.1 s before, at the start and the peak
# during the reaction (root motion + movement component together).
import json, sys, math, ast
def D(x): return x if isinstance(x, dict) else ast.literal_eval(x)
lab = sys.argv[1]; R = [r for r in json.load(open('Saved/Codex/Grip_20261106/rec/' + lab + '.json'))['rows'] if isinstance(r.get('hook'), (dict, str))]
ps = 0; ev = None; CL = {0: 'front', 1: 'front-left', 2: 'front-right', 3: 'stumble R foot', 4: 'stumble L foot', 5: 'back', 6: 'back-left', 7: 'back-right'}
R.append(dict(R[-1], hook={'ct': [0], 'cv': [0, 0]}))   # round 8b: sentinel so a reaction still running at the end of the recording is reported
for i, r in enumerate(R):
    h = D(r['hook']); st = h.get('ct', [0])[0] if isinstance(h.get('ct'), list) else 0; v = math.hypot(r['vx'], r['vy'])
    if st != 0 and ps == 0:
        c = h['cv']; ph = 'airborne' if c[0] > 50 and c[1] > 50 else ('double support' if c[0] <= 50 and c[1] <= 50 else ('left support' if c[0] <= 50 else 'right support'))
        pre = [math.hypot(q['vx'], q['vy']) for q in R[max(0, i - 8):i] if r['t'] - q['t'] <= 0.12]; ex = h.get('ex') if isinstance(h.get('ex'), list) else []
        ev = {'t': r['t'], 'ph': ph, 'pre': pre[0] if pre else v, 'v0': v, 'pk': v, 'st': st, 'ex': ex, 'cv': c[:2]}
    if st != 0 and ev: ev['pk'] = max(ev['pk'], v); ev['ex'] = (h.get('ex') if isinstance(h.get('ex'), list) and h['ex'] else ev['ex']) if st == 4 and ev['st'] == 4 and r['t'] - ev['t'] < 0.1 else ev['ex']
    if st == 0 and ps != 0 and ev:
        ex = ev['ex']; clip = CL.get(int(ex[0]), ex[0]) if (ex and ev['st'] == 4) else '-'
        print('  %s event t %.2f state %d | real phase %s (contact L %.0f R %.0f) | system support %s | clip %s | speed 0.1 s before %.0f, at start %.0f, peak during %.0f' % (lab, ev['t'], ev['st'], ev['ph'], ev['cv'][0], ev['cv'][1], {0: 'none', 1: 'left', 2: 'right'}.get(int(ex[2]), ex[2]) if len(ex) > 2 else '?', clip, ev['pre'], ev['v0'], ev['pk'])); ev = None
    ps = st
