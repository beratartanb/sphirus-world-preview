import sys, os, json, numpy as np
sys.path.insert(0, sys.argv[sys.argv.index('--')+1]); from gd42_lib import Body, ss, nrm, MX
a = sys.argv[sys.argv.index('--')+2:]; B = Body(a[0], a[1], extra=a[2]); XR = B.XR; x, y, z = XR.T
A = np.asarray(B.P['breast_apex']['l'])-np.array([MX, 0, 0]); d = np.linalg.norm(XR-A, axis=1); near = np.argsort(d)[:12]
print('nearest to apex:', [(np.round(XR[i], 1).tolist(), round(float(B.arm[i]), 2), round(float(B.leg[i]), 2)) for i in near])
sel = (x > 4) & (x < 16) & (z > 121) & (z < 136) & (y > 4); print('box verts', sel.sum(), 'arm pct', np.round(np.percentile(B.arm[sel], [5, 50, 95]), 2) if sel.any() else None)
i = np.argmax(y*sel) if sel.any() else None; print('box max-y vert', np.round(XR[i], 2) if i is not None else None)
sel2 = (x > 4) & (x < 16) & (z > 121) & (z < 136); print('box verts any y', sel2.sum(), 'y pct', np.round(np.percentile(y[sel2], [5, 50, 95]), 1))
print('weights keys', list(B.P['weights'].keys())[:5] if isinstance(B.P.get('weights'), dict) else type(B.P.get('weights')))
