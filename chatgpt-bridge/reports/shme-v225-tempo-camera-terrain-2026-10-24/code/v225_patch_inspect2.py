"""V2.25 SHME source patch I2: the inspection releases promptly when the player looks away or walks.
Measured (v225t7 ins_qa): the dwell accumulated for the whole hold (2-3 s) and decayed at 2/s, so InspectOn stayed latched ~2 s after the
look turned away (and walking at 132 cm/s was below InspectMaxSpeed 170). Now the dwell is capped at InspectDwellOn + 0.15 s (decays to 0
in ~0.25 s after the gaze leaves) and the speed limit default drops to 60 cm/s (walking off releases; standing / shuffling keeps it)."""
import pathlib
V1 = pathlib.Path(__file__).resolve().parents[2] / 'Tools/SHME_V1_20260925'
def patch(fname, old, new, marker):
    p = V1 / fname; t = p.read_bytes().decode('utf8')
    if marker in t: print(fname, marker, 'already'); return
    for nl in ('\n', '\r\n'):
        o = old.replace('\n', nl)
        if t.count(o) == 1: p.write_bytes(t.replace(o, new.replace('\n', nl)).encode('utf8')); print(fname, marker, 'patched'); return
    raise AssertionError((fname, marker))
patch('shm_src.py', "  (bind dwell1 (select cand (select isame (+ InspectDwell dt) 0.0) (max 0.0 (- InspectDwell (* dt 2.0)))))\n",
      "  (bind dwell1 (min (+ (R InspectDwellOn) 0.15) (select cand (select isame (+ InspectDwell dt) 0.0) (max 0.0 (- InspectDwell (* dt 2.0))))))   ; V2.25 I2 dwell cap\n", 'V2.25 I2 dwell cap')
patch('shm_profiles.py', "('InspectMaxSpeed', 'float', 170.0, 'V225')", "('InspectMaxSpeed', 'float', 60.0, 'V225')", "('InspectMaxSpeed', 'float', 60.0")
print('done')
