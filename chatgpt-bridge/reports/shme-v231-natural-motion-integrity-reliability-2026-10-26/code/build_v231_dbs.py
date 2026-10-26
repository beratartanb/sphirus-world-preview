"""build_v231_dbs.py (editor job): PSD_SHM231S_SlowRevBwd (B_F slow bins + rear loops) / _Fwd (F_B slow bins + rear loops) = build_v226_revdbs.py
with the V2.31 names, full BranchIn windows (V2.25 entry-window trap) and the bins that exist. builtins.V231_DB = {'dry': bool, 'nph': 16}."""
import builtins, io
c = dict(getattr(builtins, 'V231_DB', {}))
src = io.open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V226_20261024/build_v226_revdbs.py', encoding='utf8').read()
FAM = c.get('fam', 'SlowRev'); TAGP = c.get('tag', 'SHM231S')   # SlowRev / SHM231S (low-speed) or LoadRev / SHM231L (loaded)
for a, b in (("V = '/Game/GraceRanger/SHME/Animations/V226/'", "V = '/Game/GraceRanger/SHME/Animations/V231/'"), ('PSD_SHM226_JogRev', 'PSD_%s_%s' % (TAGP, FAM)),
             ('SHM226_JogRev_', '%s_%s_' % (TAGP, FAM)), ("'SHME_V226_'", "'SHME_V231%s_'" % TAGP[-1]), ("n.replace('PSD_SHM226_', '')", "n.replace('PSD_%s_', '')" % TAGP)):
    assert a in src, a; src = src.replace(a, b)
src = src.replace("win = ln if 'JogRev' not in c else min(ENTRY, ln - 0.01)", "win = ln if '%s' not in c else min(ENTRY, ln - 0.01)" % FAM)
builtins.V226_DRY = bool(c.get('dry', True)); builtins.V226_ENTRY = 100.0; builtins.V226_NPH = int(c.get('nph', 16))
assert src.count("PLAN = {") == 1
src = src.replace("seed = u.load_asset(", "PLAN = {k: [p for p in v if u.EditorAssetLibrary.does_asset_exist(p)] for k, v in PLAN.items()}" + chr(10) + "seed = u.load_asset(", 1)
exec(compile(src, 'build_v231_dbs.py', 'exec'), {'__name__': 'b231'})
