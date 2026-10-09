"""GD12 region surface differences: per anatomical region the signed displacement along the F1H surface normal (mm, + = outward / fuller),
mean / p95 / max |d|, and the mean displacement vector (lateral +x out, forward +y, up +z). usage: -- <F1H.npy> <GD12.npy> <out.txt>"""
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Tools/CharacterLookdev_20260930')); from id_common import pkg
a = sys.argv[sys.argv.index('--')+1:]; A = np.load(a[0])[:24049]; X = np.load(a[1])[:24049]; MX = -0.23
T = np.asarray(pkg()['head']['triangles']); T = T[(T < 24049).all(1)]; N = np.zeros_like(A); fn = -np.cross(A[T[:, 1]]-A[T[:, 0]], A[T[:, 2]]-A[T[:, 0]])
for k in range(3): np.add.at(N, T[:, k], fn)
N /= np.maximum(np.linalg.norm(N, axis=1), 1e-9)[:, None]
if (N[A[:, 1] > 12, 1]).mean() < 0: N = -N
D = X-A; dn = (D*N).sum(1)*10; ax = np.abs(A[:, 0]-MX); y, z = A[:, 1], A[:, 2]; sgn = np.sign(A[:, 0]-MX)
R = [('frontal (forehead)', (ax < 4.5) & (z > 165.6) & (z < 171) & (y > 8)), ('temporal', (ax > 4.8) & (ax < 7.5) & (z > 162) & (z < 168) & (y > 2) & (y < 9)),
     ('brow / supraorbital', (ax > 0.8) & (ax < 5.6) & (z > 163.6) & (z < 165.6) & (y > 9)), ('upper lid / hood', (ax > 1.8) & (ax < 4.6) & (z > 162.6) & (z < 163.8) & (y > 10)),
     ('lower lid / under-eye', (ax > 1.8) & (ax < 4.8) & (z > 160.4) & (z < 162.0) & (y > 10)), ('malar / zygomatic', (ax > 3.0) & (ax < 6.4) & (z > 158.2) & (z < 160.8) & (y > 7)),
     ('mid cheek', (ax > 3.2) & (ax < 6.0) & (z > 155.6) & (z < 158.2) & (y > 6)), ('lower cheek / jowl', (ax > 2.8) & (ax < 5.6) & (z > 151.5) & (z < 155.6) & (y > 5)),
     ('nasolabial', (ax > 1.8) & (ax < 3.4) & (z > 155.0) & (z < 158.3) & (y > 10.5)), ('nose tip / alae', (ax < 2.2) & (z > 157.6) & (z < 160.2) & (y > 12.3)),
     ('upper lip', (ax < 2.6) & (z > 155.1) & (z < 157.2) & (y > 12.4)), ('lower lip', (ax < 2.6) & (z > 153.9) & (z < 155.05) & (y > 12.2)),
     ('chin (mentum)', (ax < 2.6) & (z > 150.5) & (z < 153.6) & (y > 10.5)), ('mandibular body / angle', (ax > 3.0) & (ax < 6.6) & (z > 148.6) & (z < 151.8) & (y > 0)),
     ('submandibular', (ax > 1.5) & (ax < 5.5) & (z > 147.0) & (z < 149.4) & (y > 3))]
out = ['region | n | normal disp mean (mm) | |d| p95 | |d| max | mean vector lat/fwd/up (mm)']
for nm, m in R:
    v = D[m]*10; v[:, 0] *= sgn[m]; out.append('%-26s | %4d | %+5.2f | %4.2f | %4.2f | %+.2f / %+.2f / %+.2f' % (nm, m.sum(), dn[m].mean(), np.percentile(np.abs(dn[m]), 95), np.linalg.norm(D[m], axis=1).max()*10, *v.mean(0)))
d = np.linalg.norm(D, axis=1)*10; out.append('ALL moved verts (>0.05 mm) %d, max %.2f mm, mean of moved %.2f mm' % ((d > 0.05).sum(), d.max(), d[d > 0.05].mean()))
open(a[2], 'w').write('\n'.join(out)); print('\n'.join(out))
