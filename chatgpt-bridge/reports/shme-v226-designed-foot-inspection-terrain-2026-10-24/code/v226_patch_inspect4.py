"""V2.26 SHME source patch I4: inspection target CONTRACT + framing split.
Contract: a gaze hit is a candidate only when the hit ACTOR has the tag GR_Inspect or the hit COMPONENT has the tag GR_Inspect (QA props
and the real house targets carry the tag; display-name keys are no longer a contract - InspectKey* stay as data but are unused).
Focus point = the hit actor's bounds ORIGIN (stable: no hit point wandering over the surface; two close masks have different origins, so
the dwell restarts between them; a moving target's origin follows it). Target identity = that origin (InspectJump now 2 cm).
Framing split (section 8): InspectZoomOn (bool, default false) gates the CLOSENESS part - the boom factor and the along-view part of the
pivot share; with it off only the view-lateral pivot share (character / target composition), the calm follow and the body look remain,
so B (no closeness) and C (small closeness) can be compared at equal camera-capsule distance."""
import pathlib
V1 = pathlib.Path(__file__).resolve().parents[2] / 'Tools/SHME_V1_20260925'
def patch(fname, old, new, marker):
    p = V1 / fname; t = p.read_bytes().decode('utf8')
    if marker in t: print(fname, marker, 'already'); return
    for nl in ('\n', '\r\n'):
        o = old.replace('\n', nl)
        if t.count(o) == 1: p.write_bytes(t.replace(o, new.replace('\n', nl)).encode('utf8')); print(fname, marker, 'patched'); return
    raise AssertionError((fname, marker))
patch('shm_profiles.py', "('InspectJump', 'float', 45.0, 'V225')", "('InspectJump', 'float', 2.0, 'V225'), ('InspectZoomOn', 'bool', False, 'V226'), ('InspectTag', 'string', 'GR_Inspect', 'V226')", "('InspectZoomOn'")
patch('shm_component_vars.py', "('InspectMatch', F, 'SHM|V226'),", "('InspectMatch', F, 'SHM|V226'), ('InspectHitActorName', 'string', 'SHM|V226'),", 'InspectHitActorName')
OLD1 = ("  (bind (ibh iio itm idd iloc iip inrm iinrm ipm iact) (Çarpışma|BreakHitResult :Hit ihh))\n"
        "  (bind iname (İşlevsellikler|GetDisplayName :Object iact))\n")
NEW1 = ("  (bind (ibh iio itm idd iloc iip inrm iinrm ipm iact icomp) (Çarpışma|BreakHitResult :Hit ihh))\n"
        "  (bind iname (İşlevsellikler|GetDisplayName :Object iact))\n"
        "  ; V2.26 I4 contract: actor tag or component tag GR_Inspect; focus point = actor bounds origin\n"
        "  (bind itag (or (Aktör|ActorHasTag :self iact :Tag (R InspectTag)) (Bileşenler|ComponentHasTag :self icomp :Tag (R InspectTag))))\n"
        "  (bind (iorg iext) (Çarpışma|GetActorBounds :self iact :bOnlyCollidingComponents false :bIncludeFromChildActors false))\n")
patch('shm_src.py', OLD1, NEW1, 'V2.26 I4 contract')
OLD2 = "  (bind cand (and insOn (and ihok (and imatch (and (> idist (R InspectMinDist)) (< idist (R InspectMaxDist)))))))\n  (bind isame (< (dist iip InspectPoint) (R InspectJump)))\n"
NEW2 = "  (bind cand (and insOn (and ihok (and itag (and (> idist (R InspectMinDist)) (< idist (R InspectMaxDist)))))))   ; V2.26 I4: tag, not name\n  (bind isame (< (dist iorg InspectPoint) (R InspectJump)))\n"
patch('shm_src.py', OLD2, NEW2, 'V2.26 I4: tag, not name')
OLD3 = "  (set InspectPoint (selv (and cand (not isame)) iip (selv cand (+ InspectPoint (vscale (- iip InspectPoint) (min 1.0 (* dt 6.0)))) InspectPoint)))\n"
NEW3 = "  (set InspectPoint (selv (and cand (not isame)) iorg (selv cand (+ InspectPoint (vscale (- iorg InspectPoint) (min 1.0 (* dt 6.0)))) InspectPoint)))   ; V2.26 I4 origin\n"
patch('shm_src.py', OLD3, NEW3, 'V2.26 I4 origin')
OLD4 = "  (set InspectMatch (select (and ihok imatch) 1.0 0.0))\n"
NEW4 = "  (set InspectMatch (select (and ihok itag) 1.0 0.0))\n  (set InspectHitActorName (select ihok (İşlevsellikler|GetObjectName :Object iact) \"\"))\n"
patch('shm_src.py', OLD4, NEW4, 'InspectHitActorName (select')
OLD5 = "  (set CamOffset (+ CamOffset (vscale ishare (* InspectOn (R InspectShare)))))\n"
NEW5 = ("  ; V2.26 I4 framing split: the along-view part of the pivot share is closeness (InspectZoomOn); the view-lateral part is composition\n"
        "  (bind cfwH (normal (vec (.x cfw3) (.y cfw3) 0.0)))\n"
        "  (bind ishareAlong (vscale cfwH (dot ishare cfwH)))\n"
        "  (bind ishareLat (- ishare ishareAlong))\n"
        "  (set CamOffset (+ CamOffset (vscale (+ ishareLat (selv (R InspectZoomOn) ishareAlong (vec 0.0 0.0 0.0))) (* InspectOn (R InspectShare)))))\n")
patch('shm_src.py', OLD5, NEW5, 'V2.26 I4 framing split')
OLD6 = "(lerp 1.0 (R InspectBoom) InspectOn)))   ; V2.25 inspect boom\n"
NEW6 = "(lerp 1.0 (select (R InspectZoomOn) (R InspectBoom) 1.0) InspectOn)))   ; V2.25 inspect boom, V2.26 gated by InspectZoomOn\n"
patch('shm_src.py', OLD6, NEW6, 'V2.26 gated by InspectZoomOn')
print('done')
