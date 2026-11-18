#!/bin/bash
# skin_dx.sh <tag>: read-only diagnosis of the white skin patches in direct sun indoors. Same indoor spot and camera as
# bio4.sh; runtime console variables only (reset afterwards), no asset or save change.
cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"; . Tools/Grip_20261106/g.sh
W(){ sleep $1; }
TG=${1:-a}; O=Saved/UE59Work/skin_dx_$TG; mkdir -p $O
SV=Saved/SaveGames/SFSaveSlot.sav; [ -f $SV ] || { echo NO_USER_SLOT; exit 8; }
USHA=$(sha1sum $SV | cut -c1-40); cp -p $SV $O/slot_user.sav; mv $SV $O/slot_user_moved.sav
restore(){ h=$(sha1sum $SV 2>/dev/null | cut -c1-40); if [ "$h" != "$USHA" ]; then [ -f $SV ] && mv $SV $O/slot_written_by_test.sav; cp -p $O/slot_user.sav $SV; fi; echo "USER_SLOT $(sha1sum $SV | cut -c1-40)"; }
trap restore EXIT
NK="exec(open(u.Paths.project_dir()+'Tools/Neck_20261114/nk.py',encoding='utf8').read())"
for k in 1 2 3; do o=$(bash Tools/Embodied_20261105/relaunch.sh emb_sk$TG$k 2>&1 | tail -1); echo "$o" | cut -c1-40; echo "$o" | grep -q RUNNER_READY && break; taskkill //IM UnrealEditor.exe //F >/dev/null 2>&1; sleep 10; done
bash Tools/Day_20261107/ed.sh Tools/GASP_20261109/warm.py measure 600 | grep -c WARM
PS; NOTHR; W 18
DX "[rel(k) for k in ('W','A','S','D','C','SpaceBar','LeftShift','LeftControl')]; at(397,100,241,90,-8); print(1)" | tail -1; W 5
DX "$NK; cam('q34',300,38,0,'spine_03')" >/dev/null; W 1.5
shot(){ W 2.5; HR $O/$1.png >/dev/null; }
shot base
G "cmd('r.SubsurfaceScattering 0')" >/dev/null; shot sss_off; G "cmd('r.SubsurfaceScattering 1')" >/dev/null
G "cmd('r.SSS.Checkerboard 0')" >/dev/null; shot checker_off; G "cmd('r.SSS.Checkerboard 2')" >/dev/null
G "cmd('r.BloomQuality 0')" >/dev/null; shot bloom_off; G "cmd('r.BloomQuality 5')" >/dev/null
G "cmd('r.SSS.Burley.Quality 0')" >/dev/null; shot burley_q0; G "cmd('r.SSS.Burley.Quality 1')" >/dev/null
G "cmd('viewmode lit_detaillighting')" >/dev/null; shot detail_lighting; G "cmd('viewmode lit')" >/dev/null
shot base_again
W 1; PE; W 3
ls $O/*.png | wc -l
