"""GUARDIAN face pass shared helpers (numpy; used from Blender python): the reference-solved UE capture cameras, exact perspective
projection of UE-cm points into the reference image frames (crop of the capture), ray generation, head mesh access.
Views: 'front' = reffront cam -> ref_front_x4 frame (800x960); 'close' = refclose cam -> ref_close_x2 frame (794x940)."""
import json, math, os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Tools/CharacterLookdev_20260930'))
from id_common import pkg, SEG
I = 'Saved/Codex/CharacterIdentity_20260930'; G = 'Saved/Codex/CharacterGuardian_20261001'
VIEWS = {'front': dict(cam=[0.95, 129.7, 170.3, -90.4, -3.8], fov=15.0, W=800, H=960, ref=I+'/track/ref_front_x4.png', trk=G+'/track/ref_front.json'),
         'close': dict(cam=[-91.0, 88.6, 143.3, -42.6, 8.6], fov=15.0, W=794, H=940, ref=I+'/track/ref_close_x2.png', trk=G+'/track/ref_close.json')}
_RC = None
def recon_cam(view):
    global _RC
    if _RC is None: _RC = json.load(open(I+'/recon_c/recon.json'))['cams']
    return _RC[view]
def basis(cam):
    x, y, z, yaw, pit = cam; cy, sy, cp, sp = math.cos(math.radians(yaw)), math.sin(math.radians(yaw)), math.cos(math.radians(pit)), math.sin(math.radians(pit))
    return np.array([x, y, z], float), np.array([cy*cp, sy*cp, sp]), np.array([-sy, cy, 0.0]), np.array([-cy*sp, -sy*sp, cp])
def _norm_proj(view, P):
    v = VIEWS[view]; o, f, r, u = basis(v['cam']); t = math.tan(math.radians(v['fov'])/2); d = np.asarray(P, float)-o; dd = d@f
    return np.stack([0.5+0.5*(d@r)/dd/t, 0.5-0.5*(d@u)/dd/t], -1)
_CF = {}
for _v in ('front', 'close'):   # re-solved camera (blender_gd_camfit.py) replaces the recon camera for that view
    _p = f'{G}/camfit_{_v}.json'
    if os.path.exists(_p) and not os.environ.get('GD_OLDCAM'):
        _c = json.load(open(_p)); _CF[_v] = _c; VIEWS[_v]['cam'] = [_c['origin'][0], _c['origin'][1], _c['origin'][2], _c['yaw'], _c['pitch']]
def crop_rect(view):
    """fractions (x0, y0, x1, y1) of the capture image that show the reference image extent (same as id_ref_frame.py)"""
    v = VIEWS[view]
    if view in _CF:
        c = _CF[view]; s_, t_ = c['s'], c['t']; return 0.5+0.5*(-t_[0]/s_), 0.5+0.5*(-t_[1]/s_), 0.5+0.5*((v['W']-t_[0])/s_), 0.5+0.5*((v['H']-t_[1])/s_)
    c = recon_cam(view); R, s, tr = c['R'], c['s'], c['t']; depth = float(np.dot(R[2], [0, 10, 160]))
    def world(px, py): uu, vv = (px-tr[0])/s, (py-tr[1])/s; return [R[0][k]*uu+R[1][k]*vv+R[2][k]*depth for k in range(3)]
    a = _norm_proj(view, [world(0, 0)])[0]; b = _norm_proj(view, [world(v['W'], v['H'])])[0]; return a[0], a[1], b[0], b[1]
def topix(view, P):
    v = VIEWS[view]; x0, y0, x1, y1 = crop_rect(view); q = _norm_proj(view, P); return np.stack([(q[:, 0]-x0)/(x1-x0)*v['W'], (q[:, 1]-y0)/(y1-y0)*v['H']], -1)
def ray(view, px, py):
    """world ray (origin, dir) through reference-frame pixel (px, py)"""
    v = VIEWS[view]; x0, y0, x1, y1 = crop_rect(view); nx = x0+px/v['W']*(x1-x0); ny = y0+py/v['H']*(y1-y0)
    o, f, r, u = basis(v['cam']); t = math.tan(math.radians(v['fov'])/2); d = f+r*(nx-0.5)*2*t-u*(ny-0.5)*2*t; return o, d/np.linalg.norm(d)
def head_topology():
    P = pkg(); return np.asarray(P['head']['triangles'], np.int64), np.asarray(P['head']['material_ids'])
def ref_curves(view): return json.load(open(VIEWS[view]['trk']))
