# an_rev7.py <label> <plan>: reversals and turning starts. Per step: heading change requested, time until the velocity points into the new
# direction (> 0 along it), time spent playing a BACKWARD or opposite-direction LOOP clip while the capsule still moves the old way (> 50 cm/s
# along the old direction) = "back walk while still going forward", peak deceleration, head drop (max head height decrease in the first
# 1.2 s) and trunk pitch peak (pelvis->neck against vertical), clip sequence.
import json, sys, math, ast
lab = sys.argv[1]; plan = ast.literal_eval(open(sys.argv[2]).read())
R = [r for r in json.load(open('Saved/Codex/Grip_20261106/rec/' + lab + '.json'))['rows'] if isinstance(r.get('hook'), dict) and r['hook'].get('cv')]
seg = {}
for r in R: seg.setdefault(r['s'], []).append(r)
print('#### %s' % lab)
for s in sorted(seg):
    S = seg[s]
    if s == 0 or len(S) < 8: continue
    v0 = (S[0]['vx'], S[0]['vy']); sp0 = math.hypot(*v0); u0 = (v0[0] / sp0, v0[1] / sp0) if sp0 > 30 else None
    t_new = None; bad = 0.0; dec = 0.0; prev = sp0
    for r in S:
        sp = math.hypot(r['vx'], r['vy'])
        if u0 is not None:
            along = r['vx'] * u0[0] + r['vy'] * u0[1]
            if t_new is None and along < 0: t_new = r['t'] - S[0]['t']
            c = str(r['gasp'][0])
            if along > 50 and (('_B' in c and 'Loop' in c) or 'Loop_B' in c or 'Bwd' in c and 'Pivot' not in c): bad += r['gdt']
        dec = max(dec, (prev - sp) / max(r['gdt'], 1e-3)); prev = sp
    W = [r for r in S if r['t'] - S[0]['t'] <= 1.2]; h0 = W[0]['v_head'][2]
    pit = []
    for r in W:
        p = r['ub']['pelvis']; n = r['ub']['neck_01']; pit.append(math.degrees(math.atan2(math.hypot(n[0] - p[0], n[1] - p[1]), n[2] - p[2])))
    clips = []
    for r in S:
        c = str(r['gasp'][0]).replace('M_Neutral_', 'N_').replace('M_Relaxed_', 'R_').replace('Transition_', 'Tr_')
        if not clips or clips[-1][0] != c: clips.append([c, 0.0])
        clips[-1][1] += r['gdt']
    print('s%-2d [%-12s] v0 %3.0f | new direction after %s s | back-loop while still going forward %.2f s | peak decel %5.0f | head drop %4.1f cm | trunk tilt max %4.1f | %s' % (
        s, plan[s][0].replace('LeftShift', 'Sh').replace('LeftControl', 'Ct') or '-', sp0, ('%.2f' % t_new) if t_new is not None else '-', bad, dec, h0 - min(r['v_head'][2] for r in W), max(pit),
        ' > '.join('%s %.2f' % (c[0][-22:], c[1]) for c in clips[:5])))
