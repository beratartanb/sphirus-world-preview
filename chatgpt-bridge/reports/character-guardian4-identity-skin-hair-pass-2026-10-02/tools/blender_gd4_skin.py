"""GUARDIAN-4 Phase E skin textures (isolated copies, sources untouched). Adult, sun-exposed, matte skin with multi-scale REGIONAL
detail and NO wrinkles / bags / folds. Regions are soft ellipses in the MetaHuman head UV (top-left origin, measured on the c17 BC).
  BC   (4K, from g2 c17): sun exposure (forehead / nose bridge / cheekbones warmer-darker, under-jaw lighter), low+mid frequency
       pigment mottling, sparse sun spots, periorbital grey-purple neutralised toward cheek chroma, lips muted rose-brown. Freckles kept.
  N    (4K, from c14s 1K seam-shaded normal, upsampled): neck ring folds flattened, + procedural pores in three size classes with
       per-region density / size (nose + inner cheeks large & dense, forehead / chin medium, cheeks medium-fine, eyelids / lips none),
       fine micro-grain; detail fades out toward the neck collar so the seam shading of c14s stays intact.
  SRMF (2K, from c14s): roughness per region (T-zone a little less rough, cheeks / temples matte), specular per region (cheeks lower,
       nose / forehead mid), pore cavities rougher with lower specular; collar band (v > NECK_V) untouched (seam match of c14s).
Writes <out>/T_LK_Head_{BC,N,SRMF}_<tag>.png and <out>/_masks_<tag>.png (debug: region masks over the BC).
usage: blender -b --factory-startup --python blender_gd4_skin.py -- <BC png> <N png> <SRMF png> <out dir> <tag>"""
import bpy, sys, os, numpy as np
a = sys.argv[sys.argv.index('--')+1:]; BCP, NP, SRP, OUT, TAG = a; os.makedirs(OUT, exist_ok=True)
E = lambda k, d: float(os.environ.get(k, d)); RNG = np.random.default_rng(int(E('SEED', 7)))
def load(p):
    im = bpy.data.images.load(os.path.abspath(p)); w, h = im.size; x = np.asarray(im.pixels[:], np.float32).reshape(h, w, im.channels)[::-1].copy(); bpy.data.images.remove(im)
    return x
def save(x, p, lin=False):
    h, w = x.shape[:2]; rgba = np.ones((h, w, 4), np.float32); rgba[..., :x.shape[2]] = np.clip(x, 0, 1)
    im = bpy.data.images.new(os.path.basename(p), w, h, alpha=True, float_buffer=False)
    if lin: im.colorspace_settings.name = 'Non-Color'
    im.pixels.foreach_set(np.ascontiguousarray(rgba[::-1]).ravel()); im.filepath_raw = os.path.abspath(p); im.file_format = 'PNG'; im.save(); bpy.data.images.remove(im)
def blur(x, s):   # gaussian blur via FFT (periodic), x 2D
    h, w = x.shape; fy = np.fft.fftfreq(h)[:, None]; fx = np.fft.rfftfreq(w)[None, :]
    return np.fft.irfft2(np.fft.rfft2(x)*np.exp(-2*(np.pi*s)**2*(fx*fx+fy*fy)), s=(h, w)).astype(np.float32)
def resize(x, n):  # bilinear resample of HxWxC to n x n
    h, w = x.shape[:2]; ys = (np.arange(n)+0.5)*h/n-0.5; xs = (np.arange(n)+0.5)*w/n-0.5
    y0 = np.clip(np.floor(ys).astype(int), 0, h-1); x0 = np.clip(np.floor(xs).astype(int), 0, w-1); y1 = np.clip(y0+1, 0, h-1); x1 = np.clip(x0+1, 0, w-1)
    fy = np.clip(ys-y0, 0, 1)[:, None, None]; fx = np.clip(xs-x0, 0, 1)[None, :, None]
    return (x[y0][:, x0]*(1-fy)*(1-fx)+x[y0][:, x1]*(1-fy)*fx+x[y1][:, x0]*fy*(1-fx)+x[y1][:, x1]*fy*fx).astype(np.float32)
def sstep(t): t = np.clip(t, 0, 1); return t*t*(3-2*t)
def masks(n):
    v, u = (np.mgrid[0:n, 0:n].astype(np.float32)+0.5)/n
    def el(cu, cv, ru, rv, mirror=False):
        m = sstep(1-np.sqrt(((u-cu)/ru)**2+((v-cv)/rv)**2))
        if mirror: m = np.maximum(m, sstep(1-np.sqrt(((u-(1-cu))/ru)**2+((v-cv)/rv)**2)))
        return m
    M = {'forehead': el(0.5, 0.24, 0.21, 0.10), 'nose': np.maximum(el(0.5, 0.46, 0.055, 0.10), el(0.5, 0.505, 0.09, 0.045)),
         'cheek': el(0.33, 0.53, 0.10, 0.09, True), 'inner_cheek': el(0.41, 0.52, 0.05, 0.05, True), 'cheekbone': el(0.355, 0.445, 0.09, 0.05, True),
         'chin': el(0.5, 0.69, 0.085, 0.05), 'periorb': el(0.385, 0.40, 0.075, 0.035, True), 'lid': el(0.385, 0.375, 0.07, 0.03, True),
         'lips': el(0.5, 0.595, 0.105, 0.042), 'ear': el(0.15, 0.47, 0.06, 0.11, True)}
    M['face'] = sstep(1-np.sqrt(((u-0.5)/0.36)**2+((v-0.47)/0.34)**2)/1.0)
    M['neck'] = sstep((v-E('NECK_V', 0.74))/0.08)
    M['collar_keep'] = 1-sstep((v-0.80)/0.06)   # 1 = free to change, 0 = collar band (seam shading kept)
    M['sun'] = np.clip(M['forehead']*0.8+M['nose']*1.0+M['cheekbone']*0.9+el(0.5, 0.40, 0.04, 0.06)*0.7, 0, 1)*(1-M['lid'])
    return M
# ---------------- BC ----------------
BC = load(BCP)[..., :3]; n = BC.shape[0]; M = masks(n)
lum = BC@np.array([0.299, 0.587, 0.114], np.float32)
cheek_col = BC[M['cheek'] > 0.6].mean(0); out = BC.copy()
sun = M['sun'][..., None]*E('SUN', 1.0); out *= 1-sun*(1-np.array([E('SUNR', 0.93), E('SUNG', 0.92), E('SUNB', 0.905)], np.float32))
neckl = (M['neck']*M['collar_keep'])[..., None]; out *= 1+neckl*np.array([0.02, 0.015, 0.01], np.float32)
po = (M['periorb']*(1-M['lid']*0.5))[..., None]*E('PERI', 0.45); ch = cheek_col/cheek_col.mean(); out = out*(1-po)+(lum[..., None]*ch)*po
lp = M['lips'][..., None]*0.18; out = out*(1-lp)+(lum[..., None]*np.array([1.12, 0.93, 0.86], np.float32))*lp
g1 = blur(RNG.standard_normal((n, n)).astype(np.float32), n/100); g1 /= g1.std()+1e-6
g2 = blur(RNG.standard_normal((n, n)).astype(np.float32), n/340); g2 /= g2.std()+1e-6
mot = (g1*E('MOT1', 0.028)+g2*E('MOT2', 0.018))*M['face']*M['collar_keep']; out *= (1+mot)[..., None]
red = blur(RNG.standard_normal((n, n)).astype(np.float32), n/160); red = np.clip(red/red.std(), 0, None)*(M['inner_cheek']+M['nose']*0.6)*E('RED', 0.03)
out *= np.stack([1+red, 1-red*0.6, 1-red*0.8], -1)
imp = (RNG.random((n, n)) < E('SPOTS', 1.0)*2.2e-5).astype(np.float32)*(M['sun']+0.35*M['cheek'])*M['collar_keep']
sp = blur(imp, n/1400); sp = np.clip(sp/max(sp.max(), 1e-6)*1.6, 0, 1)**0.8*0.38; spc = np.array([0.80, 0.70, 0.60], np.float32)
out = out*(1-sp[..., None])+out*spc*sp[..., None]
save(out, os.path.join(OUT, f'T_LK_Head_BC_{TAG}.png'))
dbg = BC*0.55; dbg[..., 0] += M['sun']*0.4; dbg[..., 1] += (M['nose']+M['inner_cheek'])*0.4; dbg[..., 2] += (M['periorb']+M['lips']+M['lid'])*0.4; dbg += M['neck'][..., None]*0.15
save(resize(dbg, 1024), os.path.join(OUT, f'_masks_{TAG}.png'))
# ---------------- N ----------------
N0 = load(NP); NS = int(E('NSIZE', 4096)); N = resize(N0[..., :3], NS); M = masks(NS)
xy = N[..., :2]*2-1
lowxy = np.stack([blur(xy[..., 0], 6), blur(xy[..., 1], 6)], -1); ring = (M['neck']*(1-M['face']))[..., None]*E('RINGFLAT', 0.7)
xy = xy-lowxy*ring
dens = {'L': (M['nose']*1.0+M['inner_cheek']*0.8+M['cheek']*0.25)*(1-M['lips'])*(1-M['lid']),
        'M': (M['forehead']*0.8+M['chin']*0.8+M['cheek']*0.7+M['nose']*0.4+0.15*M['face'])*(1-M['lips'])*(1-M['lid']),
        'S': (0.6*M['face']+0.3)*(1-M['lips']*0.8)*(1-M['lid']*0.7)}
H = np.zeros((NS, NS), np.float32); sc = NS/4096
for k, (rate, sig, depth) in {'L': (0.020, 1.55, 1.0), 'M': (0.030, 1.05, 0.7), 'S': (0.045, 0.7, 0.45)}.items():
    imp = (RNG.random((NS, NS)) < rate*dens[k]/(sc*sc)*0.25).astype(np.float32)*(0.6+0.4*RNG.random((NS, NS)).astype(np.float32))
    H -= blur(imp, sig*sc)*depth*(2*np.pi*(sig*sc)**2)
H += blur(RNG.standard_normal((NS, NS)).astype(np.float32), 0.8*sc)*0.10
H += blur(RNG.standard_normal((NS, NS)).astype(np.float32), 5.0*sc)*0.35*(M['cheek']+M['forehead'])
fade = (M['collar_keep']*np.clip(M['face']*1.4+0.25, 0, 1)*(1-M['ear']*0.6))
gy, gx = np.gradient(H); k = E('PORE', 0.55)
dx = -gx*k*fade; dy = -gy*k*fade
xy = xy+np.stack([dx, dy], -1); z = np.sqrt(np.clip(1-(xy**2).sum(-1), 0.05, 1))
Nout = np.concatenate([xy*0.5+0.5, np.ones((NS, NS, 1), np.float32)], -1)
save(Nout, os.path.join(OUT, f'T_LK_Head_N_{TAG}.png'), lin=True)
print('N detail rms', float(np.sqrt((dx**2+dy**2)[fade > 0.5].mean())))
# ---------------- SRMF ----------------
S = load(SRP); ns = S.shape[0]; M = masks(ns); keep = M['collar_keep']
Hs = resize(H[..., None], ns)[..., 0]; cav = np.clip(-Hs/0.6, 0, 1)*keep
rough = S[..., 1]; spec = S[..., 0]
dr = (-0.05*M['nose']-0.035*M['forehead']*(1-M['sun']*0.3)+0.05*M['cheek']+0.04*M['chin']*0.5+0.03*M['cheekbone']+0.06*M['ear'])*E('RGAIN', 1.0)
ds = (-0.06*M['cheek']-0.03*M['chin']+0.02*M['nose']-0.02*M['forehead'])*E('SGAIN', 1.0)
S[..., 1] = np.clip(rough+(dr+E('RGLOB', 0.03)*M['face'])*keep+cav*0.06, 0, 1)
S[..., 0] = np.clip(spec+ds*keep-cav*0.10, 0, 1)
save(S[..., :4] if S.shape[2] == 4 else S, os.path.join(OUT, f'T_LK_Head_SRMF_{TAG}.png'), lin=True)
print('SKIN_OK', TAG, 'rough mean face', float(S[..., 1][M['face'] > 0.5].mean()), 'spec mean face', float(S[..., 0][M['face'] > 0.5].mean()))
