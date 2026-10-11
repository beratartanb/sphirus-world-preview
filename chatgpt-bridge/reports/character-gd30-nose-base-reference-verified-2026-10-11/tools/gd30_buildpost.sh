#!/bin/bash
# gd30_buildpost.sh <SRC> <TAG> <PUSH_mm> <FILL_mm> : posterior-lobule step on top of a bottom-lowered head: back-lateral normal push of the lobule's
# posterior face (both sides), fill-only crease softening, junction relaxation (4 zones x 10 iterations)
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; V=Saved/Codex/GD30_Identity_20261011; B="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"; Wp() { cygpath -w "$(pwd)/$1"; }; H() { echo "$(Wp $V/data/head_$1.npy)"; }
S=$1; T=$2; P=$3; F=${4:-1.5}
"$B" -b --factory-startup --python "$(Wp $V/tools/gd30_normal_push.py)" -- "$(H $S)" "$(Wp $V/data/head_topo.npz)" "$(H ${T}_1)" "[1.37,12.85,158.7,0.6,0.8,0.8,0.2,0.3,0.3]" $P "[0.45,-0.9,0]" 0.2 2>&1 | grep -E "rror"
"$B" -b --factory-startup --python "$(Wp $V/tools/gd30_normal_push.py)" -- "$(H ${T}_1)" "$(Wp $V/data/head_topo.npz)" "$(H ${T}_2)" "[-1.83,12.85,158.7,0.6,0.8,0.8,0.2,0.3,0.3]" $P "[-0.45,-0.9,0]" 0.2 2>&1 | grep -E "rror"
"$B" -b --factory-startup --python "$(Wp $V/tools/gd30_groovefill.py)" -- "$(H ${T}_2)" "$(Wp $V/data/head_topo.npz)" "$(H $T)" "[[1.42,12.7,158.8,0.5,0.7,0.8,0.15,0.25,0.3,$F],[-1.88,12.7,158.8,0.5,0.7,0.8,0.15,0.25,0.3,$F]]" 0.2 1.0 4 2 2>&1 | grep -E "rror"
for Zb in "[1.5,12.85,158.5,0.45,0.45,0.45,0.15,0.15,0.15]" "[-1.96,12.85,158.5,0.45,0.45,0.45,0.15,0.15,0.15]" "[1.48,12.84,159.09,0.38,0.38,0.38,0.12,0.12,0.12]" "[-1.94,12.84,159.09,0.38,0.38,0.38,0.12,0.12,0.12]"; do "$B" -b --factory-startup --python "$(Wp $V/tools/gd30_crease_smooth.py)" -- "$(H $T)" "$(Wp $V/data/head_topo.npz)" "$(H ${T}_s)" "$Zb" 10 0.5 -1.0 0.3 2>&1 | grep -E "rror"; cp $V/data/head_${T}_s.npy $V/data/head_$T.npy; done
rm -f $V/data/head_${T}_1.npy $V/data/head_${T}_2.npy $V/data/head_${T}_s.npy; echo BUILDPOST_${T}_OK
