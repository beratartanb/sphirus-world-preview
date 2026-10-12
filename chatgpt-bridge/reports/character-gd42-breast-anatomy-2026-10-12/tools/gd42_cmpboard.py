"""GD42: before/after clay comparison strips (cropped body) for the given labels and views. usage: blender -b --python gd42_cmpboard.py -- <rdir> <out.png> <views comma> label ..."""
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Saved/Codex/GD13_Identity_20261009/tools')); import gd13_img as gi
a = sys.argv[sys.argv.index('--')+1:]; R, OUT, VIEWS = a[0], a[1], a[2].split(','); LABS = a[3:]
rows = []
for v in VIEWS:
    tiles = [gi.resize(gi.load(f'{R}/{l}_{v}_'+os.environ.get('CMP_MODE', 'clay')+'.png')[150:1650, 250:750, :3], 420, 1260) for l in LABS]; rows.append(np.concatenate(tiles, 1))
gi.save(OUT, np.concatenate(rows, 1) if len(VIEWS) > 1 else rows[0]); print('CMP_OK')
