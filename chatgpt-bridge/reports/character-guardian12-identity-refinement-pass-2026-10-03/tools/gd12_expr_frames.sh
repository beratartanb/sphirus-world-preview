#!/bin/bash
# gd2_expr_frames.sh <prefix> : crop <prefix>_expr_<case>_{reffront,refclose2} captures into the reference frames -> Guardian2 frames/<prefix>_expr_<case>_{F,C}.png
set -u; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; P=$1; T=Tools/CharacterLookdev_20260930; O=Saved/Codex/CharacterGuardian12_20261003/frames
C="$(cygpath -m "$(pwd)/Saved/Codex/CharacterLookdev_20260930/captures")"; OM="$(cygpath -m "$(pwd)/$O")"; BL="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"
RR=$("$BL" -b --factory-startup --python-expr "import sys; sys.path.insert(0,'Tools/CharacterLookdev_20260930'); from gd_common import crop_rect; f=crop_rect('front'); c=crop_rect('close'); print('RECTS', '%.5f|%.5f|%.5f|%.5f' % f, '%.5f|%.5f|%.5f|%.5f' % c)" 2>&1 | grep RECTS); RF=$(echo $RR | cut -d' ' -f2); RC=$(echo $RR | cut -d' ' -f3)
J=(); for c in neutral ref_expr_soft ref_expr ref_expr_firm squint_half squint; do J+=("$C/${P}_expr_${c}_reffront_custom.png|$OM/${P}_expr_${c}_F.png|${RF}|800|960" "$C/${P}_expr_${c}_refclose2_custom.png|$OM/${P}_expr_${c}_C.png|${RC}|794|940"); done
"$BL" -b --factory-startup --python $T/id_crop_rect.py -- "${J[@]}" 2>&1 | grep -c RECT
