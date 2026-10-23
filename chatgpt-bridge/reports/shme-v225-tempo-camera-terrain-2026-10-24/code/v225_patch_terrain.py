"""V2.25 SHME source patch T (terrain stepping chain), applied to Tools/SHME_V1_20260925/{shm_src,shm_profiles,shm_component_vars}.py.
Measured on the V2.24 production (v224t9 ter_bump_walk_p / ter_drop_walk_p, fixed 30, per-frame feet):
 (1) bump top catch: the V2.24 rise gate compared the ground AHEAD OF THE FOOT with the support plane UNDER THE CAPSULE (FootZ). On the
     up-ramp the capsule is already on the top (+20) while the trailing swing foot (ball z 7) still has 11 cm of ramp ahead -> gate
     closed, lift 0, the sole skimmed the crest for 12 frames. Fix: the rise is measured against the ground UNDER THE FOOT (own probe),
     and the clearance target takes the MAX ground of three probes along the swing path (0.5 / 1.0 / 1.5 x ahead): the lift holds
     until the foot has passed the highest point it will cross, not until the next centimetre stops rising.
 (2) 15 cm step UP: the landing foot was planted INSIDE the platform (ball z 1-2 on a 28 top, lift on: 18) and popped 26 / 10 cm when the
     capsule stepped up (+30 in 4 frames). (3) 15 cm step DOWN: the capsule dropped 15 cm in ONE frame once its centre passed the edge
     (pelvis 105 -> 90 pop) while the planted foot hung 5 cm above the lower floor. Both are the pelvis / capsule pop at a planned
     height change. Fix: PLANNED STEP PREPARATION on the existing pelvis owner (PelvisOffsetTarget -> PBI pelvis ModifyBone): when the
     ground ahead (the travel probe gA, 35-140 cm) differs from the support ground by StepPrepMin..StepPrepMax, the pelvis target moves
     TOWARD the new level in advance (StepPrepGain x the difference, ramped over StepPrepTau), so the stance knee flexes before a step
     down / the stance leg extends before a step up, the reaching foot gets the range, and when the capsule height actually changes
     (gDz jump) the prepared offset is RELEASED through the existing absorb path (the pelvis stays continuous instead of popping).
     The pelvis z term gets its own clamp (StepPrepMax 14 cm) instead of the 4 cm PelvisOffsetMaxCm vector clamp.
 Planned vs fall: the preparation needs the drop / rise to be SEEN ahead (planned); a drop under the capsule that was not seen keeps the
     V2.21 unexpected-drop absorb; drops beyond StepPrepMax are not prepared (the existing fall / landing owners keep them).
Knobs (SHME DA): StepPrepEnabled (default False), StepPrepMin 5, StepPrepMax 16, StepPrepGain 0.75, StepPrepTau 0.22, StepPrepReleaseTau 0.12.
Outputs: StepPrepZ (cm, +up), SwingPathMaxL/R (ground max along the swing path, cm over base)."""
import pathlib
V1 = pathlib.Path(__file__).resolve().parents[2] / 'Tools/SHME_V1_20260925'
def patch(fname, old, new, marker):
    p = V1 / fname; t = p.read_bytes().decode('utf8')
    if marker in t: print(fname, marker, 'already'); return
    for nl in ('\n', '\r\n'):
        o = old.replace('\n', nl)
        if t.count(o) == 1: p.write_bytes(t.replace(o, new.replace('\n', nl)).encode('utf8')); print(fname, marker, 'patched'); return
    raise AssertionError((fname, marker))
patch('shm_profiles.py', "('SwingLiftRiseMin', 'float', 1.0, 'V224'),",
      "('SwingLiftRiseMin', 'float', 1.0, 'V224'), ('StepPrepEnabled', 'bool', False, 'V225'), ('StepPrepMin', 'float', 5.0, 'V225'), ('StepPrepMax', 'float', 16.0, 'V225'),\n"
      "    ('StepPrepGain', 'float', 0.75, 'V225'), ('StepPrepTau', 'float', 0.22, 'V225'), ('StepPrepReleaseTau', 'float', 0.12, 'V225'),", 'StepPrepEnabled')
patch('shm_component_vars.py', "('SwingLiftL', F, 'SHM|V224'),", "('SwingLiftL', F, 'SHM|V224'), ('StepPrepZ', F, 'SHM|V225'), ('StepPrepSeen', F, 'SHM|V225'), ('SwingPathMaxL', F, 'SHM|V225'), ('SwingPathMaxR', F, 'SHM|V225'),", 'StepPrepZ')
# ---- (1) swing lift: ground under the foot + max along the swing path
OLD1 = ("  (bind gL (select sok1 (.z sip1) baseZ))\n"
        "  (bind gRt (select sok2 (.z sip2) baseZ))\n")
NEW1 = ("  ; V2.25 T1: the foot's own ground (gate reference) and the MAX ground along the swing path (0.5 / 1.0 / 1.5 x ahead)\n"
        "  (bind (sxu1 shu1 soku1) (Çarpışma|LineTraceByChannel :Start (vec (.x FootCenterL) (.y FootCenterL) (+ baseZ 70.0)) :End (vec (.x FootCenterL) (.y FootCenterL) (- baseZ 90.0)) :TraceChannel \"TraceTypeQuery1\" :bTraceComplex false :bIgnoreSelf true))\n"
        "  (bind (sbhu1 siou1 stmu1 sddu1 slocu1 sipu1 snrmu1) (Çarpışma|BreakHitResult :Hit shu1))\n"
        "  (bind (sxu2 shu2 soku2) (Çarpışma|LineTraceByChannel :Start (vec (.x FootCenterR) (.y FootCenterR) (+ baseZ 70.0)) :End (vec (.x FootCenterR) (.y FootCenterR) (- baseZ 90.0)) :TraceChannel \"TraceTypeQuery1\" :bTraceComplex false :bIgnoreSelf true))\n"
        "  (bind (sbhu2 siou2 stmu2 sddu2 slocu2 sipu2 snrmu2) (Çarpışma|BreakHitResult :Hit shu2))\n"
        "  (bind pLh (+ FootCenterL (vscale slDir (* slA 0.5))))\n"
        "  (bind pRh (+ FootCenterR (vscale slDir (* slA 0.5))))\n"
        "  (bind pLf (+ FootCenterL (vscale slDir (* slA 1.5))))\n"
        "  (bind pRf (+ FootCenterR (vscale slDir (* slA 1.5))))\n"
        "  (bind (sxh1 shh1 sokh1) (Çarpışma|LineTraceByChannel :Start (vec (.x pLh) (.y pLh) (+ baseZ 70.0)) :End (vec (.x pLh) (.y pLh) (- baseZ 90.0)) :TraceChannel \"TraceTypeQuery1\" :bTraceComplex false :bIgnoreSelf true))\n"
        "  (bind (sbhh1 sioh1 stmh1 sddh1 sloch1 siph1 snrmh1) (Çarpışma|BreakHitResult :Hit shh1))\n"
        "  (bind (sxh2 shh2 sokh2) (Çarpışma|LineTraceByChannel :Start (vec (.x pRh) (.y pRh) (+ baseZ 70.0)) :End (vec (.x pRh) (.y pRh) (- baseZ 90.0)) :TraceChannel \"TraceTypeQuery1\" :bTraceComplex false :bIgnoreSelf true))\n"
        "  (bind (sbhh2 sioh2 stmh2 sddh2 sloch2 siph2 snrmh2) (Çarpışma|BreakHitResult :Hit shh2))\n"
        "  (bind (sxf1 shf1 sokf1) (Çarpışma|LineTraceByChannel :Start (vec (.x pLf) (.y pLf) (+ baseZ 70.0)) :End (vec (.x pLf) (.y pLf) (- baseZ 90.0)) :TraceChannel \"TraceTypeQuery1\" :bTraceComplex false :bIgnoreSelf true))\n"
        "  (bind (sbhf1 siof1 stmf1 sddf1 slocf1 sipf1 snrmf1) (Çarpışma|BreakHitResult :Hit shf1))\n"
        "  (bind (sxf2 shf2 sokf2) (Çarpışma|LineTraceByChannel :Start (vec (.x pRf) (.y pRf) (+ baseZ 70.0)) :End (vec (.x pRf) (.y pRf) (- baseZ 90.0)) :TraceChannel \"TraceTypeQuery1\" :bTraceComplex false :bIgnoreSelf true))\n"
        "  (bind (sbhf2 siof2 stmf2 sddf2 slocf2 sipf2 snrmf2) (Çarpışma|BreakHitResult :Hit shf2))\n"
        "  (bind guL (select soku1 (.z sipu1) baseZ))\n"
        "  (bind guR (select soku2 (.z sipu2) baseZ))\n"
        "  (bind gL (max (max (select sokh1 (.z siph1) baseZ) (select sok1 (.z sip1) baseZ)) (select sokf1 (.z sipf1) baseZ)))\n"
        "  (bind gRt (max (max (select sokh2 (.z siph2) baseZ) (select sok2 (.z sip2) baseZ)) (select sokf2 (.z sipf2) baseZ)))\n"
        "  (set SwingPathMaxL (- gL baseZ))\n"
        "  (set SwingPathMaxR (- gRt baseZ))\n")
patch('shm_src.py', OLD1, NEW1, 'V2.25 T1')
OLD2 = ("  (bind wRL (clamp (/ (- (- gL FootZ) (R SwingLiftRiseMin)) (max (R SwingLiftRiseRamp) 0.1)) 0.0 1.0))\n"
        "  (bind wRR (clamp (/ (- (- gRt FootZ) (R SwingLiftRiseMin)) (max (R SwingLiftRiseRamp) 0.1)) 0.0 1.0))\n")
NEW2 = ("  ; V2.25 T1 gate: rise of the swing path over the ground under the FOOT (not the capsule's plane)\n"
        "  (bind wRL (clamp (/ (- (- gL guL) (R SwingLiftRiseMin)) (max (R SwingLiftRiseRamp) 0.1)) 0.0 1.0))\n"
        "  (bind wRR (clamp (/ (- (- gRt guR) (R SwingLiftRiseMin)) (max (R SwingLiftRiseRamp) 0.1)) 0.0 1.0))\n")
patch('shm_src.py', OLD2, NEW2, 'V2.25 T1 gate')
# ---- (2)(3) planned step preparation on the pelvis owner
OLD3 = "  (bind pot (vec apaBack (+ (+ inward supShift) apaRight) (- 0.0 (+ (max drop landDrop) (+ settleDip (+ terrDip dropDip))))))\n"
NEW3 = ("  ; V2.25 T2: planned step preparation - the pelvis moves toward the level seen AHEAD before the capsule changes height; the capsule's\n"
        "  ; own height change (gDz) then releases it (continuous pelvis instead of a one-frame pop). Only seen steps within the limits.\n"
        "  (bind spOn (and (R StepPrepEnabled) (and terrOn (> Speed 20.0))))\n"
        "  (bind spDiff (- gA g0))\n"
        "  (bind spPlan (select (and spOn (and (> (abs spDiff) (R StepPrepMin)) (< (abs spDiff) (R StepPrepMax)))) (* (R StepPrepGain) spDiff) 0.0))\n"
        "  (bind spJump (> (abs gDz) 4.0))\n"
        "  (bind aSp (- 1.0 (exp (/ (- 0.0 h) (max (R StepPrepTau) 0.02)))))\n"
        "  (bind aSpR (- 1.0 (exp (/ (- 0.0 h) (max (R StepPrepReleaseTau) 0.02)))))\n"
        "  ; a capsule height change consumes the preparation: the offset is re-based by the jump (pelvis world height continuous)\n"
        "  (bind spRebased (select spJump (- StepPrepZ gDz) StepPrepZ))\n"
        "  (bind spTarget (select spJump 0.0 spPlan))\n"
        "  (set StepPrepZ (select spOn (+ spRebased (* (- spTarget spRebased) (select spJump aSpR aSp))) 0.0))\n"
        "  (set StepPrepSeen (select (> (abs spPlan) 0.1) 1.0 0.0))\n"
        "  (bind pot (vec apaBack (+ (+ inward supShift) apaRight) (- 0.0 (+ (max drop landDrop) (+ settleDip (+ terrDip dropDip))))))\n")
patch('shm_src.py', OLD3, NEW3, 'V2.25 T2')
OLD4 = "  (set PelvisOffsetTarget (selv (> potLen (R PelvisOffsetMaxCm)) (vscale pot (/ (R PelvisOffsetMaxCm) (max potLen 0.001))) pot))\n"
NEW4 = ("  ; V2.25 T2: the prepared step height is added AFTER the 4 cm vector clamp with its own limit\n"
        "  (bind potC (selv (> potLen (R PelvisOffsetMaxCm)) (vscale pot (/ (R PelvisOffsetMaxCm) (max potLen 0.001))) pot))\n"
        "  (set PelvisOffsetTarget (+ potC (vec 0.0 0.0 (clamp StepPrepZ (- 0.0 (R StepPrepMax)) (R StepPrepMax)))))\n")
patch('shm_src.py', OLD4, NEW4, 'V2.25 T2 clamp')
print('done')
