#!/bin/bash
# gd_frames.sh <prefix> [sets] : crop <prefix>_<set>_reffront / refclose2 captures into the reference frames -> Saved/Codex/CharacterGuardian_20261001/frames/<prefix>_<set>_{F,C}.png (+ 50% overlays _ovF/_ovC for real)
set -u; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; P=$1; SETS=${2:-clay real hair}; T=Tools/CharacterLookdev_20260930; O=Saved/Codex/CharacterGuardian_20261001/frames; mkdir -p $O
C="$(cygpath -m "$(pwd)/Saved/Codex/CharacterLookdev_20260930/captures")"; OM="$(cygpath -m "$(pwd)/$O")"; TD="$(cygpath -m "$(pwd)/Saved/Codex/CharacterIdentity_20260930/track")"
BL="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"
RR=$("$BL" -b --factory-startup --python-expr "import sys; sys.path.insert(0,'Tools/CharacterLookdev_20260930'); from gd_common import crop_rect; f=crop_rect('front'); c=crop_rect('close'); print('RECTS', '%.5f|%.5f|%.5f|%.5f' % f, '%.5f|%.5f|%.5f|%.5f' % c)" 2>&1 | grep RECTS); RF=$(echo $RR | cut -d' ' -f2); RC=$(echo $RR | cut -d' ' -f3)
J=(); for s in $SETS; do J+=("$C/${P}_${s}_reffront_custom.png|$OM/${P}_${s}_F.png|${RF}|800|960" "$C/${P}_${s}_refclose2_custom.png|$OM/${P}_${s}_C.png|${RC}|794|940"); done
J+=("$C/${P}_real_reffront_custom.png|$OM/${P}_ovF.png|${RF}|800|960|$TD/ref_front_x4.png" "$C/${P}_real_refclose2_custom.png|$OM/${P}_ovC.png|${RC}|794|940|$TD/ref_close_x2.png")
"$BL" -b --factory-startup --python $T/id_crop_rect.py -- "${J[@]}" 2>&1 | grep -c RECT
