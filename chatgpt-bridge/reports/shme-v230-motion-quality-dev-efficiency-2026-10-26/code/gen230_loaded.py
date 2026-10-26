"""gen230_loaded.py (editor job): V2.30 LOADED authored reversal family (effort -> body). Same character generator as production (gen226_rev +
the V2.28 planted-brake-foot rule), different designed physics: a body that has spent its short-term effort brakes a little longer (lower
designed deceleration), lands the first step a little later, absorbs a little deeper over the brake plant and pushes off smaller and
slower (lower re-push acceleration, smaller push lean) - one support step more before the loop speed, no slow motion (the brake runs on
the loop's natural cadence, the re-push on the rate-floored clock as in production). Output /Game/GraceRanger/SHME/Animations/V230L/
SHM230L_JogRev_<fam>_P<k> (32 phase bins x 2 families). builtins.G230L = {'dry_run', 'only', 'scale'}; prints G230L {...}."""
import builtins, io, json
SRC = r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V226_20261024/gen226_rev.py'
src = io.open(SRC, encoding='utf8').read()
REPL = [("OUTDIR = '/Game/GraceRanger/SHME/Animations/V226'", "OUTDIR = '/Game/GraceRanger/SHME/Animations/V230L'"),
        ("name = 'SHM226_JogRev_%s_P%d' % (fam, k)", "name = 'SHM230L_JogRev_%s_P%d' % (fam, k)"),
        ("(P / 'Saved/Codex/SHME_V226_20261024' / ('gen226_rev_%s.json'", "(P / 'Saved/Codex/SHME_V230_20261026' / ('gen230L_rev_%s.json'"),
        ("    B = 'l' if landt['l'] < landt['r'] else 'r'; S = 'r' if B == 'l' else 'l'\n",
         "    B = 'l' if landt['l'] < landt['r'] else 'r'; S = 'r' if B == 'l' else 'l'\n    if EL.rel(L0, 'ball_' + B)[0][2] < EL.BZ0[B] + 3.0: B, S = S, B   # V2.28 rule\n")]
for a, b in REPL:
    assert src.count(a) == 1, a[:50]
    src = src.replace(a, b)
c = dict(getattr(builtins, 'G230L', {})); k = float(c.get('scale', 1.0))
# production (measured) profile: B_F 245 -> 0 at ~720 cm/s2, push 261 to 300; F_B 300 -> 0 at ~680, push 198 to 245. Loaded (k = 1): brake x0.83,
# push x0.70; first step +0.06 s; absorb dip 3.5 cm; brake counter-lean 5 deg; push lean 2 deg.
prof = {'B_F': {'v0': 245.0, 'brake': 720.0 * (1 - 0.17 * k), 'push': 261.0 * (1 - 0.30 * k), 'vexit': 300.0},
        'F_B': {'v0': 300.0, 'brake': 680.0 * (1 - 0.17 * k), 'push': 198.0 * (1 - 0.30 * k), 'vexit': 245.0}}
# measured production capsule table (V2.25), time-stretched: the brake part (old travel, v < 0) by 1 / (1 - 0.17 k), the re-push part by
# 1 / (1 - 0.30 k) - same shape, slower tempo (the production family was generated from this table; analytic ramps gave more foot error)
import math as _m
TAB = json.load(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Saved/Codex/SHME_V225_20261023/capsule_rev_table.json'))
LT = {}
for fam_, t_ in TAB.items():
    dt_ = t_['dt']; v_ = list(t_['v']); n_ = len(v_)
    # canonical in gen226: tab = -v (old travel negative). Find the zero crossing index in that sign convention
    tab_ = [-x for x in v_]; iz = next((i for i in range(1, n_) if tab_[i - 1] < 0 <= tab_[i]), n_ // 2)
    sb, sp = 1.0 / (1 - 0.17 * k), 1.0 / (1 - 0.30 * k)
    def sample(tt):
        kk = tt / dt_; i = int(kk); w = kk - i
        if i >= n_ - 1: return v_[-1]
        return v_[i] * (1 - w) + v_[i + 1] * w
    tz = iz * dt_; out_v = []; T = 0.0; tend = tz * sb + (n_ - 1 - iz) * dt_ * sp
    while T <= tend + 1e-9:
        src_t = T / sb if T <= tz * sb else tz + (T - tz * sb) / sp
        out_v.append(sample(src_t)); T += dt_
    LT[fam_] = {'dt': dt_, 'v': out_v}
LTP = r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Saved/Codex/SHME_V230_20261026/capsule_rev_table_loaded.json'
open(LTP, 'w').write(json.dumps(LT))
builtins.G225 = {'dry_run': bool(c.get('dry_run', True)), 'nph': 32, 'only': c.get('only'), 'prof_table': LTP, 't_first': 0.40 + 0.06 * k,
                 'dip_cm': 2.5 + 1.0 * k, 'brake_deg': 4.0 + 1.0 * k, 'push_deg': 3.0 - 1.0 * k, 'tail': 0.30}
g = {'__name__': 'g230L'}
exec(compile(src, 'gen226_rev_v230L.py', 'exec'), g)
out = g.get('out', {})
summ = {n: {kk: v.get(kk) for kk in ('B', 'S', 'tB', 'len', 'foot_err', 'planted_drift', 'penetration', 'steps', 'saved', 'err')} for n, v in out.get('clips', {}).items()}
print('G230L ' + json.dumps({'dry': builtins.G225['dry_run'], 'prof': prof, 'clips': summ}, default=str))
