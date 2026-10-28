"""patch234_revkeep.py (offline source patch, idempotent) - V2.34 chain 1 / release-repress (sphirus-natural-motion):
a reversal (routing family 3) whose input was released and pressed again in the SAME direction within RevGraceTime s continues as the
reversal - the body is still braking / turning in the reversal pose - instead of being forced into the from-rest start family (4), whose
start clip begins from a quiet stance (j30_rel_3200: 51 cm drag). The start family keeps every real onset from rest (no recent reversal
or a different direction). RevGraceTime 0 = off. State: SHM234_RevAgo (s since family 3), SHM234_RevDir (the reversal's input direction)."""
import os
H = os.path.dirname(os.path.abspath(__file__)) + '/../SHME_V1_20260925/'
p = H + 'shm_profiles.py'; s = open(p, encoding='utf8').read()
if 'RevGraceTime' not in s:
    a = "    ('CamRecWalkRate', 'float', 0.0, 'V234'),\n"
    assert a in s
    s = s.replace(a, a + "    ('RevGraceTime', 'float', 0.0, 'V234'), ('RevGraceDot', 'float', 0.7, 'V234'),\n"); open(p, 'w', encoding='utf8').write(s)
p = H + 'shm_component_vars.py'; s = open(p, encoding='utf8').read()
if 'SHM234_RevAgo' not in s:
    a = "VARS += [('CamEnv', F, 'SHM|V234'), ('CamEnvT', F, 'SHM|V234'), ('CamRecTurnSign', F, 'SHM|V234')]"
    assert a in s
    s = s.replace(a, a + "\nVARS += [('SHM234_RevAgo', F, 'SHM|V234'), ('SHM234_RevDir', V, 'SHM|V234')]"); open(p, 'w', encoding='utf8').write(s)
p = H + 'shm_src.py'; s = open(p, encoding='utf8').read()
if 'SHM234_RevAgo' not in s:
    a = "  (bind cand (select Blocked 5.0 (select revCand 3.0"
    assert s.count(a) == 1
    s = s.replace(a, """  ; V2.34 release-repress: a re-press in the reversal's own direction within RevGraceTime continues the reversal (not a from-rest start)
  (bind rkeep (and (> (R RevGraceTime) 0.0) (and HasIntent (and (< SHM234_RevAgo (R RevGraceTime)) (> (+ (* (.x DesiredDir) (.x SHM234_RevDir)) (* (.y DesiredDir) (.y SHM234_RevDir))) (R RevGraceDot))))))
  (bind cand (select Blocked 5.0 (select (or revCand rkeep) 3.0""")
    a2 = "  (set FamilyTime (select RouteSwitch 0.0 FamilyTime))\n"
    assert s.count(a2) == 1
    s = s.replace(a2, a2 + """  (set SHM234_RevAgo (select (< (abs (- Family 3.0)) 0.5) 0.0 (+ SHM234_RevAgo dt)))   ; V2.34 release-repress memory
  (set SHM234_RevDir (selv (and HasIntent (< (abs (- Family 3.0)) 0.5)) DesiredDir SHM234_RevDir))
""")
    open(p, 'w', encoding='utf8').write(s)
print('PATCH234_REVKEEP ok')
