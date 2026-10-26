"""apply_insp230.py: V2.30 inspection probe without member calls on a missing hit (idempotent). Measured: when the gaze trace hits
nothing, ActorHasTag / ComponentHasTag / GetActorBounds / GetActorLocation ran on None every frame -> 12 966 Blueprint "Accessed None"
runtime errors per 6 short PIE runs (PIE message log). Replacement (null-safe, static / parameter functions only): target test = the
existing name-key match (INS_ / Mask / Door / Lamp; GetDisplayName(None) = "None"), target centre = GetComponentBounds(hit component)
(the GR_Inspect probe sphere), used for identity distance and focus."""
import pathlib
S = pathlib.Path(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_src.py')
s = S.read_text(encoding='utf8')
if 'V2.30 null-safe inspection' in s: print('APPLYINSP230 already'); raise SystemExit
reps = [
 ("  (bind itag (or (Aktör|ActorHasTag :self iact :Tag (R InspectTag)) (Bileşenler|ComponentHasTag :self icomp :Tag (R InspectTag))))\n", ""),
 ("  (bind (iorg iext) (Çarpışma|GetActorBounds :self iact :bOnlyCollidingComponents false :bIncludeFromChildActors false))\n",
  "  ; V2.30 null-safe inspection: no member call on the (possibly missing) hit actor / component\n  (bind (iorg iext irad) (Çarpışma|GetComponentBounds :Component icomp))\n"),
 ("  (bind idist (vlenxy (- iip Position)))\n", "  (bind itag imatch)\n  (bind idist (vlenxy (- iip Position)))\n"),
 ("  (bind ifocus (selv (> (R InspectFocusMode) 0.5) (Dönüşüm|GetActorLocation :self iact) iorg))\n", "  (bind ifocus iorg)\n"),
]
for a, b in reps:
    assert s.count(a) == 1, a[:60]
    s = s.replace(a, b)
S.write_text(s, encoding='utf8'); print('APPLYINSP230 ok')
