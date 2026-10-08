"""pass XX: skin basecolor x19 from T_LK_Head_BC_k9b (source untouched). k9b carries deliberate mid-scale darkening (UNDEREYE 0.12, PLANE_TONE
0.06 at the lid-cheek junction / nasolabial plane, SUN on the cheekbones) that reads as hollows and hard 'muscle' shapes in game light.
Mid-scale tone (Gaussian ~12 px @1K) relative to the broad tone (~60 px @1K) is evened in the face: darker-than-surroundings areas are lifted
(G_LIFT), lighter ones lowered a little (G_DARK); pores / freckles / spots (fine scale) and the broad colour are kept, face mean luminance
preserved. Lips, lids, nostrils, brows, ears and the collar band are excluded (soft UV ellipses, same layout as blender_gd4_skin.py).
usage: blender -b --factory-startup --python blender_g11xx_skinbc.py -- <BC in png> <BC out png> [G_LIFT=0.8] [G_DARK=0.4]"""
import bpy, sys, os, json, numpy as np
a = sys.argv[sys.argv.index('--')+1:]; GL = float(a[2]) if len(a) > 2 else 0.8; GD = float(a[3]) if len(a) > 3 else 0.4
im = bpy.data.images.load(os.path.abspath(a[0])); w, h = im.size; BC = np.asarray(im.pixels[:], np.float32).reshape(h, w, im.channels)[::-1, :, :3].copy(); bpy.data.images.remove(im)
n = h
def sstep(t): t = np.clip(t, 0, 1); return t*t*(3-2*t)
def blur(z, s):
    hh, ww = z.shape; fy = np.fft.fftfreq(hh)[:, None]; fx = np.fft.rfftfreq(ww)[None, :]
    return np.fft.irfft2(np.fft.rfft2(z)*np.exp(-2*(np.pi*s)**2*(fx*fx+fy*fy)), s=(hh, ww)).astype(np.float32)
v, u = (np.mgrid[0:n, 0:n].astype(np.float32)+0.5)/n
def el(cu, cv, ru, rv, mirror=False):
    m = sstep(1-np.sqrt(((u-cu)/ru)**2+((v-cv)/rv)**2))
    if mirror: m = np.maximum(m, sstep(1-np.sqrt(((u-(1-cu))/ru)**2+((v-cv)/rv)**2)))
    return m
face = sstep(1-np.sqrt(((u-0.5)/0.36)**2+((v-0.47)/0.34)**2)); collar = 1-sstep((v-0.80)/0.06)
excl = np.maximum.reduce([el(0.5, 0.595, 0.105, 0.042), el(0.385, 0.375, 0.07, 0.03, True), el(0.465, 0.46, 0.024, 0.02, True),
                          el(0.385, 0.335, 0.085, 0.026, True), el(0.15, 0.47, 0.07, 0.12, True)])
W = face*collar*(1-excl); L0 = BC@np.array([0.2126, 0.7152, 0.0722], np.float32)
if float(os.environ.get('UNDO_K9', '1')) > 0:   # exact inverse of the k9 darkening layers (blender_gd4_skin.py, k9 params UNDEREYE 0.12, PLANE_TONE 0.06, SUN 0.5, AGE_BC 0.05)
    ue = float(os.environ.get('UNDO_UNDEREYE', '0.12')); ptn = float(os.environ.get('UNDO_PLANE', '0.06')); sunk = float(os.environ.get('UNDO_SUN', '0.5')); ageb = float(os.environ.get('UNDO_AGE', '0.05'))
    lid = el(0.385, 0.375, 0.07, 0.03, True)
    infra = np.maximum(sstep(1-np.sqrt(((u-0.385)/0.075)**2+((v-0.425)/0.028)**2)), sstep(1-np.sqrt(((u-0.615)/0.075)**2+((v-0.425)/0.028)**2)))*(1-lid)
    BC = BC/np.maximum(1-(infra*ue)[..., None]*np.array([0.9, 1.05, 0.85], np.float32), 0.5)
    pt = (el(0.40, 0.445, 0.07, 0.022, True)*0.8+el(0.405, 0.555, 0.022, 0.06, True))*ptn
    BC = BC/np.maximum(1-pt[..., None]*np.array([0.85, 1.0, 1.05], np.float32), 0.5)
    sun = np.clip(el(0.5, 0.24, 0.21, 0.10)*0.8+np.maximum(el(0.5, 0.46, 0.055, 0.10), el(0.5, 0.505, 0.09, 0.045))*1.0+el(0.355, 0.445, 0.09, 0.05, True)*0.9+el(0.5, 0.40, 0.04, 0.06)*0.7, 0, 1)*(1-lid)
    cb = el(0.355, 0.445, 0.09, 0.05, True)*0.9*(1-lid)   # undo the sun tone on the cheekbones only (forehead / nose sun kept)
    BC = BC/np.maximum(1-(cb*sunk)[..., None]*(1-np.array([0.93, 0.92, 0.905], np.float32)), 0.5)
    AG = np.zeros((n, n), np.float32); wl = 0.0022
    for vv, amp in ((0.205, 0.8), (0.228, 1.0), (0.252, 0.7)):
        vline = vv+0.004*np.sin(u*31.0+vv*90); AG -= amp*np.exp(-((v-vline)/wl)**2)*sstep(1-np.abs(u-0.5)/0.13)*(0.6+0.4*np.sin(u*57.0+vv*40)**2)
    for uu in (0.487, 0.513): AG -= 0.9*np.exp(-((u-uu)/(wl*1.2))**2)*sstep(1-np.abs(v-0.312)/0.022)
    for uc in (0.385, 0.615):
        for dv, amp in ((0.0, 0.8), (0.009, 0.5)):
            arc = 0.418+dv+0.9*(u-uc)**2; AG -= amp*np.exp(-((v-arc)/(wl*0.9))**2)*sstep(1-np.abs(u-uc)/0.05)
    for uc, sg in ((0.405, 1), (0.595, -1)):
        line = uc-sg*0.35*(v-0.505); AG -= 0.6*np.exp(-((u-line)/(wl*2.5))**2)*sstep(1-np.abs(v-0.555)/0.06)
    agem = np.clip(-AG, 0, 1)*collar; agem[v < 0.30] *= float(os.environ.get('UNDO_AGE_FOREHEAD', '0'))   # forehead / glabella lines kept unless asked
    BC = BC/np.maximum(1-agem[..., None]*ageb, 0.5)
L = BC@np.array([0.2126, 0.7152, 0.0722], np.float32)
lo = blur(L, n/85.0); big = blur(L, n/17.0); rel = lo/np.maximum(big, 1e-4)
c = np.where(rel < 1, rel**(-GL), rel**(-GD)).astype(np.float32); c = np.clip(c, 0.85, 1.35)
out = BC*(1+W*(c-1))[..., None]
L2 = out@np.array([0.2126, 0.7152, 0.0722], np.float32); m = W > 0.5
k = float(L0[m].mean()/L2[m].mean())   # keep the ORIGINAL face mean (lifted darks, others a touch lower); out = out*(1+W*(k-1))[..., None]
rgba = np.ones((n, n, 4), np.float32); rgba[..., :3] = np.clip(out, 0, 1)
o = bpy.data.images.new(os.path.basename(a[1]), n, n, alpha=True, float_buffer=False); o.pixels.foreach_set(np.ascontiguousarray(rgba[::-1]).ravel())
o.filepath_raw = os.path.abspath(a[1]); o.file_format = 'PNG'; o.save()
f = n//1024; rel2 = blur(L2*k, n/85.0)/np.maximum(blur(L2*k, n/17.0), 1e-4)
st = {'G_LIFT': GL, 'G_DARK': GD, 'mean_keep_k': k, 'rel_before_p05_p95_face': [float(np.percentile(rel[m], 5)), float(np.percentile(rel[m], 95))],
      'rel_after_p05_p95_face': [float(np.percentile(rel2[m], 5)), float(np.percentile(rel2[m], 95))]}
json.dump(st, open(os.path.abspath(a[1]).replace('.png', '_stats.json'), 'w'), indent=1); print('SKINBC', json.dumps(st))
