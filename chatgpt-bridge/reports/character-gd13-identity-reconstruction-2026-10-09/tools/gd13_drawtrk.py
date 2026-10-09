"""draw tracker curves (json {tag:{curves}}) on panels side by side (x2) -> one jpg. usage: -- <tracks.json> <panel dir> <out.jpg> tag1 tag2 ..."""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(__file__)); import gd13_img as gi
a = sys.argv[sys.argv.index('--')+1:]; T = json.load(open(a[0])); PD = a[1]; OUT = a[2]; tags = a[3:]
row = []
for t in tags:
    A = gi.load(f'{PD}/GD13_REF_panel_{t}.png'); A = gi.resize(A, A.shape[1]*2, A.shape[0]*2)
    for k, c in T[t]['curves'].items():
        col = [0, 1, 1] if 'eyelid' in k else ([1, 0.2, 0.8] if 'lip' in k else [1, 1, 0])
        P = np.asarray(c)*2
        for i in range(len(P)-1):
            for s in np.linspace(0, 1, 12):
                x, y = (P[i]*(1-s)+P[i+1]*s).astype(int)
                if 0 <= y < A.shape[0] and 0 <= x < A.shape[1]: A[y, x, :3] = col
        for p in P.astype(int):
            A[max(p[1]-1, 0):p[1]+2, max(p[0]-1, 0):p[0]+2, :3] = [1, 0, 0]
    row.append(A[:1082, :964])
gi.save(OUT, np.concatenate(row, 1)); print('DRAW_OK')
