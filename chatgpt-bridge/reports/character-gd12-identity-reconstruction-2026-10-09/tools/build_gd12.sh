#!/bin/bash
# build_gd12.sh : rebuilds the GD12 identity master head from F1H with the full recipe (surface brushes -> orbit cleanup -> inner brow -> cleanup -> lids -> unfold -> lip / mentolabial cleanup)
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; O=Saved/Codex/GD12_Identity_20261009; T=Tools/CharacterLookdev_20260930; B="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"; Wp() { cygpath -w "$(pwd)/$1"; }
S() { "$B" -b --factory-startup --python "$(Wp $T/blender_gd12_sculpt.py)" -- "$(Wp $O/build/$1)" "$(Wp $O/ops/$2)" "$(Wp $O/build/$3)" 2>&1 | grep -E "SCULPT_OK|Error"; }
S head_F1H.npy G12g.json B1.npy; S B1.npy G12h_orbit.json B2.npy; S B2.npy G12i_brow.json B3.npy; S B3.npy G12j_clean.json B4.npy
"$B" -b --factory-startup --python "$(Wp $T/blender_gd12_lids.py)" -- "$(Wp $O/build/B4.npy)" "$(Wp $O/build/B5.npy)" 0.15 0.05 2>&1 | grep LIDS
S B5.npy GD12_lip.json B6.npy; S B6.npy GD12_mento.json B7.npy
"$B" -b --factory-startup --python "$(Wp $T/blender_g11yy_unfold.py)" -- "$(Wp $O/head_F1H.npy)" "$(Wp $O/build/B7.npy)" "$(Wp $O/head_GD12_final.npy)" 0.35 2 600 2>&1 | grep "UNFOLD done"
