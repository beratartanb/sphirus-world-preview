import sys, os, json, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Saved/Codex/GD13_Identity_20261009/tools')); from gd13_common import NS, MX, mirror_map, pkg
MM = mirror_map()[:NS]; mutual = MM[MM] == np.arange(NS); print('MMCHECK mutual pairs %.1f %% | self-mapped %d | unique targets %d of %d' % (100*mutual.mean(), (MM == np.arange(NS)).sum(), len(np.unique(MM)), NS))
UV = None
try:
    P = pkg()['head']; T = np.asarray(P['triangles']); UVc = np.asarray(P['uv']); U = np.zeros((NS, 2)); C = np.zeros(NS)
    for k in range(3):
        m = T[:, k] < NS; np.add.at(U, T[m, k], UVc[m, k]); np.add.at(C, T[m, k], 1)
    U = U/np.maximum(C, 1)[:, None]; print('MMCHECK uv range u %.3f..%.3f v %.3f..%.3f' % (U[:, 0].min(), U[:, 0].max(), U[:, 1].min(), U[:, 1].max()))
    d = np.abs(U[MM, 0]-(1-U[:, 0]))+np.abs(U[MM, 1]-U[:, 1]); print('MMCHECK uv-mirror residual of MM: median %.4f p95 %.4f max %.4f' % (np.median(d), np.percentile(d, 95), d.max()))
except Exception as e: print('MMCHECK uv fail', e)
