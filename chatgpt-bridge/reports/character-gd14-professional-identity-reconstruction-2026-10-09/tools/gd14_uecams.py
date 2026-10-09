"""GD14: solved reference cameras (GD13 model: X_cam = (X-CH) R^T, d = D + z, u = f x/d + cx) -> UE scene-capture cameras with the SAME optical centre and
optical axis (roll 0, fov FOV, square SIZE px), plus a FIXED common camera set (same lens / distance for every candidate). The UE image is later warped
exactly onto the panel frame by gd14_warp.py (pure rotation + intrinsics homography, same centre => exact).
usage (any numpy python): gd14_uecams.py <cams.json> <out.json> [fov=15] [size=1600]"""
import sys, json, math, numpy as np
a = sys.argv[1:]; CJ = json.load(open(a[0])); OUT = a[1]; FOV = float(a[2]) if len(a) > 2 else 15.0; SIZE = int(a[3]) if len(a) > 3 else 1600
MX = -0.23; CH = np.array([MX, 5.0, 160.0]); R_FRONT = np.array([[1.0, 0, 0], [0, 0, -1.0], [0, -1.0, 0]])
PANEL = {'front': (483, 541), 'q3_faceR': (483, 541), 'q3_faceL': (482, 541), 'prof_faceL': (483, 545)}
def rod(r):
    r = np.asarray(r, float); th = np.linalg.norm(r)
    if th < 1e-12: return np.eye(3)
    k = r/th; K = np.array([[0, -k[2], k[1]], [k[2], 0, -k[0]], [-k[1], k[0], 0]]); return np.eye(3)+math.sin(th)*K+(1-math.cos(th))*K@K
def ue_axes(yaw, pitch):
    y, p = math.radians(yaw), math.radians(pitch)
    return (np.array([math.cos(p)*math.cos(y), math.cos(p)*math.sin(y), math.sin(p)]), np.array([-math.sin(y), math.cos(y), 0.0]), np.array([-math.sin(p)*math.cos(y), -math.sin(p)*math.sin(y), math.cos(p)]))
out = {'fov': FOV, 'size': SIZE, 'ref': {}, 'common': {}}
for v, c in CJ.items():
    if v not in PANEL: continue
    R = rod(c['rvec'])@R_FRONT; fwd = R[2]; C = CH-c['D']*fwd
    yaw = math.degrees(math.atan2(fwd[1], fwd[0])); pitch = math.degrees(math.asin(np.clip(fwd[2], -1, 1)))
    F, Rt, U = ue_axes(yaw, pitch); roll = math.degrees(math.atan2(np.dot(R[0], U)*-1, np.dot(R[0], Rt)))
    out['ref'][v] = {'cam': [round(float(C[0]), 4), round(float(C[1]), 4), round(float(C[2]), 4), round(yaw, 5), round(pitch, 5)], 'R': R.tolist(), 'f': c['f'], 'cx': c['cx'], 'cy': c['cy'], 'panel': PANEL[v], 'roll_deg_info': round(roll, 3)}
# common cameras: optical axis through CH, distance 150 cm, pitch 0, same lens for every view and every candidate
for k, yaw_from in (('front', 90.0), ('q3_faceR', 135.0), ('q3_faceL', 45.0), ('prof_faceL', 0.0), ('prof_faceR', 180.0)):
    ang = math.radians(yaw_from); dirc = np.array([math.cos(ang), math.sin(ang), 0.0]); C = CH+150.0*dirc; yaw = math.degrees(math.atan2(-dirc[1], -dirc[0]))
    out['common'][k] = {'cam': [round(float(C[0]), 4), round(float(C[1]), 4), round(float(C[2]), 4), round(yaw, 5), 0.0]}
json.dump(out, open(OUT, 'w'), indent=1)
for v, d in out['ref'].items(): print('REFCAM', v, d['cam'], 'roll', d['roll_deg_info'])
for v, d in out['common'].items(): print('COMMON', v, d['cam'])
