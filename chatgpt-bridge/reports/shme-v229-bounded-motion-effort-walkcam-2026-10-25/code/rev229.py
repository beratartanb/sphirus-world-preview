"""rev229.py label [--from=T] [--to=T] [--all]: sprint-reversal frame audit (V2.29). Per frame: input (lix/liy), actor yaw, velocity
vector + speed + its heading, visible-body yaw (vwy) and pelvis heading (pelvis x axis), visible pelvis offset from the capsule (cm,
horizontal), camera -> head distance, camera -> capsule distance, render flags (vvis/vrr), selected clip / time / DB, clip-speed contract.
Flags per frame: MESH (visible pelvis > 35 cm from the capsule), CAM (camera < 35 cm from the head or inside the capsule radius 40),
REND (vrr 0 or vvis 0), VELFLIP (velocity heading vs input heading > 150 deg while speed rises), YAWJ (actor yaw jump > 25 deg/frame),
BODYJ (shoulder-line facing jump > 30 deg/frame). Prints a compact table of the window and a summary line REV229 {...}."""
import json, sys, math, pathlib
E = pathlib.Path(__file__).resolve().parents[2] / 'Saved/Codex/SHME_V1_20260925/Evidence'
def f(x, d=0.0):
    try: return float(x)
    except Exception: return d
def ang(a): return (a + 180.0) % 360.0 - 180.0
args = [a for a in sys.argv[1:] if not a.startswith('--')]; opt = {a.split('=')[0]: (a.split('=') + [''])[1] for a in sys.argv[1:] if a.startswith('--')}
for lab in args:
    p = E / (lab + '.json')
    if not p.exists(): print('REV229 %s MISSING' % lab); continue
    R = sorted([r for r in json.load(open(p)) if isinstance(r, dict) and r.get('t') is not None and isinstance(r.get('ax'), list)], key=lambda r: f(r['t']))
    t0 = f(opt.get('--from'), 0.0); t1 = f(opt.get('--to'), 1e9)
    flags = {}; rows = []; prev = None; prev_ph = None; prev_tw = None; worst = {'mesh': 0, 'camhead': 999, 'yawj': 0, 'pose': 0}
    for r in R:
        t = f(r['t']); ax = r['ax']; vx, vy = f(r.get('avx')), f(r.get('avy')); sp = math.hypot(vx, vy); vh = math.degrees(math.atan2(vy, vx)) if sp > 5 else None
        ay = f(r.get('ay')); li = (f(r.get('lix')), f(r.get('liy'))); ih = math.degrees(math.atan2(li[1], li[0])) if math.hypot(*li) > 0.1 else None
        pel = r.get('vb_pelvis') or ax; md = math.hypot(pel[0] - ax[0], pel[1] - ax[1])
        cam = r.get('camera') or [0, 0, 0]; hd = r.get('vb_head') or ax
        ch = math.dist(cam, hd); cc = math.hypot(cam[0] - ax[0], cam[1] - ax[1])
        sl, sr = r.get('vb_sh_l'), r.get('vb_sh_r'); ph = None   # body facing from the shoulder line (forward = (dy, -dx) of right - left)
        if isinstance(sl, list) and isinstance(sr, list): ph = math.degrees(math.atan2(-(sr[0] - sl[0]), sr[1] - sl[1]))
        fl = []
        if md > 35: fl.append('MESH')
        if ch < 35 or cc < 40: fl.append('CAM')
        if str(r.get('vrr', '1')) in ('0', '0.0') or str(r.get('vvis', '1')) in ('0', '0.0'): fl.append('REND')
        if ph is not None and prev_ph is not None and abs(ang(ph - prev_ph)) > 30: fl.append('BODYJ')
        prev_ph = ph
        tw = None   # V2.29: spine twist = heading of the spine_03 bone Z axis minus the pelvis Z axis (MM mesh), wrapped
        if isinstance(r.get('maz_spine_03'), list) and isinstance(r.get('maz_pelvis'), list):
            tw = ang(math.degrees(math.atan2(r['maz_spine_03'][1], r['maz_spine_03'][0])) - math.degrees(math.atan2(r['maz_pelvis'][1], r['maz_pelvis'][0])))
            worst['twist'] = max(worst.get('twist', 0), abs(tw))
            if prev_tw is not None:
                dtw = abs(ang(tw - prev_tw)); worst['twistj'] = max(worst.get('twistj', 0), dtw)
                if dtw > 40: fl.append('SPIN'); worst.setdefault('spin_t', []).append(round(t, 2))
        prev_tw = tw
        if prev is not None:
            dy = abs(ang(ay - f(prev.get('ay')))); worst['yawj'] = max(worst['yawj'], dy)
            if dy > 25: fl.append('YAWJ')
            psp = math.hypot(f(prev.get('avx')), f(prev.get('avy')))
            if vh is not None and ih is not None and abs(ang(vh - ih)) > 150 and sp > psp + 3 and sp > 150: fl.append('VELFLIP')
        worst['mesh'] = max(worst['mesh'], md); worst['camhead'] = min(worst['camhead'], ch)
        for x in fl: flags[x] = flags.get(x, 0) + 1
        if t0 <= t <= t1 and (fl or '--all' in opt or True):
            rows.append((t, r.get('stage', '')[-14:], li, ay, sp, vh, f(r.get('vwy')), ph, md, ch, cc, r.get('vrr', '-'), str(r.get('av_Phase27_SelectedObject', ''))[-26:], f(r.get('av_Phase27_SelectedTime')), str(r.get('av_CurrentSelectedDatabase', ''))[-26:], r.get('cv_ClipSpeedOn'), f(r.get('cv_ClipSpeed')), ' '.join(fl)))
        prev = r
    if t0 > 0 or t1 < 1e9:
        print('   t   stage           lix   liy   ayaw   spd  vhead  vwy  bodyH  mesh camH camC vrr clip                          ct    db                         cso  cs   flags')
        for x in rows:
            print('%5.2f %-14s %5.2f %5.2f %6.1f %5.0f %6s %5.0f %6s %5.1f %4.0f %4.0f %3s %-28s %4.2f %-26s %-5s %5.0f %s' % (x[0], x[1], x[2][0], x[2][1], x[3], x[4], '-' if x[5] is None else '%.0f' % x[5], x[6], '-' if x[7] is None else '%.0f' % x[7], x[8], x[9], x[10], x[11], x[12], x[13], x[14], x[15], x[16], x[17]))
    print('REV229 %s %s' % (lab, json.dumps({'frames': len(R), 'flags': flags, 'worst_mesh_cm': round(worst['mesh'], 1), 'min_cam_head_cm': round(worst['camhead'], 1), 'max_yaw_jump': round(worst['yawj'], 1), 'max_twist': round(worst.get('twist', 0), 0), 'max_twist_jump': round(worst.get('twistj', 0), 0), 'spin_t': worst.get('spin_t', [])[:12]})))
