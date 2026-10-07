# pass RR op generator: midline profile targets = current Q8 profile (same sampler as blender_gd15_ops.profile) + deltas (cm)
import sys, json, numpy as np
a = sys.argv[sys.argv.index('--')+1:]; X = np.load(a[0]); OUT = a[1]; MX = -0.23; NH = 24049; H = X[:NH]
F = [float(v) for v in a[2].split(',')]; LIPS, CHIN, SKULL = F[:3]; UPPER = F[3] if len(F) > 3 else LIPS   # scale factors per feature group (lower lip, chin, skull, upper lip)
def prof(z):
    m = (np.abs(H[:, 0]-MX) < 0.15) & (H[:, 1] > 11); s = H[m & (np.abs(H[:, 2]-z) < 0.11)]; return float(s[:, 1].max())
lower = [(151.45, 0, 'c'), (151.7, .12, 'c'), (152.1, .20, 'c'), (152.55, .22, 'c'), (153.0, .08, 'c'), (153.6, -.15, 'c'), (153.95, -.04, 'l'),
         (154.25, .20, 'l'), (154.55, .32, 'l'), (154.8, .24, 'l'), (155.0, .06, 'l'), (155.05, 0, 'l')]
upper = [(155.05, 0), (155.3, .08), (155.5, .12), (155.8, .25), (156.05, .12), (156.3, 0)]
ops = []
if LIPS or CHIN:
    ops.append({'name': 'lower_lip_sulcus_chin_profile', 'type': 'profile', 'knots': [[z, round(prof(z)+d*(CHIN if g == 'c' else LIPS), 4)] for z, d, g in lower],
                'sigma': [[151.0, 1.1], [152.5, 1.3], [153.6, 1.4], [154.5, 1.6], [155.1, 1.6]], 'pow': 2, 'front': 0.25, 'depth': [0.25, 0.3]})
if UPPER:
    ops.append({'name': 'upper_lip_fill_profile', 'type': 'profile', 'knots': [[z, round(prof(z)+d*UPPER, 4)] for z, d in upper], 'sigma': 1.6, 'pow': 2, 'front': 0.25, 'depth': [0.25, 0.3]})
if CHIN:
    ops.append({'name': 'relax_chin_pad', 'type': 'relax', 'c': [0.0, 12.4, 152.4], 'r': [2.2, 1.6, 1.6], 'iters': 2, 'sym': False})
if SKULL:
    kn = [[-10, 0], [15, 0], [20, .05], [25, .15], [30, .27], [35, .38], [40, .47], [45, .56], [50, .64], [55, .69], [60, .64], [65, .61], [70, .61], [75, .59], [80, .53], [85, .49], [90, .44], [95, .40], [100, .40], [105, .27], [110, .13], [115, 0]]
    ops.append({'name': 'vault_back_arc_round', 'type': 'radial', 'c': [0.0, 1.0, 163.6], 'knots': [[p, round(v*SKULL, 3)] for p, v in kn], 'xw': 8.0, 'xp': 1.0, 'zmin': 160.8, 'ymax': 4.0})
    ops.append({'name': 'relax_vault', 'type': 'relax', 'c': [0.0, -2.5, 168.0], 'r': [7.8, 6.0, 6.0], 'iters': 2, 'sym': False})
json.dump({'mx': MX, 'ops': ops}, open(OUT, 'w'), indent=1); print('GEN', OUT, len(ops))
