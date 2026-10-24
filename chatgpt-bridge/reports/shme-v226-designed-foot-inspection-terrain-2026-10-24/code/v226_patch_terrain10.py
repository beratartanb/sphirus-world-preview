"""V2.26 SHME source patch T3g: the lift target was computed against the ALREADY-LIFTED foot (half convergence).
Measured: the platform-plant lift settled at 17.4 cm for a 34 cm deficit (28 cm top + 7.5 - pose ball ~1), and on the bumps the V2.24
lift settled near half the rise. Cause: tL = ground + margin - FootCenter.z where FootCenter is the final (post-lift) foot, so the
equilibrium is L = (deficit)/2. Now both terms use the pose foot without the applied lift (FootCenter.z - SwingLiftL): L = deficit.
With the full deficit the swing margin is a real clearance; the production value 10.5 (tuned on the halved lift) becomes 6 (promotion /
candidate flag SwingLiftMargin), so a 20 cm bump gets ~6 cm of clearance instead of ~0-3."""
import pathlib
V1 = pathlib.Path(__file__).resolve().parents[2] / 'Tools/SHME_V1_20260925'
def patch(fname, old, new, marker):
    p = V1 / fname; t = p.read_bytes().decode('utf8')
    if marker in t: print(fname, marker, 'already'); return
    for nl in ('\n', '\r\n'):
        o = old.replace('\n', nl)
        if t.count(o) == 1: p.write_bytes(t.replace(o, new.replace('\n', nl)).encode('utf8')); print(fname, marker, 'patched'); return
    raise AssertionError((fname, marker))
OLD = ("  (bind tL (max (select swL (* wRL (clamp (- (+ gL (R SwingLiftMargin)) (.z FootCenterL)) 0.0 (R SwingLiftMax))) 0.0) (select penL (clamp (- (+ guL 7.5) (.z FootCenterL)) 0.0 (R StepPenLiftMax)) 0.0)))   ; V2.26 T3d/T3e\n"
       "  (bind tR (max (select swR (* wRR (clamp (- (+ gRt (R SwingLiftMargin)) (.z FootCenterR)) 0.0 (R SwingLiftMax))) 0.0) (select penR (clamp (- (+ guR 7.5) (.z FootCenterR)) 0.0 (R StepPenLiftMax)) 0.0)))\n")
NEW = ("  ; V2.26 T3g: targets against the POSE foot (final foot minus the lift already applied) - the old form converged to half the deficit\n"
       "  (bind fzL (- (.z FootCenterL) SwingLiftL))\n"
       "  (bind fzR (- (.z FootCenterR) SwingLiftR))\n"
       "  (bind tL (max (select swL (* wRL (clamp (- (+ gL (R SwingLiftMargin)) fzL) 0.0 (R SwingLiftMax))) 0.0) (select penL (clamp (- (+ guL 7.5) fzL) 0.0 (R StepPenLiftMax)) 0.0)))   ; V2.26 T3d/T3e/T3g\n"
       "  (bind tR (max (select swR (* wRR (clamp (- (+ gRt (R SwingLiftMargin)) fzR) 0.0 (R SwingLiftMax))) 0.0) (select penR (clamp (- (+ guR 7.5) fzR) 0.0 (R StepPenLiftMax)) 0.0)))\n")
patch('shm_src.py', OLD, NEW, 'V2.26 T3g')
print('done')
