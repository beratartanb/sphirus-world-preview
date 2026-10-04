#!/bin/bash
# build_hair.sh <tag> : Blender build of Saved/Codex/GD11_HeadRefinementI_20261004/hair/<tag> with the E builder; prints HAIR_OK or BUILD_FAILED
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; E=Saved/Codex/GD11_HeadRefinementI_20261004; T=Tools/CharacterLookdev_20260930
env $(grep -v '^$' $E/hair/$1/build_env.txt | tr '\n' ' ') "/c/Program Files/Blender Foundation/Blender 5.2/blender.exe" -b --factory-startup --python "$(cygpath -w "$(pwd)/$T/blender_g11ri_hair.py")" -- "$(cygpath -w "$(pwd)/Saved/Codex/CharacterFinal_20260929/sculpt_package_v6.json.gz")" "$(cygpath -w "$(pwd)/$E/hair/$1")" > $E/hair/$1/build_log.txt 2>&1
[ -f $E/hair/$1/strands.npz ] && grep -q HAIR_OK $E/hair/$1/build_log.txt && echo "HAIR_OK $1" || { echo "BUILD_FAILED $1"; grep -E "Error|line [0-9]+" $E/hair/$1/build_log.txt | head -4; }
