"""V2.26 SHME source patch I3 (diagnosis telemetry for the inspection gaze): what the gaze trace hits every frame.
New component vars (telemetry only, no behaviour change): InspectHitName (string: display name of the hit actor, 'None' = no hit),
InspectHitDist (float: trace distance), InspectHitZ (float: impact z), InspectMatch (float 1/0: name matched a key).
V2.25 ins_ws never produced a candidate on the R05 workshop masks and the report could not say why; this shows the first blocker."""
import pathlib
V1 = pathlib.Path(__file__).resolve().parents[2] / 'Tools/SHME_V1_20260925'
def patch(fname, old, new, marker):
    p = V1 / fname; t = p.read_bytes().decode('utf8')
    if marker in t: print(fname, marker, 'already'); return
    for nl in ('\n', '\r\n'):
        o = old.replace('\n', nl)
        if t.count(o) == 1: p.write_bytes(t.replace(o, new.replace('\n', nl)).encode('utf8')); print(fname, marker, 'patched'); return
    raise AssertionError((fname, marker))
patch('shm_component_vars.py', "('InspectCand', F, 'SHM|V225'),", "('InspectCand', F, 'SHM|V225'), ('InspectHitName', 'string', 'SHM|V226'), ('InspectHitDist', F, 'SHM|V226'), ('InspectHitZ', F, 'SHM|V226'), ('InspectMatch', F, 'SHM|V226'),", 'InspectHitName')
OLD = "  (set InspectCand (select cand 1.0 0.0))\n"
NEW = ("  (set InspectCand (select cand 1.0 0.0))\n"
       "  ; V2.26 I3 gaze telemetry: the first blocker of the gaze trace (name / distance / impact height / key match)\n"
       "  (set InspectHitName iname)\n"   # no string select in the DSL (select = SelectFloat); a null hit reads None
       "  (set InspectHitDist (select ihok idd 0.0))\n"
       "  (set InspectHitZ (select ihok (.z iip) 0.0))\n"
       "  (set InspectMatch (select (and ihok imatch) 1.0 0.0))\n")
patch('shm_src.py', OLD, NEW, 'V2.26 I3')
print('done')
