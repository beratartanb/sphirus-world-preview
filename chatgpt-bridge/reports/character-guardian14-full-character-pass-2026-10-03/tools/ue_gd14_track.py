"""GUARDIAN-14: MetaHuman face contour tracker on images (reference photos and clay/real renders in the same review frame).
builtins.GD14_TR = {'images': {tag: abs png path}, 'out': abs json path}. Writes {tag: {size, curves: {name: [[x, y]..]}}}"""
import unreal as u, json, builtins
C = builtins.GD14_TR; S = u.get_editor_subsystem(u.MetaHumanCharacterEditorSubsystem); out = {}
for tag, p in C['images'].items():
    import struct, zlib
    raw = open(p, 'rb').read(); pos = 8; W = H = 0; idat = b''; ct = 0
    while pos < len(raw):
        ln, typ = struct.unpack('>I4s', raw[pos:pos+8]); dat = raw[pos+8:pos+8+ln]; pos += 12+ln
        if typ == b'IHDR': W, H, bd, ct = struct.unpack('>IIBB', dat[:10])
        elif typ == b'IDAT': idat += dat
    bpp = {2: 3, 6: 4}[ct]; d = zlib.decompress(idat); stride = W*bpp; rows = []; prev = bytearray(stride); i = 0
    for y in range(H):
        f = d[i]; line = bytearray(d[i+1:i+1+stride]); i += 1+stride
        for x in range(stride):
            a_ = line[x-bpp] if x >= bpp else 0; b_ = prev[x]; c_ = prev[x-bpp] if x >= bpp else 0
            if f == 1: line[x] = (line[x]+a_) & 255
            elif f == 2: line[x] = (line[x]+b_) & 255
            elif f == 3: line[x] = (line[x]+((a_+b_) >> 1)) & 255
            elif f == 4:
                pp = a_+b_-c_; pa, pb, pc = abs(pp-a_), abs(pp-b_), abs(pp-c_); line[x] = (line[x]+(a_ if pa <= pb and pa <= pc else (b_ if pb <= pc else c_))) & 255
        rows.append(line); prev = line
    px = []
    for r in rows:
        for x in range(W):
            c = u.Color(); c.r = r[x*bpp]; c.g = r[x*bpp+1]; c.b = r[x*bpp+2]; c.a = 255; px.append(c)
    res = S.track_face_landmarks_from_image(px, W, H)
    def pts(v):
        for at in ('points', 'positions', 'tracking_points'):
            try: return [[float(q.x), float(q.y)] for q in v.get_editor_property(at)]
            except Exception: pass
        return [x for x in dir(v) if not x.startswith('_')]
    out[tag] = {'size': [W, H], 'curves': {k: pts(v) for k, v in (res or {}).items()}}
open(C['out'], 'w').write(json.dumps(out)); print('GD14_TR', {k: len(v['curves']) for k, v in out.items()})
