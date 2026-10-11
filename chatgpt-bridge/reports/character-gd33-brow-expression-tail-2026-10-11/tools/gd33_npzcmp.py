import sys, numpy as np
a = np.load(sys.argv[sys.argv.index('--')+1]); b = np.load(sys.argv[sys.argv.index('--')+2])
for k in a.files:
    print('NPZ', k, a[k].shape, b[k].shape, float(np.abs(a[k].astype(float)-b[k].astype(float)).max()) if a[k].shape == b[k].shape else 'shape differs')
