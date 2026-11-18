# an_bio2.py (2026-11-18, fixed copy of Bio_20261115/an_bio.py) <label> [seg,seg ...]: whole-body gait biomechanics of the VISIBLE body from a recorder JSON (ub / ub2 rows).
# Travel frame per frame = capsule velocity direction (falls back to actor yaw). All cm / deg / s.
#  contact   a ball is "down" when its height is within DZ of the segment's floor and its world speed < VS
#  cadence   steps / min from landings; step length = along-travel distance between successive opposite landings (world);
#            step width = lateral distance between successive opposite landings; duty = stance share; flight = no foot down share
#  slide     world speed of a ball while down (mean / p90) and total drift per stance (cm)
#  pelvis    bob (z range per step), lateral shift toward the stance foot (cm, + = toward), yaw range, list (roll) range
#  counter   chest (spine_05) yaw minus pelvis yaw range; corr(pelvis yaw, chest-minus-pelvis yaw)
#  arms      hand fore-aft swing range; corr(hand_l fwd, foot_r fwd) (+1 = contralateral coupling)
#  knee      support knee angle at mid stance and at landing (thigh-calf-foot), trunk pitch (pelvis->spine_05 from vertical)
import sys, json, math, statistics as st
# 2026-11-18 fixes:
#  contact  height of the ball / ankle above the ground traced under that foot (row['gnd'], vidm_patch) minus the standing bone
#           offset, and |vertical speed| < VZ. No horizontal-speed gate, so a fast-sliding planted foot stays a contact and its
#           speed is reported (slide, p90, share of contact time above 60 cm/s). Old recordings without 'gnd': segment floor.
#  cadence  N/A when the segment is stationary (< 30 cm/s), has < 3 landings or < 0.5 s between first and last landing
#           (the old 60000 /min came from two landings on the same frame divided by 1e-3 s).
#  angles   yaw / chest ranges unwrapped around their circular mean (backward travel gave 359.6 / 710.4 deg).
VZ = 40.0
def cmean(a):
    if not a: return 0.0
    return math.degrees(math.atan2(sum(math.sin(math.radians(x)) for x in a), sum(math.cos(math.radians(x)) for x in a)))
def unwrap(a):
    m = cmean(a); return [m + nang(x - m) for x in a]
RD = 'Saved/Codex/Grip_20261106/rec/'
DZ, VS = 4.0, 60.0
def nang(a): return (a + 180) % 360 - 180
def corr(a, b):
    if len(a) < 4: return 0.0
    ma, mb = st.mean(a), st.mean(b); sa = math.sqrt(sum((x-ma)**2 for x in a)); sb = math.sqrt(sum((x-mb)**2 for x in b))
    return sum((x-ma)*(y-mb) for x, y in zip(a, b)) / (sa*sb) if sa > 1e-6 and sb > 1e-6 else 0.0
def ang3(a, b, c):
    v1 = [a[i]-b[i] for i in range(3)]; v2 = [c[i]-b[i] for i in range(3)]
    n1 = math.sqrt(sum(x*x for x in v1)); n2 = math.sqrt(sum(x*x for x in v2))
    return math.degrees(math.acos(max(-1, min(1, sum(x*y for x, y in zip(v1, v2))/(n1*n2+1e-9)))))
def analyse(lab, segs=None, quiet=False, loops=True):
    d = json.load(open(RD + lab + '.json')); rows = [r for r in d['rows'] if 'ub' in r]
    out = {}
    for s in sorted(set(r['s'] for r in rows)):
        if segs and s not in segs: continue
        R = [r for r in rows if r['s'] == s]
        L = [r for r in R if 'Loop' in str(r.get('gasp', [''])[0])]
        if loops and len(L) >= 40: R = L[len(L)//6:]
        if len(R) < 20: continue
        dt = (R[-1]['t'] - R[0]['t']) / (len(R) - 1); sp = [math.hypot(r['vx'], r['vy']) for r in R]
        def frame(r):
            v = math.hypot(r['vx'], r['vy'])
            if v > 30: return (r['vx']/v, r['vy']/v)
            y = math.radians(r['yaw']); return (math.cos(y), math.sin(y))
        F = [frame(r) for r in R]
        P = lambda r, b: (r['ub'][b] if b in r['ub'] else r['ub2'][b])
        def fwd(i, p, o): return (p[0]-o[0])*F[i][0] + (p[1]-o[1])*F[i][1]
        def lat(i, p, o): return -(p[0]-o[0])*F[i][1] + (p[1]-o[1])*F[i][0]
        bl = [P(r, 'ball_l') for r in R]; br = [P(r, 'ball_r') for r in R]; pel = [P(r, 'pelvis') for r in R]; ch = [P(r, 'spine_05') for r in R]
        floor = min(min(b[2] for b in bl), min(b[2] for b in br))
        al = [r['v_foot_l'] for r in R]; ar = [r['v_foot_r'] for r in R]; afloor = min(min(b[2] for b in al), min(b[2] for b in ar))
        G = all(isinstance(r.get('gnd'), dict) for r in R)
        def gz(i, k, B):
            g = R[i]['gnd']['f'][k] if G else None
            return g[0] if g else None
        OFF = getattr(sys.modules[__name__], 'OFFS', None) or (3.0, 3.0, 8.0, 8.0)
        def down(B, A, kb, ka):
            o = []
            for i in range(len(B)):
                j = max(1, i); vz = abs(B[j][2] - B[j-1][2]) / dt; vza = abs(A[j][2] - A[j-1][2]) / dt
                if G:
                    gb = gz(i, kb, B); ga = gz(i, ka, A)
                    hb = (B[i][2] - gb - OFF[kb]) if gb is not None else 99; ha = (A[i][2] - ga - OFF[ka]) if ga is not None else 99
                else:
                    hb = B[i][2] - floor; ha = A[i][2] - afloor - 0.0
                o.append((hb < DZ and vz < VZ) or (ha < 3.0 and vza < VZ))
            return o
        dl, dr = down(bl, al, 0, 2), down(br, ar, 1, 3)
        def stances(D):
            o = []; i = 0
            while i < len(D):
                if D[i]:
                    j = i
                    while j + 1 < len(D) and D[j+1]: j += 1
                    if (j - i) * dt >= 0.05: o.append((i, j))
                    i = j + 1
                else: i += 1
            return o
        SL, SR = stances(dl), stances(dr)
        land = sorted([(a, 'L', b) for a, b in SL] + [(a, 'R', b) for a, b in SR])
        steps = []; widths = []
        for k in range(1, len(land)):
            (i0, s0, e0), (i1, s1, e1) = land[k-1], land[k]
            if s0 == s1: continue
            B0 = (bl if s0 == 'L' else br)[i0]; B1 = (bl if s1 == 'L' else br)[i1]
            steps.append(fwd(i1, B1, B0)); widths.append(abs(lat(i1, B1, B0)))
        T = R[-1]['t'] - R[0]['t']; span = (land[-1][0] - land[0][0]) * dt if len(land) > 1 else 0
        cad = 60.0 * (len(land) - 1) / span if (len(land) >= 3 and span >= 0.5 and st.mean(sp) >= 30) else None
        duty = (sum(dl) + sum(dr)) / (2.0 * len(R)); flight = sum(1 for a, b in zip(dl, dr) if not a and not b) / len(R); dbl = sum(1 for a, b in zip(dl, dr) if a and b) / len(R)
        sl = []; drift = []
        for S, B in ((SL, bl), (SR, br)):
            for a, b in S:
                v = [math.dist(B[i][:2], B[i-1][:2]) / dt for i in range(a+1, b+1)]; sl += v; drift.append(math.dist(B[a][:2], B[b][:2]))
        fast = (sum(1 for x in sl if x > 60) / len(sl)) if sl else 0
        # pelvis toward stance foot: lateral offset of the pelvis from the capsule line, signed toward the single-support foot
        tow = []
        for i in range(len(R)):
            if dl[i] != dr[i]:
                side = bl[i] if dl[i] else br[i]; cap = (R[i]['x'], R[i]['y'], 0)
                ls = lat(i, side, cap); lp = lat(i, pel[i], cap)
                tow.append(lp * (1 if ls > 0 else -1))
        def lineyaw(i, a, b):
            A = P(R[i], a); B = P(R[i], b); return math.degrees(math.atan2(fwd(i, B, A), lat(i, B, A)))   # + = right side forward
        pyaw = [lineyaw(i, 'thigh_l', 'thigh_r') for i in range(len(R))]; cyaw0 = [lineyaw(i, 'upperarm_l', 'upperarm_r') for i in range(len(R))]
        pyaw = unwrap(pyaw); cyaw0 = unwrap(cyaw0); cyaw = unwrap([a - b for a, b in zip(cyaw0, pyaw)])
        proll = [math.degrees(math.atan2(P(R[i], 'thigh_r')[2] - P(R[i], 'thigh_l')[2], math.dist(P(R[i], 'thigh_r')[:2], P(R[i], 'thigh_l')[:2]))) for i in range(len(R))]; pz = [pel[i][2] for i in range(len(R))]
        hl = [fwd(i, R[i]['v_hand_l'], pel[i]) for i in range(len(R))]; hr = [fwd(i, R[i]['v_hand_r'], pel[i]) for i in range(len(R))]
        fl = [fwd(i, bl[i], pel[i]) for i in range(len(R))]; fr = [fwd(i, br[i], pel[i]) for i in range(len(R))]
        tp = [math.degrees(math.atan2(fwd(i, ch[i], pel[i]), ch[i][2] - pel[i][2])) for i in range(len(R))]
        knee_mid = []; knee_land = []
        for S, sd in ((SL, 'l'), (SR, 'r')):
            for a, b in S:
                for idx, acc in (((a+b)//2, knee_mid), (a, knee_land)):
                    r = R[idx]
                    try: acc.append(ang3(P(r, 'thigh_'+sd)[:3], P(r, 'calf_'+sd)[:3], r['v_foot_'+sd]))
                    except Exception: pass
        rng = lambda a: (max(a) - min(a)) if a else 0; mean = lambda a: st.mean(a) if a else 0
        p90 = lambda a: sorted(a)[int(0.9*(len(a)-1))] if a else 0
        o = dict(t0=R[0]['t'], t1=R[-1]['t'], spd=mean(sp), n_land=len(land), cad=cad, step=mean(steps), step_sd=(st.pstdev(steps) if len(steps) > 1 else 0), width=mean(widths),
                 fast=fast, gnd=G, duty=duty, flight=flight, dbl=dbl, slide=mean(sl), slide90=p90(sl), drift=mean(drift), pel_bob=rng(pz), pel_tow=mean(tow), pel_yaw=rng(pyaw), pel_roll=rng(proll),
                 counter=rng(cyaw), counter_corr=corr(pyaw, cyaw0), chest_yaw=rng(cyaw0), swingL=rng(hl), swingR=rng(hr), arm_leg=corr(hl, fr), arm_leg2=corr(hr, fl), trunk=mean(tp), trunk_rng=rng(tp),
                 knee_mid=mean(knee_mid), knee_land=mean(knee_land), clip=str(R[len(R)//2].get('gasp', [''])[0])[:34])
        out[s] = o
        if not quiet:
            o2 = dict(o); o2['cad'] = o['cad'] if o['cad'] is not None else -1
            print(' s%-2d %5.1f-%5.1f v%4.0f %-34s| cad %3.0f step %5.1f+-%4.1f w %4.1f duty %.2f dbl %.2f fl %.2f | slide %4.1f p90 %4.1f >60 %3.0f%% drift %4.1f | pel bob %4.1f tow %+4.1f yaw %4.1f roll %4.1f | chest %4.1f rel %4.1f c %+.2f | arm %4.1f/%4.1f al %+.2f %+.2f | trunk %+5.1f r%4.1f | knee mid %3.0f land %3.0f%s' % (
                s, o['t0'], o['t1'], o['spd'], o['clip'], o2['cad'], o['step'], o['step_sd'], o['width'], o['duty'], o['dbl'], o['flight'], o['slide'], o['slide90'], 100*o['fast'], o['drift'], o['pel_bob'], o['pel_tow'], o['pel_yaw'], o['pel_roll'],
                o['chest_yaw'], o['counter'], o['counter_corr'], o['swingL'], o['swingR'], o['arm_leg'], o['arm_leg2'], o['trunk'], o['trunk_rng'], o['knee_mid'], o['knee_land'], ('' if o['cad'] is not None else '  [cad N/A: stationary or <3 landings]') + ('' if G else '  [no ground traces: old floor rule]')))
    return out
if __name__ == '__main__':
    a = sys.argv[1:]; i = 0
    while i < len(a):
        segs = None
        if i + 1 < len(a) and a[i+1][0].isdigit(): segs = [int(v) for v in a[i+1].split(',')]
        print('==', a[i]); analyse(a[i], segs); i += 2 if segs else 1
