"""apply_cam229.py (offline, run ONLY when no QA chain runs): V2.29 walk framing knobs in SHM_UpdateCameraV21 (neutral defaults = V2.28).
(1) shoulder swap only above CamSwapMinSpeed (was a fixed 60 cm/s): at walk the V2.1 half swap drifted the body to the screen centre on
every A / D / diagonal. (2) soft-zone size by speed: CamFolDZLatWalk / CamFolDZFwdWalk at <= CamWalkSpeedLo, the V2.23 zone (CamFolDZLat /
Fwd) from CamWalkSpeedHi up: the walk keeps the body at its shoulder place, jog / sprint keep the wider follow.
Profile defaults are NEUTRAL (60 / 12 / 10). Idempotent. Prints APPLYCAM229 {...}."""
import pathlib, json
T = pathlib.Path(__file__).resolve().parents[2] / 'Tools/SHME_V1_20260925'
out = {}
p = T / 'shm_profiles.py'; s = p.read_text(encoding='utf8')
if "'CamSwapMinSpeed'" in s: out['profiles'] = 'already'
else:
    add = """    ('CamSwapMinSpeed', 'float', 60.0, 'V229'), ('CamFolDZLatWalk', 'float', 12.0, 'V229'), ('CamFolDZFwdWalk', 'float', 10.0, 'V229'),
    ('CamWalkSpeedLo', 'float', 150.0, 'V229'), ('CamWalkSpeedHi', 'float', 260.0, 'V229'),
"""
    i = s.rindex(']'); s = s[:i] + add + s[i:]; p.write_text(s, encoding='utf8'); out['profiles'] = 'added'
s = open(T / 'shm_src.py', encoding='utf8', newline='').read()
if 'CamSwapMinSpeed' in s: out['src'] = 'already'
else:
    a = "(bind lat (select (and Grounded (> Speed 60.0)) (dot vh rtv) 0.0))"
    assert s.count(a) == 1; s = s.replace(a, "(bind lat (select (and Grounded (> Speed (R CamSwapMinSpeed))) (dot vh rtv) 0.0))   ; V2.29: swap only above CamSwapMinSpeed")
    a2 = "  (bind zL (R CamFolDZLat))"; a3 = "  (bind zF (R CamFolDZFwd))"
    assert s.count(a2) == 1 and s.count(a3) == 1
    s = s.replace(a2, "  (bind wz (clamp (/ (- Speed (R CamWalkSpeedLo)) (max (- (R CamWalkSpeedHi) (R CamWalkSpeedLo)) 1.0)) 0.0 1.0))   ; V2.29 walk -> run zone blend\n  (bind zL (lerp (R CamFolDZLatWalk) (R CamFolDZLat) wz))")
    s = s.replace(a3, "  (bind zF (lerp (R CamFolDZFwdWalk) (R CamFolDZFwd) wz))")
    open(T / 'shm_src.py', 'w', encoding='utf8', newline='').write(s); out['src'] = 'patched'
print('APPLYCAM229 ' + json.dumps(out))
