"""V2.25 SHME source patch T1b: no swing lift on a planted foot (feedback flicker fix).
Measured (v225t1 ter_bump_walk_o, 6.0-6.6 s): with the T1 gate (rise over the ground under the FOOT) the planted left foot before the
bump got lift 2-10 cm on alternate frames: the lift raised the foot -> ContactL false + a foot-speed spike -> 'swing' -> more lift; the
next contact frame released it fast (aCt) -> repeat. Ball z 2..13 cm vs V2.24 0..4 cm. Now the lift needs a CONFIRMED swing: the foot has
been out of contact for SwingAirT > 0.10 s (any contact frame resets the timer), so a one-frame contact drop can never start the loop."""
import pathlib
V1 = pathlib.Path(__file__).resolve().parents[2] / 'Tools/SHME_V1_20260925'
def patch(fname, old, new, marker):
    p = V1 / fname; t = p.read_bytes().decode('utf8')
    if marker in t: print(fname, marker, 'already'); return
    for nl in ('\n', '\r\n'):
        o = old.replace('\n', nl)
        if t.count(o) == 1: p.write_bytes(t.replace(o, new.replace('\n', nl)).encode('utf8')); print(fname, marker, 'patched'); return
    raise AssertionError((fname, marker))
patch('shm_component_vars.py', "('StepPrepPrevZ', F, 'SHM|V225'),", "('StepPrepPrevZ', F, 'SHM|V225'), ('SwingAirTL', F, 'SHM|V225'), ('SwingAirTR', F, 'SHM|V225'),", 'SwingAirTL')
OLD = ("  (bind swL (and slOn (and (not ContactL) (> FootSpeedL (R SwingLiftMinSpeed)))))\n"
       "  (bind swR (and slOn (and (not ContactR) (> FootSpeedR (R SwingLiftMinSpeed)))))\n")
NEW = ("  ; V2.25 T1b: lift only in a CONFIRMED swing (> 0.10 s out of contact): a planted foot whose contact flag drops for a frame never lifts\n"
       "  (set SwingAirTL (select ContactL 0.0 (min 1.0 (+ SwingAirTL dt))))\n"
       "  (set SwingAirTR (select ContactR 0.0 (min 1.0 (+ SwingAirTR dt))))\n"
       "  (bind swL (and slOn (and (> SwingAirTL 0.10) (> FootSpeedL (R SwingLiftMinSpeed)))))\n"
       "  (bind swR (and slOn (and (> SwingAirTR 0.10) (> FootSpeedR (R SwingLiftMinSpeed)))))\n")
patch('shm_src.py', OLD, NEW, 'V2.25 T1b')
print('done')
