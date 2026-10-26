"""add_curves230L.py (editor job): the clip clock (SHM226_Rev) and designed-speed (SHM226_V / SHM226_W) curves on the loaded family - same curve
NAMES as production (the ABP reads them), the V2.27 / V2.28 tools with the V230L clip list. builtins.V230L_CURVE_DRY prints only."""
import builtins, io
dry = bool(getattr(builtins, 'V230L_CURVE_DRY', True))
for path, flag in ((r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V227_20261024/add_revcurve227.py', 'V227_CURVE_DRY'),
                   (r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V228_20261025/add_speedcurve228.py', 'V228_CURVE_DRY')):
    src = io.open(path, encoding='utf8').read()
    for a, b in (("V = '/Game/GraceRanger/SHME/Animations/V226/'", "V = '/Game/GraceRanger/SHME/Animations/V230L/'"), ("'SHM226_JogRev_%s_P%d'", "'SHM230L_JogRev_%s_P%d'")):
        assert a in src, (path, a); src = src.replace(a, b)
    cl = "CLIPS = [V + 'SHM230L_JogRev_%s_P%d' % (f, k) for f in ('B_F', 'F_B') for k in range(32)]"
    assert cl in src, path
    src = src.replace(cl, cl + chr(10) + "import unreal as _u" + chr(10) + "CLIPS = [c for c in CLIPS if _u.EditorAssetLibrary.does_asset_exist(c)]", 1)
    setattr(builtins, flag, dry)
    exec(compile(src, path.rsplit('/', 1)[-1] + '_230L', 'exec'), {'__name__': 'c230L'})
