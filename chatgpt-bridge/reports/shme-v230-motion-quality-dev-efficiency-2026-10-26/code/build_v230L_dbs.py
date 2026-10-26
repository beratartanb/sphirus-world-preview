"""build_v230L_dbs.py (editor job): PSD_SHM230L_JogRevBwd / _Fwd for the loaded family = build_v226_revdbs.py with the V230L names, full BranchIn
windows (V2.25 entry-window trap) and 32 bins. builtins.V230L_DB_DRY prints only."""
import builtins, io
src = io.open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V226_20261024/build_v226_revdbs.py', encoding='utf8').read()
for a, b in (("V = '/Game/GraceRanger/SHME/Animations/V226/'", "V = '/Game/GraceRanger/SHME/Animations/V230L/'"), ('PSD_SHM226_', 'PSD_SHM230L_'),
             ('SHM226_JogRev_', 'SHM230L_JogRev_'), ("'SHME_V226_'", "'SHME_V230L_'")):
    assert a in src, a; src = src.replace(a, b)
builtins.V226_DRY = bool(getattr(builtins, 'V230L_DB_DRY', True)); builtins.V226_ENTRY = 100.0; builtins.V226_NPH = 32
# only the bins that passed the generation gate exist (loaded_good.json): drop missing clips from the plan
import unreal as _u
_P = "PLAN = {'PSD_SHM226_JogRevBwd'"
assert src.count("PLAN = {") == 1
src = src.replace("seed = u.load_asset(", "PLAN = {k: [p for p in v if u.EditorAssetLibrary.does_asset_exist(p)] for k, v in PLAN.items()}" + chr(10) + "seed = u.load_asset(", 1)
exec(compile(src, 'build_v230L_dbs.py', 'exec'), {'__name__': 'b230L'})
