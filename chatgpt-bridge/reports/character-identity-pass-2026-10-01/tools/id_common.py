"""IDENTITY pass shared helpers (numpy; used from Blender scripts): package / export loading, similarity alignment."""
import json, gzip, numpy as np
PKG = 'Saved/Codex/CharacterFinal_20260929/sculpt_package_v6.json.gz'; I = 'Saved/Codex/CharacterIdentity_20260930'
SEG = {'skin': (0, 24049), 'teeth': (24049, 28295), 'saliva': (28295, 28955), 'eyeL': (28955, 29725), 'eyeR': (29725, 30495), 'eyeshell': (30495, 31047), 'lashes': (31047, 33191), 'eyeEdge': (33191, 33459), 'cartilage': (33459, 33845)}
_P = None
def pkg():
    global _P
    if _P is None: _P = json.loads(gzip.open(PKG, 'rb').read())
    return _P
def head_base():   # accepted_b2 head = UE face LOD0 base (package / GeometryScript order)
    P = pkg(); return np.asarray(P['accepted_b2'], np.float64)[P['NB']:]
def head_brn():    # base + original BR_Neutral (collar)
    P = pkg(); return np.asarray(P['br_neutral'], np.float64)[P['NB']:]
def export_lod(name, lod=0): return np.asarray(json.load(open(f'{I}/export_{name}.json'))[str(lod)], np.float64)
def umeyama(src, dst, scale=True):
    ms, md = src.mean(0), dst.mean(0); a, b = src-ms, dst-md; C = b.T@a/len(src); U, S, Vt = np.linalg.svd(C); D = np.eye(3); D[2, 2] = np.sign(np.linalg.det(U@Vt))
    R = U@D@Vt; s = (S*np.diag(D)).sum()/(a**2).sum()*len(src) if scale else 1.0; t = md-s*R@ms; return s, R, t
def apply(T, X): s, R, t = T; return s*(X@R.T)+t
