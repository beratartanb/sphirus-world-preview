"""gen236_rev.py (editor job): V2.36 jog reversal = the V2.35 support exchange (feet, capsule profile and timing UNCHANGED) + the whole-body
brake the user asked for (V2.35 review: the legs brake while the arms keep running in jog carriage, the trunk stays rigid).
Source = gen226_rev.py with the V2.35 patches (gen235_rev.py) + V2.36 upper-body patches:
  * arms: the entry -> exit hand-over keeps its clock, but inside the brake window (B's plant -> S's catch landing) the swing AMPLITUDE about the
    loops' mean carriage drops to ARM_KEEP (no mechanical jog swing during the brake), and the upper arms carry a short inertial swing toward the
    OLD travel (ARM_FWD deg; forward for F_B, backward for B_F) that resolves before the push;
  * head: the brake / push trunk lean (BRAKE_DEG / PUSH_DEG at spine_01) is countered at neck_01 by NECK_K so the head stays level;
  * trunk lean values from builtins (defaults as V2.35).
Output: /Game/GraceRanger/SHME/Animations/V236/SHM236_JogRev_{B_F,F_B}_P<k>. builtins.G236R = {'dry_run': True, 'only': [...], 'fam': [...],
'nph': 32, 'arm_keep': 0.4, 'arm_fwd': 6.0, 'neck_k': 0.7}. Stick JSON per clip to Saved/Codex/SHME_V236_20261028/stick/. Prints G236R {...}."""
import builtins, io, json
SRC = r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V226_20261024/gen226_rev.py'
src = io.open(SRC, encoding='utf8').read()
def rep(old, new, n=1):
    global src
    assert src.count(old) == n, ('patch anchor', old[:60], src.count(old))
    src = src.replace(old, new)
# ---- V2.35 patches (identical to gen235_rev.py)
rep("    B = 'l' if landt['l'] < landt['r'] else 'r'; S = 'r' if B == 'l' else 'l'\n",
    "    B = 'l' if landt['l'] < landt['r'] else 'r'; S = 'r' if B == 'l' else 'l'\n"
    "    if EL.rel(L0, 'ball_' + B)[0][2] < EL.BZ0[B] + 3.0: B, S = S, B   # V2.28: a foot already on the floor is not redirected along it\n")
rep("    tS = max(tz + T_FIRST, tS_lift + 0.22, tB + 0.10)\n", "    tS = max(tz + T_FIRST, tS_lift + 0.22, tB + 0.12)   # V2.35: catch / first step at the zero crossing\n")
rep("    tRedir = max(tS_lift, tB - REDIR_LEAD)\n", "    tRedir = tS_lift if s_planted0 else (0.0 if EL.rel(L0, 'ball_' + S)[0][2] < EL.BZ0[S] + 3.0 else max(tS_lift, tB - REDIR_LEAD))\n")
# ---- V2.36 output names
rep("OUTDIR = '/Game/GraceRanger/SHME/Animations/V226'", "OUTDIR = '/Game/GraceRanger/SHME/Animations/V236'")
rep("        name = 'SHM226_JogRev_%s_P%d' % (fam, k)\n", "        name = 'SHM236_JogRev_%s_P%d' % (fam, k)\n")
rep("(P / 'Saved/Codex/SHME_V226_20261024' / ('gen226_rev_%s.json'", "(P / 'Saved/Codex/SHME_V236_20261028' / ('gen236_rev_%s.json'")
rep("    try: c.open_bracket(u.Text('SHME V2.25 authored reversal ' + name), True)\n", "    try: c.open_bracket(u.Text('SHME V2.36 whole-body reversal ' + name), True)\n")
# ---- V2.36 whole-body brake: arm amplitude in the brake window + inertial arm swing toward the old travel + neck counter
rep("        for b in ARMS: pose[b] = (lerp(Le[b][0], Lx[b][0], wA), slerp(Le[b][1], Lx[b][1], wA), lerp(Le[b][2], Lx[b][2], wA))\n",
    "        keep = 1.0 - (1.0 - ARM_KEEP) * bell(t, tB - 0.15, tS + 0.35)\n"
    "        for b in ARMS:\n"
    "            q_ = slerp(Le[b][1], Lx[b][1], wA); m_ = slerp(MEAN_E[b], MEAN_X[b], wA)\n"
    "            pose[b] = (lerp(Le[b][0], Lx[b][0], wA), slerp(m_, q_, keep), lerp(Le[b][2], Lx[b][2], wA))\n")
rep("        if abs(a) > 1e-3: ae.apply_bone_delta(clip, local, 'spine_01', f, ae.qaxis(lat, -a))\n",
    "        if abs(a) > 1e-3:\n"
    "            ae.apply_bone_delta(clip, local, 'spine_01', f, ae.qaxis(lat, -a)); ae.apply_bone_delta(clip, local, 'neck_01', f, ae.qaxis(lat, a * NECK_K))\n"
    "        fw = -sgn * ARM_FWD * bell(t, tB - 0.06, tB + 0.34)\n"
    "        if abs(fw) > 1e-3:\n"
    "            for s_ in ('l', 'r'): ae.apply_bone_delta(clip, local, 'upperarm_' + s_, f, ae.qaxis(lat, fw))\n"
    "        el = ELBOW * bell(t, tB - 0.10, tS + 0.30)\n"
    "        if el > 1e-3:\n"
    "            for s_ in ('l', 'r'): ae.apply_bone_delta(clip, local, 'lowerarm_' + s_, f, ae.qaxis(lat, -el))\n")
rep("TRUNK = [b for b in UB if b not in ARMS]\n",
    "TRUNK = [b for b in UB if b not in ARMS]\n"
    "def _qavg(qs):\n"
    "    ref = qs[0]; acc = [0.0] * 4\n"
    "    for q in qs:\n"
    "        if sum(q[i] * ref[i] for i in range(4)) < 0: q = tuple(-x for x in q)\n"
    "        for i in range(4): acc[i] += q[i]\n"
    "    return ae.qnorm(tuple(acc))\n"
    "ARM_KEEP = float(cfg.get('arm_keep', 0.4)); ARM_FWD = float(cfg.get('arm_fwd', 6.0)); ELBOW = float(cfg.get('elbow', 18.0)); NECK_K = float(cfg.get('neck_k', 0.7))\n")
# loop means need the Loop objects: insert after the loops exist (FL / RL)
rep("def build(fam, key):\n",
    "MEAN_F = {b: _qavg([FL.Lk[b][k][1] for k in range(FL.NK)]) for b in ARMS}; MEAN_R = {b: _qavg([RL.Lk[b][k][1] for k in range(RL.NK)]) for b in ARMS}\n"
    "def build(fam, key):\n"
    "    global MEAN_E, MEAN_X\n"
    "    MEAN_E, MEAN_X = (MEAN_R, MEAN_F) if fam == 'B_F' else (MEAN_F, MEAN_R)\n")
rep("'head', 'neck_01', 'spine_05', 'spine_03', 'spine_01'] + [b for b in ('ik_foot_l', 'ik_foot_r') if b in names])",
    "'head', 'neck_01', 'spine_05', 'spine_03', 'spine_01', 'hand_l', 'hand_r', 'upperarm_l', 'upperarm_r', 'lowerarm_l', 'lowerarm_r', 'clavicle_l', 'clavicle_r', 'thigh_l', 'thigh_r'] + [b for b in ('ik_foot_l', 'ik_foot_r') if b in names])")
rep("    return local, info\ndef write(", "    _STICK['SHM236_JogRev_%s_P%d' % (fam, key)] = (local, clip)\n    return local, info\n_STICK = {}\ndef write(")
c = dict(getattr(builtins, 'G236R', {}))
builtins.G225 = {'dry_run': bool(c.get('dry_run', True)), 'nph': int(c.get('nph', 32)), 'only': c.get('only'), 'fam': c.get('fam', ['B_F', 'F_B']),
                 't_first': float(c.get('t_first', -0.04)), 'brake_deg': float(c.get('brake_deg', 4.0)), 'push_deg': float(c.get('push_deg', 3.0)),
                 'tail': float(c.get('tail', 0.20)), 'brake_behind': float(c.get('brake_behind', 10.0)), 'dip_cm': float(c.get('dip_cm', 2.5)),
                 'arm_keep': float(c.get('arm_keep', 0.25)), 'arm_fwd': float(c.get('arm_fwd', 9.0)), 'neck_k': float(c.get('neck_k', 0.7)), 'elbow': float(c.get('elbow', 18.0)),
                 'prof_table': r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Saved/Codex/SHME_V235_20261028/capsule_rev235.json'}
g = {'__name__': 'g236r'}
exec(compile(src, 'gen226_rev_v236.py', 'exec'), g)
out = g.get('out', {})
# stick data for the source review (only the clips built in this call)
import pathlib
SD = pathlib.Path(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Saved/Codex/SHME_V236_20261028/stick'); SD.mkdir(parents=True, exist_ok=True)
for name, (local, clip) in g.get('_STICK', {}).items():
    SB = ['pelvis', 'spine_03', 'spine_05', 'neck_01', 'head', 'clavicle_l', 'upperarm_l', 'lowerarm_l', 'hand_l', 'clavicle_r', 'upperarm_r', 'lowerarm_r', 'hand_r',
          'thigh_l', 'calf_l', 'foot_l', 'ball_l', 'thigh_r', 'calf_r', 'foot_r', 'ball_r']
    n = len(local['root'])
    (SD / (name + '.json')).write_text(json.dumps({'name': name, 'dt': 1.0 / 30.0, 'bones': SB, 'frames': [[[round(x, 1) for x in clip.comp(b, f, local)[0]] for b in SB] for f in range(n)]}))
summ = {k: {kk: v.get(kk) for kk in ('B', 'S', 'tB', 'tz', 'tS', 'tS_lift', 'len', 'foot_err', 'planted_drift', 'penetration', 'entry_err', 'exit_err', 'steps', 'saved', 'err')}
        for k, v in out.get('clips', {}).items()}
print('G236R ' + json.dumps({'dry': builtins.G225['dry_run'], 'clips': summ}, default=str))
