"""curves236.py (editor job): the V2.27 / V2.28 clip curves on the V2.36 reversal clips: SHM226_Rev (remaining clip seconds, ABP reversal
hold) and SHM226_V / SHM226_W (designed capsule speed + blend witness, V2.28 clip-bound capsule) - same curve names as production so the
existing ABP consumers read them unchanged. builtins.V236_CURVES = {'prefix': 'SHM236_JogRev' | 'SHM236L_LoadRev', 'fams': [...], 'n': 32}.
Executes add_revcurve227.py and add_speedcurve228.py with the V236 clip list. Prints REVCURVE227 / SPEEDCURVE228."""
import io, builtins
c = dict(getattr(builtins, 'V236_CURVES', {})); PRE = c.get('prefix', 'SHM236_JogRev'); FAMS = c.get('fams', ['B_F', 'F_B']); NB = int(c.get('n', 32))
R = r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/'
for f in ('SHME_V227_20261024/add_revcurve227.py', 'SHME_V228_20261025/add_speedcurve228.py'):
    s = io.open(R + f, encoding='utf8').read()
    a = "V = '/Game/GraceRanger/SHME/Animations/V226/'"; assert s.count(a) == 1, (f, a); s = s.replace(a, "V = '/Game/GraceRanger/SHME/Animations/V236/'")
    import re
    m = re.search(r"CLIPS = \[V \+ 'SHM226_JogRev_%s_P%d' % \(f, k\) for f in \([^)]*\) for k in range\(\d+\)\]", s); assert m, f
    s = s.replace(m.group(0), "CLIPS = [V + '%s_%%s_P%%d' %% (f, k) for f in %r for k in range(%d)]" % (PRE, tuple(FAMS), NB))
    exec(compile(s, f, 'exec'), {'__name__': 'c236'})
