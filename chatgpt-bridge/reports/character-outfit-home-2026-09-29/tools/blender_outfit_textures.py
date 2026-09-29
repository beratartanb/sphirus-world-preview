"""Textile texture authoring for the home outfit (Blender 5.2 background, numpy; writes PNG through bpy images).
Unique 2048^2 sets per garment (BaseColor sRGB, Normal, RA = roughness/AO packed) driven by the garment UV layout
(seam stitch lines along island borders, wash variation, wrinkle memory, edge fading) + tiling 512^2 weave detail normals
(jersey knit for the Henley, twill for the trousers). Charcoal trousers carry a very faint tonal textile motif.
usage: blender -b --factory-startup --python blender_outfit_textures.py -- <outfit_geometry.json.gz> <out_dir>"""
import bpy, sys, os, json, gzip, math
import numpy as np
argv = sys.argv[sys.argv.index('--')+1:]; GEO, OUT = argv; os.makedirs(OUT, exist_ok=True)
UV = json.loads(gzip.open(GEO, 'rb').read())['uv_layout']
rng = np.random.default_rng(20260929)
def value_noise(size, cells, seed):
    r = np.random.default_rng(seed); g = r.random((cells+1, cells+1))
    x = np.linspace(0, cells, size, endpoint=False); i = np.floor(x).astype(int); f = x-i; f = f*f*(3-2*f)
    a = g[i[:, None], i[None, :]]; b = g[i[:, None]+1, i[None, :]]; c = g[i[:, None], i[None, :]+1]; d = g[i[:, None]+1, i[None, :]+1]
    fy = f[:, None]; fx = f[None, :]
    return (a*(1-fy)+b*fy)*(1-fx)+(c*(1-fy)+d*fy)*fx
def fbm(size, base_cells, octaves, seed, gain=0.5):
    out = np.zeros((size, size)); amp = 1.0; tot = 0.0
    for o in range(octaves):
        out += amp*value_noise(size, base_cells*2**o, seed+o); tot += amp; amp *= gain
    return out/tot
def save_png(name, rgb, srgb_data=True):
    h, w = rgb.shape[:2]; img = bpy.data.images.new(name, w, h, alpha=True); img.colorspace_settings.name = 'Non-Color'
    px = np.ones((h, w, 4), np.float32); px[..., :3] = np.clip(rgb, 0, 1)
    img.pixels.foreach_set(px[::-1].copy().ravel())   # Blender image rows are bottom-up; row 0 of the array is the top (v = 1)
    img.filepath_raw = os.path.join(OUT, name+'.png'); img.file_format = 'PNG'; img.save(); bpy.data.images.remove(img); print('saved', name)
def lin2srgb(c): c = np.clip(c, 0, 1); return np.where(c <= 0.0031308, 12.92*c, 1.055*np.power(c, 1/2.4)-0.055)
def height_to_normal(hmap, strength):
    dx = np.roll(hmap, -1, 1)-np.roll(hmap, 1, 1); dy = np.roll(hmap, -1, 0)-np.roll(hmap, 1, 0)
    n = np.stack([-dx*strength, dy*strength, np.ones_like(hmap)], -1); n /= np.linalg.norm(n, axis=-1, keepdims=True)
    return n*0.5+0.5
S = 2048
def island_masks(layout):
    """per-pixel: inside-any-island mask, distance to island border (px), and a stitch-line mask along the borders"""
    yy, xx = np.mgrid[0:S, 0:S]; u = (xx+0.5)/S; v = 1-(yy+0.5)/S
    inside = np.zeros((S, S), bool); border = np.full((S, S), 1e9)
    for name, (u0, v0, u1, v1) in layout.items():
        m = (u >= u0) & (u <= u1) & (v >= v0) & (v <= v1); inside |= m
        d = np.minimum.reduce([np.abs(u-u0), np.abs(u1-u), np.abs(v-v0), np.abs(v1-v)])*S
        border = np.where(m, np.minimum(border, d), border)
    return inside, border
def stitches(border, offset_px, period_px, width_px=1.6):
    """two rows of stitches parallel to island borders (seam allowance look)"""
    line = np.exp(-((border-offset_px)/width_px)**2)
    yy, xx = np.mgrid[0:S, 0:S]; dash = 0.5+0.5*np.sign(np.sin(2*np.pi*(xx+yy)/period_px))
    return line*(0.55+0.45*dash)

# ---------------------------------------------------------------- HENLEY (jersey/linen blend, warm ivory, washed)
lay = UV['henley']; inside, border = island_masks(lay)
mottle = fbm(S, 6, 5, 11); wash = fbm(S, 3, 3, 12); wrinkle = fbm(S, 10, 4, 13); fibre = fbm(S, 128, 3, 14)
base = np.array([0.66, 0.60, 0.50])            # linear ivory/oatmeal (sRGB ~ 0.84,0.80,0.74)
tint = (mottle-0.5)*0.10+(wash-0.5)*0.06+(fibre-0.5)*0.03
col = base[None, None, :]*(1+tint[..., None])
col[..., 2] *= 1-(wash-0.5)*0.05                # washed areas slightly cooler
edge_fade = np.clip(1-border/40, 0, 1)*0.05     # edges (hems, cuffs, placket) lightly faded
col *= (1-edge_fade)[..., None]
st = stitches(border, 9, 7)*0.45+stitches(border, 4, 7)*0.15
col = col*(1-st[..., None]*0.35)+np.array([0.62, 0.56, 0.46])[None, None, :]*st[..., None]*0.35
save_png('T_Henley_BC', lin2srgb(col))
h = (mottle-0.5)*0.35+(wrinkle-0.5)*0.9+(fibre-0.5)*0.25-st*0.9+np.clip(1-border/6, 0, 1)*0.8
save_png('T_Henley_N', height_to_normal(h, 3.5))
rough = 0.84+(mottle-0.5)*0.08+(fibre-0.5)*0.06-st*0.08; ao = 1-st*0.25-np.clip(1-border/5, 0, 1)*0.15
save_png('T_Henley_RA', np.stack([rough, ao, np.zeros_like(rough)], -1))

# ---------------------------------------------------------------- TROUSERS (washed cotton twill, charcoal, faint motif)
lay = UV['trousers']; inside, border = island_masks(lay)
mottle = fbm(S, 5, 5, 21); wash = fbm(S, 3, 3, 22); wrinkle = fbm(S, 12, 4, 23); fibre = fbm(S, 160, 3, 24)
# faint organic tonal motif: sparse soft blobs with thin curling strokes (reads as an aged printed weave up close)
motif = np.zeros((S, S)); yy, xx = np.mgrid[0:S, 0:S]
for k in range(140):
    cx, cy = rng.random(2)*S; r = 18+rng.random()*46; ang = rng.random()*np.pi; e = 0.45+rng.random()*0.5
    dx = (xx-cx)/S*S; dy = (yy-cy)/S*S; xr = dx*np.cos(ang)+dy*np.sin(ang); yr = -dx*np.sin(ang)+dy*np.cos(ang)
    blob = np.exp(-((xr/r)**2+(yr/(r*e))**2)*1.6); motif += blob*(0.6+0.4*rng.random())
    for s in range(3):
        t = np.linspace(0, 1, 60); px = cx+np.cos(ang+s*2.1)*r*1.3*t*(1+0.3*np.sin(t*7)); py = cy+np.sin(ang+s*2.1)*r*1.3*t
        for qx, qy in zip(px, py):
            ix, iy = int(qx) % S, int(qy) % S; motif[max(0, iy-1):iy+2, max(0, ix-1):ix+2] += 0.08
motif = np.clip(motif, 0, 1)*(0.5+0.5*fbm(S, 8, 3, 25))
base = np.array([0.055, 0.056, 0.058])         # linear charcoal (sRGB ~ 0.26)
tint = (mottle-0.5)*0.22+(wash-0.5)*0.14+(fibre-0.5)*0.05
col = base[None, None, :]*(1+tint[..., None])
col = col*(1+motif[..., None]*0.10)             # motif lifts the tone by ~10 % (very subtle)
col[..., 0] *= 1+motif*0.03                     # a hint of warmth in the motif
edge_fade = np.clip(1-border/50, 0, 1)*0.10; col *= (1+edge_fade)[..., None]   # worn edges lighten on dark cloth
st = stitches(border, 10, 8)*0.5+stitches(border, 4, 8)*0.2
col = col*(1-st[..., None]*0.3)+np.array([0.10, 0.095, 0.085])[None, None, :]*st[..., None]*0.3
save_png('T_Trousers_BC', lin2srgb(col))
h = (mottle-0.5)*0.3+(wrinkle-0.5)*1.0+(fibre-0.5)*0.2+motif*0.25-st*0.9+np.clip(1-border/6, 0, 1)*0.8
save_png('T_Trousers_N', height_to_normal(h, 3.2))
rough = 0.80+(mottle-0.5)*0.10+(fibre-0.5)*0.05-motif*0.03-st*0.06; ao = 1-st*0.25-np.clip(1-border/5, 0, 1)*0.15
save_png('T_Trousers_RA', np.stack([rough, ao, np.zeros_like(rough)], -1))

# ---------------------------------------------------------------- detail weave tiles (512, tiling)
D = 512; yy, xx = np.mgrid[0:D, 0:D]
# jersey knit: columns of V loops (rib period 8 px = ~1.1 mm at the intended 30x tiling over ~0.7 m)
per = 8; col_phase = (xx % per)/per; row = (yy % (per*1.4))/(per*1.4)
knit = np.sin(col_phase*2*np.pi)*0.5*(0.7+0.3*np.cos(row*2*np.pi+col_phase*np.pi))+np.sin(row*2*np.pi)*0.2
knit += (fbm(D, 32, 3, 31)-0.5)*0.4
save_png('T_Detail_Jersey_N', height_to_normal(knit, 2.2))
# twill: diagonal 2/1 ribs
diag = ((xx+yy) % 6)/6.0; tw = np.abs(diag-0.5)*2-0.5; tw += (np.sin(xx*2*np.pi/3)*0.15)+(fbm(D, 32, 3, 32)-0.5)*0.35
save_png('T_Detail_Twill_N', height_to_normal(tw, 2.0))
print('TEXTURES_OK')
