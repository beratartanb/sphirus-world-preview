"""Write capture_request.json for the outfit QA harness. Pose sources = the validated BodyRealism captures
(same animations/times as the BR deformation boards br_dfm_* and regression br_reg9_*).
usage: python make_of_request.py <set>   sets: neutral | closeups | deform | gameplay | lods | all"""
import json, sys, pathlib
R = pathlib.Path(__file__).resolve().parents[2]; E = R/'Saved/Codex/CharacterShoulderFix_20260928/EquivalenceFix_20260929'; O = R/'Saved/Codex/OutfitHome_20260929/captures'; O.mkdir(parents=True, exist_ok=True)
def src(name):
    d = json.loads((E/f'{name}_front.json').read_text()); return {'animation': d.get('animation'), 'time': d.get('time', 0)}
POSES = {'neutral': {'animation': None, 'time': 0}}
for p in ['armsfwd', 'backext', 'crouch', 'elbow', 'elev150', 'elev180', 'hipflex', 'squat', 'twist']: POSES[p] = src('br_dfm_'+p)
for p, s in [('idle', 'br_reg9_idle'), ('walk', 'br_reg9_walk'), ('jog', 'br_reg9_jog'), ('sprint', 'br_reg9_sprint'), ('jump', 'br_reg9_jump'), ('elev165', 'br_v9_elev_165'), ('internal90', 'br_v9_internal90'), ('external90', 'br_v9_external90')]: POSES[p] = src(s)
sets = {}
full = dict(camera_z=90, fov=11.5)
sets['neutral'] = [dict(name='of_neutral', view=v, garments=True, materials='real', measure=(v == 'front'), **full) for v in ['front', 'side', 'back', 'front3q', 'rear3q']] + \
                  [dict(name='of_neutral_body', view=v, garments=False, materials='real', **full) for v in ['front', 'side']]
CU = {'neckline': ([0, 130, 138, -90, -4], 11), 'chest': ([0, 150, 126, -90, -3], 13), 'shoulder_armpit': ([60, 130, 132, -115, -6], 12), 'waist_tuck': ([0, 150, 100, -90, -2], 13),
      'waistband_drawstring': ([0, 130, 101, -90, -2], 10), 'crotch_hip': ([0, 160, 84, -90, -2], 14), 'knee_folds': ([0, 160, 50, -90, -2], 14), 'hem': ([0, 170, 12, -90, -4], 14),
      'back_waist': ([0, -150, 98, 90, -2], 13), 'sleeve_elbow': ([100, 110, 118, -135, -5], 14), 'seat': ([0, -160, 84, 90, -2], 14), 'side_hip': ([170, 0, 92, 180, -2], 14)}
sets['closeups'] = [dict(name='of_cu_'+k, view='custom', cam=c, fov=f, garments=True, materials='real') for k, (c, f) in CU.items()]
DEF = ['neutral', 'armsfwd', 'elev150', 'elev165', 'elev180', 'twist', 'crouch', 'squat', 'elbow', 'hipflex', 'backext', 'internal90', 'external90']
sets['deform'] = [dict(name='of_dfm_'+p, view=v, garments=True, materials='real', measure=(v == 'front'), bones=(v == 'front'), **POSES[p], **full) for p in DEF for v in ['front', 'side', 'rear3q']]
sets['gameplay'] = [dict(name='of_gp_'+p, view=v, garments=True, materials='real', measure=(v == 'front'), **POSES[p], **full) for p in ['idle', 'walk', 'jog', 'sprint', 'jump'] for v in ['front', 'side', 'rear3q']]
sets['lods'] = [dict(name=f'of_lod{L}_'+p, view='front', garments=True, materials='real', lod=L, measure=True, **POSES[p], **full) for L in [1, 2] for p in ['neutral', 'walk', 'squat', 'elev180']]
sets['clay'] = [dict(name='of_clay_'+p, view=v, garments=True, materials='clay', **POSES[p], **full) for p in ['neutral', 'elev180', 'squat'] for v in ['front', 'rear3q']]
sets['shc'] = [dict(name='of_dfm_'+p, view=v, garments=True, materials='real', measure=(v == 'front'), **POSES[p], **full) for p in ['elev150', 'elev165', 'elev180', 'armsfwd', 'hipflex'] for v in ['front', 'side', 'rear3q']]
sets['all'] = [c for k in ['neutral', 'closeups', 'deform', 'gameplay', 'lods', 'clay'] for c in sets[k]]
which = sys.argv[1] if len(sys.argv) > 1 else 'neutral'
req = {'label': 'of_'+which, 'cases': sets[which]}
(O/'capture_request.json').write_text(json.dumps(req, indent=1)); print(which, len(req['cases']), 'cases'); print(json.dumps(POSES, indent=1))
