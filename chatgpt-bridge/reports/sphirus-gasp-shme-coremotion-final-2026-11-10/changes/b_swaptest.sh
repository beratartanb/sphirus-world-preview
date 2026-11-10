. Tools/Grip_20261106/g.sh
W(){ sleep $1; }
SV=Saved/SaveGames/SFSaveSlot.sav; BK=Saved/Codex/Day_20261107/videos/swaptest_slot.sav; [ -f $SV ] && mv $SV $BK
bash Tools/Day_20261107/ed.sh Tools/GASP_20261109/warm.py measure 600 | grep WARM
PS; NOTHR; W 14
DX "[rel(k) for k in ('W','A','S','D','LeftShift')]; at(2200,-700,190,180,-12); exec(open(u.Paths.project_dir()+'Tools/GASP_20261109/swap.py',encoding='utf8').read()); swap('/Game/Sphirus/Player/GASP/BP_Sph_GASP_B.BP_Sph_GASP_B_C')" 2>&1 | grep -v "^OK" | cut -c1-300
W 3
G "p=PC.get_controlled_pawn(); ai=p.mesh.get_anim_instance(); k={c.get_name():c for c in p.get_components_by_class(u.SkeletalMeshComponent)}; print('PAWN',p.get_class().get_name(),'drv',p.mesh.get_skeletal_mesh_asset().get_name(),type(ai).__name__,'manny',type(k['Manny'].get_anim_instance()).__name__,'cam',[c.get_name() for c in p.get_components_by_class(u.CameraComponent) if c.is_active()],'vt',PC.get_view_target().get_name())" 2>&1 | grep -E "PAWN|rror|Trace" | cut -c1-400
G "tap('W')"; W 3; G "p=PC.get_controlled_pawn(); v=p.get_velocity(); ai=p.mesh.get_anim_instance(); print('MOVE spd',round(v.length()),'gait',ai.get_editor_property('Gait'),'anim',ai.get_editor_property('CurrentSelectedAnim').get_name() if ai.get_editor_property('CurrentSelectedAnim') else None,'db',ai.get_editor_property('CurrentSelectedDatabase').get_name() if ai.get_editor_property('CurrentSelectedDatabase') else None,'cmc',p.character_movement.max_walk_speed)" 2>&1 | grep -E "MOVE|rror" | cut -c1-300
G "rel('W')"; W 1; HR Saved/Codex/Day_20261107/frames/b_swaptest.png 1510x922
PE; [ -f $BK ] && cp -p $BK $SV && cmp $BK $SV && echo SLOT_RESTORED
