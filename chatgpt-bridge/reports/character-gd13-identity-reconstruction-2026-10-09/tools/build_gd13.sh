#!/bin/bash
# build_gd13.sh [out.npy] : rebuilds the GD13 Identity Master head from the GD11 F1H head with the exact GD13 operator chain
#   S2 (large-form re-proportioning: lower-face narrowing, gonial lift, radix, alae, lip roll-in, lower-lip base, chin pad)
#   S3c (eyelid aperture over the eyeball + lid relax, lateral canthus, nose tip rotation, mouth corners, vermilion borders)
#   S4 (malar prominence, submalar soft plane, lateral brow overhang, tip lobules, lip centre volume)
#   S5 (posterior + mid mandibular border lift)   S6 (jaw corner / mid-jaw / radix relax vs F1H) + unfold
#   SF1 (lips set back + rounded volume)  S9 (mouth corners, nose tip lobules, alar rims)  SF3 (alae, canthus / corner relax) + unfold
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; O=Saved/Codex/GD13_Identity_20261009; OUT=${1:-$O/build/head_GD13_rebuilt.npy}; mkdir -p $O/build
B="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"; W() { cygpath -w "$(pwd)/$1"; }; F=$O/data/head_F1H.npy
S() { "$B" -b --factory-startup --python "$(W $O/tools/gd13_sculpt.py)" -- "$(W $1)" "$(W $O/ops/$2.json)" "$(W $3)" ${4:+"$(W $4)"} 2>&1 | grep -E "SCULPT_OK|Error"; }
U() { "$B" -b --factory-startup --python "$(W Tools/CharacterLookdev_20260930/blender_g11yy_unfold.py)" -- "$(W $F)" "$(W $1)" "$(W $2)" 0.35 2 600 2>&1 | grep -E "UNFOLD done|Error"; }
S $F S2 $O/build/b_S2.npy; S $O/build/b_S2.npy S3c $O/build/b_S3c.npy; S $O/build/b_S3c.npy S4 $O/build/b_S4.npy; S $O/build/b_S4.npy S5 $O/build/b_S5.npy
S $O/build/b_S5.npy S6 $O/build/b_S6.npy $F; U $O/build/b_S6.npy $O/build/b_S6u.npy
S $O/build/b_S6u.npy SF1 $O/build/b_F1.npy $F; S $O/build/b_F1.npy S9 $O/build/b_F2.npy $F; S $O/build/b_F2.npy SF3 $O/build/b_F3.npy $F; U $O/build/b_F3.npy $OUT
