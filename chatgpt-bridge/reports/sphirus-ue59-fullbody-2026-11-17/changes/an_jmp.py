# an_jmp.py <label>: jumps in a vc55 recording: capsule apex, air time, visible-pelvis dip after landing (vs capsule), speed kept, clips.
import sys, json, math
d = json.load(open('Saved/Codex/Grip_20261106/rec/%s.json' % sys.argv[1])); R = d['rows']; z0 = R[0]['z']
i = 0; n = len(R)
while i < n:
    if R[i]['z'] - z0 > 3:
        j = i
        while j < n and R[j]['z'] - z0 > 1: j += 1
        air = R[min(j, n-1)]['t'] - R[i]['t']; apex = max(r['z'] for r in R[i:j]) - z0
        pre = R[max(0, i-3)]; sp0 = math.hypot(pre['vx'], pre['vy'])
        post = [r for r in R[j:] if r['t'] - R[min(j, n-1)]['t'] < 1.2]
        rel = [r['v_pelvis'][2] - r['z'] for r in post if r.get('v_pelvis')]
        stand = [r['v_pelvis'][2] - r['z'] for r in R[max(0, i-20):max(1, i-3)] if r.get('v_pelvis')]
        dip = (sum(stand)/len(stand) - min(rel)) if rel and stand else float('nan')
        tdip = post[rel.index(min(rel))]['t'] - post[0]['t'] if rel else 0
        spmin = min(math.hypot(r['vx'], r['vy']) for r in post) if post else 0
        sp03 = [math.hypot(r['vx'], r['vy']) for r in post if r['t'] - post[0]['t'] >= 0.3][:1]
        clips = []
        for r in R[max(0, i-2):j+25]:
            g = r.get('gasp') or ['']; c = str(g[0])
            if c and (not clips or clips[-1] != c): clips.append(c)
        monts = sorted(set(str(r.get('mont')) for r in R[i:j+25]))
        print('JUMP t=%.2f seg %s | v0 %3.0f apex %4.1f cm air %.2f s | land dip %4.1f cm at +%.2f s | speed min %3.0f, at +0.3s %s | mont %s' % (R[i]['t'], R[i]['s'], sp0, apex, air, dip, tdip, spmin, ['%.0f' % x for x in sp03], monts))
        print('     clips:', ' > '.join(clips))
        i = j + 20
    else: i += 1
