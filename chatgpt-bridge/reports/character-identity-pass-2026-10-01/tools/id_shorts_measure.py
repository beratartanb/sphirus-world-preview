import json, gzip, numpy as np
out = {}
for t in ('g14h', 'g15a', 'g15b'):
    G = json.load(gzip.open(f'Saved/Codex/CharacterLookdev_20260930/garments/{t}/outfit_geometry.json.gz', 'rt')); tr = G['trousers']; X = np.asarray(tr['positions'])
    log = open(f'Saved/Codex/CharacterLookdev_20260930/garments/{t}/build_log.txt').read()
    import re; rl = re.search(r"rise lengths CF / CB ([0-9.]+) ([0-9.]+)", log); lm = re.search(r"'z_cr_g': ([0-9.]+)", log)
    band_top = X[:, 2].max(); mid = X[np.abs(X[:, 0]) < 1.0]; crotch_low = mid[:, 2].min()
    front = X[(X[:, 1] > 6)]; back = X[(X[:, 1] < -6)]
    inner = X[(np.abs(X[:, 0]) > 1.5) & (np.abs(X[:, 0]) < 6) ]; side = X[np.abs(X[:, 0]) > 13]
    d = {'band_top_z': round(float(band_top), 1), 'crotch_fabric_lowest_z': round(float(crotch_low), 1), 'anatomical_crotch_z': 76.5, 'crotch_sag_below_body_cm': round(76.5-float(crotch_low), 1),
         'waistband_top_to_crotch_fabric_cm': round(float(band_top-crotch_low), 1), 'inner_hem_lowest_z': round(float(inner[:, 2].min()), 1), 'side_hem_lowest_z': round(float(side[:, 2].min()), 1),
         'inseam_below_body_crotch_cm': round(76.5-float(inner[:, 2].min()), 1), 'front_rise_cm': float(rl.group(1)), 'back_rise_cm': float(rl.group(2)), 'pattern_crotch_z': float(lm.group(1)),
         'hem_width_at_hem_cm': round(float(np.ptp(X[(X[:, 0] > 2) & (X[:, 2] < inner[:, 2].min()+2.5)][:, 0])), 1) if len(X[(X[:, 0] > 2) & (X[:, 2] < inner[:, 2].min()+2.5)]) else None}
    out[t] = d; print('SHM', t, json.dumps(d))
json.dump(out, open('Saved/Codex/CharacterIdentity_20260930/shorts_measure.json', 'w'), indent=1)
