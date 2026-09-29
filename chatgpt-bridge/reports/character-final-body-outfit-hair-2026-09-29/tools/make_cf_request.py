"""Write capture_request.json for the CharacterFinal QA harness. Pose sources = the validated BodyRealism captures
(same animations/times as the BR deformation boards br_dfm_* and regression br_reg9_*).
usage: python make_cf_request.py <set> [prefix]   sets: audit | body_dfm | neutral | closeups | deform | gameplay | lods | clay | shc | hair | final"""
import json, sys, pathlib
R = pathlib.Path(__file__).resolve().parents[2]; E = R/'Saved/Codex/CharacterShoulderFix_20260928/EquivalenceFix_20260929'; O = R/'Saved/Codex/CharacterFinal_20260929/captures'; O.mkdir(parents=True, exist_ok=True)
def src(name):
    d = json.loads((E/f'{name}_front.json').read_text()); return {'animation': d.get('animation'), 'time': d.get('time', 0)}
POSES = {'neutral': {'animation': None, 'time': 0}}
for p in ['armsfwd', 'backext', 'crouch', 'elbow', 'elev150', 'elev180', 'hipflex', 'squat', 'twist']: POSES[p] = src('br_dfm_'+p)
for p, s in [('idle', 'br_reg9_idle'), ('walk', 'br_reg9_walk'), ('jog', 'br_reg9_jog'), ('sprint', 'br_reg9_sprint'), ('jump', 'br_reg9_jump'), ('elev165', 'br_v9_elev_165'), ('elev90', 'br_v9_elev_90'), ('elev120', 'br_v9_elev_120'), ('internal90', 'br_v9_internal90'), ('external90', 'br_v9_external90'), ('forward90', 'br_v9_forward90')]: POSES[p] = src(s)
which = sys.argv[1] if len(sys.argv) > 1 else 'audit'; PFX = sys.argv[2] if len(sys.argv) > 2 else 'cf'
full = dict(camera_z=90, fov=11.5); VIEWS5 = ['front', 'side', 'back', 'front3q', 'rear3q']
# body close-ups (custom cams x,y,z,yaw,pitch + fov); the body is centred at the origin, +y = front, +x = character left
BODYCU = {'chest_ribcage': ([0, 150, 126, -90, -3], 13), 'chest_3q': ([-95, 120, 126, -52, -3], 13), 'abdomen_waist': ([0, 150, 103, -90, -2], 13), 'waist_side': ([170, 0, 103, 180, -2], 13),
          'pelvis_hip': ([0, 160, 88, -90, -2], 14), 'hip_3q': ([-110, 120, 88, -47, -2], 14), 'glutes_rear': ([0, -160, 84, 90, -2], 14), 'glutes_3q': ([110, -120, 84, 133, -2], 14),
          'thigh_knee': ([0, 160, 58, -90, -2], 14), 'knee_side': ([170, 0, 48, 180, 0], 12), 'calf_ankle': ([0, -170, 22, 90, -4], 14), 'calf_side': ([170, 0, 24, 180, -3], 12),
          'feet_front': ([0, 110, 9, -90, -3], 12), 'feet_side': ([110, 8, 8, 180, -2], 12), 'feet_3q': ([-70, 80, 10, -48, -4], 12), 'feet_medial': ([-40, 95, 8, -68, -3], 10), 'shoulder_arm': ([-100, 110, 128, -48, -4], 14), 'arm_side': ([170, 0, 118, 180, -2], 13),
          'hand_l': ([105, 95, 99, -128, -6], 9), 'hand_dorsal': ([70, 110, 118, -118, -20], 9), 'back_upper': ([0, -150, 126, 90, -2], 13), 'back_lower': ([0, -150, 100, 90, -2], 13), 'neck_clavicle': ([0, 130, 140, -90, -4], 11)}
sets = {}
# PHASE A / C: body audit in clay, body only (no garments, no hair), neutral + grazing light
sets['audit'] = [dict(name=f'{PFX}_body', view=v, garments=False, hair=False, materials='clay', **full) for v in VIEWS5] + \
                [dict(name=f'{PFX}_bodyg', view=v, garments=False, hair=False, materials='clay', light='grazing', **full) for v in ['front', 'back', 'side']] + \
                [dict(name=f'{PFX}_cu_'+k, view='custom', cam=c, fov=f, garments=False, hair=False, materials='clay') for k, (c, f) in BODYCU.items()] + \
                [dict(name=f'{PFX}_cug_'+k, view='custom', cam=c, fov=f, garments=False, hair=False, materials='clay', light='grazing') for k, (c, f) in BODYCU.items() if k in ('chest_3q', 'abdomen_waist', 'glutes_3q', 'thigh_knee', 'feet_3q', 'back_upper')] + \
                [dict(name=f'{PFX}_skin', view=v, garments=False, hair=False, materials='real', **full) for v in ['front', 'back']] + \
                [dict(name=f'{PFX}_skincu_'+k, view='custom', cam=c, fov=f, garments=False, hair=False, materials='real') for k, (c, f) in BODYCU.items() if k in ('chest_3q', 'back_upper', 'feet_3q', 'knee_side', 'hand_l')]
DEFB = ['neutral', 'armsfwd', 'elev90', 'elev120', 'elev150', 'elev165', 'elev180', 'twist', 'hipflex', 'backext', 'crouch', 'squat', 'sprint', 'elbow', 'forward90']
sets['body_dfm'] = [dict(name=f'{PFX}_bdfm_'+p, view=v, garments=False, hair=False, materials='clay', measure=(v == 'front'), **POSES[p], **full) for p in DEFB for v in ['front', 'side', 'rear3q']]
# outfit / final sets (garments + hair visible)
sets['neutral'] = [dict(name=f'{PFX}_neutral', view=v, garments=True, materials='real', measure=(v == 'front'), **full) for v in VIEWS5]
CU = {'hair_face': ([0, 120, 152, -90, -4], 10), 'hair_3q': ([-90, 90, 152, -45, -4], 10), 'hair_rear': ([0, -120, 152, 90, -4], 10), 'hair_side': ([120, 0, 152, 180, -4], 10),
      'neckline': ([0, 130, 132, -90, -4], 11), 'clavicle_chest': ([0, 130, 137, -90, -3], 10), 'henley_chest': ([-70, 130, 126, -62, -3], 13), 'waist_hem': ([0, 150, 100, -90, -2], 13), 'waist_hem_side': ([170, 0, 100, 180, -2], 13),
      'waistband_drawstring': ([0, 130, 102, -90, -2], 10), 'side_hip': ([170, 0, 88, 180, -2], 14), 'seat': ([0, -160, 82, 90, -2], 14), 'seat_3q': ([110, -120, 82, 133, -2], 14), 'crotch': ([0, 160, 74, -90, -3], 13),
      'short_hem': ([0, 160, 64, -90, -2], 14), 'thigh_opening': ([-110, 120, 66, -47, -2], 14), 'foot_ankle': ([-80, 90, 14, -48, -12], 12), 'shoulder_armpit': ([-60, 130, 132, -65, -6], 12), 'sleeve_elbow': ([100, 110, 118, -135, -5], 14), 'back_waist': ([0, -150, 98, 90, -2], 13)}
sets['closeups'] = [dict(name=f'{PFX}_cu_'+k, view='custom', cam=c, fov=f, garments=True, materials='real') for k, (c, f) in CU.items()]
DEF = ['neutral', 'armsfwd', 'elev90', 'elev120', 'elev150', 'elev165', 'elev180', 'twist', 'crouch', 'squat', 'elbow', 'hipflex', 'backext', 'internal90', 'external90']
sets['deform'] = [dict(name=f'{PFX}_dfm_'+p, view=v, garments=True, materials='real', measure=(v == 'front'), bones=(v == 'front'), **POSES[p], **full) for p in DEF for v in ['front', 'side', 'rear3q']]
sets['gameplay'] = [dict(name=f'{PFX}_gp_'+p, view=v, garments=True, materials='real', measure=(v == 'front'), **POSES[p], **full) for p in ['idle', 'walk', 'jog', 'sprint', 'crouch', 'jump'] for v in ['front', 'side', 'rear3q']] + \
                   [dict(name=f'{PFX}_gpcam_'+p, view='custom', cam=[-230, 330, 150, -55, -8], fov=40, garments=True, materials='real', **POSES[p]) for p in ['idle', 'walk', 'jog', 'sprint', 'crouch', 'jump']]
sets['lods'] = [dict(name=f'{PFX}_lod{L}_'+p, view='front', garments=True, materials='real', lod=L, measure=True, **POSES[p], **full) for L in [1, 2] for p in ['neutral', 'walk', 'squat', 'elev180']] + \
               [dict(name=f'{PFX}_lod{L}_'+p, view='rear3q', garments=True, materials='real', lod=L, **POSES[p], **full) for L in [1, 2] for p in ['neutral', 'squat']]
sets['clay'] = [dict(name=f'{PFX}_clay_'+p, view=v, garments=True, materials='clay', **POSES[p], **full) for p in ['neutral', 'elev180', 'squat'] for v in ['front', 'rear3q']]
sets['shc'] = [dict(name=f'{PFX}_dfm_'+p, view=v, garments=True, materials='real', measure=(v == 'front'), **POSES[p], **full) for p in ['elev90', 'elev120', 'elev150', 'elev165', 'elev180', 'armsfwd', 'hipflex', 'squat'] for v in ['front', 'side', 'rear3q']]
sets['hair'] = [dict(name=f'{PFX}_hair_'+p, view=v, garments=True, materials='real', **POSES[p], **full) for p in ['neutral', 'idle', 'walk', 'sprint', 'crouch', 'twist'] for v in ['front', 'side', 'rear3q']] + \
               [dict(name=f'{PFX}_haircu_'+k, view='custom', cam=c, fov=f, garments=True, materials='real') for k, (c, f) in CU.items() if k.startswith('hair')]
sets['hairalt'] = [dict(name=f'{PFX}_hairalt', view=v, garments=True, materials='real', **full) for v in ['front', 'side', 'rear3q']] + [dict(name=f'{PFX}_hairaltcu', view='custom', cam=CU['hair_3q'][0], fov=CU['hair_3q'][1], garments=True, materials='real')]
sets['final'] = [c for k in ['neutral', 'closeups', 'deform', 'gameplay', 'lods', 'clay', 'hair'] for c in sets[k]]
req = {'label': f'{PFX}_{which}', 'cases': sets[which]}
(O/'capture_request.json').write_text(json.dumps(req, indent=1)); print(which, len(req['cases']), 'cases')
