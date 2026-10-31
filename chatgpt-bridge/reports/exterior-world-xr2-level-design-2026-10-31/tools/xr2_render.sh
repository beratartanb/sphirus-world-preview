#!/bin/bash
# xr2_render.sh <variant> : plan / clay maps with routes, ring, stands, spawn footprints + walkability map for a design variant.
V=$1; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"
PY="/c/Program Files/Blender Foundation/Blender 5.2/5.2/python/bin/python.exe"; R=Saved/Codex/ExteriorRedesign_20261031/recon; D=Saved/Codex/ExteriorWorld_XR2_20261031
"$PY" - "$D/design/overlay_$V.json" "$D/design/spawn_$V.json" "$D/design/overlay_${V}_sp.json" <<'PYEOF'
import json, sys, math
ov = json.load(open(sys.argv[1])); sp = json.load(open(sys.argv[2]))
C = {'ring_rock': [0.35, 0.3, 0.3], 'r6_outcrop': [0.35, 0.3, 0.3], 'ring_deadfall': [0.55, 0.3, 0.1], 'yard_windthrow': [0.55, 0.3, 0.1], 'windthrow': [0.55, 0.3, 0.1], 'single_log': [0.55, 0.3, 0.1], 'inner_rock': [0.35, 0.3, 0.3], 'inner_deadfall': [0.55, 0.3, 0.1], 'inner_bank': [0.35, 0.3, 0.3], 'landmark': [0.9, 0.2, 0.9], 'decal': [0.6, 0.45, 0.2], 'wade_limit': [0.2, 0.9, 0.9]}
for s in sp:
    c, n = math.cos(math.radians(s['yaw'])), math.sin(math.radians(s['yaw']))
    pts = [(s['fx'] + a * s['hx'] * c - b * s['hy'] * n, s['fy'] + a * s['hx'] * n + b * s['hy'] * c) for a, b in ((-1, -1), (1, -1), (1, 1), (-1, 1), (-1, -1))]
    ov['polys'].append({'pts': pts, 'rgb': C.get(s['kind'], [0, 0, 0]), 'w': 2 if s['kind'] != 'wade_limit' else 1})
json.dump(ov, open(sys.argv[3], 'w'))
PYEOF
"$PY" Tools/ExteriorRedesign_20261031/xr_maps.py $R $D/design/height_$V.u16 $D/design/foliage_full_$V.json $D/maps/${V}_plan.png -6000 5500 -8500 10500 5 plan $D/design/overlay_${V}_sp.json | tail -1
"$PY" Tools/ExteriorRedesign_20261031/xr_maps.py $R $D/design/height_$V.u16 $D/design/foliage_full_$V.json $D/maps/${V}_clay.png -6000 5500 -8500 10500 5 clay $D/design/overlay_$V.json | tail -1
"$PY" Tools/ExteriorWorld_XR2_20261031/xr2_walkmap.py $D/design/height_$V.u16 $D/design/foliage_full_$V.json $R/actors.json $D/maps/$V $D/design/spawn_$V.json
