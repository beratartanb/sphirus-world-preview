"""moments228.py label [label ...] [--req=T]: ONE event (the reversal request nearest --req, default the first request after 4.5 s) as a
timeline of moments, each with its own time: request (DesiredVelocity along x flips), brake (actor speed along the old direction starts
falling), component episode (cv_RedirectActive), ABP episode (av_SHM_RedirectActive), selection (asset changes to a non-loop clip; clip
+ start time), clip in the visible pose (SHM226_Rev curve weight > 0.5 of the clip remaining time, authored clips only), brake-foot
plant (first ball low & slow after the selection; foot, duration, drift), zero crossing (actor velocity along the old direction changes
sign), push (velocity along the new direction > 50 cm/s), handover to the loop (asset becomes a loop again), and the ENTRY STATE at the
selection frame: actor velocity vector (from the actor position), desired velocity, pawn yaw, support side / gait phase / contacts, ball
positions and velocities relative to the actor, pelvis, clip + ct, ABP frame counter. Travel axis = world x. cm, s. Harness evidence JSON."""
import json, sys, math, pathlib
E = pathlib.Path(__file__).resolve().parents[2] / 'Saved/Codex/SHME_V1_20260925/Evidence'
LENS = {}
try: LENS = {k: v['len'] for k, v in json.load(open(pathlib.Path(__file__).resolve().parents[2] / 'Saved/Codex/SHME_V226_20261024/gen226_rev_write.json'))['clips'].items()}
except Exception: pass
def f(x, d=0.0):
    try: return float(x)
    except Exception: return d
def b(x): return str(x) in ('True', 'true', '1', '1.0')
req_t = None
for a in sys.argv[1:]:
    if a.startswith('--req='): req_t = float(a[6:])
for lab in [a for a in sys.argv[1:] if not a.startswith('--')]:
    p = E / (lab + '.json')
    if not p.exists(): print('MOM228 %s MISSING' % lab); continue
    R = sorted([r for r in json.load(open(p)) if isinstance(r, dict) and r.get('t') is not None and isinstance(r.get('ax'), list) and isinstance(r.get('vb_ball_l'), list)], key=lambda r: f(r['t']))
    n = len(R); T = [f(r['t']) for r in R]
    def vel(k):
        if k <= 0: return (0.0, 0.0)
        dt = T[k] - T[k - 1]
        if dt <= 0: return (0.0, 0.0)
        return ((R[k]['ax'][0] - R[k - 1]['ax'][0]) / dt, (R[k]['ax'][1] - R[k - 1]['ax'][1]) / dt)
    def ballv(k, s):
        if k <= 0: return (0.0, 0.0)
        dt = T[k] - T[k - 1]; q, pq = R[k]['vb_ball_' + s], R[k - 1]['vb_ball_' + s]
        return ((q[0] - pq[0]) / dt, (q[1] - pq[1]) / dt) if dt > 0 else (0.0, 0.0)
    floor = {}
    for s in ('l', 'r'):
        zs = sorted(r['vb_ball_' + s][2] for r in R); floor[s] = zs[n // 10] + 2.0
    dvx = [(r.get('cv_DesiredVelocity') or [0, 0, 0])[0] for r in R]
    cands = [k for k in range(1, n) if dvx[k] * dvx[k - 1] < 0 and abs(dvx[k]) > 50 and T[k] > 4.5]
    if not cands: print('MOM228 %s no request found' % lab); continue
    k_req = min(cands, key=lambda k: abs(T[k] - req_t)) if req_t else cands[0]
    old_dir = 1.0 if dvx[k_req - 1] > 0 else -1.0
    out = {'request': T[k_req], 'old_dir': old_dir}
    v0 = vel(k_req - 1)[0] * old_dir
    k_br = next((k for k in range(k_req, n) if vel(k)[0] * old_dir < v0 - 0.03 * abs(v0) - 1), None); out['brake'] = T[k_br] if k_br else None
    k_crd = next((k for k in range(k_req, n) if b(R[k].get('cv_RedirectActive'))), None); out['comp_episode'] = T[k_crd] if k_crd else None
    k_ard = next((k for k in range(k_req, n) if b(R[k].get('av_SHM_RedirectActive'))), None); out['abp_episode'] = T[k_ard] if k_ard else None
    a0 = str(R[k_req - 1].get('av_Phase27_SelectedObject'))
    k_sel = next((k for k in range(k_req, n) if str(R[k].get('av_Phase27_SelectedObject')) != a0), None)
    out['selection'] = T[k_sel] if k_sel else None
    if k_sel:
        clip = str(R[k_sel].get('av_Phase27_SelectedObject')); ct = f(R[k_sel].get('av_Phase27_SelectedTime')); out['clip'] = clip[-24:]; out['ct_entry'] = round(ct, 3)
        L = LENS.get(clip.rsplit('.', 1)[-1])
        k_pose = None
        if L:
            for k in range(k_sel, n):
                ct_k = f(R[k].get('av_Phase27_SelectedTime')); rem = L - ct_k
                if rem > 0.05 and f(R[k].get('ac_SHM226_Rev')) > 0.5 * rem: k_pose = k; break
        out['in_pose_50'] = T[k_pose] if k_pose else None
        k_pl = None; foot = None
        for k in range(k_sel, n - 3):
            for s in ('l', 'r'):
                if all(R[j]['vb_ball_' + s][2] < floor[s] and math.hypot(*ballv(j, s)) < 80 for j in range(k, k + 3)):
                    k_pl = k; foot = s; break
            if k_pl: break
        if k_pl:
            j = k_pl
            while j + 1 < n and R[j + 1]['vb_ball_' + foot][2] < floor[foot] and math.hypot(*ballv(j + 1, foot)) < 80: j += 1
            out['plant'] = T[k_pl]; out['plant_foot'] = foot; out['plant_dur'] = round(T[j] - T[k_pl], 2)
            out['plant_drift'] = round(math.hypot(R[j]['vb_ball_' + foot][0] - R[k_pl]['vb_ball_' + foot][0], R[j]['vb_ball_' + foot][1] - R[k_pl]['vb_ball_' + foot][1]), 1)
        k_z = next((k for k in range(k_req, n) if vel(k)[0] * old_dir < 0), None); out['zero_cross'] = T[k_z] if k_z else None
        k_push = next((k for k in range(k_z or k_req, n) if vel(k)[0] * old_dir < -50), None); out['push50'] = T[k_push] if k_push else None
        def is_loop(s): return ('JogRev' not in s) and ('Pivot' not in s) and ('Rev' not in s)
        k_loop = next((k for k in range(k_sel + 1, n) if is_loop(str(R[k].get('av_Phase27_SelectedObject')))), None)
        out['handover'] = T[k_loop] if k_loop else None; out['next_asset'] = str(R[k_loop].get('av_Phase27_SelectedObject'))[-22:] if k_loop else None
        r = R[k_sel]; vx, vy = vel(k_sel)
        st = {'t': T[k_sel], 'actor_v': (round(vx), round(vy)), 'speed2d': round(f(r.get('Speed2D'))), 'desired_v': [round(x) for x in (r.get('cv_DesiredVelocity') or [0, 0, 0])[:2]], 'pawn_yaw': r.get('py'), 'mesh_yaw': r.get('my'),
              'support': r.get('cv_SupportSide'), 'gait_phase': r.get('cv_GaitPhase'), 'contactL': r.get('cv_ContactL'), 'contactR': r.get('cv_ContactR'),
              'ballL_rel': [round(r['vb_ball_l'][i] - r['ax'][i], 1) for i in (0, 1)] + [round(r['vb_ball_l'][2], 1)], 'ballR_rel': [round(r['vb_ball_r'][i] - r['ax'][i], 1) for i in (0, 1)] + [round(r['vb_ball_r'][2], 1)],
              'ballL_v': [round(x) for x in ballv(k_sel, 'l')], 'ballR_v': [round(x) for x in ballv(k_sel, 'r')], 'pelvis_rel': [round(r['vb_pelvis'][i] - r['ax'][i], 1) for i in (0, 1)] + [round(r['vb_pelvis'][2], 1)],
              'abp_frames': r.get('av_SHM_RedirectFrames'), 'db': str(r.get('av_CurrentSelectedDatabase'))[-22:], 'rd_speed0': r.get('cv_RedirectSpeed0'), 'rd_time': r.get('cv_RedirectTime')}
        out['entry_state'] = st
    print('MOM228 %-28s %s' % (lab[-28:], json.dumps(out)))
