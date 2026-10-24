"""V2.26 SHME source patch T3e: the penetration lift (foot inside a platform) may exceed SwingLiftMax.
Measured (v226t5 ter_drop_walk, 28 cm step): with T3d the lift stayed on (17.4 at the plant) but the ball still planted at z 18 (10 cm inside
the box): the flat loop's landing pose puts the ball at -2 and the lift is clamped at SwingLiftMax 25 (swing clearance limit), so the
foot could not reach the 28 cm top. The platform-plant lift gets its own limit StepPenLiftMax (36 cm, reachable with a bent knee:
foot 45 cm ahead / 62 cm below the hip)."""
import pathlib
V1 = pathlib.Path(__file__).resolve().parents[2] / 'Tools/SHME_V1_20260925'
def patch(fname, old, new, marker):
    p = V1 / fname; t = p.read_bytes().decode('utf8')
    if marker in t: print(fname, marker, 'already'); return
    for nl in ('\n', '\r\n'):
        o = old.replace('\n', nl)
        if t.count(o) == 1: p.write_bytes(t.replace(o, new.replace('\n', nl)).encode('utf8')); print(fname, marker, 'patched'); return
    raise AssertionError((fname, marker))
patch('shm_profiles.py', "('StepEdgeProbe', 'float', 15.0, 'V226'),", "('StepEdgeProbe', 'float', 15.0, 'V226'), ('StepPenLiftMax', 'float', 36.0, 'V226'),", "('StepPenLiftMax'")
patch('shm_src.py', "(select penL (clamp (- (+ guL 7.5) (.z FootCenterL)) 0.0 (R SwingLiftMax)) 0.0)))   ; V2.26 T3d\n", "(select penL (clamp (- (+ guL 7.5) (.z FootCenterL)) 0.0 (R StepPenLiftMax)) 0.0)))   ; V2.26 T3d/T3e\n", 'T3d/T3e')
patch('shm_src.py', "(select penR (clamp (- (+ guR 7.5) (.z FootCenterR)) 0.0 (R SwingLiftMax)) 0.0)))\n", "(select penR (clamp (- (+ guR 7.5) (.z FootCenterR)) 0.0 (R StepPenLiftMax)) 0.0)))\n", '(R StepPenLiftMax)) 0.0)))\n')
print('done')
