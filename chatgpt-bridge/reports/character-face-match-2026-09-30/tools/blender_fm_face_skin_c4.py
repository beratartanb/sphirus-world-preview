"""FACE-MATCH pass §5 (isolated): facial skin maturity on top of the FINAL-ART v2 face textures (T_LK_Head_*_v2 -> *_c4).
Applied after the likeness geometry; supports it, never replaces it. On the MetaHuman head UV (measured on _prev_face_bc_v2):
  under-eye tear trough / lower-lid tone (brown-violet, slightly asymmetric), upper-lid crease shadow, mild nasolabial tone,
  forehead: sun-warm tone + faint horizontal lines (mostly in the normal map), glabella lines, crow's feet (normal),
  blotchy redness (nose sides, inner cheeks) instead of a uniform pink, lips muted (less saturated, rose-brown), pores untouched.
usage: blender -b --factory-startup --python blender_fm_face_skin_c4.py -- <v2 skin dir> <out dir>"""
import bpy, sys, os
import numpy as np
a = sys.argv[sys.argv.index('--')+1:]; D, O = a[0], a[1]; os.makedirs(O, exist_ok=True)
E = lambda k, d: float(os.environ.get(k, d))
def load(fn):
    im = bpy.data.images.load(os.path.join(D, fn)); w, h = im.size; x = np.asarray(im.pixels[:], np.float32).reshape(h, w, im.channels)[::-1].copy(); bpy.data.images.remove(im); return x   # top-left origin
def save(arr, name, lin):
    h, w = arr.shape[:2]; rgba = np.ones((h, w, 4), np.float32); rgba[..., :3] = np.clip(arr[::-1, :, :3], 0, 1)
    im = bpy.data.images.new(name, w, h, alpha=True)
    if lin: im.colorspace_settings.name = 'Non-Color'
    im.pixels.foreach_set(rgba.ravel()); im.filepath_raw = os.path.join(O, name+'.png'); im.file_format = 'PNG'; im.save(); print('saved', name, w, h, flush=True)
def sstep(x): x = np.clip(x, 0, 1); return x*x*(3-2*x)
def vnoise(h, w, cell, seed):
    r = np.random.default_rng(seed); gh, gw = int(h/cell)+3, int(w/cell)+3; g = r.random((gh, gw)).astype(np.float32)
    y = np.arange(h)/cell; x = np.arange(w)/cell; y0 = np.floor(y).astype(int); x0 = np.floor(x).astype(int); fy = (y-y0)[:, None]; fx = (x-x0)[None, :]; fy = fy*fy*(3-2*fy); fx = fx*fx*(3-2*fx)
    return g[y0][:, x0]*(1-fy)*(1-fx)+g[y0+1][:, x0]*fy*(1-fx)+g[y0][:, x0+1]*(1-fy)*fx+g[y0+1][:, x0+1]*fy*fx
def fbm(h, w, cell, seed, o=4):
    s = np.zeros((h, w), np.float32); am = 1.0; t = 0.0
    for k in range(o): s += am*vnoise(h, w, max(cell/2**k, 1.5), seed+k); t += am; am *= 0.5
    return s/t
def s2l(x): return np.where(x <= 0.04045, x/12.92, ((x+0.055)/1.055)**2.4)
def l2s(x): x = np.clip(x, 0, 1); return np.where(x <= 0.0031308, x*12.92, 1.055*x**(1/2.4)-0.055)
E_TAG = os.environ.get('C4_TAG', 'c4')
B = load('T_LK_Head_BC_v2.png')[..., :3]; N = B.shape[0]; L = s2l(B)
yy, xx = np.mgrid[0:N, 0:N].astype(np.float32); U = (xx+0.5)/N; V = (yy+0.5)/N
def ell(cu, cv, ru, rv, p=2): return np.exp(-(np.abs((U-cu)/ru)**p+np.abs((V-cv)/rv)**p))
def seg(u0, v0, u1, v1, w):
    du, dv = u1-u0, v1-v0; t = np.clip(((U-u0)*du+(V-v0)*dv)/(du*du+dv*dv), 0, 1); d = np.hypot(U-(u0+t*du), V-(v0+t*dv)); return np.exp(-(d/w)**2)*np.clip(np.sin(np.pi*t), 0, 1)**0.6
mot = 0.7+0.6*fbm(N, N, 70, 51)
# under-eye: tear trough + lower-lid band (brown-violet), left slightly stronger (asymmetry)
ue = sum(s*(ell(cu, 0.402, 0.052, 0.016)+0.7*seg(cu-sg*0.012, 0.395, cu+sg*0.045, 0.425, 0.007)) for cu, sg, s in ((0.38, -1, 1.0), (0.62, 1, 0.85)))
ue = np.clip(ue, 0, 1)*mot; k = E('C4_UE', '0.16')
L = L*(1-k*ue[..., None]*np.array([E('C4_UE_R', '0.85'), 1.0, E('C4_UE_B', '0.9')], np.float32))
# periocular redness (base lids / under-eye read pink-red): remove the red EXCESS only
ring = np.clip(ell(0.38, 0.37, 0.075, 0.05)+ell(0.62, 0.37, 0.075, 0.05), 0, 1)*(1-np.clip(ell(0.38, 0.36, 0.035, 0.012)+ell(0.62, 0.36, 0.035, 0.012), 0, 1))
redx = np.clip(L[..., 0]-0.5*(L[..., 1]+L[..., 2])-0.05, 0, None); L[..., 0] = L[..., 0]-E('C4_EYE_DERED', '0.0')*ring*redx
# upper-lid crease shadow
cr = np.clip(ell(0.38, 0.334, 0.045, 0.008)+ell(0.62, 0.334, 0.045, 0.008), 0, 1)
L = L*(1-E('C4_CREASE', '0.10')*cr[..., None])
# nasolabial tone (mild; the fold itself is geometry)
nl = np.clip(seg(0.452, 0.512, 0.418, 0.598, 0.008)+seg(0.548, 0.512, 0.582, 0.598, 0.008)*0.9, 0, 1)*mot
L = L*(1-E('C4_NL', '0.08')*nl[..., None]*np.array([0.9, 1.0, 1.0], np.float32))
# marionette hint below the mouth corners
mar = np.clip(seg(0.405, 0.60, 0.415, 0.66, 0.007)+seg(0.595, 0.60, 0.585, 0.66, 0.007), 0, 1)*mot
L = L*(1-E('C4_MAR', '0.05')*mar[..., None])
# forehead: sun-warm, uneven
fh = ell(0.5, 0.215, 0.17, 0.06)*(0.6+0.8*fbm(N, N, 110, 61))
L = L*(1-E('C4_SUN', '0.07')*fh[..., None]*np.array([0.6, 0.95, 1.3], np.float32))
# blotchy redness: nose sides / inner cheeks / chin, low-frequency patches (instead of a uniform pink)
rz = np.clip(ell(0.5, 0.47, 0.045, 0.05)+ell(0.43, 0.47, 0.04, 0.04)+ell(0.57, 0.47, 0.04, 0.04)+0.6*ell(0.5, 0.66, 0.05, 0.03), 0, 1)
bl = np.clip((fbm(N, N, 45, 71)-0.45)/0.25, 0, 1)*rz
L = L*(1+E('C4_RED', '0.10')*bl[..., None]*np.array([0.35, -0.55, -0.6], np.float32))
# lips: muted, rose-brown, slightly darker at the border
lip = sstep((1-np.sqrt(((U-0.5)/0.105)**2+((V-0.588)/0.036)**2))/0.35)
g_ = (L*np.array([0.3, 0.59, 0.11], np.float32)).sum(-1, keepdims=True); tgt = g_*np.array([E('C4_LT_R', '1.18'), E('C4_LT_G', '0.92'), E('C4_LT_B', '0.84')], np.float32)
L = L*(1-E('C4_LIP', '0.45')*lip[..., None])+tgt*E('C4_LIP', '0.45')*lip[..., None]
L = L*(1-0.06*lip[..., None])
assert not np.isnan(L).any(), 'nan'; save(l2s(L), 'T_LK_Head_BC_'+E_TAG, False); save(l2s(L)[::8, ::8], '_prev_face_bc_'+E_TAG, False)
# normal: faint forehead lines, glabella, crow's feet (height field -> tangent-space perturbation added to the v2 normal)
Nm = load('T_LK_Head_N_v2.png')[..., :3]; M = Nm.shape[0]; yy, xx = np.mgrid[0:M, 0:M].astype(np.float32); U = (xx+0.5)/M; V = (yy+0.5)/M
H = np.zeros((M, M), np.float32); wob = (fbm(M, M, 40, 81)-0.5)*0.006
for vv, s in ((0.195, 0.8), (0.222, 1.0), (0.248, 0.7)):
    H += s*np.exp(-((V+wob+0.012*np.sin(U*9+vv*40)-vv)/0.0028)**2)*ell(0.5, vv, 0.12, 0.2, 4)
H += 0.8*(np.exp(-((U-0.483+0.02*(V-0.29))/0.0022)**2)+np.exp(-((U-0.517-0.02*(V-0.29))/0.0022)**2))*ell(0.5, 0.29, 0.05, 0.02)
for cu, sg in ((0.305, -1), (0.695, 1)):
    for ang in (-0.35, 0.0, 0.35):
        d = (V-0.36)-np.tan(ang)*(U-cu)*(-sg); H += 0.6*np.exp(-(d/0.0025)**2)*ell(cu+sg*0.01, 0.36, 0.025, 0.03)
H *= (0.7+0.6*fbm(M, M, 30, 91))
gy, gx = np.gradient(H); s = E('C4_NRM', '0.9')
P = (Nm*2-1); P[..., 0] += -gx*s*M/1024; P[..., 1] += gy*s*M/1024; P /= np.maximum(np.linalg.norm(P, axis=-1, keepdims=True), 1e-6)
save(P*0.5+0.5, 'T_LK_Head_N_'+E_TAG, True)
print('FACESKIN_C4_OK')
