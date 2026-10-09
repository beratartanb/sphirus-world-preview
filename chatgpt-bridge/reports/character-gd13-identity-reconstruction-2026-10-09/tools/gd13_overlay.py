"""GD13 overlay: reference panel (2x) | candidate render | 50 % blend, with the candidate silhouette (alpha edge, magenta) drawn on panes 1 and 3.
usage: -- <ref panel png> <render png> <alpha render png> <out jpg> [label]"""
import sys, os, numpy as np
sys.path.insert(0, os.path.dirname(__file__)); import gd13_img as gi
a = sys.argv[sys.argv.index('--')+1:]; R = gi.load(a[0]); C = gi.load(a[1]); A = gi.load(a[2])
R = gi.resize(R, C.shape[1], C.shape[0]); al = A[..., 3] > 0.5
e = al ^ (np.roll(al, 1, 0) & np.roll(al, -1, 0) & np.roll(al, 1, 1) & np.roll(al, -1, 1)); e &= al
def mark(I):
    I = I.copy(); I[e, :3] = [1, 0.1, 0.85]; return I
B = R*0.5+C*0.5
gi.save(a[3], np.concatenate([mark(R), C, mark(B)], 1)); print('OVL_OK', a[3])
