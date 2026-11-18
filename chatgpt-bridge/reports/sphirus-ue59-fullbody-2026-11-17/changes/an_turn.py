# an_turn.py <label> [t0 t1]: planted-foot rotation on driver (src, UEFN) vs visible (vis, MetaHuman) from turnrec JSON.
# Contact: ball within 2.5 cm of the segment-local floor (min ball z over 1 s window) and ball horizontal speed < 20 cm/s, >= 0.12 s.
# Per contact: foot yaw change (heel->ball heading), ball drift, actor yaw change during the contact.
import json, sys, math
lab = sys.argv[1]; T0 = float(sys.argv[2]) if len(sys.argv) > 2 else 0; T1 = float(sys.argv[3]) if len(sys.argv) > 3 else 1e9
d = json.load(open(r'C:/Users/berat/Documents/Unreal Projects/sphirus_UE59/Saved/UE59Work/rec/' + lab + '.json')); R = [r for r in d['rows'] if T0 <= r[0] <= T1]
print('==', lab, 'abp', d.get('abp'), 'rows', len(R))
def col(m, b, k):  # m 0 src 1 vis ; b index 0 foot_l 1 ball_l 2 foot_r 3 ball_r 4 root ; k 0..3
    return 2 + m*20 + b*4 + k
def wrap(a): return (a + 180) % 360 - 180
res = {}
for m, mn in ((0, 'src'), (1, 'vis')):
    for s, (fb, bb) in (('L', (0, 1)), ('R', (2, 3))):
        z = [r[col(m, bb, 2)] for r in R]; n = len(R); down = []
        for i in range(n):
            lo = min(z[max(0, i-15):min(n, i+16)])
            sp = 0
            if i > 0:
                dt = max(1e-3, R[i][0]-R[i-1][0]); sp = math.hypot(R[i][col(m, bb, 0)]-R[i-1][col(m, bb, 0)], R[i][col(m, bb, 1)]-R[i-1][col(m, bb, 1)])/dt
            down.append(z[i]-lo < 2.5 and sp < 20)
        i = 0; out = []
        while i < n:
            if down[i]:
                j = i
                while j+1 < n and down[j+1]: j += 1
                if R[j][0]-R[i][0] >= 0.12:
                    h = lambda r: math.degrees(math.atan2(r[col(m, bb, 1)]-r[col(m, fb, 1)], r[col(m, bb, 0)]-r[col(m, fb, 0)]))
                    yawc = max(abs(wrap(h(R[k])-h(R[i]))) for k in range(i, j+1))
                    drift = math.hypot(R[j][col(m, bb, 0)]-R[i][col(m, bb, 0)], R[j][col(m, bb, 1)]-R[i][col(m, bb, 1)])
                    ay = wrap(R[j][1]-R[i][1]); spd = math.hypot(R[i][-2], R[i][-1])
                    tw = 0.0
                    if len(R[i]) >= 56:
                        tb = 42 if s == 'L' else 48
                        def kneehead(r):
                            th = r[tb:tb+3]; ca = r[tb+3:tb+6]; an = (r[col(1, fb, 0)], r[col(1, fb, 1)])
                            mx, my = (th[0]+an[0])/2, (th[1]+an[1])/2; return math.degrees(math.atan2(ca[1]-my, ca[0]-mx))
                        def foothead(r): return math.degrees(math.atan2(r[col(1, bb, 1)]-r[col(1, fb, 1)], r[col(1, bb, 0)]-r[col(1, fb, 0)]))
                        tw = max(abs(wrap(kneehead(R[k])-foothead(R[k]))) for k in range(i, j+1))
                    out.append((round(R[i][0], 2), round(R[j][0]-R[i][0], 2), round(yawc, 1), round(drift, 1), round(ay, 1), round(spd), round(tw, 1)))
                i = j+1
            else: i += 1
        res[mn+s] = out
        turning = [o for o in out if abs(o[4]) > 5]
        yv = sorted(o[2] for o in turning)
        print(mn, s, 'contacts', len(out), 'turning', len(turning), 'footyaw med/max', (yv[len(yv)//2] if yv else '-'), (yv[-1] if yv else '-'), 'drift max', max([o[3] for o in turning] or [0]), 'knee-foot twist max', max([o[6] for o in turning] or [0]), 'straight twist max', max([o[6] for o in out if abs(o[4]) <= 5] or [0]))
        for o in turning[:14]: print('   t %5.2f dur %.2f footyaw %5.1f drift %4.1f actoryaw %6.1f v %d twist %4.1f' % o)
