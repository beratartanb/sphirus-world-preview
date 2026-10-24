"""V2.26 SHME source patch T3d (replaces the T3c swing condition): a foot INSIDE a platform is lifted to the platform, not released.
Measured (v226t3 ter_drop_walk, frames 11.97-12.07): the lift (17.9) was released to 5.9 the frame ContactR turned true - the foot was slow
and, measured against the LOCAL ground (28), 'low' (ball 18.4 = 10 cm inside the box) so the contact rule counted it as planted and the
fast contact release (aCt) dropped the lift; FootPlacement then popped the foot out. The T3c speed OR cannot help: the swing-confirmation
timer resets on contact.
T3d: penetration term per foot: penL = (platform under the foot above the support ground) AND (foot centre below local ground + 3 cm);
lift target = max(swing term (T1/T1b/T3a as before), penetration term = local ground + 7.5 - foot centre); in contact the fast release
applies only when the foot is NOT penetrating. The foot is carried to the platform top (not above it: no hover); FootPlacement plants it there."""
import pathlib
V1 = pathlib.Path(__file__).resolve().parents[2] / 'Tools/SHME_V1_20260925'
def patch(fname, old, new, marker):
    p = V1 / fname; t = p.read_bytes().decode('utf8')
    if marker in t: print(fname, marker, 'already'); return
    for nl in ('\n', '\r\n'):
        o = old.replace('\n', nl)
        if t.count(o) == 1: p.write_bytes(t.replace(o, new.replace('\n', nl)).encode('utf8')); print(fname, marker, 'patched'); return
    raise AssertionError((fname, marker))
OLD1 = ("  (bind swL (and slOn (and (> SwingAirTL 0.10) (or (> FootSpeedL (R SwingLiftMinSpeed)) (> (- guL g0) (R SwingLiftRiseMin))))))\n"
        "  (bind swR (and slOn (and (> SwingAirTR 0.10) (or (> FootSpeedR (R SwingLiftMinSpeed)) (> (- guR g0) (R SwingLiftRiseMin))))))\n")
NEW1 = ("  (bind swL (and slOn (and (> SwingAirTL 0.10) (> FootSpeedL (R SwingLiftMinSpeed)))))\n"
        "  (bind swR (and slOn (and (> SwingAirTR 0.10) (> FootSpeedR (R SwingLiftMinSpeed)))))\n"
        "  ; V2.26 T3d: a foot inside a platform the body has not climbed (local ground above the support ground, foot centre below it)\n"
        "  (bind penL (and slOn (and (> (- guL g0) (R SwingLiftRiseMin)) (< (.z FootCenterL) (+ guL 3.0)))))\n"
        "  (bind penR (and slOn (and (> (- guR g0) (R SwingLiftRiseMin)) (< (.z FootCenterR) (+ guR 3.0)))))\n")
patch('shm_src.py', OLD1, NEW1, 'V2.26 T3d: a foot inside')
OLD2 = ("  (bind tL (select swL (* wRL (clamp (- (+ gL (R SwingLiftMargin)) (.z FootCenterL)) 0.0 (R SwingLiftMax))) 0.0))\n"
        "  (bind tR (select swR (* wRR (clamp (- (+ gRt (R SwingLiftMargin)) (.z FootCenterR)) 0.0 (R SwingLiftMax))) 0.0))\n")
NEW2 = ("  (bind tL (max (select swL (* wRL (clamp (- (+ gL (R SwingLiftMargin)) (.z FootCenterL)) 0.0 (R SwingLiftMax))) 0.0) (select penL (clamp (- (+ guL 7.5) (.z FootCenterL)) 0.0 (R SwingLiftMax)) 0.0)))   ; V2.26 T3d\n"
        "  (bind tR (max (select swR (* wRR (clamp (- (+ gRt (R SwingLiftMargin)) (.z FootCenterR)) 0.0 (R SwingLiftMax))) 0.0) (select penR (clamp (- (+ guR 7.5) (.z FootCenterR)) 0.0 (R SwingLiftMax)) 0.0)))\n")
patch('shm_src.py', OLD2, NEW2, 'V2.26 T3d\n')
OLD3 = ("  (set SwingLiftL (select slOn (+ SwingLiftL (* (- tL SwingLiftL) (select (> tL SwingLiftL) aUp (select ContactL aCt aDn)))) 0.0))\n"
        "  (set SwingLiftR (select slOn (+ SwingLiftR (* (- tR SwingLiftR) (select (> tR SwingLiftR) aUp (select ContactR aCt aDn)))) 0.0))\n")
NEW3 = ("  (set SwingLiftL (select slOn (+ SwingLiftL (* (- tL SwingLiftL) (select (> tL SwingLiftL) aUp (select (and ContactL (not penL)) aCt aDn)))) 0.0))   ; V2.26 T3d: no fast release while penetrating\n"
        "  (set SwingLiftR (select slOn (+ SwingLiftR (* (- tR SwingLiftR) (select (> tR SwingLiftR) aUp (select (and ContactR (not penR)) aCt aDn)))) 0.0))\n")
patch('shm_src.py', OLD3, NEW3, 'V2.26 T3d: no fast release')
print('done')
