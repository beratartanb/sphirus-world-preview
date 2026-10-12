"""GD42 capture requests for the lookdev harness (Tools/CharacterLookdev_20260930/ue_lk_capture.py), garment-free body review.
BEFORE = the same mesh with the GD42_Body morph zeroed (morph_zero), AFTER = as authored. usage: python gd42_req.py <set> <prefix> <out_request.json>
sets: full   5 full-body views (front, side, back, front3q, rear3q) x clay (hair off) / real (hair on) x after / before
      close  body close-ups (chest, waist, hip, glute, thigh, knee, calf, back, shoulder) clay + real, after / before
      dfm    deformation poses (EquivalenceFix captures: arms forward, back extension, crouch, elbow, elevation 150 / 180, hip flexion,
             squat, twist) clay, front3q + rear3q, after / before"""
import json, sys, pathlib
which, P, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
R = pathlib.Path(__file__).resolve().parents[4]; E = R/'Saved/Codex/CharacterShoulderFix_20260928/EquivalenceFix_20260929'
S = []
def add(name, **k):
    S.append(dict(name=f'{P}_{name}', garments=False, materials=k.pop('materials', 'clay'), light=k.pop('light', 'studio'), animation=k.pop('animation', None), time=k.pop('time', 0), **k))
FULL = ['front', 'side', 'back', 'front3q', 'rear3q']
if which == 'full':
    for v in FULL:
        for mat, hair in (('clay', False), ('real', True)):
            add(f'{mat}_{v}_after', view=v, materials=mat, hair=hair)
            add(f'{mat}_{v}_before', view=v, materials=mat, hair=hair, morph_zero=['GD42_Body'])
if which == 'close':
    CU = {'chest_front': ([0, 120, 126, -90, -2], 20), 'chest_side': ([130, 20, 125, 188, -2], 18), 'waist_front3q': ([-100, 100, 100, -45, -2], 22),
          'hip_side': ([150, 0, 88, 180, -2], 22), 'glute_rear': ([0, -150, 84, 90, -2], 22), 'glute_rear3q': ([105, -105, 86, 135, -2], 22),
          'back_upper': ([0, -140, 120, 90, -3], 22), 'thigh_knee_front3q': ([-70, 110, 55, -54, -2], 22), 'calf_rear3q': ([70, -95, 35, 125, -2], 20),
          'shoulder_arm_front3q': ([-80, 90, 128, -45, -3], 18), 'chest_3q': ([-85, 85, 127, -45, -2], 17), 'chest_low3q': ([-85, 85, 110, -45, 10], 17)}
    for k, (c, f) in CU.items():
        for mat in ('clay', 'real'):
            add(f'cu_{mat}_{k}_after', view='custom', cam=c, fov=f, materials=mat, hair=False)
            add(f'cu_{mat}_{k}_before', view='custom', cam=c, fov=f, materials=mat, hair=False, morph_zero=['GD42_Body'])
if which == 'dfm':
    for p in ['armsfwd', 'backext', 'crouch', 'elbow', 'elev150', 'elev180', 'hipflex', 'squat', 'twist']:
        d = json.loads((E/f'br_dfm_{p}_front.json').read_text()); an = {'animation': d.get('animation'), 'time': d.get('time', 0)}
        for v in ('front3q', 'rear3q'):
            add(f'dfm_{p}_{v}_after', view=v, hair=False, camera_z=90, fov=11.5, **an)
            add(f'dfm_{p}_{v}_before', view=v, hair=False, camera_z=90, fov=11.5, morph_zero=['GD42_Body'], **an)
pathlib.Path(OUT).write_text(json.dumps({'label': f'{P}_{which}', 'cases': S}, indent=1)); print('GD42REQ', which, len(S))
