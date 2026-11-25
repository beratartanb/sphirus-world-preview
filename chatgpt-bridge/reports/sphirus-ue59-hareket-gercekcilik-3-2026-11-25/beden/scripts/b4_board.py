# b4_board.py (Blender background): side-by-side boards (before | after) of clay renders. args: <dir> <out prefix>
import bpy, sys, os, numpy as np
D, P = sys.argv[sys.argv.index('--') + 1:][:2]
for v in ('front', 'side', 'back', 'front34'):
    a = bpy.data.images.load(os.path.join(D, 'clay_before_%s.png' % v)); b = bpy.data.images.load(os.path.join(D, 'clay_after_%s.png' % v))
    w, h = a.size; A = np.array(a.pixels[:]).reshape(h, w, 4); B = np.array(b.pixels[:]).reshape(h, w, 4)
    gap = np.ones((h, 12, 4)); gap[:, :, :3] = 0.15; C = np.concatenate([A, gap, B], axis=1)
    o = bpy.data.images.new('board_' + v, C.shape[1], h, alpha=True); o.pixels = C.ravel().tolist(); o.filepath_raw = os.path.join(D, '%s_%s.png' % (P, v)); o.file_format = 'PNG'; o.save()
open(os.path.join(D, P + '_done.txt'), 'w').write('ok')
