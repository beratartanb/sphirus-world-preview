"""V2.26 SHME source patch T3f: the landing shift HOLDS once the swing foot is over the raised platform until it plants.
Measured (v226t5 ter_drop_jog te, 28 cm step): the shift (12) brought the left foot over the step, then faded (9 -> 1 cm over 0.3 s)
while the foot hovered inside the box waiting for the body - the landing estimate had moved on so the edge test went false. Now the shift
target keeps its current value while the foot's own ground is above the support ground (gate2) and the foot has no contact yet."""
import pathlib
V1 = pathlib.Path(__file__).resolve().parents[2] / 'Tools/SHME_V1_20260925'
def patch(fname, old, new, marker):
    p = V1 / fname; t = p.read_bytes().decode('utf8')
    if marker in t: print(fname, marker, 'already'); return
    for nl in ('\n', '\r\n'):
        o = old.replace('\n', nl)
        if t.count(o) == 1: p.write_bytes(t.replace(o, new.replace('\n', nl)).encode('utf8')); print(fname, marker, 'patched'); return
    raise AssertionError((fname, marker))
OLD = ("  (bind seL (select (and (R StepEdgeOn) (and swL (> (- eLb eLa) (R StepEdgeMin)))) (R StepEdgeShift) 0.0))\n"
       "  (bind seR (select (and (R StepEdgeOn) (and swR (> (- eRb eRa) (R StepEdgeMin)))) (R StepEdgeShift) 0.0))\n")
NEW = ("  ; V2.26 T3f: hold the shift while the foot is over the platform (own ground above the support ground) and not yet planted\n"
       "  (bind holdL (and (> SwingShiftTL 1.0) (and (not ContactL) (> (- guL g0) (R SwingLiftRiseMin)))))\n"
       "  (bind holdR (and (> SwingShiftTR 1.0) (and (not ContactR) (> (- guR g0) (R SwingLiftRiseMin)))))\n"
       "  (bind seL (select (and (R StepEdgeOn) (and swL (> (- eLb eLa) (R StepEdgeMin)))) (R StepEdgeShift) (select holdL SwingShiftTL 0.0)))\n"
       "  (bind seR (select (and (R StepEdgeOn) (and swR (> (- eRb eRa) (R StepEdgeMin)))) (R StepEdgeShift) (select holdR SwingShiftTR 0.0)))\n")
patch('shm_src.py', OLD, NEW, 'V2.26 T3f')
print('done')
