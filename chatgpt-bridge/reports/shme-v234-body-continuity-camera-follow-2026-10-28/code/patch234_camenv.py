"""patch234_camenv.py (offline source patch, idempotent) - V2.34 camera package 4 (sphirus-camera-direction):
  (a) phase envelope CamEnv for the cinematic orbit (CamEnvEnabled): rises (CamEnvRise s) when a brake / reversal / turn / redirect
      episode starts, holds while it lasts, decays (CamEnvRelease s) CamEnvHold s after the episode ended (push established) - the orbit
      target is multiplied by it, so the 3/4 view happens WHILE the body brakes / changes support / pushes and is handed back to the base
      follow afterwards (no swing-out after the turn is finished). Continuous: a new request during the decay raises it from its current
      value (no restart from zero, no wobble).
  (b) recentre only when the BODY faces the travel (CamRecFaceMax deg; 0 = off): a deliberate strafe / backpedal (body facing the view,
      travel sideways / backward) is never turned into a forward run by the camera.
  (c) real 180 deg turn vs backward travel (CamRecTurnSide): backward travel = the body faces away from the travel -> no recentre (b);
      a real turn = the body faces the new travel -> the recentre may exceed CamRecMaxErr and takes the side the body itself turned
      (CamRecTurnSign = sign of the last |YawRate| > 60 deg/s) - never the sin-zero side by chance.
Profiles / vars are appended to shm_profiles.py / shm_component_vars.py."""
import os
H = os.path.dirname(os.path.abspath(__file__)) + '/../SHME_V1_20260925/'
W = lambda x: '(Matematik|Trig|Atan2(Degrees) :Y (Matematik|Trig|Sin(Degrees) :A %s) :X (Matematik|Trig|Cos(Degrees) :A %s))' % (x, x)
p = H + 'shm_profiles.py'; s = open(p, encoding='utf8').read()
if 'CamEnvEnabled' not in s:
    a = "    ('LocoExploreKeep', 'float', 40.0, 'V234'),\n"
    assert a in s
    s = s.replace(a, a + "    ('CamEnvEnabled', 'bool', False, 'V234'), ('CamEnvRise', 'float', 0.12, 'V234'), ('CamEnvRelease', 'float', 0.6, 'V234'),\n"
                       "    ('CamEnvHold', 'float', 0.3, 'V234'), ('CamEnvTrig', 'float', 0.25, 'V234'), ('CamRecFaceMax', 'float', 0.0, 'V234'),\n"
                       "    ('CamRecTurnSide', 'bool', False, 'V234'),\n")
    open(p, 'w', encoding='utf8').write(s)
p = H + 'shm_component_vars.py'; s = open(p, encoding='utf8').read()
if "'CamEnv'" not in s:
    a = "('LocoHold', B_, 'SHM|V234'), ('LocoState', F, 'SHM|V234')]"
    assert a in s
    s = s.replace(a, a + "\nVARS += [('CamEnv', F, 'SHM|V234'), ('CamEnvT', F, 'SHM|V234'), ('CamRecTurnSign', F, 'SHM|V234')]")
    open(p, 'w', encoding='utf8').write(s)
p = H + 'shm_src.py'; s = open(p, encoding='utf8').read()
if 'CamEnvEnabled' not in s:
    # (a) envelope before the orbit target; the target is scaled by it
    a = "  (bind otg (select oOn"
    assert s.count(a) == 1
    env = """  ; V2.34 phase envelope (CamEnvEnabled): brake / reversal / turn / redirect episode -> rise, hold, then decay CamEnvHold s after it ended
  (bind etr (or RedirectActive (> (max (max BrakingDemand ReversalDemand) TurnSeverity) (R CamEnvTrig))))
  (bind etT (select etr 0.0 (+ CamEnvT dt)))
  (bind etg (select (< etT (R CamEnvHold)) 1.0 0.0))
  (bind etau (select (> etg CamEnv) (R CamEnvRise) (R CamEnvRelease)))
  (bind envN (select tele 0.0 (+ CamEnv (* (- etg CamEnv) (- 1.0 (exp (/ (- 0.0 h) (max etau 0.03))))))))
  (bind envK (select (R CamEnvEnabled) envN 1.0))
"""
    s = s.replace(a, env + a)
    s = s.replace("  (bind otg (select oOn (* (* omS osn)", "  (bind otg (select oOn (* (* (* omS osn) envK)", 1)
    assert "(* (* omS osn) envK)" in s
    a2 = "  (set CamOrbitLookT olt)\n"
    assert s.count(a2) == 1
    s = s.replace(a2, "  (set CamEnv envN)\n  (set CamEnvT etT)\n" + a2)
    # (b) + (c) in the recentre condition
    a3 = "  (bind rok (and (R CamRecEnabled)"
    assert s.count(a3) == 1
    rc = """  ; V2.34 (b) body faces the travel, (c) real turn side
  (bind rfa (abs %s))
  (bind rface (or (< (R CamRecFaceMax) 0.5) (< rfa (R CamRecFaceMax))))
  (bind rbig (and (R CamRecTurnSide) (and rface (not (< (abs re) (R CamRecMaxErr))))))
  (bind reE (select rbig (* (select (< CamRecTurnSign 0.0) -1.0 1.0) (abs re)) re))
""" % W('(- Yaw rty)')
    s = s.replace(a3, rc + a3)
    old_rok = s[s.index(a3):s.index('\n', s.index(a3))]
    new_rok = old_rok.replace("(and (> (abs re) (R CamRecDead)) (< (abs re) (R CamRecMaxErr)))", "(and rface (and (> (abs re) (R CamRecDead)) (or rbig (< (abs re) (R CamRecMaxErr)))))")
    assert new_rok != old_rok
    s = s.replace(old_rok, new_rok)
    a4 = "  (bind racc (select rok (- (* (* rw rw) re)"
    assert s.count(a4) == 1
    s = s.replace(a4, "  (bind racc (select rok (- (* (* rw rw) reE)")
    a5 = "  (set CamRecStableT rst)\n"
    assert s.count(a5) == 1
    s = s.replace(a5, a5 + "  (set CamRecTurnSign (select (> (abs YawRate) 60.0) (select (> YawRate 0.0) 1.0 -1.0) CamRecTurnSign))   ; V2.34 (c) the side the body last turned\n")
    open(p, 'w', encoding='utf8').write(s)
print('PATCH234_CAMENV ok')
