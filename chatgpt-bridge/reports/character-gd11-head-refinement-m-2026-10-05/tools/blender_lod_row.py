"""LOD distance row: centre-square crops of <prefix>_{f,d,b}_<dist>_custom.png (8 distances x 3 directions), half resolution, into one image.
usage: blender -b --factory-startup --python blender_lod_row.py -- <captures dir> <prefix> <out.png>"""
import bpy, sys, os, numpy as np
a = sys.argv[sys.argv.index('--')+1:]; C, PFX, OUT = a[0], a[1], a[2]; ims = []
for k in ('f', 'd', 'b'):
    row = []
    for d in (125, 300, 600, 900, 1200, 1600, 2000, 2500):
        im = bpy.data.images.load(os.path.join(C, '%s_%s_%d_custom.png' % (PFX, k, d))); w, h = im.size; A = np.array(im.pixels[:], np.float32).reshape(h, w, 4)[::-1]; bpy.data.images.remove(im)
        cx, cy = w//2, h//2; s = min(w, h)//2; row.append(A[cy-s:cy+s, cx-s:cx+s][::2, ::2])
    ims.append(np.concatenate(row, 1))
G = np.concatenate(ims, 0); o = bpy.data.images.new('o', G.shape[1], G.shape[0]); o.pixels.foreach_set(np.ascontiguousarray(G[::-1]).ravel()); o.filepath_raw = os.path.abspath(OUT); o.file_format = 'PNG'; o.save(); print('LODROW', G.shape, OUT)
