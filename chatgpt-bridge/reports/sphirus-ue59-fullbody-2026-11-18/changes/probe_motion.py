# probe_motion.py (read-only, PIE): live AC_Sph_Motion and body-layer switches on the player -> Saved/UE59Work/probe/motion_live.txt
import unreal as u
W = u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world(); P = u.GameplayStatics.get_player_controller(W, 0).get_controlled_pawn()
o = []
for c in P.get_components_by_class(u.ActorComponent):
    if c.get_name() == 'SphMotion':
        for n in ('Enabled', 'EffortEnabled', 'BodyOn', 'EffLeanDeg', 'EffLean', 'SettleDeg', 'LeadMax', 'TurnCapOn', 'PhysBrake', 'RevOn', 'IdleEnabled', 'GaitUpAcc', 'GaitUpMin', 'LatLow', 'LatHigh', 'CapMin'):
            try: o.append('SphMotion.%s = %s' % (n, c.get_editor_property(n)))
            except Exception as e: o.append('SphMotion.%s ?' % n)
cm = P.get_movement_component()
for n in ('use_flat_base_for_floor_checks', 'max_walk_speed', 'max_acceleration', 'braking_deceleration_walking', 'ground_friction', 'rotation_rate'):
    try: o.append('CMC.%s = %s' % (n, cm.get_editor_property(n)))
    except Exception: pass
vis = [c for c in P.get_components_by_class(u.SkeletalMeshComponent) if c.get_name() == 'Manny'][0]; va = vis.get_anim_instance()
o.append('BodyABP %s' % va.get_class().get_name())
for n in ('eff_lean', 'set_x', 'chest_lead', 'pitch_axis', 'h_level', 'h_level_max'):
    try: o.append('Body.%s = %s' % (n, va.get_editor_property(n)))
    except Exception: pass
open(u.Paths.project_dir() + 'Saved/UE59Work/probe/motion_live.txt', 'w', encoding='utf8').write('\n'.join(o)); print('MOTIONLIVE', len(o))
