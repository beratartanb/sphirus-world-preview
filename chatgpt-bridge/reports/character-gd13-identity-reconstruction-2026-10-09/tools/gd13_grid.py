"""GD13: labelled pixel-grid crops for manual landmark picking. Coordinates are PANEL-ORIGINAL pixels (483 x 541 panels).
usage: blender -b --factory-startup --python gd13_grid.py -- <panel.png> <out.jpg> x0 y0 x1 y1 [zoom=4] [step=5] [points.json:view]
Lines every <step> px (dim), every 5*step px (bright, labelled on the top / left margin). Optional points drawn as small crosses."""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(__file__)); import gd13_img as gi
a = sys.argv[sys.argv.index('--')+1:]; SRC, OUT = a[0], a[1]; x0, y0, x1, y1 = [float(v) for v in a[2:6]]
Z = int(a[6]) if len(a) > 6 else 4; ST = float(a[7]) if len(a) > 7 else 5.0; PTS = a[8] if len(a) > 8 else None
FONT = {'0': '111101101101111', '1': '010110010010111', '2': '111001111100111', '3': '111001111001111', '4': '101101111001001', '5': '111100111001111',
        '6': '111100111101111', '7': '111001010010010', '8': '111101111101111', '9': '111101111001111', '-': '000000111000000', '.': '000000000000010'}
def text(img, s, x, y, col, sc=3):
    for ch in s:
        g = FONT.get(ch)
        if g:
            for k, b in enumerate(g):
                if b == '1': img[y+(k//3)*sc:y+(k//3+1)*sc, x+(k % 3)*sc:x+(k % 3+1)*sc, :3] = col
        x += 4*sc
A = gi.load(SRC); H, W = A.shape[:2]
xs = np.arange(int(x0*Z), int(x1*Z))/Z; ys = np.arange(int(y0*Z), int(y1*Z))/Z
xi = np.clip(xs.astype(int), 0, W-1); yi = np.clip(ys.astype(int), 0, H-1)   # nearest (keep pixels honest)
C = A[yi][:, xi].copy(); M = 34; out = np.full((C.shape[0]+M, C.shape[1]+M+18, 4), 0.12, np.float32); out[..., 3] = 1; out[M:, M+18:] = C
for v in np.arange(np.ceil(x0/ST)*ST, x1, ST):
    px = int(round((v-x0)*Z))+M+18; big = abs(v/(5*ST)-round(v/(5*ST))) < 1e-6
    out[M:, px, :3] = out[M:, px, :3]*0.4+np.array([0.1, 1.0, 0.2] if big else [0.0, 0.7, 1.0])*0.6 if big else out[M:, px, :3]*0.75+np.array([0, 0.7, 1.0])*0.25
    if big: text(out, str(int(v)), px-8, 6, [1, 1, 0.3])
for v in np.arange(np.ceil(y0/ST)*ST, y1, ST):
    py = int(round((v-y0)*Z))+M; big = abs(v/(5*ST)-round(v/(5*ST))) < 1e-6
    out[py, M+18:, :3] = out[py, M+18:, :3]*0.4+np.array([0.1, 1.0, 0.2])*0.6 if big else out[py, M+18:, :3]*0.75+np.array([0, 0.7, 1.0])*0.25
    if big: text(out, str(int(v)), 1, py-7, [1, 1, 0.3], 3)
if PTS:
    f, vw = PTS.rsplit(':', 1) if not PTS.endswith('.json') else (PTS, None); P = json.load(open(f)); P = P.get(vw, P) if vw else P
    flat = []
    for k, p in P.items():
        if isinstance(p, list) and len(p) == 2 and not isinstance(p[0], list): flat.append(p)
        elif isinstance(p, list): flat += [q for q in p if isinstance(q, list) and len(q) == 2]
    for p in flat:
        px = int(round((p[0]-x0)*Z))+M+18; py = int(round((p[1]-y0)*Z))+M
        for d in range(-2, 3):
            for (yy, xx) in ((py, px+d), (py+d, px)):
                if M <= yy < out.shape[0] and M+18 <= xx < out.shape[1]: out[yy, xx, :3] = [1, 0.1, 0.8]
gi.save(OUT, out); print('GRID_OK', OUT, out.shape)
