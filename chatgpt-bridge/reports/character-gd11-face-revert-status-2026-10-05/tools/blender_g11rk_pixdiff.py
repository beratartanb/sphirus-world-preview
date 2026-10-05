"""GD11 K revert proof: mean absolute pixel difference between same-camera captures. usage: blender -b --factory-startup --python blender_g11rk_pixdiff.py -- <captures dir> <A prefix> <B prefix> <C prefix> <view> [...]"""
import bpy, sys, os, numpy as np
a = sys.argv[sys.argv.index('--')+1:]; C, PA, PB, PC = a[:4]; views = a[4:]
def L(n):
    im = bpy.data.images.load(os.path.join(C, n+'_custom.png')); w, h = im.size; A = np.array(im.pixels[:], np.float32).reshape(h, w, 4)[::-1, :, :3]; bpy.data.images.remove(im); return A
for v in views:
    A = L(PA+'_'+v); B = L(PB+'_'+v); Cc = L(PC+'_'+v)
    print('PDIFF %s  A-vs-C mean abs %.4f (pixels >0.1: %d)   B-vs-C mean abs %.4f (pixels >0.1: %d)' % (v, np.abs(A-Cc).mean(), int((np.abs(A-Cc).max(2) > 0.1).sum()), np.abs(B-Cc).mean(), int((np.abs(B-Cc).max(2) > 0.1).sum())))
