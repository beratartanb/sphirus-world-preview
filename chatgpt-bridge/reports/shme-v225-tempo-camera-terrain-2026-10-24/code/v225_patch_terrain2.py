"""V2.25 SHME source patch T2b: the step preparation is RELEASED against the CAPSULE's own height change, in the human order.
Measured (v225t1 ter_drop_walk_tp): (a) the rebase keyed on the ground-under-capsule probe fired 0.23 s BEFORE the capsule actually dropped
(the probe sees the edge when the centre passes it, the capsule falls when its bottom loses the platform ~34 cm later) and (b) it fired on
an UNPREPARED 28 cm step (-22.7 cm pelvis target after the step-up). CMC steps the capsule up when it collides with the step, i.e. before
the swing foot has reached the top - the opposite of a human, whose pelvis rises AFTER the foot plants on the step.
Now: capDz = the capsule's z change this frame; while the capsule changes height (|capDz| > 6 cm, held active 0.3 s for the gradual CMC
step-up) the offset absorbs it (StepPrepZ -= capDz: the pelvis stays world-continuous); afterwards it is released toward the plan FAST
(StepPrepReleaseTau) once a foot contact begins on the new level (the planted foot defines the new height), SLOWLY (StepPrepHoldTau) until
then. The pelvis therefore rises after the step foot plants (step up) and lowers with the stance knee before the drop (prepared) - no pop,
no 'elevator'. Output clamp StepPrepHoldMax (32) separate from the preparation limit StepPrepMax (16)."""
import pathlib
V1 = pathlib.Path(__file__).resolve().parents[2] / 'Tools/SHME_V1_20260925'
def patch(fname, old, new, marker):
    p = V1 / fname; t = p.read_bytes().decode('utf8')
    if marker in t: print(fname, marker, 'already'); return
    for nl in ('\n', '\r\n'):
        o = old.replace('\n', nl)
        if t.count(o) == 1: p.write_bytes(t.replace(o, new.replace('\n', nl)).encode('utf8')); print(fname, marker, 'patched'); return
    raise AssertionError((fname, marker))
patch('shm_profiles.py', "('StepPrepReleaseTau', 'float', 0.12, 'V225'),", "('StepPrepReleaseTau', 'float', 0.12, 'V225'), ('StepPrepHoldTau', 'float', 0.5, 'V225'), ('StepPrepHoldMax', 'float', 32.0, 'V225'),", 'StepPrepHoldTau')
patch('shm_component_vars.py', "('StepPrepZ', F, 'SHM|V225'),", "('StepPrepZ', F, 'SHM|V225'), ('StepPrepPrevZ', F, 'SHM|V225'), ('StepPrepActT', F, 'SHM|V225'), ('StepPrepRel', F, 'SHM|V225'), ('StepPrepPrevCL', B_, 'SHM|V225'), ('StepPrepPrevCR', B_, 'SHM|V225'),", 'StepPrepPrevZ')
OLD = ("  (bind spJump (> (abs gDz) 4.0))\n"
       "  (bind aSp (- 1.0 (exp (/ (- 0.0 h) (max (R StepPrepTau) 0.02)))))\n"
       "  (bind aSpR (- 1.0 (exp (/ (- 0.0 h) (max (R StepPrepReleaseTau) 0.02)))))\n"
       "  ; a capsule height change consumes the preparation: the offset is re-based by the jump (pelvis world height continuous)\n"
       "  (bind spRebased (select spJump (- StepPrepZ gDz) StepPrepZ))\n"
       "  (bind spTarget (select spJump 0.0 spPlan))\n"
       "  (set StepPrepZ (select spOn (+ spRebased (* (- spTarget spRebased) (select spJump aSpR aSp))) 0.0))\n")
NEW = ("  ; V2.25 T2b: the capsule's own height change is absorbed by the offset (pelvis world-continuous) and released in the human order\n"
       "  (bind capDz (select TerrainInit (- (.z Position) StepPrepPrevZ) 0.0))\n"
       "  (bind spBig (> (abs capDz) 6.0))\n"
       "  (set StepPrepActT (select spBig 0.30 (max 0.0 (- StepPrepActT dt))))\n"
       "  (bind spAct (or spBig (and (> StepPrepActT 0.0) (> (abs capDz) 1.0))))\n"
       "  (bind contactEdge (or (and ContactL (not StepPrepPrevCL)) (and ContactR (not StepPrepPrevCR))))\n"
       "  (set StepPrepRel (select spAct 0.0 (select contactEdge 1.0 StepPrepRel)))\n"
       "  (bind aSp (- 1.0 (exp (/ (- 0.0 h) (max (R StepPrepTau) 0.02)))))\n"
       "  (bind aSpR (- 1.0 (exp (/ (- 0.0 h) (max (R StepPrepReleaseTau) 0.02)))))\n"
       "  (bind aSpH (- 1.0 (exp (/ (- 0.0 h) (max (R StepPrepHoldTau) 0.02)))))\n"
       "  (bind spRebased (select spAct (- StepPrepZ capDz) StepPrepZ))\n"
       "  (bind spHeld (> (abs (- spRebased spPlan)) 2.0))\n"
       "  (bind aSpUse (select spAct 0.0 (select (and spHeld (< StepPrepRel 0.5)) aSpH (select spHeld aSpR aSp))))\n"
       "  (set StepPrepZ (select spOn (+ spRebased (* (- spPlan spRebased) aSpUse)) 0.0))\n"
       "  (set StepPrepPrevZ (.z Position))\n"
       "  (set StepPrepPrevCL ContactL)\n"
       "  (set StepPrepPrevCR ContactR)\n")
patch('shm_src.py', OLD, NEW, 'V2.25 T2b')
OLD2 = "  (set PelvisOffsetTarget (+ potC (vec 0.0 0.0 (clamp StepPrepZ (- 0.0 (R StepPrepMax)) (R StepPrepMax)))))\n"
NEW2 = "  (set PelvisOffsetTarget (+ potC (vec 0.0 0.0 (clamp StepPrepZ (- 0.0 (R StepPrepHoldMax)) (R StepPrepHoldMax)))))   ; V2.25 T2b hold clamp\n"
patch('shm_src.py', OLD2, NEW2, 'V2.25 T2b hold clamp')
print('done')
