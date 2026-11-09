# cm_steady3.py (write): GR_SteadyEnable default back to TRUE. The "full database selects the loop by itself" reading
# (G_full.json) was wrong: that run still used the WalkLoop database (the test prelude did not take effect). With the full
# Walk database alone (G_gaits5.json) the body is back in the Walk_Fwd_Start 0.7-1.2 s window and the loop is never
# played, even after the double-evaluation fix. The steady-state loop databases stay the production mechanism.
import unreal as u
PP='/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'
bp=u.load_asset(PP); cdo=u.get_default_object(bp.generated_class()); cdo.set_editor_property('GR_SteadyEnable',True)
u.BlueprintEditorLibrary.compile_blueprint(bp); assert u.EditorAssetLibrary.save_loaded_asset(bp,False); print('DEFAULT steadyEnable',cdo.get_editor_property('GR_SteadyEnable')); print('DONE')
