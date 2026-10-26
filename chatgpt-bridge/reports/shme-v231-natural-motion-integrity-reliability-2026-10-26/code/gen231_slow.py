"""gen231_slow.py (editor job): V2.31 LOW-SPEED authored reversal family (brake -> support -> first step -> measured push -> jog loop) for an
entry state the production family was never designed for: the body is WALKING (or nearly stopped) in the old direction, 30-110 cm/s, when the
opposite request arrives (s29_swl12: back-walk A_LB_Walk_Bwd at 49-63 cm/s after a sprint pivot; j30_rel early release: forward walk-stop at
45-64 cm/s). The production bins start from the JOG loops at 245 / 300 cm/s: entered from a walk pose at 50 cm/s their planted foot is in the
wrong place (P6: 46.5 cm drag) and their designed speed is 70-80 cm/s too fast (the clip-bound capsule jumps -18 -> -86 cm/s).
Same character generator as production (gen226_rev + the V2.28 planted-brake-foot rule), different entry loop and designed physics:
  B_F : entry A_LB_Walk_Bwd (strafe back-walk) at v0 -> brake at BRAKE cm/s2 (stop within ~4 cm) -> first forward step -> push 261 cm/s2 -> A_CT_Jog_Fwd 300
  F_B : entry A_CT_Walk_Fwd (strafe forward walk) at v0 -> brake -> first backward step -> push 198 cm/s2 -> A_RB_Jog_Rear 245
The entry loop keeps its natural cadence (rate >= ENTRY_RATE_MIN; the walk legs never go into slow motion; planted feet are pinned by the
generator, so the cadence never slides them). Output /Game/GraceRanger/SHME/Animations/V231/SHM231S_SlowRev_<fam>_P<k> (NPH bins x 2).
builtins.G231S = {'dry_run', 'only', 'nph', 'v0', 'brake', 'entry_rate_min', 't_first', 'brake_behind'}; prints G231S {...}."""
import builtins, io, json
SRC = r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V226_20261024/gen226_rev.py'
src = io.open(SRC, encoding='utf8').read()
c = dict(getattr(builtins, 'G231S', {}))
REPL = [("OUTDIR = '/Game/GraceRanger/SHME/Animations/V226'", "OUTDIR = '/Game/GraceRanger/SHME/Animations/V231'"),
        ("name = 'SHM226_JogRev_%s_P%d' % (fam, k)", "name = 'SHM231S_SlowRev_%s_P%d' % (fam, k)"),
        ("(P / 'Saved/Codex/SHME_V226_20261024' / ('gen226_rev_%s.json'", "(P / 'Saved/Codex/SHME_V231_20261026' / ('gen231_slow_%s.json'"),
        ("    B = 'l' if landt['l'] < landt['r'] else 'r'; S = 'r' if B == 'l' else 'l'\n",
         "    B = 'l' if landt['l'] < landt['r'] else 'r'; S = 'r' if B == 'l' else 'l'\n"
         "    zb_ = {s_: ball0[s_][2] - EL.BZ0[s_] for s_ in ('l', 'r')}; B = 'l' if zb_['l'] <= zb_['r'] else 'r'; S = 'r' if B == 'l' else 'l'   # V2.31 slow: B = the SUPPORT foot (lowest ball): it brakes and pushes where it stands\n"),
        ("    qB = EL.rel(LB, 'foot_' + B)[1]\n",
         "    qB = EL.rel(LB, 'foot_' + B)[1]\n    tB = DT; ballB_world = (ball0[B][0], ball0[B][1], EL.BZ0[B]); qB = EL.rel(L0, 'foot_' + B)[1]; BSW_H = SWING_H * 0.8   # V2.31 slow: no brake swing at 30-110 cm/s (the stop takes ~3 cm)\n"
         "    if zb_[B] > 1.5:   # V2.31 slow r2: the support foot is still LANDING at tau0 -> it completes the loop landing (r1 pinned it in the air: 4-6 m/s crossfade drag at 60 FPS)\n"
         "        tlB_ = EL.next_land(B, tau0); tB = min(TB_MAX, max(TB_MIN, (tlB_ - tau0) / r0t)); LBb_ = EL.at(tlB_); bb_ = EL.rel(LBb_, 'ball_' + B)[0]; rB_ = ae.vsc(FWD, df(tB))\n"
         "        ballB_world = (rB_[0] + bb_[0], rB_[1] + bb_[1], EL.BZ0[B]); qB = EL.rel(LBb_, 'foot_' + B)[1]; BSW_H = 1.0\n"),
        ("SWING_H * 0.8, z0=bPos0[2])", "BSW_H, z0=bPos0[2])"),
        ("    tS_lift = (EL.next_lift(S, tau0) - tau0) / r0t if s_planted0 else 0.0\n",
         "    tS_lift = (EL.next_lift(S, tau0) - tau0) / r0t if s_planted0 else 0.0\n    tS_lift = min(tS_lift, SLOW_LIFT_MAX)   # V2.31 slow: a double-support S lifts right after the tiny brake (the walk loop's late lift overstretched the leg)\n"),
        # walk entry loops (track names: the intersection of all four loops)
        ("names_r = set(str(n) for n in AL.get_animation_track_names(u.load_asset(REAR))); names_f = set(str(n) for n in AL.get_animation_track_names(u.load_asset(FWDL)))\nNAMES = sorted(names_r & names_f)",
         "WBWD = '/Game/GraceRanger/Animations/LocomotionBehavior/A_LB_Walk_Bwd'; WFWD = '/Game/GraceRanger/Animations/Continuity/A_CT_Walk_Fwd'\n"
         "_tn = lambda p: set(str(n) for n in AL.get_animation_track_names(u.load_asset(p)))\nNAMES = sorted(_tn(REAR) & _tn(FWDL) & _tn(WBWD) & _tn(WFWD))"),
        ("RL = Loop(REAR, NAMES); FL = Loop(FWDL, NAMES)", "RL = Loop(REAR, NAMES); FL = Loop(FWDL, NAMES); WB = Loop(WBWD, NAMES); WF = Loop(WFWD, NAMES)"),
        ("    EL, XL = (RL, FL) if fam == 'B_F' else (FL, RL)          # entry loop, exit loop",
         "    EL, XL = (WB, FL) if fam == 'B_F' else (WF, RL)          # V2.31: WALK entry loop, jog exit loop"),
        ("    r0t = v0 / EL.V                                              # loop seconds per real second at full speed",
         "    r0t = max(v0 / EL.V, ENTRY_RATE_MIN)                         # V2.31: walk cadence kept (planted feet are pinned below)"),
        ("out = {'dry': DRY, 'loops': {'rear': {'T': round(RL.T, 3), 'V': round(RL.V, 1), 'NK': RL.NK}, 'fwd': {'T': round(FL.T, 3), 'V': round(FL.V, 1), 'NK': FL.NK}},",
         "out = {'dry': DRY, 'loops': {'rear': {'T': round(RL.T, 3), 'V': round(RL.V, 1), 'NK': RL.NK}, 'fwd': {'T': round(FL.T, 3), 'V': round(FL.V, 1), 'NK': FL.NK}, 'walk_bwd': {'T': round(WB.T, 3), 'V': round(WB.V, 1), 'NK': WB.NK}, 'walk_fwd': {'T': round(WF.T, 3), 'V': round(WF.V, 1), 'NK': WF.NK}},")]
for a, b in REPL:
    assert src.count(a) == 1, a[:70]
    src = src.replace(a, b)
src = src.replace("FL = Loop(FWDL, NAMES); WB", "FL = Loop(FWDL, NAMES); ENTRY_RATE_MIN = float(cfg.get('entry_rate_min', 0.9)); SLOW_LIFT_MAX = float(cfg.get('slow_lift_max', 0.16)); WB", 1)
v0 = float(c.get('v0', 55.0)); A = float(c.get('brake', 600.0))
prof = {'B_F': {'v0': v0, 'brake': A, 'push': 261.0, 'vexit': 300.0}, 'F_B': {'v0': v0, 'brake': A, 'push': 198.0, 'vexit': 245.0}}
builtins.G225 = {'dry_run': bool(c.get('dry_run', True)), 'nph': int(c.get('nph', 16)), 'only': c.get('only'), 'prof': prof, 'fam': c.get('fam', ['B_F', 'F_B']),
                 't_first': float(c.get('t_first', 0.30)), 'brake_behind': float(c.get('brake_behind', 4.0)), 'dip_cm': float(c.get('dip_cm', 1.5)),
                 'brake_deg': float(c.get('brake_deg', 2.5)), 'push_deg': float(c.get('push_deg', 3.0)), 'tail': 0.25, 'entry_rate_min': float(c.get('entry_rate_min', 0.9)),
                 'tb_min': float(c.get('tb_min', 0.10)), 'slow_lift_max': float(c.get('slow_lift_max', 0.16)), 'fade_len': float(c.get('fade_len', 0.25))}
g = {'__name__': 'g231S'}
exec(compile(src, 'gen226_rev_v231S.py', 'exec'), g)
out = g.get('out', {})
summ = {n: {kk: v.get(kk) for kk in ('B', 'S', 's_planted0', 'tB', 'tz', 'tS', 'len', 'foot_err', 'planted_drift', 'penetration', 'entry_err', 'exit_err', 'pelvis_min_minus_final', 'steps', 'saved', 'err')} for n, v in out.get('clips', {}).items()}
print('G231S ' + json.dumps({'dry': builtins.G225['dry_run'], 'prof': prof, 'loops': out.get('loops'), 'clips': summ}, default=str))
