# an_fat5.py <label>: fatigue course. Every 2 s: speed, effort E, fatigue Fat (0..1), controller effort PS_Eff, trunk lean (pelvis->spine_05
# vs vertical in the travel / facing plane, deg), shoulder height above spine_05 (cm, mean L/R), head pitch offset PS_CH, breathing
# amplitude proxy = peak-to-peak clavicle height over the window (cm). Shows the gradual build-up and the recovery.
import json, sys, math
lab = sys.argv[1]; D = json.load(open('Saved/Codex/Grip_20261106/rec/' + lab + '.json')); R = D['rows'] if isinstance(D, dict) else D
R = [r for r in R if isinstance(r.get('hook'), dict) and r['hook'].get('pv') and r['hook'].get('eff')]
W = 120
for i in range(0, len(R) - W + 1, W):
    S = R[i:i + W]; r = S[W // 2]; pv = [x['hook']['pv'] for x in S]
    def lean(p):
        a = p['pelvis']; b = p['spine_05']; return math.degrees(math.atan2(b[1] - a[1], b[2] - a[2]))
    sh = [0.5 * (p['clavicle_l'][2] + p['clavicle_r'][2]) - p['spine_05'][2] for p in pv]; ua = [0.5 * (p['upperarm_l'][2] + p['upperarm_r'][2]) - p['spine_05'][2] for p in pv]
    e = r['hook']['eff']; ps = r['hook'].get('ps') or [0] * 23
    print('  t %5.1f s%-2d v %3.0f | E %.2f Fat %.2f PS_Eff %.2f | trunk lean %5.1f deg | shoulder joint above spine_05 %5.1f cm (p2p %.1f) | head PS_CH %5.1f' % (
        r['t'], r['s'], math.hypot(r['vx'], r['vy']), e[0], e[2], ps[17], sum(lean(p) for p in pv) / W, sum(ua) / W, max(ua) - min(ua), ps[3]))
