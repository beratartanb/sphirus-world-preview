"""gen231_loaded.py (editor job): V2.31 LOADED reversal = a different CHOREOGRAPHY, not a slower tempo (the V2.30 loaded family stretched the
production brake/push in time and showed no visible gain). Under accumulated effort the brake foot cannot absorb the whole momentum:
  1. BRAKE plant B lands SHORT of the stop point (B_SHORT cm before it in the old travel): the body keeps moving over and past it
     (lower designed deceleration BRAKE cm/s2 = the loaded body cannot stop on one foot)
  2. CATCH step: the other foot S swings on through and lands BRAKE_BEHIND cm beyond the stop point (old travel), takes the load, the pelvis
     absorbs deeper (DIP_CM) with more counter-lean (BRAKE_DEG) -> the body stops over S
  3. FIRST STEP of the new travel by B (it lifts from behind the stopped body), time-designed T_FIRST after the zero crossing
  4. measured RE-PUSH: lower push acceleration (PUSH cm/s2) on the rate-floored exit-loop clock, then the loop rhythm
Built from the production generator (gen226_rev: loops, swing, pins, leg solve, checks, write) with the phase-1/2 foot plan replaced.
Families: F_B (forward jog 300 -> backward, the second reversal of e29_load) and B_F (back-run 245 -> forward). Output
/Game/GraceRanger/SHME/Animations/V231/SHM231L_LoadRev_<fam>_P<k>. builtins.G231L = {'dry_run', 'only', 'nph', 'fam', 'brake', 'push', 'b_short',
'brake_behind', 't_first', 'dip_cm', 'brake_deg', 'push_deg', 'catch_lead'}; prints G231L {...}."""
import builtins, io, json
SRC = r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V226_20261024/gen226_rev.py'
src = io.open(SRC, encoding='utf8').read()
c = dict(getattr(builtins, 'G231L', {}))
head = src[:src.index("out = {'dry': DRY")]
assert head.count("OUTDIR = '/Game/GraceRanger/SHME/Animations/V226'") == 1
head = head.replace("OUTDIR = '/Game/GraceRanger/SHME/Animations/V226'", "OUTDIR = '/Game/GraceRanger/SHME/Animations/V231'")
prof = {'F_B': {'v0': 300.0, 'brake': float(c.get('brake', 540.0)), 'push': float(c.get('push', 150.0)), 'vexit': 245.0},
        'B_F': {'v0': 245.0, 'brake': float(c.get('brake', 540.0)) * 245.0 / 300.0 * 1.15, 'push': float(c.get('push', 150.0)) * 261.0 / 198.0, 'vexit': 300.0}}
builtins.G225 = {'dry_run': bool(c.get('dry_run', True)), 'nph': int(c.get('nph', 16)), 'prof': prof, 'fam': c.get('fam', ['F_B']), 'only': c.get('only'),
                 't_first': float(c.get('t_first', 0.36)), 'brake_behind': float(c.get('brake_behind', 6.0)), 'dip_cm': float(c.get('dip_cm', 4.0)),
                 'brake_deg': float(c.get('brake_deg', 6.0)), 'push_deg': float(c.get('push_deg', 2.0)), 'tail': 0.30}
CATCH = '''
B_SHORT = float(CFG231.get('b_short', 22.0)); CATCH_LEAD = float(CFG231.get('catch_lead', 0.04)); REACH_MAX = float(CFG231.get('reach_max', 36.0))
def build_catch(fam, key):
    EL, XL = (RL, FL) if fam == 'B_F' else (FL, RL)
    sgn = 1.0 if fam == 'B_F' else -1.0
    vfun, dfun, tz, tv = profile(fam); vexit = PROF[fam]['vexit']; v0 = PROF[fam]['v0']
    vf = lambda t: sgn * vfun(t); df = lambda t: sgn * dfun(t)
    tau0 = key * EL.T / NPH; L0 = EL.at(tau0); root0 = (0.0, 0.0, 0.0)
    r0t = v0 / EL.V; tauE = lambda t: tau0 + r0t * t
    ball0 = {s: EL.rel(L0, 'ball_' + s)[0] for s in ('l', 'r')}
    landt = {s: EL.next_land(s, tau0) for s in ('l', 'r')}
    B = 'l' if landt['l'] < landt['r'] else 'r'; S = 'r' if B == 'l' else 'l'
    if EL.rel(L0, 'ball_' + B)[0][2] < EL.BZ0[B] + 3.0: B, S = S, B
    tB = min(TB_MAX, max(TB_MIN, (landt[B] - tau0) / r0t))
    latv = ae.vnorm(ae.vcross((0.0, 0.0, 1.0), FWD)); oldd = ae.vsc(FWD, -sgn)
    LB = EL.at(landt[B]); latB = ae.vdot(EL.rel(LB, 'ball_' + B)[0], latv); qB = EL.rel(LB, 'foot_' + B)[1]
    stopP = ae.vsc(FWD, df(tz))
    reachB = max(ae.vdot(ae.vsc(FWD, df(tB)), oldd) + 8.0, ae.vdot(stopP, oldd) - B_SHORT)
    pB = ae.vadd(ae.vsc(oldd, reachB), ae.vsc(latv, latB)); ballB = (pB[0], pB[1], EL.BZ0[B]); bTarget = foot_at_ball(B, ballB, qB)
    s_planted0 = EL.planted(S, tau0); ballS0 = (ball0[S][0], ball0[S][1], EL.BZ0[S]) if s_planted0 else None
    tS_lift = (EL.next_lift(S, tau0) - tau0) / r0t if s_planted0 else 0.0
    tRedir = max(tS_lift, tB - REDIR_LEAD)
    # r2: a PINNED support foot cannot stay planted once the body has passed it by more than REACH_MAX (leg extension = natural toe-off);
    # r1 kept it pinned until the loop lift -> 44-59 cm behind the pelvis, leg overstretched, dragged foot (P0-2, P15, P21-25, P31)
    if s_planted0:
        for kk in range(1, 60):
            tt = kk * DT
            if ae.vdot(ae.vsub(ae.vsc(FWD, df(tt)), ballS0), oldd) > REACH_MAX: tRedir = min(tRedir, tt); tS_lift = min(tS_lift, tt); break
    LS_ = EL.at(EL.next_land(S, tau0)); latS = ae.vdot(EL.rel(LS_, 'ball_' + S)[0], latv); qS = EL.rel(LS_, 'foot_' + S)[1]
    pC = ae.vadd(ae.vadd(stopP, ae.vsc(oldd, BRAKE_BEHIND)), ae.vsc(latv, latS)); ballC = (pC[0], pC[1], EL.BZ0[S]); cTarget = foot_at_ball(S, ballC, qS)
    tC = max(tRedir + 0.26, tB + 0.20, tz - CATCH_LEAD)
    tauHS = XL.next_land(B, 0.02); LH = XL.at(tauHS); rB_hs = XL.rel(LH, 'foot_' + B); qB_hs = rB_hs[1]
    tBl = tC + 0.04; tF = max(tz + T_FIRST, tBl + 0.24)
    rootF = ae.vsc(FWD, df(tF)); landB = ae.vadd(rootF, rB_hs[0]); landB = (landB[0], landB[1], rB_hs[0][2])
    tauTO = XL.prev_lift(B, tauHS)
    L = tv + TAIL; N = int(math.ceil(L / DT)) + 1
    info = {'fam': fam, 'B': B, 'S': S, 'tau0': round(tau0, 3), 'tB': round(tB, 3), 'tC': round(tC, 3), 'tz': round(tz, 3), 'tF': round(tF, 3), 'tv': round(tv, 3),
            's_planted0': s_planted0, 'ballB': [round(x, 1) for x in ballB], 'ballC': [round(x, 1) for x in ballC], 'landB': [round(x, 1) for x in landB], 'stop': round(df(tz), 1)}
    frames = []; sw0 = None; sPos = None; sVel = (0.0, 0.0, 0.0); qSl = None; sLand = None
    b0 = EL.rel(L0, 'foot_' + B); bPos0 = ae.vadd(root0, b0[0]); qB0 = b0[1]
    e = DT; b1 = EL.rel(EL.at(tauE(e)), 'foot_' + B); bVel0 = tuple((ae.vadd(ae.vsc(FWD, df(e)), b1[0])[i] - bPos0[i]) / e for i in range(3))
    pin = {}; off = {}; liftTau = {}; tauX = tauHS
    for f in range(N):
        t = f * DT; rt = ae.vsc(FWD, df(t))
        Le = EL.at(tauE(min(t, tB + 0.15)))
        if t < tF: tauX = tauTO + (tauHS - tauTO) * sm((t - tC) / max(tF - tC, 1e-3)); Lx = XL.at(tauX)
        else:
            if f > 0 and (f - 1) * DT >= tF: tauX += max(RATE_MIN, min(1.0, abs(vf(t)) / vexit)) * DT
            else: tauX = tauHS
            Lx = XL.at(tauX)
        wA = sm((t - (tB - 0.05)) / max(tF + 0.15 - (tB - 0.05), 1e-3)); wT = sm((t - tB) / max(tF + 0.25 - tB, 1e-3))
        pose = blend_pose(Le, Lx, wT, TRUNK)
        for b in ARMS: pose[b] = (lerp(Le[b][0], Lx[b][0], wA), slerp(Le[b][1], Lx[b][1], wA), lerp(Le[b][2], Lx[b][2], wA))
        dip = DIP_CM * bell(t, tB - 0.05, tF + 0.05)
        pt, pq, ps = pose['pelvis']; pose['pelvis'] = ((pt[0], pt[1], pt[2] - dip), pq, ps)
        pose['root'] = (rt, FL.Lk['root'][0][1], FL.Lk['root'][0][2])
        ft = {}
        if t < tF:
            if t < tB: ft[B] = (swing(bPos0, bVel0, bTarget, 0.0, tB, t, SWING_H * 0.8, z0=bPos0[2]), slerp(qB0, qB, mj(t / max(tB, 1e-3))))
            elif t < tBl: ft[B] = (bTarget, qB)
            else: ft[B] = (swing(bTarget, (0.0, 0.0, 0.0), landB, tBl, tF, t, SWING_H * 0.9, z0=bTarget[2]), slerp(qB, qB_hs, mj((t - tBl) / max(tF - tBl, 1e-3))))
            if s_planted0 and t < max(tS_lift, tRedir):
                qs = EL.rel(Le, 'foot_' + S)[1]; ft[S] = (foot_at_ball(S, ballS0, qs), qs)
            elif t < tRedir:
                ls = EL.rel(Le, 'foot_' + S)
                # r2: S landing in the loop before the redirect is PINNED where it lands (r1 followed the loop shape on the floor: 8-25 cm slides)
                if EL.planted(S, tauE(t)):
                    if sLand is None: lb_ = EL.rel(Le, 'ball_' + S)[0]; sLand = (rt[0] + lb_[0], rt[1] + lb_[1], EL.BZ0[S])
                    ft[S] = (foot_at_ball(S, sLand, ls[1]), ls[1])
                else: ft[S] = (ae.vadd(rt, ls[0]), ls[1])
            elif t < tC:
                if sw0 is None:
                    sw0 = t; ls = EL.rel(Le, 'foot_' + S); sPos = ae.vadd(rt, ls[0]); qSl = ls[1]
                    ls2 = EL.rel(EL.at(tauE(min(t + e, tB + 0.15))), 'foot_' + S); sVel = tuple((ae.vadd(ae.vsc(FWD, df(t + e)), ls2[0])[i] - sPos[i]) / e for i in range(3))
                    if s_planted0: sPos = foot_at_ball(S, ballS0, qSl); sVel = (0.0, 0.0, 0.0)
                    elif sLand is not None: sPos = foot_at_ball(S, sLand, qSl); sVel = (0.0, 0.0, 0.0)
                ft[S] = (swing(sPos, sVel, cTarget, sw0, tC, t, SWING_H, z0=sPos[2]), slerp(qSl, qS, mj((t - sw0) / max(tC - sw0, 1e-3))))
            else: ft[S] = (cTarget, qS)
            if f == N - 1 or (f + 1) * DT >= tF:
                bb = ae.vadd(landB, ae.qrot(qB_hs, BALL_LOCAL[B])); pin[B] = (bb[0], bb[1], XL.BZ0[B]); pin[S] = ballC
        else:
            for s in ('l', 'r'):
                ls = XL.rel(Lx, 'foot_' + s); loopPos = ae.vadd(rt, ls[0]); pl = XL.planted(s, tauX)
                if pl and s not in pin:
                    lb = XL.rel(Lx, 'ball_' + s)[0]; pin[s] = (rt[0] + lb[0], rt[1] + lb[1], XL.BZ0[s]); off.pop(s, None)
                if not pl and s in pin:
                    off[s] = ae.vsub(foot_at_ball(s, pin[s], ls[1]), loopPos); off[s] = (off[s][0], off[s][1], 0.0); liftTau[s] = tauX; pin.pop(s)
                if s in pin: ft[s] = (foot_at_ball(s, pin[s], ls[1]), ls[1])
                else:
                    fade = 1.0 - mj((tauX - liftTau.get(s, tauX)) / FADE_LEN) if s in off else 0.0
                    ft[s] = (ae.vadd(loopPos, ae.vsc(off.get(s, (0.0, 0.0, 0.0)), fade)), ls[1])
        frames.append((pose, ft))
    return finish(fam, frames, info, tB, tz, tF, tauX, EL, XL, N, tC)
'''
# the production build() tail (leans, leg solve, ik copy, checks) is reused verbatim as finish(); the brake lean runs to the catch
b1 = head.index("    local = {b: [fr[0][b] for fr in frames] for b in NAMES}")
tail = head[b1:head.index("def write(")]
ol = "a = sgn * (BRAKE_DEG * bell(t, tB - 0.10, tz + 0.15))"
assert tail.count(ol) == 1
tail = tail.replace(ol, "a = sgn * (BRAKE_DEG * bell(t, tB - 0.10, tC + 0.15))")
fin = ("def finish(fam, frames, info, tB, tz, tS, tauX, EL, XL, N, tC):\n    sgn = 1.0 if fam == 'B_F' else -1.0; tau0 = info['tau0']; L0 = EL.at(tau0)\n"
       "    vfun, dfun, _tz, _tv = profile(fam); df = lambda t: sgn * dfun(t)\n" + tail)
head = head + "\nCFG231 = " + repr(c) + "\n" + fin + CATCH
loop = '''
out = {'dry': DRY, 'prof': PROF, 'cfg': {k: v for k, v in cfg.items() if k != 'only'}, 'clips': {}}
for fam in FAMS:
    for k in range(NPH):
        name = 'SHM231L_LoadRev_%s_P%d' % (fam, k)
        if ONLY and name not in ONLY: continue
        try:
            local, info = build_catch(fam, k)
            if not DRY: info['saved'], info['path'] = write(name, local, len(local['root']), FL if fam == 'B_F' else RL)
        except Exception:
            import traceback; info = {'err': traceback.format_exc()[-900:]}
        out['clips'][name] = info
(P / 'Saved/Codex/SHME_V231_20261026' / ('gen231_loaded_%s.json' % ('dry' if DRY else 'write'))).write_text(json.dumps(out, indent=1))
'''
g = {'__name__': 'g231L'}
exec(compile(head + loop, 'gen231_loaded_full.py', 'exec'), g)
out = g.get('out', {})
summ = {n: {kk: v.get(kk) for kk in ('B', 'S', 's_planted0', 'tB', 'tC', 'tz', 'tF', 'len', 'stop', 'foot_err', 'planted_drift', 'penetration', 'entry_err', 'exit_err', 'pelvis_min_minus_final', 'steps', 'saved', 'err')} for n, v in out.get('clips', {}).items()}
print('G231L ' + json.dumps({'dry': builtins.G225['dry_run'], 'prof': prof, 'clips': summ}, default=str))
