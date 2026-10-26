"""apply_src230.py: V2.30 DSL + profile edits (idempotent). Low-speed reversal class: a body that ran recently (SpeedPeak >
RedirectLowRevPeak, above any walk speed) and gets a reversal request (angle > RedirectReversalClassAngle) above RedirectLowRevSpeed
opens a redirect episode and is classed REVERSAL (2) even when its onset speed is below RedirectBridgeMinSpeed, so the authored
SHM226 reversal family (entered at the brake time whose designed speed matches the body) is used instead of the vendor
stand-sprint-pivot tail + WalkToSprint. RedirectLowRevSpeed 0 = V2.29 behaviour."""
import pathlib
S = pathlib.Path(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_src.py')
P = pathlib.Path(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_profiles.py')
s = S.read_text(encoding='utf8'); out = []
if 'RedirectLowRevSpeed' not in s:
    a = "  (bind rdCand (and (and Grounded HasIntent) (and (> Speed (R RedirectEpisodeMinSpeed)) (> RedirectionAngle (R RedirectEpisodeAngle)))))\n"
    assert s.count(a) == 1
    s = s.replace(a, """  ; V2.30 low-speed reversal: a recently running body (SpeedPeak above walk) reversing above RedirectLowRevSpeed is a reversal episode
  (bind lowRev (and (> (R RedirectLowRevSpeed) 0.5) (and (> SpeedPeak (R RedirectLowRevPeak)) (> RedirectionAngle (R RedirectReversalClassAngle)))))
  (bind rdCand (and (and Grounded HasIntent) (and (> Speed (select lowRev (min (R RedirectLowRevSpeed) (R RedirectEpisodeMinSpeed)) (R RedirectEpisodeMinSpeed))) (> RedirectionAngle (R RedirectEpisodeAngle)))))
""")
    b = "  (bind rdClassNow (select (and (R RedirectBridgeEnabled) (> SpeedOnset (R RedirectBridgeMinSpeed))) (select (> RedirectionAngle (R RedirectReversalClassAngle)) 2.0 1.0) 0.0))\n"
    assert s.count(b) == 1
    s = s.replace(b, "  (bind rdClassNow (select (and (R RedirectBridgeEnabled) (or (> SpeedOnset (R RedirectBridgeMinSpeed)) lowRev)) (select (> RedirectionAngle (R RedirectReversalClassAngle)) 2.0 1.0) 0.0))\n")
    S.write_text(s, encoding='utf8'); out.append('src')
p = P.read_text(encoding='utf8')
if 'RedirectLowRevSpeed' not in p:
    a = "('RedirectReversalAngle', 'float', 135.0, 'Routing'),"
    assert p.count(a) == 1
    p = p.replace(a, a + " ('RedirectLowRevSpeed', 'float', 0.0, 'V230'), ('RedirectLowRevPeak', 'float', 145.0, 'V230'),")
    P.write_text(p, encoding='utf8'); out.append('profiles')
print('APPLY230', out or 'already')
