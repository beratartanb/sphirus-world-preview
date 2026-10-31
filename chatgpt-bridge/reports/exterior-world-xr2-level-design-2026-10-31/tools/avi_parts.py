"""avi_parts.py <frames_dir> <out_prefix> <capture_fps> <step> <max_mb> : Motion-JPEG AVI parts for publication (pure Python, no re-encode).
Every <step>-th JPEG frame is kept and played at capture_fps / step, so playback stays REAL SPEED; the clip is split into parts
<out_prefix>_partN.avi of at most <max_mb> MB each (GitHub file limit). Writer = Tools/SHME_V29_20261016/mjpeg_avi.py layout."""
import sys, struct, pathlib

src, pre, cfps, step, maxmb = pathlib.Path(sys.argv[1]), sys.argv[2], float(sys.argv[3]), int(sys.argv[4]), float(sys.argv[5])
frames = sorted(src.glob('*.jpg'))[::step]
assert frames, 'no frames'
fps = cfps / step


def jpeg_size(data):
    i = 2
    while i < len(data):
        if data[i] != 0xFF: i += 1; continue
        m = data[i + 1]
        if m in (0xC0, 0xC1, 0xC2):
            h, w = struct.unpack('>HH', data[i + 5:i + 9]); return w, h
        if m in (0xD8, 0x01) or 0xD0 <= m <= 0xD7: i += 2; continue
        i += 2 + struct.unpack('>H', data[i + 2:i + 4])[0]
    raise ValueError('no SOF')


def write(out, blobs):
    W, H = jpeg_size(blobs[0]); n = len(blobs); usec = int(round(1e6 / fps)); maxb = max(len(x) for x in blobs) + 8
    chunk = lambda fcc, d: fcc + struct.pack('<I', len(d)) + d + (b'\0' if len(d) % 2 else b'')
    lst = lambda fcc, d: b'LIST' + struct.pack('<I', len(d) + 4) + fcc + d
    avih = struct.pack('<IIIIIIIIII4I', usec, maxb * int(fps + 1), 0, 0x10, n, 0, 1, maxb, W, H, 0, 0, 0, 0)
    strh = b'vids' + b'MJPG' + struct.pack('<IHHIIIIIIIIhhhh', 0, 0, 0, 0, 1000, int(round(fps * 1000)), 0, n, maxb, 0xFFFFFFFF, 0, 0, 0, W, H)
    strf = struct.pack('<IiiHH4sIiiII', 40, W, H, 1, 24, b'MJPG', W * H * 3, 0, 0, 0, 0)
    hdrl = lst(b'hdrl', chunk(b'avih', avih) + lst(b'strl', chunk(b'strh', strh) + chunk(b'strf', strf)))
    movi = b''; idx = b''; off = 4
    for d in blobs:
        c = chunk(b'00dc', d); idx += b'00dc' + struct.pack('<III', 0x10, off, len(d)); movi += c; off += len(c)
    body = b'AVI ' + hdrl + lst(b'movi', movi) + chunk(b'idx1', idx)
    pathlib.Path(out).write_bytes(b'RIFF' + struct.pack('<I', len(body)) + body)
    print('AVI %s %dx%d frames %d play %.1f fps (%.1f s real) %.1f MB' % (out, W, H, n, fps, n / fps, pathlib.Path(out).stat().st_size / 1e6))


part, cur, size = 1, [], 0
for f in frames:
    b = f.read_bytes()
    if cur and size + len(b) > maxmb * 1e6 * 0.97:
        write('%s_part%d.avi' % (pre, part), cur); part += 1; cur, size = [], 0
    cur.append(b); size += len(b) + 16
if cur:
    write('%s_part%d.avi' % (pre, part), cur if part > 1 else cur)
