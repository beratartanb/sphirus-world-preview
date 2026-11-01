"""make244_tools.py : derive the V2.44 editor tools from the V2.42 ones (text patches, each asserted):
  gen244_latstop.py  = gen242_latstop + (a) reachable first landing, (b) non-final plant orientation continuity, V244 names/paths
  gen244_idle.py     = gen242_idle + base pose from the stop families' final stance (SHM_A_CP2_Jog_Fwd_Stop last frame)
  build244_latdb.py / build244_idledb.py = V242 builders with the V244 folder and their own BranchIn track names
Run with the engine python (no unreal import here)."""
import re, pathlib
root = pathlib.Path(__file__).resolve().parents[2]
T2 = root / 'Tools/SHME_V242_20261101'; T4 = root / 'Tools/SHME_V244_20261101'

def rep(s, old, new, n=1):
    assert s.count(old) >= 1, ('missing', old[:90])
    return s.replace(old, new) if n == 0 else s.replace(old, new, n)

# ---------- gen244_latstop.py
s = (T2 / 'gen242_latstop.py').read_text(encoding='utf8')
hdr = '''"""gen244_latstop.py (editor job): V2.44 lateral brake/stop family = gen242_latstop.py with two plan/build fixes for the entry phases where
the brake foot is already landing at the release (V2.43 production j41_rl_p10 -> SHM242_LatStop_L_Bl_P21: the plan asked the left foot,
0.11 s from its loop landing, to land 38 cm further along the travel AND snapped its orientation to the final idle orientation at that
non-final plant -> the blended foot skimmed 31 cm and whipped ~90 deg = 32.5 cm "slide"):
  (a) reachable first landing: a brake foot in flight lands at most EXTRA_V x t_land cm beyond its natural loop landing (extra_v 60 cm/s);
      the braking continues with the following steps (plan unchanged otherwise);
  (b) orientation continuity: a NON-final plant keeps the foot orientation reached in its swing = slerp(loop q, final q, qpart 0.45);
      only the swing into a FINAL plant rotates the foot fully to the idle orientation (the yaw change happens unloaded, in the air).
Names SHM244_LatStop_<L|R>_B<brake foot>_P<bin> in /Game/GraceRanger/SHME/Animations/V244; builtins.G244L = G242L keys + extra_v, qpart.
--- gen242 docstring: '''
s = rep(s, '"""gen242_latstop.py (editor job): ', hdr)
s = rep(s, "cfg = dict(getattr(builtins, 'G242L', {}))", "cfg = dict(getattr(builtins, 'G244L', {}))")
s = rep(s, "OUTDIR = cfg.get('outdir', '/Game/GraceRanger/SHME/Animations/V242')", "OUTDIR = cfg.get('outdir', '/Game/GraceRanger/SHME/Animations/V244')")
s = rep(s, "SD = P / 'Saved/Codex/SHME_V242_20261101'", "SD = P / 'Saved/Codex/SHME_V244_20261101'")
s = rep(s, "STEP_MAX = K('step_max', 38.0); STEP_MAX_V = K('step_max_v', 0.08)",
        "STEP_MAX = K('step_max', 38.0); STEP_MAX_V = K('step_max_v', 0.08); EXTRA_V = K('extra_v', 60.0); QPART = K('qpart', 0.45)")
old = """        po_ = state['r' if foot == 'l' else 'l']['pos']
        smax = STEP_MAX + STEP_MAX_V * stop_v(t_land)"""
new = """        if k == 0 and not pl[B] and not final:            # V2.44 (a): a brake foot already landing cannot be driven far beyond its natural landing
            tau_land = next_event(B, tau0, True); nat_fwd = rootY + ae.vdot(rel(loop_local(tau_land), 'ball_' + B)[0], FWD)
            lim = nat_fwd + EXTRA_V * t_land; pf = ae.vdot(p, FWD)
            if pf > lim: p = ae.vadd(p, ae.vsc(FWD, lim - pf)); p = (p[0], p[1], IDLE_BALL[foot][2]); CLAMPED.append((foot, round(pf - lim, 1)))
        po_ = state['r' if foot == 'l' else 'l']['pos']
        smax = STEP_MAX + STEP_MAX_V * stop_v(t_land)"""
s = rep(s, old, new)
s = rep(s, "def plan(tau0):\n", "CLAMPED = []\ndef plan(tau0):\n")
old = """            if inflight and st is mine[0]:
                vv = vloop[s]; sp = math.hypot(vv[0], vv[1]) * st['t_land']; cap = min(1.0, VCAP / sp) if sp > 1e-6 else 1.0
                tl[s].append(('swing0', 0.0, st['t_land'], cur, (vv[0] * cap, vv[1] * cap, 0.0), st['p'], cur_q)); inflight = False
            else:
                tl[s].append(('plant', t_cur, st['t_lift'], cur, None, None, cur_q))
                T_ = max(st['t_land'] - st['t_lift'], 1e-3); k_ = LIFT_K1 if (pl[s] and st is mine[0]) else LIFT_K2
                vf = min(k_ * stop_v(st['t_lift']), VCAP / T_) if st['kind'] != 'close' else 0.0
                tl[s].append(('swing1' if (pl[s] and st is mine[0]) else 'swing', st['t_lift'], st['t_land'], cur, ae.vsc(FWD, vf), st['p'], cur_q))
            cur = st['p']; t_cur = st['t_land']; cur_q = QFIN[s]"""
new = """            q1 = QFIN[s] if st['final'] else slerp(cur_q, QFIN[s], QPART)      # V2.44 (b): a non-final plant keeps a partial orientation
            if inflight and st is mine[0]:
                vv = vloop[s]; sp = math.hypot(vv[0], vv[1]) * st['t_land']; cap = min(1.0, VCAP / sp) if sp > 1e-6 else 1.0
                tl[s].append(('swing0', 0.0, st['t_land'], cur, (vv[0] * cap, vv[1] * cap, 0.0), st['p'], cur_q, q1)); inflight = False
            else:
                tl[s].append(('plant', t_cur, st['t_lift'], cur, None, None, cur_q))
                T_ = max(st['t_land'] - st['t_lift'], 1e-3); k_ = LIFT_K1 if (pl[s] and st is mine[0]) else LIFT_K2
                vf = min(k_ * stop_v(st['t_lift']), VCAP / T_) if st['kind'] != 'close' else 0.0
                tl[s].append(('swing1' if (pl[s] and st is mine[0]) else 'swing', st['t_lift'], st['t_land'], cur, ae.vsc(FWD, vf), st['p'], cur_q, q1))
            cur = st['p']; t_cur = st['t_land']; cur_q = q1"""
s = rep(s, old, new)
old = """            kind, ta, tb, p0, v0, p1, q0 = seg
            if kind == 'plant':"""
new = """            kind, ta, tb, p0, v0, p1, q0 = seg[:7]; qt = seg[7] if len(seg) > 7 else QFIN[s]
            if kind == 'plant':"""
s = rep(s, old, new)
s = rep(s, "                q = slerp(q0, QFIN[s], mj(x)); bp = swing(p0, v0 if v0 else (0.0, 0.0, 0.0), p1, ta, tb, t, h, z0=p0[2])",
        "                q = slerp(q0, qt, mj(x)); bp = swing(p0, v0 if v0 else (0.0, 0.0, 0.0), p1, ta, tb, t, h, z0=p0[2])")
s = s.replace("SHM242_LatStop_%s_B%s_P0", "SHM244_LatStop_%s_B%s_P0").replace("SHM242_LatStop_%s_B%s_P%02d", "SHM244_LatStop_%s_B%s_P%02d")
s = rep(s, "    print('G242L_STEPS', name,", "    print('G244L_STEPS', name, CLAMPED[-1:],")
s = s.replace("print('G242L_SKIP'", "print('G244L_SKIP'").replace("gen242_latstop_%s_%s.json", "gen244_latstop_%s_%s.json").replace("print('G242L ' + json.dumps", "print('G244L ' + json.dumps")
s = rep(s, "c.open_bracket(u.Text('SHME V2.42 lateral stop ' + name), True)", "c.open_bracket(u.Text('SHME V2.44 lateral stop ' + name), True)")
(T4 / 'gen244_latstop.py').write_text(s, encoding='utf8'); print('gen244_latstop ok', s.count('V2.44'))

# ---------- gen244_idle.py
s = (T2 / 'gen242_idle.py').read_text(encoding='utf8')
s = rep(s, '"""gen242_idle.py (editor job): ', '''"""gen244_idle.py (editor job): V2.44 weighted idle = gen242_idle.py with the BASE POSE taken from the stance the project stop families end in
(base_src / base_last / base_frame: default = last frame of SHM_A_CP2_Jog_Fwd_Stop, the final_src of the V2.37 jog stops and the V2.42/44
lateral stops), so a stop hands over to this clip pose-exactly at its frame 0 (the V2.43 clip was built on af_Stand_Idle frame 0 -> MM
entered it at arbitrary times, e.g. 11 s = weight on one foot -> restart slide); the loop is CLOSED (frame N-1 = frame 0) so the re-search
at the clip end re-enters at the neutral start. builtins.G244I = G242I keys + base_src, base_last, base_frame.
--- gen242 docstring: ''')
s = rep(s, "cfg = dict(getattr(builtins, 'G242I', {}))", "cfg = dict(getattr(builtins, 'G244I', {}))")
s = rep(s, "OUT = cfg.get('out', '/Game/GraceRanger/SHME/Animations/V242/SHM242_Idle_Weighted')", "OUT = cfg.get('out', '/Game/GraceRanger/SHME/Animations/V244/SHM244_Idle_Weighted')")
s = rep(s, "SD = P / 'Saved/Codex/SHME_V242_20261101'; SD.mkdir(parents=True, exist_ok=True)", "SD = P / 'Saved/Codex/SHME_V244_20261101'; SD.mkdir(parents=True, exist_ok=True)")
old = "B0 = ae.read_local(idle, NAMES, [0]); BASE = {b: B0[b][0] for b in NAMES}"
new = """BSRC = cfg.get('base_src', '/Game/GraceRanger/SHME/Animations/Stops/SHM_A_CP2_Jog_Fwd_Stop'); base = u.load_asset(BSRC); assert base, BSRC
BNAMES = [str(n) for n in AL.get_animation_track_names(base)]; assert all(b in BNAMES for b in NAMES), [b for b in NAMES if b not in BNAMES][:5]
BFR = (ae.num_frames(base) - 1) if cfg.get('base_last', True) else int(cfg.get('base_frame', 0))
B0 = ae.read_local(base, NAMES, [BFR]); BASE = {b: B0[b][0] for b in NAMES}"""
s = rep(s, old, new)
s = s.replace("gen242_idle_%s.json", "gen244_idle_%s.json").replace("print('G242I ' + json.dumps", "print('G244I ' + json.dumps")
s = s.replace("label='SHM242_Idle_Weighted'", "label='SHM244_Idle_Weighted'").replace("'SHME V2.42 weighted idle'", "'SHME V2.44 weighted idle'")
(T4 / 'gen244_idle.py').write_text(s, encoding='utf8'); print('gen244_idle ok')

# ---------- DB builders (V244 folder, own track names)
for src, dst, V, tr, tag in (('build242_latdb.py', 'build244_latdb.py', 'V244', 'SHME_V244_LatStop', 'LDB244'),
                             ('build242_idledb.py', 'build244_idledb.py', 'V244', 'SHME_V244_Idle', 'IDB244')):
    s = (T2 / src).read_text(encoding='utf8')
    s = rep(s, "V = '/Game/GraceRanger/SHME/Animations/V242'", "V = '/Game/GraceRanger/SHME/Animations/%s'" % V)
    s, n = re.subn(r"tr = 'SHME_V242_\w+'", "tr = '%s'" % tr, s, count=1); assert n == 1
    s = s.replace("print('LDB242 '", "print('%s '" % tag).replace("print('IDB242 '", "print('%s '" % tag)
    (T4 / dst).write_text(s, encoding='utf8'); print(dst, 'ok')
