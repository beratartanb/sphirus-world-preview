# probe_state.py (read-only, editor): saved defaults of the active player and its locomotion ABP -> Saved/UE59Work/probe/state_<tag>.txt
import unreal as u, builtins
o = []
def cdo(path):
    c = u.load_object(None, path); return c.get_default_object() if c else None
P = cdo('/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player.BP_HybridA_Player_C')
A = cdo('/Game/Sphirus/Player/GASP/ABP_Sph_GASP.ABP_Sph_GASP_C')
for n in ('WalkSpeeds', 'RunSpeeds', 'SprintSpeeds', 'CrouchSpeeds'):
    try: o.append('PAWN %s = %s' % (n, P.get_editor_property(n)))
    except Exception as e: o.append('PAWN %s ?' % n)
try:
    cm = P.get_editor_property('character_movement')
    for n in ('max_walk_speed', 'max_acceleration', 'braking_deceleration_walking', 'ground_friction', 'braking_friction', 'use_separate_braking_friction', 'walkable_floor_angle', 'max_step_height', 'perch_radius_threshold', 'rotation_rate', 'orient_rotation_to_movement', 'maintain_horizontal_ground_velocity'):
        try: o.append('CMC %s = %s' % (n, cm.get_editor_property(n)))
        except Exception: pass
except Exception as e: o.append('CMC ? %s' % e)
for n in ('SphRelaxed', 'SphCM', 'PlantSettings_Default', 'PlantSettings_Stops', 'plant_settings_default', 'plant_settings_stops', 'Gait'):
    try:
        v = A.get_editor_property(n); o.append('ABP %s = %s' % (n, str(v)[:400]))
    except Exception: pass
for n in ('CM_Keys', 'CM_Vals', 'cm_keys', 'cm_vals'):
    try:
        v = A.get_editor_property(n); o.append('ABP %s (%d)' % (n, len(v)))
        for x in v: o.append('    %s' % (x.get_name() if x else None))
    except Exception: pass
mo = None
try:
    for c in u.SubobjectDataSubsystem and []: pass
except Exception: pass
M = cdo('/Game/Sphirus/Player/Motion/AC_Sph_Motion.AC_Sph_Motion_C')
for n in ('Enabled', 'EffortEnabled', 'BodyOn', 'TurnCapOn', 'PhysBrake', 'BrakeDecelLow', 'BrakeDecelHigh', 'RevOn', 'IdleEnabled'):
    try: o.append('MOTION %s = %s' % (n, M.get_editor_property(n)))
    except Exception: pass
req = open(u.Paths.project_dir() + 'Saved/UE59Work/profile_req.json').read()
o.append('PROFILE_REQ ' + req)
tag = getattr(builtins, 'PS_TAG', 'x')
open(u.Paths.project_dir() + 'Saved/UE59Work/probe/state_%s.txt' % tag, 'w', encoding='utf8').write('\n'.join(o)); print('STATE', tag, len(o))
