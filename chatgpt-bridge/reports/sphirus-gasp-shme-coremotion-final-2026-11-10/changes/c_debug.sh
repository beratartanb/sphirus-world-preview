. Tools/Grip_20261106/g.sh
W(){ sleep $1; }
SV=Saved/SaveGames/SFSaveSlot.sav; BK=Saved/Codex/Day_20261107/videos/cdebug_slot.sav; [ -f $SV ] && mv $SV $BK
bash Tools/Day_20261107/ed.sh Tools/GASP_20261109/warm.py measure 600 | grep -c WARM
PS; NOTHR; W 14
DX "[rel(k) for k in ('W','A','S','D','LeftShift')]; at(2200,-700,190,180,-12); exec(open(u.Paths.project_dir()+'Tools/GASP_20261109/swap.py',encoding='utf8').read()); swap('/Game/Sphirus/Player/GASP/BP_Sph_GASP_B.BP_Sph_GASP_B_C')" 2>&1 | grep -E "SWAP|rror" | cut -c1-200
Q="p=PC.get_controlled_pawn(); m=[c for c in p.get_components_by_class(u.ActorComponent) if c.get_name()=='SphMotion'][0]; print('MO',{k:(round(m.get_editor_property(k),3) if isinstance(m.get_editor_property(k),float) else m.get_editor_property(k)) for k in ('Enabled','EffortEnabled','SpeedScale','AccScale','Acc','TurnSev','Demand','E','EUse','ReqLoad','SpeedNow')},'in',p.get_last_movement_input_vector(),'v',round(p.get_velocity().length()),'max',p.character_movement.max_walk_speed,'tick',m.is_component_tick_enabled())"
W 2; G "$Q" 2>&1 | grep -E "MO|rror" | cut -c1-500
G "tap('W')"; W 2; G "$Q" 2>&1 | grep -E "MO|rror" | cut -c1-500
G "tap('S')"; G "rel('W')"; W 0.3; G "$Q" 2>&1 | grep -E "MO|rror" | cut -c1-500
G "rel('S')"; PE; [ -f $BK ] && cp -p $BK $SV && cmp $BK $SV && echo SLOT_RESTORED
