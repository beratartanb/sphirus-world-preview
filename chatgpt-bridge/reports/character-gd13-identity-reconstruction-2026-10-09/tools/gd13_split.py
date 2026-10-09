"""split the user's GD13 6-view sheet (1448x1086, panels abut: x 0|483|966|1448, y 0|541|1086) into named panels (+ x2 bilinear for the tracker)"""
import sys, os, numpy as np
sys.path.insert(0, os.path.dirname(__file__)); import gd13_img as gi
a = sys.argv[sys.argv.index('--')+1:]; SRC, OUTD, OUTD2 = a[0], a[1], a[2]
A = gi.load(SRC); X = [0, 483, 966, 1448]; Y = [0, 541, 1086]
names = {(0, 0): 'front', (1, 0): 'q3_faceR', (2, 0): 'q3_faceL', (0, 1): 'prof_faceL', (1, 1): 'rear34_faceR', (2, 1): 'back'}
for (i, j), n in names.items():
    P = A[Y[j]:Y[j+1], X[i]:X[i+1]]; gi.save(f'{OUTD}/GD13_REF_panel_{n}.png', P); P2 = gi.resize(P, P.shape[1]*2, P.shape[0]*2); gi.save(f'{OUTD2}/ref_{n}_x2.png', P2)
    print('PANEL', n, P.shape[1], P.shape[0])
