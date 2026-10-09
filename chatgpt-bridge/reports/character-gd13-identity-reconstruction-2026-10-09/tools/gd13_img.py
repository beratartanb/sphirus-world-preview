"""GD13 image IO helpers for Blender python (no PIL): load/save PNG/JPG as numpy (H, W, 4) float32, row 0 = top."""
import bpy, numpy as np, os
def load(path):
    im = bpy.data.images.load(os.path.abspath(path), check_existing=False); im.colorspace_settings.name = 'Non-Color'
    W, H = im.size; a = np.empty(W*H*4, np.float32); im.pixels.foreach_get(a); bpy.data.images.remove(im)
    return a.reshape(H, W, 4)[::-1].copy()
def save(path, arr, quality=92):
    arr = np.asarray(arr, np.float32)
    if arr.ndim == 2: arr = np.stack([arr]*3, -1)
    if arr.shape[2] == 3: arr = np.concatenate([arr, np.ones(arr.shape[:2]+(1,), np.float32)], -1)
    H, W = arr.shape[:2]; im = bpy.data.images.new('tmp_out', W, H, alpha=True, float_buffer=False); im.colorspace_settings.name = 'Non-Color'
    im.pixels.foreach_set(np.clip(arr[::-1], 0, 1).ravel()); ext = os.path.splitext(path)[1].lower()
    sc = bpy.context.scene; s = sc.render.image_settings; s.file_format = 'JPEG' if ext in ('.jpg', '.jpeg') else 'PNG'; s.color_mode = 'RGB'
    if s.file_format == 'JPEG': s.quality = quality
    s.color_management = 'OVERRIDE'; s.view_settings.view_transform = 'Standard'; s.display_settings.display_device = 'sRGB'
    im.save_render(os.path.abspath(path), scene=sc); bpy.data.images.remove(im)
def resize(arr, W, H):
    """bilinear resize (numpy)"""
    h, w = arr.shape[:2]; ys = (np.arange(H)+0.5)*h/H-0.5; xs = (np.arange(W)+0.5)*w/W-0.5
    y0 = np.clip(np.floor(ys).astype(int), 0, h-1); x0 = np.clip(np.floor(xs).astype(int), 0, w-1); y1 = np.clip(y0+1, 0, h-1); x1 = np.clip(x0+1, 0, w-1)
    fy = np.clip(ys-y0, 0, 1)[:, None, None]; fx = np.clip(xs-x0, 0, 1)[None, :, None]
    return (arr[y0][:, x0]*(1-fy)*(1-fx)+arr[y0][:, x1]*(1-fy)*fx+arr[y1][:, x0]*fy*(1-fx)+arr[y1][:, x1]*fy*fx).astype(np.float32)
