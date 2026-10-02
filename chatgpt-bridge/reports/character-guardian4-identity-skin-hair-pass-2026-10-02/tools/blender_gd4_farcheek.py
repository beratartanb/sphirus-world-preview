"""GUARDIAN-4: 33 deg 3/4 (Tier A close, re-solved camera) far-cheek silhouette vs the Tier A far-cheek picks: candidate = outermost projected
skin vertex toward image right within a 3 px band at each pick height (px; + = candidate wider than the reference), plus chin / jaw-bottom picks.
usage: blender -b -P blender_gd4_farcheek.py -- <head.npy> [...]"""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Tools/CharacterLookdev_20260930'))
from gd_common import topix
PK = json.load(open('Saved/Codex/CharacterIdentity_20260930/ref_picks.json'))['close']; P = {p['name']: p['ref'] for p in PK['points']+PK['contours']}
for hp in sys.argv[sys.argv.index('--')+1:]:
    X = np.load(hp); S = X[:24049]; Q = topix('close', S[S[:, 1] > -2.0]); r = {}
    for k in ('farcheek_1', 'farcheek_2', 'farcheek_3', 'farcheek_4', 'farcheek_5', 'chin_p1', 'chin_p2', 'chin_p3'):
        x, y = P[k]; b = np.abs(Q[:, 1]-y) < 3.0; r[k] = round(float(Q[b, 0].max()-x), 1)
    print('FARCHEEK', os.path.basename(hp), json.dumps(r))
