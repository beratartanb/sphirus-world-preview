"""apply_insp231.py: V2.31 inspection target identity + focus (idempotent DSL source edit of SHM_UpdateCameraV21 in shm_src.py).
V2.30 kept memory safe by replacing the tag contract with a NAME key (INS_ / Mask in the display name) and the focus with the bounds origin of
the hit component (= the query probe sphere, 15-25 cm in front of the mask). V2.31 (DA InspectFocusMode >= 1.5; 0/1 keep V2.26/V2.28/V2.30):
  - the camera function only STORES the hit component (SHM231_InsHit, unconditional object store - the DSL cannot branch)
  - SHM231_InspectResolve (exec graph, install_v231_inspect.py, runs right after the camera function in SHM_Tick) does every member call
    behind IsValid: tag GR_Inspect on the component or its actor -> SHM231_InsTag, SHM231_InsId = owner path name, SHM231_InsFocus = bounds
    origin of the OWNER'S ROOT component (the mask mesh itself, not the probe)
  - the camera function uses them one frame later, but only for the SAME object: tag = InsTag AND path(hit actor) == InsId (both-way
    Contains = equality; GetPathName / GetObjectName are static and null-safe), identity for dwell / switching = path equality with last
    frame (SHM231_InsPrevId), focus = InsFocus. Query sphere centre (probe) and visual focus (mask) are separate."""
import pathlib
S = pathlib.Path(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_src.py')
s = S.read_text(encoding='utf8')
if 'V2.31 inspection' in s: print('APPLYINSP231 already'); raise SystemExit
C = '(İşlevsellikler|Dize|Contains :SearchIn %s :Substring %s)'
eq = lambda a, b: '(and %s %s)' % (C % (a, b), C % (b, a))
reps = [
 ("  (bind cand (and insOn (and ihok (and itag (and (> idist (R InspectMinDist)) (< idist (R InspectMaxDist)))))))   ; V2.26 I4: tag, not name\n",
  "  ; V2.31 inspection: explicit tag contract resolved behind IsValid (SHM231_InspectResolve), identity = the same object path, focus = mask mesh\n"
  "  (bind m231 (> (R InspectFocusMode) 1.5))\n"
  "  (bind ipath (İşlevsellikler|GetObjectPathString :Object iact))\n"
  "  (bind itag231 (and SHM231_InsTag " + eq('ipath', 'SHM231_InsId') + "))\n"
  "  (bind itagU (selb m231 itag231 itag))\n"
  "  (bind cand (and insOn (and ihok (and itagU (and (> idist (R InspectMinDist)) (< idist (R InspectMaxDist)))))))   ; V2.26 I4: tag, not name (V2.31: resolved tag)\n"),
 ("  (bind isame (selb (> (R InspectIdOn) 0.5) idsame isameD))\n",
  "  (bind isame (selb m231 " + eq('ipath', 'SHM231_InsPrevId') + " (selb (> (R InspectIdOn) 0.5) idsame isameD)))\n"),
 ("  (bind ifocus iorg)\n", "  (bind ifocus (selv m231 SHM231_InsFocus iorg))\n"),
 ("  (set InspectMatch (select (and ihok itag) 1.0 0.0))\n", "  (set InspectMatch (select (and ihok itagU) 1.0 0.0))\n"),
 ("  (set InspectPrevHitName inameo)\n", "  (set InspectPrevHitName inameo)\n  (set SHM231_InsPrevId ipath)\n  (set SHM231_InsHit icomp)\n"),
]
for a, b in reps:
    assert s.count(a) == 1, a[:70]
    s = s.replace(a, b)
S.write_text(s, encoding='utf8'); print('APPLYINSP231 ok')
