"""V2.25 SHME source patch I (inspection camera + limited look-at), applied to Tools/SHME_V1_20260925/{shm_src,shm_profiles,shm_component_vars}.py.
Behaviour (SHM_UpdateCameraV21, knob CamInspectEnabled, default False):
  gaze = one sphere trace (InspectRadius) along the PLAYER CAMERA forward up to InspectMaxDist. A hit whose display name (actor label in the
  editor / PIE, object name in a build) contains one of InspectKey1..4 ("INS_" test props, "Mask", "Door", "Lamp") is a candidate while the
  character is slow (Speed < InspectMaxSpeed) and the view is not spinning (camera yaw rate < InspectYawRateMax). Occluded targets are not
  hit (the trace stops at the occluder). The candidate's impact point must stay within InspectJump cm for InspectDwellOn seconds (no
  hopping between leaves); then the focus LATCHES. It is released when the gaze leaves for ~InspectDwellOn/2 (dwell decays at 2x), the
  character moves faster than InspectMaxSpeed, or the view spins. InspectOn eases in (InspectTauOn) / out (InspectTauOff).
  Camera while on: the pivot moves toward the focus point by InspectShare of the character->point horizontal vector (bounded by
  InspectOffsetMax) so character and object share the frame; the boom scales by InspectBoom; the perceptual follow re-centres (calm).
  Nothing rotates the control rotation; the mouse stays in charge. Head: InspectLookAlpha (gated by the yaw between the facing and the
  point, InspectLookMaxYaw) + InspectLookPoint -> ABP look-at chain (install_v225_lookat.py)."""
import pathlib
V1 = pathlib.Path(__file__).resolve().parents[2] / 'Tools/SHME_V1_20260925'
def patch(fname, old, new, marker):
    p = V1 / fname; t = p.read_bytes().decode('utf8')
    if marker in t: print(fname, marker, 'already'); return
    for nl in ('\n', '\r\n'):
        o = old.replace('\n', nl)
        if t.count(o) == 1: p.write_bytes(t.replace(o, new.replace('\n', nl)).encode('utf8')); print(fname, marker, 'patched'); return
    raise AssertionError((fname, marker))
patch('shm_profiles.py', "('CamFolYawFade', 'float', 0.0, 'V224'),",
      "('CamFolYawFade', 'float', 0.0, 'V224'), ('CamInspectEnabled', 'bool', False, 'V225'), ('InspectMaxDist', 'float', 450.0, 'V225'), ('InspectMinDist', 'float', 60.0, 'V225'),\n"
      "    ('InspectRadius', 'float', 22.0, 'V225'), ('InspectJump', 'float', 45.0, 'V225'), ('InspectDwellOn', 'float', 0.35, 'V225'), ('InspectMaxSpeed', 'float', 170.0, 'V225'),\n"
      "    ('InspectYawRateMax', 'float', 220.0, 'V225'), ('InspectTauOn', 'float', 0.35, 'V225'), ('InspectTauOff', 'float', 0.6, 'V225'), ('InspectShare', 'float', 0.35, 'V225'),\n"
      "    ('InspectOffsetMax', 'float', 140.0, 'V225'), ('InspectBoom', 'float', 0.94, 'V225'), ('InspectLookMaxYaw', 'float', 75.0, 'V225'),\n"
      "    ('InspectKey1', 'string', 'INS_', 'V225'), ('InspectKey2', 'string', 'Mask', 'V225'), ('InspectKey3', 'string', 'Door', 'V225'), ('InspectKey4', 'string', 'Lamp', 'V225'),", 'CamInspectEnabled')
patch('shm_component_vars.py', "('CamFolPrevYaw', F, 'SHM|V224'),",
      "('CamFolPrevYaw', F, 'SHM|V224'), ('InspectOn', F, 'SHM|V225'), ('InspectLatch', F, 'SHM|V225'), ('InspectDwell', F, 'SHM|V225'), ('InspectPoint', V, 'SHM|V225'),\n"
      "    ('InspectLookAlpha', F, 'SHM|V225'), ('InspectLookPoint', V, 'SHM|V225'), ('InspectPrevYaw', F, 'SHM|V225'), ('InspectCand', F, 'SHM|V225'),", 'InspectOn')
OLD = "  ; ---- V2.23 perceptual follow: per-axis soft zone in the camera frame (e = follow point - capsule, cm; + right / + view forward)\n"
NEW = ("  ; ---- V2.25 inspection: what the player looks at (one sphere trace along the view), dwell -> latch, calm framing, limited look-at\n"
       "  (bind insOn (and (R CamInspectEnabled) (not tele)))\n"
       "  (bind camL (Kamera|GetCameraLocation :self pcm3))\n"
       "  (bind cfw3 (Matematik|Vektör|GetForwardVector :InRot (Matematik|Döndürücü|MakeRotator :Roll 0.0 :Pitch cp3 :Yaw cy3)))\n"
       "  (bind gazeEnd (+ camL (vscale cfw3 (+ (R InspectMaxDist) 200.0))))\n"
       "  (bind (ihx ihh ihok) (Çarpışma|SphereTraceByChannel :Start camL :End gazeEnd :Radius (R InspectRadius) :TraceChannel \"TraceTypeQuery1\" :bTraceComplex false :bIgnoreSelf true))\n"
       "  (bind (ibh iio itm idd iloc iip inrm iinrm ipm iact) (Çarpışma|BreakHitResult :Hit ihh))\n"
       "  (bind iname (İşlevsellikler|GetDisplayName :Object iact))\n"
       "  (bind imatch (or (İşlevsellikler|Dize|Contains :SearchIn iname :Substring (R InspectKey1)) (or (İşlevsellikler|Dize|Contains :SearchIn iname :Substring (R InspectKey2)) (or (İşlevsellikler|Dize|Contains :SearchIn iname :Substring (R InspectKey3)) (İşlevsellikler|Dize|Contains :SearchIn iname :Substring (R InspectKey4))))))\n"
       "  (bind idist (vlenxy (- iip Position)))\n"
       "  (bind iyd0 (- cy3 InspectPrevYaw))\n"
       "  (bind iydw (Matematik|Trig|Atan2(Degrees) :Y (Matematik|Trig|Sin(Degrees) :A iyd0) :X (Matematik|Trig|Cos(Degrees) :A iyd0)))\n"
       "  (bind iyawRate (abs (/ iydw (max h 0.001))))\n"
       "  (bind islow (< Speed (R InspectMaxSpeed)))\n"
       "  (bind icalm (< iyawRate (R InspectYawRateMax)))\n"
       "  (bind cand (and insOn (and ihok (and imatch (and (> idist (R InspectMinDist)) (< idist (R InspectMaxDist)))))))\n"
       "  (bind isame (< (dist iip InspectPoint) (R InspectJump)))\n"
       "  (bind dwell1 (select cand (select isame (+ InspectDwell dt) 0.0) (max 0.0 (- InspectDwell (* dt 2.0)))))\n"
       "  (bind acquire (and (> dwell1 (R InspectDwellOn)) (and islow icalm)))\n"
       "  (bind lose (or (not islow) (or (not icalm) (< dwell1 0.001))))\n"
       "  (set InspectLatch (select acquire 1.0 (select lose 0.0 InspectLatch)))\n"
       "  (set InspectPoint (selv (and cand (not isame)) iip (selv cand (+ InspectPoint (vscale (- iip InspectPoint) (min 1.0 (* dt 6.0)))) InspectPoint)))\n"
       "  (set InspectDwell dwell1)\n"
       "  (set InspectCand (select cand 1.0 0.0))\n"
       "  (bind aIns (- 1.0 (exp (/ (- 0.0 h) (max (select (> InspectLatch 0.5) (R InspectTauOn) (R InspectTauOff)) 0.02)))))\n"
       "  (set InspectOn (select tele 0.0 (+ InspectOn (* (- InspectLatch InspectOn) aIns))))\n"
       "  (bind toP (- InspectPoint Position))\n"
       "  (bind toPh (vec (.x toP) (.y toP) 0.0))\n"
       "  (bind toPl (vlenxy toPh))\n"
       "  (bind ishare (vscale toPh (/ (min toPl (R InspectOffsetMax)) (max toPl 0.001))))\n"
       "  (set CamOffset (+ CamOffset (vscale ishare (* InspectOn (R InspectShare)))))\n"
       "  (bind lookDir (normal toPh))\n"
       "  (bind lookYaw (acosd (clamp (dot lookDir (normal (vec (.x Facing) (.y Facing) 0.0))) -1.0 1.0)))\n"
       "  (bind lookGate (clamp (/ (- (R InspectLookMaxYaw) lookYaw) 25.0) 0.0 1.0))\n"
       "  (set InspectLookAlpha (* InspectOn lookGate))\n"
       "  (set InspectLookPoint InspectPoint)\n"
       "  (set InspectPrevYaw cy3)\n"
       "  ; ---- V2.23 perceptual follow: per-axis soft zone in the camera frame (e = follow point - capsule, cm; + right / + view forward)\n")
patch('shm_src.py', OLD, NEW, 'V2.25 inspection')
# calm follow while inspecting: the D-patch re-centre weight takes the inspect level
OLD2 = "  (bind yK (select (and (> (R CamFolYawFade) 0.5) (not tele)) (clamp (/ (abs (/ ydw (max h 0.001))) (R CamFolYawFade)) 0.0 1.0) 0.0))\n"
NEW2 = ("  (bind yK0 (select (and (> (R CamFolYawFade) 0.5) (not tele)) (clamp (/ (abs (/ ydw (max h 0.001))) (R CamFolYawFade)) 0.0 1.0) 0.0))\n"
        "  (bind yK (max yK0 InspectOn))   ; V2.25: inspecting = the follow re-centres (calm frame)\n")
patch('shm_src.py', OLD2, NEW2, 'V2.25: inspecting = the follow')
OLD3 = "  (bind kt (select (R CamCloseEnabled) (lerp 1.0 kv CamOpenness) 1.0))\n"
NEW3 = "  (bind kt (* (select (R CamCloseEnabled) (lerp 1.0 kv CamOpenness) 1.0) (lerp 1.0 (R InspectBoom) InspectOn)))   ; V2.25 inspect boom\n"
patch('shm_src.py', OLD3, NEW3, 'V2.25 inspect boom')
print('done')
