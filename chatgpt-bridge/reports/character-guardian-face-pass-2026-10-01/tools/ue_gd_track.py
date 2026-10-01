"""GUARDIAN face pass: run the MetaHuman face contour tracker (track_face_landmarks_from_image, NNE models) on raw BGRA images.
builtins.GD_TRACK = [(bin path, w, h, out json), ...] -> json {curve name: [[x, y], ...]} (image space, top-left origin)"""
import unreal as u, json, builtins
S = u.get_editor_subsystem(u.MetaHumanCharacterEditorSubsystem); rep = {}
for path, w, h, outp in builtins.GD_TRACK:
    b = open(path, 'rb').read(); assert len(b) == w*h*4, (len(b), w, h)
    px = [u.Color(b[i+2], b[i+1], b[i], b[i+3]) for i in range(0, len(b), 4)]
    r = S.track_face_landmarks_from_image(px, w, h)
    if r is None: rep[outp] = 'NO FACE'; continue
    curves = {}
    for k, tp in r.items():
        pts = None
        for attr in ('tracking_points', 'points'):
            try: pts = tp.get_editor_property(attr); break
            except Exception: pass
        if pts is None: pts = []
        curves[str(k)] = [[round(p.x, 2), round(p.y, 2)] for p in pts]
    open(outp, 'w').write(json.dumps(curves)); rep[outp] = {k: len(v) for k, v in curves.items()}
print('GD_TRACK', json.dumps(rep))
