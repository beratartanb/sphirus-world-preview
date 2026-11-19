#!/bin/bash
# seqK.sh: shadow LOD bias stills (player camera, PIE, HighResShot without UI) at an indoor and an outdoor spot for -1.5 / -0.5 / 0.
cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"; . Tools/Grip_20261106/g.sh; W(){ sleep $1; }
O=Saved/UE59Work/shadowstills; mkdir -p $O
SV=Saved/SaveGames/SFSaveSlot.sav; cp -p $SV $O/slot_user.sav; mv $SV $O/slot_moved.sav
restore(){ [ -f $SV ] && mv $SV $O/slot_written.sav; cp -p $O/slot_user.sav $SV; echo "SLOT $(sha1sum $SV | cut -c1-40)"; }; trap restore EXIT
PS; NOTHR; W 16
for spot in "in 520 160 241 180 -8" "out 2640 420 322 -83 -10"; do set -- $spot
  DX "[rel(k) for k in ('W','A','S','D','LeftShift')]; at($2,$3,$4,$5,$6); print(1)" >/dev/null; W 6
  for b in -1.5 -0.5 0; do G "cmd('r.Shadow.Virtual.ResolutionLodBiasDirectional $b'); print(1)" >/dev/null; W 3; HR $O/$1_b$b.png 1920x1080; done
done
G "cmd('r.Shadow.Virtual.ResolutionLodBiasDirectional -1.5'); print(1)" >/dev/null
W 1; PE; W 3
