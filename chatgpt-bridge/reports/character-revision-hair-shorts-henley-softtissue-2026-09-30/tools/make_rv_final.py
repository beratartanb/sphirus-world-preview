"""Final evidence capture requests for the character revision. usage: python make_rv_final.py <set> <prefix>
sets: final (views + close-ups) | deform | gameplay | lods | neck (dynamic neckline, chest-tracking cameras) | clay (soft tissue,
body only) | hairseq (hair views per pose)"""
import json, sys, pathlib, math
R = pathlib.Path(__file__).resolve().parents[2]; E = R/'Saved/Codex/CharacterShoulderFix_20260928/EquivalenceFix_20260929'; RV = R/'Saved/Codex/CharacterRevision_20260930'; O = RV/'captures'
def src(name):
    d = json.loads((E/f'{name}_front.json').read_text()); return {'animation': d.get('animation'), 'time': d.get('time', 0)}
POSES = {'neutral': {'animation': None, 'time': 0}}
for p in ['armsfwd', 'backext', 'crouch', 'elbow', 'hipflex', 'squat']: POSES[p] = src('br_dfm_'+p)
for p, s in [('idle', 'br_reg9_idle'), ('walk', 'br_reg9_walk'), ('jog', 'br_reg9_jog'), ('sprint', 'br_reg9_sprint'), ('jump', 'br_reg9_jump'), ('elev90', 'br_v9_elev_90'), ('elev120', 'br_v9_elev_120'),
             ('elev150', 'br_v9_elev_150'), ('elev165', 'br_v9_elev_165'), ('elev180', 'br_v9_elev_180'), ('forward90', 'br_v9_forward90')]: POSES[p] = src(s)
PL = json.loads((RV/'rv_poselib.json').read_text())
for n, t in PL['times'].items(): POSES['pl_'+n] = {'animation': PL['asset'].split('.')[0], 'time': t}
full = dict(camera_z=90, fov=11.5); V3 = ['front', 'side', 'rear3q']; V5 = ['front', 'side', 'back', 'front3q', 'rear3q']
which, PFX = sys.argv[1], sys.argv[2]; MEASURE = (len(sys.argv) > 3 and sys.argv[3] == 'measure')
def spine5(pose):
    f = O/f'b0_bodyrev_{pose}_front.json'
    if not f.exists(): return None
    return json.loads(f.read_text())['bone_transforms']['Body']['spine_05']['translation']
def bone(pose, n):
    f = O/f'b0_bodyrev_{pose}_front.json'
    if not f.exists(): return None
    return json.loads(f.read_text())['bone_transforms']['Body'][n]['translation']
S = []
if which == 'final':
    S += [dict(name=f'{PFX}_final', view=v, garments=True, materials='real', **full) for v in V5]
    HEAD = {'front': ([0, 125, 159, -90, 0], 15), 'side': ([125, 3, 159, 180, 0], 15), 'back': ([0, -118, 159, 90, 0], 15), 'front3q': ([-88, 90, 159, -45, 0], 15), 'rear3q': ([86, -84, 159, 135, 0], 15), 'side_r': ([-125, 3, 159, 0, 0], 15)}
    S += [dict(name=f'{PFX}_head_{k}', view='custom', cam=c, fov=f, garments=True, materials='real') for k, (c, f) in HEAD.items()]
    CU = {'neckline': ([0, 130, 132, -90, -4], 11), 'clavicle_chest': ([0, 130, 137, -90, -3], 10), 'henley_chest': ([-70, 130, 126, -62, -3], 13), 'waist_hem': ([0, 150, 100, -90, -2], 13),
          'waistband_drawstring': ([0, 130, 102, -90, -2], 10), 'side_hip': ([170, 0, 88, 180, -2], 14), 'seat': ([0, -160, 82, 90, -2], 14), 'seat_3q': ([110, -120, 82, 133, -2], 14),
          'crotch': ([0, 160, 74, -90, -3], 13), 'short_hem': ([0, 160, 64, -90, -2], 14), 'thigh_opening': ([-110, 120, 66, -47, -2], 14), 'foot_ankle': ([-70, 80, 10, -48, -4], 12),
          'shoulder_armpit': ([-60, 130, 132, -65, -6], 12), 'sleeve_elbow': ([100, 110, 118, -135, -5], 14), 'back_waist': ([0, -150, 98, 90, -2], 13), 'hand': ([105, 95, 99, -128, -6], 9)}
    S += [dict(name=f'{PFX}_cu_'+k, view='custom', cam=c, fov=f, garments=True, materials='real') for k, (c, f) in CU.items()]
    S += [dict(name=f'{PFX}_clay', view=v, garments=True, hair=False, materials='clay', **full) for v in ['front', 'rear3q']]
elif which == 'deform':
    for p in ['neutral', 'armsfwd', 'elev90', 'elev120', 'elev150', 'elev165', 'elev180', 'pl_twist_l', 'pl_twist_r', 'elbow', 'backext', 'pl_bend30', 'pl_bend45', 'pl_bend60', 'pl_bend90',
              'crouch', 'squat', 'hipflex', 'pl_highknee_l', 'pl_stride']:
        S += [dict(name=f'{PFX}_dfm_{p}', view=v, garments=True, materials='real', measure=(v == 'front'), **POSES[p], **full) for v in V3]
elif which == 'gameplay':
    for p in ['idle', 'walk', 'jog', 'sprint', 'jump', 'crouch']:
        S += [dict(name=f'{PFX}_gp_{p}', view=v, garments=True, materials='real', measure=(v == 'front'), track=True, **POSES[p], **full) for v in V3]
        S += [dict(name=f'{PFX}_gpcam_{p}', view='custom', cam=[-230, 330, 150, -55, -8], fov=40, garments=True, materials='real', track=True, **POSES[p])]
elif which == 'lods':
    for L in (0, 1, 2):
        for p in ['neutral', 'walk', 'squat', 'elev180', 'pl_bend60']:
            S += [dict(name=f'{PFX}_lod{L}_{p}', view=v, garments=True, materials='real', lod=L, measure=(MEASURE and v == 'front' and L > 0), **POSES[p], **full) for v in ['front', 'rear3q']]
elif which in ('neck', 'clay'):
    garments = which == 'neck'
    ST = sorted(json.loads((RV/'morph_rv_softtissue.json').read_text())['Body'].keys())
    for p in ['neutral', 'pl_bend20', 'pl_bend30', 'pl_bend45', 'pl_bend60', 'pl_bend90', 'armsfwd', 'elev180', 'pl_twist_l', 'pl_twist_r', 'squat', 'hipflex']:
      for NP, mz in ([(PFX, [])] if garments else [(PFX+'c', []), (PFX+'cb', ST)]):   # clay: AFTER (c) and BEFORE (cb, soft-tissue morphs zeroed) from the same cameras
        s5 = spine5(p); base = dict(garments=garments, hair=False, materials='real' if garments else 'clay', morph_zero=mz, **POSES[p])
        S += [dict(name=f'{NP}_{p}', view=v, **base, **full) for v in (['front', 'side', 'front3q'] if garments else ['front', 'side', 'front3q', 'rear3q'])]
        if s5:   # chest-tracking close-ups: aim a little below / in front of spine_05 (the upper chest in that pose)
            x, y, z = s5; t = [x, y+8.0, z-6.0]
            for k, (dx, dy, dz, yaw) in {'chest_front': (0, 120, -10, -90), 'chest_side': (120, 0, -4, 180), 'chest_front3q': (-85, 85, -8, -45)}.items():
                cam = [t[0]+dx, t[1]+dy, t[2]-dz, yaw, math.degrees(math.atan2(dz, math.hypot(dx, dy)))]
                S.append(dict(name=f'{NP}_{p}_{k}', view='custom', cam=cam, fov=16, **base))
        pv = bone(p, 'pelvis')
        if pv and not garments:   # glute / abdomen / thigh close-ups tracking the pelvis
            x, y, z = pv
            for k, (dx, dy, dz, yaw) in {'hip_side': (130, 0, 0, 180), 'hip_rear3q': (92, -92, 0, 135), 'hip_front3q': (-92, 92, 0, -45)}.items():
                S.append(dict(name=f'{NP}_{p}_{k}', view='custom', cam=[x+dx, y+dy, z-6, yaw, 0], fov=20, **base))
elif which == 'hairseq':
    HC = {'front3q': ([-88, 90, 159, -45, 0], 18), 'rear3q': ([86, -84, 159, 135, 0], 18), 'side': ([125, 3, 159, 180, 0], 18)}
    for p in ['idle', 'walk', 'jog', 'sprint', 'crouch', 'jump', 'pl_twist_l', 'pl_bend45']:
        S += [dict(name=f'{PFX}_{p}_{k}', view='custom', cam=c, fov=f, garments=True, materials='real', **POSES[p]) for k, (c, f) in HC.items()]
(O/'capture_request.json').write_text(json.dumps({'label': f'{PFX}_{which}', 'cases': S}, indent=1)); print(which, len(S), 'cases')
