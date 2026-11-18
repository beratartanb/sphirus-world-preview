#!/bin/bash
# skin_pie.sh <tag> <python-file-or-empty>...: PIE at the indoor look spot (bio4 camera), run each given python (runtime only),
# take a still after each: Saved/UE59Work/skin_<tag>/<n>_<name>.png. No asset or save change.
cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"; . Tools/Grip_20261106/g.sh
W(){ sleep $1; }
TG=$1; shift; O=Saved/UE59Work/skin_$TG; mkdir -p $O
SV=Saved/SaveGames/SFSaveSlot.sav; [ -f $SV ] || { echo NO_USER_SLOT; exit 8; }
USHA=$(sha1sum $SV | cut -c1-40); cp -p $SV $O/slot_user.sav; mv $SV $O/slot_user_moved.sav
restore(){ h=$(sha1sum $SV 2>/dev/null | cut -c1-40); if [ "$h" != "$USHA" ]; then [ -f $SV ] && mv $SV $O/slot_written_by_test.sav; cp -p $O/slot_user.sav $SV; fi; echo "USER_SLOT $(sha1sum $SV | cut -c1-40)"; }
trap restore EXIT
NK="exec(open(u.Paths.project_dir()+'Tools/Neck_20261114/nk.py',encoding='utf8').read())"
for k in 1 2 3; do o=$(bash Tools/Embodied_20261105/relaunch.sh emb_sp$TG$k 2>&1 | tail -1); echo "$o" | cut -c1-40; echo "$o" | grep -q RUNNER_READY && break; taskkill //IM UnrealEditor.exe //F >/dev/null 2>&1; sleep 10; done
bash Tools/Day_20261107/ed.sh Tools/GASP_20261109/warm.py measure 600 | grep -c WARM
PS; NOTHR; W 18
DX "[rel(k) for k in ('W','A','S','D','C','SpaceBar','LeftShift','LeftControl')]; at(${SKAT:-397,100,241,90,-8}); print(1)" | tail -1; W 5
DX "$NK; cam('q34',300,38,0,'spine_03')" >/dev/null; W 2.5; HR $O/0_base.png >/dev/null
n=1; for f in "$@"; do G "exec(open(u.Paths.project_dir()+'Tools/UE59_20261116/$f',encoding='utf8').read())" 6 | tail -2; W 3; HR $O/${n}_${f%.py}.png >/dev/null; n=$((n+1)); done
W 1; PE; W 3; ls $O/*.png | wc -l
