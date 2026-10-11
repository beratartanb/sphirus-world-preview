"""GD36: horizontally flipped copy of an image (to compare the right-turned view with the mirrored left-turned view). usage: -- <in> <out>"""
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'GD13_Identity_20261009', 'tools')); import gd13_img as gi
a = sys.argv[sys.argv.index('--')+1:]; I = gi.load(a[0]); gi.save(a[1], I[:, ::-1].copy()); print('FLIP_OK')
