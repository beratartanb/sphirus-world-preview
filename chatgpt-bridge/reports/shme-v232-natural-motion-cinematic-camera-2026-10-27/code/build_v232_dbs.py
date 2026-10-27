"""build_v232_dbs.py (editor job): the V2.31 loaded databases rebuilt (build_v231_dbs LoadRev / SHM231L) with the V2.32 content: B_F loaded
bins (PSD_SHM231L_LoadRevBwd, 32 phases) and, in PSD_SHM231L_LoadRevFwd, the PRODUCTION F_B bin for every entry phase whose loaded design
fails the quality gate (P21 / P30: the catch plan double-lands the other foot) -> those phases enter the proven production reversal instead
of a neighbouring loaded bin with the wrong support foot. builtins.V232_DB = {'dry': bool, 'fallback': ['F_B_P21', 'F_B_P30']}."""
import builtins, io
c = dict(getattr(builtins, 'V232_DB', {}))
FB = c.get('fallback', ['F_B_P21', 'F_B_P30'])
src = io.open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V231_20261026/build_v231_dbs.py', encoding='utf8').read()
a = 'src = src.replace("seed = u.load_asset(", "PLAN = {k: [p for p in v if u.EditorAssetLibrary.does_asset_exist(p)] for k, v in PLAN.items()}" + chr(10) + "seed = u.load_asset(", 1)'
assert src.count(a) == 1
extra = ('"PLAN[\\"PSD_SHM231L_LoadRevFwd\\"] += [\'/Game/GraceRanger/SHME/Animations/V226/SHM226_JogRev_%s\' % k for k in ' + repr(FB) +
         ' if not u.EditorAssetLibrary.does_asset_exist(V + \'SHM231L_LoadRev_\' + k)]" + chr(10) + ')
b = a.replace('"PLAN = {k: [p for p in v if u.EditorAssetLibrary.does_asset_exist(p)] for k, v in PLAN.items()}" + chr(10) + ',
              '"PLAN = {k: [p for p in v if u.EditorAssetLibrary.does_asset_exist(p)] for k, v in PLAN.items()}" + chr(10) + ' + extra)
src = src.replace(a, b)
builtins.V231_DB = {'dry': bool(c.get('dry', True)), 'nph': 32, 'fam': 'LoadRev', 'tag': 'SHM231L'}
exec(compile(src, 'build_v232_dbs.py', 'exec'), {'__name__': 'b232'})
