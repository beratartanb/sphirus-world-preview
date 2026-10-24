"""V2.26 SHME source patch T3: high step - hold the swing foot over a raised platform until the body has risen, and land it ON the platform.
Measured (v225t13 ter_drop_walk, 28 cm step): the right foot came over the box at 23 cm (gz 28) and SANK to 13.6 cm (14 cm inside the box)
while the capsule stepped up, because the T1 gate (rise of the path AHEAD over the ground under the FOOT) went to 0 as soon as the foot
was over the box; the swing foot then followed the flat loop's descent until FootPlacement/LegIK popped it up. The plant came 11 cm past the
edge (the heel hanging off the step).
T3a gate2: a second rise term = the ground under the swing foot over the SUPPORT ground (g0, under the capsule). Over a platform the body
  has not climbed yet this holds the lift target at (platform + margin); as the capsule climbs, g0 rises and the term releases (human order:
  the body comes up, the lift is no longer needed; the planted foot belongs to FootPlacement).
T3b landing shift (StepEdgeOn, candidate flag): when the landing probe (1.0 x ahead) is on raised ground but the mid probe (0.5 x) is not,
  the natural landing is within half a probe step of the edge -> shift the swing foot forward by StepEdgeShift cm along the travel; when the
  landing probe is still low but the far probe (1.5 x) is high -> StepEdgeShiftFar (reach onto the platform). The shift ramps in like the
  lift, is HELD while the foot is planted (FootPlacement locks the unshifted foot; a constant shift keeps the visible foot still) and fades
  during the next swing. World-space vector SwingShiftL/R -> ABP SHM226_ShiftL/R -> world-space additive ModifyBone on ik_foot after the lift."""
import pathlib
V1 = pathlib.Path(__file__).resolve().parents[2] / 'Tools/SHME_V1_20260925'
def patch(fname, old, new, marker):
    p = V1 / fname; t = p.read_bytes().decode('utf8')
    if marker in t: print(fname, marker, 'already'); return
    for nl in ('\n', '\r\n'):
        o = old.replace('\n', nl)
        if t.count(o) == 1: p.write_bytes(t.replace(o, new.replace('\n', nl)).encode('utf8')); print(fname, marker, 'patched'); return
    raise AssertionError((fname, marker))
patch('shm_profiles.py', "('SwingLiftRiseRamp', 'float', 2.0, 'V224'),", "('SwingLiftRiseRamp', 'float', 2.0, 'V224'), ('StepEdgeOn', 'bool', False, 'V226'), ('StepEdgeShift', 'float', 12.0, 'V226'), ('StepEdgeShiftFar', 'float', 18.0, 'V226'), ('StepEdgeMin', 'float', 6.0, 'V226'),", "('StepEdgeOn'")
patch('shm_component_vars.py', "('SwingAirTL', F, 'SHM|V225'),", "('SwingAirTL', F, 'SHM|V225'), ('SwingShiftL', V, 'SHM|V226'), ('SwingShiftR', V, 'SHM|V226'), ('SwingShiftTL', F, 'SHM|V226'), ('SwingShiftTR', F, 'SHM|V226'),", 'SwingShiftL')
OLD = ("  (bind wRL (clamp (/ (- (- gL guL) (R SwingLiftRiseMin)) (max (R SwingLiftRiseRamp) 0.1)) 0.0 1.0))\n"
       "  (bind wRR (clamp (/ (- (- gRt guR) (R SwingLiftRiseMin)) (max (R SwingLiftRiseRamp) 0.1)) 0.0 1.0))\n")
NEW = ("  ; V2.26 T3a: rise ahead over the foot's own ground OR the foot's own ground over the SUPPORT ground (g0): a foot already over a platform\n"
       "  ; the body has not climbed yet keeps its lift until the capsule rises\n"
       "  (bind wRL (clamp (/ (- (max (- gL guL) (- guL g0)) (R SwingLiftRiseMin)) (max (R SwingLiftRiseRamp) 0.1)) 0.0 1.0))\n"
       "  (bind wRR (clamp (/ (- (max (- gRt guR) (- guR g0)) (R SwingLiftRiseMin)) (max (R SwingLiftRiseRamp) 0.1)) 0.0 1.0))\n")
patch('shm_src.py', OLD, NEW, 'V2.26 T3a')
OLD2 = "  (set SwingGroundL (- gL baseZ))\n"
NEW2 = ("  ; V2.26 T3b landing shift onto a step (candidate: StepEdgeOn). Probes: mid 0.5x (siph), landing 1.0x (sip), far 1.5x (sipf)\n"
        "  (bind gmL (select sokh1 (.z siph1) baseZ))\n"
        "  (bind glL (select sok1 (.z sip1) baseZ))\n"
        "  (bind gfL (select sokf1 (.z sipf1) baseZ))\n"
        "  (bind gmR (select sokh2 (.z siph2) baseZ))\n"
        "  (bind glR (select sok2 (.z sip2) baseZ))\n"
        "  (bind gfR (select sokf2 (.z sipf2) baseZ))\n"
        "  (bind seL (select (and (R StepEdgeOn) swL) (select (and (> (- glL guL) (R StepEdgeMin)) (< (- gmL guL) (R StepEdgeMin))) (R StepEdgeShift) (select (and (> (- gfL guL) (R StepEdgeMin)) (< (- glL guL) (R StepEdgeMin))) (R StepEdgeShiftFar) 0.0)) 0.0))\n"
        "  (bind seR (select (and (R StepEdgeOn) swR) (select (and (> (- glR guR) (R StepEdgeMin)) (< (- gmR guR) (R StepEdgeMin))) (R StepEdgeShift) (select (and (> (- gfR guR) (R StepEdgeMin)) (< (- glR guR) (R StepEdgeMin))) (R StepEdgeShiftFar) 0.0)) 0.0))\n"
        "  ; held while planted (a constant shift on a FootPlacement-locked foot keeps the visible foot still); ramps like the lift in swing\n"
        "  (set SwingShiftTL (select ContactL SwingShiftTL (+ SwingShiftTL (* (- seL SwingShiftTL) (select (> seL SwingShiftTL) aUp aDn)))))\n"
        "  (set SwingShiftTR (select ContactR SwingShiftTR (+ SwingShiftTR (* (- seR SwingShiftTR) (select (> seR SwingShiftTR) aUp aDn)))))\n"
        "  (set SwingShiftL (selv (R StepEdgeOn) (vscale slDir SwingShiftTL) (vec 0.0 0.0 0.0)))\n"
        "  (set SwingShiftR (selv (R StepEdgeOn) (vscale slDir SwingShiftTR) (vec 0.0 0.0 0.0)))\n"
        "  (set SwingGroundL (- gL baseZ))\n")
patch('shm_src.py', OLD2, NEW2, 'V2.26 T3b')
print('done')
