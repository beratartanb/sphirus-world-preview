# an_vidtab.py <suffix> [labels...]: markdown rows for the video section from the video telemetry JSONs
# (Saved/Codex/Grip_20261106/rec/<label>_<suffix>.json): duration, real-time check (game step mean / max), frame count,
# head normalized X per input segment (min-mean-max) and time outside the 0.28-0.43 band after the 0.4 s start transient.
import json, math, os, sys
suf = sys.argv[1]; labels = sys.argv[2:] or ['PH_phys', 'CL_strafe', 'A_loco', 'B_turns', 'H_hall', 'D_chop', 'I_idle']
root = 'Saved/Codex/Grip_20261106/rec/'
print('| Video | Süre / kare | Gerçek zaman (oyun adımı ort / maks) | Baş X segmentlere göre (min–ort–maks; bant dışı s) |')
print('|---|---|---|---|')
for lb in labels:
    fn = root + '%s_%s.json' % (lb, suf)
    if not os.path.exists(fn): print('| `videos/%s_%s.mp4` | KAYIT YOK | | |' % (lb, suf)); continue
    d = json.load(open(fn)); R = d['rows']; plan = d['plan']
    g = [float(r['gdt']) for r in R]; T = sum(g)
    segs = []
    for s in sorted(set(int(r['s']) for r in R)):
        rows = [r for r in R if int(r['s']) == s]; t = 0.0; hx = []; out = 0.0; ok = True
        for r in rows:
            sc = r.get('scr')
            if not isinstance(sc, dict): ok = False; break
            h = sc['head'][0]; hx.append(h)
            if t > 0.4 and not (0.28 <= h <= 0.43): out += float(r['gdt'])
            t += float(r['gdt'])
        key = (plan[s][0] or 'bırak').replace('LeftShift', 'Shift').replace('LeftMouseButton', 'LMB')
        if not ok or not hx: segs.append('%s: ölçüm yok' % key); continue
        segs.append('%s %.2f–%.2f–%.2f%s' % (key, min(hx), sum(hx) / len(hx), max(hx), (' (dışarıda %.1f s)' % out) if out > 0.05 else ''))
    print('| `videos/%s_%s.mp4` | %.1f s / %d | %.4f / %.4f | %s |' % (lb, suf, T, len(R), sum(g) / len(g), max(g), '; '.join(segs)))
