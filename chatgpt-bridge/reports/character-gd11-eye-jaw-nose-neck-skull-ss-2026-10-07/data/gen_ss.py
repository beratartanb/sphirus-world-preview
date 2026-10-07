# pass SS op groups on R6 (cm, UE frame, x from midline MX). usage: python gen_ss.py <outdir>
import json, sys, os
O = sys.argv[1]
EYE = [  # 1: give back about half of the pass-R hood that Y1 removed (Y1: -2 deg, hood -0.17/-0.10) + brow tissue 1.3 mm lower
    {"name": "upper_lid_drop_half", "type": "lidrot", "c": [2.97, 10.5, 162.25], "deg": 1.5, "z0": 0.3, "zr0": 0.25, "z1": 1.45, "zr1": 0.5, "xw": 1.5, "rmax": 2.4, "yf": 0.25, "sym": True},
    {"name": "hood_half", "type": "normal", "c": [3.5, 11.9, 163.8], "r": [1.15, 0.85, 0.48], "amt": 0.12, "sym": True},
    {"name": "lateral_hood_half", "type": "normal", "c": [4.15, 11.2, 163.95], "r": [0.9, 0.9, 0.52], "amt": 0.07, "sym": True},
    {"name": "brow_tissue_lower", "type": "grab", "c": [2.9, 11.2, 164.9], "r": [2.3, 1.3, 0.85], "d": [0.0, 0.0, -0.2], "sym": True},
    {"name": "relax_hood", "type": "relax", "c": [3.4, 11.5, 164.1], "r": [1.9, 1.3, 1.0], "iters": 2, "sym": True}]
JAW = [  # 3: soften the flaring jaw angle, a little lower-cheek softness; 4: chin less prominent in 3/4 (lateral chin back, pogonion -0.8 mm)
    {"name": "gonial_flare_soften", "type": "normal", "c": [4.9, 2.8, 149.9], "r": [1.3, 1.7, 1.3], "amt": -0.3, "sym": True},
    {"name": "lower_cheek_soft", "type": "normal", "c": [4.6, 7.2, 152.9], "r": [1.3, 1.4, 1.2], "amt": 0.1, "sym": True},
    {"name": "chin_lateral_back", "type": "normal", "c": [2.9, 10.3, 153.2], "r": [0.9, 1.0, 1.2], "amt": -0.25, "sym": True},
    {"name": "pogonion_back", "type": "grab", "c": [0.0, 12.6, 152.6], "r": [1.6, 1.0, 1.1], "d": [0.0, -0.08, 0.0], "sym": False},
    {"name": "relax_jaw", "type": "relax", "c": [4.3, 5.5, 151.2], "r": [2.2, 3.2, 2.0], "iters": 2, "sym": True},
    {"name": "relax_chin", "type": "relax", "c": [0.0, 11.8, 152.8], "r": [3.6, 1.6, 1.6], "iters": 1, "sym": False}]
NOSE = [  # 5: alar base 1 mm narrower per side (rigid lobule grab), fuller rounder tip, slightly broader dorsum
    {"name": "alar_narrow", "type": "grab", "c": [1.8, 12.9, 157.65], "r": [0.8, 1.0, 0.78], "d": [-0.14, -0.01, 0.0], "sym": True},
    {"name": "tip_fuller", "type": "grab", "c": [0.75, 15.1, 158.95], "r": [0.55, 0.65, 0.65], "d": [0.06, 0.0, 0.0], "sym": True},
    {"name": "dorsum_broader", "type": "grab", "c": [0.85, 13.8, 161.0], "r": [0.45, 0.6, 1.5], "d": [0.05, 0.0, 0.0], "sym": True},
    {"name": "relax_nose", "type": "relax", "c": [0.0, 14.3, 158.4], "r": [2.3, 1.7, 1.6], "iters": 2, "sym": False, "outer": True}]
NECK = [  # 7: suboccipital / nape curve (nape 8 mm forward under the occiput, fades out above the body seam) + subtle sternocleidomastoid ridges
    {"name": "nape_forward", "type": "grab", "c": [0.0, -4.0, 155.8], "r": [6.2, 3.0, 3.6], "d": [0.0, 1.2, 0.0], "sym": False},
    {"name": "relax_nape", "type": "relax", "c": [0.0, -3.5, 155.8], "r": [6.5, 3.5, 4.5], "iters": 2, "sym": False}]
for i, (x, y, z) in enumerate([(4.9, 1.0, 154.6), (4.3, 2.0, 152.4), (3.6, 3.0, 150.2), (2.9, 3.9, 148.2), (2.3, 4.6, 146.6)]):
    NECK.append({"name": "scm_%d" % i, "type": "normal", "c": [x, y, z], "r": [0.55, 0.6, 1.0], "amt": 0.05, "sym": True})
NECK.append({"name": "relax_scm", "type": "relax", "c": [3.6, 2.9, 150.5], "r": [2.0, 2.6, 4.6], "iters": 1, "sym": True})
SKULL = [  # 8: higher vault + shorter back of the skull as two broad smooth volume moves (no hard masks: the radial op left a temple notch and a crown ridge)
    {"name": "vault_raise", "type": "grab", "c": [0.0, 0.5, 175.0], "r": [9.0, 10.0, 7.0], "d": [0.0, 0.0, 0.6], "sym": False},
    {"name": "occiput_shorten", "type": "grab", "c": [0.0, -6.5, 164.5], "r": [8.0, 4.5, 5.5], "d": [0.0, 0.7, 0.0], "sym": False},
    {"name": "relax_vault", "type": "relax", "c": [0.0, -1.0, 168.0], "r": [8.5, 8.0, 7.0], "iters": 2, "sym": False}]
G = {'EYE': EYE, 'JAW': JAW, 'NOSE': NOSE, 'NECK': NECK, 'SKULL': SKULL}
for k, v in G.items(): json.dump({'mx': -0.23, 'ops': v}, open(os.path.join(O, 'S_%s.json' % k), 'w'), indent=1)
json.dump({'mx': -0.23, 'ops': EYE+JAW+NOSE+NECK+SKULL}, open(os.path.join(O, 'SS1.json'), 'w'), indent=1); print('GEN_SS ok', {k: len(v) for k, v in G.items()})
