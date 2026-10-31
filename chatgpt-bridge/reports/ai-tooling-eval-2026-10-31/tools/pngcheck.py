# independent PNG decode (zlib + PNG filters, pure Python/numpy) to validate the System.Drawing raw conversion
import struct, sys, zlib, numpy as np
d = open(sys.argv[1], 'rb').read(); i = 8; idat = b''
while i < len(d):
    n, t = struct.unpack('>I4s', d[i:i+8])
    if t == b'IHDR': w, h, bd, ct = struct.unpack('>IIBB', d[i+8:i+18])
    if t == b'IDAT': idat += d[i+8:i+8+n]
    i += 12 + n
raw = zlib.decompress(idat); bpp = 4; stride = w * bpp
out = np.zeros((h, stride), np.uint8); prev = np.zeros(stride, np.int32); filt = []
for y in range(h):
    f = raw[y*(stride+1)]; line = np.frombuffer(raw, np.uint8, stride, y*(stride+1)+1).astype(np.int32); filt.append(f)
    if f == 0: cur = line
    elif f == 2: cur = (line + prev) & 255
    elif f == 1:
        cur = line.reshape(w, bpp).cumsum(0).reshape(-1) & 255
    else:
        cur = np.zeros(stride, np.int32); L = line.tolist(); P = prev.tolist(); C = [0]*stride
        for x in range(stride):
            a = C[x-bpp] if x >= bpp else 0; b = P[x]; c = P[x-bpp] if x >= bpp else 0
            if f == 3: C[x] = (L[x] + ((a + b) >> 1)) & 255
            else:
                p = a + b - c; pa, pb, pc = abs(p-a), abs(p-b), abs(p-c)
                C[x] = (L[x] + (a if pa <= pb and pa <= pc else (b if pb <= pc else c))) & 255
        cur = np.array(C, np.int32)
    out[y] = cur; prev = cur
img = out.reshape(h, w, 4)
r = open(sys.argv[2], 'rb').read(); rw, rh = struct.unpack('<ii', r[:8]); rr = np.frombuffer(r[8:], np.uint8).reshape(rh, rw, 3)[:, :, ::-1]
print('filters used', sorted(set(filt)), 'alpha min/max', img[..., 3].min(), img[..., 3].max())
print('max |png_rgb - raw_rgb| =', int(np.abs(img[..., :3].astype(int) - rr.astype(int)).max()))
