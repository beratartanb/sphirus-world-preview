"""GD46: where are the flipped triangles? region breakdown of main-cloth triangles whose normal reversed vs the START (LBS) state and vs the BIND state.
usage: blender -b --python gd46_flipwhere.py -- <build_dir> <g17e_build_dir>"""
import sys, os, json, gzip, numpy as np
a = sys.argv[sys.argv.index('--')+1:]; BD, GDIR = a[0], a[1]
H = json.loads(gzip.open(os.path.join(GDIR, 'outfit_geometry.json.gz'), 'rb').read())['henley']; T = np.asarray(H['triangles'], np.int64); PART = np.asarray(H['part']); X0 = np.asarray(H['positions'])
S0 = np.asarray(json.loads(gzip.open(os.path.join(BD, 'henley_posed_start.json.gz'), 'rt').read())['positions']); S1 = np.asarray(json.loads(gzip.open(os.path.join(BD, 'henley_posed_settled.json.gz'), 'rt').read())['positions'])
main = PART == 'SPH_Henley'; Tm = T[np.all(main[T], axis=1)]
def nrm(X): n = np.cross(X[Tm[:, 1]]-X[Tm[:, 0]], X[Tm[:, 2]]-X[Tm[:, 0]]); return n/np.maximum(np.linalg.norm(n, axis=1), 1e-9)[:, None]
nb, n0, n1 = nrm(X0), nrm(S0), nrm(S1); c = X0[Tm].mean(axis=1)
regions = {'armpit_|x|12-26_z120-133': (np.abs(c[:, 0]) > 12) & (np.abs(c[:, 0]) < 26) & (c[:, 2] > 120) & (c[:, 2] < 133), 'sleeve_|x|>26': np.abs(c[:, 0]) >= 26, 'yoke_z>136_|x|<12': (c[:, 2] > 136) & (np.abs(c[:, 0]) <= 12), 'shoulder_cap_z128-136_|x|12-26': (c[:, 2] > 128) & (c[:, 2] <= 136) & (np.abs(c[:, 0]) > 12) & (np.abs(c[:, 0]) < 26), 'torso_front_y>0_z<128': (c[:, 1] > 0) & (c[:, 2] <= 128) & (np.abs(c[:, 0]) <= 12), 'torso_back_y<0_z<128': (c[:, 1] <= 0) & (c[:, 2] <= 128) & (np.abs(c[:, 0]) <= 12), 'sides_|x|12-26_z<120': (np.abs(c[:, 0]) > 12) & (np.abs(c[:, 0]) < 26) & (c[:, 2] <= 120)}
f_s = np.einsum('ij,ij->i', n0, n1) < 0; f_b = np.einsum('ij,ij->i', nb, n1) < 0; f0b = np.einsum('ij,ij->i', nb, n0) < 0
out = {'total': {'vs_start': int(f_s.sum()), 'settled_vs_bind': int(f_b.sum()), 'start_vs_bind': int(f0b.sum())}}
for k, m in regions.items(): out[k] = {'n': int(m.sum()), 'vs_start': int((f_s & m).sum()), 'settled_vs_bind': int((f_b & m).sum()), 'start_vs_bind': int((f0b & m).sum())}
print('FLIPWHERE', json.dumps(out))
