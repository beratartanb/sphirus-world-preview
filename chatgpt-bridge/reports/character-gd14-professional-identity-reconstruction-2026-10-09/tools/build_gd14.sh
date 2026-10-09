#!/bin/bash
# build_gd14.sh : documented reproduction chain of GD14 W9 (final candidate). Every step writes NEW names only (guards refuse existing assets).
# 0  base E = GD11 MHC_GD11_E (unchanged)                -> duplicate MHC_GD14_W0 (ue_gd14_mhc.py op dup)
# 1  MetaHuman Creator landmark sculpt (ops/W2.json)      -> gd14_targets.py (W0 landmarks + ops) -> gd14_step.sh MHC_GD14_W0 MHC_GD14_W2 tgt_W2.json W2 12
# 2  real Blender sculpt brushes, GUI session (ops/C1.json, outward-corrected winding) on data/head_W2.npy:
#      blender --factory-startup --python gd14_bsculpt.py -- head_W2.npy head_topo.npz C1.json head_W9S0.npy log.json
# 3  technical lid-margin fold repair (local blend to E):  gd14_foldrepair.py -- head_W9S0.npy head_E.npy head_W9S.npy "[[-4.78,10.85,162.35,0.35,0.75],[-3.92,11.13,162.66,0.15,0.4],[3.18,11.19,162.98,0.15,0.4]]"
# 4  transfer to MetaHuman (fit + 2 residual-feedback fits): gd14_fitfb.sh MHC_GD14_W2 MHC_GD14_W9 head_W9S.npy W9
# 5  auto-rig + DNA + face + bindings + composition:        gd14_ue_cycle.sh MHC_GD14_W9 w9
# 6  captures / tracker / boards:                            gd14_caps.sh, gd14_track.sh, make_gd14_boards.sh w9
set -e; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; W=Saved/Codex/GD14_Identity_20261009; Wp() { cygpath -w "$(pwd)/$1"; }
[ "${1:-}" = "--brush-stage-only" ] || { echo "UE steps are listed above; run them one by one (each needs the editor runner + gd14_memguard.sh)"; exit 0; }
timeout 1500 "/c/Program Files/Blender Foundation/Blender 5.2/blender.exe" --factory-startup --python "$(Wp $W/tools/gd14_bsculpt.py)" -- "$(Wp $W/data/head_W2.npy)" "$(Wp $W/data/head_topo.npz)" "$(Wp $W/ops/C1.json)" "$(Wp $W/data/head_W9S0_rebuild.npy)" "$(Wp $W/bs_W9S_rebuild_log.json)"
"/c/Program Files/Blender Foundation/Blender 5.2/blender.exe" -b --factory-startup --python "$(Wp $W/tools/gd14_foldrepair.py)" -- "$(Wp $W/data/head_W9S0_rebuild.npy)" "$(Wp $W/data/head_E.npy)" "$(Wp $W/data/head_W9S_rebuild.npy)" "[[-4.78, 10.85, 162.35, 0.35, 0.75], [-3.92, 11.13, 162.66, 0.15, 0.4], [3.18, 11.19, 162.98, 0.15, 0.4]]" | grep REPAIR
