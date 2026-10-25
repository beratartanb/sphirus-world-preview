"""gen228_rev.py (editor job): regenerate the ten V2.26 reversal bins whose designed brake foot was ALREADY on the floor at the request frame
and was redirected 24-46 cm along the floor (a low shuffle FootPlacement turns into a 30 cm slide: P6 at 120 FPS / real time). Rule added to
gen226_rev.build(): if the chosen brake foot B is within 3 cm of the floor at tau0 it is treated as planted -> the OTHER foot (airborne,
landing next) becomes B and the touching foot becomes the pinned S. Everything else unchanged (same capsule table, same lengths).
Bins: B_F P6 P14, F_B P2 P6 P10 P13 P18 P26 P29 P30 (offline scan of clipfoot226.json). write() removes the notify tracks and curves of a
rewritten clip: run build_v226_revdbs.py (full windows) and add_revcurve227.py + add_speedcurve228.py afterwards. builtins.G228_DRY dry run.
Prints G228 {...} (per clip: B/S, tB, foot error, planted drift, penetration)."""
import builtins, io, json
SRC = r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V226_20261024/gen226_rev.py'
src = io.open(SRC, encoding='utf8').read()
old = "    B = 'l' if landt['l'] < landt['r'] else 'r'; S = 'r' if B == 'l' else 'l'\n"
new = ("    B = 'l' if landt['l'] < landt['r'] else 'r'; S = 'r' if B == 'l' else 'l'\n"
       "    if EL.rel(L0, 'ball_' + B)[0][2] < EL.BZ0[B] + 3.0: B, S = S, B   # V2.28: a foot already on the floor is not redirected along it\n")
assert old in src, 'B choice line not found'
src = src.replace(old, new)
ONLY = ['SHM226_JogRev_B_F_P6', 'SHM226_JogRev_B_F_P14', 'SHM226_JogRev_F_B_P2', 'SHM226_JogRev_F_B_P6', 'SHM226_JogRev_F_B_P10', 'SHM226_JogRev_F_B_P13', 'SHM226_JogRev_F_B_P18', 'SHM226_JogRev_F_B_P26', 'SHM226_JogRev_F_B_P29', 'SHM226_JogRev_F_B_P30']
builtins.G225 = {'dry_run': bool(getattr(builtins, 'G228_DRY', True)), 'nph': 32, 'only': ONLY, 'prof_table': r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Saved/Codex/SHME_V225_20261023/capsule_rev_table.json'}
g = {'__name__': 'g228'}
exec(compile(src, 'gen226_rev_v228.py', 'exec'), g)
out = g.get('out', {})
summ = {k: {kk: v.get(kk) for kk in ('B', 'S', 'tB', 'foot_err', 'planted_drift', 'penetration', 'saved', 'err')} for k, v in out.get('clips', {}).items()}
print('G228 ' + json.dumps({'dry': builtins.G225['dry_run'], 'clips': summ}, default=str))
