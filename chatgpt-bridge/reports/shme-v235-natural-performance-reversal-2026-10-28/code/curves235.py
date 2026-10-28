"""curves235.py (editor job): the V2.27 / V2.28 clip curves on the V2.35 reversal clips (SHM235_JogRev_*): SHM226_Rev (remaining clip
seconds; the ABP reversal hold) and SHM226_V / SHM226_W (designed capsule speed + blend witness; the V2.28 clip-bound capsule). Same names as
production so the existing ABP consumers read them unchanged. Executes add_revcurve227.py and add_speedcurve228.py with the V235 clip list.
Prints REVCURVE227 {...} and SPEEDCURVE228 {...}."""
import io
R = r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/'
for f in ('SHME_V227_20261024/add_revcurve227.py', 'SHME_V228_20261025/add_speedcurve228.py'):
    s = io.open(R + f, encoding='utf8').read()
    for a, b in (("V = '/Game/GraceRanger/SHME/Animations/V226/'", "V = '/Game/GraceRanger/SHME/Animations/V235/'"),
                 ("V + 'SHM226_JogRev_%s_P%d'", "V + 'SHM235_JogRev_%s_P%d'")):
        assert s.count(a) == 1, (f, a); s = s.replace(a, b)
    exec(compile(s, f, 'exec'), {'__name__': 'c235'})
