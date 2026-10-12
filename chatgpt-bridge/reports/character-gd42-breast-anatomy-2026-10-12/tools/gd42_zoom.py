"""GD42 zoom strips: crops of the lit renders (1000x1700, figure 94 % of the height, z = 0 at row ~1650, 9.2 px/cm) for labels x views.
usage: blender -b --python gd42_zoom.py -- <rdir> <out.png> <region torso|legs|back> <views comma> label ..."""
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Saved/Codex/GD13_Identity_20261009/tools')); import gd13_img as gi
a = sys.argv[sys.argv.index('--')+1:]; R, OUT, REG, VIEWS = a[0], a[1], a[2], a[3].split(','); LABS = a[4:]
ROWS = {'torso': (380, 900), 'legs': (820, 1580), 'full': (150, 1650)}[REG]; COLS = (270, 730)
rows = []
for v in VIEWS:
    tiles = [gi.resize(gi.load(f'{R}/{l}_{v}_lit.png')[ROWS[0]:ROWS[1], COLS[0]:COLS[1], :3], 2*(COLS[1]-COLS[0]), 2*(ROWS[1]-ROWS[0])) for l in LABS]; rows.append(np.concatenate(tiles, 1))
gi.save(OUT, np.concatenate(rows, 0)); print('ZOOM_OK')
