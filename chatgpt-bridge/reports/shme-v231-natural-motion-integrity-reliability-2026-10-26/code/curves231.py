"""curves231.py (editor job): clip clock (SHM226_Rev) + designed speed (SHM226_V / SHM226_W) curves on a V2.31 authored family - the same
curve NAMES as production (the ABP hold / clip-bound capsule read them), the V2.27 / V2.28 tools with the V2.31 clip list.
builtins.V231_CURVE = {'dry': bool, 'prefix': 'SHM231S_SlowRev_', 'nph': 16}."""
import builtins, io
c = dict(getattr(builtins, 'V231_CURVE', {})); dry = bool(c.get('dry', True)); pre = c.get('prefix', 'SHM231S_SlowRev_'); nph = int(c.get('nph', 16))
for path, flag in ((r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V227_20261024/add_revcurve227.py', 'V227_CURVE_DRY'),
                   (r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V228_20261025/add_speedcurve228.py', 'V228_CURVE_DRY')):
    src = io.open(path, encoding='utf8').read()
    cl = "CLIPS = [V + 'SHM226_JogRev_%s_P%d' % (f, k) for f in ('B_F', 'F_B') for k in range(32)]"
    assert "V = '/Game/GraceRanger/SHME/Animations/V226/'" in src and cl in src, path
    src = src.replace("V = '/Game/GraceRanger/SHME/Animations/V226/'", "V = '/Game/GraceRanger/SHME/Animations/V231/'")
    src = src.replace(cl, "import unreal as _u" + chr(10) + "CLIPS = [c for c in [V + '%s%%s_P%%d' %% (f, k) for f in ('B_F', 'F_B') for k in range(%d)] if _u.EditorAssetLibrary.does_asset_exist(c)]" % (pre, nph), 1)
    setattr(builtins, flag, dry)
    exec(compile(src, path.rsplit('/', 1)[-1] + '_231', 'exec'), {'__name__': 'c231'})
