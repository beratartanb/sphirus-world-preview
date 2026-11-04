#!/bin/bash
# run_p3.sh : p3 = p2 + darker owned litter instances (FT override materials). Applies only the new-foliage and material steps on top of the
# p2 world, captures 8 verification stations, then the corrected light comparison (restore = pre-pass XR5 values, 24 places, re-apply p3 look)
# and the PF-look set at the same 24 places. Outputs cap/views_after_p3, cap/views_p3_xr5, cap/views_p3_pf.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
MY="/c/Users/berat/AppData/Local/Temp/claude/bbc6f8fdff1f8341/58bc34ab-b0fd-4574-9259-4850d781d32b/scratchpad"; D=Saved/Codex/PineForestRedesign_20261104; T=Tools/PineForestRedesign_20261104
PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; BPY="/c/Program Files/Blender Foundation/Blender 5.2/5.2/python/bin/python.exe"
export PFR_MANIFEST=Saved/Codex/SHME_V233_20261027/checkpoint/manifests/pfr_world.json
echo "P3 start $(date +%H:%M:%S)"
"$BPY" $T/pfr_design.py p3 2>&1 | grep -E "^DESIGN|Traceback|Error" | cut -c1-200
"$PY" -I -c "
import json; S=json.load(open('$D/data/stations_core.json')); want=['P0_refuge_house_back','P0_refuge_front_path','P1_landing_from_veranda','P1_landing_back','P2_rockshelf_back','D13_backyard_fwd','D09_hollow_fwd','D07_gate_fwd']
json.dump([s for s in S if s['name'] in want], open('$D/data/stations_p3.json','w'), indent=1); print('stations_p3', len(want))"
printf "import builtins\nbuiltins.PFR_MODE = 'apply'\nbuiltins.PFR_VARIANT = 'p3'\nbuiltins.PFR_STEPS = ['newfol', 'mats']\nexec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/PineForestRedesign_20261104/pfr_apply.py', encoding='utf-8').read(), 'pfr_apply.py', 'exec'), {'__name__': '__job__'})\n" > "$MY/apply_p3.py"
rm -f "$D/design/p3/apply_apply.json"; bash $T/pfr_chain.sh "job:write:$MY/apply_p3.py:600" | tail -1
for i in $(seq 1 100); do [ -f "$D/design/p3/apply_apply.json" ] && break; sleep 3; done
"$PY" -I -c "
import json; r=json.load(open('$D/design/p3/apply_apply.json')); print('apply p3 ok', r.get('ok'), 'problems', r.get('problems'), 'ft_materials_set', r.get('ft_materials_set'), 'newmats', r.get('newmats_created'))" | cut -c1-600
bash $T/pfr_chain.sh "views:after_p3:lit:$D/data/stations_p3.json" | tail -1
bash $T/run_lookcmp.sh p3 2>&1 | grep -E "look_source|problems|copied|LOOKCMP" | cut -c1-300
bash $T/pfr_chain.sh "views:p3_pf:lit:$D/data/stations_places.json" | tail -1
echo "P3 done $(date +%H:%M:%S)"
