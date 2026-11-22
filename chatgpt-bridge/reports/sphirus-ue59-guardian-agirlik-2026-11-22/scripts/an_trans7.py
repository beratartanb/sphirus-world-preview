# an_trans7.py <label> <plan>: gait transitions. Per plan step: speed before -> target, time to cover 90 % of the change, peak
# acceleration (cm/s2), clips visited (with seconds), time the capsule moved > 35 % faster than the playing clip's movedata_speed
# (= "walk cycle while the capsule is still fast" or the reverse), largest 0.2 s change of world head height (bump) and of pelvis height.
import json, sys, math, ast
lab = sys.argv[1]; plan = ast.literal_eval(open(sys.argv[2]).read())
R = [r for r in json.load(open('Saved/Codex/Grip_20261106/rec/' + lab + '.json'))['rows'] if isinstance(r.get('hook'), dict) and r['hook'].get('cv')]
def sp(r): return math.hypot(r['vx'], r['vy'])
seg = {}
for r in R: seg.setdefault(r['s'], []).append(r)
print('#### %s' % lab)
for s in sorted(seg):
    S = seg[s]
    if len(S) < 10 or s == 0: continue
    v0 = sp(S[0]); v1 = sum(sp(r) for r in S[-12:]) / 12; dv = v1 - v0
    t90 = next((r['t'] - S[0]['t'] for r in S if abs(sp(r) - v0) >= 0.9 * abs(dv)), None) if abs(dv) > 20 else 0
    acc = max((abs(sp(S[i]) - sp(S[i - 1])) / max(S[i]['gdt'], 1e-3) for i in range(1, len(S))), default=0)
    clips = []; mm = 0.0
    for i, r in enumerate(S):
        c = str(r['gasp'][0]).replace('M_Neutral_', 'N_').replace('M_Relaxed_', 'R_').replace('Transition_', 'Tr_')
        if not clips or clips[-1][0] != c: clips.append([c, 0.0])
        clips[-1][1] += r['gdt']
        md = r['hook']['cv'][2]
        if sp(r) > 60 and md > 20 and sp(r) > 1.35 * md: mm += r['gdt']
    def bump(key):
        b = 0
        for i in range(len(S)):
            j = i
            while j < len(S) and S[j]['t'] - S[i]['t'] < 0.2: j += 1
            if j < len(S): b = max(b, abs(key(S[j]) - key(S[i])))
        return b
    print('s%-2d [%-14s] v %3.0f -> %3.0f | 90%% in %s s | peak acc %5.0f | capsule faster than clip %.2f s | head dz/0.2s %4.1f pelvis %4.1f | %s' % (
        s, plan[s][0].replace('LeftShift', 'Sh').replace('LeftControl', 'Ct') or '-', v0, v1, ('%.2f' % t90) if t90 is not None else '-', acc, mm,
        bump(lambda r: r['v_head'][2]), bump(lambda r: r['ub']['pelvis'][2]), ' > '.join('%s %.2f' % (c[0][-24:], c[1]) for c in clips[:5])))
