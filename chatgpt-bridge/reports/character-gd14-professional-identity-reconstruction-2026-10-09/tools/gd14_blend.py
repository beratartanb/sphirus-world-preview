"""GD14: 50/50 blend + edge overlay of the 2x reference panel and a warped UE capture (same frame). usage: -- <view> <ue.png> <out.png> [rect x0 y0 x1 y1]"""
import sys, os, numpy as np
sys.path.insert(0, r'C:\Users\berat\OneDrive\Documents\Unreal Projects\ActionAdventureMovementS\Saved\Codex\GD13_Identity_20261009\tools'); import gd13_img as gi; from gd13_common import ROOT
a = sys.argv[sys.argv.index('--')+1:]; V, U, OUT = a[:3]; R = [int(x) for x in a[3:7]] if len(a) >= 7 else None
A = gi.load(f'{ROOT}/SourceAssets/Characters/GD13_IdentityMaster_20261009/references/GD13_REF_panel_{V}.png'); A = gi.resize(A, A.shape[1]*2, A.shape[0]*2); B = gi.load(U)
def edges(I):
    g = I[..., :3].mean(-1); gx = np.abs(np.roll(g, 1, 1)-np.roll(g, -1, 1)); gy = np.abs(np.roll(g, 1, 0)-np.roll(g, -1, 0)); return np.clip((gx+gy)*4, 0, 1)
M = A.copy(); M[..., :3] = 0.5*A[..., :3]+0.5*B[..., :3]
E = A.copy(); E[..., :3] = A[..., :3]*0.55; eb = edges(B); E[..., 0] = np.maximum(E[..., 0], eb); E[..., 1] = np.maximum(E[..., 1], eb*0.9)
O = np.concatenate([M, E], 1) if R is None else np.concatenate([M[R[1]:R[3], R[0]:R[2]], E[R[1]:R[3], R[0]:R[2]]], 1)
gi.save(OUT, O); print('BLEND_OK', OUT)
