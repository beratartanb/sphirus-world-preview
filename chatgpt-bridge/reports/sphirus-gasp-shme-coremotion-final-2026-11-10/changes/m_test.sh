. Tools/Grip_20261106/g.sh
W(){ sleep $1; }
SV=Saved/SaveGames/SFSaveSlot.sav; BK=Saved/Codex/Day_20261107/videos/mtest_slot.sav; [ -f $SV ] && mv $SV $BK
bash Tools/Day_20261107/ed.sh Tools/GASP_20261109/warm.py measure 600 | grep -c WARM
PS; NOTHR; W 14
DX "[rel(k) for k in ('W','A','S','D','LeftShift')]; at(2200,-700,190,180,-12); exec(open(u.Paths.project_dir()+'Tools/GASP_20261109/swap.py',encoding='utf8').read()); swap('/Game/Sphirus/Player/GASP/BP_Sph_GASP_B.BP_Sph_GASP_B_C')" 2>&1 | grep -E "SWAP|rror" | cut -c1-200
W 3
Q="p=PC.get_controlled_pawn(); ai=p.mesh.get_anim_instance(); k={c.get_name():c for c in p.get_components_by_class(u.SkeletalMeshComponent)}; v=k['Manny']; m=ai.get_current_active_montage(); print('MT',m.get_name() if m else None,'handR',[round(x) for x in (v.get_socket_location('hand_r')-p.get_actor_location()).to_tuple()],'handL',[round(x) for x in (v.get_socket_location('hand_l')-p.get_actor_location()).to_tuple()],'pelvisZ',round(v.get_socket_location('pelvis').z-p.get_actor_location().z,1))"
G "$Q" 2>&1 | grep -E "MT|rror" | cut -c1-300
G "p=PC.get_controlled_pawn(); ai=p.mesh.get_anim_instance(); print('PLAY',ai.montage_play(u.load_asset('/Game/Sphirus/Player/Anim/Day/AM_GR_Day_Chop'),1.0))" 2>&1 | grep -E "PLAY|rror" | cut -c1-200
W 1.5; G "$Q" 2>&1 | grep -E "MT|rror" | cut -c1-300
W 2.5; G "$Q" 2>&1 | grep -E "MT|rror" | cut -c1-300
HR Saved/Codex/Day_20261107/frames/mtest_chop.png 1510x922
G "p=PC.get_controlled_pawn(); ai=p.mesh.get_anim_instance(); ai.montage_stop(0.2,None); print('PLAY',ai.montage_play(u.load_asset('/Game/Sphirus/Player/Anim/Day/AM_GR_Day_CarryArms'),1.0))" 2>&1 | grep -E "PLAY|rror" | cut -c1-200
G "tap('W')"; W 1.5; G "$Q" 2>&1 | grep -E "MT|rror" | cut -c1-300
HR Saved/Codex/Day_20261107/frames/mtest_carry.png 1510x922
G "rel('W')"; PE; [ -f $BK ] && cp -p $BK $SV && cmp $BK $SV && echo SLOT_RESTORED
