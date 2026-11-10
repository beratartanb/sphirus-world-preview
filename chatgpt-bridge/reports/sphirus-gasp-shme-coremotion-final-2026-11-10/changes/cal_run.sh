. Tools/Grip_20261106/g.sh
W(){ sleep $1; }
SV=Saved/SaveGames/SFSaveSlot.sav; BK=Saved/Codex/Day_20261107/videos/cal_slot.sav; [ -f $SV ] && mv $SV $BK
bash Tools/Day_20261107/ed.sh Tools/GASP_20261109/warm.py measure 600 | grep -c WARM
rm -f Saved/Codex/Day_20261107/cal_breath.json
PS; NOTHR; W 14
DX "[rel(k) for k in ('W','A','S','D','LeftShift')]; at(2200,-700,190,180,-12); exec(open(u.Paths.project_dir()+'Tools/GASP_20261109/swap.py',encoding='utf8').read()); swap('/Game/Sphirus/Player/GASP/BP_Sph_GASP_B.BP_Sph_GASP_B_C')" 2>&1 | grep -E "SWAP|rror" | cut -c1-200
W 3
G "exec(open(u.Paths.project_dir()+'Tools/GASP_20261109/cal_breath.py',encoding='utf8').read()); calrun()" 2>&1 | grep -E "CAL|rror" | cut -c1-200
for i in $(seq 1 40); do [ -f Saved/Codex/Day_20261107/cal_breath.json ] && break; W 2; done
cat Saved/Codex/Day_20261107/cal_breath.json; echo
PE; [ -f $BK ] && cp -p $BK $SV && cmp $BK $SV && echo SLOT_RESTORED
