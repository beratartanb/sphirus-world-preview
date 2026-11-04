"""poptab255.py <prefixA:variantA> <prefixB:variantB> [scenario ...] : pop table per scenario from pop_report.py. peak (m/s2) scales with frame rate and shows slow large accelerations; exc_cm is the displacement a smooth motion would not have made, the FPS-robust read.
Prints count > 25 m/s2, worst peak, worst exc_cm and events with exc_cm > 1.5 for both builds, and the entry time of the worst exc event."""
import subprocess, sys, re
PY = sys.executable
def rep(L):
    o = subprocess.run([PY, 'Tools/SHME_V21_20261014/pop_report.py', L], capture_output=True, text=True, encoding='utf8', errors='replace').stdout
    h = re.search(r'pops >25 m/s2: (\d+) \(worst (\d+)\)', o)
    if not h: return None
    ev = []
    for l in o.split('\n'):
        m = re.match(r'\s+([\d.]+)\s+(\d+)\s+(\S+)\s+([\d.]+)\s+(\d+)\s+(\S+)\s+([\d.]+)\s+([\d.]+) \|', l)
        if m: ev.append((float(m[7]), float(m[1]), m[3], float(m[4]), int(m[5]), m[6], int(m[2])))
    return int(h[1]), int(h[2]), ev
PA, VA = sys.argv[1].split(':'); PB, VB = sys.argv[2].split(':')
SC = sys.argv[3:] or 's54_revR s54_revL s54_r135 s54_r90 s54_l90 j54_rev j54_r135 j54_r90 j38_c90l w54_rev s54_tap s54_mid s54_lr fz_sprint_a fz_sprint_m fz_jog_a fz_jog_m fz_walk_a fz_walk_m wstart w42_id taps jstart j36_stop j45_sl2 gait w43_idle j40_rlw'.split()
print('| senaryo | sayı A→B | en yüksek m/s² A→B | en yüksek exc cm A→B | exc>1.5 A→B | B en kötü exc nerede |'); print('|---|---|---|---|---|---|')
for s in SC:
    a = rep('%s_%s_%s_r1' % (PA, s, VA)); b = rep('%s_%s_%s_r1' % (PB, s, VB))
    if not a or not b: print('| %s | yok |' % s); continue
    ea = max([e[0] for e in a[2]] or [0]); eb = max([e[0] for e in b[2]] or [0]); w = max(b[2]) if b[2] else None
    print('| %s | %d→%d | %d→%d | %.2f→%.2f | %d→%d | %s |' % (s, a[0], b[0], a[1], b[1], ea, eb, sum(e[0] > 1.5 for e in a[2]), sum(e[0] > 1.5 for e in b[2]), ('t %.2f %s +%.2f v%d %s' % (w[1], w[2][-16:], w[3], w[4], w[5])) if w else ''))
