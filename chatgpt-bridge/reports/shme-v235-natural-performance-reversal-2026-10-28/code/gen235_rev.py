"""gen235_rev.py (editor job): V2.35 jog reversal = ONE continuous support exchange (no held double-support pose).
Diagnosis (diag235 + sheet235 on the V2.34 production capture j30_rel_3200): the production F_B clip SHM226_JogRev_F_B_P14 advances at clip
rate 1.0 but both feet stay planted 0.64 s (5.20 -> 5.87 s) with the arms in jog carriage = the visible freeze. Owner = the V2.25/26
generator's plan: the capsule table (measured V2.24 production) lingers below 40 cm/s for ~0.3 s after the zero crossing, and the first step
of the new travel (S) was designed to land T_FIRST 0.40 s AFTER the zero crossing, so S hovers in a 0.6 s slow swing while B is planted.
V2.35 plan (same footstep machinery as gen226_rev.py + the V2.28 'B already on the floor' rule, executed from its source with patches):
  * capsule = DESIGNED profile (Saved/Codex/SHME_V235_20261028/capsule_rev235.json): brake at 800 cm/s^2 (0.05 s onset), the push continues
    THROUGH the zero crossing at 550 (F_B, backpedal) / 650 (B_F, forward) cm/s^2, first-order approach above half the exit speed; no dwell.
  * S = the catch / first step of the new travel: lands at the zero crossing - 0.04 s (or its natural swing minimum 0.22 s after its toe-off,
    or 0.12 s after the brake plant) under the reversing body; B (the brake foot) then pushes and lifts on the exit loop's clock.
  * the arm / trunk hand-over and the absorb dip follow the shorter brake -> catch timeline automatically.
Output: /Game/GraceRanger/SHME/Animations/V235/SHM235_JogRev_{B_F,F_B}_P<k> (32 bins each, new assets). builtins.G235 = {'dry_run': True,
'only': [...], 'fam': [...], 't_first': -0.04, 'nph': 32}. Afterwards: curves235.py (SHM226_Rev / SHM226_V / SHM226_W), build235_dbs.py.
Prints G235 {...} (per clip: B/S, tB, tz, tS, foot error, planted drift, penetration, steps)."""
import builtins, io, json
SRC = r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V226_20261024/gen226_rev.py'
src = io.open(SRC, encoding='utf8').read()
def rep(old, new, n=1):
    global src
    assert src.count(old) == n, ('patch anchor', old[:60], src.count(old))
    src = src.replace(old, new)
rep("    B = 'l' if landt['l'] < landt['r'] else 'r'; S = 'r' if B == 'l' else 'l'\n",
    "    B = 'l' if landt['l'] < landt['r'] else 'r'; S = 'r' if B == 'l' else 'l'\n"
    "    if EL.rel(L0, 'ball_' + B)[0][2] < EL.BZ0[B] + 3.0: B, S = S, B   # V2.28: a foot already on the floor is not redirected along it\n")
rep("    tS = max(tz + T_FIRST, tS_lift + 0.22, tB + 0.10)\n", "    tS = max(tz + T_FIRST, tS_lift + 0.22, tB + 0.12)   # V2.35: catch / first step at the zero crossing\n")
# V2.35: a planted S leaves at its natural toe-off (pinned up to the redirect it overreached 11 cm); a touching-down S is redirected at once
# (the loop shape landed it under the braking root and it slid 33 cm, F_B_P18; pinning it instead waited for its next toe-off = 0.95 s hold)
rep("    tRedir = max(tS_lift, tB - REDIR_LEAD)\n", "    tRedir = tS_lift if s_planted0 else (0.0 if EL.rel(L0, 'ball_' + S)[0][2] < EL.BZ0[S] + 3.0 else max(tS_lift, tB - REDIR_LEAD))\n")
rep("OUTDIR = '/Game/GraceRanger/SHME/Animations/V226'", "OUTDIR = '/Game/GraceRanger/SHME/Animations/V235'")
rep("        name = 'SHM226_JogRev_%s_P%d' % (fam, k)\n", "        name = 'SHM235_JogRev_%s_P%d' % (fam, k)\n")
rep("(P / 'Saved/Codex/SHME_V226_20261024' / ('gen226_rev_%s.json'", "(P / 'Saved/Codex/SHME_V235_20261028' / ('gen235_rev_%s.json'")
rep("    try: c.open_bracket(u.Text('SHME V2.25 authored reversal ' + name), True)\n", "    try: c.open_bracket(u.Text('SHME V2.35 support-exchange reversal ' + name), True)\n")
c = dict(getattr(builtins, 'G235', {}))
builtins.G225 = {'dry_run': bool(c.get('dry_run', True)), 'nph': int(c.get('nph', 32)), 'only': c.get('only'), 'fam': c.get('fam', ['B_F', 'F_B']),
                 't_first': float(c.get('t_first', -0.04)), 'brake_behind': float(c.get('brake_behind', 10.0)), 'dip_cm': float(c.get('dip_cm', 2.5)),
                 'brake_deg': float(c.get('brake_deg', 4.0)), 'push_deg': float(c.get('push_deg', 3.0)), 'tail': float(c.get('tail', 0.20)),
                 'prof_table': r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Saved/Codex/SHME_V235_20261028/capsule_rev235.json'}
g = {'__name__': 'g235'}
exec(compile(src, 'gen226_rev_v235.py', 'exec'), g)
out = g.get('out', {})
summ = {k: {kk: v.get(kk) for kk in ('B', 'S', 'tB', 'tz', 'tS', 'tS_lift', 'len', 'foot_err', 'planted_drift', 'penetration', 'entry_err', 'exit_err', 'steps', 'saved', 'err')}
        for k, v in out.get('clips', {}).items()}
print('G235 ' + json.dumps({'dry': builtins.G225['dry_run'], 'clips': summ}, default=str))
