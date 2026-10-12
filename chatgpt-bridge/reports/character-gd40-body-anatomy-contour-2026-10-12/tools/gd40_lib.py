"""GD40 shared helpers: current body state (accepted_b2 + BR_Neutral v6 + LK_Neutral), skin-weight chains, true planar cross sections
(triangle-edge / plane intersections, not vertex slabs), Laplacian neighbourhood, smoothstep. Bind space UE cm (x = subject's left,
y = front, z = up); x is returned relative to the midline MX = -0.23."""
import json, gzip, numpy as np
MX = -0.23
def ss(v): v = np.clip(v, 0, 1); return v*v*(3-2*v)
def nrm(v): v = np.asarray(v, float); return v/max(np.linalg.norm(v), 1e-9)
class Body:
    def __init__(self, pkg_path, lk_path, extra=None):
        P = json.loads(gzip.open(pkg_path, 'rb').read()); self.P = P; self.NB = NB = P['NB']
        XALL = np.asarray(P['br_neutral'], np.float64); X = XALL[:NB].copy()
        for k, v in json.load(open(lk_path))['Body']['LK_Neutral'].items(): X[int(k)] += v
        if extra:
            for name, dd in json.load(open(extra))['Body'].items():
                for k, v in dd.items(): X[int(k)] += v
        self.X = X; self.XR = X-np.array([MX, 0, 0]); self.T = np.asarray(P['body']['triangles'], np.int64)
        self.ZTOP = float(XALL[:, 2].max()); self.H = self.ZTOP-float(XALL[:, 2].min())
        W8 = P['weights']
        def chain(pre): return np.asarray([sum(w for b, w in W8[v].items() if b.startswith(pre)) for v in range(NB)])
        self.arm = chain(('upperarm', 'lowerarm', 'hand', 'clavicle', 'index', 'middle', 'ring', 'pinky', 'thumb')); self.leg = chain(('thigh', 'calf', 'foot', 'ball'))
        self.hand = chain(('hand', 'index', 'middle', 'ring', 'pinky', 'thumb')); self.uarm = chain(('upperarm',))
        T = self.T; E = np.unique(np.sort(np.r_[T[:, [0, 1]], T[:, [1, 2]], T[:, [2, 0]]], 1), axis=0); self.E = E
        nbr = [[] for _ in range(NB)]
        for a, b in E: nbr[a].append(b); nbr[b].append(a)
        self.NBR = [np.asarray(n, np.int64) for n in nbr]
        self.weld = np.asarray(P['weld_pairs'])[:, 0]
        B = P['skeleton']['Body']['bind']; self.bone = lambda b: np.asarray(B[b]['translation'], float)-np.array([MX, 0, 0])
    def normals(self, XR=None):
        XR = self.XR if XR is None else XR; T = self.T
        fn = -np.cross(XR[T[:, 1]]-XR[T[:, 0]], XR[T[:, 2]]-XR[T[:, 0]]); N = np.zeros_like(XR)
        for k in range(3): np.add.at(N, T[:, k], fn)
        return N/np.maximum(np.linalg.norm(N, axis=1), 1e-9)[:, None]
    def lap(self, F):
        acc = np.zeros_like(F); cnt = np.zeros(len(F))
        for a, b in self.E: pass
        return None
    def smooth_field(self, D, it=1, w=0.5):
        E = self.E; I0 = np.r_[E[:, 0], E[:, 1]]; I1 = np.r_[E[:, 1], E[:, 0]]; deg = np.bincount(I0, minlength=len(D)).astype(float)
        for _ in range(it):
            acc = np.zeros_like(D); np.add.at(acc, I0, D[I1]); D = (1-w)*D+w*acc/np.maximum(deg, 1)[:, None]
        return D
    def section(self, zz, mask, XR=None):
        """planar cross section points (x_rel, y) at height zz over edges whose both ends satisfy mask"""
        XR = self.XR if XR is None else XR; E = self.E; ok = mask[E[:, 0]] & mask[E[:, 1]]
        za, zb = XR[E[ok, 0], 2], XR[E[ok, 1], 2]; cross = ((za-zz)*(zb-zz) < 0); e = E[ok][cross]
        t = (zz-XR[e[:, 0], 2])/(XR[e[:, 1], 2]-XR[e[:, 0], 2]); p = XR[e[:, 0]]+t[:, None]*(XR[e[:, 1]]-XR[e[:, 0]]); return p[:, :2]
    def extents(self, zz, mask, XR=None):
        p = self.section(zz, mask, XR)
        if len(p) < 4: return (np.nan,)*4
        return (float(p[:, 1].max()), float(p[:, 1].min()), float(p[:, 0].max()), float(p[:, 0].min()))   # front, back, xmax, xmin
