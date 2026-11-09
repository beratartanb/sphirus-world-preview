# cm_phys1.py (write): capsule friction contract. Measured (R_rev4, P_phys_before): on W->S the velocity flips through zero
# in 0.13 s and on release the capsule stops in 0.13-0.17 s at every gait, because CharacterMovement GroundFriction 8
# (x BrakingFrictionFactor 2) both redirects the velocity toward the new input in ~4 frames and brakes with ~16/s x speed.
# The stop/pivot clips decelerate over 0.4-1.2 s, so the search could never play them in phase (the body jumped between
# the idle-start-turn clips). Fix: braking friction separated and zero -> stops are governed by BrakingDeceleration only
# (650 cm/s2: walk 0.28 s / 25 cm, jog 0.46 s / 69 cm, run 0.77 s / 1.9 m); GroundFriction 8 -> 3 so a direction change
# redirects the velocity over ~0.4 s (a step) instead of 0.13 s.
import unreal as u
PP='/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'
bp=u.load_asset(PP); sds=u.get_engine_subsystem(u.SubobjectDataSubsystem); SB=u.SubobjectDataBlueprintFunctionLibrary; n=0
KEYS=('ground_friction','braking_friction','use_separate_braking_friction','braking_friction_factor','braking_deceleration_walking','max_acceleration')
for h in sds.k2_gather_subobject_data_for_blueprint(bp):
    o=SB.get_object(SB.get_data(h))
    if o and isinstance(o,u.CharacterMovementComponent):
        c=SB.get_object_for_blueprint(SB.get_data(h),bp)
        print('BEFORE',{k:str(c.get_editor_property(k)) for k in KEYS})
        c.set_editor_property('use_separate_braking_friction',True); c.set_editor_property('braking_friction',0.0); c.set_editor_property('ground_friction',3.0)
        print('AFTER',{k:str(c.get_editor_property(k)) for k in KEYS}); n+=1
assert n==1,n
u.BlueprintEditorLibrary.compile_blueprint(bp); assert u.EditorAssetLibrary.save_loaded_asset(bp,False); print('DONE')
