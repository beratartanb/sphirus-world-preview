"""GUARDIAN-4: per-side lower-face / jaw / chin / zygoma measurements of DNA-order heads (project frame, UE cm; character LEFT = +x).
Facial midline = mean x of the midline landmarks (nasion/pronasale/subnasale/philtrum/stomion/menton region of the 'mid' strip).
Reports, per side (L = character left = +x = IMAGE RIGHT in a front view):
  - silhouette half-widths (front-of-ear skin, y > ear plane) at heights relative to the eye line
  - gonion (max-curvature point of the jaw lower border), mandibular body length (gonion -> menton), lower-face vertical length per side
  - chin side planes, menton / pogonion offsets from the midline, mouth-corner positions, cheek fullness (lateral bulge at z of the mouth)
usage: blender -b -P blender_gd4_asym.py -- <head.npy> [<head2.npy> ...]  -> prints ASYM json per head"""
import sys, os, json, numpy as np
a = sys.argv[sys.argv.index('--')+1:]
def analyse(X):
    S = X[:24049]; eL = X[28955:29725].mean(0); eR = X[29725:30495].mean(0); ez = (eL[2]+eR[2])/2
    # midline: vertices nearest the sagittal plane of the eyes' midpoint, refined with nose tip / philtrum / chin ridges
    mx0 = (eL[0]+eR[0])/2
    front = S[:, 1] > 6.0
    def ridge(z0, z1):
        m = front & (S[:, 2] > z0) & (S[:, 2] < z1) & (np.abs(S[:, 0]-mx0) < 1.5); i = np.nonzero(m)[0]; return S[i[np.argmax(S[i, 1])]] if len(i) else None
    pron = ridge(ez-4.5, ez-1.5); sub = ridge(ez-6.8, ez-5.2); chin = ridge(ez-12.5, ez-9.5)
    out = {'eye_mid_x': round(float(mx0), 3), 'pronasale_x': round(float(pron[0]), 3), 'philtrum_x': round(float(sub[0]), 3), 'pogonion': np.round(chin, 3).tolist()}
    # menton: lowest point of the chin within 1.2 cm of the chin ridge x, front part
    m = (S[:, 1] > chin[1]-3.5) & (np.abs(S[:, 0]-chin[0]) < 1.6) & (S[:, 2] > 146.5) & (S[:, 2] < chin[2]); i = np.nonzero(m)[0]; men = S[i[np.argmin(S[i, 2])]]; out['menton'] = np.round(men, 3).tolist()
    mid = float(np.mean([pron[0], sub[0]])); out['face_midline_x'] = round(mid, 3)
    out['menton_offset_from_midline_cm'] = round(float(men[0]-mid), 3); out['pogonion_offset_cm'] = round(float(chin[0]-mid), 3)
    # half-widths per side at heights relative to the eye line (cm below eyes), skin in front of the ear plane
    hw = {}
    for dz in (0.0, 1.5, 2.5, 3.5, 5.0, 6.5, 8.0, 9.5, 10.5, 11.5):
        z = ez-dz; mm = (np.abs(S[:, 2]-z) < 0.15) & (S[:, 1] > 3.6)
        if mm.sum() < 4: continue
        xs = S[mm, 0]; hw[f'-{dz}'] = {'L': round(float(xs.max()-mid), 3), 'R': round(float(mid-xs.min()), 3)}
    out['half_widths_front_of_ear'] = hw
    # jaw lower border per side: for y slices, the lowest z of the lateral jaw skin (x side), take the gonion as max-distance from the chin->ear-lobe chord
    res = {}
    for side, sg in (('L', 1), ('R', -1)):
        pts = []
        for y in np.arange(-1.0, chin[1]-0.5, 0.25):
            mm = (np.abs(S[:, 1]-y) < 0.13) & (sg*(S[:, 0]-mid) > 1.5) & (S[:, 2] > 147.5) & (S[:, 2] < ez-5)
            if mm.sum() < 3: continue
            P = S[mm]
            # jaw border = outer-lower envelope point: maximise lateral distance minus height (corner of the jaw section)
            k = np.argmax(sg*(P[:, 0]-mid)*0.6-(P[:, 2]-148)); pts.append(P[k])
        pts = np.asarray(pts)
        if len(pts) < 5: continue
        # gonion: point of the border with max distance from the line menton -> most posterior border point
        A, B = men, pts[np.argmin(pts[:, 1])]; d = np.linalg.norm(np.cross(pts-A, B-A), axis=1)/np.linalg.norm(B-A); g = pts[np.argmax(d)]
        seg = np.r_[[men], pts[np.argsort(-pts[:, 1])]]; body = float(np.linalg.norm(np.diff(seg[seg[:, 1] >= g[1]-1e-6], axis=0), axis=1).sum())
        mc = None
        res[side] = {'gonion': np.round(g, 3).tolist(), 'gonion_halfwidth': round(float(sg*(g[0]-mid)), 3), 'gonion_height_below_eyes': round(float(ez-g[2]), 3),
                     'mandibular_body_len_cm': round(float(np.linalg.norm(g-men)), 3), 'jaw_border_path_cm': round(body, 3)}
    out['jaw'] = res
    # lower-face vertical length per side: eye centre (that side) -> jaw border directly below the mouth corner
    return out
for hp in a:
    X = np.load(hp); print('ASYM', os.path.basename(hp), json.dumps(analyse(X)))
