"""gen236_load.py (editor job): V2.36 LOADED (effort) jog reversal = the V2.31/V2.32 loaded catch-step choreography (brake foot lands SHORT,
the other foot catches beyond the stop point, deeper absorb, measured re-push on a lower push acceleration) with
  * no held double support: the first step of the new travel follows the catch (T_FIRST 0.12 s after the zero crossing, was 0.36 s ->
    e29_load held both feet 0.4 s in the V2.35 tables = the user's freeze in the effort state);
  * the V2.36 whole-body brake: arm swing amplitude drops to ARM_KEEP over brake -> catch -> first step, the upper arms carry a short inertial
    swing toward the OLD travel, the neck counters the brake / push trunk lean (head level);
  * the effort difference stays a choreography + capsule difference (lower brake 540 and push 150 cm/s2 than the rested 800 / 550-650,
    deeper dip, catch step) - not a slowed clip.
Source = gen231_loaded.py + the gen232_loaded.py catch_natural patch, executed with these patches. Output
/Game/GraceRanger/SHME/Animations/V236/SHM236L_LoadRev_<fam>_P<k>. builtins.G236L = G231L keys + 'arm_keep', 'arm_fwd', 'neck_k'.
Prints G236L {...}."""
import builtins, io, json
S231 = r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V231_20261026/gen231_loaded.py'
txt = io.open(S231, encoding='utf8').read()
def rep(old, new, n=1):
    global txt
    assert txt.count(old) == n, ('patch anchor', old[:70], txt.count(old))
    txt = txt.replace(old, new)
# ---- gen232 catch_natural (verbatim REPL of gen232_loaded.py)
rep("    tC = max(tRedir + 0.26, tB + 0.20, tz - CATCH_LEAD)\n",
    "    tC = max(tRedir + 0.26, tB + 0.20, tz - CATCH_LEAD)\n"
    "    natC = False\n"
    "    if bool(CFG231.get('catch_natural', False)) and not s_planted0:\n"
    "        tSL = (EL.next_land(S, tau0) - tau0) / r0t\n"
    "        if tB - float(CFG231.get('catch_nat_pre', 0.25)) <= tSL <= min(tC, tB + 0.15):\n"
    "            natC = True; tRedir = 1.0e9\n"
    "            LSL = EL.at(EL.next_land(S, tau0)); bl_ = EL.rel(LSL, 'ball_' + S)[0]; rS_ = ae.vsc(FWD, df(tSL))\n"
    "            ballC = (rS_[0] + bl_[0], rS_[1] + bl_[1], EL.BZ0[S]); qS = EL.rel(LSL, 'foot_' + S)[1]; cTarget = foot_at_ball(S, ballC, qS)\n")
rep("    info = {'fam': fam, 'B': B, 'S': S,", "    info = {'nat_catch': natC, 'fam': fam, 'B': B, 'S': S,")
rep("                bb = ae.vadd(landB, ae.qrot(qB_hs, BALL_LOCAL[B])); pin[B] = (bb[0], bb[1], XL.BZ0[B]); pin[S] = ballC\n",
    "                bb = ae.vadd(landB, ae.qrot(qB_hs, BALL_LOCAL[B])); pin[B] = (bb[0], bb[1], XL.BZ0[B]); pin[S] = sLand if (natC and sLand is not None) else ballC\n")
# ---- V2.36 output
rep("head = head.replace(\"OUTDIR = '/Game/GraceRanger/SHME/Animations/V226'\", \"OUTDIR = '/Game/GraceRanger/SHME/Animations/V231'\")",
    "head = head.replace(\"OUTDIR = '/Game/GraceRanger/SHME/Animations/V226'\", \"OUTDIR = '/Game/GraceRanger/SHME/Animations/V236'\")")
rep("        name = 'SHM231L_LoadRev_%s_P%d' % (fam, k)\n", "        name = 'SHM236L_LoadRev_%s_P%d' % (fam, k)\n")
rep("(P / 'Saved/Codex/SHME_V231_20261026' / ('gen231_loaded_%s.json'", "(P / 'Saved/Codex/SHME_V236_20261028' / ('gen236_load_%s.json'")
rep("builtins.G225 = {", "builtins.G225 = {'arm_keep': float(c.get('arm_keep', 0.4)), 'arm_fwd': float(c.get('arm_fwd', 7.0)), 'neck_k': float(c.get('neck_k', 0.7)), ")
# ---- V2.36 arms in the catch build (keep the swing small through brake -> catch -> first step)
rep("        for b in ARMS: pose[b] = (lerp(Le[b][0], Lx[b][0], wA), slerp(Le[b][1], Lx[b][1], wA), lerp(Le[b][2], Lx[b][2], wA))\n",
    "        keep = 1.0 - (1.0 - ARM_KEEP) * bell(t, tB - 0.12, tF + 0.15)\n"
    "        for b in ARMS:\n"
    "            q_ = slerp(Le[b][1], Lx[b][1], wA); m_ = slerp(MEAN_E[b], MEAN_X[b], wA)\n"
    "            pose[b] = (lerp(Le[b][0], Lx[b][0], wA), slerp(m_, q_, keep), lerp(Le[b][2], Lx[b][2], wA))\n")
rep("def build_catch(fam, key):\n", "def build_catch(fam, key):\n    global MEAN_E, MEAN_X\n    MEAN_E, MEAN_X = (MEAN_R, MEAN_F) if fam == 'B_F' else (MEAN_F, MEAN_R)\n")
# ---- V2.36 patches of the production source the loaded generator reads (trunk lean neck counter + arm inertia, full FK bones, arm means)
rep("src = io.open(SRC, encoding='utf8').read()\n",
    "src = io.open(SRC, encoding='utf8').read()\n"
    "for _a, _b in V236_SRC_PATCHES:\n"
    "    assert src.count(_a) == 1, ('v236 src anchor', _a[:60]); src = src.replace(_a, _b)\n")
PATCHES = [
    ("        if abs(a) > 1e-3: ae.apply_bone_delta(clip, local, 'spine_01', f, ae.qaxis(lat, -a))\n",
     "        if abs(a) > 1e-3:\n"
     "            ae.apply_bone_delta(clip, local, 'spine_01', f, ae.qaxis(lat, -a)); ae.apply_bone_delta(clip, local, 'neck_01', f, ae.qaxis(lat, a * NECK_K))\n"
     "        fw = -sgn * ARM_FWD * bell(t, tB - 0.06, tB + 0.34)\n"
     "        if abs(fw) > 1e-3:\n"
     "            for s_ in ('l', 'r'): ae.apply_bone_delta(clip, local, 'upperarm_' + s_, f, ae.qaxis(lat, fw))\n"),
    ("'head', 'neck_01', 'spine_05', 'spine_03', 'spine_01'] + [b for b in ('ik_foot_l', 'ik_foot_r') if b in names])",
     "'head', 'neck_01', 'spine_05', 'spine_03', 'spine_01', 'hand_l', 'hand_r', 'upperarm_l', 'upperarm_r', 'lowerarm_l', 'lowerarm_r', 'clavicle_l', 'clavicle_r', 'thigh_l', 'thigh_r'] + [b for b in ('ik_foot_l', 'ik_foot_r') if b in names])"),
    ("TRUNK = [b for b in UB if b not in ARMS]\n",
     "TRUNK = [b for b in UB if b not in ARMS]\n"
     "def _qavg(qs):\n"
     "    ref = qs[0]; acc = [0.0] * 4\n"
     "    for q in qs:\n"
     "        if sum(q[i] * ref[i] for i in range(4)) < 0: q = tuple(-x for x in q)\n"
     "        for i in range(4): acc[i] += q[i]\n"
     "    return ae.qnorm(tuple(acc))\n"
     "ARM_KEEP = float(cfg.get('arm_keep', 0.4)); ARM_FWD = float(cfg.get('arm_fwd', 7.0)); NECK_K = float(cfg.get('neck_k', 0.7))\n"),
    ("def build(fam, key):\n",
     "MEAN_F = {b: _qavg([FL.Lk[b][k][1] for k in range(FL.NK)]) for b in ARMS}; MEAN_R = {b: _qavg([RL.Lk[b][k][1] for k in range(RL.NK)]) for b in ARMS}\n"
     "MEAN_E = MEAN_X = None\n"
     "def build(fam, key):\n"),
]
c = dict(getattr(builtins, 'G236L', {}))
c.setdefault('t_first', 0.12); c.setdefault('catch_natural', True)
builtins.G231L = c
g = {'__name__': 'g236L', 'V236_SRC_PATCHES': PATCHES}
exec(compile(txt, 'gen231_loaded_v236.py', 'exec'), g)
