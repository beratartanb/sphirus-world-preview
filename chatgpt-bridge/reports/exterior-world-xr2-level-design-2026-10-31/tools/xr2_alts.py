"""xr2_alts.py <variant> : overlay JSONs for the three updated r6 alternatives drawn over the implemented XR2 plan.
  r6-A (implemented): pond path east + faint west-shore loop; rear trail through the yard gate; landing dock = first destination.
  r6-B (linear):      the west shore is closed (marsh + deadfall at the NW and SW pond corners): pond path ends at the far-shore glade.
  r6-C (grand loop):  the ring moves out over the east ridge; a ridge trail links the saddle back to the SE inlet (one world loop)."""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import xr2_layout as LY
V = sys.argv[1]; D = 'Saved/Codex/ExteriorWorld_XR2_20261031'
base = json.load(open('%s/design/overlay_%s_sp.json' % (D, V)))
ALT = {
    'r6A': {'polys': [{'pts': LY.WEST_LOOP, 'rgb': [0.45, 0.45, 1.0], 'w': 4}], 'title': 'r6-A (uygulandi): gol dongusu - dogu ana yol + bati zor iz'},
    'r6B': {'polys': [{'pts': [(-2500, 2500), (-3300, 2300), (-4300, 2100)], 'rgb': [0.9, 0.1, 0.1], 'w': 5},
                      {'pts': [(-2900, 7900), (-3500, 8500), (-4100, 8900)], 'rgb': [0.9, 0.1, 0.1], 'w': 5}],
            'title': 'r6-B: dogrusal - bati kiyi kapali (sazlik+devrik), gol yolu karsi kiyida biter'},
    'r6C': {'polys': [{'pts': [(1380, -6250), (2600, -6900), (3700, -5600), (4100, -3600), (4000, -1100), (4000, 1500), (3700, 3500), (3800, 5500), (3900, 7300), (3650, 8000)],
                       'rgb': [1.0, 0.5, 0.0], 'w': 4},
                      {'pts': [(4800, -6500), (5600, -3000), (5600, 1000), (5000, 5000), (5300, 8500)], 'rgb': [0.9, 0.1, 0.1], 'w': 3}],
            'title': 'r6-C: buyuk dongu - sirttan dogu sirti boyunca kuru dereye inen ikinci yol (halka disari tasinir)'}}
for k, a in ALT.items():
    o = {'polys': base['polys'] + a['polys'], 'discs': base.get('discs', [])}
    json.dump(o, open('%s/design/overlay_%s_%s.json' % (D, V, k), 'w')); print(k, a['title'])
