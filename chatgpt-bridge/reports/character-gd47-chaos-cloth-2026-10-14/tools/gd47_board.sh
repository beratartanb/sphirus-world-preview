#!/bin/bash
# gd47_board.sh <out.png> <cell_h> <crop "x0 y0 x1 y1"|-> row1(comma list of files) [row2 ...] : img_grid wrapper with Windows paths
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; OUT=$1; CH=$2; CR=$3; shift 3; rows=()
for r in "$@"; do w=""; IFS=',' read -ra fs <<< "$r"; for f in "${fs[@]}"; do w="$w${w:+,}$(cygpath -w "$(pwd)/$f")"; done; rows+=("$w"); done
args=("$(cygpath -w "$(pwd)/$OUT")" "$CH" "${rows[@]}"); [ "$CR" != "-" ] && args+=($CR)
"/c/Program Files/Blender Foundation/Blender 5.2/blender.exe" -b --python Saved/Codex/GD46_GarmentFit_20261013/tools/img_grid.py -- "${args[@]}" 2>&1 | grep -iE 'error|Traceback' ; ls -la "$OUT" | awk '{print $5, $9}'
