"""landmark index map: front and side orthographic projections of the head skin (dots) with the MHC face landmarks numbered."""
import sys, os, json, numpy as np
sys.path.insert(0, r'C:\Users\berat\OneDrive\Documents\Unreal Projects\ActionAdventureMovementS\Saved\Codex\GD13_Identity_20261009\tools'); import gd13_img as gi
a = sys.argv[sys.argv.index('--')+1:]; X = np.fromfile(a[0], np.float32).reshape(-1, 3).astype(float); L = np.array(json.load(open(a[1]))); OUT = a[2]; E = np.load(a[3]) if len(a) > 3 else None
if E is not None: d = np.linalg.norm(X-E, axis=1); print('VS_E max %.3f mean %.4f' % (d.max(), d.mean()))
S = X[:24049]; m = (S[:, 2] > 148) & (S[:, 1] > -2)
FONT = {'0': '111101101101111', '1': '010110010010111', '2': '111001111100111', '3': '111001111001111', '4': '101101111001001', '5': '111100111001111', '6': '111100111101111', '7': '111001010010010', '8': '111101111101111', '9': '111101111001111'}
def text(img, s, x, y, col, sc=2):
    for ch in s:
        g = FONT.get(ch)
        if g:
            for k, b in enumerate(g):
                if b == '1': img[max(0, y+(k//3)*sc):y+(k//3+1)*sc, max(0, x+(k % 3)*sc):x+(k % 3+1)*sc, :3] = col
        x += 4*sc
def panel(u, v, flipu=False):
    W, H = 900, 1100; img = np.full((H, W, 4), 0.15, np.float32); img[..., 3] = 1
    u0, u1, v0, v1 = -9, 9, 146, 176; sc = min(W/(u1-u0), H/(v1-v0))
    def px(P): uu = (-P[:, u] if flipu else P[:, u]); return np.stack([(uu-u0)*sc, (v1-P[:, v])*sc], 1).astype(int)
    for p in px(S[m])[::2]:
        if 0 <= p[1] < H and 0 <= p[0] < W: img[p[1], p[0], :3] = 0.55
    for i, p in enumerate(px(L)):
        if 0 <= p[1] < H and 0 <= p[0] < W: img[max(p[1]-3, 0):p[1]+4, max(p[0]-3, 0):p[0]+4, :3] = [1, 0.2, 0.2]; text(img, str(i), p[0]+5, p[1]-6, [1, 1, 0.2])
    return img
F = panel(0, 2); Sd = panel(1, 2, True)
gi.save(OUT, np.concatenate([F, Sd], 1)); print('LMMAP_OK', len(L))
