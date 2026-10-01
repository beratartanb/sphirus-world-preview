"""GUARDIAN face pass: PNG -> raw BGRA8 bytes (top-left origin) for unreal track_face_landmarks_from_image.
usage: blender -b --factory-startup --python blender_gd_png2bgra.py -- <in.png> <out.bin> [<in2.png> <out2.bin> ...]  (prints DIMS name w h)"""
import bpy, sys, numpy as np
a = sys.argv[sys.argv.index('--')+1:]
for i in range(0, len(a), 2):
    im = bpy.data.images.load(a[i]); w, h = im.size; x = np.asarray(im.pixels[:], np.float32).reshape(h, w, im.channels)[::-1]
    if im.channels == 3: x = np.concatenate([x, np.ones((h, w, 1), np.float32)], -1)
    if im.colorspace_settings.name != 'Non-Color': pass   # pixels are already display (sRGB) values for 8-bit PNG
    b = (np.clip(x, 0, 1)*255+0.5).astype(np.uint8)[..., [2, 1, 0, 3]]; open(a[i+1], 'wb').write(b.tobytes()); print('DIMS', a[i+1], w, h)
