#!/bin/bash
# pie_probe.sh "<x,y,z,yaw,pitch> <python-list-of-(tag,script)>" ...: PIE, place the player at each spot, run each probe. Test save moved aside and restored.
cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"; . Tools/Grip_20261106/g.sh; W(){ sleep $1; }
SV=Saved/SaveGames/SFSaveSlot.sav; O=Saved/UE59Work/pieprobe; mkdir -p $O; USHA=$(sha1sum $SV | cut -c1-40); cp -p $SV $O/slot_user.sav; mv $SV $O/slot_user_moved.sav
restore(){ [ -f $SV ] && mv $SV $O/slot_written_by_probe.sav; cp -p $O/slot_user.sav $SV; echo "USER_SLOT $(sha1sum $SV | cut -c1-40)"; }; trap restore EXIT
PS; NOTHR; W 16
for spot in "$@"; do
  at=${spot%% *}; py=${spot#* }
  DX "[rel(k) for k in ('W','A','S','D','C','SpaceBar','LeftShift','LeftControl')]; at($at); print(1)" >/dev/null; W ${PSET:-4}
  G "$py" 6 | tail -1
done
W 1; PE; W 3
