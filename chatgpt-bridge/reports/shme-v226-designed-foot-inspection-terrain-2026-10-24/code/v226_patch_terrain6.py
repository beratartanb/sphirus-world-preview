"""V2.26 SHME source patch T3c: (a) the lift must not decay while the slowing swing foot is still over a platform the body has not
climbed; (b) the landing shift needs a real landing estimate, not the 16 cm lift probes.
Measured (v226t3 ter_drop_walk, 28 cm step, T3a in): the right foot still planted 10 cm onto the step at ball z 18 (10 cm inside the box).
T3a's gate2 was true (platform under the foot, support ground low) but swR also requires FootSpeed > SwingLiftMinSpeed (60): at the end of
the swing the foot slows below it, the lift target went to 0 and decayed (TauDown 0.12) in the last frames before the plant - the foot sank
into the box. And the T3b shift reached only 3.7 cm: its probes sit 8 / 16 / 24 cm ahead of the foot (SwingLiftAhead 0.12 s x speed), so
the edge is seen only ~0.05 s before the landing.
T3c: swL/swR = confirmed swing AND (foot speed > min OR the foot is over a platform above the support ground: gate2 > RiseMin). Landing
estimate = the STANCE foot + travel direction x step length (Speed x StepEdgeStepTime, clamped); two probes around it (+-StepEdgeProbe cm):
a rise between them > StepEdgeMin means the natural landing straddles the edge -> shift forward by StepEdgeShift (rest of T3b unchanged:
ramp in swing, hold while planted)."""
import pathlib
V1 = pathlib.Path(__file__).resolve().parents[2] / 'Tools/SHME_V1_20260925'
def patch(fname, old, new, marker):
    p = V1 / fname; t = p.read_bytes().decode('utf8')
    if marker in t: print(fname, marker, 'already'); return
    for nl in ('\n', '\r\n'):
        o = old.replace('\n', nl)
        if t.count(o) == 1: p.write_bytes(t.replace(o, new.replace('\n', nl)).encode('utf8')); print(fname, marker, 'patched'); return
    raise AssertionError((fname, marker))
patch('shm_profiles.py', "('StepEdgeMin', 'float', 6.0, 'V226'),", "('StepEdgeMin', 'float', 6.0, 'V226'), ('StepEdgeStepTime', 'float', 0.45, 'V226'), ('StepEdgeStepMax', 'float', 120.0, 'V226'), ('StepEdgeProbe', 'float', 15.0, 'V226'),", "('StepEdgeStepTime'")
OLD1 = ("  (bind swL (and slOn (and (> SwingAirTL 0.10) (> FootSpeedL (R SwingLiftMinSpeed)))))\n"
        "  (bind swR (and slOn (and (> SwingAirTR 0.10) (> FootSpeedR (R SwingLiftMinSpeed)))))\n")
NEW1 = ("  ; V2.26 T3c: a slowing swing foot over a platform the body has not climbed keeps its lift (no decay into the step before the plant)\n"
        "  (bind swL (and slOn (and (> SwingAirTL 0.10) (or (> FootSpeedL (R SwingLiftMinSpeed)) (> (- guL g0) (R SwingLiftRiseMin))))))\n"
        "  (bind swR (and slOn (and (> SwingAirTR 0.10) (or (> FootSpeedR (R SwingLiftMinSpeed)) (> (- guR g0) (R SwingLiftRiseMin))))))\n")
patch('shm_src.py', OLD1, NEW1, 'V2.26 T3c: a slowing')
OLD2 = ("  (bind seL (select (and (R StepEdgeOn) swL) (select (and (> (- glL guL) (R StepEdgeMin)) (< (- gmL guL) (R StepEdgeMin))) (R StepEdgeShift) (select (and (> (- gfL guL) (R StepEdgeMin)) (< (- glL guL) (R StepEdgeMin))) (R StepEdgeShiftFar) 0.0)) 0.0))\n"
        "  (bind seR (select (and (R StepEdgeOn) swR) (select (and (> (- glR guR) (R StepEdgeMin)) (< (- gmR guR) (R StepEdgeMin))) (R StepEdgeShift) (select (and (> (- gfR guR) (R StepEdgeMin)) (< (- glR guR) (R StepEdgeMin))) (R StepEdgeShiftFar) 0.0)) 0.0))\n")
NEW2 = ("  ; V2.26 T3c landing estimate = stance foot + travel x step length; probes +-StepEdgeProbe around it; a rise between them = the landing straddles an edge\n"
        "  (bind stepLen (clamp (* Speed (R StepEdgeStepTime)) 30.0 (R StepEdgeStepMax)))\n"
        "  (bind pLandL (+ FootCenterR (vscale slDir stepLen)))\n"
        "  (bind pLandR (+ FootCenterL (vscale slDir stepLen)))\n"
        "  (bind pLa (- pLandL (vscale slDir (R StepEdgeProbe))))\n"
        "  (bind pLb (+ pLandL (vscale slDir (R StepEdgeProbe))))\n"
        "  (bind pRa (- pLandR (vscale slDir (R StepEdgeProbe))))\n"
        "  (bind pRb (+ pLandR (vscale slDir (R StepEdgeProbe))))\n"
        "  (bind (exa1 eha1 eoka1) (Çarpışma|LineTraceByChannel :Start (vec (.x pLa) (.y pLa) (+ baseZ 70.0)) :End (vec (.x pLa) (.y pLa) (- baseZ 90.0)) :TraceChannel \"TraceTypeQuery1\" :bTraceComplex false :bIgnoreSelf true))\n"
        "  (bind (ebha1 eioa1 etma1 edda1 eloca1 eipa1 enrma1) (Çarpışma|BreakHitResult :Hit eha1))\n"
        "  (bind (exb1 ehb1 eokb1) (Çarpışma|LineTraceByChannel :Start (vec (.x pLb) (.y pLb) (+ baseZ 70.0)) :End (vec (.x pLb) (.y pLb) (- baseZ 90.0)) :TraceChannel \"TraceTypeQuery1\" :bTraceComplex false :bIgnoreSelf true))\n"
        "  (bind (ebhb1 eiob1 etmb1 eddb1 elocb1 eipb1 enrmb1) (Çarpışma|BreakHitResult :Hit ehb1))\n"
        "  (bind (exa2 eha2 eoka2) (Çarpışma|LineTraceByChannel :Start (vec (.x pRa) (.y pRa) (+ baseZ 70.0)) :End (vec (.x pRa) (.y pRa) (- baseZ 90.0)) :TraceChannel \"TraceTypeQuery1\" :bTraceComplex false :bIgnoreSelf true))\n"
        "  (bind (ebha2 eioa2 etma2 edda2 eloca2 eipa2 enrma2) (Çarpışma|BreakHitResult :Hit eha2))\n"
        "  (bind (exb2 ehb2 eokb2) (Çarpışma|LineTraceByChannel :Start (vec (.x pRb) (.y pRb) (+ baseZ 70.0)) :End (vec (.x pRb) (.y pRb) (- baseZ 90.0)) :TraceChannel \"TraceTypeQuery1\" :bTraceComplex false :bIgnoreSelf true))\n"
        "  (bind (ebhb2 eiob2 etmb2 eddb2 elocb2 eipb2 enrmb2) (Çarpışma|BreakHitResult :Hit ehb2))\n"
        "  (bind eLa (select eoka1 (.z eipa1) baseZ))\n"
        "  (bind eLb (select eokb1 (.z eipb1) baseZ))\n"
        "  (bind eRa (select eoka2 (.z eipa2) baseZ))\n"
        "  (bind eRb (select eokb2 (.z eipb2) baseZ))\n"
        "  (bind seL (select (and (R StepEdgeOn) (and swL (> (- eLb eLa) (R StepEdgeMin)))) (R StepEdgeShift) 0.0))\n"
        "  (bind seR (select (and (R StepEdgeOn) (and swR (> (- eRb eRa) (R StepEdgeMin)))) (R StepEdgeShift) 0.0))\n")
patch('shm_src.py', OLD2, NEW2, 'V2.26 T3c landing estimate')
print('done')
