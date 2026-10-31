"""pngtool.py: minimal PNG read/write (numpy, zlib) + 'crop' CLI: pngtool.py crop <in> <out> <ext x0 x1 y0 y1 cm> <cell cm> <crop x0 x1 y0 y1> <upscale>"""
import zlib, struct, sys
import numpy as np


def rpng(p):
    d = open(p, 'rb').read(); i = 8; w = h = 0; idat = b''; ct = 2
    while i < len(d):
        L = struct.unpack('>I', d[i:i + 4])[0]; t = d[i + 4:i + 8]; c = d[i + 8:i + 8 + L]
        if t == b'IHDR': w, h = struct.unpack('>II', c[:8]); ct = c[9]
        if t == b'IDAT': idat += c
        i += 12 + L
    nch = 4 if ct == 6 else 3
    raw = np.frombuffer(zlib.decompress(idat), np.uint8).reshape(h, w * nch + 1)
    assert (raw[:, 0] == 0).all(), 'filtered PNG not supported'
    return raw[:, 1:].reshape(h, w, nch)[..., :3].copy()


def wpng(p, a):
    h, w, _ = a.shape; raw = b''.join(b'\x00' + a[r].tobytes() for r in range(h))
    ch = lambda t, d: struct.pack('>I', len(d)) + t + d + struct.pack('>I', zlib.crc32(t + d) & 0xffffffff)
    open(p, 'wb').write(b'\x89PNG\r\n\x1a\n' + ch(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 2, 0, 0, 0)) + ch(b'IDAT', zlib.compress(raw, 6)) + ch(b'IEND', b''))


if __name__ == '__main__' and sys.argv[1] == 'crop':
    a = rpng(sys.argv[2]); ex = list(map(float, sys.argv[4:8])); cell = float(sys.argv[8]); cr = list(map(float, sys.argv[9:13])); up = int(sys.argv[13])
    c = a[int((cr[2] - ex[2]) / cell):int((cr[3] - ex[2]) / cell), int((cr[0] - ex[0]) / cell):int((cr[1] - ex[0]) / cell)]
    wpng(sys.argv[3], np.repeat(np.repeat(c, up, 0), up, 1)); print('CROP', sys.argv[3], c.shape)
