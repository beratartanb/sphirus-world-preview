"""redir254.py <label> [--v] [--step 0.05] : V2.54 per direction-change event (input/desired-velocity direction turns > 60 deg while moving
> 100 cm/s) - what the capsule, the body and the systems do, on the SAME frames.
Event = first frame the component DesiredVelocity direction differs > 60 deg from the actual velocity direction at speed > 100.
Timeline (every --step s for 2.2 s): speed, travel heading vs the old travel (deg), actor yaw vs the old travel, visible-body facing
(pelvis->chest horizontal is unreliable; uses the mesh yaw 'vwy') minus travel = backward travel when |.| > 120, trunk lean (deg, chest
over pelvis along the facing; + = forward), selected clip / time / database, family, redirect class, backpedal flag, contacts.
Summary: decel peak (g), min speed, time travel reaches 80 % of the turn, time the body faces within 30 deg of the new travel, time spent
travelling backwards (|facing-travel| > 120 deg) and the trunk lean during it, trunk lean change in the first 0.3 s (spine straightening),
clips / databases in the first 1.5 s."""
import sys, math
L = sys.argv[1]; VERB = '--v' in sys.argv; STEP = float(sys.argv[sys.argv.index('--step') + 1]) if '--step' in sys.argv else 0.05
def vec(s):
    p = dict(kv.split('=') for kv in s.split()); return float(p['X']), float(p['Y']), float(p['Z'])
def ang(a): return (a + 180.0) % 360.0 - 180.0
rows = []
for line in open('Saved/Codex/SHME_V1_20260925/LTP/%s.ltp' % L, encoding='utf8', errors='ignore'):
    d = {}
    for kv in line.rstrip('\n').split('|')[2:]:
        if '=' in kv: k, v = kv.split('=', 1); d.setdefault(k, v)
    try:
        t = float(d['t']); P = {k: vec(d[k]) for k in ('ax', 'vb_pelvis', 'vb_chest', 'vb_head', 'vb_ball_l', 'vb_ball_r')}
        dv = vec(d['cv_DesiredVelocity']) if 'cv_DesiredVelocity' in d else (0.0, 0.0, 0.0)
        rows.append((t, d, P, dv))
    except Exception: pass
# velocity by 3-frame difference
V = []
for i in range(len(rows)):
    a, b = rows[max(0, i - 2)], rows[min(len(rows) - 1, i + 2)]
    dt = max(1e-4, b[0] - a[0]); V.append(((b[2]['ax'][0] - a[2]['ax'][0]) / dt, (b[2]['ax'][1] - a[2]['ax'][1]) / dt))
def hd(v): return math.degrees(math.atan2(v[1], v[0]))
def fl(k):
    z = [r[2][k][2] for r in rows if r[0] < rows[0][0] + 1.0]; return sorted(z)[len(z) // 2]
FB = {s: fl('vb_ball_' + s) for s in 'lr'}
i = 1; ev = 0
while i < len(rows):
    t, d, P, dvel = rows[i]; sp = math.hypot(*V[i]); dsp = math.hypot(dvel[0], dvel[1])
    if sp > 100 and dsp > 50 and abs(ang(hd(dvel) - hd(V[i]))) > 60:
        ev += 1; h0 = hd(V[max(0, i - 3)]); tgt = ang(hd(dvel) - h0)
        seg = [k for k in range(i, len(rows)) if rows[k][0] <= t + 2.2]
        out = []; minsp = 1e9; peaka = 0.0; t80 = None; tface = None; back_t = 0.0; back_lean = []; lean0 = None; lean03 = []
        clips = []; dbs = []
        for n, k in enumerate(seg):
            tk, dk, Pk, _ = rows[k]; v = V[k]; s_ = math.hypot(*v); trav = ang(hd(v) - h0) if s_ > 20 else None
            face = ang(float(dk.get('vwy', 0) or 0) - h0)
            fa = math.radians(float(dk.get('vwy', 0) or 0) + 90.0)   # mesh yaw -> forward (mesh is -90)
            fx, fy = math.cos(fa), math.sin(fa)
            lean = math.degrees(math.atan2((Pk['vb_chest'][0] - Pk['vb_pelvis'][0]) * fx + (Pk['vb_chest'][1] - Pk['vb_pelvis'][1]) * fy, Pk['vb_chest'][2] - Pk['vb_pelvis'][2]))
            if lean0 is None: lean0 = lean
            if tk - t <= 0.3: lean03.append(lean)
            if k > seg[0]:
                k0, k1 = max(0, k - 3), min(len(rows) - 1, k + 3)
                a_ = math.hypot(V[k1][0] - V[k0][0], V[k1][1] - V[k0][1]) / max(1e-4, rows[k1][0] - rows[k0][0]); peaka = max(peaka, a_)
            minsp = min(minsp, s_)
            if t80 is None and trav is not None and abs(ang(trav - tgt)) < 0.2 * abs(tgt) and s_ > 30: t80 = tk - t
            facetrav = ang(face + 90.0 - (trav if trav is not None else face + 90.0)) if trav is not None else 0.0
            if tface is None and trav is not None and s_ > 60 and abs(ang(face + 90.0 - tgt)) < 30: tface = tk - t
            if trav is not None and s_ > 60 and abs(facetrav) > 120: back_t += (tk - rows[k - 1][0]) if k > seg[0] else 0.0; back_lean.append(lean)
            o = dk.get('av_Phase27_SelectedObject', '')[-30:]; db = dk.get('av_CurrentSelectedDatabase', '')[-26:]
            if tk - t <= 1.5:
                if not clips or clips[-1][0] != o: clips.append((o, round(tk - t, 2), dk.get('av_Phase27_SelectedTime', '')[:5]))
                if not dbs or dbs[-1] != db: dbs.append(db)
            if VERB and n % max(1, int(round(STEP / max(1e-4, rows[1][0] - rows[0][0])))) == 0:
                cl = 'L' if Pk['vb_ball_l'][2] < FB['l'] + 2 else '.'; cr = 'R' if Pk['vb_ball_r'][2] < FB['r'] + 2 else '.'
                out.append('  +%.2f v %4.0f trav %+5.0f face %+5.0f f-t %+5.0f lean %+5.1f | %s %s [%s] fam %s cls %s bp %s %s%s' % (
                    tk - t, s_, trav if trav is not None else 0, face + 90.0, facetrav, lean, o, dk.get('av_Phase27_SelectedTime', '')[:5], db,
                    dk.get('cv_Family', '')[:3], dk.get('cv_RedirectClass', '')[:3], dk.get('pv_CR_Backpedal', '')[:1], cl, cr))
        print('REDIR254 %s ev%d t=%.2f v0 %.0f req %+.0f | min v %.0f | peak a %.2f g | travel 80%% +%s | body faces new +%s | backward travel %.2f s lean %s | lean %+.1f -> %+.1f in 0.3 s | clips %s | dbs %s' % (
            L, ev, t, sp, tgt, minsp, peaka / 980.0, '%.2f' % t80 if t80 is not None else '-', '%.2f' % tface if tface is not None else '-', back_t,
            ('%+.1f..%+.1f' % (min(back_lean), max(back_lean))) if back_lean else '-', lean0, min(lean03) if lean03 else 0.0,
            ' > '.join('%s@%s(%s)' % (c[0], c[1], c[2]) for c in clips[:7]), ' > '.join(dbs[:6])))
        for o_ in out: print(o_)
        i = seg[-1] if seg else i + 1
    i += 1
